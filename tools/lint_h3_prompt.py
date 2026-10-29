#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H3 Ref2VA 六段式提示词体检器（stdlib only）。

用法：
    python lint_h3_prompt.py prompt.txt            # 体检一个文件
    python lint_h3_prompt.py prompt.txt --budget 6000 7000
    python lint_h3_prompt.py prompt.txt --json

退出码：0 全通过；1 有 FAIL；2 参数/文件错误。

检查项（全部来自 V8 规范集；原始文档不入库）：
  C1 六段齐全且顺序固定（HARD_SCHEMA）
  C2 整串字符数落在 6000–7000（含标题/标点/空格/换行，LF 计 1）
  C3 中文只允许出现在 <d>...</d> 内，且 <d> 必须带 [Chinese] 前缀
  C4 <d> 内不得夹英文说明句；<d> 外不得有中文标点
  C5 summary 必须以 [任务类型] 开头，类型名在六种合法值内
  C6 正文不得混入内部编号与内部状态（G0-/CG0-/ADN-/P-/QC_/repair_variable 等）
  C7 retention_analysis 不得出现 Sx 编号，不得复述整段台词
  C8 不得出现除六段以外的自有段落名（第七段检测）
"""
import argparse, io, json, re, sys

SIX = [
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
]
TASK_TYPES = [
    "reference generation",
    "keyframe completion",
    "video editing",
    "video continuation",
    "audio reuse",
    "audio reference",
]
CJK = re.compile(r"[\u4e00-\u9fff]")
CJK_PUNCT = re.compile(r"[\u3000-\u303f\uff00-\uffef]")
D_TAG = re.compile(r"<d>(.*?)</d>", re.S)
INTERNAL = re.compile(
    r"\b(?:G[0-9]{1,2}|CG0[1-8]|P1[0-4]|P[0-9]|ADN-[0-9]|ACT-[0-9]{2,}|SB-P[0-2]-[0-9]{3}|SB-BLOCK-[0-9]{3})\b"
    r"|QC_PASSED|REPAIR_REQUIRED|repair_variable|propagated_fields|scene_routing|shot_card",
    re.I,
)
SX = re.compile(r"\bS[0-9]{1,2}\b")


def strip_d(text):
    return D_TAG.sub(" ", text)


def read_text(path):
    with io.open(path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8")
    # 规范：换行按 LF 计 1，CRLF/CR 先归一化再计数
    return text.replace("\r\n", "\n").replace("\r", "\n")


def section_positions(text):
    """Return {name: (start, end)} for the six canonical sections."""
    hits = []
    for name in SIX:
        m = re.search(r"(?m)^\s*" + re.escape(name) + r"\s*$", text)
        if m:
            hits.append((m.start(), name))
    hits.sort()
    order = [n for _, n in hits]
    pos = {}
    for idx, (start, name) in enumerate(hits):
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(text)
        pos[name] = (start, end)
    return pos, order


def lint(text, budget_min=6000, budget_max=7000):
    fails, warns, info = [], [], {}

    # C1
    pos, order = section_positions(text)
    missing = [s for s in SIX if s not in pos]
    if missing:
        fails.append("C1 缺段: " + ", ".join(missing))
    if order and order != [s for s in SIX if s in pos]:
        fails.append("C1 段序错: " + " → ".join(order))
    info["sections_found"] = len(pos)

    # C2
    n = len(text)
    info["chars"] = n
    if n < budget_min or n > budget_max:
        fails.append("C2 字符数 %d 不在 %d–%d" % (n, budget_min, budget_max))

    # C3 / C4
    outside = strip_d(text)
    cjk_outside = CJK.findall(outside)
    if cjk_outside:
        snippet = "".join(cjk_outside[:12])
        fails.append("C3 <d> 外出现中文 %d 处，例如：%s" % (len(cjk_outside), snippet))
    punct_outside = CJK_PUNCT.findall(outside)
    if punct_outside:
        fails.append("C4 <d> 外出现中文标点 %d 处，例如：%s" % (len(punct_outside), "".join(punct_outside[:8])))
    for body in D_TAG.findall(text):
        if "[Chinese]" not in body:
            fails.append("C3 <d> 缺 [Chinese] 前缀：%s" % body[:24])
        body_wo_prefix = re.sub(r"^\s*\[Chinese\]", "", body)
        if re.search(r"[A-Za-z]{3,}", body_wo_prefix):
            fails.append("C4 <d> 内混入英文说明：%s" % body_wo_prefix[:32])

    # C5
    if "summary" in pos:
        s, e = pos["summary"]
        block = text[s:e]
        m = re.search(r"\[([^\]]+)\]", block)
        if not m:
            fails.append("C5 summary 缺 [任务类型] 前缀")
        else:
            t = m.group(1).strip().lower()
            parts = [p.strip() for p in t.split("+")]
            bad = [p for p in parts if p not in TASK_TYPES]
            if bad:
                fails.append("C5 非法任务类型: " + ", ".join(bad))

    # C6
    hits = INTERNAL.findall(text)
    if hits:
        uniq = sorted(set(h if isinstance(h, str) else h[0] for h in hits))
        fails.append("C6 正文混入内部编号/状态 %d 处：%s" % (len(hits), ", ".join(uniq[:10])))

    # C7
    if "retention_analysis" in pos:
        s, e = pos["retention_analysis"]
        block = strip_d(text[s:e])
        if SX.search(block):
            fails.append("C7 retention_analysis 里出现 Sx 编号")
        if D_TAG.search(text[s:e]):
            warns.append("C7 retention_analysis 里出现台词块，注意不要复述整段对白")

    # C8 第七段
    known = set(SIX)
    heads = re.findall(r"(?m)^\s*([a-z_]{3,})\s*$", text)
    extra = [h for h in heads if h not in known]
    if extra:
        fails.append("C8 出现六段之外的段落名（疑似第七段）: " + ", ".join(sorted(set(extra))[:6]))

    return fails, warns, info


def main():
    ap = argparse.ArgumentParser(description="H3 Ref2VA 六段式提示词体检器")
    ap.add_argument("path", help="提示词文本文件（UTF-8）")
    ap.add_argument("--budget", nargs=2, type=int, default=[6000, 7000], metavar=("MIN", "MAX"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        text = read_text(args.path)
    except OSError as ex:
        print("ERROR cannot read: %s" % ex, file=sys.stderr)
        return 2
    fails, warns, info = lint(text, args.budget[0], args.budget[1])
    report = {"path": args.path, "info": info, "fails": fails, "warns": warns,
              "status": "PASS" if not fails else "FAIL"}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("file:", args.path)
        print("chars:", info.get("chars"), "| sections:", info.get("sections_found"), "/6")
        print("status:", report["status"])
        for f in fails:
            print("  FAIL", f)
        for w in warns:
            print("  WARN", w)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())