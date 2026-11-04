#!/usr/bin/env python3
"""Summarise Lighthouse or PageSpeed Insights JSON for a Core Web Vitals pass.

Standard library only, no network. Accepts:
  - a Lighthouse report saved with --output=json (the "lhr" object), or
  - a PageSpeed Insights API v5 response (it contains field data in
    loadingExperience / originLoadingExperience and lab data in lighthouseResult).

Prints field data (CrUX p75 for LCP, INP, CLS) when present, lab metrics
(LCP, CLS, TBT, FCP, Speed Index, server response), the LCP element, and the
failing audits or insights with their estimated metric savings. Works with
both the older audit IDs and the Lighthouse 13 "-insight" IDs.

Thresholds (p75): LCP good <= 2500 ms, poor > 4000 ms; INP good <= 200 ms,
poor > 500 ms; CLS good <= 0.1, poor > 0.25. TBT is a lab proxy for
responsiveness; INP needs real interactions (field data or a timespan run).

Usage:
  cwv_report.py report.json
  cwv_report.py before.json after.json      # adds a before/after delta table
  cwv_report.py report.json --top 15        # show more failing audits

Exit status: 0 on success, 2 on unreadable input.
"""

from __future__ import annotations

import argparse
import json
import sys

FIELD_KEYS = {
    "LCP": ("LARGEST_CONTENTFUL_PAINT_MS", 1.0, "ms"),
    "INP": ("INTERACTION_TO_NEXT_PAINT", 1.0, "ms"),
    "CLS": ("CUMULATIVE_LAYOUT_SHIFT_SCORE", 0.01, ""),
    "FCP": ("FIRST_CONTENTFUL_PAINT_MS", 1.0, "ms"),
    "TTFB": ("EXPERIMENTAL_TIME_TO_FIRST_BYTE", 1.0, "ms"),
}
THRESHOLDS = {"LCP": (2500, 4000), "INP": (200, 500), "CLS": (0.1, 0.25), "TBT": (200, 600), "FCP": (1800, 3000), "TTFB": (800, 1800)}
LAB_AUDITS = [
    ("LCP", ["largest-contentful-paint"]),
    ("CLS", ["cumulative-layout-shift"]),
    ("TBT", ["total-blocking-time"]),
    ("INP", ["interaction-to-next-paint"]),
    ("FCP", ["first-contentful-paint"]),
    ("SI", ["speed-index"]),
    ("TTFB", ["server-response-time", "document-latency-insight"]),
]
METRIC_AUDIT_IDS = {a for _, ids in LAB_AUDITS for a in ids} | {"interactive", "max-potential-fid", "first-meaningful-paint"}


def rate(metric: str, value: float | None) -> str:
    if value is None or metric not in THRESHOLDS:
        return ""
    good, poor = THRESHOLDS[metric]
    return "good" if value <= good else ("poor" if value > poor else "needs improvement")


def fmt(metric: str, value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.3f}" if metric == "CLS" else f"{value:,.0f} ms"


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if "lighthouseResult" in data:
        return {"lhr": data["lighthouseResult"], "field": data.get("loadingExperience"), "origin": data.get("originLoadingExperience")}
    if "audits" in data:
        return {"lhr": data, "field": None, "origin": None}
    raise ValueError("not a Lighthouse or PageSpeed Insights JSON file")


def field_metrics(block: dict | None) -> dict:
    out = {}
    if not block or "metrics" not in block:
        return out
    for name, (key, scale, _) in FIELD_KEYS.items():
        m = block["metrics"].get(key)
        if m and "percentile" in m:
            out[name] = m["percentile"] * scale
    return out


def lab_metrics(lhr: dict) -> dict:
    audits = lhr.get("audits", {})
    out = {}
    for name, ids in LAB_AUDITS:
        for aid in ids:
            a = audits.get(aid)
            if a and isinstance(a.get("numericValue"), (int, float)):
                out[name] = float(a["numericValue"])
                break
    return out


def find_snippet(obj) -> str | None:
    if isinstance(obj, dict):
        node = obj.get("node")
        if isinstance(node, dict) and node.get("snippet"):
            return node["snippet"]
        if obj.get("type") == "node" and obj.get("snippet"):
            return obj["snippet"]
        for v in obj.values():
            s = find_snippet(v)
            if s:
                return s
    elif isinstance(obj, list):
        for v in obj:
            s = find_snippet(v)
            if s:
                return s
    return None


