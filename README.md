# PaperLens

<p align="center">
  <a href="#简体中文"><kbd>简体中文</kbd></a>
  &nbsp;|&nbsp;
  <a href="#english"><kbd>English</kbd></a>
</p>

## 简体中文

> 面向计算机视觉与三维视觉研究的、强调证据可追溯性的论文阅读助手。

PaperLens 是一个 Codex Skill，用于辅助研究者交互式阅读论文。它不会用冗长的摘要代替阅读，而是帮助你定位重要章节、理解方法为什么这样设计、解释图表和公式、判断真正的技术贡献，并维护一个轻量且带有证据的论文关系图。

它尤其适合 NeRF、3D Gaussian Splatting、三维重建、新视角合成、全景视觉、渲染和场景更新等 3D Vision 方向。

### PaperLens 能做什么

- 上传论文 PDF 后生成分区舒展的 Reading Card，而不是一段改写摘要或一张拥挤表格。
- 将阅读顺序组织成“目的—位置—离开问题”的认知旅程，并可生成响应式 HTML 时间线。
- 结合上下文解释选中段落、图、表和公式。
- 将论文创新定位到 CV/3D Vision 技术管线中。
- 区分复用组件、技术修改和真正的核心创新。
- 区分论文事实、论文内归纳、外部核实信息和 AI 推断。
- 分析假设、局限、缺失实验和潜在延伸方向。
- 在对齐任务、数据集、指标和管线阶段后比较论文。
- 维护带有 Evidence 和 Confidence 的轻量论文关系图。

### 命令

| 命令 | 作用 |
|---|---|
| `/start` | 生成分区式 Reading Card、阅读取舍与带目标和检查问题的可视化路线。 |
| `/explain` | 解释一段内容在做什么、为什么存在以及位于管线哪里。 |
| `/figure N` | 解释图或表的目的、阅读顺序和作者希望表达的结论。 |
| `/formula N` | 从直觉、变量和用途开始解释公式，再按需展开推导。 |
| `/core` | 判断真正的创新，并区分核心设计、辅助设计和工程实现。 |
| `/why-important` | 解释研究问题及论文贡献为什么重要。 |
| `/reviewer` | 进行带证据的批判性阅读并提出缺失实验。 |
| `/compare A B` | 在对齐技术和评测条件后比较多篇论文。 |
| `/related` | 推荐 3–5 篇真正值得继续阅读的前置、基线、替代或后续工作。 |
| `/note` | 生成可长期保存且避免重复的论文笔记。 |
| `/map` | 展示或更新带有证据的轻量论文关系图。 |

也可以直接使用自然语言。例如，“Fig. 4 没看懂”等价于 `/figure 4`。

### Reading Card 长什么样

`/start` 使用留白和分区建立视觉层级，不再把所有信息塞进一张表：

> # 📄 PaperLens
> ## Paper title
> `Venue/Year`　`Task`　`Representation`
>
> ---
>
> ### 01 · 先决定：值不值得读
>
> **为什么读**  
> 这篇论文补上了什么具体知识缺口。
>
> **读完以后，你应该能判断**  
> 某项技术改动是否真正解决了目标失败模式。
>
> `快读 15 min`　`深读 60 min`　`优先级 High`
>
> ---
>
> ### 02 · 方法主线
>
> 🎯 **问题**：论文试图解决的具体失败模式。  
> ⚠️ **原方法为什么不行**：失败来自哪个假设或管线阶段。  
> 💡 **关键洞察**：作者把约束放回问题真正发生的位置。
>
> `Input reused` → `Representation ★changed` → `Rendering ★changed` → `Output reused`
>
> ---
>
> ### 03 · 阅读取舍
>
> | | 精确位置 | 阅读目的 |
> |---|---|---|
> | ✅ 必看 | `Fig. 2` | 建立方法全局图 |
> | ✅ 必看 | `§3.2 + Eq. 7` | 拆核心机制 |
> | ⏭️ 稍后再读 | `Related Work` | 只在术语卡住时返回 |
>
> ---
>
> ### 04 · 阅读旅程
>
> **01 · 建立全局图**　`Fig. 2`  
> 目的：确认输入、表示、改动阶段与输出。  
> **离开前回答：哪些阶段 changed，哪些 reused？**
>
> **02 · 定位失败原因**　`Introduction + Fig. 1`  
> 目的：把现象连接到 baseline 的具体假设。  
> **离开前回答：原方法为什么会在这里失效？**
>
> ↳ **如果答不出：** 只补 baseline 的表示章节，然后返回第 03 站。
>
> **03 · 拆核心机制**　`§3.2 + Eq. 7`  
> 目的：追踪“原因 → 操作 → 效果”。  
> **离开前回答：数学上改了什么，进入管线哪里？**
>
> **04 · 检查证据**　`Table 2 + Ablation`  
> 目的：确认实验是否隔离了核心模块的贡献。  
> **离开前回答：哪项证据真正支持作者的核心解释？**
>
> ---
>
> **Evidence** `论文 PDF 已定位`　**Confidence** `High`
>
> ## ▶ START HERE
> **先看 Fig. 2，并找出输入、表示、改动阶段和输出。**

