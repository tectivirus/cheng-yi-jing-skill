# 程一镜 · MiniMax H3 Ref2VA 短剧工业化技能

> 把一部短剧剧本，压成能投喂、能验收、能返修、能追溯的**单镜任务**。

一个可直接加载到 AI Agent 的技能包：**工作方法（PART A）** + **工作人格（PART B）**。
面向 MiniMax H3 的 Ref2VA 参考生成模式，产出固定六段式英文提示词，配套 Shot Card、九阶段时间轴、质量门禁与单变量返修。

## 安装（一条命令）

```bash
git clone https://github.com/tectivirus/cheng-yi-jing-skill.git
cd cheng-yi-jing-skill
./install.sh dsh
```

装完即用，技能名 **`colleague-cheng-yi-jing`**（DSH 默认路径 `~/.dsh/skills/colleague-cheng-yi-jing`）。

- Windows 用 Git Bash 跑：`bash install.sh dsh`
- 自定义目录：`DSH_SKILLS_DIR=/path/to/skills ./install.sh dsh`
- Claude Code：`./install.sh claude`；Codex：`./install.sh codex`

手动安装也行：把 `SKILL.md work.md persona.md work_skill.md persona_skill.md manifest.json meta.json` 复制进 `<skills 目录>/colleague-cheng-yi-jing/` 即可——目录名必须和 frontmatter 的 `name` 一致。

## 它解决什么

单镜生成最容易翻车的三件事，这里都有硬约束：

| 翻车点 | 本技能的约束 |
|---|---|
| 每镜换脸 | 身份锚点绑定 `Subject N` + 资产版本，不许凭外观即兴 |
| 参考图被当成首帧 | 任务类型必须写 `[reference generation]`，帧锚点另立 `Picture N` |
| 说话人编号乱套 | `Sx` 按**全局首次发声**分配，Subject 编号不等于 Sx |
| 提示词越写越散 | 固定六段式、顺序不可换、不加第七段；整串 6000–7000 字符 |
| 中文混进正文 | 正文全英文，中文只允许出现在 `<d>[Chinese]…</d>` 里 |
| 返修越修越烂 | 一次只动一个主变量组，记 before/after，其余字段禁止漂移 |
| 门禁变成卡点 | `PASS / HOLD / BLOCKED` 三态，只挂受影响那一镜，无关工作继续 |

## 六段式（唯一输出壳）

```text
subject_definitions
summary
retention_analysis
detailed_description
overall_soundscape
non_diegetic_music
```

- `subject_definitions`：先写 Shot ID / Duration / Aspect ratio，再定义实际起作用的 Subject / Picture / Video / Audio
- `retention_analysis`：可见四档保留度 + 音频四档关系，不写 Sx
- `detailed_description`：一至两句定风格时间空间照明，再按播放顺序写起幅→触发→动作→反应→接触与声音→台词→落幅
- `non_diegetic_music`：无配乐写 `N/A`

## 工作流

**项目级 12 步**：建项目 → 喂剧本 → 资产图 → 资产表 → 拆单镜 → 语速节拍 → 六段式 → 工作台 → 投喂 H3 → 结果回喂 → 返修 → 交付归档
（真实顺序是 `1→2→3→4→5→6→7→11→8→9→10→12`，工作台先交付验收，再投喂生成）

**每镜 15 步**：身份证 → 冻结事实 → 锁主体 → 参考图组 → 起幅 → 落幅 → 九阶段动作 → 持续行为 → 面部嘴型 → 声线台词窗口 → 机位构图 → 灯光 → 道具与音效 → 渲染约束 → 门禁

## 怎么用

直接说人话，不用记编号：

- 「这是第 3 集剧本和角色图，按规范拆镜，先给我 Shot Card 和第一镜的六段式。」
- 「第 2 镜嘴型和台词差半拍，只修这一镜，别动其他镜头。」
- 「换对话前给我一份续做摘要：做到哪、哪些已确认、带哪些文件走。」

它回你的会是：当前能用到哪一步、这版能不能用、下一步要你补什么——而不是一屏门禁代码。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `SKILL.md` | 合成技能：PART A 工作能力 + PART B 人格 + 运行规则 |
| `work.md` / `work_skill.md` | 方法与规范主体 |
| `persona.md` / `persona_skill.md` | 判断方式与语气 |
| `manifest.json` / `meta.json` | 元数据与入口声明 |
| `scripts/install.sh` | 一键安装（dsh / claude / codex） |
| `scripts/check_skill.py` | 仓库自检脚本 |
| `.github/workflows/validate.yml` | CI：自检 + 安装到临时 skills 目录并校验 |

## 自检与验证

- `python scripts/check_skill.py`：BOM、frontmatter、PART A/B、Layer 0–5、六段名、占位符、人格名。
- CI 每次 push / PR：先自检，再把仓库装进临时 `DSH_SKILLS_DIR` 并验证安装副本（frontmatter 名、六段齐全）。
- 另做过一次端到端样例：6 秒单镜，六段齐全、`<d>` 外零汉字、整串 6308 字符落在 6000–7000、九阶段与 `end_hold` 算术自洽。

## 设计原则（写进 Layer 0 的纪律）

1. 先给口径，再给做法。
2. 小缺项不停；核心事实冲突才局部 BLOCKED。
3. 判断必须带替代写法，只说"不行"等于没干活。
4. 不虚构、不冒充已验证：没看片是 `UNTESTED`，没计数是"估算"。
5. 默认先给最小改动，确有取舍才给备选。
6. 用户不需要学门禁代码。
7. 只改该改的，其余字段禁止漂移。
8. 事实和可用性优先于好看。

## 作者

本仓库内容为作者原创作品；"程一镜"是作者的工作人格笔名。GitHub：[@tectivirus](https://github.com/tectivirus)。

## 许可

MIT，见 [LICENSE](LICENSE)。
