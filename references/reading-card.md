# Visual Reading Card contract

Use this contract for every `/start` response. The goal is decision support at a glance, not decorative relabeling of a summary.

## Required behavior

- Start the response with the card. Add no introduction before it.
- Render one visually bounded Markdown block using a callout/blockquote, compact tables, and inline code chips.
- Keep every content cell to one or two short lines.
- Put reading actions before optional background detail.
- Use exact paper locators for `必看`, `可跳过`, and the reading route.
- Mark unknown metadata as `未核实`; never fill a card cell from memory.
- End the card with exactly one `▶ START HERE` action.
- Add deeper explanation only after the card and only when requested.

## Default card template

Replace every placeholder. Remove a row only when it truly does not apply; do not leave template text in the response.

> ### 📄 PaperLens · Reading Card
> **{Full paper title}**  
> `{Venue/Year or 未核实}` `Task: {task}` `Representation: {representation}`
>
> | 阅读决策 | 结论 |
> |---|---|
> | **为什么读** | {The specific knowledge or method gap this paper fills} |
> | **读完获得** | {One concrete capability or judgment the reader should gain} |
> | **预计时间** | `{quick minutes} min 快读` · `{deep minutes} min 深读` |
>
> | 核心判断 | 内容 |
> |---|---|
> | 🎯 **Problem** | {problem} |
> | ⚠️ **Baseline failure** | {why the direct baseline fails} |
> | 💡 **Key insight** | {the observation that unlocks the method} |
>
> **Pipeline delta**  
> `Input {reused/changed}` → `Pose {reused/changed}` → `Representation {reused/changed}` → `Optimization {reused/changed}` → `Rendering {reused/changed}` → `Loss {reused/changed}`
>
> | 阅读动作 | 精确位置 |
> |---|---|
> | ✅ **必看** | `{Fig./Eq./Table/§}` · `{Fig./Eq./Table/§}` · `{Fig./Eq./Table/§}` |
> | ⏭️ **可跳过** | `{location}` — {why it can wait} |
> | 🧊 **暂不深究** | `{location/concept}` — {what prerequisite is missing} |
>
> **Reading route**  
> `① {object}` → `② {object}` → `③ {object}` → `④ {object}`
>
> **Difficulty**  
> `数学 {★☆☆☆☆–★★★★★}: {reason}` · `代码 {stars}: {reason}` · `背景 {stars}: {reason}`
>
> **Evidence** `{status}` · **Confidence** `{High/Medium/Low}`  
> {Locators used; list any unverified or missing field}
>
> ▶ **START HERE：{one exact first action}**

## Formatting rules

- Preserve the title strip, the three compact tables/rows, pipeline, route, evidence footer, and start action.
- Use bold labels, emoji, and code chips as visual hierarchy; do not turn each cell into a paragraph.
- Limit `必看` to 3–5 objects. A section title alone is insufficient when a key figure, equation, algorithm, or table is available.
- Use `changed`, `reused`, or `N/A` consistently in the pipeline. Highlight changed stages with `★changed`.
- Estimate reading time from paper length and technical density; mark it `[AI 推断]` in the evidence footer.
- If the card exceeds roughly one screen, shorten content rather than splitting it into several cards.

## Failure cases

Do not output:

- a paragraph headed “Reading Card”;
- nine prose subsections with no visual boundary;
- a generic `Abstract → Introduction → Method → Experiments` route;
- invented page numbers or unverified venue metadata;
- a pipeline where every stage is marked changed;
- a card followed by a duplicate prose summary.
