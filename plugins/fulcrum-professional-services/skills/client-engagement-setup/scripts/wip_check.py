#!/usr/bin/env python3
"""Weekly WIP and unbilled-time check for a professional services firm.

Reads time entries and engagement settings from CSV, then reports per
engagement: unbilled hours and value, ageing buckets, budget burn and flags
(overrun risk, cap reached, retainer overage, aged WIP, missed billing cycle),
plus people whose timesheets look behind.

Values are hours x the charge-out rate on each time entry, as supplied by the
firm. The script never invents a rate: an entry with a blank rate is counted in
hours and flagged.

Standard library only. No network access.

Time entries (--time), header row required:
  date (YYYY-MM-DD), engagement, person, hours
  optional: rate (charge-out rate ex GST), billed (Y/N, default N),
            billable (Y/N, default Y), task

Engagements (--engagements):
  engagement, fee_basis (fixed | tm | retainer)
  optional: client, budget_ex_gst (fixed fee, T&M estimate or cap),
            percent_complete (0-100, fixed fee), retainer_hours (per month)

Example:
  python3 wip_check.py --time time.csv --engagements engagements.csv --date 2026-11-06
"""

import argparse
import csv
import datetime as dt
import sys
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

BUCKETS = [(0, 30, "0-30"), (31, 60, "31-60"), (61, 90, "61-90"), (91, 10**6, "90+")]


def money(v):
    return f"{v.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"


def dec(raw):
    raw = (raw or "").strip().replace("$", "").replace(",", "")
    if raw == "":
        return None
    try:
        return Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"not a number: {raw!r}")


def yes(raw, default):
    raw = (raw or "").strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes", "true", "1")


def read(path, required, label):
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
            missing = [c for c in required if c not in headers]
            if missing:
                raise SystemExit(f"{label} {path} is missing columns: {', '.join(missing)}")
            return [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in reader if any((v or "").strip() for v in r.values())]
    except FileNotFoundError:
        raise SystemExit(f"{label} file not found: {path}")


def working_days_between(start, end):
    """Working days (Mon-Fri) after start up to and including end."""
    days, d = 0, start
    while d < end:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            days += 1
    return days


def analyse(args):
    today = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    engagements = {}
    for r in read(args.engagements, ["engagement", "fee_basis"], "Engagements"):
        basis = r["fee_basis"].lower().replace("&", "").replace(" ", "")
        basis = {"timeandmaterials": "tm", "t&m": "tm", "fixedfee": "fixed"}.get(basis, basis)
        if basis not in ("fixed", "tm", "retainer"):
            raise SystemExit(f"Engagement {r['engagement']}: fee_basis must be fixed, tm or retainer, not {r['fee_basis']!r}")
        engagements[r["engagement"]] = {
            "client": r.get("client", ""),
            "basis": basis,
            "budget": dec(r.get("budget_ex_gst")),
            "pct": dec(r.get("percent_complete")),
            "retainer_hours": dec(r.get("retainer_hours")),
        }

    stats = defaultdict(lambda: {"unbilled_h": Decimal(0), "unbilled_v": Decimal(0), "billed_v": Decimal(0),
                                 "nonbillable_h": Decimal(0), "buckets": defaultdict(Decimal),
                                 "month_h": Decimal(0), "no_rate": 0, "oldest": None})
    last_entry = {}
    unknown = set()
    for i, r in enumerate(read(args.time, ["date", "engagement", "person", "hours"], "Time entries"), start=2):
        try:
            d = dt.date.fromisoformat(r["date"])
            hours = dec(r["hours"])
            rate = dec(r.get("rate"))
        except ValueError as exc:
            raise SystemExit(f"Time entries row {i}: {exc}")
        if hours is None:
            raise SystemExit(f"Time entries row {i}: hours is blank")
        eng = r["engagement"]
        if eng not in engagements:
            unknown.add(eng)
        person = r["person"]
        last_entry[person] = max(last_entry.get(person, d), d)
        s = stats[eng]
        if (d.year, d.month) == (today.year, today.month):
            s["month_h"] += hours
        if not yes(r.get("billable"), True):
            s["nonbillable_h"] += hours
            continue
        value = hours * rate if rate is not None else Decimal(0)
        if rate is None:
            s["no_rate"] += 1
        if yes(r.get("billed"), False):
            s["billed_v"] += value
            continue
        s["unbilled_h"] += hours
        s["unbilled_v"] += value
        age = (today - d).days
        for lo, hi, label in BUCKETS:
            if lo <= age <= hi:
                s["buckets"][label] += value
                break
        s["oldest"] = d if s["oldest"] is None else min(s["oldest"], d)

    rows = []
    for eng in sorted(set(engagements) | set(stats)):
        e = engagements.get(eng, {"client": "", "basis": "unknown", "budget": None, "pct": None, "retainer_hours": None})
        s = stats[eng]
        flags = []
        to_date = s["billed_v"] + s["unbilled_v"]
        burn = (to_date / e["budget"] * 100) if e["budget"] else None
        if eng in unknown:
            flags.append("Engagement not in the engagements file: check the code or set it up.")
        if s["no_rate"]:
            flags.append(f"{s['no_rate']} entr{'y' if s['no_rate'] == 1 else 'ies'} without a rate: value understated; get the firm's rate.")
        if e["basis"] == "fixed" and burn is not None:
            if burn > 100:
                flags.append(f"Over the fixed fee ({burn:.0f}% used): write-down likely; partner review or scope change request.")
            elif burn >= 80:
                pct = e["pct"]
                if pct is None:
                    flags.append(f"{burn:.0f}% of fixed fee used and percent complete unknown: ask the engagement lead.")
                elif pct + 10 < burn:
                    flags.append(f"Overrun risk: {burn:.0f}% of fee used at {pct:.0f}% complete.")
        if e["basis"] == "tm" and burn is not None:
            if burn >= 100:
                flags.append(f"Estimate or cap reached ({burn:.0f}%): stop non-urgent work and get client approval before continuing.")
            elif burn >= 80:
                flags.append(f"{burn:.0f}% of estimate or cap: notify the client as the engagement letter requires.")
        if e["basis"] == "retainer" and e["retainer_hours"]:
            used = s["month_h"] / e["retainer_hours"] * 100
            if used > 100:
                flags.append(f"Retainer overage this month ({used:.0f}% of {e['retainer_hours']} h): bill or discuss per the letter.")
            elif used >= 90:
                flags.append(f"Retainer at {used:.0f}% of monthly hours.")
        if s["oldest"] is not None:
            age = (today - s["oldest"]).days
            if age > 60:
                flags.append(f"Aged WIP: oldest unbilled time is {age} days old; bill, or decide on a write-off.")
            elif e["basis"] == "tm" and age > 30:
                flags.append(f"Unbilled T&M time older than 30 days ({age} days): billing cycle missed.")
        rows.append({
            "engagement": eng, "client": e["client"], "basis": e["basis"],
            "unbilled_hours": s["unbilled_h"], "unbilled_value": s["unbilled_v"],
            "buckets": {label: s["buckets"].get(label, Decimal(0)) for _, _, label in BUCKETS},
            "budget": e["budget"], "burn": burn, "nonbillable_hours": s["nonbillable_h"], "flags": flags,
        })

    gaps = []
    for person, last in sorted(last_entry.items()):
        lag = working_days_between(last, today)
        if lag > args.timesheet_lag:
            gaps.append((person, last, lag))
    return today, rows, gaps


