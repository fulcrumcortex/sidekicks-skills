#!/usr/bin/env python3
"""WCAG 2.x contrast checker for design tokens (Python standard library only).

Checks colour pairs with the WCAG relative luminance formula and reports the
ratio against the thresholds that apply to each use:

  text   normal-size text          AA 4.5:1   AAA 7:1     (SC 1.4.3 / 1.4.6)
  large  >= 24px, or >= 18.66px bold  AA 3:1  AAA 4.5:1   (SC 1.4.3 / 1.4.6)
  ui     UI component boundaries, focus indicators, meaningful icons and
         graphics                  AA 3:1                 (SC 1.4.11)

Accepted colour formats: #rgb, #rgba, #rrggbb, #rrggbbaa, rgb()/rgba(),
hsl()/hsla(), oklch(L C H [/ alpha]) with L as 0-1 or a percentage, and the
keywords white, black and transparent. A semi-transparent foreground is
composited over the background first. Out-of-gamut OKLCH is clipped to sRGB
with a warning, as browsers on sRGB displays do.

Usage:
  contrast_check.py "#1a1a1a" "#ffffff"
  contrast_check.py "oklch(55% 0.2 260)" "oklch(98% 0.01 260)" --use ui
  contrast_check.py --pairs pairs.csv --css theme.css [--scope dark] [--suggest]

pairs.csv has a header row: fg,bg,use[,label]. fg and bg are colours or token
names such as --color-ink or var(--color-ink), resolved from --css.
With --scope dark, declarations inside selectors or at-rules that mention
"dark" override the light values.

Exit status: 0 if every pair meets AA for its use, 1 if any pair fails,
2 on input errors (bad rows are reported, skipped, and make the exit 2).
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys

RGB = tuple[float, float, float]  # subscripting tuple at runtime needs Python 3.9+
THRESHOLDS = {"text": (4.5, 7.0), "large": (3.0, 4.5), "ui": (3.0, None)}


class ColourError(ValueError):
    pass


# ---------- colour parsing ----------

def _num(token: str, scale: float = 1.0) -> float:
    token = token.strip()
    if token.endswith("%"):
        return float(token[:-1]) / 100.0 * scale
    return float(token)


def _clamp01(c: float) -> float:
    return min(1.0, max(0.0, c))


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_srgb(L: float, C: float, H: float) -> tuple[tuple[float, float, float], bool]:
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )
    clipped = any(c < -1e-4 or c > 1 + 1e-4 for c in lin)
    r, g, b = (_linear_to_srgb(_clamp01(c)) for c in lin)
    return (r, g, b), clipped


def srgb_to_oklch(rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l_, m_, s_))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return L, C, H


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    def f(n: float) -> float:
        k = (n + h / 30) % 12
        a = s * min(l, 1 - l)
        return l - a * max(-1, min(k - 3, 9 - k, 1))
    return f(0), f(8), f(4)


def parse_colour(text: str) -> tuple[tuple[float, float, float], float, list[str]]:
    """Return ((r, g, b) in 0-1 sRGB, alpha, warnings)."""
    s = text.strip().lower()
    warnings: list[str] = []
    if s == "white":
        return (1.0, 1.0, 1.0), 1.0, warnings
    if s == "black":
        return (0.0, 0.0, 0.0), 1.0, warnings
    if s == "transparent":
        return (0.0, 0.0, 0.0), 0.0, warnings
    if s.startswith("#"):
        h = s[1:]
        if len(h) in (3, 4):
            h = "".join(ch * 2 for ch in h)
        if len(h) not in (6, 8) or not re.fullmatch(r"[0-9a-f]+", h):
            raise ColourError(f"bad hex colour: {text}")
        r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
        alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return (r, g, b), alpha, warnings
    m = re.fullmatch(r"(rgba?|hsla?|oklch)\((.*)\)", s)
    if not m:
        raise ColourError(f"unsupported colour: {text}")
    fn, body = m.group(1), m.group(2)
    alpha = 1.0
    if "/" in body:
        body, a = body.split("/", 1)
        alpha = _num(a)
    parts = [p for p in re.split(r"[\s,]+", body.strip()) if p]
    if fn.startswith("rgb"):
        if len(parts) == 4:
            alpha = _num(parts.pop())
        if len(parts) != 3:
            raise ColourError(f"bad rgb(): {text}")
        r, g, b = (_clamp01(_num(p, 255) / 255) for p in parts)
        return (r, g, b), _clamp01(alpha), warnings
    if fn.startswith("hsl"):
        if len(parts) == 4:
            alpha = _num(parts.pop())
        if len(parts) != 3:
            raise ColourError(f"bad hsl(): {text}")
        h = float(parts[0].replace("deg", ""))
        # CSS Color 4 allows bare numbers (0-100) for saturation and lightness.
        sat, light = (_clamp01(_num(p) if p.endswith("%") else float(p) / 100) for p in parts[1:])
        return _hsl_to_rgb(h, sat, light), _clamp01(alpha), warnings
    if len(parts) != 3:
        raise ColourError(f"bad oklch(): {text}")
    L = _num(parts[0])
    C = _num(parts[1], 0.4)  # CSS: 100% chroma = 0.4
    H = 0.0 if parts[2] == "none" else float(parts[2].replace("deg", ""))
    rgb, clipped = oklch_to_srgb(L, C, H)
    if clipped:
        warnings.append(f"{text} is outside sRGB and was clipped; reduce chroma for a predictable result")
    return rgb, _clamp01(alpha), warnings


# ---------- WCAG maths ----------

def luminance(rgb: tuple[float, float, float]) -> float:
    r, g, b = (_srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: tuple[float, float, float], bg: tuple[float, float, float]) -> float:
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def composite(fg: RGB, alpha: float, bg: RGB) -> RGB:
    r, g, b = (alpha * f + (1 - alpha) * k for f, k in zip(fg, bg))
    return (r, g, b)


def suggest(fg_rgb: RGB, bg_rgb: RGB, target: float) -> str | None:
    """Move the foreground's OKLCH lightness away from the background until it passes."""
    L, C, H = srgb_to_oklch(fg_rgb)
    darker = luminance(bg_rgb) > 0.18
    step = -0.005 if darker else 0.005
    cand = L
    for _ in range(400):
        cand += step
        if not 0 <= cand <= 1:
            return None
        rgb, _ = oklch_to_srgb(cand, C, H)
        if ratio(rgb, bg_rgb) >= target:
            return f"oklch({cand * 100:.1f}% {C:.3f} {H:.1f})"
    return None


