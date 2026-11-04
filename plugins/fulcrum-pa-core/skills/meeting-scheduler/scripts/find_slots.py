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

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from typing import Dict, List, Set, Tuple
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DEFAULT_HOURS = {d: [["09:00", "17:00"]] for d in DAYS[:5]}
EDGE_MINUTES = 60  # slots in the first or last hour of someone's day score lower
MAX_SEARCH_DAYS = 92


class RequestError(Exception):
    """A problem with the request JSON, reported without a traceback."""


@dataclass
class Participant:
    name: str
    tz: ZoneInfo
    tz_name: str
    required: bool
    windows: Dict[str, List[Tuple[time, time]]]
    days_off: Set[date] = field(default_factory=set)
    busy: List[Tuple[datetime, datetime]] = field(default_factory=list)
    apply_buffers: bool = True


@dataclass
class Request:
    people: List[Participant]
    search_tz: ZoneInfo
    duration: timedelta
    step: timedelta
    before: int
    after: int
    avoid: List[Tuple[time, time]]
    max_options: int
    earliest: datetime
    first_start: datetime
    stop: datetime


def parse_hm(value, where="time"):
    try:
        hour, minute = str(value).strip().split(":")
        return time(int(hour), int(minute))
    except (ValueError, AttributeError):
        raise RequestError(f"{where}: expected HH:MM, got {value!r}") from None


def parse_date(value, where="date"):
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        raise RequestError(f"{where}: expected YYYY-MM-DD, got {value!r}") from None


def parse_dt(value, tz, where="date-time"):
    text = str(value).strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"  # fromisoformat accepts Z only from Python 3.11
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        raise RequestError(f"{where}: expected an ISO date-time such as 2026-11-10T09:00:00+11:00, "
                           f"got {value!r}") from None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(timezone.utc)


def get_zone(name, where):
    try:
        return ZoneInfo(str(name))
    except (ZoneInfoNotFoundError, ValueError):
        raise RequestError(f"{where} needs a valid IANA timezone such as Australia/Brisbane "
                           f"(got {name!r})") from None


def get_int(raw, key, default=None, minimum=0):
    value = raw.get(key, default)
    if value is None:
        raise RequestError(f"request is missing '{key}'")
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise RequestError(f"'{key}' must be a whole number of minutes, got {value!r}") from None
    if number < minimum:
        raise RequestError(f"'{key}' must be at least {minimum}, got {number}")
    return number


def load_participant(raw, index):
    if not isinstance(raw, dict):
        raise RequestError(f"participant {index} must be a JSON object")
    name = str(raw.get("name") or f"Participant {index}")
    if not raw.get("timezone"):
        raise RequestError(f"participant {name!r} needs a timezone such as Australia/Brisbane")
    tz = get_zone(raw["timezone"], f"participant {name!r}")
    hours = raw.get("working_hours") or DEFAULT_HOURS
    if not isinstance(hours, dict):
        raise RequestError(f"participant {name!r}: working_hours must map mon..sun to [[start, end], ...]")
    windows = {}
    for day in DAYS:
        spans = hours.get(day) or []
        windows[day] = []
        for span in spans:
            if not isinstance(span, (list, tuple)) or len(span) != 2:
                raise RequestError(f"participant {name!r}: working_hours.{day} entries must be [start, end]")
            where = f"participant {name!r} working_hours.{day}"
            windows[day].append((parse_hm(span[0], where), parse_hm(span[1], where)))
    busy = []
    for n, block in enumerate(raw.get("busy") or [], start=1):
        where = f"participant {name!r} busy block {n}"
        if not isinstance(block, dict):
            raise RequestError(f"{where}: must be an object with start and end, or date")
        if "date" in block:
            d = parse_date(block["date"], where)
            start = datetime.combine(d, time(0), tzinfo=tz)
            busy.append((start.astimezone(timezone.utc),
                         (start + timedelta(days=1)).astimezone(timezone.utc)))
        elif block.get("start") and block.get("end"):
            b_start, b_end = parse_dt(block["start"], tz, where), parse_dt(block["end"], tz, where)
            if b_end <= b_start:
                raise RequestError(f"{where}: end is not after start")
            busy.append((b_start, b_end))
        else:
            raise RequestError(f"{where}: needs both start and end, or a date")
    return Participant(
        name=name, tz=tz, tz_name=str(raw["timezone"]), required=bool(raw.get("required", True)),
        windows=windows, days_off={parse_date(d, f"participant {name!r} days_off") for d in raw.get("days_off") or []},
        busy=busy, apply_buffers=bool(raw.get("apply_buffers", True)),
    )


