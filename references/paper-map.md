# Lightweight Paper Map

## Scope

Keep the map useful for reading recall, not exhaustive bibliography. Add one paper node after it has a stable identity and a minimal Paper DNA. Add at most 3–5 high-value edges per paper.

Store mutable data in the active workspace, normally `paperlens-data/paper-map.json`. Never write personal research data into the installed skill folder.

## Paper schema

Required:

- `id`: stable lowercase slug, preferably `first-author-year-short-title`.
- `title`: verified full title.
- `year`: integer or `null` when unverified.
- `problem`: one concise sentence.
- `core_idea`: one concise sentence.
- `methods`: short controlled tags.
- `tags`: domain/task tags.

## Relation schema

Allowed types:

- `BASED_ON`: source explicitly builds on target.
- `IMPROVES`: source targets a limitation of target and provides relevant evidence.
- `SAME_PROBLEM`: papers address the same defined problem, possibly by different routes.
- `SIMILAR_METHOD`: method mechanism is materially similar; semantic proximity alone is insufficient.
- `FOLLOW_UP`: source is temporally later and explicitly follows or extends target.

Every relation requires source and target IDs, type, confidence from 0 to 1, concise evidence, `source_type` (`paper_evidence`, `external_verified`, or `ai_inferred`), and a locator when one exists.

## Decision rules

- Prefer `BASED_ON` over vague similarity when the source paper states the dependency.
- Use `IMPROVES` only when the compared limitation and improvement are aligned.
- Use `SAME_PROBLEM` when settings are comparable; otherwise explain the scope difference.
- Use `SIMILAR_METHOD` for a shared mechanism, not shared keywords.
- Use `FOLLOW_UP` only with temporal and documentary evidence.
- Omit relations below 0.55 from the default view.
- Never create inverse edges automatically.
- Do not merge preprint and final versions as separate papers unless the user wants version tracking.

## Script usage

Initialize:

```powershell
python scripts/paper_map.py init paperlens-data/paper-map.json
```

Add a paper:

```powershell
python scripts/paper_map.py add-paper paperlens-data/paper-map.json --id kerbl-2023-3dgs --title "3D Gaussian Splatting for Real-Time Radiance Field Rendering" --year 2023 --problem "Real-time high-quality novel-view rendering" --core-idea "Optimize anisotropic 3D Gaussians and rasterize them with visibility-aware splatting" --methods 3dgs splatting --tags novel-view-synthesis rendering
```

Add a relation:

```powershell
python scripts/paper_map.py add-relation paperlens-data/paper-map.json --source newer-paper --target kerbl-2023-3dgs --type BASED_ON --confidence 0.96 --source-type paper_evidence --evidence "The introduction explicitly states that the method builds on 3DGS." --locator "§1"
```

Validate and show:

```powershell
python scripts/paper_map.py validate paperlens-data/paper-map.json
python scripts/paper_map.py show paperlens-data/paper-map.json
```

The script refuses duplicate paper IDs, dangling edges, invalid relation types, out-of-range confidence, and overwriting an existing map during initialization.

