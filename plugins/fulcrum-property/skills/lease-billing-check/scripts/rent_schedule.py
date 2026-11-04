#!/usr/bin/env python3
"""Build the rent a lease says should be charged, period by period, and
optionally compare it with what was actually billed.

Input 1 (required): a JSON file of lease terms extracted from the signed lease.
Input 2 (optional): a CSV of billed amounts, one row per billing period.

Lease terms JSON (all money GST-exclusive):
{
  "commencement": "2024-07-01",          # first day of the term
  "end": "2029-06-30",                   # last day to schedule (term or today)
  "base_rent": 120000,                   # starting rent
  "base_rent_basis": "annual",           # annual | monthly | weekly
  "frequency": "monthly",                # monthly | fortnightly | weekly
  "gst_rate": 10,                        # 0 for residential (input-taxed)
  "reviews": [
    {"date": "2025-07-01", "type": "fixed", "percent": 4},
    {"date": "2026-07-01", "type": "cpi", "cpi_old": 136.4, "cpi_new": 140.1,
     "floor_percent": null, "cap_percent": null, "ratchet": true},
    {"date": "2027-07-01", "type": "market", "new_rent": 138000, "ratchet": true}
  ],
  "incentives": [
    {"from": "2024-07-01", "to": "2024-09-30", "payable_percent": 0},
    {"from": "2024-10-01", "to": "2025-06-30", "payable_percent": 50}
  ]
}

Review amounts ("new_rent") use the same basis as base_rent.
CPI values are index numbers the user supplies; this script makes no
network calls and does not look up CPI.

Billed CSV columns: period_start, rent_billed [, gst_billed]
(rent_billed is GST-exclusive; dates as YYYY-MM-DD).

Method: monthly periods run from the commencement day-of-month. When a review
or incentive boundary falls inside a period, that period is pro-rated by days
and marked "prorated". Leases differ on proration and rounding; check the
lease and treat small differences on prorated periods with care.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date, timedelta
from typing import Any, Dict, List, Optional, Tuple

ANNUAL_FACTOR = {"annual": 1, "monthly": 12, "weekly": 52}
PERIODS_PER_YEAR = {"monthly": 12, "fortnightly": 26, "weekly": 52}

Step = Tuple[date, float, str]
Billed = Tuple[float, Optional[float]]  # (rent_billed, gst_billed or None)
Incentive = Tuple[date, date, float]


class InputError(Exception):
    """A problem with the user's terms or billed file, reported without a traceback."""


def parse_date(value: Any, where: str) -> date:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{where}: date is missing; expected YYYY-MM-DD")
    try:
        return date.fromisoformat(value.strip())
    except ValueError:
        raise InputError(f"{where}: {value!r} is not a YYYY-MM-DD date") from None


def number(value: Any, where: str) -> float:
    if isinstance(value, bool) or value is None or (isinstance(value, str) and not value.strip()):
        raise InputError(f"{where}: a number is required")
    try:
        result = float(str(value).replace(",", "").replace("$", "")) if isinstance(value, str) else float(value)
    except (TypeError, ValueError):
        raise InputError(f"{where}: {value!r} is not a number") from None
    if not math.isfinite(result):
        raise InputError(f"{where}: {value!r} is not a number")
    return result


def require(obj: Dict[str, Any], key: str, where: str) -> Any:
    if key not in obj or obj[key] is None:
        raise InputError(f"{where}: '{key}' is missing")
    return obj[key]


def as_list(value: Any, where: str) -> List[Dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, dict) for v in value):
        raise InputError(f"{where} must be a list of objects")
    return value


def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    # clamp day to month length
    for day in (d.day, 30, 29, 28):
        try:
            return date(y, m, day)
        except ValueError:
            continue
    raise ValueError("bad date")


def build_periods(start: date, end: date, frequency: str) -> List[Tuple[date, date]]:
    periods: List[Tuple[date, date]] = []
    i = 0
    cur = start
    while cur <= end:
        if frequency == "monthly":
            nxt = add_months(start, i + 1)
        else:
            nxt = cur + timedelta(days=7 if frequency == "weekly" else 14)
        periods.append((cur, min(nxt - timedelta(days=1), end)))
        cur = nxt
        i += 1
    return periods


