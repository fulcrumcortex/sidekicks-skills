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

import argparse
import csv
import json
import sys
from datetime import date, timedelta

ANNUAL_FACTOR = {"annual": 1, "monthly": 12, "weekly": 52}
PERIODS_PER_YEAR = {"monthly": 12, "fortnightly": 26, "weekly": 52}


def parse_date(s):
    return date.fromisoformat(str(s).strip())


def add_months(d, n):
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


def build_periods(start, end, frequency):
    periods = []
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


def apply_reviews(base_annual, basis, reviews):
    """Return a sorted list of (effective_date, annual_rent, note)."""
    factor = ANNUAL_FACTOR[basis]
    steps = []
    rent = base_annual
    for r in sorted(reviews, key=lambda x: x["date"]):
        kind = r["type"].lower()
        old = rent
        if kind == "fixed":
            new = old * (1 + float(r["percent"]) / 100)
            note = "fixed %s%%" % r["percent"]
        elif kind == "cpi":
            change = float(r["cpi_new"]) / float(r["cpi_old"]) - 1
            if r.get("floor_percent") is not None:
                change = max(change, float(r["floor_percent"]) / 100)
            if r.get("cap_percent") is not None:
                change = min(change, float(r["cap_percent"]) / 100)
            new = old * (1 + change)
            note = "CPI %+.3f%%" % (change * 100)
        elif kind == "market":
            new = float(r["new_rent"]) * factor
            note = "market"
        else:
            raise ValueError("unknown review type: %s" % kind)
        if r.get("ratchet") and new < old:
            new = old
            note += ", ratchet held"
        rent = round(new, 2)
        steps.append((parse_date(r["date"]), rent, note))
    return steps


def annual_rent_on(day, base_annual, steps):
    rent = base_annual
    for eff, amount, _ in steps:
        if day >= eff:
            rent = amount
    return rent


def payable_fraction_on(day, incentives):
    for inc in incentives:
        if parse_date(inc["from"]) <= day <= parse_date(inc["to"]):
            return float(inc["payable_percent"]) / 100
    return 1.0


def schedule(terms):
    basis = terms.get("base_rent_basis", "annual")
    freq = terms.get("frequency", "monthly")
    if basis not in ANNUAL_FACTOR or freq not in PERIODS_PER_YEAR:
        raise ValueError("base_rent_basis or frequency not recognised")
    base_annual = float(terms["base_rent"]) * ANNUAL_FACTOR[basis]
    steps = apply_reviews(base_annual, basis, terms.get("reviews", []))
    incentives = terms.get("incentives", [])
    gst_rate = float(terms.get("gst_rate", 0)) / 100
    start = parse_date(terms["commencement"])
    end = parse_date(terms["end"])
    rows = []
    for p_start, p_end in build_periods(start, end, freq):
        days = (p_end - p_start).days + 1
        if freq == "monthly":
            nominal_days = (add_months(p_start, 1) - p_start).days
        else:
            nominal_days = 7 if freq == "weekly" else 14
        segments = {}
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


def load_billed(path):
    billed = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            key = parse_date(row["period_start"]).isoformat()
            billed[key] = {
                "rent_billed": float(row["rent_billed"]),
                "gst_billed": float(row["gst_billed"]) if row.get("gst_billed") not in (None, "") else None,
            }
    return billed


def main():
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
    terms = json.load(sys.stdin if args.terms == "-" else open(args.terms))
    rows, steps = schedule(terms)
    billed = load_billed(args.billed) if args.billed else None

    cols = ["period_start", "period_end", "annual_rent", "payable_percent", "expected_rent", "expected_gst", "note"]
    if billed is not None:
        cols += ["rent_billed", "rent_diff", "gst_billed", "gst_diff", "status"]
        seen = set()
        for r in rows:
            b = billed.get(r["period_start"])
            seen.add(r["period_start"])
            if b is None:
                r.update(rent_billed="", rent_diff="", gst_billed="", gst_diff="", status="NOT BILLED")
                continue
            rd = round(b["rent_billed"] - r["expected_rent"], 2)
            gd = "" if b["gst_billed"] is None else round(b["gst_billed"] - r["expected_gst"], 2)
            bad = abs(rd) > args.tolerance or (gd != "" and abs(gd) > args.tolerance)
            status = "MISMATCH" if bad else "ok"
            if bad and r["note"] == "prorated":
                status = "MISMATCH (prorated period, check method)"
            r.update(rent_billed=b["rent_billed"], rent_diff=rd,
                     gst_billed="" if b["gst_billed"] is None else b["gst_billed"], gst_diff=gd, status=status)
        for k, b in sorted(billed.items()):
            if k not in seen:
                rows.append({c: "" for c in cols} | {"period_start": k, "rent_billed": b["rent_billed"],
                                                      "status": "BILLED, NO MATCHING PERIOD"})
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


if __name__ == "__main__":
    main()
