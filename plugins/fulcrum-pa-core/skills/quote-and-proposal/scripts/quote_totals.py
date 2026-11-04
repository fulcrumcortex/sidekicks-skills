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

Examples:
  python3 quote_totals.py lines.csv
  python3 quote_totals.py lines.csv --prices inc --deposit 20
  python3 quote_totals.py lines.csv --not-registered
"""

import argparse
import csv
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
RATE = Decimal("0.10")


def d(value, field, line):
    try:
        return Decimal(str(value).replace("$", "").replace(",", "").strip() or "0")
    except InvalidOperation:
        sys.exit(f"Line {line}: '{value}' is not a number in column {field}")


def r(x):
    return x.quantize(CENT, ROUND_HALF_UP)


def fmt(x):
    return f"{r(x):,.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="line items CSV, or - for stdin")
    ap.add_argument("--prices", choices=["ex", "inc"], default="ex", help="unit prices exclude (ex) or include (inc) GST")
    ap.add_argument("--not-registered", action="store_true", help="business is not registered for GST")
    ap.add_argument("--deposit", type=Decimal, help="deposit as a percentage of the total, e.g. 20")
    args = ap.parse_args()

    fh = sys.stdin if args.input == "-" else open(args.input, newline="", encoding="utf-8-sig")
    reader = csv.DictReader(fh)
    reader.fieldnames = [f.strip().lower() for f in (reader.fieldnames or [])]
    for need in ("description", "qty", "unit_price"):
        if need not in reader.fieldnames:
            sys.exit(f"Missing column '{need}'. Found: {', '.join(reader.fieldnames)}")

    lines, options = [], OrderedDict()
    for n, row in enumerate(reader, start=2):
        qty = d(row["qty"], "qty", n)
        unit = d(row["unit_price"], "unit_price", n)
        disc = d(row.get("discount_pct") or 0, "discount_pct", n)
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
        lines.append({"desc": row["description"].strip(), "qty": qty, "unit": unit, "disc": disc,
                      "taxable": taxable and not args.not_registered, "ex": ex, "gst": gst, "opt": opt})

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


if __name__ == "__main__":
    main()
