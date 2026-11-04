#!/usr/bin/env python3
"""Weekly pipeline review: flag deal hygiene problems and forecast a period.

Reads a CSV export of deals and prints:
  1. a flag table (stale, stuck, no next step, past close date, pushed,
     probability out of line with stage, missing amount/owner/close date)
  2. a best / likely / worst forecast for the period
  3. an action list per owner, highest value first

CSV columns (header names, case-insensitive; owner, stage, amount and one of
deal_id or name are required):
  deal_id, name, owner, stage, amount,
  probability        percent; blank = stage default
  expected_close     ISO (2026-11-30) or Australian (30/11/2026) date
  last_activity      date of the last logged call, email, meeting or note
  next_step          text; blank = none
  next_step_due      date
  stage_entered      date the deal entered its current stage
  close_date_changes number of times the expected close date moved
  status             open (default), won or lost
  closed_date        date won or lost

Rows with a blank stage or an unreadable date, amount, probability or count
are listed under "Rows skipped" and left out of the review.

Options let you set the review date, the forecast period and a JSON config
that overrides stage probabilities and stale thresholds, for example:
  {"stages": {"Site visit": {"probability": 30, "stale_days": 10}}}

Standard library only. No network calls.

Examples:
  python3 pipeline_review.py deals.csv --as-of 2026-11-06
  python3 pipeline_review.py deals.csv --period 2026-11-01:2026-12-31 --target 120000
  python3 pipeline_review.py deals.csv --format json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from datetime import date, datetime, timedelta

# Defaults follow a common seven-stage pipeline. Match is by keyword in the stage name.
DEFAULT_STAGES = [
    # keyword, probability, stale_days (no activity), stuck_days (time in stage)
    ("lost", 0, None, None),
    ("won", 100, None, None),
    ("contract", 80, 5, 21),
    ("negotiat", 60, 7, 21),
    ("proposal", 40, 10, 30),
    ("qualif", 20, 14, 30),
    ("lead", 10, 21, 45),
]
FALLBACK = (None, 10, 14, 30)
ACTIONS = {
    "PAST_CLOSE": "Confirm a new close date with the customer, or close it as lost",
    "STALE": "Contact the customer and log the outcome",
    "NO_NEXT_STEP": "Agree and record a dated next step",
    "NEXT_STEP_OVERDUE": "Do the overdue next step or reschedule it",
    "PUSHED": "Ask what changed; re-qualify budget, timing and decision maker",
    "STUCK": "Decide: advance, re-plan or close",
    "PROB_MISMATCH": "Move the stage or reset the probability so they agree",
    "MISSING_AMOUNT": "Add an amount (best estimate, marked as such)",
    "MISSING_CLOSE": "Set an expected close date",
    "CLOSE_TOO_FAR": "Check the close date; over 12 months out is usually a placeholder",
    "NO_OWNER": "Assign an owner",
}
SEVERITY = ["PAST_CLOSE", "STALE", "NO_NEXT_STEP", "NEXT_STEP_OVERDUE", "PUSHED", "STUCK",
            "NO_OWNER", "MISSING_CLOSE", "MISSING_AMOUNT", "PROB_MISMATCH", "CLOSE_TOO_FAR"]


def parse_date(value):
    if not value or not str(value).strip():
        return None
    text = str(value).strip()[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date {value!r}; use YYYY-MM-DD or DD/MM/YYYY")


def parse_amount(value):
    if value is None or not str(value).strip():
        return None
    text = str(value).strip()
    cleaned = re.sub(r"[^\d.\-]", "", text)
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"unreadable amount {text!r}") from None


def parse_probability(value):
    text = str(value).strip().rstrip("%").strip()
    try:
        prob = float(text)
    except ValueError:
        raise ValueError(f"unreadable probability {value!r}; use a percent such as 40") from None
    if not 0 <= prob <= 100:
        raise ValueError(f"probability {value!r} is outside 0-100")
    return prob


def parse_count(value):
    if not value:
        return 0
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"unreadable close_date_changes {value!r}") from None
    if number < 0 or number != int(number):
        raise ValueError(f"close_date_changes must be a whole number, got {value!r}")
    return int(number)


def stage_rule(stage, overrides):
    for name, rule in overrides.items():
        if name.lower() == stage.lower():
            base = next((r for r in DEFAULT_STAGES if r[0] in stage.lower()), FALLBACK)
            return (name, rule.get("probability", base[1]), rule.get("stale_days", base[2]),
                    rule.get("stuck_days", base[3]))
    return next((r for r in DEFAULT_STAGES if r[0] in stage.lower()), FALLBACK)


def money(x):
    return f"${x:,.0f}"


def review(rows, as_of, period, overrides):
    deals, problems = [], []
    for n, raw in enumerate(rows, start=2):
        row = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if k}
        if not any(row.values()):
            continue
        label = row.get("deal_id") or row.get("name") or "(unnamed)"
        try:
            d, rule = parse_deal(row, overrides)
        except ValueError as exc:
            problems.append(f"row {n} ({label}): {exc}")
            continue
        flag_deal(d, rule, as_of)
        deals.append(d)
    return summarise(deals, problems, as_of, period)


def parse_deal(row, overrides):
    """Turn one CSV row into a deal dict, or raise ValueError naming the bad field."""
    stage = row.get("stage", "")
    if not stage:
        raise ValueError("no stage")
    rule = stage_rule(stage, overrides)
    status = (row.get("status") or "open").lower()
    if "won" in stage.lower():
        status = "won"
    elif "lost" in stage.lower():
        status = "lost"
    prob = parse_probability(row["probability"]) if row.get("probability") else float(rule[1])
    d = {
        "id": row.get("deal_id") or row.get("id") or row.get("name"),
        "name": row.get("name", "?"),
        "owner": row.get("owner") or "Unassigned",
        "stage": stage,
        "status": status,
        "amount": parse_amount(row.get("amount")),
        "probability": prob,
        "stage_probability": rule[1],
        "expected_close": parse_date(row.get("expected_close")),
        "last_activity": parse_date(row.get("last_activity")),
        "next_step": row.get("next_step", ""),
        "next_step_due": parse_date(row.get("next_step_due")),
        "stage_entered": parse_date(row.get("stage_entered")),
        "pushes": parse_count(row.get("close_date_changes")),
        "closed_date": parse_date(row.get("closed_date")),
        "flags": [],
        "details": [],
    }
    return d, rule


def flag_deal(d, rule, as_of):
    """Add hygiene flags and details to an open deal, in place."""
    if d["status"] == "open":
        flags, details = d["flags"], d["details"]
        stale_days, stuck_days = rule[2], rule[3]
        if d["last_activity"] is None:
            flags.append("STALE")
            details.append("no activity on record")
        elif stale_days is not None:
            idle = (as_of - d["last_activity"]).days
            d["idle_days"] = idle
            if idle > stale_days:
                flags.append("STALE")
                details.append(f"no activity {idle}d (limit {stale_days}d)")
        if stuck_days and d["stage_entered"]:
            in_stage = (as_of - d["stage_entered"]).days
            if in_stage > stuck_days:
                flags.append("STUCK")
                details.append(f"{in_stage}d in stage (limit {stuck_days}d)")
        if not d["next_step"]:
            flags.append("NO_NEXT_STEP")
        elif d["next_step_due"] and d["next_step_due"] < as_of:
            flags.append("NEXT_STEP_OVERDUE")
            details.append(f"next step due {d['next_step_due']:%d %b}")
        if d["expected_close"] is None:
            flags.append("MISSING_CLOSE")
        elif d["expected_close"] < as_of:
            flags.append("PAST_CLOSE")
            details.append(f"close date {d['expected_close']:%d %b} passed")
        elif d["expected_close"] > as_of + timedelta(days=365):
            flags.append("CLOSE_TOO_FAR")
        if d["pushes"] >= 2:
            flags.append("PUSHED")
            details.append(f"close date moved {d['pushes']}x")
        if d["amount"] in (None, 0):
            flags.append("MISSING_AMOUNT")
        if d["owner"] == "Unassigned":
            flags.append("NO_OWNER")
        if abs(d["probability"] - d["stage_probability"]) >= 20:
            flags.append("PROB_MISMATCH")
            details.append(f"{d['probability']:.0f}% vs stage {d['stage_probability']}%")
        d["dead"] = bool(stale_days and d.get("idle_days", 10**6) > 2 * stale_days) or \
            d["last_activity"] is None and d["pushes"] >= 2


def summarise(deals, problems, as_of, period):
    # Forecast
    start, end = period
    in_period = lambda dt: dt is not None and start <= dt <= end
    won = sum(d["amount"] or 0 for d in deals if d["status"] == "won" and in_period(d["closed_date"]))
    open_in = [d for d in deals if d["status"] == "open" and in_period(d["expected_close"])]
    hard = {"PAST_CLOSE", "STALE", "NO_NEXT_STEP"}
    worst = won + sum(d["amount"] or 0 for d in open_in
                      if d["stage_probability"] >= 80 and not hard & set(d["flags"]))
    likely = won
    for d in open_in:
        p = d["probability"] / 100
        if "STALE" in d["flags"]:
            p *= 0.5
        if "PAST_CLOSE" in d["flags"]:
            p *= 0.5
        if "PUSHED" in d["flags"]:
            p *= 0.7
        if "NO_NEXT_STEP" in d["flags"]:
            p *= 0.75
        d["adjusted_probability"] = round(p * 100, 1)
        likely += (d["amount"] or 0) * p
    best = won + sum(d["amount"] or 0 for d in open_in if not d.get("dead"))
    amounts = [d["amount"] for d in open_in if d["amount"]]
    concentration = None
    if amounts and best > 0:
        top = max(open_in, key=lambda d: d["amount"] or 0)
        share = (top["amount"] or 0) / max(best - won, 1)
        if share >= 0.3:
            concentration = f"{top['name']} is {share:.0%} of the open best case"

    # Actions per owner
    actions = {}
    for d in deals:
        if d["status"] != "open" or not d["flags"]:
            continue
        top_flag = min(d["flags"], key=SEVERITY.index)
        weight = (d["amount"] or 0) * d["probability"] / 100
        owner = d["owner"]
        actions.setdefault(owner, []).append({
            "deal": d["name"], "flag": top_flag, "all_flags": d["flags"],
            "action": ACTIONS[top_flag], "detail": "; ".join(d["details"]),
            "weighted_value": weight, "amount": d["amount"],
        })
    for owner in actions:
        actions[owner].sort(key=lambda a: (SEVERITY.index(a["flag"]) > 3, -a["weighted_value"]))

    open_deals = [d for d in deals if d["status"] == "open"]
    return {
        "as_of": as_of.isoformat(),
        "period": [start.isoformat(), end.isoformat()],
        "counts": {
            "open": len(open_deals),
            "flagged": sum(1 for d in open_deals if d["flags"]),
            "by_flag": {f: sum(1 for d in open_deals if f in d["flags"]) for f in SEVERITY
                        if any(f in d["flags"] for d in open_deals)},
        },
        "forecast": {"won_in_period": won, "worst": worst, "likely": round(likely, 2), "best": best,
                     "open_in_period": len(open_in),
                     "median_open_amount": statistics.median(amounts) if amounts else None,
                     "concentration": concentration},
        "deals": deals,
        "actions": actions,
        "problems": problems,
    }


def print_text(result, target):
    f = result["forecast"]
    print(f"Pipeline review as of {result['as_of']} · forecast period {result['period'][0]} to {result['period'][1]}")
    c = result["counts"]
    print(f"\nOpen deals: {c['open']} · flagged: {c['flagged']}")
    for flag, n in c["by_flag"].items():
        print(f"  {flag}: {n}")
    print("\nFORECAST")
    print(f"  Won so far:  {money(f['won_in_period'])}")
    print(f"  Worst:       {money(f['worst'])}  (won + clean deals at 80%+ stages)")
    print(f"  Likely:      {money(f['likely'])}  (won + amount x flag-adjusted probability)")
    print(f"  Best:        {money(f['best'])}  (won + every open deal in period not gone cold)")
    if target:
        print(f"  Target:      {money(target)} · likely is {f['likely'] / target:.0%} of target")
        remaining = target - f["won_in_period"]
        if remaining > 0:
            print(f"  Coverage:    {(f['best'] - f['won_in_period']) / remaining:.1f}x "
                  f"(open best case / target still to win)")
    if f["concentration"]:
        print(f"  Concentration risk: {f['concentration']}")
    print("\nFLAGGED DEALS")
    print("| Deal | Owner | Stage | Amount | Prob | Flags | Detail |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for d in result["deals"]:
        if d["status"] == "open" and d["flags"]:
            amt = money(d["amount"]) if d["amount"] else "-"
            print(f"| {d['name']} | {d['owner']} | {d['stage']} | {amt} | {d['probability']:.0f}% | "
                  f"{', '.join(d['flags'])} | {'; '.join(d['details'])} |")
    start = result["period"][0]
    earlier = [d for d in result["deals"] if d["status"] == "open" and d["expected_close"]
               and d["expected_close"].isoformat() < start]
    if earlier:
        print("\nNEEDS A NEW CLOSE DATE (close date passed before this period; left out of the forecast)")
        for d in earlier:
            print(f"  - {d['name']} ({d['owner']}): was {d['expected_close']:%d %b %Y}")
    if result["problems"]:
        print("\nROWS SKIPPED (fix in the CRM export and re-run)")
        for problem in result["problems"]:
            print(f"  - {problem}")
    print("\nACTIONS BY OWNER")
    for owner, items in sorted(result["actions"].items()):
        print(f"\n{owner}")
        for i, a in enumerate(items[:7], 1):
            extra = f" ({a['detail']})" if a["detail"] else ""
            print(f"  {i}. {a['deal']}: {a['action']}{extra}")
        if len(items) > 7:
            print(f"  +{len(items) - 7} more")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", nargs="?", help="deals CSV (default: stdin)")
    parser.add_argument("--as-of", help="review date, YYYY-MM-DD (default: today)")
    parser.add_argument("--period", help="forecast period START:END (default: the review date's calendar month)")
    parser.add_argument("--target", type=float, help="target for the period, to show coverage")
    parser.add_argument("--config", help="JSON file with stage overrides")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    try:
        as_of = parse_date(args.as_of) if args.as_of else date.today()
        if as_of is None:
            raise ValueError("--as-of is blank; use YYYY-MM-DD")
        period = parse_period(args.period, as_of)
    except ValueError as exc:
        parser.error(str(exc))
    overrides = load_config(args.config) if args.config else {}
    rows = read_rows(args.csv)
    result = review(rows, as_of, period, overrides)
    for problem in result["problems"]:
        print(f"skipped {problem}", file=sys.stderr)
    if args.format == "json":
        json.dump(result, sys.stdout, indent=2, default=str)
        print()
    else:
        print_text(result, args.target)


def parse_period(text, as_of):
    if not text:
        first = as_of.replace(day=1)
        nxt = (first + timedelta(days=32)).replace(day=1)
        return first, nxt - timedelta(days=1)
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError(f"--period must be START:END, got {text!r}")
    start, end = parse_date(parts[0]), parse_date(parts[1])
    if start is None or end is None:
        raise ValueError(f"--period needs both a start and an end date, got {text!r}")
    if end < start:
        raise ValueError(f"--period ends before it starts: {text!r}")
    return start, end


def load_config(path):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            config = json.load(fh)
    except OSError as exc:
        sys.exit(f"error: cannot open config {path}: {exc.strerror}")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        sys.exit(f"error: config {path} is not valid JSON: {exc}")
    stages = config.get("stages", {}) if isinstance(config, dict) else None
    if not isinstance(stages, dict) or not all(isinstance(v, dict) for v in stages.values()):
        sys.exit('error: config must look like {"stages": {"Stage name": {"probability": 30, "stale_days": 10}}}')
    for name, rule in stages.items():
        for key, value in rule.items():
            if key in ("probability", "stale_days", "stuck_days") and not (
                    value is None or (isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0)):
                sys.exit(f"error: config stage {name!r}: {key} must be a non-negative number, got {value!r}")
    return stages


def read_rows(path):
    name = path or "stdin"
    try:
        handle = open(path, newline="", encoding="utf-8-sig") if path else sys.stdin
    except OSError as exc:
        sys.exit(f"error: cannot open {path}: {exc.strerror}")
    try:
        reader = csv.DictReader(handle)
        header = {h.strip().lower() for h in (reader.fieldnames or []) if h}
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as exc:
        sys.exit(f"error: cannot read {name} as CSV: {exc}")
    finally:
        if handle is not sys.stdin:
            handle.close()
    if not header:
        sys.exit(f"error: {name} is empty; expected a deals CSV with a header row")
    missing = [c for c in ("owner", "stage", "amount") if c not in header]
    if not header & {"deal_id", "id", "name"}:
        missing.insert(0, "deal_id or name")
    if missing:
        sys.exit(f"error: missing required column(s): {', '.join(missing)}. Found: {', '.join(sorted(header))}")
    return rows


if __name__ == "__main__":
    main()
