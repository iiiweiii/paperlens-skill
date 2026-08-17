# Command contracts

Use these output contracts as defaults, then shorten them when the user's question is narrower. Do not repeat content already established in the conversation.

## `/start` — Reading Card

Return:

1. **Paper**: title, authors, year, venue only when verified from the paper.
2. **一句话**: problem plus key solution, not an abstract rewrite.
3. **Why this paper**: the gap in the direct baseline.
4. **Core ideas**: at most three.
5. **Pipeline position**: stages changed versus reused.
6. **Recommended reading**: exact sections, figures, tables, or equations.
7. **Suggested order**: a short route such as `Fig. 2 → Introduction → §3.1 → §3.2 → Table 2 → Limitations`.
8. **Prerequisites**: only concepts that block comprehension.
9. **Difficulty**: math, implementation, and background on a five-point scale, with one reason each.

Do not provide a long summary. If pagination is unreliable, cite section and object labels instead of pages.

## `/explain <target>`

Return:

- **作者在做什么？** One plain technical sentence.
- **为什么要这样做？** State the failure mode or design pressure.
- **Pipeline 位置**: show the immediate predecessor and successor; mark the current module.
- **和 baseline 的区别**: reused versus changed.
- **机制**: explain cause → operation → effect.
- **记住这 1–3 点**.
- **Evidence / Confidence** for the central explanation.

If the supplied selection lacks context, inspect the preceding definition and following consequence. Explain symbols only when they affect the reasoning.

## `/figure <N>` and table equivalents

Inspect the actual figure, caption, surrounding paragraph, and paper references to it. Return:

- **这张图想回答什么？**
- **阅读顺序**: panels, arrows, axes, legend, or rows/columns.
- **模块/坐标含义**.
- **作者想让你得出的结论**.
- **它与核心创新的关系**.
- **图能证明什么 / 不能证明什么**.
- **Evidence / Confidence**.

For qualitative examples, distinguish cherry-picked visual evidence from aggregate evaluation. For a method overview with three or more stages, use a compact HTML pipeline only if it improves comprehension.

## `/formula <N>`

Inspect the equation, symbol definitions, preceding motivation, and subsequent use. Explain in this order:

1. **公式在算什么？**
2. **输入、输出与单位/shape** when meaningful.
3. **为什么需要它？**
4. **Pipeline 位置**.
5. **直觉**.
6. **与前一公式或 baseline 的变化**.
7. **数学细节** only to the depth requested.
8. **删掉或替换后会怎样？** Mark as paper evidence or inference.

Never claim a derivation is in the paper if you supplied it yourself. State assumptions behind any added derivation.

## `/core`

Return:

- **Previous method**.
- **Failure mode**.
- **Key insight**.
- **Technical change**.
- **Pipeline delta**: `changed / reused / not relevant`.
- **Why it works**: mechanism and evidence.
- **Novelty split**: `核心创新 / 辅助设计 / 工程实现`.
- **Strongest supporting experiment**.
- **One-sentence real novelty**.

Compare with the direct baseline, not a vague field average. Do not equate the number of modules with novelty.

## `/why-important`

Return:

- why the problem matters;
- why prior work did not solve it adequately;
- the observation that unlocked the solution;
- the most valuable contribution;
- the easily missed contribution;
- what the evidence says about impact versus what remains speculative.

Do not infer acceptance reasons from venue prestige. Phrase “why publishable” as a technical assessment unless reviewer evidence is available.

## `/reviewer`

Return:

- **Strengths** tied to evidence.
- **Major weaknesses** and affected claims.
- **Assumptions / scope limits**.
- **Missing experiment**: what it would test and which claim it resolves.
- **Reviewer questions**.
- **Potential extensions** marked `[AI 推断]`.
- **Verdict boundary**: what is established, suggested, and not shown.

Avoid manufacturing flaws. A limitation must follow from the paper, its evaluation, or a clearly stated inference.

## `/compare <A> <B> ...`

First resolve exact paper identities. Align the comparison on:

| Dimension | Paper A | Paper B |
|---|---|---|
| Problem and setting | | |
| Direct baseline | | |
| Core insight | | |
| Input / pose | | |
| Representation | | |
| Initialization | | |
| Optimization | | |
| Renderer / rasterizer | | |
| Loss / supervision | | |
| Datasets and metrics | | |
| Geometry evidence | | |
| Rendering evidence | | |
| Cost / limitations | | |

Then answer:

- the true difference;
- same problem or adjacent problem;
- direct competitors, complementary methods, or incomparable settings;
- what would make a fair comparison;
- evidence and confidence for each non-obvious conclusion.

Do not compare numbers across different datasets, protocols, resolutions, or train/test splits as if they were controlled.

## `/related`

Return 3–5 verified papers total, selected by role rather than popularity:

- **Prerequisite**.
- **Direct baseline**.
- **Same problem / alternative route**.
- **Follow-up** when one exists.

For each paper include title, venue/year if verified, primary link, role, and one sentence explaining why to read it. Separate official code status from paper availability. If only two papers are truly useful, return two.

## `/note`

Create a durable note with:

```text
# Paper
## One sentence
## Problem and motivation
## Core insight
## Pipeline delta
## Method
## Key figure
## Key equation
## Experimental evidence
## Strongest result
## Limitations and assumptions
## Related papers
## My takeaway
## Potential extension [AI 推断]
## Evidence index
```

Avoid duplicating the same explanation under multiple headings. Use links or short cross-references inside the note.

## `/map`

Without arguments, summarize the active paper's 3–5 strongest relations and label each edge with type, source status, confidence, and evidence. With an explicit save/update request, use the map script and validate afterward.

Text view:

```text
Paper A --IMPROVES--> Paper B
Source: paper_evidence
Evidence: §1 explicitly frames B as the baseline and Table 3 reports the controlled gain.
Confidence: 0.95
```

Use solid-edge language only for paper or externally verified evidence. Describe AI-inferred relations as tentative; never convert semantic similarity alone into `IMPROVES` or `FOLLOW_UP`.

