#!/usr/bin/env python3
"""Calculate quote totals with Australian GST from a CSV of line items.

Input CSV columns (header names are case-insensitive):
  description   required
  qty           required (decimals allowed, e.g. 2.5 hours)
  unit_price    required, as it appears in the price list
  gst           optional: Y (taxable, default) or N (GST-free / input-taxed)
  discount_pct  optional: line discount in percent
  option        optional: option name (e.g. Good, Better, Best); totals are
                produced per option, and lines with no option are included
                in every option

--prices says whether unit prices in the file include GST (inc) or exclude
it (ex, the default). GST is 10%: ex-GST price x 10%, or inc-GST price / 11.
GST is calculated per line and rounded to the cent (half up), then summed.

--not-registered: the business is not registered for GST, so no GST is
charged and the quote must not show any.

A line with a blank or unreadable qty, unit_price or discount_pct is left
out and listed under "Lines not included"; the script then exits with
status 1 so the totals are not used until the line is fixed.

Examples:
  python3 quote_totals.py lines.csv
  python3 quote_totals.py lines.csv --prices inc --deposit 20
  python3 quote_totals.py lines.csv --not-registered
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
RATE = Decimal("0.10")


class LineError(ValueError):
    """A line item that cannot be priced."""


def d(value, field, default=None):
    text = (value or "").replace("$", "").replace(",", "").strip()
    if not text:
        if default is None:
            raise LineError(f"{field} is blank")
        return default
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise LineError(f"'{value}' is not a number in column {field}") from None
    if not number.is_finite():
        raise LineError(f"'{value}' is not a number in column {field}")
    return number


def percent(value):
    try:
        number = Decimal(value)
    except InvalidOperation:
        raise argparse.ArgumentTypeError(f"expected a percentage such as 20, got '{value}'") from None
    if not number.is_finite() or not 0 <= number <= 100:
        raise argparse.ArgumentTypeError(f"must be between 0 and 100, got '{value}'")
    return number


def r(x):
    return x.quantize(CENT, ROUND_HALF_UP)


def fmt(x):
    return f"{r(x):,.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="line items CSV, or - for stdin")
    ap.add_argument("--prices", choices=["ex", "inc"], default="ex", help="unit prices exclude (ex) or include (inc) GST")
    ap.add_argument("--not-registered", action="store_true", help="business is not registered for GST")
    ap.add_argument("--deposit", type=percent, help="deposit as a percentage of the total, e.g. 20")
    args = ap.parse_args()

    try:
        fh = sys.stdin if args.input == "-" else open(args.input, newline="", encoding="utf-8-sig")
    except OSError as e:
        sys.exit(f"Cannot open {args.input}: {e.strerror}")
    try:
        reader = csv.DictReader(fh)
        fieldnames = [f.strip().lower() for f in (reader.fieldnames or []) if f is not None]
        reader.fieldnames = fieldnames
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as e:
        sys.exit(f"Cannot read {args.input} as CSV: {e}")
    finally:
        if fh is not sys.stdin:
            fh.close()
    if not fieldnames:
        sys.exit("Input is empty: expected a CSV with description, qty and unit_price columns.")
    for need in ("description", "qty", "unit_price"):
        if need not in fieldnames:
            sys.exit(f"Missing column '{need}'. Found: {', '.join(fieldnames)}")

    lines, options, problems = [], OrderedDict(), []
    for n, row in enumerate(rows, start=2):
        if not any((v or "").strip() for k, v in row.items() if k is not None):
            continue
        desc = (row.get("description") or "").strip()
        try:
            qty = d(row.get("qty"), "qty")
            unit = d(row.get("unit_price"), "unit_price")
            disc = d(row.get("discount_pct"), "discount_pct", Decimal(0))
            if not 0 <= disc <= 100:
                raise LineError(f"discount_pct {disc:g} is outside 0-100")
        except LineError as e:
            problems.append(f"line {n} ({desc or 'no description'}): {e}")
            continue
        taxable = (row.get("gst") or "Y").strip().upper() not in ("N", "NO", "FREE", "GST-FREE", "0")
        gross = qty * unit * (Decimal(100) - disc) / Decimal(100)
        if args.not_registered or not taxable:
            ex, gst = r(gross), Decimal(0)
        elif args.prices == "ex":
            ex = r(gross)
            gst = r(ex * RATE)
        else:
            inc = r(gross)
            gst = r(inc / 11)
            ex = inc - gst
        opt = (row.get("option") or "").strip()
        if opt:
            options.setdefault(opt, None)
        lines.append({"desc": desc or "(no description)", "qty": qty, "unit": unit, "disc": disc,
                      "taxable": taxable and not args.not_registered, "ex": ex, "gst": gst, "opt": opt})

    if not lines and not problems:
        print("No line items: the CSV has a header row but no lines.")
        return
    groups = list(options) or [""]
    for g in groups:
        sel = [l for l in lines if l["opt"] in ("", g)]
        title = f"Option: {g}" if g else "Quote totals"
        print(f"## {title}\n")
        if args.not_registered:
            print("| Item | Qty | Unit price | Disc % | Amount |\n| --- | ---: | ---: | ---: | ---: |")
        else:
            print("| Item | Qty | Unit price | Disc % | Ex GST | GST | Inc GST |\n"
                  "| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for l in sel:
            name = l["desc"] + ("" if l["taxable"] or args.not_registered else " (GST-free)")
            if args.not_registered:
                print(f"| {name} | {l['qty']:g} | {fmt(l['unit'])} | {l['disc']:g} | {fmt(l['ex'])} |")
            else:
                print(f"| {name} | {l['qty']:g} | {fmt(l['unit'])} | {l['disc']:g} | {fmt(l['ex'])} | "
                      f"{fmt(l['gst'])} | {fmt(l['ex'] + l['gst'])} |")
        ex = sum((l["ex"] for l in sel), Decimal(0))
        gst = sum((l["gst"] for l in sel), Decimal(0))
        total = ex + gst
        print()
        if args.not_registered:
            print(f"Total: ${fmt(total)} (no GST: the business is not registered for GST)")
        else:
            print(f"Subtotal (ex GST): ${fmt(ex)}")
            print(f"GST (10%): ${fmt(gst)}")
            print(f"Total (inc GST): ${fmt(total)}")
            print(f"Unit prices in the source were {'inclusive' if args.prices == 'inc' else 'exclusive'} of GST.")
        if args.deposit is not None:
            dep = r(total * args.deposit / Decimal(100))
            print(f"Deposit {args.deposit:g}%: ${fmt(dep)}   Balance: ${fmt(total - dep)}")
        print()
    if problems:
        print("## Lines not included\n")
        for p in problems:
            print(f"- {p}")
        print("\nWARNING: the totals above leave these lines out. Fix them and re-run before quoting.")
        for p in problems:
            print(f"Not included: {p}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