def render(today, rows, gaps):
    out = [f"# WIP and unbilled time check, {today}\n"]
    out.append("| Engagement | Client | Basis | Unbilled h | Unbilled value | 0-30 | 31-60 | 61-90 | 90+ | Budget | Burn % | Non-billable h |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    totals = defaultdict(Decimal)
    for r in rows:
        b = r["buckets"]
        for k, v in b.items():
            totals[k] += v
        totals["value"] += r["unbilled_value"]
        budget = money(r["budget"]) if r["budget"] is not None else ""
        burn = f"{r['burn']:.0f}" if r["burn"] is not None else ""
        out.append(f"| {r['engagement']} | {r['client']} | {r['basis']} | {r['unbilled_hours']} | {money(r['unbilled_value'])} | "
                   f"{money(b['0-30'])} | {money(b['31-60'])} | {money(b['61-90'])} | {money(b['90+'])} | "
                   f"{budget} | {burn} | {r['nonbillable_hours']} |")
    out.append(f"| **Total** | | | | **{money(totals['value'])}** | {money(totals['0-30'])} | {money(totals['31-60'])} | "
               f"{money(totals['61-90'])} | {money(totals['90+'])} | | | |")
    flagged = [r for r in rows if r["flags"]]
    out.append("\n## Flags\n")
    if not flagged:
        out.append("None.")
    for r in flagged:
        out.append(f"**{r['engagement']}**")
        out.extend(f"- {f}" for f in r["flags"])
        out.append("")
    out.append("## Timesheets behind\n")
    if not gaps:
        out.append("None.")
    for person, last, lag in gaps:
        out.append(f"- {person}: last entry {last} ({lag} working days ago)")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Run with --columns for the expected CSV columns.")
    p.add_argument("--time", help="Time entries CSV")
    p.add_argument("--engagements", help="Engagements CSV")
    p.add_argument("--date", help="Report date YYYY-MM-DD (default today)")
    p.add_argument("--timesheet-lag", type=int, default=2,
                   help="Flag people whose last entry is more than this many working days old (default 2)")
    p.add_argument("--columns", action="store_true", help="Print the expected CSV columns and exit")
    args = p.parse_args(argv)
    if args.columns:
        print(__doc__)
        return 0
    if not args.time or not args.engagements:
        p.error("--time and --engagements are required")
    today, rows, gaps = analyse(args)
    print(render(today, rows, gaps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