def apply_reviews(base_annual: float, basis: str, reviews: List[Dict[str, Any]]) -> List[Step]:
    """Return a sorted list of (effective_date, annual_rent, note)."""
    factor = ANNUAL_FACTOR[basis]
    dated = [(parse_date(r.get("date"), f"reviews[{i}].date"), i, r) for i, r in enumerate(reviews)]
    steps: List[Step] = []
    rent = base_annual
    for eff, i, r in sorted(dated, key=lambda x: (x[0], x[1])):
        where = f"reviews[{i}] ({eff})"
        kind = str(require(r, "type", where)).lower()
        old = rent
        if kind == "fixed":
            pct = number(require(r, "percent", where), f"{where}.percent")
            new = old * (1 + pct / 100)
            note = "fixed %s%%" % r["percent"]
        elif kind == "cpi":
            cpi_old = number(require(r, "cpi_old", where), f"{where}.cpi_old")
            cpi_new = number(require(r, "cpi_new", where), f"{where}.cpi_new")
            if cpi_old <= 0 or cpi_new <= 0:
                raise InputError(f"{where}: CPI index numbers must be greater than zero")
            change = cpi_new / cpi_old - 1
            if r.get("floor_percent") is not None:
                change = max(change, number(r["floor_percent"], f"{where}.floor_percent") / 100)
            if r.get("cap_percent") is not None:
                change = min(change, number(r["cap_percent"], f"{where}.cap_percent") / 100)
            new = old * (1 + change)
            note = "CPI %+.3f%%" % (change * 100)
        elif kind == "market":
            new = number(require(r, "new_rent", where), f"{where}.new_rent") * factor
            note = "market"
        else:
            raise InputError(f"{where}: unknown review type {kind!r}; use fixed, cpi or market")
        if r.get("ratchet") and new < old:
            new = old
            note += ", ratchet held"
        rent = round(new, 2)
        steps.append((eff, rent, note))
    return steps


def parse_incentives(incentives: List[Dict[str, Any]]) -> List[Incentive]:
    out: List[Incentive] = []
    for i, inc in enumerate(incentives):
        where = f"incentives[{i}]"
        start = parse_date(inc.get("from"), f"{where}.from")
        end = parse_date(inc.get("to"), f"{where}.to")
        if end < start:
            raise InputError(f"{where}: 'to' ({end}) is before 'from' ({start})")
        pct = number(require(inc, "payable_percent", where), f"{where}.payable_percent")
        out.append((start, end, pct / 100))
    return out


def annual_rent_on(day: date, base_annual: float, steps: List[Step]) -> float:
    rent = base_annual
    for eff, amount, _ in steps:
        if day >= eff:
            rent = amount
    return rent


def payable_fraction_on(day: date, incentives: List[Incentive]) -> float:
    for start, end, frac in incentives:
        if start <= day <= end:
            return frac
    return 1.0


def schedule(terms: Any) -> Tuple[List[Dict[str, Any]], List[Step]]:
    if not isinstance(terms, dict):
        raise InputError("terms file must contain a JSON object")
    basis = str(terms.get("base_rent_basis") or "annual").lower()
    freq = str(terms.get("frequency") or "monthly").lower()
    if basis not in ANNUAL_FACTOR:
        raise InputError(f"base_rent_basis {basis!r} not recognised; use annual, monthly or weekly")
    if freq not in PERIODS_PER_YEAR:
        raise InputError(f"frequency {freq!r} not recognised; use monthly, fortnightly or weekly")
    base_annual = number(require(terms, "base_rent", "terms"), "base_rent") * ANNUAL_FACTOR[basis]
    steps = apply_reviews(base_annual, basis, as_list(terms.get("reviews"), "reviews"))
    incentives = parse_incentives(as_list(terms.get("incentives"), "incentives"))
    gst_rate = number(terms.get("gst_rate") or 0, "gst_rate") / 100
    start = parse_date(terms.get("commencement"), "commencement")
    end = parse_date(terms.get("end"), "end")
    if end < start:
        raise InputError(f"end ({end}) is before commencement ({start})")
    rows: List[Dict[str, Any]] = []
    for p_start, p_end in build_periods(start, end, freq):
        days = (p_end - p_start).days + 1
        if freq == "monthly":
            nominal_days = (add_months(p_start, 1) - p_start).days
        else:
            nominal_days = 7 if freq == "weekly" else 14
        segments: Dict[Tuple[float, float], int] = {}
        d = p_start
        while d <= p_end:
            key = (annual_rent_on(d, base_annual, steps), payable_fraction_on(d, incentives))
            segments[key] = segments.get(key, 0) + 1
            d += timedelta(days=1)
        amount = 0.0
        for (annual, frac), n in segments.items():
            amount += annual / PERIODS_PER_YEAR[freq] * frac * n / nominal_days
        prorated = len(segments) > 1 or days != nominal_days
        rent = round(amount, 2)
        rows.append({
            "period_start": p_start.isoformat(),
            "period_end": p_end.isoformat(),
            "annual_rent": round(annual_rent_on(p_start, base_annual, steps), 2),
            "payable_percent": round(payable_fraction_on(p_start, incentives) * 100, 2),
            "expected_rent": rent,
            "expected_gst": round(rent * gst_rate, 2),
            "note": "prorated" if prorated else "",
        })
    return rows, steps