四站以上的路线还会通过 `scripts/render_reading_card.py` 生成独立 HTML 卡片：包含彩色 Pipeline、纵向时间线、前置知识旁路、明暗主题和窄屏布局。

```bash
python scripts/render_reading_card.py --example
python scripts/render_reading_card.py card.json reading-card.html
```

### Evidence 与 Confidence

PaperLens 会给关键结论添加标签，避免把作者陈述和模型分析混在一起：

- `[论文事实]`：论文直接陈述或展示的信息。
- `[论文内归纳]`：基于论文证据形成的归纳。
- `[外部已核实]`：通过一手外部来源核实的信息。
- `[AI 推断]`：模型的解释、质疑、假设或延伸建议。
- `[论文未说明]`：论文没有建立或验证的信息。

核心判断会附带简洁的证据位置和置信度，优先引用章节、页码、公式、图、表、附录或可唯一定位的短语。

### CV 与 3D Vision 管线定位

对于相关论文，PaperLens 会将技术变化定位到以下管线：

```text
输入 → 相机/位姿 → 预处理/特征 → 表示
    → 初始化 → 优化 → 渲染/光栅化
    → 损失/监督 → 输出 → 评测
```

它还会明确任务和指标边界。PSNR、SSIM、LPIPS 和 FPS 等渲染指标不会被当作几何精度证据；几何质量需要单独依据 Accuracy、Completeness、Chamfer Distance、F-score、深度、法线或位姿指标判断。

### 快速开始

1. 安装 Skill；如果 Codex 已经运行，请重启以刷新 Skill 列表。
2. 上传一篇论文 PDF。
3. 调用 `$paperlens` 或输入 `/start`。
4. 阅读过程中继续使用 `/figure 2`、`/formula 7`、`/core` 和 `/reviewer` 等命令。

```text
Use $paperlens on this PDF.
/start
```

随后可以输入：

```text
/figure 3
/formula 7
/core
/reviewer
/note
```

### 安装

将仓库克隆到个人 Codex Skills 目录：

```powershell
git clone https://github.com/iiiweiii/paperlens-skill.git "$env:USERPROFILE\.codex\skills\paperlens"
```

重启 Codex 以刷新 Skill 列表。轻量关系图脚本只依赖 Python 标准库，不需要安装第三方包。

### 轻量 Paper Map

MVP 中的 `/map` 有意保持轻量。它使用工作区内的 JSON 文件，并支持五种关系：

- `BASED_ON`
- `IMPROVES`
- `SAME_PROBLEM`
- `SIMILAR_METHOD`
- `FOLLOW_UP`

每条关系都会记录证据来源、定位信息和置信度。MVP 暂不实现完整图数据库或三维可视化。

### 仓库结构

```text
paperlens-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── paper-map.template.json
├── references/
│   ├── commands.md
│   ├── cv-3d-pipeline.md
│   ├── evidence-and-confidence.md
│   ├── reading-card.md
│   └── paper-map.md
└── scripts/
    ├── paper_map.py
    └── render_reading_card.py
```

