#!/usr/bin/env python3
"""Lint marketing copy for readability, banned phrases and claims needing evidence.

Standard library only, no network. Reads plain text or Markdown from files or
stdin and reports:
  - Flesch Reading Ease and Flesch-Kincaid grade (approximate, English)
  - average sentence length and sentences over the length limit
  - phrases from the ban list (references/slop-phrases.md by default; the
    first column of every Markdown table is read as a phrase)
  - claims that need substantiation (the "Claims that need evidence" table)
  - exclamation marks, passive-voice hints, and the ratio of "you" to "we"

The scores are heuristics for comparing drafts, not a verdict. A short
headline can score oddly; judge it by the clarity test instead.

Usage:
  copy_lint.py page-copy.md
  cat hero.txt | copy_lint.py -
  copy_lint.py copy.md --max-sentence 20 --banlist path/to/list.md --json

Exit status: 0 if no banned phrases or unsupported claims were found,
1 if any were found, 2 on input errors.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BANLIST = os.path.join(HERE, "..", "references", "slop-phrases.md")
CLAIMS_HEADING = "claims that need evidence"


def load_banlist(path: str) -> tuple[list[str], list[str]]:
    banned: list[str] = []
    claims: list[str] = []
    section = ""
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                section = line.strip("# \n").lower()
                continue
            m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
            if not m:
                continue
            cell = m.group(1).strip().lower()
            if cell in ("phrase",) or set(cell) <= set("-: "):
                continue
            (claims if section.startswith(CLAIMS_HEADING) else banned).append(cell)
    return banned, claims


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)
    text = re.sub(r"[*_]{1,3}", "", text)
    return text


def sentences(text: str) -> list[str]:
    # Treat line breaks between headings or list items as sentence ends.
    chunks = re.split(r"(?<=[.!?])\s+|\n\s*\n|\n(?=\S)", text)
    return [c.strip() for c in chunks if re.search(r"[A-Za-z]", c)]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def syllables(word: str) -> int:
    w = word.lower().strip("'’-")
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    groups = re.findall(r"[aeiouy]{1,2}", w)
    return max(1, len(groups))


def find_phrases(text: str, phrases: list[str]) -> list[tuple[str, int]]:
    low = text.lower()
    hits = []
    for p in phrases:
        pat = r"(?<![a-z0-9])" + re.escape(p) + r"(?![a-z0-9])"
        n = len(re.findall(pat, low))
        if n:
            hits.append((p, n))
    return sorted(hits, key=lambda x: -x[1])


def analyse(raw: str, banned: list[str], claims: list[str], max_sentence: int) -> dict:
    text = strip_markdown(raw)
    sents = sentences(text)
    ws = words(text)
    n_w, n_s = max(1, len(ws)), max(1, len(sents))
    syl = sum(syllables(w) for w in ws)
    # No words means no meaningful readability score; report None, not 205.8.
    fre: float | None = round(206.835 - 1.015 * (n_w / n_s) - 84.6 * (syl / n_w), 1) if ws else None
    fkgl: float | None = round(0.39 * (n_w / n_s) + 11.8 * (syl / n_w) - 15.59, 1) if ws else None
    long = [s for s in sents if len(words(s)) > max_sentence]
    passive = re.findall(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b", text, flags=re.I)
    lw = [w.lower() for w in ws]
    you = sum(lw.count(x) for x in ("you", "your", "you're", "yours"))
    we = sum(lw.count(x) for x in ("we", "our", "we're", "us", "ours"))
    return {
        "words": len(ws),
        "sentences": len(sents),
        "avg_sentence_words": round(n_w / n_s, 1) if ws else 0.0,
        "flesch_reading_ease": fre,
        "fk_grade": fkgl,
        "long_sentences": long,
        "banned": find_phrases(text, banned),
        "claims": find_phrases(text, claims),
        "exclamations": text.count("!"),
        "passive_hints": passive[:10],
        "you_we": (you, we),
    }


def print_report(name: str, r: dict, max_sentence: int) -> None:
    print(f"== {name}")
    if not r["words"]:
        print("no words to check (empty input)")
        print()
        return
    print(f"words {r['words']}, sentences {r['sentences']}, average {r['avg_sentence_words']} words per sentence")
    print(f"Flesch reading ease {r['flesch_reading_ease']} (60-70 plain English; higher is easier)")
    print(f"Flesch-Kincaid grade {r['fk_grade']} (consumer copy: aim for 8 or lower; specialist B2B: 11 or lower)")
    you, we = r["you_we"]
    print(f"'you' words {you}, 'we' words {we}" + ("  -> copy talks about the business more than the reader" if we > you else ""))
    if r["exclamations"]:
        print(f"exclamation marks: {r['exclamations']} (usually remove)")
    if r["long_sentences"]:
        print(f"sentences over {max_sentence} words: {len(r['long_sentences'])}")
        for s in r["long_sentences"][:5]:
            print(f"  - {s[:140]}")
    if r["passive_hints"]:
        print("possible passive voice: " + "; ".join(r["passive_hints"]))
    print("banned phrases:" + (" none" if not r["banned"] else ""))
    for p, n in r["banned"]:
        print(f"  - {p} x{n}")
    print("claims needing evidence:" + (" none" if not r["claims"] else ""))
    for p, n in r["claims"]:
        print(f"  - {p} x{n}")
    print()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="text or Markdown files, or - for stdin")
    ap.add_argument("--banlist", default=DEFAULT_BANLIST, help="Markdown ban list (default: references/slop-phrases.md)")
    ap.add_argument("--max-sentence", type=int, default=25, help="flag sentences longer than this many words (default 25)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    args = ap.parse_args(argv)
    try:
        banned, claims = load_banlist(args.banlist)
    except OSError as exc:
        print(f"error: cannot read ban list: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"error: ban list {args.banlist} is not UTF-8 text: {exc.reason}", file=sys.stderr)
        return 2
    if not banned and not claims:
        print(f"error: ban list {args.banlist} has no phrases (expected Markdown tables whose first column is 'Phrase')", file=sys.stderr)
        return 2
    if args.max_sentence < 1:
        print("error: --max-sentence must be at least 1", file=sys.stderr)
        return 2
    out = {}
    for f in args.files:
        try:
            if f == "-":
                raw = sys.stdin.read()
            else:
                with open(f, encoding="utf-8") as fh:
                    raw = fh.read()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        except UnicodeDecodeError as exc:
            print(f"error: {f} is not UTF-8 text: {exc.reason}", file=sys.stderr)
            return 2
        out[f] = analyse(raw, banned, claims, args.max_sentence)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        for name, r in out.items():
            print_report(name, r, args.max_sentence)
    return 1 if any(r["banned"] or r["claims"] for r in out.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
