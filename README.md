# PaperLens

> An evidence-aware paper reading companion for computer vision and 3D vision research.

PaperLens is a Codex Skill that helps researchers read papers interactively. It does not replace reading with a long abstract summary. Instead, it helps you locate the important sections, understand why a method is designed that way, explain figures and equations, identify the real contribution, and preserve a small evidence-backed paper map.

It is especially suited to 3D Vision topics such as NeRF, 3D Gaussian Splatting, reconstruction, novel-view synthesis, panoramic vision, rendering, and scene updating.

## What PaperLens does

- Creates a concise reading route after you attach a paper PDF.
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
| `/start` | Build a Reading Card, reading route, prerequisites, and difficulty estimate. |
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
│   └── paper-map.md
└── scripts/
    └── paper_map.py
```

## Scope

PaperLens is a reading assistant, not a full literature-management platform. It prioritizes focused explanations, verifiable evidence, and a small number of meaningful paper relations over exhaustive summaries or automatically generated knowledge graphs.