### 范围说明

PaperLens 是论文阅读助手，不是大而全的文献管理平台。它优先提供聚焦的解释、可核实的证据和少量有意义的论文关系，而不是生成穷尽式总结或庞大的自动知识图谱。

<p align="right"><a href="#paperlens">返回顶部</a></p>

---

## English

> An evidence-aware paper reading companion for computer vision and 3D vision research.

PaperLens is a Codex Skill that helps researchers read papers interactively. It does not replace reading with a long abstract summary. Instead, it helps you locate the important sections, understand why a method is designed that way, explain figures and equations, identify the real contribution, and preserve a small evidence-backed paper map.

It is especially suited to 3D Vision topics such as NeRF, 3D Gaussian Splatting, reconstruction, novel-view synthesis, panoramic vision, rendering, and scene updating.

## What PaperLens does

- Creates a spacious, sectioned Reading Card after you attach a paper PDF instead of returning renamed prose or one dense table.
- Turns reading order into a purpose–locator–exit-question journey and can render it as a responsive HTML timeline.
- Explains selected paragraphs, figures, tables, and equations in context.
- Locates each contribution in a CV/3D Vision pipeline.
- Separates reused components, technical changes, and actual novelty.
- Distinguishes paper facts from synthesis, external verification, and AI inference.
- Reviews assumptions, limitations, missing experiments, and possible extensions.
- Compares papers using aligned tasks, datasets, metrics, and pipeline stages.
- Maintains a lightweight paper relation map with evidence and confidence.

## Commands

| Command | Purpose |
|---|---|
| `/start` | Build a sectioned Reading Card and a visual route with goals, locators, and exit questions. |
| `/explain` | Explain what a passage does, why it exists, and where it sits in the pipeline. |
| `/figure N` | Explain the purpose, reading order, and conclusion of a figure or table. |
| `/formula N` | Explain an equation from intuition and variables to optional derivation. |
| `/core` | Identify the real novelty and separate core, supporting, and engineering changes. |
| `/why-important` | Explain why the problem and contribution matter. |
| `/reviewer` | Perform evidence-aware critical reading and propose missing experiments. |
| `/compare A B` | Compare papers on aligned technical and evaluation dimensions. |
| `/related` | Recommend only 3–5 high-value prerequisite, baseline, alternative, or follow-up papers. |
| `/note` | Produce a durable, non-redundant paper note. |
| `/map` | Show or update a lightweight evidence-bearing paper relation map. |

Natural-language requests work too. For example, “Fig. 4 没看懂” is treated like `/figure 4`.

## What the Reading Card looks like

`/start` uses spacing and sections to build hierarchy instead of packing every fact into one table:

> # 📄 PaperLens
> ## Paper title
> `Venue/Year`　`Task`　`Representation`
>
> ---
>
> ### 01 · Decide whether to read
>
> **Why read it**  
> The precise knowledge gap filled by the paper.
>
> **After reading, you should be able to judge**  
> Whether the technical change actually addresses the target failure mode.
>
> `15 min quick`　`60 min deep`　`Priority High`
>
> ---
>
> ### 02 · Method through-line
>
> 🎯 **Problem:** the precise failure mode.  
> ⚠️ **Why the baseline fails:** the responsible assumption or pipeline stage.  
> 💡 **Key insight:** move the constraint to the stage where the failure originates.
>
> `Input reused` → `Representation ★changed` → `Rendering ★changed` → `Output reused`
>
> ---
>
> ### 03 · Reading choices
>
> | | Exact locator | Reading purpose |
> |---|---|---|
> | ✅ Must read | `Fig. 2` | Build the global method picture |
> | ✅ Must read | `§3.2 + Eq. 7` | Trace the core mechanism |
> | ⏭️ Later | `Related Work` | Return only when terminology blocks you |
>
> ---
>
> ### 04 · Reading journey
>
> **01 · Build the global picture**　`Fig. 2`  
> Purpose: identify input, representation, changed stages, and output.  
> **Exit question: which stages changed, and which were reused?**
>
> **02 · Locate the failure**　`Introduction + Fig. 1`  
> Purpose: connect the symptom to one baseline assumption.  
> **Exit question: why does the baseline fail here?**
>
> ↳ **If you cannot answer:** read only the baseline representation section, then return to stage 03.
>
> **03 · Trace the mechanism**　`§3.2 + Eq. 7`  
> Purpose: follow cause → operation → intended effect.  
> **Exit question: what changes mathematically, and where does it enter the pipeline?**
>
> **04 · Check the evidence**　`Table 2 + Ablation`  
> Purpose: determine whether the experiment isolates the core module.  
> **Exit question: which evidence actually supports the central explanation?**
>
> ---
>
> **Evidence** `located in attached PDF`　**Confidence** `High`
>
> ## ▶ START HERE
> **Open Fig. 2 and identify the input, representation, changed stages, and output.**