# ---------- CSS token resolution ----------

DECL_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;{}]+);")


def load_tokens(css: str, scope: str) -> dict[str, str]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    light: dict[str, str] = {}
    dark: dict[str, str] = {}
    stack: list[str] = []
    buf = ""
    for ch in css:
        if ch == "{":
            stack.append(buf.strip().lower())
            buf = ""
        elif ch == "}":
            for name, value in DECL_RE.findall(buf + ";"):
                target = dark if any("dark" in sel for sel in stack) else light
                target[name] = value.strip()
            buf = ""
            if stack:
                stack.pop()
        elif ch == ";":
            for name, value in DECL_RE.findall(buf + ";"):
                target = dark if any("dark" in sel for sel in stack) else light
                target[name] = value.strip()
            buf = ""
        else:
            buf += ch
    tokens = dict(light)
    if scope == "dark":
        tokens.update(dark)
    return tokens


def resolve(value: str, tokens: dict[str, str], depth: int = 0) -> str:
    value = value.strip()
    if depth > 20:
        raise ColourError(f"token chain too deep at {value}")
    m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)", value)
    if m:
        name, fallback = m.group(1), m.group(2)
        if name in tokens:
            return resolve(tokens[name], tokens, depth + 1)
        if fallback:
            return resolve(fallback, tokens, depth + 1)
        raise ColourError(f"unknown token {name}")
    if value.startswith("--"):
        if value not in tokens:
            raise ColourError(f"unknown token {value}")
        return resolve(tokens[value], tokens, depth + 1)
    return value


# ---------- reporting ----------

def check(fg_text: str, bg_text: str, use: str, label: str, tokens: dict[str, str], want_suggest: bool) -> dict:
    if use not in THRESHOLDS:
        raise ColourError(f"use must be one of {', '.join(THRESHOLDS)}, got {use!r}")
    fg_rgb, fg_a, w1 = parse_colour(resolve(fg_text, tokens))
    bg_rgb, bg_a, w2 = parse_colour(resolve(bg_text, tokens))
    warnings = w1 + w2
    if bg_a < 1:
        warnings.append(f"background {bg_text} is translucent; checked as if over white")
        bg_rgb = composite(bg_rgb, bg_a, (1.0, 1.0, 1.0))
    if fg_a < 1:
        fg_rgb = composite(fg_rgb, fg_a, bg_rgb)
    r = ratio(fg_rgb, bg_rgb)
    aa, aaa = THRESHOLDS[use]
    passed = r >= aa
    row = {
        "label": label or f"{fg_text} on {bg_text}",
        "use": use,
        "ratio": r,
        "aa": "pass" if passed else "FAIL",
        "aaa": "-" if aaa is None else ("pass" if r >= aaa else "fail"),
        "suggest": "",
        "warnings": warnings,
    }
    if not passed and want_suggest:
        row["suggest"] = suggest(fg_rgb, bg_rgb, aa) or "no passing lightness at this hue and chroma"
    return row


