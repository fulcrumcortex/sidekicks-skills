#!/usr/bin/env python3
"""Build an aged-receivables view from an invoice CSV and suggest a chasing
stage for each debtor.

Accepts exports from most accounting tools and CRMs (Xero, MYOB, QuickBooks,
Fulcrum CRM invoice lists, spreadsheets). Column names are matched loosely;
override them with the --*-col options. Dates are read day-first (Australian)
unless --month-first is given.

Buckets by days past due on --as-of: Current (not yet due), 1-30, 31-60,
61-90, 90+.

Suggested stage from the oldest overdue invoice:
  0  not due            no action (optional reminder 3 days before due)
  1  1-7 days           friendly nudge
  2  8-14 days          firm reminder
  3  15-30 days         phone call
  4  31-45 days         statement of account and call
  5  46-60 days         final notice, offer a payment plan
  6  61+ days           external options review (after final notice expires)

Rows whose status is paid, void, voided, deleted or draft are skipped. Rows
flagged in a dispute/on-hold column are reported as ON HOLD, not chased.

Examples:
  python3 ageing.py receivables.csv --as-of 2026-11-05
  python3 ageing.py export.csv --terms 14 --format csv > aged.csv
  python3 ageing.py export.csv --eom --terms 30 --detail
"""

import argparse
import calendar
import csv
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

ALIASES = {
    "debtor": ["contact", "contactname", "customer", "customer name", "client", "debtor", "company", "name", "account"],
    "invoice": ["invoice", "invoicenumber", "invoice number", "invoice no", "number", "inv", "reference", "id"],
    "invoice_date": ["invoicedate", "invoice date", "date", "issue date", "issued", "created"],
    "due_date": ["duedate", "due date", "payment due date"],
    "outstanding": ["amountdue", "amount due", "outstanding", "balance", "balance due", "amount outstanding", "open amount"],
    "total": ["total", "amount", "invoice total", "gross", "total amount"],
    "paid": ["amountpaid", "amount paid", "paid"],
    "credited": ["amountcredited", "amount credited", "credited", "credit"],
    "status": ["status", "invoice status", "state"],
    "hold": ["disputed", "dispute", "on hold", "on_hold", "hold"],
    "email": ["email", "emailaddress", "email address", "billing email", "accounts email"],
}
SKIP_STATUS = {"paid", "void", "voided", "deleted", "draft"}
TRUTHY = {"y", "yes", "true", "1", "disputed", "hold", "on hold"}
BUCKETS = ["Current", "1-30", "31-60", "61-90", "90+"]
STAGES = [
    (0, "0 not due"), (7, "1 friendly nudge"), (14, "2 firm reminder"), (30, "3 phone call"),
    (45, "4 statement and call"), (60, "5 final notice / payment plan"), (10**6, "6 external options review"),
]
MONTHS = {m.lower(): i for i, m in enumerate(calendar.month_abbr) if m}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower().replace("_", " ")).strip()


def find(header, key, override):
    if override:
        if override not in header:
            sys.exit(f"Column '{override}' not found. Columns: {', '.join(header)}")
        return override
    table = {norm(h): h for h in header}
    for a in ALIASES[key]:
        if norm(a) in table:
            return table[norm(a)]
    return None


def money(s):
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    neg = t.startswith("(") and t.endswith(")")
    t = re.sub(r"[^0-9.\-]", "", t)
    if t in ("", "-", "."):
        return None
    try:
        v = Decimal(t)
    except InvalidOperation:
        return None
    return -v if neg else v


def parse_date(s, month_first):
    if not s or not str(s).strip():
        return None
    t = str(s).strip().split("T")[0].split(" ")[0] if re.match(r"\d{4}-", str(s).strip()) else str(s).strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})", t)
    if m:
        a, b, y = int(m[1]), int(m[2]), int(m[3])
        y = y + 2000 if y < 100 else y
        d, mo = (b, a) if month_first else (a, b)
        return dt.date(y, mo, d)
    m = re.fullmatch(r"(\d{1,2})[ -]([A-Za-z]{3})[A-Za-z]*[ ,-]*(\d{2,4})", t)
    if m and m[2].lower() in MONTHS:
        y = int(m[3])
        y = y + 2000 if y < 100 else y
        return dt.date(y, MONTHS[m[2].lower()], int(m[1]))
    raise ValueError(f"unrecognised date '{s}'")