Routes with four or more stops can also be rendered by `scripts/render_reading_card.py` as a standalone HTML card with a colored pipeline, vertical timeline, prerequisite detour, theme switch, and responsive layout.

```bash
python scripts/render_reading_card.py --example
python scripts/render_reading_card.py card.json reading-card.html
```

## Evidence and confidence

PaperLens labels important claims so that author statements and model interpretations are not mixed:

- `[论文事实]`: directly stated or shown by the paper.
- `[论文内归纳]`: a synthesis grounded in paper evidence.
- `[外部已核实]`: verified from a primary external source.
- `[AI 推断]`: interpretation, critique, hypothesis, or extension.
- `[论文未说明]`: not established by the paper.

Central claims include a compact evidence locator and confidence level. Whenever possible, PaperLens cites a section, page, equation, figure, table, appendix, or unique phrase.

## CV and 3D Vision positioning

For relevant papers, PaperLens locates changes in this pipeline:

```text
Input → Camera/Pose → Preprocessing/Features → Representation
      → Initialization → Optimization → Rendering/Rasterization
      → Loss/Supervision → Output → Evaluation
```

It also keeps task and metric boundaries explicit. Rendering metrics such as PSNR, SSIM, LPIPS, and FPS are not presented as evidence of geometric accuracy; geometry evidence is handled separately through accuracy, completeness, Chamfer distance, F-score, depth, normal, or pose metrics.

## Quick start

1. Install the Skill and restart Codex if it is already running.
2. Attach a paper PDF.
3. Invoke `$paperlens` or enter `/start`.
4. Continue reading with commands such as `/figure 2`, `/formula 7`, `/core`, and `/reviewer`.

Example:

```text
Use $paperlens on this PDF.
/start
```

Then:

```text
/figure 3
/formula 7
/core
/reviewer
/note
```

## Installation

Clone the repository into your personal Codex Skills directory:

```powershell
git clone https://github.com/iiiweiii/paperlens-skill.git "$env:USERPROFILE\.codex\skills\paperlens"
```

Restart Codex so the Skill list refreshes. The lightweight map helper uses only the Python standard library and does not require third-party packages.

## Lightweight Paper Map

`/map` is intentionally small in the MVP. It stores a workspace-local JSON file and supports five relation types:

- `BASED_ON`
- `IMPROVES`
- `SAME_PROBLEM`
- `SIMILAR_METHOD`
- `FOLLOW_UP`

Each relation records its evidence source, locator, and confidence. The MVP does not implement a full graph database or 3D visualization.

## Repository layout

```text
paperlens-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── paper-map.template.json
├── references/
│   ├── commands.md
│   ├── cv-3d-pipeline.md
│   ├── evidence-and-confidence.md
│   ├── reading-card.md
│   └── paper-map.md
└── scripts/
    ├── paper_map.py
    └── render_reading_card.py
```

## Scope

PaperLens is a reading assistant, not a full literature-management platform. It prioritizes focused explanations, verifiable evidence, and a small number of meaningful paper relations over exhaustive summaries or automatically generated knowledge graphs.

<p align="right"><a href="#paperlens">Back to top</a></p>
