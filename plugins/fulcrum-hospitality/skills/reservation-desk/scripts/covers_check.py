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

import argparse
import csv
import sys

IGNORED = {"cancelled", "canceled", "no-show", "noshow", "waitlist", "declined"}


def to_min(hhmm):
    h, m = hhmm.strip().split(":")
    return int(h) * 60 + int(m)


def to_hhmm(mins):
    return "%02d:%02d" % (mins // 60, mins % 60)


def parse_turns(spec):
    # "2:90,4:105,6:120,99:150" -> list of (max_party, minutes)
    rules = []
    for part in spec.split(","):
        size, mins = part.split(":")
        rules.append((int(size), int(mins)))
    return sorted(rules)


def turn_for(party, rules):
    for max_party, mins in rules:
        if party <= max_party:
            return mins
    return rules[-1][1]


def load(path, rules):
    fh = sys.stdin if path == "-" else open(path, newline="")
    rows = []
    for i, r in enumerate(csv.DictReader(fh), start=2):
        if (r.get("status") or "").strip().lower() in IGNORED:
            continue
        try:
            start = to_min(r["time"])
            party = int(r["party_size"])
        except (KeyError, ValueError):
            print("skipping line %d: needs time HH:MM and party_size" % i, file=sys.stderr)
            continue
        dur = int(r["duration"]) if (r.get("duration") or "").strip() else turn_for(party, rules)
        rows.append({"name": (r.get("name") or "").strip() or "line %d" % i,
                     "start": start, "party": party, "end": start + dur})
    return rows


def grid(rows, slot, first, last):
    slots = list(range(first - first % slot, last + slot, slot))
    out = []
    for s in slots:
        seated = sum(b["party"] for b in rows if b["start"] < s + slot and b["end"] > s)
        arrivals = sum(b["party"] for b in rows if s <= b["start"] < s + slot)
        out.append((s, seated, arrivals))
    return out


def fits(rows, start, party, rules, args):
    trial = rows + [{"name": "request", "start": start, "party": party,
                     "end": start + turn_for(party, rules)}]
    open_, last_seat = args.window
    if not (open_ <= start <= last_seat):
        return False
    for s, seated, arrivals in grid(trial, args.slot, start, start + turn_for(party, rules) - 1):
        if seated > args.seats or (s <= start < s + args.slot and arrivals > args.pacing):
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bookings", help="bookings CSV, or - for stdin")
    ap.add_argument("--seats", type=int, required=True, help="covers the room can seat at once")
    ap.add_argument("--pacing", type=int, required=True, help="max covers arriving per slot (kitchen pacing)")
    ap.add_argument("--service", required=True, help="START-END, where END is the last seating, e.g. 17:30-21:00")
    ap.add_argument("--slot", type=int, default=15, help="slot length in minutes (default 15)")
    ap.add_argument("--turns", default="2:90,4:105,6:120,999:150", help="turn-time rule max_party:minutes,...")
    ap.add_argument("--try", dest="try_", help="test a request HH:MM,party and suggest alternatives within 60 min")
    args = ap.parse_args()

    rules = parse_turns(args.turns)
    a, b = args.service.split("-")
    args.window = (to_min(a), to_min(b))
    rows = load(args.bookings, rules)

    flags = []
    for r in rows:
        if not (args.window[0] <= r["start"] <= args.window[1]):
            flags.append("%s (%d) arrives %s, outside service %s" % (r["name"], r["party"], to_hhmm(r["start"]), args.service))
    if rows:
        first = min(args.window[0], min(r["start"] for r in rows))
        last = max(r["end"] for r in rows)
    else:
        first, last = args.window
    print("| Slot | Seated covers | Arrivals | Flag |")
    print("| --- | --- | --- | --- |")
    for s, seated, arrivals in grid(rows, args.slot, first, last - 1):
        f = []
        if seated > args.seats:
            f.append("over seats by %d" % (seated - args.seats))
        if arrivals > args.pacing:
            f.append("over pacing by %d" % (arrivals - args.pacing))
        if f:
            flags.append("%s: %s" % (to_hhmm(s), ", ".join(f)))
        print("| %s | %d | %d | %s |" % (to_hhmm(s), seated, arrivals, "; ".join(f)))
    total = sum(r["party"] for r in rows)
    print("\nBookings: %d, covers: %d, seats: %d, pacing per %d min: %d" % (len(rows), total, args.seats, args.slot, args.pacing))
    print("Flags:" if flags else "Flags: none")
    for f in flags:
        print("- " + f)

    if args.try_:
        t, p = args.try_.split(",")
        start, party = to_min(t), int(p)
        print("\nRequest %s for %d: %s" % (t, party, "fits" if fits(rows, start, party, rules, args) else "does not fit"))
        options = []
        for delta in range(args.slot, 61, args.slot):
            for cand in (start - delta, start + delta):
                if fits(rows, cand, party, rules, args):
                    options.append(cand)
        if options:
            print("Alternatives within 60 min: " + ", ".join(to_hhmm(o) for o in sorted(set(options))))
        else:
            print("No alternative within 60 min; offer the waitlist or another service.")


if __name__ == "__main__":
    main()
