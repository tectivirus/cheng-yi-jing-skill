# 更新日志

## v1.1.0 — 2026-10-29

打包版本 v1.1.0（对应蒸馏版本 v11）。技能内容不变，补齐「拿起来就能用」的那一层。

- 新增 `examples/shot-card-01.md`：一场戏从 Shot Card 到六段式骨架的完整工作示例。
- README 重写：真实克隆地址、三端安装、一分钟流程、体检器 8 项对照表、CI 徽章。
- 修正 README 里 `git clone <repo>` 占位符。
- 新增本更新日志，与 `VERIFICATION.md` 分工：一个记改了什么，一个记怎么验、哪没验。

## v1.0.0 — 2026-10-29

首次发布。全量重建的 V8 规范执行体：

- `SKILL.md`：PART A 工作能力（职责边界 / 层级与优先级 / 六段式硬契约 / 镜头事实层 / 工作流 / 门禁与状态 / 自动判定 / 失败码 / 协作硬要求）+ PART B 人格 + 运行规则，含 108 条语料章节索引。
- `work.md` / `work_skill.md`、`persona.md` / `persona_skill.md`、`manifest.json` / `meta.json`。
- `tools/lint_h3_prompt.py`：六段式体检器，8 项确定性检查，附 golden / bad-cjk / bad-internal 三份样例。
- `scripts/check_skill.py` + GitHub Actions：结构自检与端到端安装验证。