def due_from(inv_date, terms, eom):
    if eom:
        last = calendar.monthrange(inv_date.year, inv_date.month)[1]
        return dt.date(inv_date.year, inv_date.month, last) + dt.timedelta(days=terms)
    return inv_date + dt.timedelta(days=terms)


def bucket(days):
    if days <= 0:
        return "Current"
    if days <= 30:
        return "1-30"
    if days <= 60:
        return "31-60"
    if days <= 90:
        return "61-90"
    return "90+"


def stage(days):
    for limit, label in STAGES:
        if days <= limit:
            return label
    return STAGES[-1][1]


def fmt(v):
    return f"{v.quantize(Decimal('0.01'), ROUND_HALF_UP):,.2f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="invoice CSV, or - for stdin")
    ap.add_argument("--as-of", help="ageing date YYYY-MM-DD (default today)")
    ap.add_argument("--terms", type=int, default=30, help="payment terms in days when no due date column (default 30)")
    ap.add_argument("--eom", action="store_true", help="terms run from end of invoice month (e.g. 30 days EOM)")
    ap.add_argument("--month-first", action="store_true", help="read 03/04/2026 as 4 March (US style)")
    ap.add_argument("--format", choices=["md", "csv", "json"], default="md")
    ap.add_argument("--detail", action="store_true", help="also list each open invoice (md format)")
    for k in ALIASES:
        ap.add_argument(f"--{k.replace('_', '-')}-col", dest=f"{k}_col", help=f"column for {k}")
    args = ap.parse_args()

    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today()
    fh = sys.stdin if args.input == "-" else open(args.input, newline="", encoding="utf-8-sig")
    reader = csv.DictReader(fh)
    header = reader.fieldnames or []
    col = {k: find(header, k, getattr(args, f"{k}_col")) for k in ALIASES}
    if not col["debtor"]:
        sys.exit(f"No debtor/customer column found; use --debtor-col. Columns: {', '.join(header)}")
    if not (col["outstanding"] or col["total"]):
        sys.exit("No amount column found; use --outstanding-col or --total-col.")
    if not (col["due_date"] or col["invoice_date"]):
        sys.exit("No due date or invoice date column found; use --due-date-col or --invoice-date-col.")

    invoices, problems = [], []
    for n, row in enumerate(reader, start=2):
        status = (row.get(col["status"]) or "").strip().lower() if col["status"] else ""
        if status in SKIP_STATUS:
            continue
        if col["outstanding"] and money(row.get(col["outstanding"])) is not None:
            amt = money(row.get(col["outstanding"]))
        else:
            amt = money(row.get(col["total"])) if col["total"] else None
            if amt is None:
                problems.append(f"row {n}: no amount")
                continue
            paid = (money(row.get(col["paid"])) or 0) if col["paid"] else 0
            amt -= paid
            amt -= money(row.get(col["credited"])) or 0 if col["credited"] else 0
        if amt == 0:
            continue
        part_paid = bool(col["paid"]) and (money(row.get(col["paid"])) or 0) > 0
        try:
            due = parse_date(row.get(col["due_date"]), args.month_first) if col["due_date"] else None
            if due is None:
                inv_d = parse_date(row.get(col["invoice_date"]), args.month_first) if col["invoice_date"] else None
                if inv_d is None:
                    problems.append(f"row {n}: no due or invoice date")
                    continue
                due = due_from(inv_d, args.terms, args.eom)
        except ValueError as e:
            problems.append(f"row {n}: {e}")
            continue
        hold = col["hold"] and (row.get(col["hold"]) or "").strip().lower() in TRUTHY
        days = (as_of - due).days
        invoices.append({
            "debtor": (row.get(col["debtor"]) or "").strip() or "(no name)",
            "invoice": (row.get(col["invoice"]) or "").strip() if col["invoice"] else "",
            "email": (row.get(col["email"]) or "").strip() if col["email"] else "",
            "due": due.isoformat(), "days_overdue": max(days, 0), "bucket": bucket(days),
            "amount": amt, "hold": bool(hold), "credit": amt < 0, "part_paid": part_paid,
        })

    debtors = defaultdict(lambda: {b: Decimal(0) for b in BUCKETS} | {"total": Decimal(0), "oldest": 0,
                                                                         "flags": set(), "count": 0, "email": ""})
    totals = {b: Decimal(0) for b in BUCKETS}
    hold_total = Decimal(0)
    for inv in invoices:
        d = debtors[inv["debtor"]]
        d["email"] = d["email"] or inv["email"]
        if inv["hold"]:
            d["flags"].add("ON HOLD: disputed invoice")
            hold_total += inv["amount"]
            continue
        if inv["credit"]:
            d["flags"].add("credit on account: apply before chasing")
        if inv["part_paid"]:
            d["flags"].add("part-paid: check for an arrangement")
        d[inv["bucket"]] += inv["amount"]
        d["total"] += inv["amount"]
        d["count"] += 1
        totals[inv["bucket"]] += inv["amount"]
        if inv["amount"] > 0:
            d["oldest"] = max(d["oldest"], inv["days_overdue"])

    rows = []
    for name, d in debtors.items():
        flags = set(d["flags"])
        if not d["email"]:
            flags.add("no contact email in export")
        rows.append({"debtor": name, **{b: d[b] for b in BUCKETS}, "total": d["total"],
                     "oldest_days": d["oldest"], "stage": stage(d["oldest"]) if d["total"] > 0 else "-",
                     "flags": "; ".join(sorted(flags))})
    rows.sort(key=lambda r: (r["90+"], r["61-90"], r["31-60"], r["total"]), reverse=True)
    grand = sum(totals.values(), Decimal(0))

    if args.format == "json":
        out = {"as_of": as_of.isoformat(), "totals": {k: str(v) for k, v in totals.items()},
               "on_hold": str(hold_total), "debtors": [{k: (str(v) if isinstance(v, Decimal) else v)
                                                         for k, v in r.items()} for r in rows],
               "problems": problems}
        if args.detail:
            out["invoices"] = [{k: (str(v) if isinstance(v, Decimal) else v) for k, v in i.items()} for i in invoices]
        json.dump(out, sys.stdout, indent=2)
        print()
        return
    if args.format == "csv":
        w = csv.writer(sys.stdout)
        w.writerow(["debtor"] + BUCKETS + ["total", "oldest_days", "stage", "flags"])
        for r in rows:
            w.writerow([r["debtor"]] + [fmt(r[b]) for b in BUCKETS] + [fmt(r["total"]), r["oldest_days"],
                                                                      r["stage"], r["flags"]])
        for p in problems:
            print(f"WARNING {p}", file=sys.stderr)
        return

    print(f"# Aged receivables as of {as_of.isoformat()}\n")
    print("| Bucket | Amount | Share |\n| --- | ---: | ---: |")
    for b in BUCKETS:
        share = f"{(totals[b] / grand * 100):.0f}%" if grand else "-"
        print(f"| {b} | {fmt(totals[b])} | {share} |")
    print(f"| **Total** | **{fmt(grand)}** | |")
    if hold_total:
        print(f"\nOn hold (disputed, not chased): {fmt(hold_total)}")
    print("\n## By debtor\n")
    print("| Debtor | " + " | ".join(BUCKETS) + " | Total | Oldest days | Suggested stage | Flags |")
    print("| --- | " + " | ".join("---:" for _ in BUCKETS) + " | ---: | ---: | --- | --- |")
    for r in rows:
        print(f"| {r['debtor']} | " + " | ".join(fmt(r[b]) for b in BUCKETS) +
              f" | {fmt(r['total'])} | {r['oldest_days']} | {r['stage']} | {r['flags']} |")
    if args.detail:
        print("\n## Open invoices\n")
        print("| Debtor | Invoice | Due | Days overdue | Amount | Note |\n| --- | --- | --- | ---: | ---: | --- |")
        for i in sorted(invoices, key=lambda x: (x["debtor"], x["due"])):
            note = "ON HOLD" if i["hold"] else ("credit" if i["credit"] else "")
            print(f"| {i['debtor']} | {i['invoice']} | {i['due']} | {i['days_overdue']} | {fmt(i['amount'])} | {note} |")
    if problems:
        print("\n## Rows not processed\n")
        for p in problems:
            print(f"- {p}")
    print("\nStages are a starting point. Adjust for relationship, disputes and payments not yet reconciled.")


if __name__ == "__main__":
    main()
