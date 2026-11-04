#!/usr/bin/env python3
"""Clean an Australian call list before an outbound campaign.

Normalises phone numbers to +61 format, removes duplicates, applies
suppression lists and the user's own Do Not Call Register wash result,
and assigns each row a time-zone group for scheduling.

This script does NOT wash numbers against the Do Not Call Register. It
only applies a wash result that the user obtained themselves (or through
an access seeker) and supplied with --dncr-registered.

Output: the cleaned CSV on stdout (or --out), with added columns
phone_e164, tz_group, status (ok / review / excluded) and reason.
A summary is printed to stderr.

Examples:
  python3 clean_call_list.py list.csv
  python3 clean_call_list.py list.csv --suppress dnc.csv --suppress unsubscribed.txt \
      --dncr-registered wash_registered.csv --wash-date 2026-11-01 --consent-col consent
"""

import argparse
import csv
import datetime as dt
import re
import sys
from collections import Counter

PHONE_ALIASES = ["phone", "mobile", "phone_number", "number", "mobile_phone", "telephone", "phone number"]
STATE_ALIASES = ["state", "region", "state_code"]
TRUTHY = {"y", "yes", "true", "1", "express", "inferred", "consented", "opted in", "opt-in", "opt in"}

STATE_TO_TZ = {
    "NSW": "Australia/Sydney", "ACT": "Australia/Sydney", "VIC": "Australia/Sydney", "TAS": "Australia/Sydney",
    "QLD": "Australia/Brisbane", "SA": "Australia/Adelaide", "NT": "Australia/Darwin", "WA": "Australia/Perth",
}
STATE_NAMES = {
    "NEW SOUTH WALES": "NSW", "AUSTRALIAN CAPITAL TERRITORY": "ACT", "VICTORIA": "VIC", "TASMANIA": "TAS",
    "QUEENSLAND": "QLD", "SOUTH AUSTRALIA": "SA", "NORTHERN TERRITORY": "NT", "WESTERN AUSTRALIA": "WA",
}
WASH_VALID_DAYS = 30


def normalise(raw):
    """Return (e164, kind) where kind is mobile, landline, service, international or invalid."""
    if raw is None:
        return "", "invalid"
    s = raw.strip()
    if not s:
        return "", "invalid"
    plus = s.startswith("+")
    digits = re.sub(r"\D", "", s)
    if plus and not digits.startswith("61"):
        return "+" + digits, "international"
    if digits.startswith("0061"):
        digits = "0" + digits[4:]
    elif digits.startswith("61") and len(digits) == 11:
        digits = "0" + digits[2:]
    elif re.fullmatch(r"[2-478]\d{8}", digits):
        # leading zero lost, typically by a spreadsheet
        digits = "0" + digits
    if digits.startswith("00") or (len(digits) > 10 and not digits.startswith("0")):
        return digits, "international"
    if re.fullmatch(r"04\d{8}", digits):
        return "+61" + digits[1:], "mobile"
    if re.fullmatch(r"0[2378]\d{8}", digits):
        return "+61" + digits[1:], "landline"
    if re.fullmatch(r"1[38]00\d{6}", digits) or re.fullmatch(r"13\d{4}", digits):
        return digits, "service"
    return digits, "invalid"


def state_from(row_state, e164, kind):
    if row_state:
        st = row_state.strip().upper()
        st = STATE_NAMES.get(st, st)
        if st in STATE_TO_TZ:
            return st
    if kind == "landline":
        area = e164[3]
        if area == "2":
            return "NSW/ACT"
        if area == "3":
            return "VIC/TAS"
        if area == "7":
            return "QLD"
    return ""


def tz_group(state):
    if state in ("NSW/ACT", "VIC/TAS"):
        return "Australia/Sydney"
    return STATE_TO_TZ.get(state, "unknown")


def numbers_in_file(path):
    found = set()
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for line in fh:
            for token in re.findall(r"\+?[\d][\d\s().-]{5,}\d", line):
                e164, kind = normalise(token)
                if kind != "invalid":
                    found.add(e164)
    return found


