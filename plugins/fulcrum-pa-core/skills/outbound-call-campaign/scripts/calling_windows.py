#!/usr/bin/env python3
"""Show the permitted telemarketing calling window for each Australian time
zone on a given date, translated into the calling platform's time zone.

The recipient's local window (default Monday to Friday 09:00-20:00,
Saturday 09:00-17:00, no Sunday, no national public holiday) is intersected
with the platform's own calling window (default the same hours in
Australia/Sydney time). The "ALL ZONES" row is the window that is valid in
every Australian time zone; use it for recipients whose state is unknown.

National public holidays flagged: 1 Jan, 26 Jan, Good Friday, Easter Monday,
25 Apr, 25 Dec, 26 Dec. Check the current industry standard for substitute
days. Local public holidays are not checked.

Examples:
  python3 calling_windows.py --date 2026-11-09
  python3 calling_windows.py --date 2026-11-14 --platform-tz Australia/Sydney
  python3 calling_windows.py --date 2026-11-09 --days 7
"""

import argparse
import datetime as dt
import sys

try:
    from zoneinfo import ZoneInfo
except ImportError:  # Python < 3.9
    sys.exit("Python 3.9 or later is required (zoneinfo).")

ZONES = [
    ("NSW/ACT/VIC/TAS", "Australia/Sydney"),
    ("QLD", "Australia/Brisbane"),
    ("SA", "Australia/Adelaide"),
    ("NT", "Australia/Darwin"),
    ("WA", "Australia/Perth"),
]


def easter(year):
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def national_holidays(year):
    e = easter(year)
    return {
        dt.date(year, 1, 1): "New Year's Day",
        dt.date(year, 1, 26): "Australia Day",
        e - dt.timedelta(days=2): "Good Friday",
        e + dt.timedelta(days=1): "Easter Monday",
        dt.date(year, 4, 25): "Anzac Day",
        dt.date(year, 12, 25): "Christmas Day",
        dt.date(year, 12, 26): "Boxing Day",
    }


def parse_hhmm(s):
    h, m = s.split(":")
    return dt.time(int(h), int(m))


def window_for(day, weekday_hours, saturday_hours):
    wd = day.weekday()
    if wd < 5:
        return weekday_hours
    if wd == 5:
        return saturday_hours
    return None


def to_platform(day, hours, zone, platform_zone):
    start = dt.datetime.combine(day, hours[0], tzinfo=ZoneInfo(zone)).astimezone(platform_zone)
    end = dt.datetime.combine(day, hours[1], tzinfo=ZoneInfo(zone)).astimezone(platform_zone)
    return start, end


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", help="first calling date, YYYY-MM-DD (default today)")
    ap.add_argument("--days", type=int, default=1, help="number of consecutive days to show (default 1)")
    ap.add_argument("--platform-tz", default="Australia/Sydney", help="time zone the calling platform uses")
    ap.add_argument("--weekday", default="09:00-20:00", help="recipient-local weekday window")
    ap.add_argument("--saturday", default="09:00-17:00", help="recipient-local Saturday window")
    ap.add_argument("--platform-weekday", default="09:00-20:00", help="platform weekday window in platform time")
    ap.add_argument("--platform-saturday", default="09:00-17:00", help="platform Saturday window in platform time")
    args = ap.parse_args()

    def rng(s):
        a, b = s.split("-")
        return parse_hhmm(a), parse_hhmm(b)

    local_wd, local_sat = rng(args.weekday), rng(args.saturday)
    plat_wd, plat_sat = rng(args.platform_weekday), rng(args.platform_saturday)
    pz = ZoneInfo(args.platform_tz)
    first = dt.date.fromisoformat(args.date) if args.date else dt.date.today()

    for n in range(args.days):
        day = first + dt.timedelta(days=n)
        print(f"\n{day.strftime('%A %d %B %Y')}  (times shown in {args.platform_tz})")
        hol = national_holidays(day.year).get(day)
        if hol:
            print(f"  NO CALLS: national public holiday ({hol}).")
            continue
        local = window_for(day, local_wd, local_sat)
        plat = window_for(day, plat_wd, plat_sat)
        if local is None or plat is None:
            print("  NO CALLS: Sunday (or no platform window).")
            continue
        p_start = dt.datetime.combine(day, plat[0], tzinfo=pz)
        p_end = dt.datetime.combine(day, plat[1], tzinfo=pz)
        all_start, all_end = p_start, p_end
        for label, zone in ZONES:
            s, e = to_platform(day, local, zone, pz)
            s, e = max(s, p_start), min(e, p_end)
            all_start, all_end = max(all_start, s), min(all_end, e)
            if s >= e:
                print(f"  {label:<16} no overlap with platform window")
            else:
                print(f"  {label:<16} {s:%H:%M}-{e:%H:%M}")
        if all_start >= all_end:
            print(f"  {'ALL ZONES':<16} no common window")
        else:
            print(f"  {'ALL ZONES':<16} {all_start:%H:%M}-{all_end:%H:%M}   (use for unknown state)")
    print("\nCheck substitute and local public holidays separately. Windows assume no consent to out-of-hours calls.")


if __name__ == "__main__":
    main()
