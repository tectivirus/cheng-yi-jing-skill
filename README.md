# 程一镜 · MiniMax H3 Ref2VA 短剧工业化分镜技能

> 把一部短剧剧本，压成能投喂、能验收、能返修、能追溯的**单镜任务**。

一个可直接加载到 AI Agent 的技能包：**工作方法（PART A）** + **工作人格（PART B）**。
面向 MiniMax H3 的 Ref2VA 参考生成模式：固定六段式英文提示词、Shot Card、八类微节点、G/CG 门禁、单主因返修。

## 安装

```bash
git clone <repo> && cd cheng-yi-jing-skill
./scripts/install.sh dsh          # 或 claude / codex
```

装完技能名 **`celebrity-cheng-yi-jing`**（默认路径 `~/.dsh/skills/celebrity-cheng-yi-jing`）。

- Windows 用 Git Bash 跑
- 自定义目录：`DSH_SKILLS_DIR=/path/to/skills ./scripts/install.sh dsh`

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

## 结构

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 合成技能：PART A 工作能力 + PART B 人格 + 运行规则（**单文件即可用**） |
| `work.md` / `work_skill.md` | 方法与规范主体 |
| `persona.md` / `persona_skill.md` | 判断方式与语气 |
| `manifest.json` / `meta.json` | 元数据与入口声明 |
| `tools/lint_h3_prompt.py` | 六段式体检器：顺序、6000–7000 字符、语言边界、内部编号泄漏、第七段 |
| `fixtures/` | 体检器样例：golden 应通过，bad-cjk / bad-internal 应失败 |
| `scripts/check_skill.py` | 仓库自检：结构、frontmatter、六段、禁词、manifest、语料索引 |
| `.github/workflows/validate.yml` | CI：自检 + 假目录安装 + 体检器跑 golden |

## 自检与验证

```bash
python scripts/check_skill.py                 # 结构自检
python tools/lint_h3_prompt.py fixtures/golden.txt
```

体检器 8 项：六段齐全与顺序、整串字符预算、中文只在台词标签内、标签内不夹英文说明、summary 任务类型合法、正文无 G/CG/ADN 等内部编号、retention 无 Sx、无第七段。

## 边界

- 只执行 MiniMax H3 Ref2VA，不切模型、不推荐其他模式。
- 平台能力（时长档位、参考输入互斥）只有文档依据，标 DOCUMENTED 不标 VERIFIED，不当硬上限。
- 未生成视频之前，媒体项一律 DEFERRED / UNTESTED，不写成通过。
- 技能是操作层：逐章容差、风格参数卡、节点库体例、方言口音表仍以原始规范为准，正文给的是索引与行号。

## 许可

MIT，见 LICENSE。
