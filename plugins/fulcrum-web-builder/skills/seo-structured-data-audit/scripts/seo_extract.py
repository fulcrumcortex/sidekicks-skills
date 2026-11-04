#!/usr/bin/env python3
"""Extract on-page SEO signals and JSON-LD from saved HTML (standard library only).

Reads one or more HTML files (or '-' for stdin) and reports: <html lang>,
title, meta description, robots directives, canonical, hreflang alternates,
Open Graph and Twitter tags, heading outline, images without alt, link
counts, and every JSON-LD block with its @type values and missing
recommended properties. Ends with a list of issues tagged HIGH, MEDIUM or LOW.

It makes no network calls. Save the rendered HTML first, for example:
  curl -sL https://www.example.com/ -o home.html
For client-rendered pages, save the DOM from the browser instead
(DevTools > Elements > Copy outerHTML), because crawlers may not run your JS.

Usage:
  seo_extract.py home.html [about.html ...] [--base https://www.example.com] [--json]

Exit status: 0 when no HIGH issues, 1 when any HIGH issue is found, 2 on errors.
"""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

TITLE_MAX = 60
DESC_MIN, DESC_MAX = 70, 160

# Properties worth checking per type. Google's required/recommended lists change;
# confirm in the Rich Results Test. These catch the common omissions.
TYPE_CHECKS = {
    "Organization": ["name", "url", "logo"],
    "LocalBusiness": ["name", "address", "telephone", "url"],
    "Product": ["name", "image", "offers|review|aggregateRating"],
    "Offer": ["price", "priceCurrency", "availability"],
    "Article": ["headline", "image", "datePublished", "author"],
    "BlogPosting": ["headline", "image", "datePublished", "author"],
    "NewsArticle": ["headline", "image", "datePublished", "author"],
    "BreadcrumbList": ["itemListElement"],
    "FAQPage": ["mainEntity"],
    "WebSite": ["name", "url"],
    "Service": ["name", "provider"],
    "Event": ["name", "startDate", "location"],
}
LOCAL_BUSINESS_SUBTYPES = {
    "LocalBusiness", "ProfessionalService", "HomeAndConstructionBusiness", "Electrician", "Plumber",
    "RoofingContractor", "HVACBusiness", "GeneralContractor", "HousePainter", "Locksmith",
    "MedicalBusiness", "Dentist", "Physician", "MedicalClinic", "Optician", "Pharmacy",
    "FoodEstablishment", "Restaurant", "CafeOrCoffeeShop", "Bakery", "BarOrPub",
    "LodgingBusiness", "Hotel", "Motel", "BedAndBreakfast", "HealthAndBeautyBusiness",
    "BeautySalon", "HairSalon", "DaySpa", "AutomotiveBusiness", "AutoRepair", "AutoDealer",
    "LegalService", "Attorney", "AccountingService", "FinancialService", "RealEstateAgent",
    "Store", "ChildCare", "SportsActivityLocation", "ExerciseGym", "AnimalShelter",
    "EmergencyService", "EmploymentAgency", "TravelAgency", "InsuranceAgency",
}


class Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title_parts: list[str] = []
        self.in_title = False
        self.metas: list[dict] = []
        self.links: list[dict] = []
        self.headings: list[tuple[int, str]] = []
        self._heading: list | None = None
        self.images: list[dict] = []
        self.anchors: list[dict] = []
        self._anchor: dict | None = None
        self.jsonld: list[str] = []
        self._script: list[str] | None = None
        self.microdata = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if "itemtype" in a:
            self.microdata += 1
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._heading = [int(tag[1]), []]
        elif tag == "img":
            self.images.append(a)
        elif tag == "a":
            self._anchor = {"href": a.get("href", ""), "rel": a.get("rel", ""), "text": [], "aria": a.get("aria-label", "")}
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self._script = []
        if self._anchor is not None and tag == "img":
            self._anchor["text"].append(a.get("alt", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._heading:
            self.headings.append((self._heading[0], " ".join("".join(self._heading[1]).split())))
            self._heading = None
        elif tag == "a" and self._anchor is not None:
            self._anchor["text"] = " ".join("".join(self._anchor["text"]).split())
            self.anchors.append(self._anchor)
            self._anchor = None
        elif tag == "script" and self._script is not None:
            self.jsonld.append("".join(self._script))
            self._script = None

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self._heading is not None:
            self._heading[1].append(data)
        if self._anchor is not None:
            self._anchor["text"].append(data)
        if self._script is not None:
            self._script.append(data)


def meta(c: Collector, key: str, attr: str = "name") -> list[str]:
    return [m.get("content", "") for m in c.metas if m.get(attr, "").lower() == key]


def iter_nodes(data):
    if isinstance(data, list):
        for item in data:
            yield from iter_nodes(item)
    elif isinstance(data, dict):
        if "@graph" in data:
            yield from iter_nodes(data["@graph"])
        if "@type" in data:
            yield data
        for key, value in data.items():
            if key != "@graph" and isinstance(value, (dict, list)):
                yield from iter_nodes(value)


def check_node(node: dict) -> tuple[list[str], list[str]]:
    raw = node["@type"] if isinstance(node["@type"], list) else [node["@type"]]
    # @type should be a string or a list of strings; anything else would crash
    # the set lookups below, so stringify it and report it.
    types = [t if isinstance(t, str) else json.dumps(t) for t in raw]
    missing: list[str] = []
    notes: list[str] = []
    if any(not isinstance(t, str) for t in raw):
        missing.append("@type must be a string or a list of strings")
    for t in types:
        key = "LocalBusiness" if t in LOCAL_BUSINESS_SUBTYPES else t
        for prop in TYPE_CHECKS.get(key, []):
            if not any(p in node for p in prop.split("|")):
                missing.append(f"{t}.{prop}")
        if key == "LocalBusiness" and isinstance(node.get("address"), dict):
            for p in ("streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry"):
                if p not in node["address"]:
                    missing.append(f"{t}.address.{p}")
        if t == "FAQPage":
            notes.append("FAQPage: Google stopped showing FAQ rich results in 2026; markup gives no Google snippet")
        if t == "HowTo":
            notes.append("HowTo: Google no longer shows HowTo rich results")
        if t == "BreadcrumbList" and isinstance(node.get("itemListElement"), list):
            for i, item in enumerate(node["itemListElement"], 1):
                if isinstance(item, dict) and ("position" not in item or "name" not in item):
                    missing.append(f"BreadcrumbList.itemListElement[{i}] position/name")
    return types, missing + notes


def analyse(html: str, source: str, base: str | None) -> dict:
    c = Collector()
    c.feed(html)
    c.close()
    if c._script is not None:  # unterminated <script type="application/ld+json">
        c.jsonld.append("".join(c._script))
    issues: list[tuple[str, str]] = []
    title = " ".join("".join(c.title_parts).split())
    descs = meta(c, "description")
    robots = meta(c, "robots") + meta(c, "googlebot")
    canonicals = [l.get("href", "") for l in c.links if "canonical" in l.get("rel", "").lower().split()]
    hreflangs = [(l.get("hreflang", ""), l.get("href", "")) for l in c.links
                 if "alternate" in l.get("rel", "").lower().split() and l.get("hreflang")]
    og = {m.get("property", ""): m.get("content", "") for m in c.metas if m.get("property", "").startswith("og:")}
    tw = {m.get("name", ""): m.get("content", "") for m in c.metas if m.get("name", "").startswith("twitter:")}

    if not c.lang:
        issues.append(("MEDIUM", "<html> has no lang attribute (use en-AU for an Australian site)"))
    if not title:
        issues.append(("HIGH", "missing <title>"))
    elif len(title) > TITLE_MAX:
        issues.append(("LOW", f"title is {len(title)} characters; likely truncated beyond about {TITLE_MAX}"))
    if not descs:
        issues.append(("MEDIUM", "missing meta description"))
    elif len(descs) > 1:
        issues.append(("MEDIUM", f"{len(descs)} meta descriptions"))
    elif not DESC_MIN <= len(descs[0]) <= DESC_MAX:
        issues.append(("LOW", f"meta description is {len(descs[0])} characters (aim for about {DESC_MIN}-{DESC_MAX})"))
    if any("noindex" in r.lower() for r in robots):
        issues.append(("HIGH", f"robots meta contains noindex: {robots}"))
    if not canonicals:
        issues.append(("MEDIUM", "no rel=canonical"))
    elif len(canonicals) > 1:
        issues.append(("HIGH", f"{len(canonicals)} canonical links: {canonicals}"))
    elif not urlparse(canonicals[0]).scheme:
        issues.append(("LOW", f"canonical is relative ({canonicals[0]}); use an absolute URL"))
    if hreflangs:
        codes = [h for h, _ in hreflangs]
        if "x-default" not in codes:
            issues.append(("LOW", "hreflang set has no x-default"))
        if any(h.lower() == "en-au" for h in codes) is False and c.lang and c.lang.lower() == "en-au":
            issues.append(("LOW", "page is en-AU but its hreflang set does not list en-AU (pages must reference themselves)"))
    for key in ("og:title", "og:description", "og:image", "og:url"):
        if key not in og:
            issues.append(("LOW", f"missing {key}"))
    if "og:image" in og and not urlparse(og["og:image"]).scheme:
        issues.append(("MEDIUM", "og:image is relative; social platforms need an absolute URL"))

    h1s = [t for lvl, t in c.headings if lvl == 1]
    if len(h1s) != 1:
        issues.append(("MEDIUM", f"{len(h1s)} <h1> elements (expect exactly one)"))
    prev = 0
    for lvl, text in c.headings:
        if prev and lvl > prev + 1:
            issues.append(("LOW", f"heading level skipped: h{prev} -> h{lvl} ('{text[:50]}')"))
        prev = lvl

    no_alt = [i.get("src", "")[:80] for i in c.images if "alt" not in i]
    if no_alt:
        issues.append(("MEDIUM", f"{len(no_alt)} <img> without an alt attribute"))

    host = urlparse(base).netloc if base else None
    internal = external = 0
    empty_text = []
    for a in c.anchors:
        href = a["href"]
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        full = urljoin(base or "", href)
        if not urlparse(full).netloc or (host and urlparse(full).netloc == host):
            internal += 1
        else:
            external += 1
        if not a["text"] and not a["aria"]:
            empty_text.append(href[:80])
    if empty_text:
        issues.append(("MEDIUM", f"{len(empty_text)} links with no text or aria-label"))
    generic = [a["text"] for a in c.anchors if a["text"].lower() in {"click here", "read more", "learn more", "here", "more"}]
    if generic:
        issues.append(("LOW", f"{len(generic)} links with generic text ('{generic[0]}')"))

    blocks = []
    for raw in c.jsonld:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            issues.append(("HIGH", f"JSON-LD block does not parse: {exc}"))
            continue
        for node in iter_nodes(data):
            types, problems = check_node(node)
            blocks.append({"types": types, "problems": problems})
            for p in problems:
                sev = "LOW" if p.startswith(("FAQPage:", "HowTo:")) else "MEDIUM"
                issues.append((sev, f"JSON-LD {p}" if not p.startswith(("FAQPage:", "HowTo:")) else p))
    if not c.jsonld:
        issues.append(("LOW", "no JSON-LD found"))
    if c.microdata:
        issues.append(("LOW", f"{c.microdata} microdata itemtype attributes found; check they do not conflict with JSON-LD"))

    return {
        "source": source,
        "lang": c.lang,
        "title": title,
        "title_length": len(title),
        "description": descs[0] if descs else None,
        "description_length": len(descs[0]) if descs else 0,
        "robots": robots,
        "canonical": canonicals,
        "hreflang": hreflangs,
        "open_graph": og,
        "twitter": tw,
        "headings": c.headings,
        "images_total": len(c.images),
        "images_missing_alt": no_alt,
        "links_internal": internal,
        "links_external": external,
        "jsonld": blocks,
        "issues": issues,
    }


def print_report(r: dict) -> None:
    print(f"== {r['source']}")
    print(f"lang: {r['lang']}")
    print(f"title ({r['title_length']}): {r['title']}")
    print(f"description ({r['description_length']}): {r['description']}")
    print(f"robots: {r['robots'] or '-'}")
    print(f"canonical: {r['canonical'] or '-'}")
    if r["hreflang"]:
        print("hreflang: " + ", ".join(f"{h} -> {u}" for h, u in r["hreflang"]))
    print("open graph: " + (", ".join(f"{k}={v[:60]}" for k, v in r["open_graph"].items()) or "-"))
    print("headings:")
    for lvl, text in r["headings"][:40]:
        print(f"  {'  ' * (lvl - 1)}h{lvl}: {text[:90]}")
    print(f"images: {r['images_total']} total, {len(r['images_missing_alt'])} without alt")
    print(f"links: {r['links_internal']} internal, {r['links_external']} external")
    print("json-ld:")
    for b in r["jsonld"] or [{"types": ["(none)"], "problems": []}]:
        print(f"  {', '.join(b['types'])}" + (f"  [{'; '.join(b['problems'])}]" if b["problems"] else ""))
    print("issues:")
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    for sev, msg in sorted(r["issues"], key=lambda x: order[x[0]]) or [("-", "none")]:
        print(f"  {sev:<6} {msg}")
    print()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="+", help="saved HTML files, or - for stdin")
    p.add_argument("--base", help="site origin, used to classify links as internal (for example https://www.example.com)")
    p.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = p.parse_args(argv)
    results = []
    for f in args.files:
        try:
            if f == "-":
                html = sys.stdin.read()
            else:
                with open(f, encoding="utf-8", errors="replace") as fh:
                    html = fh.read()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        if not html.strip():
            print(f"warning: {f} is empty", file=sys.stderr)
        results.append(analyse(html, f, args.base))
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_report(r)
        titles = [r["title"] for r in results if r["title"]]
        dupes = {t for t in titles if titles.count(t) > 1}
        if dupes:
            print("cross-page: duplicate titles: " + "; ".join(sorted(dupes)))
    return 1 if any(sev == "HIGH" for r in results for sev, _ in r["issues"]) else 0


if __name__ == "__main__":
    sys.exit(main())
