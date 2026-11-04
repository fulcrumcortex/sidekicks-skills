#!/usr/bin/env python3
"""Find meeting slots that suit every required participant.

Reads a JSON request (file path or stdin) describing participants, their IANA
time zones, working hours and busy blocks, then prints the best 2-3 options
with each participant's local time. Daylight saving is handled by the
standard-library zoneinfo database, so Brisbane (no DST) and Sydney (DST)
are compared correctly on any date.

Standard library only. No network calls.

Example:
    python3 find_slots.py request.json
    python3 find_slots.py --format json < request.json
    python3 find_slots.py --all request.json

Request shape (see assets/freebusy-example.json for a full example):
{
  "duration_minutes": 45,
  "search": {"start": "2026-11-09", "end": "2026-11-13",
             "timezone": "Australia/Sydney"},
  "now": "2026-11-06T10:00:00+11:00",          optional, for minimum notice
  "min_notice_minutes": 120,                    default 120
  "step_minutes": 15,                           default 15
  "buffer_before_minutes": 10,                  default 0
  "buffer_after_minutes": 10,                   default 0
  "avoid_local": [["12:00", "13:00"]],          soft penalty, each person's local time
  "max_options": 3,                             default 3
  "participants": [
    {"name": "Organiser", "timezone": "Australia/Sydney", "required": true,
     "working_hours": {"mon": [["09:00", "17:00"]], "...": []},
     "days_off": ["2026-11-11"],
     "apply_buffers": true,
     "busy": [{"start": "2026-11-10T09:00:00+11:00", "end": "2026-11-10T10:00:00+11:00"},
              {"date": "2026-11-12"}]}
  ]
}
Busy times without an offset are read in that participant's time zone.
Working hours default to Monday-Friday 09:00-17:00 local.
"""

import argparse
import json
import sys
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DEFAULT_HOURS = {d: [["09:00", "17:00"]] for d in DAYS[:5]}
EDGE_MINUTES = 60  # slots in the first or last hour of someone's day score lower


def parse_hm(value):
    hour, minute = value.split(":")
    return time(int(hour), int(minute))


def parse_dt(value, tz):
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(timezone.utc)


def load_participant(raw):
    try:
        tz = ZoneInfo(raw["timezone"])
    except (KeyError, ZoneInfoNotFoundError):
        sys.exit(f"error: participant {raw.get('name', '?')!r} needs a valid IANA "
                 f"timezone such as Australia/Brisbane (got {raw.get('timezone')!r})")
    hours = raw.get("working_hours") or DEFAULT_HOURS
    windows = {}
    for day in DAYS:
        windows[day] = [(parse_hm(a), parse_hm(b)) for a, b in hours.get(day, [])]
    busy = []
    for block in raw.get("busy", []):
        if "date" in block:
            d = date.fromisoformat(block["date"])
            start = datetime.combine(d, time(0), tzinfo=tz)
            busy.append((start.astimezone(timezone.utc),
                         (start + timedelta(days=1)).astimezone(timezone.utc)))
        else:
            busy.append((parse_dt(block["start"], tz), parse_dt(block["end"], tz)))
    return {
        "name": raw.get("name", "Participant"),
        "tz": tz,
        "tz_name": raw["timezone"],
        "required": raw.get("required", True),
        "windows": windows,
        "days_off": {date.fromisoformat(d) for d in raw.get("days_off", [])},
        "busy": busy,
        "apply_buffers": raw.get("apply_buffers", True),
    }


def check(person, start, end, before, after, avoid):
    """Return (ok, reason, penalty) for one participant and one slot."""
    local_start = start.astimezone(person["tz"])
    local_end = end.astimezone(person["tz"])
    if local_start.date() != local_end.date() and local_end.time() != time(0):
        return False, "outside working hours", 0
    if local_start.date() in person["days_off"]:
        return False, "day off", 0
    windows = person["windows"][DAYS[local_start.weekday()]]
    inside = None
    for w_start, w_end in windows:
        if w_start <= local_start.time() and local_end.time() <= w_end and local_end.time() != time(0):
            inside = (w_start, w_end)
            break
    if inside is None:
        return False, "outside working hours", 0
    pad_start = start - timedelta(minutes=before if person["apply_buffers"] else 0)
    pad_end = end + timedelta(minutes=after if person["apply_buffers"] else 0)
    for b_start, b_end in person["busy"]:
        if b_start < end and start < b_end:
            return False, "busy", 0
        if b_start < pad_end and pad_start < b_end:
            return False, "buffer clash", 0
    penalty = 0
    day = local_start.date()
    w_start_dt = datetime.combine(day, inside[0], tzinfo=person["tz"])
    w_end_dt = datetime.combine(day, inside[1], tzinfo=person["tz"])
    if (local_start - w_start_dt) < timedelta(minutes=EDGE_MINUTES) or \
       (w_end_dt - local_end) < timedelta(minutes=EDGE_MINUTES):
        penalty += 15
    for a, b in avoid:
        a_dt = datetime.combine(day, a, tzinfo=person["tz"])
        b_dt = datetime.combine(day, b, tzinfo=person["tz"])
        if a_dt < local_end and local_start < b_dt:
            penalty += 10
    return True, "", penalty


