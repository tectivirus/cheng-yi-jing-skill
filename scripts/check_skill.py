#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""仓库自检：技能文件结构、frontmatter、六段式、占位符。"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = ["SKILL.md", "work.md", "persona.md", "work_skill.md", "persona_skill.md"]
SIX = ["subject_definitions", "summary", "retention_analysis", "detailed_description",
       "overall_soundscape", "non_diegetic_music"]
fails = []

def rd(name):
    with open(os.path.join(ROOT, name), "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        fails.append(name + ": BOM")
    return raw.decode("utf-8")

for f in FILES:
    if not os.path.isfile(os.path.join(ROOT, f)):
        fails.append("missing " + f)
if fails:
    print("FAIL", fails)
    sys.exit(1)

skill = rd("SKILL.md")
m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill, re.S)
if not m:
    fails.append("SKILL.md: frontmatter 缺失")
else:
    fm = m.group(1)
    for k in ("name:", "description:", "user-invocable:"):
        if k not in fm:
            fails.append("frontmatter 缺 " + k)

for token in ("PART A", "PART B", "Layer 0", "Layer 1", "Layer 2", "Layer 3",
              "Layer 4", "Layer 5", "运行规则"):
    if token not in skill:
        fails.append("SKILL.md 缺 " + token)

for s in SIX:
    if s not in skill:
        fails.append("六段缺 " + s)

corpus = skill + rd("work.md") + rd("persona.md")
for bad in ("TODO", "XXX", "TBD", "【】", "{persona_content}", "{work_content}"):
    if bad in corpus:
        fails.append("占位符 " + bad)

if "程一镜" not in skill:
    fails.append("SKILL.md 未声明人格名")

print("files:", ", ".join(FILES))
print("six sections:", len(SIX), "ok" if not any("六段缺" in f for f in fails) else "fail")
print("checks:", "PASS" if not fails else "FAIL")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
