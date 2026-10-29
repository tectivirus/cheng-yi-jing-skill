# 验证说明

仓库内所有检查可本地复跑，不依赖外部服务。

## CI 执行的检查（scripts/check_skill.py）

| 项 | 说明 |
|---|---|
| 文件齐备 | SKILL.md / work.md / persona.md / work_skill.md / persona_skill.md / meta.json / manifest.json |
| 编码 | UTF-8，无 BOM；读写统一 LF，避免 CRLF 导致正则失配 |
| frontmatter | name / description / user-invocable；name 必须等于 celebrity-cheng-yi-jing |
| 章节 | PART A、PART B、Layer 0、运行规则、人格名 |
| 六段式 | 六个段名齐全 |
| 禁词 | 七个文件扫描，命中即失败 |
| 语料索引 | 条目数 ≥ 100（当前 108） |
| manifest | artifacts 必须含 work_skill.md 与 persona_skill.md |
| meta | slug 必须等于 cheng-yi-jing |

## 体检器（tools/lint_h3_prompt.py）

对一条六段式提示词做 8 项确定性检查，退出码 0 通过 / 1 有问题。仓库附三个样例：

| 样例 | 期望 |
|---|---|
| fixtures/golden.txt | PASS（6,565 字符） |
| fixtures/bad-cjk.txt | FAIL：台词标签外出现中文 |
| fixtures/bad-internal.txt | FAIL：正文混入 G/CG/ADN 编号 + 出现第七段 |

## 已做的实测

- 单镜端到端：按技能独立产出 8 秒单镜六段式，6,975 字符，体检器 PASS；压缩过程与卡点记录见源仓库的工作区报告。
- 事实核验：254 条规范性陈述对原始规范逐条核验，真错 5 条已修（另有 3 条为核验方检索范围错误，已驳回并留证）。
- 一致性审计：53 条提醒，5 条阻断级已修（优先级链口径、时长身份、版本账本、门数、manifest 产物）。

## 未验证的边界

1. 未附真实生成视频：画面、嘴型、接触、音轨仍属 UNTESTED。
2. 平台未公开的固定参数不写死，按项目配置与当次界面填。
3. 只做单镜端到端，未做多集长程压测。
