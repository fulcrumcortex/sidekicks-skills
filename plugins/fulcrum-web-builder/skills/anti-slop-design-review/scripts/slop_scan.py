#!/usr/bin/env python3
"""Scan front-end source for signals of the generic "AI template" look.

Standard library only, no network. Walks a source folder (tsx, jsx, ts, js,
html, css, scss, vue, svelte, astro, mdx) and counts patterns that often mark
templated design: default purple/indigo gradients, gradient text, glass
effects, emoji used as icons, centred-everything layouts, repeated
three-column card grids, one radius plus shadow everywhere, a timid type
scale, decorative motion, stock illustration files, placeholder content and
hype copy.

Counts are evidence for a human review, not a verdict. A pattern used once,
on purpose, can be right. Look at the files listed for each signal.

Usage:
  slop_scan.py src
  slop_scan.py app components --json
  slop_scan.py . --exclude node_modules,.next,dist

Exit status: 0 after a scan, 2 if no source files were found.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

EXTS = {".tsx", ".jsx", ".ts", ".js", ".html", ".css", ".scss", ".vue", ".svelte", ".astro", ".mdx"}
DEFAULT_EXCLUDE = {"node_modules", ".next", "dist", "build", "out", ".git", "coverage", ".turbo", "vendor"}

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\U00002B50\U00002B06\U00002705\U0000274C]"
)

SIGNALS = {
    "purple_blue_gradient": (
        re.compile(r"\b(?:from|via|to)-(?:purple|violet|indigo|fuchsia)-\d{2,3}\b|linear-gradient\([^)]*(?:#(?:8b5cf6|7c3aed|6366f1|4f46e5|a855f7|9333ea|6d28d9|ec4899)|purple|violet|indigo)", re.I),
        "Default purple, violet or indigo gradients",
    ),
    "gradient_text": (re.compile(r"bg-clip-text[^\"'`]*text-transparent|text-transparent[^\"'`]*bg-clip-text|background-clip:\s*text"), "Gradient-filled text"),
    "glass": (re.compile(r"\bbackdrop-blur(?:-\w+)?\b|backdrop-filter:\s*blur"), "Glassmorphism (backdrop blur)"),
    "translucent_white_panels": (re.compile(r"\bbg-white/(?:5|10|15|20)\b|\bborder-white/(?:5|10|15|20)\b"), "Translucent white panels and hairlines"),
    "centred_text": (re.compile(r"\btext-center\b"), "Centred text blocks"),
    "three_col_grid": (re.compile(r"\b(?:sm:|md:|lg:|xl:)?grid-cols-3\b"), "Three-column grids"),
    "transition_all": (re.compile(r"\btransition-all\b|transition:\s*all"), "transition-all (unfocused motion)"),
    "hover_lift": (re.compile(r"hover:(?:scale-1(?:02|05|10)|-translate-y-\d)|whileHover=\{\{\s*scale"), "Hover lift or scale on cards"),
    "decorative_animate": (re.compile(r"\banimate-(?:bounce|pulse|ping)\b"), "Bounce, pulse or ping animations"),
    "blob_orbs": (re.compile(r"\bblur-(?:2xl|3xl)\b|\brounded-full[^\"'`]*\bblur-|blob", re.I), "Blurred orbs and blobs"),
    "sparkle_icons": (re.compile(r"\b(?:Sparkles?|Zap|Rocket|Wand2?|Stars?|Bot|BrainCircuit)\b(?=[\s,}/>])"), "Sparkle, rocket or zap icons"),
    "placeholder_content": (re.compile(r"lorem ipsum|john doe|jane doe|acme(?: corp| inc)?\b|feature (?:one|1)\b|placeholder text|testimonial author", re.I), "Placeholder content"),
    "hype_copy": (re.compile(r"\b(?:unlock|unleash|elevate|seamless(?:ly)?|empower|supercharge|revolutioni[sz]e|cutting-edge|next-gen(?:eration)?|game-chang\w+|effortless(?:ly)?|transform your)\b", re.I), "Hype copy"),
    "stock_illustration": (re.compile(r"undraw_|storyset|illustration[-_]\w*\.(?:svg|png)|hero[-_]illustration|3d[-_]\w+\.(?:png|webp)", re.I), "Stock illustration assets"),
}

RADIUS_RE = re.compile(r"\brounded(?:-(?:none|xs|sm|md|lg|xl|2xl|3xl|full|\[[^\]]+\]|[a-z-]+))?\b")
SHADOW_RE = re.compile(r"\bshadow(?:-(?:xs|sm|md|lg|xl|2xl|none|\[[^\]]+\]|[a-z-]+))?\b")
TEXT_SIZE_RE = re.compile(r"\btext-(xs|sm|base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl)\b")
CLASS_ATTR_RE = re.compile(r"class(?:Name)?=(?:\"([^\"]*)\"|'([^']*)'|\{`([^`]*)`\})")
FONT_RE = re.compile(r"\b(Inter|Roboto|Poppins|Montserrat|Open_Sans|Open Sans|Lato|Space_Grotesk|Space Grotesk)\b")
SIZE_ORDER = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl", "8xl", "9xl"]


def iter_files(roots: list[str], exclude: set[str]):
    for root in roots:
        if os.path.isfile(root):
            yield root
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in exclude]
            for f in filenames:
                if os.path.splitext(f)[1] in EXTS:
                    yield os.path.join(dirpath, f)


def scan(roots: list[str], exclude: set[str]) -> dict:
    counts: Counter = Counter()
    where: dict[str, Counter] = defaultdict(Counter)
    radius: Counter = Counter()
    radius_shadow_pairs = 0
    class_lists = 0
    sizes: Counter = Counter()
    fonts: Counter = Counter()
    emoji_files: Counter = Counter()
    files = 0
    clamp_type = 0
    for path in iter_files(roots, exclude):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"warning: skipped {path}: {exc.strerror or exc}", file=sys.stderr)
            continue
        files += 1
        for key, (rx, _) in SIGNALS.items():
            n = len(rx.findall(text))
            if n:
                counts[key] += n
                where[key][path] += n
        if path.endswith((".tsx", ".jsx", ".html", ".vue", ".svelte", ".astro", ".mdx")):
            stripped = re.sub(r"(?s)/\*.*?\*/|//[^\n]*", "", text)
            n = len(EMOJI_RE.findall(stripped))
            if n:
                emoji_files[path] += n
        for m in CLASS_ATTR_RE.finditer(text):
            cls = next(g for g in m.groups() if g is not None)
            class_lists += 1
            r = RADIUS_RE.findall(cls)
            s = [x for x in SHADOW_RE.findall(cls) if x != "shadow-none"]
            for x in r:
                radius[x] += 1
            if r and s:
                radius_shadow_pairs += 1
            for size in TEXT_SIZE_RE.findall(cls):
                sizes[size] += 1
        for f in FONT_RE.findall(text):
            fonts[f.replace("_", " ")] += 1
        clamp_type += len(re.findall(r"--text-[\w-]+:\s*clamp\(|font-size:\s*clamp\(", text))
    return {
        "files": files,
        "counts": counts,
        "where": where,
        "radius": radius,
        "radius_shadow_pairs": radius_shadow_pairs,
        "class_lists": class_lists,
        "sizes": sizes,
        "fonts": fonts,
        "emoji_files": emoji_files,
        "clamp_type": clamp_type,
    }


def findings(r: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    c = r["counts"]
    if c["purple_blue_gradient"] >= 2:
        out.append(("strong", f"{c['purple_blue_gradient']} purple/indigo gradient uses: the default AI palette unless it is the brand"))
    if c["gradient_text"] >= 2:
        out.append(("medium", f"{c['gradient_text']} gradient-text headings: usually decoration standing in for a typographic idea"))
    if c["glass"] >= 4:
        out.append(("medium", f"{c['glass']} backdrop-blur uses: glass everywhere flattens hierarchy and costs performance"))
    if r["emoji_files"]:
        total = sum(r["emoji_files"].values())
        out.append(("strong" if total >= 5 else "medium", f"{total} emoji in markup across {len(r['emoji_files'])} files: emoji used as icons or decoration"))
    if c["three_col_grid"] >= 3:
        out.append(("medium", f"{c['three_col_grid']} three-column grids: check for identical icon-title-text card rows"))
    if c["centred_text"] >= 8:
        out.append(("medium", f"{c['centred_text']} text-center uses: check whether every section is centred"))
    total_radius = sum(r["radius"].values())
    if total_radius >= 10:
        top, n = r["radius"].most_common(1)[0]
        share = n / total_radius
        if share >= 0.6:
            out.append(("medium", f"'{top}' is {share:.0%} of all radius classes: one radius on everything"))
    if r["radius_shadow_pairs"] >= 8:
        out.append(("medium", f"{r['radius_shadow_pairs']} elements combine rounded and shadow: the default card look"))
    if r["sizes"]:
        largest = max(r["sizes"], key=SIZE_ORDER.index)
        if SIZE_ORDER.index(largest) <= SIZE_ORDER.index("4xl") and not r["clamp_type"]:
            out.append(("medium", f"largest text size used is text-{largest} and no fluid display size exists: timid type scale"))
    if c["transition_all"] >= 5 or c["hover_lift"] >= 4 or c["decorative_animate"] >= 2:
        out.append(("medium", f"motion: {c['transition_all']} transition-all, {c['hover_lift']} hover lifts, {c['decorative_animate']} bounce/pulse/ping: check each has a purpose"))
    if c["blob_orbs"] >= 3:
        out.append(("low", f"{c['blob_orbs']} blurred orb or blob patterns"))
    if c["sparkle_icons"] >= 3:
        out.append(("low", f"{c['sparkle_icons']} sparkle/rocket/zap style icons"))
    if c["placeholder_content"]:
        out.append(("strong", f"{c['placeholder_content']} placeholder content strings (lorem ipsum, John Doe, Acme)"))
    if c["hype_copy"] >= 3:
        out.append(("medium", f"{c['hype_copy']} hype words in source (unlock, elevate, seamless...)"))
    if c["stock_illustration"]:
        out.append(("low", f"{c['stock_illustration']} references to stock illustration files"))
    if r["fonts"]:
        names = ", ".join(f"{k} x{v}" for k, v in r["fonts"].most_common(3))
        out.append(("info", f"common default typefaces referenced ({names}): fine if chosen on purpose; check there is a display face with character"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", help="source folders or files to scan")
    ap.add_argument("--exclude", default=",".join(sorted(DEFAULT_EXCLUDE)), help="comma-separated folder names to skip")
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args(argv)
    for p in args.paths:
        if not os.path.exists(p):
            print(f"warning: path not found: {p}", file=sys.stderr)
    r = scan(args.paths, {x.strip() for x in args.exclude.split(",") if x.strip()})
    if not r["files"]:
        print(f"error: no source files found (looked for {', '.join(sorted(EXTS))})", file=sys.stderr)
        return 2
    f = findings(r)
    if args.json:
        print(json.dumps({
            "files": r["files"],
            "counts": dict(r["counts"]),
            "top_files": {k: v.most_common(5) for k, v in r["where"].items()},
            "radius": dict(r["radius"]),
            "radius_shadow_pairs": r["radius_shadow_pairs"],
            "text_sizes": dict(r["sizes"]),
            "emoji_files": dict(r["emoji_files"]),
            "findings": f,
        }, indent=2))
        return 0
    base = args.paths[0] if os.path.isdir(args.paths[0]) else os.path.dirname(args.paths[0]) or "."

    def rel(p: str) -> str:
        return os.path.relpath(p, base)

    print(f"scanned {r['files']} files under {', '.join(args.paths)}\n")
    print("signals:")
    for key, (_, label) in SIGNALS.items():
        n = r["counts"][key]
        if n:
            top = ", ".join(f"{rel(p)} ({k})" for p, k in r["where"][key].most_common(3))
            print(f"  {label:<46} {n:>4}   {top}")
    if r["emoji_files"]:
        top = ", ".join(f"{rel(p)} ({k})" for p, k in r["emoji_files"].most_common(3))
        print(f"  {'Emoji in markup':<46} {sum(r['emoji_files'].values()):>4}   {top}")
    if r["radius"]:
        print("  radius classes: " + ", ".join(f"{k} x{v}" for k, v in r["radius"].most_common(5)))
    if r["sizes"]:
        print("  text sizes: " + ", ".join(f"{s} x{r['sizes'][s]}" for s in SIZE_ORDER if s in r["sizes"]))
    print("\nfindings (evidence for review, not verdicts):")
    order = {"strong": 0, "medium": 1, "low": 2, "info": 3}
    for sev, msg in sorted(f, key=lambda x: order[x[0]]) or [("-", "no strong template signals found")]:
        print(f"  [{sev}] {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