def fmt_local(person, start, end):
    s = start.astimezone(person["tz"])
    e = end.astimezone(person["tz"])
    return f"{s:%a %d %b %H:%M}-{e:%H:%M} {s.tzname()} ({person['tz_name']})"


def pick_diverse(slots, count, search_tz):
    """Prefer options on different days, then 3 hours apart, then 1 hour apart."""
    chosen = []
    for slot in slots:
        day = slot["start"].astimezone(search_tz).date()
        if all(c["start"].astimezone(search_tz).date() != day for c in chosen):
            chosen.append(slot)
        if len(chosen) == count:
            return chosen
    for gap in (timedelta(hours=3), timedelta(hours=1), timedelta(0)):
        for slot in slots:
            if len(chosen) == count:
                return sorted(chosen, key=lambda s: s["start"])
            if slot in chosen:
                continue
            if all(abs(slot["start"] - c["start"]) >= gap for c in chosen):
                chosen.append(slot)
    return sorted(chosen, key=lambda s: s["start"])


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("request", nargs="?", help="request JSON file (default: stdin)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--all", action="store_true", help="list every valid slot, not just the best options")
    args = parser.parse_args()

    raw = json.load(open(args.request) if args.request else sys.stdin)
    search = raw["search"]
    search_tz = ZoneInfo(search.get("timezone", "Australia/Sydney"))
    duration = timedelta(minutes=int(raw["duration_minutes"]))
    step = timedelta(minutes=int(raw.get("step_minutes", 15)))
    before = int(raw.get("buffer_before_minutes", 0))
    after = int(raw.get("buffer_after_minutes", 0))
    notice = timedelta(minutes=int(raw.get("min_notice_minutes", 120)))
    avoid = [(parse_hm(a), parse_hm(b)) for a, b in raw.get("avoid_local", [])]
    max_options = int(raw.get("max_options", 3))
    people = [load_participant(p) for p in raw["participants"]]
    if not any(p["required"] for p in people):
        sys.exit("error: mark at least one participant as required")

    now = parse_dt(raw["now"], search_tz) if raw.get("now") else datetime.now(timezone.utc)
    earliest = now + notice
    cursor = datetime.combine(date.fromisoformat(search["start"]), time(0), tzinfo=search_tz).astimezone(timezone.utc)
    stop = datetime.combine(date.fromisoformat(search["end"]) + timedelta(days=1), time(0),
                            tzinfo=search_tz).astimezone(timezone.utc)

    slots, rejections, examined = [], {}, 0
    while cursor + duration <= stop:
        start, end = cursor, cursor + duration
        cursor += step
        if start < earliest:
            continue
        examined += 1
        ok_all, penalty, optional_free, optional_missing = True, 0, [], []
        for person in people:
            ok, reason, pen = check(person, start, end, before, after, avoid)
            if person["required"]:
                if not ok:
                    ok_all = False
                    key = f"{person['name']}: {reason}"
                    rejections[key] = rejections.get(key, 0) + 1
                    break
                penalty += pen
            else:
                (optional_free if ok else optional_missing).append(person["name"])
        if not ok_all:
            continue
        score = 100 - penalty - 20 * len(optional_missing)
        slots.append({"start": start, "end": end, "score": score,
                      "optional_free": optional_free, "optional_missing": optional_missing})

    ranked = sorted(slots, key=lambda s: (-s["score"], s["start"]))
    options = ranked if args.all else pick_diverse(ranked, max_options, search_tz)

    if args.format == "json":
        out = {
            "valid_slots": len(slots),
            "examined": examined,
            "options": [{
                "start_utc": s["start"].isoformat(),
                "end_utc": s["end"].isoformat(),
                "score": s["score"],
                "local": {p["name"]: fmt_local(p, s["start"], s["end"]) for p in people},
                "optional_unavailable": s["optional_missing"],
            } for s in options],
            "rejections": dict(sorted(rejections.items(), key=lambda kv: -kv[1])),
        }
        json.dump(out, sys.stdout, indent=2)
        print()
        return

    print(f"Examined {examined} start times; {len(slots)} suit every required participant.")
    if not options:
        print("No common slot. Constraints that removed the most candidates:")
        for key, count in sorted(rejections.items(), key=lambda kv: -kv[1])[:5]:
            print(f"  - {key}: {count}")
        print("Try a wider date range, a shorter meeting, smaller buffers or a booking link.")
        sys.exit(2)
    for i, s in enumerate(options, 1):
        print(f"\nOption {i} (score {s['score']})")
        for p in people:
            tag = "" if p["required"] else " [optional]"
            if not p["required"] and p["name"] in s["optional_missing"]:
                tag = " [optional, NOT free]"
            print(f"  {p['name']}{tag}: {fmt_local(p, s['start'], s['end'])}")


if __name__ == "__main__":
    main()
