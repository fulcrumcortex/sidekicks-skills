#!/usr/bin/env python3
"""Reconcile delivered NDIS sessions against invoices and claims.

Reads two CSV files (sessions and claims) and, optionally, a budgets CSV and a
public-holidays file. Writes a Markdown or JSON exception report to stdout and,
with --out-claims, a CSV of claim candidates for lines that look claimable but
are not yet billed. Nothing is submitted anywhere: the output is for review.

Standard library only. No network access.

sessions.csv columns (one row per billable line; a session with therapy plus
provider travel has two rows with the same session_id):
  session_id, participant_ref, date (YYYY-MM-DD), start (HH:MM), end (HH:MM),
  status (completed | cancelled | no_show | scheduled), notice_at
  (YYYY-MM-DD HH:MM, when the cancellation was received; blank otherwise),
  support_item, unit (hour | each | km), quantity (blank = derive hours from
  start/end), unit_price, note_ref (blank = no progress note on file), worker

claims.csv columns (invoices to plan managers or participants, and portal
claims, in one file):
  claim_ref, participant_ref, date (YYYY-MM-DD), support_item, quantity,
  unit_price, session_id (blank if unknown), status (draft | submitted | paid |
  rejected | void), claim_type (standard | cancellation | other)

budgets.csv columns (optional, one row per service-agreement line):
  participant_ref, support_item (exact item, or a prefix such as 15_ ending in
  an underscore), agreed_amount, period_start, period_end, funding_type
  (ndia | plan | self)

Thresholds such as the short-notice period are inputs, not facts: confirm them
against the current NDIS Pricing Arrangements and the service agreement.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

LIVE_CLAIM_STATUSES = {"draft", "submitted", "paid"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = []
        for row in csv.DictReader(handle):
            rows.append({(k or "").strip().lower(): (v or "").strip() for k, v in row.items()})
        return rows


def to_float(value, default=None):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_dt(value):
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognised date-time: {value!r}")


def session_hours(row):
    try:
        start = datetime.strptime(row["start"], "%H:%M")
        end = datetime.strptime(row["end"], "%H:%M")
    except (KeyError, ValueError):
        return None
    if end <= start:
        end += timedelta(days=1)
    return round((end - start).total_seconds() / 3600, 4)


def clear_business_days(notice: date, service: date, holidays: set) -> int:
    """Whole business days strictly between the notice day and the service day."""
    count = 0
    day = notice + timedelta(days=1)
    while day < service:
        if day.weekday() < 5 and day not in holidays:
            count += 1
        day += timedelta(days=1)
    return count


def money(value):
    return f"{value:,.2f}"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Reconcile delivered NDIS sessions against invoices and claims (report only; submits nothing).",
        epilog="Example: python3 reconcile.py --sessions sessions.csv --claims claims.csv "
        "--budgets budgets.csv --as-of 2026-11-05 --out-claims claim-candidates.csv",
    )
    parser.add_argument("--sessions", required=True, help="sessions CSV (see module docstring for columns)")
    parser.add_argument("--claims", required=True, help="claims and invoices CSV")
    parser.add_argument("--budgets", help="optional service-agreement budgets CSV")
    parser.add_argument("--holidays", help="optional file with one YYYY-MM-DD public holiday per line")
    parser.add_argument("--short-notice-days", type=int, default=2,
                        help="cancellations with fewer clear business days of notice than this are short notice "
                             "(default 2; verify against the current Pricing Arrangements)")
    parser.add_argument("--near-budget", type=float, default=0.9,
                        help="flag agreement lines at or above this share of the agreed amount (default 0.9)")
    parser.add_argument("--tolerance", type=float, default=0.01, help="allowed difference in quantity or price")
    parser.add_argument("--as-of", help="report date YYYY-MM-DD (default today); scheduled sessions before it are flagged")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    parser.add_argument("--out-claims", help="write claim candidates (unbilled, note on file) to this CSV")
    args = parser.parse_args(argv)

    as_of = parse_date(args.as_of) if args.as_of else date.today()
    holidays = set()
    if args.holidays:
        with open(args.holidays, encoding="utf-8") as handle:
            holidays = {parse_date(line.strip()) for line in handle if line.strip() and not line.startswith("#")}

    sessions = read_csv(args.sessions)
    claims = read_csv(args.claims)
    budgets = read_csv(args.budgets) if args.budgets else []

    findings = []

    def add(kind, severity, row_ref, participant, detail, amount=0.0):
        findings.append({"type": kind, "severity": severity, "ref": row_ref, "participant": participant,
                         "detail": detail, "amount": round(amount, 2)})

    funding = {b["participant_ref"]: b.get("funding_type", "") for b in budgets if b.get("participant_ref")}

    # Index live claims.
    live_claims = [c for c in claims if c.get("status", "").lower() in LIVE_CLAIM_STATUSES]
    for c in claims:
        status = c.get("status", "").lower()
        if status == "rejected":
            add("REJECTED_CLAIM", "high", c.get("claim_ref"), c.get("participant_ref"),
                f"{c.get('support_item')} on {c.get('date')} was rejected; fix and resubmit or write off")
    by_session_item = defaultdict(list)
    by_day_item = defaultdict(list)
    by_session = defaultdict(list)
    for c in live_claims:
        if c.get("session_id"):
            by_session_item[(c["session_id"], c["support_item"])].append(c)
            by_session[c["session_id"]].append(c)
        else:
            by_day_item[(c["participant_ref"], c["date"], c["support_item"])].append(c)

    # Duplicates: same participant, date, item and session (or no session).
    dup_groups = defaultdict(list)
    for c in live_claims:
        dup_groups[(c["participant_ref"], c["date"], c["support_item"], c.get("session_id", ""))].append(c)
    for key, group in dup_groups.items():
        if len(group) > 1:
            refs = ", ".join(c["claim_ref"] for c in group)
            amount = sum(to_float(c["quantity"], 0) * to_float(c["unit_price"], 0) for c in group[1:])
            add("DUPLICATE_CLAIM", "high", refs, key[0],
                f"{len(group)} live claims for {key[2]} on {key[1]}; keep one and void the rest", amount)

    matched_claim_refs = set()
    candidates = []
    session_ids_with_lines = defaultdict(list)
    for s in sessions:
        session_ids_with_lines[s["session_id"]].append(s)

    for s in sessions:
        sid, who, item = s["session_id"], s["participant_ref"], s["support_item"]
        status = s.get("status", "").lower()
        sdate = parse_date(s["date"])
        unit = s.get("unit", "hour").lower() or "hour"
        qty = to_float(s.get("quantity"))
        if qty is None and unit == "hour":
            qty = session_hours(s)
        price = to_float(s.get("unit_price"), 0.0)
        ref = f"{sid}/{item}"

        matches = by_session_item.get((sid, item), [])
        if not matches:
            pool = by_day_item.get((who, s["date"], item), [])
            matches = [c for c in pool if c["claim_ref"] not in matched_claim_refs][:1]
        for c in matches:
            matched_claim_refs.add(c["claim_ref"])

        if status == "scheduled":
            if sdate < as_of:
                add("STATUS_NOT_UPDATED", "medium", ref, who,
                    f"session on {s['date']} is still 'scheduled'; confirm whether it was delivered, cancelled or a no-show")
            continue

        if status in ("cancelled", "no_show"):
            short_notice = status == "no_show"
            notice_text = "no-show"
            if status == "cancelled":
                if not s.get("notice_at"):
                    add("CANCELLATION_NOTICE_MISSING", "medium", ref, who,
                        "cancelled session has no notice time recorded; cannot test the short-notice rule")
                    continue
                notice = parse_dt(s["notice_at"]).date()
                cbd = clear_business_days(notice, sdate, holidays)
                short_notice = cbd < args.short_notice_days
                notice_text = f"{cbd} clear business day(s) notice"
            if short_notice and not matches:
                add("SHORT_NOTICE_CANCELLATION", "medium", ref, who,
                    f"{notice_text}; may be claimable as a short-notice cancellation if the service agreement allows it "
                    "and the current Pricing Arrangements conditions are met", (qty or 0) * price)
                candidates.append((s, qty, price, "cancellation"))
            elif not short_notice and matches:
                add("CANCELLATION_CLAIMED_WITH_NOTICE", "high", ref, who,
                    f"{notice_text} meets the notice period, but claim {matches[0]['claim_ref']} exists; check before submitting")
            continue

        if status != "completed":
            add("UNKNOWN_STATUS", "medium", ref, who, f"status {status!r} not recognised")
            continue

        has_note = bool(s.get("note_ref"))
        if not has_note:
            add("NO_NOTE", "high", ref, who,
                f"completed session on {s['date']} has no progress note; write the note before claiming")

        if not matches:
            others = by_session.get(sid, [])
            kind = "MISSING_LINE_ITEM" if others else "UNBILLED"
            detail = (f"session {sid} is billed, but not for {item}" if others
                      else f"completed session on {s['date']} has no invoice or claim")
            add(kind, "high", ref, who, detail, (qty or 0) * price)
            if has_note:
                candidates.append((s, qty, price, "standard"))
            continue

        c = matches[0]
        c_qty = to_float(c.get("quantity"), 0.0)
        c_price = to_float(c.get("unit_price"), 0.0)
        if qty is not None and abs(c_qty - qty) > args.tolerance:
            add("QUANTITY_MISMATCH", "medium", f"{ref} vs {c['claim_ref']}", who,
                f"delivered {qty:g} {unit}, claimed {c_qty:g}", (qty - c_qty) * price)
        if price and abs(c_price - price) > args.tolerance:
            add("PRICE_MISMATCH", "medium", f"{ref} vs {c['claim_ref']}", who,
                f"agreed {money(price)}, claimed {money(c_price)}; check the agreement and current price limit")

    for c in live_claims:
        if c["claim_ref"] in matched_claim_refs:
            continue
        if c.get("session_id") and c["session_id"] in session_ids_with_lines:
            items = sorted({s["support_item"] for s in session_ids_with_lines[c["session_id"]]})
            add("ITEM_NOT_DELIVERED", "high", c["claim_ref"], c["participant_ref"],
                f"claims {c['support_item']} for session {c['session_id']}, which recorded {', '.join(items)}")
        else:
            add("CLAIM_WITHOUT_SESSION", "high", c["claim_ref"], c["participant_ref"],
                f"{c['support_item']} on {c['date']} has no matching delivered session")

    # Budget and agreement-period checks. Candidates caught here are held, not dropped.
    held = defaultdict(list)
    for b in budgets:
        who, item = b["participant_ref"], b["support_item"]
        agreed = to_float(b.get("agreed_amount"))
        start = parse_date(b["period_start"]) if b.get("period_start") else None
        end = parse_date(b["period_end"]) if b.get("period_end") else None

        def covers(code):
            return code.startswith(item) if item.endswith("_") else code == item

        spent = sum(to_float(c["quantity"], 0) * to_float(c["unit_price"], 0)
                    for c in live_claims if c["participant_ref"] == who and covers(c["support_item"]))
        pending = 0.0
        for s, qty, price, _kind in candidates:
            if s["participant_ref"] == who and covers(s["support_item"]):
                pending += (qty or 0) * price
        for s in sessions:
            if s["participant_ref"] != who or not covers(s["support_item"]):
                continue
            sdate = parse_date(s["date"])
            if (start and sdate < start) or (end and sdate > end):
                held[(s["session_id"], s["support_item"])].append("outside agreement period")
                add("OUTSIDE_AGREEMENT_PERIOD", "high", f"{s['session_id']}/{s['support_item']}", who,
                    f"session on {s['date']} falls outside the agreement period {b.get('period_start')} to {b.get('period_end')}")
        if agreed:
            total = spent + pending
            if total > agreed + args.tolerance:
                for s, _q, _p, _k in candidates:
                    if s["participant_ref"] == who and covers(s["support_item"]):
                        held[(s["session_id"], s["support_item"])].append("agreement line over budget")
                add("OVER_BUDGET", "high", item, who,
                    f"claimed {money(spent)} + unbilled {money(pending)} = {money(total)} exceeds agreed {money(agreed)}",
                    total - agreed)
            elif total >= agreed * args.near_budget:
                add("NEAR_BUDGET", "low", item, who,
                    f"{money(total)} of {money(agreed)} used ({total / agreed:.0%}); discuss before booking more")

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order.get(f["severity"], 3), f["type"], f["participant"] or "", f["ref"] or ""))

    if args.out_claims:
        with open(args.out_claims, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["participant_ref", "session_id", "date_from", "date_to", "support_item", "quantity",
                             "unit_price", "amount", "claim_type", "funding_type", "bill_to", "note_ref", "hold_reason"])
            bill_to = {"ndia": "NDIA portal", "plan": "plan manager", "self": "participant or nominee"}
            for s, qty, price, kind in candidates:
                ft = funding.get(s["participant_ref"], "")
                writer.writerow([s["participant_ref"], s["session_id"], s["date"], s["date"], s["support_item"],
                                 f"{(qty or 0):g}", f"{price:.2f}", f"{(qty or 0) * price:.2f}", kind,
                                 ft or "unknown", bill_to.get(ft, "confirm funding type"), s.get("note_ref", ""),
                                 "; ".join(held.get((s["session_id"], s["support_item"]), []))])

    totals = defaultdict(int)
    for f in findings:
        totals[f["type"]] += 1
    unbilled_value = sum((q or 0) * p for s, q, p, k in candidates)

    if args.format == "json":
        json.dump({"as_of": as_of.isoformat(), "sessions": len(sessions), "claims": len(claims),
                   "summary": dict(totals), "claim_candidates": len(candidates),
                   "claim_candidate_value": round(unbilled_value, 2), "findings": findings}, sys.stdout, indent=2)
        print()
        return 0

    print(f"# Billing reconciliation as at {as_of.isoformat()}\n")
    print(f"- Session lines read: {len(sessions)}; claim lines read: {len(claims)}")
    print(f"- Claim candidates (unbilled, for review): {len(candidates)}, value {money(unbilled_value)}; "
          f"on hold: {sum(1 for s, q, p, k in candidates if (s['session_id'], s['support_item']) in held)}")
    print(f"- Short-notice threshold used: fewer than {args.short_notice_days} clear business days (verify)\n")
    if not findings:
        print("No exceptions found.")
        return 0
    print("## Summary\n")
    print("| Finding | Count |\n| --- | --- |")
    for kind in sorted(totals):
        print(f"| {kind} | {totals[kind]} |")
    print("\n## Exceptions\n")
    print("| Severity | Finding | Participant | Line or claim | Detail | Value |")
    print("| --- | --- | --- | --- | --- | --- |")
    for f in findings:
        value = money(f["amount"]) if f["amount"] else ""
        print(f"| {f['severity']} | {f['type']} | {f['participant']} | {f['ref']} | {f['detail']} | {value} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