def load_billed(path: str) -> Dict[str, Billed]:
    billed: Dict[str, Billed] = {}
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
            if not headers:
                raise InputError(f"billed file {path} is empty: expected a header row with period_start, rent_billed")
            missing = [c for c in ("period_start", "rent_billed") if c not in headers]
            if missing:
                raise InputError(f"billed file {path} is missing columns: {', '.join(missing)}")
            for raw in reader:
                row = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if isinstance(k, str)}
                if not any(row.values()):
                    continue
                where = f"billed row {reader.line_num}"
                try:
                    key = parse_date(row["period_start"], f"{where} period_start").isoformat()
                    rent = number(row["rent_billed"], f"{where} rent_billed")
                    gst = number(row["gst_billed"], f"{where} gst_billed") if row.get("gst_billed") else None
                except InputError as exc:
                    print(f"warning: {exc}; row skipped", file=sys.stderr)
                    continue
                if key in billed:
                    print(f"warning: {where}: period {key} billed more than once; amounts added together", file=sys.stderr)
                    prev_rent, prev_gst = billed[key]
                    billed[key] = (round(prev_rent + rent, 2),
                                   None if prev_gst is None and gst is None else round((prev_gst or 0) + (gst or 0), 2))
                    continue
                billed[key] = (rent, gst)
    except FileNotFoundError:
        raise InputError(f"billed file not found: {path}") from None
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise InputError(f"billed file {path} could not be read: {exc}") from None
    return billed


def load_terms(path: str) -> Any:
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise InputError(f"terms file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise InputError(f"terms file {path} is not valid JSON: {exc}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"terms file {path} could not be read: {exc}") from None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("terms", help="lease terms JSON file, or - for stdin")
    ap.add_argument("--billed", help="CSV of billed amounts: period_start, rent_billed[, gst_billed]")
    ap.add_argument("--tolerance", type=float, default=1.00, help="dollar difference to ignore (default 1.00)")
    ap.add_argument("--format", choices=["markdown", "csv"], default="markdown")
    ap.add_argument("--only-mismatches", action="store_true", help="print only rows that differ or are missing")
    args = ap.parse_args()
    try:
        rows, steps = schedule(load_terms(args.terms))
        billed = load_billed(args.billed) if args.billed else None
    except InputError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    cols = ["period_start", "period_end", "annual_rent", "payable_percent", "expected_rent", "expected_gst", "note"]
    if billed is not None:
        cols += ["rent_billed", "rent_diff", "gst_billed", "gst_diff", "status"]
        seen: set[str] = set()
        for r in rows:
            b = billed.get(r["period_start"])
            seen.add(r["period_start"])
            if b is None:
                r.update(rent_billed="", rent_diff="", gst_billed="", gst_diff="", status="NOT BILLED")
                continue
            rent_billed, gst_billed = b
            rd = round(rent_billed - r["expected_rent"], 2)
            gd: float | None = None if gst_billed is None else round(gst_billed - r["expected_gst"], 2)
            bad = abs(rd) > args.tolerance or (gd is not None and abs(gd) > args.tolerance)
            status = "MISMATCH" if bad else "ok"
            if bad and r["note"] == "prorated":
                status = "MISMATCH (prorated period, check method)"
            r.update(rent_billed=rent_billed, rent_diff=rd,
                     gst_billed="" if gst_billed is None else gst_billed,
                     gst_diff="" if gd is None else gd, status=status)
        for k, (rent_billed, _) in sorted(billed.items()):
            if k not in seen:
                extra: Dict[str, Any] = {c: "" for c in cols}
                extra.update(period_start=k, rent_billed=rent_billed, status="BILLED, NO MATCHING PERIOD")
                rows.append(extra)
        if args.only_mismatches:
            rows = [r for r in rows if r.get("status") != "ok"]

    out = sys.stdout
    info = sys.stderr if args.format == "csv" else out  # keep CSV output clean
    print("Review steps:", file=info)
    if not steps:
        print("- none", file=info)
    for eff, amount, note in steps:
        print("- %s: annual rent %.2f (%s)" % (eff.isoformat(), amount, note), file=info)
    print("", file=info)
    if args.format == "csv":
        w = csv.DictWriter(out, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    else:
        print("| " + " | ".join(cols) + " |", file=out)
        print("|" + " --- |" * len(cols), file=out)
        for r in rows:
            print("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |", file=out)
    if billed is not None:
        total = round(sum(float(r["rent_diff"]) for r in rows if r.get("rent_diff") not in ("", None)), 2)
        print("\nNet rent difference (billed minus expected, matched periods): %.2f" % total, file=info)
    return 0


if __name__ == "__main__":
    sys.exit(main())
