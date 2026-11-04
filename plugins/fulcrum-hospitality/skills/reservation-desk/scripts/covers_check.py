#!/usr/bin/env python3
"""Check a service's bookings against seat capacity and kitchen pacing, and
find workable times for a new booking request.

Bookings CSV columns (header required):
  time        HH:MM arrival time (24-hour)
  party_size  number of covers
  name        optional, for the report
  duration    optional, minutes the table is held; otherwise the turn-time rule
  status      optional; rows with cancelled, no-show or waitlist are ignored

Turn-time rule (minutes held by party size), override with --turns:
  1-2: 90   3-4: 105   5-6: 120   7+: 150

Checks per slot (default 15 minutes):
  seated   covers in the room during the slot must not exceed --seats
  arrivals covers arriving in the slot must not exceed --pacing
  window   arrivals must be within --service START-END (END = last seating)

Seat capacity is a cover count, not a table plan: a room that fits 60 covers
may not fit a party of 12 at 19:00. Confirm table combinations with the venue.

Examples:
  python3 covers_check.py bookings.csv --seats 60 --pacing 16 --service 17:30-21:00
  python3 covers_check.py bookings.csv --seats 60 --pacing 16 --service 17:30-21:00 --try 19:00,6
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from dataclasses import dataclass
from typing import List, Tuple

IGNORED = {"cancelled", "canceled", "no-show", "noshow", "waitlist", "declined"}

Rules = List[Tuple[int, int]]


@dataclass
class Booking:
    name: str
    start: int
    party: int
    end: int


def to_min(hhmm: str) -> int:
    """Minutes after midnight for HH:MM; raises ValueError for anything else."""
    parts = hhmm.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"not HH:MM: {hhmm!r}")
    h, m = int(parts[0]), int(parts[1])
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise ValueError(f"not a 24-hour time: {hhmm!r}")
    return h * 60 + m


def to_hhmm(mins: int) -> str:
    return "%02d:%02d" % (mins // 60, mins % 60)


def parse_turns(spec: str) -> Rules:
    # "2:90,4:105,6:120,99:150" -> list of (max_party, minutes)
    rules: Rules = []
    try:
        for part in spec.split(","):
            size, mins = part.split(":")
            rules.append((int(size), int(mins)))
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected max_party:minutes,... e.g. 2:90,4:105, not {spec!r}") from None
    if not rules or any(size < 1 or mins < 1 for size, mins in rules):
        raise argparse.ArgumentTypeError(f"party sizes and minutes must be positive: {spec!r}")
    return sorted(rules)


def parse_service(spec: str) -> Tuple[int, int]:
    try:
        a, b = spec.split("-")
        window = (to_min(a), to_min(b))
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected START-END as HH:MM-HH:MM, e.g. 17:30-21:00, not {spec!r}") from None
    if window[1] < window[0]:
        raise argparse.ArgumentTypeError(f"last seating is before the start of service: {spec!r}")
    return window


def parse_request(spec: str) -> Tuple[int, int]:
    try:
        t, p = spec.split(",")
        start, party = to_min(t), int(p)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected HH:MM,party e.g. 19:00,6, not {spec!r}") from None
    if party < 1:
        raise argparse.ArgumentTypeError(f"party size must be at least 1: {spec!r}")
    return start, party


def positive_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError(f"must be a whole number of 1 or more, not {raw!r}")
    return value


def turn_for(party: int, rules: Rules) -> int:
    for max_party, mins in rules:
        if party <= max_party:
            return mins
    return rules[-1][1]


def load(path: str, rules: Rules) -> List[Booking]:
    try:
        if path == "-":
            text = sys.stdin.read()
        else:
            with open(path, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
    except FileNotFoundError:
        raise SystemExit(f"bookings file not found: {path}") from None
    except (OSError, UnicodeDecodeError) as exc:
        raise SystemExit(f"bookings file {path} could not be read: {exc}") from None
    text = text.lstrip("\ufeff")
    if not text.strip():
        print("bookings file is empty: treating the service as having no bookings", file=sys.stderr)
        return []
    reader = csv.DictReader(io.StringIO(text))
    headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
    missing = [c for c in ("time", "party_size") if c not in headers]
    if missing:
        raise SystemExit(f"bookings file {path} is missing columns: {', '.join(missing)}")
    rows: List[Booking] = []
    for raw in reader:
        r = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if isinstance(k, str)}
        if not any(r.values()):
            continue
        i = reader.line_num
        if r.get("status", "").lower() in IGNORED:
            continue
        try:
            start = to_min(r["time"])
            party = int(r["party_size"])
            if party < 1:
                raise ValueError
        except ValueError:
            print("skipping line %d: needs time HH:MM and a party_size of 1 or more (got %r, %r)"
                  % (i, r["time"], r["party_size"]), file=sys.stderr)
            continue
        dur = turn_for(party, rules)
        if r.get("duration"):
            try:
                dur = int(r["duration"])
                if dur < 1:
                    raise ValueError
            except ValueError:
                dur = turn_for(party, rules)
                print("line %d: duration %r is not a whole number of minutes; using the turn-time rule (%d)"
                      % (i, r["duration"], dur), file=sys.stderr)
        rows.append(Booking(name=r.get("name") or "line %d" % i, start=start, party=party, end=start + dur))
    return rows


def grid(rows: List[Booking], slot: int, first: int, last: int) -> List[Tuple[int, int, int]]:
    slots = list(range(first - first % slot, last + slot, slot))
    out: List[Tuple[int, int, int]] = []
    for s in slots:
        seated = sum(b.party for b in rows if b.start < s + slot and b.end > s)
        arrivals = sum(b.party for b in rows if s <= b.start < s + slot)
        out.append((s, seated, arrivals))
    return out


def fits(rows: List[Booking], start: int, party: int, rules: Rules, args: argparse.Namespace) -> bool:
    trial = rows + [Booking(name="request", start=start, party=party, end=start + turn_for(party, rules))]
    open_, last_seat = args.service
    if not (open_ <= start <= last_seat):
        return False
    for s, seated, arrivals in grid(trial, args.slot, start, start + turn_for(party, rules) - 1):
        if seated > args.seats or (s <= start < s + args.slot and arrivals > args.pacing):
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bookings", help="bookings CSV, or - for stdin")
    ap.add_argument("--seats", type=positive_int, required=True, help="covers the room can seat at once")
    ap.add_argument("--pacing", type=positive_int, required=True, help="max covers arriving per slot (kitchen pacing)")
    ap.add_argument("--service", type=parse_service, required=True,
                    help="START-END, where END is the last seating, e.g. 17:30-21:00")
    ap.add_argument("--slot", type=positive_int, default=15, help="slot length in minutes (default 15)")
    ap.add_argument("--turns", type=parse_turns, default="2:90,4:105,6:120,999:150",
                    help="turn-time rule max_party:minutes,...")
    ap.add_argument("--try", dest="try_", type=parse_request,
                    help="test a request HH:MM,party and suggest alternatives within 60 min")
    args = ap.parse_args()

    rules: Rules = args.turns
    window: Tuple[int, int] = args.service
    service_label = "%s-%s" % (to_hhmm(window[0]), to_hhmm(window[1]))
    rows = load(args.bookings, rules)

    flags: List[str] = []
    for r in rows:
        if not (window[0] <= r.start <= window[1]):
            flags.append("%s (%d) arrives %s, outside service %s" % (r.name, r.party, to_hhmm(r.start), service_label))
    if rows:
        first = min(window[0], min(r.start for r in rows))
        last = max(r.end for r in rows)
    else:
        first, last = window
    print("| Slot | Seated covers | Arrivals | Flag |")
    print("| --- | --- | --- | --- |")
    for s, seated, arrivals in grid(rows, args.slot, first, last - 1):
        slot_flags: List[str] = []
        if seated > args.seats:
            slot_flags.append("over seats by %d" % (seated - args.seats))
        if arrivals > args.pacing:
            slot_flags.append("over pacing by %d" % (arrivals - args.pacing))
        if slot_flags:
            flags.append("%s: %s" % (to_hhmm(s), ", ".join(slot_flags)))
        print("| %s | %d | %d | %s |" % (to_hhmm(s), seated, arrivals, "; ".join(slot_flags)))
    total = sum(r.party for r in rows)
    print("\nBookings: %d, covers: %d, seats: %d, pacing per %d min: %d" % (len(rows), total, args.seats, args.slot, args.pacing))
    print("Flags:" if flags else "Flags: none")
    for f in flags:
        print("- " + f)

    if args.try_:
        start, party = args.try_
        print("\nRequest %s for %d: %s" % (to_hhmm(start), party, "fits" if fits(rows, start, party, rules, args) else "does not fit"))
        options: List[int] = []
        for delta in range(args.slot, 61, args.slot):
            for cand in (start - delta, start + delta):
                if fits(rows, cand, party, rules, args):
                    options.append(cand)
        if options:
            print("Alternatives within 60 min: " + ", ".join(to_hhmm(o) for o in sorted(set(options))))
        else:
            print("No alternative within 60 min; offer the waitlist or another service.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
