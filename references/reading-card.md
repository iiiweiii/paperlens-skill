# Visual Reading Card contract

Use this contract for every `/start` response. The result has two layers: a spacious inline overview and, for routes with four or more stops, a detailed self-contained HTML card.

## Layout principles

- Start with the inline card. Add no introductory paragraph.
- Use six visibly separated zones with blank space between them; do not compress everything into one table.
- Keep each idea short, but allow two or three lines when causal explanation needs room.
- Put the reading decision first and evidence last.
- Include 1–3 high-value objects cropped from the actual paper PDF: at least one figure or table, plus a key equation when the paper has one. Never substitute an AI-redrawn diagram.
- Render `阅读取舍` as three full-width horizontal lanes: category label on the left and reading items flowing to the right. Never squeeze all `必看` items into one narrow vertical column.
- Use exact paper locators. Mark missing metadata as `未核实` instead of recalling it from memory.
- End with exactly one immediate action.

## Inline card template

Replace every placeholder and remove inapplicable optional content.

> # 📄 PaperLens
> ## {Full paper title}
> `{Venue/Year or 未核实}`　`{task}`　`{representation}`
>
> ---
>
> ### 先决定：值不值得读
>
> **为什么读**  
> {The precise gap this paper fills.}
>
> **读完以后，你应该能判断**  
> {One concrete capability or judgment.}
>
> `快读 {minutes} min`　`深读 {minutes} min`　`优先级 {高/中/低}`
>
> ---
>
> ### 方法主线
>
> 🎯 **问题**  
> {Specific failure mode.}
>
> ⚠️ **原方法为什么不行**  
> {Cause of the baseline failure.}
>
> 💡 **关键洞察**  
> {Observation that unlocks the method.}
>
> **Pipeline delta**  
> `…` → `Representation ★changed` → `Optimization reused` → `Rendering ★changed` → `…`
>
> ---
>
> ### 论文原图、原表与公式
>
> **{Fig./Table label} · 论文原始裁剪**  
> ![{label} original crop]({absolute local image path})  
> **论文原文 / Caption：** {verified caption or defining sentence}  
> **读它时看什么：** {one focused reading instruction}  
> `Evidence: {page + locator}`　`Confidence: {level}`
>
> **{Eq. label} · 论文原公式**  
> ![{label} original equation crop]({absolute local image path})  
> **核对后的转写：** `{optional transcription checked against crop}`  
> **它在方法里的作用：** {why this equation exists}  
> `Evidence: {page + locator}`　`Confidence: {level}`
>
> ---
>
> ### 阅读取舍
>
> | | 精确位置 | 目的 |
> |---|---|---|
> | ✅ **必看** | `{locator}` | {why this object matters} |
> | ✅ **必看** | `{locator}` | {why this object matters} |
> | ⏭️ **稍后再读** | `{locator}` | {why it can wait} |
> | 🧊 **先补背景** | `{concept/locator}` | {missing prerequisite} |
>
> ---
>
> ### 阅读旅程
>
> **01 · 建立全局图**　`{locator}`  
> 目的：{what to understand}  
> **离开前回答：** {exit question}
>
> **02 · 拆核心机制**　`{locator}`  
> 目的：{what to understand}  
> **离开前回答：** {exit question}
>
> **03 · 检查证据**　`{locator}`  
> 目的：{what to verify}  
> **离开前回答：** {exit question}
>
> **04 · 确认边界**　`{locator}`  
> 目的：{what limitation or assumption to identify}  
> **离开前回答：** {exit question}
>
> ↳ **如果第 {N} 站卡住：** 先看 `{prerequisite locator/concept}`，只补到能回答该站问题为止。
>
> ---
>
> ### 难度与可信度
> `数学 {stars}` {reason}　·　`代码 {stars}` {reason}　·　`背景 {stars}` {reason}
>
> **Evidence** `{status and locators}`  
> **Confidence** `{High/Medium/Low}`　{missing or unverified fields}
>
> ## ▶ START HERE
> **{One exact first action, including what to look for.}**

## Route design

Build a cognitive route, not a document-order route. Use 4–7 stops selected from these roles:

1. **Orient**: obtain the paper's input, representation, output, and claimed delta from the overview figure or method diagram.
2. **Question**: identify the baseline failure from a motivating figure, introduction passage, or diagnostic experiment.
3. **Mechanism**: understand the changed module from the key section, equation, algorithm, or figure.
4. **Evidence**: test the central claim against the strongest main result and a targeted ablation.
5. **Boundary**: identify assumptions, failure cases, missing tests, or domain limits.
6. **Context**: visit related work only when it resolves a specific comparison or terminology gap.

Each stop requires:

- a semantic stage name, never only a section number;
- one exact locator;
- one reading purpose;
- one exit question that proves the stop is complete.

Add a detour only when it unblocks the next stage. A detour names the missing concept or locator and the minimum understanding required before returning.

## Original paper objects

Prepare the visual evidence before rendering `/start`:

- Render the exact PDF page and crop the original figure, table, or numbered equation into a workspace-local image.
- Preserve the figure/table number, axes, legend, panel labels, and enough caption context to prevent misreading.
- For equations, show the original crop. Add OCR or LaTeX only after checking every symbol against the crop; label it as a transcription, never as source text.
- Save crops under the active workspace, for example `paperlens-data/<paper-slug>/media/`. Do not store paper-derived images in the installed Skill.
- Put the crop path in `paper_objects.items[].image`. The renderer embeds local files as data URIs so the output HTML remains self-contained.
- If the paper has no meaningful equation, include figures/tables only and state `本文无需要优先理解的关键公式`. Never invent an equation to fill the section.
- If a crop cannot be verified, omit it and report the extraction gap instead of using a substitute image.

Limit the default card to 1–3 objects: typically the method overview, the key equation, and the strongest result or ablation. More objects belong in `/figure` or `/formula` follow-ups.

## HTML card

When the route has four or more stops, write the analyzed card data to a workspace-local JSON file and run:

```text
python scripts/render_reading_card.py card.json reading-card.html
```

The JSON keys are: `title`, `metadata`, `decision`, `core`, `paper_objects`, `pipeline`, `actions`, `route`, `detour`, `difficulty`, `evidence`, and `start_here`. Each `paper_objects.items[]` entry uses `kind`, `label`, `image`, `paper_text`, `reading_focus`, `evidence`, and `confidence`; equation items may also include `transcription`. Inspect the script's `--example` output for the exact schema. Link the generated HTML after the inline card. Do not put mutable paper data inside the installed Skill directory.

## Failure cases

Do not output:

- one dense table containing the entire card;
- an AI-redrawn figure presented in place of a paper original;
- a formula transcription without the original crop or symbol-by-symbol verification;
- three narrow action columns that force locators or explanations into vertical text;
- a paragraph merely headed “Reading Card”;
- a route drawn as a single unannotated arrow chain;
- a generic section-order route;
- a stop without a purpose or exit question;
- invented locators, venues, or metadata;
- a card followed by a duplicate prose summary.