def check(person, start, end, before, after, avoid):
    """Return (ok, reason, penalty) for one participant and one slot."""
    local_start = start.astimezone(person.tz)
    local_end = end.astimezone(person.tz)
    if local_start.date() != local_end.date() and local_end.time() != time(0):
        return False, "outside working hours", 0
    if local_start.date() in person.days_off:
        return False, "day off", 0
    windows = person.windows[DAYS[local_start.weekday()]]
    inside = None
    for w_start, w_end in windows:
        if w_start <= local_start.time() and local_end.time() <= w_end and local_end.time() != time(0):
            inside = (w_start, w_end)
            break
    if inside is None:
        return False, "outside working hours", 0
    pad_start = start - timedelta(minutes=before if person.apply_buffers else 0)
    pad_end = end + timedelta(minutes=after if person.apply_buffers else 0)
    for b_start, b_end in person.busy:
        if b_start < end and start < b_end:
            return False, "busy", 0
        if b_start < pad_end and pad_start < b_end:
            return False, "buffer clash", 0
    penalty = 0
    day = local_start.date()
    w_start_dt = datetime.combine(day, inside[0], tzinfo=person.tz)
    w_end_dt = datetime.combine(day, inside[1], tzinfo=person.tz)
    if (local_start - w_start_dt) < timedelta(minutes=EDGE_MINUTES) or \
       (w_end_dt - local_end) < timedelta(minutes=EDGE_MINUTES):
        penalty += 15
    for a, b in avoid:
        a_dt = datetime.combine(day, a, tzinfo=person.tz)
        b_dt = datetime.combine(day, b, tzinfo=person.tz)
        if a_dt < local_end and local_start < b_dt:
            penalty += 10
    return True, "", penalty


def fmt_local(person, start, end):
    s = start.astimezone(person.tz)
    e = end.astimezone(person.tz)
    return f"{s:%a %d %b %H:%M}-{e:%H:%M} {s.tzname()} ({person.tz_name})"


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


def read_request(path):
    name = path or "stdin"
    try:
        if path:
            with open(path, encoding="utf-8-sig") as fh:
                text = fh.read()
        else:
            text = sys.stdin.read()
    except OSError as e:
        raise RequestError(f"cannot open {path}: {e.strerror}") from None
    except UnicodeDecodeError:
        raise RequestError(f"{name} is not UTF-8 text") from None
    if not text.strip():
        raise RequestError(f"{name} is empty; expected a request JSON object (see assets/freebusy-example.json)")
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as e:
        raise RequestError(f"{name} is not valid JSON: {e.msg} at line {e.lineno}") from None
    if not isinstance(raw, dict):
        raise RequestError(f"{name} must hold a JSON object, not a {type(raw).__name__}")
    return raw


def load_request(raw):
    search = raw.get("search")
    if not isinstance(search, dict) or not search.get("start") or not search.get("end"):
        raise RequestError("request needs 'search' with 'start' and 'end' dates (YYYY-MM-DD)")
    search_tz = get_zone(search.get("timezone", "Australia/Sydney"), "search")
    duration = timedelta(minutes=get_int(raw, "duration_minutes", minimum=1))
    step = timedelta(minutes=get_int(raw, "step_minutes", 15, minimum=1))
    before = get_int(raw, "buffer_before_minutes", 0)
    after = get_int(raw, "buffer_after_minutes", 0)
    notice = timedelta(minutes=get_int(raw, "min_notice_minutes", 120))
    avoid = []
    for span in raw.get("avoid_local") or []:
        if not isinstance(span, (list, tuple)) or len(span) != 2:
            raise RequestError("avoid_local entries must be [start, end] pairs such as [\"12:00\", \"13:00\"]")
        avoid.append((parse_hm(span[0], "avoid_local"), parse_hm(span[1], "avoid_local")))
    max_options = get_int(raw, "max_options", 3, minimum=1)
    participants = raw.get("participants")
    if not isinstance(participants, list) or not participants:
        raise RequestError("request needs a non-empty 'participants' list")
    people = [load_participant(p, i) for i, p in enumerate(participants, start=1)]
    if not any(p.required for p in people):
        raise RequestError("mark at least one participant as required")

    now = parse_dt(raw["now"], search_tz, "now") if raw.get("now") else datetime.now(timezone.utc)
    first, last = parse_date(search["start"], "search.start"), parse_date(search["end"], "search.end")
    if last < first:
        raise RequestError("search.end is before search.start")
    if (last - first).days > MAX_SEARCH_DAYS:
        raise RequestError(f"search range is longer than {MAX_SEARCH_DAYS} days; narrow it")
    cursor = datetime.combine(first, time(0), tzinfo=search_tz).astimezone(timezone.utc)
    stop = datetime.combine(last + timedelta(days=1), time(0), tzinfo=search_tz).astimezone(timezone.utc)
    return Request(people=people, search_tz=search_tz, duration=duration, step=step, before=before,
                   after=after, avoid=avoid, max_options=max_options, earliest=now + notice,
                   first_start=cursor, stop=stop)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("request", nargs="?", help="request JSON file (default: stdin)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--all", action="store_true", help="list every valid slot, not just the best options")
    args = parser.parse_args()

    try:
        req = load_request(read_request(args.request))
    except RequestError as e:
        sys.exit(f"error: {e}")
    people, search_tz, duration, step = req.people, req.search_tz, req.duration, req.step
    before, after, avoid, max_options = req.before, req.after, req.avoid, req.max_options
    earliest, cursor, stop = req.earliest, req.first_start, req.stop

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
            if person.required:
                if not ok:
                    ok_all = False
                    key = f"{person.name}: {reason}"
                    rejections[key] = rejections.get(key, 0) + 1
                    break
                penalty += pen
            else:
                (optional_free if ok else optional_missing).append(person.name)
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
                "local": {p.name: fmt_local(p, s["start"], s["end"]) for p in people},
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
            tag = "" if p.required else " [optional]"
            if not p.required and p.name in s["optional_missing"]:
                tag = " [optional, NOT free]"
            print(f"  {p.name}{tag}: {fmt_local(p, s['start'], s['end'])}")


if __name__ == "__main__":
    main()