def read_pairs(path: str) -> tuple[list[tuple[str, str, str, str]], int]:
    """Read fg,bg,use[,label] rows. Bad rows are reported to stderr and skipped."""
    jobs: list[tuple[str, str, str, str]] = []
    bad = 0
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise ValueError("file is empty; expected a header row fg,bg,use[,label]")
        header = {(f or "").strip().lower() for f in reader.fieldnames}
        missing = [c for c in ("fg", "bg") if c not in header]
        if missing:
            raise ValueError(f"missing required column(s): {', '.join(missing)} (header must be fg,bg,use[,label])")
        for line, rec in enumerate(reader, 2):
            rec = {(k or "").strip().lower(): (v if isinstance(v, str) else "") for k, v in rec.items() if k is not None}
            fg, bg = rec.get("fg", "").strip(), rec.get("bg", "").strip()
            if not fg and not bg and not any(v.strip() for v in rec.values()):
                continue  # blank line
            if not fg or not bg:
                print(f"error: {path} line {line}: blank fg or bg; row skipped", file=sys.stderr)
                bad += 1
                continue
            use = (rec.get("use") or "text").strip().lower()
            if use not in THRESHOLDS:
                print(f"error: {path} line {line}: use must be one of {', '.join(THRESHOLDS)}, got {use!r}; row skipped", file=sys.stderr)
                bad += 1
                continue
            jobs.append((fg, bg, use, (rec.get("label") or "").strip()))
    return jobs, bad


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fg", nargs="?", help="foreground colour or token")
    p.add_argument("bg", nargs="?", help="background colour or token")
    p.add_argument("--use", default="text", choices=sorted(THRESHOLDS), help="threshold set (default: text)")
    p.add_argument("--pairs", help="CSV file with fg,bg,use[,label]")
    p.add_argument("--css", help="CSS file to resolve --token names from (for example theme.css)")
    p.add_argument("--scope", default="light", choices=["light", "dark"], help="token scope to resolve")
    p.add_argument("--suggest", action="store_true", help="propose an OKLCH foreground that passes AA")
    args = p.parse_args(argv)

    tokens: dict[str, str] = {}
    if args.css:
        try:
            with open(args.css, encoding="utf-8") as fh:
                tokens = load_tokens(fh.read(), args.scope)
        except (OSError, UnicodeDecodeError) as exc:
            print(f"error: cannot read --css {args.css}: {exc}", file=sys.stderr)
            return 2

    jobs: list[tuple[str, str, str, str]] = []
    bad_rows = 0
    if args.pairs:
        try:
            jobs, bad_rows = read_pairs(args.pairs)
        except (OSError, UnicodeDecodeError, csv.Error, ValueError) as exc:
            print(f"error: {args.pairs}: {exc}", file=sys.stderr)
            return 2
        if not jobs:
            print(f"no pairs to check in {args.pairs}")
            return 2 if bad_rows else 0
    elif args.fg and args.bg:
        jobs.append((args.fg, args.bg, args.use, ""))
    else:
        p.print_usage(sys.stderr)
        print("error: give FG and BG, or --pairs FILE", file=sys.stderr)
        return 2

    failures = 0
    errors = bad_rows
    print(f"{'pair':<44} {'use':<6} {'ratio':>7}  {'AA':<5} {'AAA':<5} suggestion")
    for fg, bg, use, label in jobs:
        try:
            row = check(fg, bg, use, label, tokens, args.suggest)
        except (ColourError, ValueError) as exc:
            # Report the bad pair and keep checking the rest.
            print(f"error: {label or fg + ' on ' + bg}: {exc}", file=sys.stderr)
            errors += 1
            continue
        failures += row["aa"] == "FAIL"
        print(f"{row['label'][:44]:<44} {row['use']:<6} {row['ratio']:>6.2f}:1  {row['aa']:<5} {row['aaa']:<5} {row['suggest']}")
        for w in row["warnings"]:
            print(f"  warning: {w}")
    checked = len(jobs) - (errors - bad_rows)
    summary = f"\n{checked} pair(s) checked, {failures} failing AA"
    if errors:
        summary += f", {errors} skipped with errors"
    print(summary + (f" ({args.scope} scope)" if args.css else ""))
    if errors:
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
