# 程一镜 · MiniMax H3 Ref2VA 短剧工业化分镜技能

[![validate](https://github.com/tectivirus/cheng-yi-jing-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/tectivirus/cheng-yi-jing-skill/actions/workflows/validate.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 把一部短剧剧本，压成能投喂、能验收、能返修、能追溯的**单镜任务**。

一个可直接加载到 AI Agent 的技能包：**工作方法（PART A）** + **工作人格（PART B）**。
面向 MiniMax H3 的 Ref2VA 参考生成模式：固定六段式英文提示词、Shot Card、八类微节点、G/CG 门禁、单主因返修。

一条 6000–7000 字符的提示词从这里出去，应该同时满足：**身份不漂、参考不被误当首帧、编号不乱、中文不越界、返修只动一个变量**。

---

## 快速上手

```bash
git clone https://github.com/tectivirus/cheng-yi-jing-skill.git
cd cheng-yi-jing-skill
./scripts/install.sh dsh          # 或 claude / codex
```

装完技能名 **`celebrity-cheng-yi-jing`**（默认路径 `~/.dsh/skills/celebrity-cheng-yi-jing`）。

| 场景 | 做法 |
|---|---|
| Windows | 用 Git Bash 跑 `install.sh` |
| 自定义目录 | `DSH_SKILLS_DIR=/path/to/skills ./scripts/install.sh dsh` |
| Claude Code | `./scripts/install.sh claude`（`CLAUDE_SKILLS_DIR` 可覆盖） |
| Codex | `./scripts/install.sh codex`（`CODEX_SKILLS_DIR` 可覆盖） |

装好后在会话里直接提需求即可，不需要记字段：

```
用程一镜，把第 7 集第 3 场拆成单镜，先出 Shot Card，我确认后再出提示词。
```

---

## 一分钟看懂它怎么干活

```text
剧本事实  →  Shot Card（15 字段）  →  八类微节点 + 九阶段时间轴
          →  六段式英文提示词（6000–7000 字符）
          →  tools/lint_h3_prompt.py（8 项确定性体检）
          →  G0–G20 / CG01–CG08 门禁  →  PASS / HOLD / BLOCKED
          →  单主因返修（一次只动一个变量）
```

六段固定顺序，封闭结构，不加第七段：

```text
subject_definitions
summary                 [任务类型] 开头，六种合法值之一
retention_analysis
detailed_description
overall_soundscape
non_diegetic_music
```

完整示例见 [examples/shot-card-01.md](examples/shot-card-01.md)。

---

## 出稿前先过机器

```bash
python tools/lint_h3_prompt.py fixtures/golden.txt        # PASS，6565 字符
python tools/lint_h3_prompt.py fixtures/bad-cjk.txt       # FAIL：<d> 外出现中文
python tools/lint_h3_prompt.py fixtures/bad-internal.txt  # FAIL：正文混入内部编号 + 第七段
python tools/lint_h3_prompt.py my_prompt.txt --json
```

体检器 8 项（退出码 0 通过 / 1 有问题 / 2 参数错误）：

| 项 | 检查什么 |
|---|---|
| C1 | 六段齐全且顺序固定（HARD_SCHEMA） |
| C2 | 整串 6000–7000 字符（LF 计 1，含标题标点空格） |
| C3 | 中文只出现在 `<d>[Chinese]…</d>` 内 |
| C4 | `<d>` 内不夹英文说明；`<d>` 外无中文标点 |
| C5 | `summary` 的 `[任务类型]` 在六种合法值内 |
| C6 | 正文无 G/CG/ADN/P/QC 等内部编号与内部状态 |
| C7 | `retention_analysis` 无 Sx、不复述整段台词 |
| C8 | 无六段之外的段落名（第七段） |

它只证明**格式与预算**，不证明**画面能用**——PASS 之后仍要按 §六 走生成前门禁。

---

## 它解决什么

| 翻车点 | 本技能的约束 |
|---|---|
| 每镜换脸 | 身份锚点绑定 Subject N + 资产版本，不许凭外观即兴 |
| 参考图被当首帧 | 任务类型写 reference generation；帧锚点另立 Picture N |
| 说话人编号乱套 | Sx 按全局首次发声分配，Subject 编号不等于 Sx |
| 提示词越写越散 | 六段固定顺序、不加第七段；整串 6000–7000 字符 |
| 中文混进正文 | 正文全英文，中文只允许出现在中文台词标签内 |
| 返修越修越烂 | 一次只动一个主变量，记 before/after，其余字段禁止漂移 |
| 门禁变成卡点 | PASS / HOLD / BLOCKED 三态，只挂受影响那一镜 |

---

## 结构

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 合成技能：PART A 工作能力 + PART B 人格 + 运行规则（**单文件即可用**） |
| `work.md` / `work_skill.md` | 方法与规范主体 |
| `persona.md` / `persona_skill.md` | 判断方式与语气 |
| `manifest.json` / `meta.json` | 元数据与入口声明 |
| `tools/lint_h3_prompt.py` | 六段式体检器：顺序、6000–7000 字符、语言边界、内部编号泄漏、第七段 |
| `fixtures/` | 体检器样例：golden 应通过，bad-cjk / bad-internal 应失败 |
| `examples/` | 工作示例：从 Shot Card 到六段式骨架 |
| `scripts/check_skill.py` | 仓库自检：结构、frontmatter、六段、禁词、manifest、语料索引 |
| `scripts/install.sh` | 装到 dsh / claude / codex |
| `.github/workflows/validate.yml` | CI：自检 + 假目录安装 + 体检器跑 golden |

---

## 自检

```bash
python scripts/check_skill.py      # 结构 + frontmatter + 六段 + 禁词 + manifest + 语料索引（108 条）
```

CI 在每次 push 与 PR 上跑同一套，另外做一次「装进假 skills 目录再体检 golden」的端到端验证。
验证口径与未验证边界见 [VERIFICATION.md](VERIFICATION.md)，版本变更见 [CHANGELOG.md](CHANGELOG.md)。

---

## 边界

- 只执行 MiniMax H3 Ref2VA，不切模型、不推荐其他模式。
- 平台能力（时长档位、参考输入互斥）只有文档依据，标 DOCUMENTED 不标 VERIFIED，不当硬上限。
- 未生成视频之前，媒体项一律 DEFERRED / UNTESTED，不写成通过。
- 技能是操作层：逐章容差、风格参数卡、节点库体例、方言口音表仍以原始规范为准，正文给的是索引与行号。
- 原始规范集不随仓库分发，只在方法层做索引。

## 许可

MIT，见 [LICENSE](LICENSE)。
