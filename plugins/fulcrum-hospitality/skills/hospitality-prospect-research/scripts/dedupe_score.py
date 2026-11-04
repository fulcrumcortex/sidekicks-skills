#!/usr/bin/env python3
"""De-duplicate and score a hospitality prospect research sheet.

Input: a CSV with the columns in assets/prospects-template.csv.
Output (stdout): the same columns plus total_score, max_score, score_percent,
tier, merged_rows and flags, sorted by score (highest first).

Duplicates: rows with the same website host (www. removed), or, when there
is no website, the same normalised business name and postcode. Merged rows
keep the first non-empty value for each column and join differing source URLs
with " | " so no evidence is lost.

Scoring: each dimension has a 0-3 score column and evidence, URL and date
columns: <dim>_score, <dim>_evidence, <dim>_url, <dim>_date.
Default dimensions and weights: booking=2, market=3, size=1, signal=1.
A dimension with a score but no URL or date counts as 0 and is flagged.

Tiers by percent of the maximum possible score:
  A >= 70, B >= 45, C below 45, and HOLD when a check fails (see flags).

Flags raised:
  no-evidence:<dim>      score given without URL and date
  email-no-source        email_published without email_source_url
  email-domain-mismatch  email domain differs from the website host
  stale:<dim>            evidence date older than --stale-days (default 365)
  missing-contact-route  no published phone, email or website

Examples:
  python3 dedupe_score.py prospects.csv > scored.csv
  python3 dedupe_score.py prospects.csv --weights booking=1,market=3,size=2,signal=1 --today 2026-11-05
"""

import argparse
import csv
import re
import sys
from datetime import date
from urllib.parse import urlparse

DEFAULT_WEIGHTS = "booking=2,market=3,size=1,signal=1"
NAME_NOISE = re.compile(r"\b(pty|ltd|limited|the|and|co)\b")


def host(url):
    if not url:
        return ""
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def norm_name(name):
    s = re.sub(r"[^a-z0-9 ]", " ", (name or "").lower().replace("&", " and "))
    s = NAME_NOISE.sub(" ", s)
    return " ".join(s.split())


def key_for(row):
    h = host(row.get("website", ""))
    if h:
        return "host:" + h
    return "name:%s|%s" % (norm_name(row.get("business_name", "")), (row.get("postcode") or "").strip())


def merge(a, b):
    out = dict(a)
    for k, v in b.items():
        v = (v or "").strip()
        cur = (out.get(k) or "").strip()
        if not cur:
            out[k] = v
        elif v and v != cur and (k.endswith("_url") or k == "sources"):
            parts = cur.split(" | ")
            if v not in parts:
                out[k] = cur + " | " + v
    return out


def parse_weights(spec):
    w = {}
    for part in spec.split(","):
        k, v = part.split("=")
        w[k.strip()] = float(v)
    return w


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="prospect CSV, or - for stdin")
    ap.add_argument("--weights", default=DEFAULT_WEIGHTS, help="dimension=weight,... (default %s)" % DEFAULT_WEIGHTS)
    ap.add_argument("--stale-days", type=int, default=365, help="evidence older than this is flagged (default 365)")
    ap.add_argument("--today", help="YYYY-MM-DD used for staleness (default: system date)")
    args = ap.parse_args()

    weights = parse_weights(args.weights)
    today = date.fromisoformat(args.today) if args.today else date.today()
    fh = sys.stdin if args.csv == "-" else open(args.csv, newline="")
    reader = csv.DictReader(fh)
    fields = list(reader.fieldnames or [])

    merged, counts, order = {}, {}, []
    for row in reader:
        if not any((v or "").strip() for v in row.values()):
            continue
        k = key_for(row)
        if k in merged:
            merged[k] = merge(merged[k], row)
            counts[k] += 1
        else:
            merged[k] = {f: (row.get(f) or "").strip() for f in fields}
            counts[k] = 1
            order.append(k)

    max_score = sum(3 * w for w in weights.values())
    out_rows = []
    for k in order:
        r = merged[k]
        flags, total = [], 0.0
        for dim, w in weights.items():
            raw = r.get(dim + "_score", "")
            if raw == "":
                continue
            try:
                s = max(0, min(3, int(float(raw))))
            except ValueError:
                flags.append("bad-score:" + dim)
                continue
            url, d = r.get(dim + "_url", ""), r.get(dim + "_date", "")
            if not url or not d:
                flags.append("no-evidence:" + dim)
                continue
            try:
                if (today - date.fromisoformat(d)).days > args.stale_days:
                    flags.append("stale:" + dim)
            except ValueError:
                flags.append("bad-date:" + dim)
            total += s * w
        email = r.get("email_published", "")
        if email and not r.get("email_source_url"):
            flags.append("email-no-source")
        site = host(r.get("website", ""))
        if email and site and "@" in email:
            edom = email.split("@", 1)[1].lower()
            if not (edom == site or edom.endswith("." + site) or site.endswith("." + edom)):
                flags.append("email-domain-mismatch")
        if not (r.get("phone_published") or email or site):
            flags.append("missing-contact-route")
        pct = round(100 * total / max_score, 1) if max_score else 0.0
        hold = any(f.startswith(("no-evidence", "email-no-source", "bad-")) for f in flags)
        tier = "HOLD" if hold else ("A" if pct >= 70 else "B" if pct >= 45 else "C")
        r.update(total_score=round(total, 2), max_score=max_score, score_percent=pct,
                 tier=tier, merged_rows=counts[k], flags=";".join(flags))
        out_rows.append(r)

    out_rows.sort(key=lambda x: (x["tier"] == "HOLD", -x["score_percent"]))
    extra = ["total_score", "max_score", "score_percent", "tier", "merged_rows", "flags"]
    w = csv.DictWriter(sys.stdout, fieldnames=fields + [e for e in extra if e not in fields])
    w.writeheader()
    w.writerows(out_rows)
    dupes = sum(c - 1 for c in counts.values())
    print("rows in: %d, unique: %d, duplicates merged: %d, held: %d" % (
        sum(counts.values()), len(order), dupes, sum(1 for r in out_rows if r["tier"] == "HOLD")), file=sys.stderr)


if __name__ == "__main__":
    main()
