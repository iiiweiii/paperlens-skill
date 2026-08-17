# Visual Reading Card contract

Use this contract for every `/start` response. The result has two layers: a spacious inline overview and, for routes with four or more stops, a detailed self-contained HTML card.

## Layout principles

- Start with the inline card. Add no introductory paragraph.
- Use five visibly separated zones with blank space between them; do not compress everything into one table.
- Keep each idea short, but allow two or three lines when causal explanation needs room.
- Put the reading decision first and evidence last.
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

## HTML card

When the route has four or more stops, write the analyzed card data to a workspace-local JSON file and run:

```text
python scripts/render_reading_card.py card.json reading-card.html
```

The JSON keys are: `title`, `metadata`, `decision`, `core`, `pipeline`, `actions`, `route`, `detour`, `difficulty`, `evidence`, and `start_here`. Inspect the script's `--example` output for the exact schema. Link the generated HTML after the inline card. Do not put mutable paper data inside the installed Skill directory.

## Failure cases

Do not output:

- one dense table containing the entire card;
- three narrow action columns that force locators or explanations into vertical text;
- a paragraph merely headed “Reading Card”;
- a route drawn as a single unannotated arrow chain;
- a generic section-order route;
- a stop without a purpose or exit question;
- invented locators, venues, or metadata;
- a card followed by a duplicate prose summary.
