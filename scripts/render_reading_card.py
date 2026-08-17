#!/usr/bin/env python3
"""Render PaperLens Reading Card JSON as a self-contained HTML file."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


EXAMPLE: dict[str, Any] = {
    "title": "Example Vision Paper",
    "metadata": [
        {"label": "Venue", "value": "Verified venue/year"},
        {"label": "Task", "value": "Novel-view synthesis"},
        {"label": "Representation", "value": "Example representation"},
    ],
    "decision": {
        "why_read": "Learn how the method addresses one precise baseline failure.",
        "outcome": "Judge whether the proposed change improves the claimed stage.",
        "quick_minutes": 15,
        "deep_minutes": 60,
        "priority": "High",
    },
    "core": {
        "problem": "The direct baseline fails under the paper's target condition.",
        "baseline_failure": "Its representation or renderer ignores the relevant constraint.",
        "key_insight": "Move the constraint into the stage where the failure originates.",
    },
    "pipeline": [
        {"name": "Input", "status": "reused"},
        {"name": "Pose", "status": "reused"},
        {"name": "Representation", "status": "changed"},
        {"name": "Optimization", "status": "reused"},
        {"name": "Rendering", "status": "changed"},
        {"name": "Evaluation", "status": "reused"},
    ],
    "actions": {
        "must_read": [
            {"locator": "Fig. 2", "purpose": "Build the global method picture."},
            {"locator": "§3.2", "purpose": "Understand the changed module."},
        ],
        "later": [{"locator": "Related Work", "purpose": "Return only for terminology."}],
        "prerequisite": [{"locator": "Baseline paper §3", "purpose": "Recall the original stage."}],
    },
    "route": [
        {
            "name": "建立全局图",
            "locator": "Fig. 2",
            "purpose": "Identify input, representation, changed stages, and output.",
            "exit_question": "Which stages are changed and which are reused?",
        },
        {
            "name": "定位失败原因",
            "locator": "Introduction + Fig. 1",
            "purpose": "Connect the motivating failure to a specific baseline assumption.",
            "exit_question": "Why does the baseline fail in this setting?",
        },
        {
            "name": "拆核心机制",
            "locator": "§3.2 + Eq. 7",
            "purpose": "Trace cause, operation, and intended effect.",
            "exit_question": "What changes mathematically and where does it enter the pipeline?",
        },
        {
            "name": "检查证据",
            "locator": "Table 2 + Table 3",
            "purpose": "Compare the main result with the targeted ablation.",
            "exit_question": "Which evidence isolates the contribution of the changed module?",
        },
        {
            "name": "确认边界",
            "locator": "Limitations / failure cases",
            "purpose": "Identify assumptions and unsupported generalizations.",
            "exit_question": "Under what condition should the claim not be extended?",
        },
    ],
    "detour": {
        "after_step": 2,
        "condition": "You cannot state the original baseline assumption.",
        "action": "Read only the baseline paper's representation section, then return to step 3.",
    },
    "difficulty": [
        {"label": "数学", "rating": 3, "reason": "One key derivation"},
        {"label": "代码", "rating": 4, "reason": "Custom rendering stage"},
        {"label": "背景", "rating": 3, "reason": "Baseline familiarity"},
    ],
    "evidence": {
        "status": "Attached PDF inspected",
        "confidence": "High",
        "locators": "Fig. 1–2, §3.2, Eq. 7, Tables 2–3",
        "missing": "External historical positioning not checked",
    },
    "start_here": "Open Fig. 2 and identify the input, representation, changed stages, and output.",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def require(data: dict[str, Any]) -> None:
    required = {
        "title",
        "metadata",
        "decision",
        "core",
        "pipeline",
        "actions",
        "route",
        "difficulty",
        "evidence",
        "start_here",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")
    if not isinstance(data["route"], list) or not data["route"]:
        raise ValueError("route must contain at least one reading stage")
    for stage in data["pipeline"]:
        if stage.get("status") not in {"changed", "reused", "na"}:
            raise ValueError("pipeline status must be changed, reused, or na")


def render_items(items: list[dict[str, Any]], empty: str) -> str:
    if not items:
        return f'<p class="muted">{esc(empty)}</p>'
    return "".join(
        f'<div class="action-item"><code>{esc(item.get("locator", "未定位"))}</code>'
        f'<span>{esc(item.get("purpose", ""))}</span></div>'
        for item in items
    )


def render(data: dict[str, Any]) -> str:
    require(data)
    metadata = "".join(
        f'<span class="chip"><b>{esc(item.get("label", ""))}</b>{esc(item.get("value", "未核实"))}</span>'
        for item in data["metadata"]
    )
    decision = data["decision"]
    core = data["core"]
    pipeline_parts: list[str] = []
    for index, stage in enumerate(data["pipeline"]):
        if index:
            pipeline_parts.append('<span class="pipe-arrow" aria-hidden="true">→</span>')
        status = stage["status"]
        marker = "★ " if status == "changed" else ""
        pipeline_parts.append(
            f'<div class="pipe-node {esc(status)}"><span>{esc(marker + stage["name"])}</span>'
            f'<small>{esc(status)}</small></div>'
        )
    actions = data["actions"]
    route_parts: list[str] = []
    detour = data.get("detour")
    for number, stage in enumerate(data["route"], 1):
        route_parts.append(
            '<article class="route-step">'
            f'<div class="route-number">{number:02d}</div>'
            '<div class="route-content">'
            f'<div class="route-heading"><h3>{esc(stage["name"])}</h3><code>{esc(stage["locator"])}</code></div>'
            f'<p>{esc(stage["purpose"])}</p>'
            f'<div class="exit"><span>离开前回答</span>{esc(stage["exit_question"])}</div>'
            '</div></article>'
        )
        if detour and number == int(detour.get("after_step", -1)):
            route_parts.append(
                '<aside class="detour">'
                f'<b>↳ 第 {number} 站旁路</b>'
                f'<span>如果：{esc(detour.get("condition", ""))}</span>'
                f'<span>只做：{esc(detour.get("action", ""))}</span>'
                '</aside>'
            )
    difficulty = "".join(
        f'<div class="difficulty"><b>{esc(item["label"])}</b>'
        f'<span class="stars">{"★" * int(item["rating"])}{"☆" * (5 - int(item["rating"]))}</span>'
        f'<small>{esc(item["reason"])}</small></div>'
        for item in data["difficulty"]
    )
    evidence = data["evidence"]

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(data["title"])} · PaperLens</title>
<style>
:root{{--bg:#f3f5f9;--surface:#fff;--surface-2:#f8fafc;--text:#172033;--muted:#647087;--line:#dce2ec;--brand:#5b5bd6;--brand-soft:#eeeeff;--teal:#087f8c;--teal-soft:#e7f7f6;--warn:#b65c12;--warn-soft:#fff3df;--shadow:0 18px 50px rgba(35,45,75,.10)}}
[data-theme="dark"]{{--bg:#0c1019;--surface:#151b27;--surface-2:#1b2331;--text:#eef2fb;--muted:#9ca8bc;--line:#2c3749;--brand:#9999ff;--brand-soft:#29294a;--teal:#54d2d9;--teal-soft:#15373a;--warn:#ffb267;--warn-soft:#3c2b1d;--shadow:0 18px 50px rgba(0,0,0,.32)}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 system-ui,-apple-system,"Segoe UI","PingFang SC",sans-serif}} .page{{max-width:1120px;margin:auto;padding:32px 20px 64px}} .shell{{background:var(--surface);border:1px solid var(--line);border-radius:26px;box-shadow:var(--shadow);overflow:hidden}} header{{padding:38px 42px 30px;background:linear-gradient(135deg,var(--brand-soft),var(--surface) 58%,var(--teal-soft))}} .eyebrow{{color:var(--brand);font-weight:800;letter-spacing:.1em;text-transform:uppercase}} h1{{font-size:clamp(26px,4vw,46px);line-height:1.15;margin:10px 0 18px;max-width:900px}} .chips{{display:flex;flex-wrap:wrap;gap:9px}} .chip{{display:flex;gap:7px;padding:7px 11px;border:1px solid var(--line);border-radius:999px;background:color-mix(in srgb,var(--surface) 80%,transparent);font-size:13px}} .theme{{position:fixed;right:18px;top:18px;border:1px solid var(--line);background:var(--surface);color:var(--text);border-radius:999px;padding:9px 13px;cursor:pointer;z-index:5}} section{{padding:34px 42px;border-top:1px solid var(--line)}} .section-head{{display:flex;align-items:baseline;gap:12px;margin-bottom:22px}} h2{{font-size:22px;margin:0}} .section-no{{color:var(--brand);font-weight:850}} .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}} .panel{{background:var(--surface-2);border:1px solid var(--line);border-radius:17px;padding:20px;min-height:142px}} .panel .label{{display:block;color:var(--muted);font-size:13px;font-weight:750;margin-bottom:10px}} .panel strong{{font-size:17px}} .metrics{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}} .metric{{background:var(--brand-soft);color:var(--brand);padding:6px 10px;border-radius:10px;font-size:13px;font-weight:750}} .core .panel:nth-child(2){{border-color:color-mix(in srgb,var(--warn) 35%,var(--line))}} .core .panel:nth-child(3){{border-color:color-mix(in srgb,var(--teal) 35%,var(--line))}} .pipeline{{display:flex;align-items:center;gap:10px;overflow-x:auto;padding:20px 4px 8px}} .pipe-node{{min-width:122px;text-align:center;padding:12px;border:1px solid var(--line);border-radius:13px;background:var(--surface-2)}} .pipe-node span{{display:block;font-weight:800}} .pipe-node small{{color:var(--muted)}} .pipe-node.changed{{background:var(--brand-soft);border:2px solid var(--brand);color:var(--brand)}} .pipe-node.na{{opacity:.55}} .pipe-arrow{{color:var(--muted);font-size:24px}} .action-grid{{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:16px}} .action-col{{border:1px solid var(--line);border-radius:17px;padding:18px}} .action-col h3{{margin:0 0 14px}} .action-item{{display:grid;grid-template-columns:max-content 1fr;gap:10px;padding:11px 0;border-top:1px dashed var(--line)}} .action-item:first-of-type{{border-top:0}} code{{background:var(--surface-2);border:1px solid var(--line);border-radius:8px;padding:3px 7px;color:var(--brand);font:600 13px ui-monospace,monospace}} .journey{{position:relative;max-width:880px;margin:0 auto}} .journey:before{{content:"";position:absolute;left:28px;top:25px;bottom:25px;width:2px;background:linear-gradient(var(--brand),var(--teal))}} .route-step{{position:relative;display:grid;grid-template-columns:58px 1fr;gap:20px;margin:0 0 20px}} .route-number{{width:58px;height:58px;border-radius:17px;background:var(--brand);color:white;display:grid;place-items:center;font-weight:850;z-index:1;box-shadow:0 8px 20px color-mix(in srgb,var(--brand) 35%,transparent)}} .route-content{{border:1px solid var(--line);border-radius:18px;padding:20px 22px;background:var(--surface-2)}} .route-heading{{display:flex;justify-content:space-between;gap:12px;align-items:center}} .route-heading h3{{font-size:19px;margin:0}} .route-content p{{margin:10px 0 13px}} .exit{{display:grid;grid-template-columns:max-content 1fr;gap:10px;padding:10px 12px;border-radius:11px;background:var(--teal-soft)}} .exit span{{color:var(--teal);font-size:12px;font-weight:850;text-transform:uppercase;letter-spacing:.05em}} .detour{{margin:6px 0 22px 78px;display:grid;gap:5px;padding:15px 18px;border:1px dashed var(--warn);border-radius:14px;background:var(--warn-soft);color:var(--text)}} .detour b{{color:var(--warn)}} .difficulty-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}} .difficulty{{display:grid;gap:4px;border:1px solid var(--line);border-radius:14px;padding:15px}} .stars{{color:#e39b18;letter-spacing:2px}} .difficulty small,.muted{{color:var(--muted)}} .evidence{{display:grid;grid-template-columns:repeat(2,1fr);gap:13px;margin-top:18px}} .evidence div{{background:var(--surface-2);border-radius:13px;padding:14px}} .evidence b{{display:block;color:var(--muted);font-size:12px;text-transform:uppercase}} .cta{{margin:0 42px 42px;padding:22px 25px;border-radius:18px;background:linear-gradient(135deg,var(--brand),#7777e8);color:white}} .cta small{{display:block;font-weight:800;letter-spacing:.08em;margin-bottom:4px}} .cta strong{{font-size:19px}} @media(max-width:760px){{.page{{padding:14px 10px 36px}} header,section{{padding:27px 21px}} .grid,.action-grid,.difficulty-grid,.evidence{{grid-template-columns:1fr}} .panel{{min-height:0}} .route-heading{{align-items:flex-start;flex-direction:column}} .exit{{grid-template-columns:1fr}} .detour{{margin-left:0}} .cta{{margin:0 21px 27px}} .theme{{position:absolute}}}}
</style>
</head>
<body>
<button class="theme" type="button" onclick="document.documentElement.dataset.theme=document.documentElement.dataset.theme==='dark'?'light':'dark'" aria-label="切换明暗主题">◐ 主题</button>
<main class="page"><article class="shell">
<header><div class="eyebrow">PaperLens · Reading Card</div><h1>{esc(data["title"])}</h1><div class="chips">{metadata}</div></header>
<section><div class="section-head"><span class="section-no">01</span><h2>先决定：值不值得读</h2></div><div class="grid">
<div class="panel"><span class="label">为什么读</span><strong>{esc(decision["why_read"])}</strong></div>
<div class="panel"><span class="label">读完以后，你应该能判断</span><strong>{esc(decision["outcome"])}</strong></div>
<div class="panel"><span class="label">阅读投入</span><div class="metrics"><span class="metric">快读 {esc(decision["quick_minutes"])} min</span><span class="metric">深读 {esc(decision["deep_minutes"])} min</span><span class="metric">优先级 {esc(decision["priority"])}</span></div></div></div></section>
<section><div class="section-head"><span class="section-no">02</span><h2>方法主线</h2></div><div class="grid core">
<div class="panel"><span class="label">🎯 问题</span><strong>{esc(core["problem"])}</strong></div>
<div class="panel"><span class="label">⚠️ 原方法为什么不行</span><strong>{esc(core["baseline_failure"])}</strong></div>
<div class="panel"><span class="label">💡 关键洞察</span><strong>{esc(core["key_insight"])}</strong></div></div><div class="pipeline">{''.join(pipeline_parts)}</div></section>
<section><div class="section-head"><span class="section-no">03</span><h2>阅读取舍</h2></div><div class="action-grid">
<div class="action-col"><h3>✅ 必看</h3>{render_items(actions.get("must_read", []), "未定位")}</div>
<div class="action-col"><h3>⏭️ 稍后再读</h3>{render_items(actions.get("later", []), "无")}</div>
<div class="action-col"><h3>🧊 先补背景</h3>{render_items(actions.get("prerequisite", []), "无")}</div></div></section>
<section><div class="section-head"><span class="section-no">04</span><h2>阅读旅程</h2></div><div class="journey">{''.join(route_parts)}</div></section>
<section><div class="section-head"><span class="section-no">05</span><h2>难度与可信度</h2></div><div class="difficulty-grid">{difficulty}</div><div class="evidence">
<div><b>Evidence status</b>{esc(evidence["status"])}</div><div><b>Confidence</b>{esc(evidence["confidence"])}</div><div><b>Locators</b>{esc(evidence["locators"])}</div><div><b>Missing / unverified</b>{esc(evidence["missing"])}</div></div></section>
<div class="cta"><small>▶ START HERE</small><strong>{esc(data["start_here"])}</strong></div>
</article></main></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="UTF-8 Reading Card JSON")
    parser.add_argument("output", nargs="?", help="Output HTML path")
    parser.add_argument("--example", action="store_true", help="Print example JSON and exit")
    parser.add_argument("--demo", help="Render the built-in example to this HTML path")
    args = parser.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return 0
    if args.demo:
        destination = Path(args.demo)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render(EXAMPLE), encoding="utf-8")
        print(destination.resolve())
        return 0
    if not args.input or not args.output:
        parser.error("input and output are required unless --example is used")
    source = Path(args.input)
    destination = Path(args.output)
    data = json.loads(source.read_text(encoding="utf-8"))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(data), encoding="utf-8")
    print(destination.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
