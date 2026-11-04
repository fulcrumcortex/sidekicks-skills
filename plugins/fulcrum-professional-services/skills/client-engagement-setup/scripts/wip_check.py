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

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

BUCKETS = [(0, 30, "0-30"), (31, 60, "31-60"), (61, 90, "61-90"), (91, 10**6, "90+")]
BASIS_ALIASES = {"timeandmaterials": "tm", "tandm": "tm", "fixedfee": "fixed"}


def money(v: Decimal) -> str:
    return f"{v.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):,.2f}"


def dec(raw: str | None) -> Decimal | None:
    raw = (raw or "").strip().replace("$", "").replace(",", "")
    if raw == "":
        return None
    try:
        value = Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"not a number: {raw!r}") from None
    if not value.is_finite():
        raise ValueError(f"not a number: {raw!r}")
    return value


def yes(raw: str | None, default: bool) -> bool:
    raw = (raw or "").strip().lower()
    if raw == "":
        return default
    return raw in ("y", "yes", "true", "1")


def warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


def read(path: str, required: list[str], label: str) -> list[tuple[int, dict[str, str]]]:
    """Return (line number, row) pairs with lower-cased keys; extra unnamed columns are dropped."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
            if not headers:
                raise SystemExit(f"{label} file {path} is empty: expected a header row with {', '.join(required)}")
            missing = [c for c in required if c not in headers]
            if missing:
                raise SystemExit(f"{label} {path} is missing columns: {', '.join(missing)}")
            rows: list[tuple[int, dict[str, str]]] = []
            for r in reader:
                clean = {k.strip().lower(): (v or "").strip() for k, v in r.items() if isinstance(k, str)}
                if any(clean.values()):
                    rows.append((reader.line_num, clean))
            return rows
    except FileNotFoundError:
        raise SystemExit(f"{label} file not found: {path}") from None
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise SystemExit(f"{label} file {path} could not be read: {exc}") from None


def working_days_between(start: dt.date, end: dt.date) -> int:
    """Working days (Mon-Fri) after start up to and including end."""
    days, d = 0, start
    while d < end:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            days += 1
    return days


@dataclass
class Engagement:
    client: str = ""
    basis: str = "unknown"
    budget: Decimal | None = None
    pct: Decimal | None = None
    retainer_hours: Decimal | None = None


@dataclass
class EngagementStats:
    unbilled_h: Decimal = Decimal(0)
    unbilled_v: Decimal = Decimal(0)
    billed_v: Decimal = Decimal(0)
    nonbillable_h: Decimal = Decimal(0)
    buckets: dict[str, Decimal] = field(default_factory=lambda: {label: Decimal(0) for _, _, label in BUCKETS})
    month_h: Decimal = Decimal(0)
    no_rate: int = 0
    oldest: dt.date | None = None


@dataclass
class ReportRow:
    engagement: str
    client: str
    basis: str
    unbilled_hours: Decimal
    unbilled_value: Decimal
    buckets: dict[str, Decimal]
    budget: Decimal | None
    burn: Decimal | None
    nonbillable_hours: Decimal
    flags: list[str]


def bucket_for(age: int) -> str:
    age = max(age, 0)  # future-dated entries count as current
    for lo, hi, label in BUCKETS:
        if lo <= age <= hi:
            return label
    return BUCKETS[-1][2]


def load_engagements(path: str) -> dict[str, Engagement]:
    engagements: dict[str, Engagement] = {}
    for line, r in read(path, ["engagement", "fee_basis"], "Engagements"):
        code = r["engagement"]
        if not code:
            warn(f"Engagements row {line}: engagement code is blank; row skipped")
            continue
        basis = r["fee_basis"].lower().replace("&", "and").replace(" ", "")
        basis = BASIS_ALIASES.get(basis, basis)
        if basis not in ("fixed", "tm", "retainer"):
            warn(f"Engagements row {line} ({code}): fee_basis must be fixed, tm or retainer, not {r['fee_basis']!r}; "
                 "basis treated as unknown")
            basis = "unknown"
        values: dict[str, Decimal | None] = {}
        for col in ("budget_ex_gst", "percent_complete", "retainer_hours"):
            try:
                values[col] = dec(r.get(col))
            except ValueError as exc:
                warn(f"Engagements row {line} ({code}): {col} {exc}; treated as blank")
                values[col] = None
        engagements[code] = Engagement(client=r.get("client", ""), basis=basis, budget=values["budget_ex_gst"],
                                       pct=values["percent_complete"], retainer_hours=values["retainer_hours"])
    return engagements


def engagement_flags(eng: str, e: Engagement, s: EngagementStats, burn: Decimal | None,
                     unknown: set[str], today: dt.date) -> list[str]:
    flags: list[str] = []
    if eng in unknown:
        flags.append("Engagement not in the engagements file: check the code or set it up.")
    if s.no_rate:
        flags.append(f"{s.no_rate} entr{'y' if s.no_rate == 1 else 'ies'} without a rate: value understated; get the firm's rate.")
    if e.basis == "fixed" and burn is not None:
        if burn > 100:
            flags.append(f"Over the fixed fee ({burn:.0f}% used): write-down likely; partner review or scope change request.")
        elif burn >= 80:
            if e.pct is None:
                flags.append(f"{burn:.0f}% of fixed fee used and percent complete unknown: ask the engagement lead.")
            elif e.pct + 10 < burn:
                flags.append(f"Overrun risk: {burn:.0f}% of fee used at {e.pct:.0f}% complete.")
    if e.basis == "tm" and burn is not None:
        if burn >= 100:
            flags.append(f"Estimate or cap reached ({burn:.0f}%): stop non-urgent work and get client approval before continuing.")
        elif burn >= 80:
            flags.append(f"{burn:.0f}% of estimate or cap: notify the client as the engagement letter requires.")
    if e.basis == "retainer" and e.retainer_hours:
        used = s.month_h / e.retainer_hours * 100
        if used > 100:
            flags.append(f"Retainer overage this month ({used:.0f}% of {e.retainer_hours} h): bill or discuss per the letter.")
        elif used >= 90:
            flags.append(f"Retainer at {used:.0f}% of monthly hours.")
    if s.oldest is not None:
        age = (today - s.oldest).days
        if age > 60:
            flags.append(f"Aged WIP: oldest unbilled time is {age} days old; bill, or decide on a write-off.")
        elif e.basis == "tm" and age > 30:
            flags.append(f"Unbilled T&M time older than 30 days ({age} days): billing cycle missed.")
    return flags


def analyse(args: argparse.Namespace) -> tuple[dt.date, list[ReportRow], list[tuple[str, dt.date, int]]]:
    today: dt.date = args.date or dt.date.today()
    engagements = load_engagements(args.engagements)

    stats: defaultdict[str, EngagementStats] = defaultdict(EngagementStats)
    last_entry: dict[str, dt.date] = {}
    unknown: set[str] = set()
    for line, r in read(args.time, ["date", "engagement", "person", "hours"], "Time entries"):
        try:
            d = dt.date.fromisoformat(r["date"])
        except ValueError:
            warn(f"Time entries row {line}: date {r['date']!r} is not YYYY-MM-DD; row skipped")
            continue
        try:
            hours = dec(r["hours"])
            rate = dec(r.get("rate"))
        except ValueError as exc:
            warn(f"Time entries row {line}: {exc}; row skipped")
            continue
        if hours is None:
            warn(f"Time entries row {line}: hours is blank; row skipped")
            continue
        eng = r["engagement"]
        if not eng:
            warn(f"Time entries row {line}: engagement is blank; row skipped")
            continue
        if eng not in engagements:
            unknown.add(eng)
        person = r["person"]
        if person:
            last_entry[person] = max(last_entry.get(person, d), d)
        s = stats[eng]
        if (d.year, d.month) == (today.year, today.month):
            s.month_h += hours
        if not yes(r.get("billable"), True):
            s.nonbillable_h += hours
            continue
        value = hours * rate if rate is not None else Decimal(0)
        if rate is None:
            s.no_rate += 1
        if yes(r.get("billed"), False):
            s.billed_v += value
            continue
        s.unbilled_h += hours
        s.unbilled_v += value
        s.buckets[bucket_for((today - d).days)] += value
        s.oldest = d if s.oldest is None else min(s.oldest, d)

    rows: list[ReportRow] = []
    for eng in sorted(set(engagements) | set(stats)):
        e = engagements.get(eng, Engagement())
        s = stats[eng]
        to_date = s.billed_v + s.unbilled_v
        burn = (to_date / e.budget * 100) if e.budget else None
        rows.append(ReportRow(
            engagement=eng, client=e.client, basis=e.basis,
            unbilled_hours=s.unbilled_h, unbilled_value=s.unbilled_v, buckets=dict(s.buckets),
            budget=e.budget, burn=burn, nonbillable_hours=s.nonbillable_h,
            flags=engagement_flags(eng, e, s, burn, unknown, today),
        ))

    gaps: list[tuple[str, dt.date, int]] = []
    for person, last in sorted(last_entry.items()):
        lag = working_days_between(last, today)
        if lag > args.timesheet_lag:
            gaps.append((person, last, lag))
    return today, rows, gaps


def render(today: dt.date, rows: list[ReportRow], gaps: list[tuple[str, dt.date, int]]) -> str:
    out = [f"# WIP and unbilled time check, {today}\n"]
    if not rows:
        out.append("No time entries or engagements found: nothing to report.")
        return "\n".join(out)
    out.append("| Engagement | Client | Basis | Unbilled h | Unbilled value | 0-30 | 31-60 | 61-90 | 90+ | Budget | Burn % | Non-billable h |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    for r in rows:
        b = r.buckets
        for k, v in b.items():
            totals[k] += v
        totals["value"] += r.unbilled_value
        budget = money(r.budget) if r.budget is not None else ""
        burn = f"{r.burn:.0f}" if r.burn is not None else ""
        out.append(f"| {r.engagement} | {r.client} | {r.basis} | {r.unbilled_hours} | {money(r.unbilled_value)} | "
                   f"{money(b['0-30'])} | {money(b['31-60'])} | {money(b['61-90'])} | {money(b['90+'])} | "
                   f"{budget} | {burn} | {r.nonbillable_hours} |")
    out.append(f"| **Total** | | | | **{money(totals['value'])}** | {money(totals['0-30'])} | {money(totals['31-60'])} | "
               f"{money(totals['61-90'])} | {money(totals['90+'])} | | | |")
    flagged = [r for r in rows if r.flags]
    out.append("\n## Flags\n")
    if not flagged:
        out.append("None.")
    for r in flagged:
        out.append(f"**{r.engagement}**")
        out.extend(f"- {f}" for f in r.flags)
        out.append("")
    out.append("## Timesheets behind\n")
    if not gaps:
        out.append("None.")
    for person, last, lag in gaps:
        out.append(f"- {person}: last entry {last} ({lag} working days ago)")
    return "\n".join(out)


def iso_date(raw: str) -> dt.date:
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {raw!r}") from None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0],
                                epilog="Run with --columns for the expected CSV columns.")
    p.add_argument("--time", help="Time entries CSV")
    p.add_argument("--engagements", help="Engagements CSV")
    p.add_argument("--date", type=iso_date, help="Report date YYYY-MM-DD (default today)")
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
