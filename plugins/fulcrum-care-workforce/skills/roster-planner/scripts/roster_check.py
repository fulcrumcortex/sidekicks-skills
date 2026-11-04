#!/usr/bin/env python3
"""Check a draft care roster for conflicts and suggest workers for open shifts.

Reads shifts and workers CSV files, an optional clients CSV and a JSON rules
file, then prints a Markdown (or JSON) report: conflicts by severity, ranked
candidates for open shifts, hours per worker and continuity of care per client.
It changes nothing and notifies nobody.

Standard library only. No network access.

shifts.csv:  shift_id, client_ref, start (YYYY-MM-DD HH:MM), end (YYYY-MM-DD HH:MM),
             location, required_skills (a;b), required_compliance (a;b, optional,
             added to the rules file's required_for_all), worker_id (blank = open)
workers.csv: worker_id, name, skills (a;b), max_hours_week, availability
             ("Mon 07:00-15:00;Tue 07:00-15:00"; blank = unknown),
             compliance ("ndis_screening=2029-01-31;first_aid=2027-03-01"),
             home_area (optional)
clients.csv: client_ref, preferred_workers (a;b), excluded_workers (a;b),
             max_workers_week (optional override)
rules.json:  {"required_for_all": [...], "warn_within_days": 30,
              "min_rest_hours": 10, "max_shift_hours": 10,
              "max_consecutive_days": 6, "travel_buffer_minutes": 30,
              "max_workers_per_client_week": 3}

Rule values are settings, not award advice: check the applicable Modern Award,
enterprise agreement and organisational policy before relying on them.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, datetime, time, timedelta

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DEFAULT_RULES = {
    "required_for_all": ["ndis_worker_screening", "first_aid", "cpr"],
    "warn_within_days": 30,
    "min_rest_hours": 10,
    "max_shift_hours": 10,
    "max_consecutive_days": 6,
    "travel_buffer_minutes": 30,
    "max_workers_per_client_week": 3,
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return [{(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
                for row in csv.DictReader(handle)]


def split(value):
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def parse_dt(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M")


def parse_clock(value):
    if value == "24:00":
        return time(23, 59, 59)
    return datetime.strptime(value, "%H:%M").time()


def parse_availability(text):
    """Return {weekday_index: [(start_time, end_time), ...]} or None when unknown."""
    if not text:
        return None
    windows = defaultdict(list)
    for chunk in split(text):
        day, _, span = chunk.partition(" ")
        start, _, end = span.partition("-")
        windows[DAYS.index(day[:3].title())].append((parse_clock(start), parse_clock(end)))
    return windows


def segments(start, end):
    """Split a shift into per-day pieces so overnight shifts are checked on both days."""
    pieces = []
    cursor = start
    while cursor < end:
        day_end = datetime.combine(cursor.date() + timedelta(days=1), time(0, 0))
        piece_end = min(end, day_end)
        pieces.append((cursor, piece_end))
        cursor = piece_end
    return pieces


def is_available(windows, start, end):
    if windows is None:
        return None
    for seg_start, seg_end in segments(start, end):
        last = (seg_end - timedelta(seconds=1)).time()
        if not any(w_start <= seg_start.time() and last <= w_end for w_start, w_end in windows.get(seg_start.weekday(), [])):
            return False
    return True


def hours(shift):
    return (shift["end"] - shift["start"]).total_seconds() / 3600


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check a draft care roster for conflicts and rank candidates for open shifts (report only).",
        epilog="Example: python3 roster_check.py --shifts shifts.csv --workers workers.csv "
        "--clients clients.csv --rules compliance-rules.json",
    )
    parser.add_argument("--shifts", required=True)
    parser.add_argument("--workers", required=True)
    parser.add_argument("--clients", help="optional client preferences CSV")
    parser.add_argument("--rules", help="optional JSON rules file (defaults are placeholders to confirm)")
    parser.add_argument("--top", type=int, default=3, help="candidates to list per open shift (default 3)")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args(argv)

    rules = dict(DEFAULT_RULES)
    if args.rules:
        with open(args.rules, encoding="utf-8") as handle:
            rules.update(json.load(handle))

    workers = {}
    for w in read_csv(args.workers):
        compliance = {}
        for item in split(w.get("compliance")):
            key, _, expiry = item.partition("=")
            compliance[key.strip()] = datetime.strptime(expiry.strip(), "%Y-%m-%d").date() if expiry.strip() else None
        workers[w["worker_id"]] = {
            "id": w["worker_id"], "name": w.get("name") or w["worker_id"], "skills": set(split(w.get("skills"))),
            "max_hours": float(w["max_hours_week"]) if w.get("max_hours_week") else None,
            "availability": parse_availability(w.get("availability")), "compliance": compliance,
        }
    clients = {c["client_ref"]: c for c in read_csv(args.clients)} if args.clients else {}

    shifts = []
    for s in read_csv(args.shifts):
        shift = {"id": s["shift_id"], "client": s["client_ref"], "start": parse_dt(s["start"]),
                 "end": parse_dt(s["end"]), "location": s.get("location", ""),
                 "skills": set(split(s.get("required_skills"))),
                 "compliance": set(rules["required_for_all"]) | set(split(s.get("required_compliance"))),
                 "worker": s.get("worker_id", "")}
        if shift["end"] <= shift["start"]:
            raise SystemExit(f"shift {shift['id']}: end must be after start (write overnight shifts with the next day's date)")
        shifts.append(shift)
    shifts.sort(key=lambda x: x["start"])
    roster_end = max((s["end"].date() for s in shifts), default=date.today())

    findings = []

    def add(severity, kind, shift_id, worker_id, detail):
        findings.append({"severity": severity, "type": kind, "shift": shift_id,
                         "worker": workers.get(worker_id, {}).get("name", worker_id), "detail": detail})

    def worker_issues(w, shift, assigned):
        """Return hard blockers for putting worker w on shift, given their other assignments."""
        blockers, warnings = [], []
        missing_skills = shift["skills"] - w["skills"]
        if missing_skills:
            blockers.append(("SKILL_MISMATCH", f"lacks {', '.join(sorted(missing_skills))}"))
        for item in sorted(shift["compliance"]):
            expiry = w["compliance"].get(item, "missing")
            if expiry == "missing":
                blockers.append(("COMPLIANCE_MISSING", f"no record of {item}"))
            elif expiry is not None and expiry < shift["end"].date():
                blockers.append(("COMPLIANCE_EXPIRED", f"{item} expired {expiry.isoformat()}"))
            elif expiry is not None and expiry <= roster_end + timedelta(days=rules["warn_within_days"]):
                warnings.append(("COMPLIANCE_EXPIRING", f"{item} expires {expiry.isoformat()}"))
        available = is_available(w["availability"], shift["start"], shift["end"])
        if available is False:
            blockers.append(("UNAVAILABLE", "outside stated availability"))
        elif available is None:
            warnings.append(("AVAILABILITY_UNKNOWN", "no availability on file; confirm with the worker"))
        prefs = clients.get(shift["client"], {})
        if w["id"] in split(prefs.get("excluded_workers")):
            blockers.append(("CLIENT_EXCLUDED", f"{shift['client']} has asked not to work with this worker"))
        if hours(shift) > rules["max_shift_hours"]:
            warnings.append(("LONG_SHIFT", f"{hours(shift):.1f} h exceeds {rules['max_shift_hours']} h setting"))
        for other in assigned:
            if other["id"] == shift["id"]:
                continue
            if other["start"] < shift["end"] and shift["start"] < other["end"]:
                blockers.append(("DOUBLE_BOOKED", f"overlaps {other['id']}"))
                continue
            first, second = (other, shift) if other["start"] < shift["start"] else (shift, other)
            gap_h = (second["start"] - first["end"]).total_seconds() / 3600
            if gap_h < rules["min_rest_hours"]:
                same_day = first["start"].date() == first["end"].date() == second["start"].date()
                if same_day and gap_h > 0:
                    if gap_h * 60 < rules["travel_buffer_minutes"] and first["location"] != second["location"]:
                        warnings.append(("TRAVEL_TIGHT", f"{gap_h * 60:.0f} min to get from {first['location']} to {second['location']} ({other['id']})"))
                    elif gap_h >= 1:
                        warnings.append(("BROKEN_SHIFT_CHECK", f"{gap_h:.1f} h gap with {other['id']} on the same day; check broken-shift rules"))
                else:
                    gap_text = "no break" if gap_h == 0 else f"{gap_h:.1f} h"
                    blockers.append(("SHORT_REST", f"{gap_text} between {first['id']} and {second['id']} (setting {rules['min_rest_hours']} h)"))
        return blockers, warnings

    by_worker = defaultdict(list)
    for s in shifts:
        if s["worker"]:
            by_worker[s["worker"]].append(s)

    for s in shifts:
        if not s["worker"]:
            add("high", "OPEN_SHIFT", s["id"], "", f"{s['client']} {s['start']:%a %d %b %H:%M}-{s['end']:%H:%M} at {s['location']}")
            continue
        w = workers.get(s["worker"])
        if not w:
            add("high", "UNKNOWN_WORKER", s["id"], s["worker"], "worker not in workers file")
            continue
        blockers, warnings = worker_issues(w, s, by_worker[s["worker"]])
        seen = set()
        for kind, detail in blockers:
            key = (kind, detail)
            if key not in seen:
                seen.add(key)
                add("high", kind, s["id"], s["worker"], detail)
        for kind, detail in warnings:
            key = (kind, detail)
            if key not in seen:
                seen.add(key)
                add("medium" if kind != "AVAILABILITY_UNKNOWN" else "low", kind, s["id"], s["worker"], detail)

    # Weekly hours and consecutive days per worker.
    hours_by_worker = {}
    for wid, assigned in by_worker.items():
        total = sum(hours(s) for s in assigned)
        hours_by_worker[wid] = total
        w = workers.get(wid)
        if w and w["max_hours"] is not None and total > w["max_hours"]:
            add("medium", "OVER_MAX_HOURS", "-", wid, f"{total:.1f} h rostered, maximum {w['max_hours']:g} h; check overtime rules")
        worked = sorted({s["start"].date() for s in assigned})
        run = best = 1
        for prev, cur in zip(worked, worked[1:]):
            run = run + 1 if (cur - prev).days == 1 else 1
            best = max(best, run)
        if worked and best > rules["max_consecutive_days"]:
            add("medium", "CONSECUTIVE_DAYS", "-", wid, f"{best} days in a row (setting {rules['max_consecutive_days']})")

    # Continuity of care.
    continuity = {}
    for client in sorted({s["client"] for s in shifts}):
        names = sorted({s["worker"] for s in shifts if s["client"] == client and s["worker"]})
        continuity[client] = names
        limit = int(clients.get(client, {}).get("max_workers_week") or rules["max_workers_per_client_week"])
        if len(names) > limit:
            add("medium", "CONTINUITY", "-", "", f"{client} sees {len(names)} different workers this week (limit {limit})")

    # Candidates for open shifts and for shifts with hard conflicts.
    order = {"high": 0, "medium": 1, "low": 2}
    hard_shift_ids = {f["shift"] for f in findings if f["severity"] == "high" and f["shift"] != "-"}
    suggestions = {}
    for s in shifts:
        if s["id"] not in hard_shift_ids:
            continue
        ranked = []
        for wid, w in workers.items():
            if wid == s["worker"]:
                continue
            blockers, warnings = worker_issues(w, s, by_worker[wid])
            if blockers:
                continue
            new_total = hours_by_worker.get(wid, 0) + hours(s)
            if w["max_hours"] is not None and new_total > w["max_hours"]:
                continue
            prefs = clients.get(s["client"], {})
            score = 0
            reasons = []
            if wid in split(prefs.get("preferred_workers")):
                score += 3
                reasons.append("client's preferred worker")
            if wid in continuity.get(s["client"], []):
                score += 2
                reasons.append("already supports this client this week")
            if any(o["location"] == s["location"] and o["start"].date() == s["start"].date() for o in by_worker[wid]):
                score += 1
                reasons.append("already working in this area that day")
            if warnings:
                score -= 1
                reasons.append("check: " + "; ".join(d for _, d in warnings))
            ranked.append((score, -new_total, w["name"], f"{new_total:.1f} h after", reasons))
        ranked.sort(reverse=True)
        suggestions[s["id"]] = [{"worker": r[2], "score": r[0], "hours_after": r[3], "why": r[4]} for r in ranked[: args.top]]

    findings.sort(key=lambda f: (order[f["severity"]], f["type"], f["shift"]))

    if args.format == "json":
        json.dump({"rules": rules, "findings": findings, "candidates": suggestions,
                   "hours": {workers.get(k, {}).get("name", k): round(v, 2) for k, v in hours_by_worker.items()},
                   "continuity": continuity}, sys.stdout, indent=2, default=str)
        print()
        return 0

    print("# Roster check\n")
    print(f"- Shifts: {len(shifts)}; open: {sum(1 for s in shifts if not s['worker'])}; "
          f"high-severity conflicts: {sum(1 for f in findings if f['severity'] == 'high')}")
    print(f"- Settings: min rest {rules['min_rest_hours']} h, max shift {rules['max_shift_hours']} h, "
          f"max {rules['max_consecutive_days']} consecutive days, compliance required for all: "
          f"{', '.join(rules['required_for_all'])}. Confirm these against the applicable award and policy.\n")
    print("## Conflicts\n")
    if findings:
        print("| Severity | Type | Shift | Worker | Detail |\n| --- | --- | --- | --- | --- |")
        for f in findings:
            print(f"| {f['severity']} | {f['type']} | {f['shift']} | {f['worker']} | {f['detail']} |")
    else:
        print("No conflicts found.")
    print("\n## Candidates for open or conflicting shifts\n")
    if not suggestions:
        print("None needed.")
    for shift_id, options in suggestions.items():
        print(f"- **{shift_id}**: " + ("; ".join(
            f"{o['worker']} ({o['hours_after']}{', ' + ', '.join(o['why']) if o['why'] else ''})" for o in options)
            if options else "no eligible worker; escalate to the roster owner"))
    print("\n## Hours per worker\n")
    print("| Worker | Rostered hours | Maximum |\n| --- | --- | --- |")
    for wid, w in sorted(workers.items(), key=lambda kv: kv[1]["name"]):
        max_text = f"{w['max_hours']:g}" if w["max_hours"] is not None else "not set"
        print(f"| {w['name']} | {hours_by_worker.get(wid, 0):.1f} | {max_text} |")
    print("\n## Continuity of care\n")
    print("| Client | Workers this week |\n| --- | --- |")
    for client, names in continuity.items():
        print(f"| {client} | {', '.join(workers.get(n, {}).get('name', n) for n in names) or 'none assigned'} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
