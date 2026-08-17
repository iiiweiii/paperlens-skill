# Evidence and confidence

## Evidence statuses

Use one status per claim:

| Label | Meaning | Minimum support |
|---|---|---|
| `[论文事实]` | Direct author statement, definition, method detail, or reported result | Exact paper locator |
| `[论文内归纳]` | Synthesis across paper evidence | Two or more locators, or one locator plus an explicit reasoning bridge |
| `[外部已核实]` | Current fact verified outside the PDF | Primary URL and access context |
| `[AI 推断]` | Interpretation, critique, causal hypothesis, or extension | Evidence used plus reasoning |
| `[论文未说明]` | The paper does not establish the requested fact | State what was checked |

Use direct quotation sparingly. Prefer paraphrase plus an exact locator.

## Confidence scale

Use categorical confidence for explanations:

- **High**: explicit statement/result with an unambiguous locator; or a straightforward synthesis with converging evidence.
- **Medium**: reasonable synthesis with partial evidence, ambiguous terminology, or incomplete experimental isolation.
- **Low**: plausible interpretation, weakly supported causal claim, missing source, or uncertain paper identity.

For graph relations, also store a numeric value from 0 to 1 because the schema requires sorting. Calibrate it as:

- `0.90–1.00`: explicit relation plus exact evidence.
- `0.75–0.89`: strong multi-source or structural evidence.
- `0.55–0.74`: AI-inferred but plausible relation.
- below `0.55`: omit from the default map and mention only as a hypothesis if useful.

Do not report more than two decimal places. Numeric confidence is an audit aid, not a probability estimate.

## Locator rules

Prefer, in order:

1. equation, figure, table, algorithm, or section identifier;
2. page plus paragraph/heading;
3. appendix identifier;
4. short unique phrase when extraction has unreliable pages.

If the PDF is a preprint with shifting page numbers, cite stable object identifiers and the version/date. Never invent a locator from memory.

## Claim-evidence block

Use this compact shape for a central claim:

```text
[论文内归纳] The method moves anti-aliasing into both the 3D representation and 2D rendering stages.
Evidence: §3.1 (3D smoothing), §3.2 and Eq. 7 (2D filter).
Confidence: High.
```

For a reviewer inference:

```text
[AI 推断] The reported gain may depend on the tested scale range.
Evidence: experiments cover scales X–Y; no out-of-range study is reported.
Confidence: Medium.
```

## External verification

Use primary sources for title, authors, venue, year, code, project status, and acceptance category. Prefer official proceedings/schedules, publishers/DOIs, arXiv, project pages, and author-owned repositories. Mark conflicts and version differences. Search snippets, aggregators, and repository forks are discovery aids, not final evidence.

## What experiments support

- A controlled ablation supports the contribution of the removed/changed component under that protocol.
- A benchmark improvement supports empirical performance on that benchmark, not universal superiority.
- PSNR/SSIM/LPIPS support rendering or perceptual quality, not geometric accuracy.
- FPS and memory support efficiency only under comparable hardware, resolution, and implementation.
- Qualitative examples illustrate behavior but rarely establish average performance.

