#!/usr/bin/env python3
"""Validate the Sidekick skills repository. Python standard library only.

Checks:
  * every SKILL.md has front matter with a valid `name` (lowercase-hyphenated,
    at most 64 characters, matching its folder) and a `description` of at most
    1024 characters
  * every plugin listed in .claude-plugin/marketplace.json exists, has a
    parseable .claude-plugin/plugin.json whose name matches, and every plugin
    folder on disk is listed
  * every JSON file in the repository parses
  * relative links in Markdown files point to files that exist
  * no file contains the retired internal product name or stray hook front matter
  * every http(s) link in a Markdown file returns HTTP 200 without a redirect
    (skipped with --offline); only the social hosts in BOT_BLOCKING_HOSTS,
    which refuse automated requests, are exempt
  * smoke tests: every helper script under plugins/**/scripts/*.py has cases in
    tests/smoke/*.json (help, a realistic sample, and empty and missing-field
    input unless the script reads no input), and every case runs without a
    traceback, exits with an expected code and prints the expected text
    (skipped with --no-smoke)

Usage:
  python3 scripts/validate.py [--offline] [--no-smoke] [--only PATH ...]

Smoke case files (tests/smoke/<skill>.json):
  {"scripts": {"plugins/<p>/skills/<s>/scripts/x.py": {
      "no_input": false,
      "cases": [{"kind": "help|sample|empty|missing-field|edge",
                 "args": ["..."], "stdin": "optional/path",
                 "expect_exit": [0], "expect_stdout": ["text"],
                 "expect_stderr": ["text"]}]}}}
  Paths are relative to the repository root; "{tmp}" becomes a scratch folder.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"https?://[^\s)<>\"'`\]]+")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
# The banned product word is assembled so that `grep -ri` over the repo finds nothing.
BANNED = [re.compile("quo" + "rum", re.I), re.compile(r"generated_by:\s*skills-for-architects")]
TEXT_SUFFIXES = {".md", ".json", ".py", ".csv", ".ts", ".tsx", ".css", ".yaml", ".yml", ".txt"}
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
# Social profile hosts that refuse automated requests (403, 405, 999 or a 302 to a
# login page) even though the public profile opens normally in a browser. Links to
# these exact hosts are exempt from the 200 rule; every other host must return 200
# without a redirect. Add a host here only after confirming the page in a browser.
BOT_BLOCKING_HOSTS = {"medium.com", "www.f6s.com", "www.linkedin.com", "x.com"}
# Hosts used only as example values inside code samples, never as links.
EXAMPLE_HOSTS = ("example.com", "example.org", "example.net", "localhost", "127.0.0.1")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.counts: dict[str, int] = {}

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def count(self, key: str, n: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + n


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


def iter_files(roots: list[Path]):
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*")
        for p in paths:
            if p.is_file() and not any(part in SKIP_DIRS for part in p.parts):
                yield p


def parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    key = None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            fields[key] = value
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    for k, v in fields.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            fields[k] = v[1:-1]
    return fields


def check_skills(rep: Report, roots: list[Path]) -> None:
    seen: dict[str, str] = {}
    for skill_md in sorted(p for p in iter_files(roots) if p.name == "SKILL.md"):
        rep.count("skills")
        folder = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_front_matter(text)
        if fm is None:
            rep.error(f"{rel(skill_md)}: missing YAML front matter")
            continue
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not NAME_RE.match(name) or len(name) > 64:
            rep.error(f"{rel(skill_md)}: invalid name {name!r}")
        if name != folder:
            rep.error(f"{rel(skill_md)}: name {name!r} does not match folder {folder!r}")
        if not desc:
            rep.error(f"{rel(skill_md)}: missing description")
        elif len(desc) > 1024:
            rep.error(f"{rel(skill_md)}: description is {len(desc)} characters (max 1024)")
        if name in seen:
            rep.error(f"{rel(skill_md)}: duplicate skill name, also in {seen[name]}")
        seen[name] = rel(skill_md)
        lines = text.count("\n") + 1
        if lines > 500:
            rep.error(f"{rel(skill_md)}: {lines} lines (keep SKILL.md under 500)")


def check_manifests(rep: Report) -> None:
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        marketplace = json.loads(mp_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        rep.error(f"{rel(mp_path)}: {exc}")
        return
    listed = set()
    for entry in marketplace.get("plugins", []):
        name, source = entry.get("name", ""), entry.get("source", "")
        listed.add(name)
        if not NAME_RE.match(name):
            rep.error(f"marketplace.json: invalid plugin name {name!r}")
        src = (ROOT / source).resolve()
        if ROOT not in src.parents or not src.is_dir():
            rep.error(f"marketplace.json: source for {name!r} is not a folder in the repo: {source}")
            continue
        pj = src / ".claude-plugin" / "plugin.json"
        try:
            plugin = json.loads(pj.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            rep.error(f"{rel(pj)}: {exc}")
            continue
        if plugin.get("name") != name:
            rep.error(f"{rel(pj)}: name {plugin.get('name')!r} does not match marketplace entry {name!r}")
        if not any((src / "skills").glob("*/SKILL.md")):
            rep.error(f"{rel(src)}: plugin has no skills/*/SKILL.md")
        rep.count("plugins")
    for folder in sorted((ROOT / "plugins").iterdir()):
        if folder.is_dir() and folder.name not in listed:
            rep.error(f"plugins/{folder.name}: not listed in marketplace.json")


def check_files(rep: Report, roots: list[Path]) -> set[str]:
    urls: set[str] = set()
    for path in iter_files(roots):
        if path.suffix not in TEXT_SUFFIXES and path.name != "LICENSE":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            rep.error(f"{rel(path)}: not valid UTF-8")
            continue
        if path.resolve() == Path(__file__).resolve():
            continue  # this file names the banned patterns
        for pattern in BANNED:
            if pattern.search(text):
                rep.error(f"{rel(path)}: contains banned text matching {pattern.pattern!r}")
        is_fixture = "tests/fixtures/" in rel(path)  # fixtures may be deliberately malformed
        if path.suffix == ".json" and not is_fixture:
            try:
                json.loads(text)
                rep.count("json files")
            except json.JSONDecodeError as exc:
                rep.error(f"{rel(path)}: invalid JSON: {exc}")
        if path.suffix == ".md":
            rep.count("markdown files")
            for target in MD_LINK_RE.findall(text):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target_path = (path.parent / target.split("#", 1)[0]).resolve()
                if not target_path.exists():
                    rep.error(f"{rel(path)}: broken relative link {target}")
            for url in URL_RE.findall(text):
                url = url.rstrip(".,;:")
                if any(h in url for h in EXAMPLE_HOSTS) or "{" in url or "<" in url:
                    continue
                if url.endswith(".git"):
                    continue  # git clone URLs are not pages
                urls.add(url)
    return urls


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # noqa: D401 - urllib hook
        return None


def fetch_status(url: str) -> int:
    opener = urllib.request.build_opener(NoRedirect)
    headers = {"User-Agent": "Mozilla/5.0 (sidekicks-skills link check)"}
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers=headers)
        try:
            with opener.open(req, timeout=25) as resp:
                return resp.status
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 429, 501):
                continue
            return exc.code
        except (urllib.error.URLError, TimeoutError, OSError):
            if method == "HEAD":
                continue
            return 0
    return 0


def check_links(rep: Report, urls: set[str]) -> None:
    exempt = {u for u in urls if urllib.parse.urlsplit(u).hostname in BOT_BLOCKING_HOSTS}
    rep.count("bot-blocking profile links exempted", len(exempt))
    urls = urls - exempt
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for url, status in zip(sorted(urls), pool.map(fetch_status, sorted(urls))):
            rep.count("links checked")
            if status != 200:
                rep.error(f"link returned {status or 'no response'} (needs 200, no redirect): {url}")


REQUIRED_KINDS = {"help", "sample"}
INPUT_KINDS = {"empty", "missing-field"}


def run_smoke(rep: Report) -> None:
    scripts = {rel(p) for p in (ROOT / "plugins").rglob("scripts/*.py")}
    covered: dict[str, dict] = {}
    for case_file in sorted((ROOT / "tests" / "smoke").glob("*.json")):
        try:
            data = json.loads(case_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rep.error(f"{rel(case_file)}: invalid JSON: {exc}")
            continue
        for script, spec in data.get("scripts", {}).items():
            if script in covered:
                rep.error(f"{rel(case_file)}: {script} already has cases in another file")
            covered[script] = spec
    for script in sorted(scripts - set(covered)):
        rep.error(f"{script}: no smoke cases in tests/smoke/")
    for script in sorted(set(covered) - scripts):
        rep.error(f"tests/smoke: cases for a script that does not exist: {script}")
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for script in sorted(scripts & set(covered)):
        spec = covered[script]
        cases = spec.get("cases", [])
        kinds = {c.get("kind") for c in cases}
        needed = REQUIRED_KINDS | (set() if spec.get("no_input") else INPUT_KINDS)
        if needed - kinds:
            rep.error(f"{script}: smoke cases missing kind(s): {', '.join(sorted(needed - kinds))}")
        for i, case in enumerate(cases):
            label = f"{script} [{case.get('kind', '?')} #{i}]"
            with tempfile.TemporaryDirectory() as tmp:
                args = [a.replace("{tmp}", tmp) for a in case.get("args", [])]
                stdin_path = case.get("stdin")
                try:
                    stdin_bytes = (ROOT / stdin_path).read_bytes() if stdin_path else b""
                    proc = subprocess.run([sys.executable, "-I", script, *args], cwd=ROOT, env=env,
                                          input=stdin_bytes, capture_output=True, timeout=60)
                except (OSError, subprocess.TimeoutExpired) as exc:
                    rep.error(f"{label}: could not run: {exc}")
                    continue
            rep.count("smoke cases")
            out = proc.stdout.decode("utf-8", "replace")
            err = proc.stderr.decode("utf-8", "replace")
            if "Traceback (most recent call last)" in err:
                rep.error(f"{label}: crashed: {err.strip().splitlines()[-1]}")
                continue
            expected = case.get("expect_exit", [0])
            if proc.returncode not in expected:
                tail = (err.strip() or out.strip()).splitlines()[-1:] or [""]
                rep.error(f"{label}: exit {proc.returncode}, expected {expected}: {tail[0][:160]}")
            for text in case.get("expect_stdout", []):
                if text not in out:
                    rep.error(f"{label}: stdout lacks {text!r}")
            for text in case.get("expect_stderr", []):
                if text not in err:
                    rep.error(f"{label}: stderr lacks {text!r}")
        rep.count("scripts smoke-tested")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true", help="skip the HTTP link check")
    ap.add_argument("--no-smoke", action="store_true", help="skip the helper-script smoke tests")
    ap.add_argument("--only", nargs="+", type=Path, help="limit file checks to these paths")
    args = ap.parse_args()

    roots = [p.resolve() for p in args.only] if args.only else [ROOT]
    rep = Report()
    check_skills(rep, roots)
    if not args.only:
        check_manifests(rep)
    urls = check_files(rep, roots)
    if not args.offline:
        check_links(rep, urls)
    if not args.no_smoke and not args.only:
        run_smoke(rep)

    summary = ", ".join(f"{v} {k}" for k, v in sorted(rep.counts.items()))
    if rep.errors:
        print(f"FAILED with {len(rep.errors)} problem(s):")
        for e in rep.errors:
            print(f"  - {e}")
        print(f"Checked: {summary}")
        return 1
    print(f"OK. Checked: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
