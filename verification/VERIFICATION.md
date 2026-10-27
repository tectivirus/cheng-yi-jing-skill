# 验证说明

本仓库不附带第三方验证脚本，全部检查可在仓库内复跑。

## 由 CI 执行的检查（scripts/check_skill.py）

| 项 | 说明 |
|---|---|
| 文件齐备 | SKILL.md / work.md / persona.md / work_skill.md / persona_skill.md |
| 编码 | UTF-8，无 BOM |
| frontmatter | name、description、user-invocable 三键齐全 |
| 章节 | PART A、PART B、Layer 0–5、运行规则 |
| 六段式 | subject_definitions / summary / retention_analysis / detailed_description / overall_soundscape / non_diegetic_music |
| 占位符 | 无 TODO / XXX / TBD / 未渲染模板 |
| 人格名 | SKILL.md 声明"程一镜" |

## 端到端样例（人工验证）

6 秒单镜、16:9、两人一句台词：

- 六段顺序正确，无第七段
- `<d>` 之外零汉字、零中文标点
- 唯一中文为 `<d>[Chinese]…</d>` 中的台词，逐字一致
- 整串 6308 字符，落在 6000–7000 预算内
- 只声明 S1 一个说话人，绑定 Subject 1
- 任务前缀 `[reference generation]`，未误用 keyframe
- 正文未混入 camera_control / ADN / G 编号
- 九阶段齐全，6000−4900=1100 的 end_hold 自洽
- pending / untested / deferred 三栏分离

## 未验证的边界

1. 未附真实生成视频：画面、嘴型、接触、音轨仍属 UNTESTED（这也是规范自身的口径：设计通过不等于媒体通过）。
2. 平台方未公开的固定参数（像素、部分上限）不写死，按项目配置与当次界面填。
3. 未做多集长程压测，只做单镜端到端。