def lcp_element(lhr: dict) -> str | None:
    audits = lhr.get("audits", {})
    for aid in ("largest-contentful-paint-element", "lcp-breakdown-insight", "lcp-phases-insight", "lcp-discovery-insight"):
        if aid in audits:
            s = find_snippet(audits[aid].get("details"))
            if s:
                return s
    return None


def failing(lhr: dict, top: int) -> list[tuple[str, str, str, str]]:
    rows = []
    perf_ids = None
    cat = lhr.get("categories", {}).get("performance")
    if cat:
        perf_ids = {ref["id"] for ref in cat.get("auditRefs", [])}
    for aid, a in lhr.get("audits", {}).items():
        if aid in METRIC_AUDIT_IDS:
            continue
        if perf_ids is not None and aid not in perf_ids:
            continue
        score = a.get("score")
        mode = a.get("scoreDisplayMode")
        if mode in ("notApplicable", "manual", "informative") and not a.get("metricSavings"):
            continue
        if score is not None and score >= 0.9:
            continue
        savings = a.get("metricSavings") or {}
        weight = savings.get("LCP", 0) + savings.get("FCP", 0) * 0.5 + savings.get("TBT", 0) + savings.get("INP", 0) + savings.get("CLS", 0) * 10000
        sav = ", ".join(f"{k} {v:.3f}" if k == "CLS" else f"{k} {v:,.0f} ms" for k, v in savings.items() if v)
        rows.append((weight, aid, a.get("title", ""), a.get("displayValue", ""), sav))
    rows.sort(key=lambda r: r[0], reverse=True)
    return [(aid, title, dv, sav) for _, aid, title, dv, sav in rows[:top]]


def report(path: str, top: int) -> dict:
    d = load(path)
    lhr = d["lhr"]
    lab = lab_metrics(lhr)
    field = field_metrics(d["field"])
    origin = field_metrics(d["origin"])
    env = lhr.get("configSettings", {})
    print(f"== {path}")
    print(f"url: {lhr.get('finalDisplayedUrl') or lhr.get('finalUrl') or lhr.get('requestedUrl')}")
    print(f"lighthouse {lhr.get('lighthouseVersion', '?')}, form factor: {env.get('formFactor', '?')}, throttling: {env.get('throttlingMethod', '?')}")
    perf = lhr.get("categories", {}).get("performance", {}).get("score")
    if perf is not None:
        print(f"performance score: {perf * 100:.0f}")
    for label, data in (("field (this URL, p75, last 28 days)", field), ("field (origin, p75)", origin)):
        if data:
            print(label + ":")
            for m in ("LCP", "INP", "CLS", "FCP", "TTFB"):
                if m in data:
                    print(f"  {m:<5} {fmt(m, data[m]):>10}  {rate(m, data[m])}")
    if not field and not origin:
        print("field: none in this file (use PageSpeed Insights or CrUX for real-user p75)")
    print("lab:")
    for m in ("LCP", "CLS", "TBT", "INP", "FCP", "SI", "TTFB"):
        if m in lab:
            print(f"  {m:<5} {fmt(m, lab[m]):>10}  {rate(m, lab[m])}")
    el = lcp_element(lhr)
    print(f"lcp element: {el or '-'}")
    rows = failing(lhr, top)
    if rows:
        print("failing audits and insights (highest estimated savings first):")
        for aid, title, dv, sav in rows:
            extra = " | ".join(x for x in (dv, sav) if x)
            print(f"  - {title} [{aid}]" + (f"  ({extra})" if extra else ""))
    print()
    return {"lab": lab, "field": field}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", help="one report, or two (before after) for a comparison")
    p.add_argument("--top", type=int, default=10, help="number of failing audits to list (default 10)")
    args = p.parse_args(argv)
    if len(args.files) > 2:
        p.error("give one or two files")
    results = []
    for f in args.files:
        try:
            results.append(report(f, args.top))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"error: {f}: {exc}", file=sys.stderr)
            return 2
    if len(results) == 2:
        before, after = results
        print("before -> after (lab):")
        for m in ("LCP", "CLS", "TBT", "INP", "FCP", "TTFB"):
            b, a = before["lab"].get(m), after["lab"].get(m)
            if b is None or a is None:
                continue
            delta = a - b
            sign = "+" if delta > 0 else ""
            dtxt = f"{sign}{delta:.3f}" if m == "CLS" else f"{sign}{delta:,.0f} ms"
            print(f"  {m:<5} {fmt(m, b):>10} -> {fmt(m, a):>10}  ({dtxt})")
        print("Lab runs vary; compare medians of 3 to 5 runs per side before claiming an improvement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