def pick(header, wanted, aliases):
    if wanted:
        if wanted not in header:
            sys.exit(f"Column '{wanted}' not found. Columns: {', '.join(header)}")
        return wanted
    lower = {h.lower().strip(): h for h in header}
    for a in aliases:
        if a in lower:
            return lower[a]
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="call list CSV, or - for stdin")
    ap.add_argument("--phone-col", help="phone column name (auto-detected if omitted)")
    ap.add_argument("--state-col", help="state column name (auto-detected if omitted)")
    ap.add_argument("--consent-col", help="column holding recorded consent (yes/true/express/inferred count as consent)")
    ap.add_argument("--suppress", action="append", default=[], help="file of numbers never to call (repeatable)")
    ap.add_argument("--dncr-registered", help="numbers the user's own Register wash returned as registered")
    ap.add_argument("--wash-date", help="date of the user's wash, YYYY-MM-DD")
    ap.add_argument("--as-of", help="planned call date, YYYY-MM-DD (default today)")
    ap.add_argument("--out", help="write cleaned CSV here instead of stdout")
    args = ap.parse_args()

    as_of = dt.date.fromisoformat(args.as_of) if args.as_of else dt.date.today()
    fh = sys.stdin if args.input == "-" else open(args.input, newline="", encoding="utf-8-sig")
    reader = csv.DictReader(fh)
    header = reader.fieldnames or []
    phone_col = pick(header, args.phone_col, PHONE_ALIASES)
    if not phone_col:
        sys.exit(f"No phone column found. Use --phone-col. Columns: {', '.join(header)}")
    state_col = pick(header, args.state_col, STATE_ALIASES)
    consent_col = pick(header, args.consent_col, []) if args.consent_col else None

    suppressed = set()
    for path in args.suppress:
        suppressed |= numbers_in_file(path)
    registered = numbers_in_file(args.dncr_registered) if args.dncr_registered else None

    out_rows, seen = [], set()
    reasons, groups = Counter(), Counter()
    for row in reader:
        e164, kind = normalise(row.get(phone_col, ""))
        state = state_from(row.get(state_col, "") if state_col else "", e164, kind)
        group = tz_group(state)
        consent = consent_col and str(row.get(consent_col, "")).strip().lower() in TRUTHY
        status, reason = "ok", ""
        if kind == "invalid":
            status, reason = "excluded", "invalid number"
        elif e164 in seen:
            status, reason = "excluded", "duplicate"
        elif e164 in suppressed:
            status, reason = "excluded", "on suppression / do-not-contact list"
        elif registered is not None and e164 in registered and not consent:
            status, reason = "excluded", "on Do Not Call Register, no recorded consent"
        elif kind == "service":
            status, reason = "review", "13/1300/1800 service number"
        elif kind == "international":
            status, reason = "review", "international number"
        elif registered is not None and e164 in registered and consent:
            status, reason = "review", "on Do Not Call Register, relying on recorded consent: verify evidence"
        if e164 and kind != "invalid":
            seen.add(e164)
        if status != "ok":
            reasons[reason] += 1
        else:
            groups[group] += 1
        row.update({"phone_e164": e164, "tz_group": group, "status": status, "reason": reason})
        out_rows.append(row)

    fields = header + [c for c in ("phone_e164", "tz_group", "status", "reason") if c not in header]
    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    writer = csv.DictWriter(out, fieldnames=fields)
    writer.writeheader()
    writer.writerows(out_rows)
    if args.out:
        out.close()

    total = len(out_rows)
    ok = sum(1 for r in out_rows if r["status"] == "ok")
    review = sum(1 for r in out_rows if r["status"] == "review")
    err = sys.stderr
    print("\n== Call list summary ==", file=err)
    print(f"Rows: {total}  ok: {ok}  review: {review}  excluded: {total - ok - review}", file=err)
    for reason, n in reasons.most_common():
        print(f"  {reason}: {n}", file=err)
    print("Ready rows by time-zone group:", file=err)
    for g, n in sorted(groups.items()):
        print(f"  {g}: {n}", file=err)
    if groups.get("unknown"):
        print("  'unknown' rows: schedule inside the window valid in every Australian time zone.", file=err)
    invalid = reasons.get("invalid number", 0)
    if total and invalid / total > 0.10:
        print(f"WARNING: {invalid / total:.0%} invalid numbers (over 10%). Report a list-quality problem before calling.", file=err)
    if registered is None:
        print("BLOCK: no Do Not Call Register wash result supplied. Telemarketing calls must wait until the user "
              "washes the list (this script does not wash).", file=err)
    if args.wash_date:
        age = (as_of - dt.date.fromisoformat(args.wash_date)).days
        if age > WASH_VALID_DAYS:
            print(f"BLOCK: wash is {age} days old on {as_of} (valid for {WASH_VALID_DAYS} days). Re-wash first.", file=err)
        else:
            print(f"Wash age on {as_of}: {age} days (valid until "
                  f"{dt.date.fromisoformat(args.wash_date) + dt.timedelta(days=WASH_VALID_DAYS)}).", file=err)
    elif registered is not None:
        print("FIX: supply --wash-date so wash validity can be checked.", file=err)


if __name__ == "__main__":
    main()
