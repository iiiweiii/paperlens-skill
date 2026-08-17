#!/usr/bin/env python3
"""Create, validate, update, and summarize a lightweight PaperLens map."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


RELATION_TYPES = {"BASED_ON", "IMPROVES", "SAME_PROBLEM", "SIMILAR_METHOD", "FOLLOW_UP"}
SOURCE_TYPES = {"paper_evidence", "external_verified", "ai_inferred"}
EMPTY_MAP = {"schema_version": 1, "papers": [], "relations": []}


class MapError(ValueError):
    pass


def load_map(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MapError(f"Map does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise MapError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    validate_map(data)
    return data


def validate_map(data: Any) -> None:
    if not isinstance(data, dict):
        raise MapError("Map root must be an object")
    if data.get("schema_version") != 1:
        raise MapError("schema_version must be 1")
    papers = data.get("papers")
    relations = data.get("relations")
    if not isinstance(papers, list) or not isinstance(relations, list):
        raise MapError("papers and relations must be arrays")

    paper_ids: set[str] = set()
    for index, paper in enumerate(papers):
        if not isinstance(paper, dict):
            raise MapError(f"papers[{index}] must be an object")
        required = {"id", "title", "year", "problem", "core_idea", "methods", "tags"}
        missing = required - set(paper)
        if missing:
            raise MapError(f"papers[{index}] missing: {', '.join(sorted(missing))}")
        paper_id = paper["id"]
        if not isinstance(paper_id, str) or not paper_id.strip():
            raise MapError(f"papers[{index}].id must be a non-empty string")
        if paper_id in paper_ids:
            raise MapError(f"Duplicate paper id: {paper_id}")
        paper_ids.add(paper_id)
        if not isinstance(paper["title"], str) or not paper["title"].strip():
            raise MapError(f"papers[{index}].title must be a non-empty string")
        if paper["year"] is not None and not isinstance(paper["year"], int):
            raise MapError(f"papers[{index}].year must be an integer or null")
        for key in ("problem", "core_idea"):
            if not isinstance(paper[key], str):
                raise MapError(f"papers[{index}].{key} must be a string")
        for key in ("methods", "tags"):
            if not isinstance(paper[key], list) or not all(isinstance(v, str) for v in paper[key]):
                raise MapError(f"papers[{index}].{key} must be an array of strings")

    seen_relations: set[tuple[str, str, str]] = set()
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            raise MapError(f"relations[{index}] must be an object")
        required = {"source", "target", "type", "confidence", "evidence", "source_type", "locator"}
        missing = required - set(relation)
        if missing:
            raise MapError(f"relations[{index}] missing: {', '.join(sorted(missing))}")
        source, target = relation["source"], relation["target"]
        if source not in paper_ids or target not in paper_ids:
            raise MapError(f"relations[{index}] has an unknown source or target")
        if source == target:
            raise MapError(f"relations[{index}] cannot be a self-edge")
        relation_type = relation["type"]
        if relation_type not in RELATION_TYPES:
            raise MapError(f"relations[{index}].type must be one of {sorted(RELATION_TYPES)}")
        key = (source, target, relation_type)
        if key in seen_relations:
            raise MapError(f"Duplicate relation: {source} {relation_type} {target}")
        seen_relations.add(key)
        confidence = relation["confidence"]
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            raise MapError(f"relations[{index}].confidence must be between 0 and 1")
        if relation["source_type"] not in SOURCE_TYPES:
            raise MapError(f"relations[{index}].source_type must be one of {sorted(SOURCE_TYPES)}")
        if not isinstance(relation["evidence"], str) or not relation["evidence"].strip():
            raise MapError(f"relations[{index}].evidence must be a non-empty string")
        if relation["locator"] is not None and not isinstance(relation["locator"], str):
            raise MapError(f"relations[{index}].locator must be a string or null")


def save_map(path: Path, data: dict[str, Any]) -> None:
    validate_map(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if path.exists() and not args.force:
        raise MapError(f"Refusing to overwrite existing map: {path}. Use --force explicitly.")
    save_map(path, json.loads(json.dumps(EMPTY_MAP)))
    print(f"Initialized {path}")


def cmd_add_paper(args: argparse.Namespace) -> None:
    path = Path(args.path)
    data = load_map(path)
    if any(paper["id"] == args.id for paper in data["papers"]):
        raise MapError(f"Paper id already exists: {args.id}")
    data["papers"].append({
        "id": args.id,
        "title": args.title,
        "year": args.year,
        "problem": args.problem,
        "core_idea": args.core_idea,
        "methods": args.methods or [],
        "tags": args.tags or [],
    })
    save_map(path, data)
    print(f"Added paper {args.id}")


def cmd_add_relation(args: argparse.Namespace) -> None:
    path = Path(args.path)
    data = load_map(path)
    data["relations"].append({
        "source": args.source,
        "target": args.target,
        "type": args.type,
        "confidence": round(args.confidence, 2),
        "evidence": args.evidence,
        "source_type": args.source_type,
        "locator": args.locator,
    })
    save_map(path, data)
    print(f"Added relation {args.source} --{args.type}--> {args.target}")


def cmd_validate(args: argparse.Namespace) -> None:
    data = load_map(Path(args.path))
    print(f"Valid map: {len(data['papers'])} papers, {len(data['relations'])} relations")


def cmd_show(args: argparse.Namespace) -> None:
    data = load_map(Path(args.path))
    papers = {paper["id"]: paper for paper in data["papers"]}
    relations = data["relations"]
    if args.paper:
        if args.paper not in papers:
            raise MapError(f"Unknown paper id: {args.paper}")
        relations = [r for r in relations if r["source"] == args.paper or r["target"] == args.paper]
        print(f"{papers[args.paper]['title']} ({args.paper})")
    else:
        print(f"PaperLens map: {len(papers)} papers, {len(relations)} relations")
    for relation in sorted(relations, key=lambda r: r["confidence"], reverse=True):
        locator = f"; {relation['locator']}" if relation["locator"] else ""
        print(
            f"- {relation['source']} --{relation['type']}--> {relation['target']} "
            f"[{relation['source_type']}, {relation['confidence']:.2f}{locator}]\n"
            f"  Evidence: {relation['evidence']}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create an empty map")
    init_parser.add_argument("path")
    init_parser.add_argument("--force", action="store_true")
    init_parser.set_defaults(func=cmd_init)

    paper_parser = subparsers.add_parser("add-paper", help="Add one paper")
    paper_parser.add_argument("path")
    paper_parser.add_argument("--id", required=True)
    paper_parser.add_argument("--title", required=True)
    paper_parser.add_argument("--year", type=int)
    paper_parser.add_argument("--problem", default="")
    paper_parser.add_argument("--core-idea", default="")
    paper_parser.add_argument("--methods", nargs="*")
    paper_parser.add_argument("--tags", nargs="*")
    paper_parser.set_defaults(func=cmd_add_paper)

    relation_parser = subparsers.add_parser("add-relation", help="Add one relation")
    relation_parser.add_argument("path")
    relation_parser.add_argument("--source", required=True)
    relation_parser.add_argument("--target", required=True)
    relation_parser.add_argument("--type", choices=sorted(RELATION_TYPES), required=True)
    relation_parser.add_argument("--confidence", type=float, required=True)
    relation_parser.add_argument("--evidence", required=True)
    relation_parser.add_argument("--source-type", choices=sorted(SOURCE_TYPES), required=True)
    relation_parser.add_argument("--locator")
    relation_parser.set_defaults(func=cmd_add_relation)

    validate_parser = subparsers.add_parser("validate", help="Validate a map")
    validate_parser.add_argument("path")
    validate_parser.set_defaults(func=cmd_validate)

    show_parser = subparsers.add_parser("show", help="Print a compact text view")
    show_parser.add_argument("path")
    show_parser.add_argument("--paper")
    show_parser.set_defaults(func=cmd_show)
    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.func(args)
        return 0
    except MapError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

