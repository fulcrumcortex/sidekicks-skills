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
        text = fh.read()
    if not text.strip():
        raise ValueError("file is empty")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("not a Lighthouse or PageSpeed Insights JSON file (top level is not an object)")
    if isinstance(data.get("lighthouseResult"), dict):
        lhr = data["lighthouseResult"]
        field, origin = data.get("loadingExperience"), data.get("originLoadingExperience")
    elif "audits" in data:
        lhr, field, origin = data, None, None
    else:
        raise ValueError("not a Lighthouse or PageSpeed Insights JSON file (no 'audits' or 'lighthouseResult' key)")
    if not isinstance(lhr.get("audits"), dict):
        raise ValueError("'audits' is missing or is not an object")
    return {
        "lhr": lhr,
        "field": field if isinstance(field, dict) else None,
        "origin": origin if isinstance(origin, dict) else None,
    }


def _num(value: object) -> float | None:
    """Return value as a float if it is a real number (not bool), else None."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def field_metrics(block: dict | None) -> dict:
    out: dict[str, float] = {}
    metrics = block.get("metrics") if block else None
    if not isinstance(metrics, dict):
        return out
    for name, (key, scale, _) in FIELD_KEYS.items():
        m = metrics.get(key)
        value = _num(m.get("percentile")) if isinstance(m, dict) else None
        if value is not None:
            out[name] = value * scale
    return out


def lab_metrics(lhr: dict) -> dict:
    audits = lhr.get("audits", {})
    out: dict[str, float] = {}
    for name, ids in LAB_AUDITS:
        for aid in ids:
            a = audits.get(aid)
            value = _num(a.get("numericValue")) if isinstance(a, dict) else None
            if value is not None:
                out[name] = value
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
        if isinstance(audits.get(aid), dict):
            s = find_snippet(audits[aid].get("details"))
            if s:
                return s
    return None


def failing(lhr: dict, top: int) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[float, str, str, str, str]] = []
    perf_ids = None
    cat = perf_category(lhr)
    if cat:
        perf_ids = {ref.get("id") for ref in cat.get("auditRefs", []) if isinstance(ref, dict)}
    for aid, a in lhr.get("audits", {}).items():
        if aid in METRIC_AUDIT_IDS or not isinstance(a, dict):
            continue
        if perf_ids is not None and aid not in perf_ids:
            continue
        raw = a.get("metricSavings")
        savings: dict[str, float] = {}
        if isinstance(raw, dict):
            for k, v in raw.items():
                n = _num(v)
                if n:
                    savings[str(k)] = n
        # Informative audits often carry metricSavings of all zeros; only a
        # non-zero saving makes them worth listing.
        if a.get("scoreDisplayMode") in ("notApplicable", "manual", "informative", "error") and not savings:
            continue
        score = _num(a.get("score"))
        if score is not None and score >= 0.9:
            continue
        weight = savings.get("LCP", 0) + savings.get("FCP", 0) * 0.5 + savings.get("TBT", 0) + savings.get("INP", 0) + savings.get("CLS", 0) * 10000
        sav = ", ".join(f"{k} {v:.3f}" if k == "CLS" else f"{k} {v:,.0f} ms" for k, v in savings.items())
        rows.append((weight, aid, str(a.get("title", "")), str(a.get("displayValue", "")), sav))
    rows.sort(key=lambda r: r[0], reverse=True)
    return [(aid, title, dv, sav) for _, aid, title, dv, sav in rows[:top]]


def perf_category(lhr: dict) -> dict | None:
    cats = lhr.get("categories")
    cat = cats.get("performance") if isinstance(cats, dict) else None
    return cat if isinstance(cat, dict) else None


def report(path: str, top: int) -> dict:
    d = load(path)
    lhr = d["lhr"]
    lab = lab_metrics(lhr)
    field = field_metrics(d["field"])
    origin = field_metrics(d["origin"])
    env = lhr.get("configSettings")
    if not isinstance(env, dict):
        env = {}
    print(f"== {path}")
    print(f"url: {lhr.get('finalDisplayedUrl') or lhr.get('finalUrl') or lhr.get('requestedUrl')}")
    print(f"lighthouse {lhr.get('lighthouseVersion', '?')}, form factor: {env.get('formFactor', '?')}, throttling: {env.get('throttlingMethod', '?')}")
    cat = perf_category(lhr)
    perf = _num(cat.get("score")) if cat else None
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
    if args.top < 0:
        p.error("--top must be 0 or more")
    results = []
    for f in args.files:
        try:
            results.append(report(f, args.top))
        except (OSError, ValueError) as exc:  # JSONDecodeError and UnicodeDecodeError are ValueErrors
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
