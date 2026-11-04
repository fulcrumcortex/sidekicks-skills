#!/usr/bin/env python3
"""Place each policy in the renewal pipeline and suggest the next touch.

Stages by days to expiry: upcoming (more than 60), D-60 (60 to 31),
D-30 (30 to 15), D-14 (14 to 8), D-7 (7 to 1) and expired (0 or less).
Policies with a recorded instruction (renew, lapse, change) or a final
status leave the cadence.

The script only schedules. It never sends anything and never decides what
cover a client should have.

Standard library only. No network access.

Policies CSV (--policies), header row required:
  policy, client, expiry (YYYY-MM-DD)
  optional: class, status (open | instructed | renewed | lapsed | cancelled; default open),
            last_contact (YYYY-MM-DD), docs_outstanding (Y/N),
            sms_opt_out (Y/N), do_not_call (Y/N), email_opt_out (Y/N)

Example:
  python3 renewal_stage.py --policies renewals.csv --date 2026-11-05
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from typing import Any

STAGES = [
    ("upcoming", 61, 10**6),
    ("D-60", 31, 60),
    ("D-30", 15, 30),
    ("D-14", 8, 14),
    ("D-7", 1, 7),
    ("expired", -10**6, 0),
]

ACTIONS = {
    "upcoming": "No contact yet. Check the policy, claims and notes are on file.",
    "D-60": "Pre-renewal email: needs-change questions and document request. Log it.",
    "D-30": "Chase outstanding documents. Call to discuss changes. Present terms once received.",
    "D-14": "Terms must be with the client. SMS reminder, then call if no response.",
    "D-7": "Urgent: call and SMS. Escalate to the account manager. Confirm instructions in writing.",
    "expired": "No instructions recorded. Escalate to the account manager today; confirm cover status with the insurer before telling the client anything.",
}

MIN_GAP = {"D-60": 5, "D-30": 4, "D-14": 3, "D-7": 2, "expired": 0, "upcoming": 0}
FINAL = {"instructed", "renewed", "lapsed", "cancelled"}


def yes(v: str | None) -> bool:
    return (v or "").strip().lower() in ("y", "yes", "true", "1")


def stage_for(days: int) -> str:
    for name, lo, hi in STAGES:
        if lo <= days <= hi:
            return name
    return "upcoming"


def channels(row: dict[str, str]) -> list[str]:
    out: list[str] = []
    if not yes(row.get("email_opt_out")):
        out.append("email")
    if not yes(row.get("sms_opt_out")):
        out.append("SMS")
    if not yes(row.get("do_not_call")):
        out.append("call")
    return out


def iso_date(raw: str) -> dt.date:
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {raw!r}") from None


def read_policies(path: str) -> list[tuple[int, dict[str, str]]]:
    """Return (line number, row) pairs with lower-cased keys; cells beyond the header are ignored."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
            if not headers:
                raise SystemExit(f"Policies file {path} is empty: expected a header row with policy, client, expiry")
            missing = [c for c in ("policy", "client", "expiry") if c not in headers]
            if missing:
                raise SystemExit(f"Policies file is missing columns: {', '.join(missing)}")
            rows: list[tuple[int, dict[str, str]]] = []
            for r in reader:
                clean = {k.strip().lower(): (v or "").strip() for k, v in r.items() if isinstance(k, str)}
                if any(clean.values()):
                    rows.append((reader.line_num, clean))
            return rows
    except FileNotFoundError:
        raise SystemExit(f"Policies file not found: {path}") from None
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise SystemExit(f"Policies file {path} could not be read: {exc}") from None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0],
                                epilog="Run with --columns for the expected CSV columns.")
    p.add_argument("--policies", help="Policies CSV")
    p.add_argument("--date", type=iso_date, help="Today's date YYYY-MM-DD (default today)")
    p.add_argument("--columns", action="store_true", help="Print the expected CSV columns and exit")
    args = p.parse_args(argv)
    if args.columns:
        print(__doc__)
        return 0
    if not args.policies:
        p.error("--policies is required")
    today: dt.date = args.date or dt.date.today()
    rows = read_policies(args.policies)

    due: list[dict[str, Any]] = []
    waiting: list[dict[str, Any]] = []
    closed: list[dict[str, Any]] = []
    problems: list[str] = []
    for i, r in rows:
        if not r["policy"]:
            problems.append(f"Row {i}: policy number is blank; row skipped")
            continue
        try:
            expiry = dt.date.fromisoformat(r["expiry"])
        except ValueError:
            problems.append(f"Row {i} ({r['policy']}): expiry '{r['expiry']}' is not YYYY-MM-DD; row skipped")
            continue
        status = (r.get("status") or "open").lower()
        days = (expiry - today).days
        stage = stage_for(days)
        entry: dict[str, Any] = {"policy": r["policy"], "client": r["client"], "class": r.get("class", ""),
                 "expiry": expiry, "days": days, "stage": stage}
        if status in FINAL:
            entry["note"] = f"status {status}: no further renewal reminders"
            closed.append(entry)
            continue
        ch = channels(r)
        entry["channels"] = ", ".join(ch) if ch else "NONE: all channels opted out; a person must decide"
        entry["action"] = ACTIONS[stage]
        if ch and len(ch) < 3:
            entry["action"] += " Opt-outs recorded: use only the allowed channels."
        if yes(r.get("docs_outstanding")) and stage in ("D-30", "D-14", "D-7"):
            entry["action"] += " Documents still outstanding."
        last = r.get("last_contact")
        if last and stage != "upcoming":
            try:
                last_d = dt.date.fromisoformat(last)
                next_ok = last_d + dt.timedelta(days=MIN_GAP[stage])
                if next_ok > today:
                    entry["note"] = f"last contact {last_d}; next touch from {next_ok}"
                    waiting.append(entry)
                    continue
            except ValueError:
                problems.append(f"Row {i} ({r['policy']}): last_contact '{last}' is not YYYY-MM-DD")
        (due if stage != "upcoming" else waiting).append(entry)
        if stage == "upcoming":
            entry["note"] = f"enters D-60 on {expiry - dt.timedelta(days=60)}"

    order = {name: n for n, (name, _, _) in enumerate(reversed(STAGES))}
    due.sort(key=lambda e: (order[e["stage"]], e["days"]))

    print(f"# Renewal pipeline, {today}\n")
    print("## Due for a touch today (most urgent first)\n")
    if due:
        print("| Stage | Days to expiry | Policy | Client | Class | Allowed channels | Next action |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for e in due:
            print(f"| {e['stage']} | {e['days']} | {e['policy']} | {e['client']} | {e['class']} | {e['channels']} | {e['action']} |")
    else:
        print("None.")
    print("\n## Waiting (contacted recently or not yet in the window)\n")
    if waiting:
        print("| Stage | Days to expiry | Policy | Client | Note |")
        print("| --- | --- | --- | --- | --- |")
        for e in sorted(waiting, key=lambda e: e["days"]):
            print(f"| {e['stage']} | {e['days']} | {e['policy']} | {e['client']} | {e.get('note', '')} |")
    else:
        print("None.")
    print("\n## Out of the cadence\n")
    if closed:
        for e in closed:
            print(f"- {e['policy']} ({e['client']}): {e['note']}")
    else:
        print("None.")
    if problems:
        print("\n## Data problems\n")
        for pr in problems:
            print(f"- {pr}")
            print(f"warning: {pr}", file=sys.stderr)
    if not rows:
        print("\nNo policies in the file: nothing to schedule.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
