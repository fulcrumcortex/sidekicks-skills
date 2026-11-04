#!/usr/bin/env python3
"""Normalise lead fields before they go into a CRM.

Applies the rules in references/field-normalisation.md:
  - Australian phone numbers to E.164 (+61...) plus a display format
  - ABN and ACN checksum validation and spacing
  - title case for names and companies, without breaking McDonald, O'Brien,
    van der Berg or names the person already typed in mixed case
  - lower-case email, free-webmail and role-address detection
  - state abbreviation and postcode/state consistency
  - duplicate-check keys (email, phone, company domain)

Input: a JSON object, a JSON array of objects, or CSV with a header row
(--csv, implied for a .csv file name). CSV headers are matched loosely
("First Name" reads as first_name). Recognised keys: first_name, last_name, full_name, email, phone,
mobile, company, website, abn, acn, state, postcode. Other keys pass through.

Output: JSON on stdout, one result per lead with "warnings".

Standard library only. No network calls.

Examples:
  python3 normalise_lead.py lead.json
  python3 normalise_lead.py --csv leads.csv
  echo '{"phone": "0400 000 000", "state": "qld"}' | python3 normalise_lead.py
  python3 normalise_lead.py --phone "(02) 9000 0000"
  python3 normalise_lead.py --abn "12 345 678 901"
"""

import argparse
import csv
import io
import json
import re
import sys

FREE_WEBMAIL = {
    "gmail.com", "googlemail.com", "outlook.com", "outlook.com.au", "hotmail.com",
    "hotmail.com.au", "live.com", "live.com.au", "msn.com", "yahoo.com", "yahoo.com.au",
    "icloud.com", "me.com", "mac.com", "bigpond.com", "bigpond.net.au", "bigpond.com.au",
    "optusnet.com.au", "iinet.net.au", "internode.on.net", "tpg.com.au", "westnet.com.au",
    "aol.com", "protonmail.com", "proton.me", "fastmail.com", "zoho.com", "gmx.com",
}
ROLE_LOCALS = {
    "info", "admin", "accounts", "accounting", "sales", "hello", "enquiries", "enquiry",
    "office", "reception", "bookings", "support", "contact", "team", "mail", "noreply",
    "no-reply", "service", "orders", "billing", "hr", "jobs", "careers",
}
STATES = {
    "nsw": "NSW", "new south wales": "NSW", "vic": "VIC", "victoria": "VIC",
    "qld": "QLD", "queensland": "QLD", "sa": "SA", "south australia": "SA",
    "wa": "WA", "western australia": "WA", "tas": "TAS", "tasmania": "TAS",
    "nt": "NT", "northern territory": "NT", "act": "ACT",
    "australian capital territory": "ACT",
}
STATE_AREA_CODE = {"NSW": "2", "ACT": "2", "VIC": "3", "TAS": "3", "QLD": "7", "SA": "8", "WA": "8", "NT": "8"}
POSTCODE_RANGES = {
    "NSW": [(1000, 2599), (2619, 2899), (2921, 2999)],
    "ACT": [(200, 299), (2600, 2618), (2900, 2920)],
    "VIC": [(3000, 3999), (8000, 8999)],
    "QLD": [(4000, 4999), (9000, 9999)],
    "SA": [(5000, 5999)],
    "WA": [(6000, 6999)],
    "TAS": [(7000, 7999)],
    "NT": [(800, 999)],
}
PARTICLES = {"van", "von", "der", "den", "de", "da", "di", "del", "della", "la", "le", "du", "bin", "binti", "al"}
SMALL_WORDS = {"and", "of", "the", "for", "at", "in", "on", "to", "by"}
COMPANY_SUFFIXES = [
    (r"\bpty\.?\s*ltd\.?$|\bp/l$|\bproprietary limited$", "Pty Ltd"),
    (r"\bltd\.?$|\blimited$", "Ltd"),
    (r"\binc\.?$", "Inc"),
]


# ---------- phones ----------

def normalise_phone(raw, state=None):
    """Return dict with e164, display, type and warnings."""
    out = {"input": raw, "e164": None, "display": None, "type": None, "warnings": []}
    if not raw or not str(raw).strip():
        return out
    text = str(raw).strip()
    if re.search(r"(ext|x)\.?\s*\d+$", text, re.I):
        out["warnings"].append("extension found; store it in a note, not the phone field")
        text = re.sub(r"(ext|x)\.?\s*\d+$", "", text, flags=re.I)
    plus = text.startswith("+")
    digits = re.sub(r"\D", "", text)
    if plus and digits.startswith("610"):
        digits = "61" + digits[3:]  # +61 (0)4...
    if digits.startswith("0011"):  # Australian international access code
        digits, plus = digits[4:], True
    if digits.startswith("0061"):
        digits, plus = digits[2:], True
    if digits.startswith("61") and len(digits) == 11 and digits[2] in "23478":
        digits, plus = digits, True
    elif plus and not digits.startswith("61"):
        out["e164"] = "+" + digits
        out["display"] = "+" + digits
        out["type"] = "international"
        out["warnings"].append("non-Australian number; check country code and that calling it is intended")
        return out

    if plus and digits.startswith("61"):
        national = "0" + digits[2:]
    else:
        national = digits

    # Inbound and special numbers: no E.164 for 13/1300/1800 in practice
    if re.fullmatch(r"1[38]00\d{6}", national):
        out["type"] = "inbound (1300/1800)"
        out["display"] = f"{national[:4]} {national[4:7]} {national[7:]}"
        out["warnings"].append("1300/1800 number: keep national format; not reliably callable from overseas")
        return out
    if re.fullmatch(r"13\d{4}", national):
        out["type"] = "inbound (13)"
        out["display"] = f"{national[:2]} {national[2:4]} {national[4:]}"
        out["warnings"].append("13 number: keep national format")
        return out

    if re.fullmatch(r"4\d{8}", national):
        national = "0" + national
        out["warnings"].append("leading 0 was missing; assumed Australian mobile")
    elif re.fullmatch(r"[2378]\d{8}", national):
        national = "0" + national
        out["warnings"].append("leading 0 was missing (often dropped by spreadsheets); assumed Australian landline")
    if re.fullmatch(r"\d{8}", national):
        st = (state or "").upper()
        if st in STATE_AREA_CODE:
            national = "0" + STATE_AREA_CODE[st] + national
            out["warnings"].append(f"no area code; assumed 0{STATE_AREA_CODE[st]} from state {st}, confirm")
        else:
            out["display"] = national
            out["type"] = "unknown"
            out["warnings"].append("8-digit number with no area code and no state; ask for the area code")
            return out

    if re.fullmatch(r"0[45]\d{8}", national):
        out["type"] = "mobile"
        out["display"] = f"{national[:4]} {national[4:7]} {national[7:]}"
    elif re.fullmatch(r"0[2378]\d{8}", national):
        out["type"] = "landline"
        out["display"] = f"({national[:2]}) {national[2:6]} {national[6:]}"
    else:
        out["display"] = text
        out["type"] = "invalid"
        out["warnings"].append("not a valid Australian number; keep as typed and confirm with the person")
        return out
    out["e164"] = "+61" + national[1:]
    return out


# ---------- ABN / ACN ----------

ABN_WEIGHTS = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]


def check_abn(raw):
    digits = re.sub(r"\D", "", str(raw or ""))
    out = {"input": raw, "valid": False, "formatted": None, "warnings": []}
    if not digits:
        return out
    if len(digits) != 11:
        out["warnings"].append(f"ABN must have 11 digits (got {len(digits)}); if it has 9 it may be an ACN")
        return out
    nums = [int(d) for d in digits]
    nums[0] -= 1
    total = sum(n * w for n, w in zip(nums, ABN_WEIGHTS))
    out["formatted"] = f"{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"
    out["valid"] = total % 89 == 0
    if not out["valid"]:
        out["warnings"].append("ABN fails the checksum; likely a typo, ask the person or check the ABN Lookup")
    return out


def check_acn(raw):
    digits = re.sub(r"\D", "", str(raw or ""))
    out = {"input": raw, "valid": False, "formatted": None, "warnings": []}
    if not digits:
        return out
    if len(digits) != 9:
        out["warnings"].append(f"ACN must have 9 digits (got {len(digits)})")
        return out
    total = sum(int(d) * w for d, w in zip(digits[:8], range(8, 0, -1)))
    check = (10 - total % 10) % 10
    out["formatted"] = f"{digits[:3]} {digits[3:6]} {digits[6:]}"
    out["valid"] = check == int(digits[8])
    if not out["valid"]:
        out["warnings"].append("ACN fails the checksum")
    return out


# ---------- names ----------

def _is_mixed(text):
    letters = [c for c in text if c.isalpha()]
    return any(c.isupper() for c in letters) and any(c.islower() for c in letters)


def _cap_word(word):
    if not word:
        return word
    parts = re.split(r"([-'’])", word)
    rebuilt = []
    for part in parts:
        if part in ("-", "'", "’") or not part:
            rebuilt.append(part)
            continue
        low = part.lower()
        if low.startswith("mc") and len(low) > 2:
            rebuilt.append("Mc" + low[2].upper() + low[3:])
        else:
            rebuilt.append(low[0].upper() + low[1:])
    return "".join(rebuilt)


def title_name(raw, surname=False):
    """Title-case a person's name unless they typed it in mixed case."""
    if not raw:
        return raw, []
    text = re.sub(r"\s+", " ", str(raw).strip())
    if _is_mixed(text):
        return text, []
    words = text.split(" ")
    result = []
    for i, word in enumerate(words):
        if (i > 0 or surname) and word.lower() in PARTICLES and len(words) > 1:
            result.append(word.lower())
        else:
            result.append(_cap_word(word))
    warnings = []
    if any(w.lower() in PARTICLES for w in words) and len(words) > 1:
        warnings.append("name has a particle (van, de, da...): confirm the person's preferred capitalisation")
    if any(w.lower().startswith("mac") and len(w) > 4 for w in words):
        warnings.append("name starts with Mac: confirm the spelling (MacDonald or Macdonald)")
    return " ".join(result), warnings


def title_company(raw):
    if not raw:
        return raw, []
    text = re.sub(r"\s+", " ", str(raw).strip())
    suffix = ""
    for pattern, replacement in COMPANY_SUFFIXES:
        m = re.search(pattern, text, re.I)
        if m:
            suffix = replacement
            text = text[:m.start()].rstrip(" ,")
            break
    if _is_mixed(text):
        name = text
    else:
        words = text.split(" ")
        out = []
        for i, word in enumerate(words):
            if word.isupper() and 2 <= len(word) <= 4 and text != text.upper():
                out.append(word)
            elif i > 0 and word.lower() in SMALL_WORDS:
                out.append(word.lower())
            elif word == "&":
                out.append(word)
            else:
                out.append(_cap_word(word))
        name = " ".join(out)
    warnings = []
    if not _is_mixed(text):
        warnings.append("company was typed in one case; check acronyms and brand styling (for example ABC or eBay)")
    return (name + (" " + suffix if suffix else "")).strip(), warnings


def company_key(name):
    """Lower-case company name without legal suffix or punctuation, for matching."""
    if not name:
        return None
    text = str(name).lower()
    for pattern, _ in COMPANY_SUFFIXES:
        text = re.sub(pattern, "", text.strip(), flags=re.I)
    text = re.sub(r"[^a-z0-9& ]", "", text)
    return re.sub(r"\s+", " ", text).strip() or None


# ---------- email, state, website ----------

def normalise_email(raw):
    out = {"input": raw, "email": None, "domain": None, "free_webmail": False, "role_address": False, "warnings": []}
    if not raw:
        return out
    email = str(raw).strip().strip("<>").lower()
    email = re.sub(r"^mailto:", "", email)
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", email):
        out["warnings"].append("email address looks invalid; keep the original and confirm")
        return out
    local, domain = email.split("@", 1)
    out.update(email=email, domain=domain, free_webmail=domain in FREE_WEBMAIL,
               role_address=local.split("+")[0] in ROLE_LOCALS)
    if out["role_address"]:
        out["warnings"].append("shared role address: does not identify one person; do not merge on it alone")
    return out


def normalise_state(raw):
    if not raw:
        return None
    return STATES.get(str(raw).strip().lower().rstrip("."))


def check_postcode(postcode, state):
    if not postcode:
        return []
    pc = re.sub(r"\D", "", str(postcode))
    if len(pc) != 4:
        return ["postcode should have 4 digits (NT and ACT ones may start with 0)"]
    if state and state in POSTCODE_RANGES:
        n = int(pc)
        if not any(a <= n <= b for a, b in POSTCODE_RANGES[state]):
            return [f"postcode {pc} does not match state {state}; confirm the address"]
    return []


def website_domain(raw):
    if not raw:
        return None
    text = str(raw).strip().lower()
    text = re.sub(r"^[a-z]+://", "", text)
    text = text.split("/")[0]
    return re.sub(r"^www\.", "", text) or None


# ---------- lead ----------

def normalise_lead(lead):
    result = dict(lead)
    warnings = []
    state = normalise_state(lead.get("state"))
    if lead.get("state"):
        if state:
            result["state"] = state
        else:
            warnings.append(f"unrecognised state {lead.get('state')!r}")
    if lead.get("full_name") and not (lead.get("first_name") or lead.get("last_name")):
        parts = str(lead["full_name"]).strip().split()
        if len(parts) >= 2:
            lead = dict(lead, first_name=parts[0], last_name=" ".join(parts[1:]))
            warnings.append("split full_name into first and last name; check for multi-part first names")
    for key in ("first_name", "last_name"):
        if lead.get(key):
            result[key], w = title_name(lead[key], surname=(key == "last_name"))
            warnings += w
    if lead.get("company"):
        result["company"], w = title_company(lead["company"])
        warnings += w
    email = normalise_email(lead.get("email"))
    if lead.get("email"):
        result["email"] = email["email"] or lead.get("email")
        warnings += email["warnings"]
    for key in ("mobile", "phone"):
        if lead.get(key):
            ph = normalise_phone(lead[key], state)
            result[key] = ph["e164"] or ph["display"]
            result[key + "_display"] = ph["display"]
            result[key + "_type"] = ph["type"]
            warnings += [f"{key}: {w}" for w in ph["warnings"]]
    if lead.get("abn"):
        abn = check_abn(lead["abn"])
        result["abn"] = abn["formatted"] or lead["abn"]
        result["abn_valid"] = abn["valid"]
        warnings += abn["warnings"]
    if lead.get("acn"):
        acn = check_acn(lead["acn"])
        result["acn"] = acn["formatted"] or lead["acn"]
        result["acn_valid"] = acn["valid"]
        warnings += acn["warnings"]
    warnings += check_postcode(lead.get("postcode"), state)

    domain = website_domain(lead.get("website"))
    if not domain and email["domain"] and not email["free_webmail"]:
        domain = email["domain"]
    keys = {
        "email": email["email"],
        "phones": [result.get(k) for k in ("mobile", "phone") if result.get(k, "") and str(result.get(k)).startswith("+")],
        "company_domain": domain,
        "person_name": " ".join(filter(None, [result.get("first_name"), result.get("last_name")])).lower() or None,
        "company_name": company_key(result.get("company")),
    }
    result["dedupe_keys"] = keys
    result["warnings"] = warnings
    return result


RECOGNISED = ("first_name", "last_name", "full_name", "email", "phone", "mobile", "company", "website",
              "abn", "acn", "state", "postcode")


def clean_key(key):
    return re.sub(r"[\s-]+", "_", key.strip().lower())


def read_leads(path, as_csv):
    """Return a list of lead dicts, or exit with a message on unreadable input."""
    name = path or "stdin"
    try:
        handle = open(path, newline="", encoding="utf-8-sig") if path else sys.stdin
    except OSError as e:
        sys.exit(f"Cannot open {path}: {e.strerror}")
    try:
        text = handle.read()
    except UnicodeDecodeError:
        sys.exit(f"Cannot read {name}: not UTF-8 text")
    finally:
        if handle is not sys.stdin:
            handle.close()
    if not text.strip():
        sys.exit(f"No leads: {name} is empty")
    if as_csv:
        try:
            rows = list(csv.DictReader(io.StringIO(text)))
        except csv.Error as e:
            sys.exit(f"Cannot read {name} as CSV: {e}")
        if not rows:
            sys.exit(f"No leads: {name} has a header row but no data rows")
        leads = []
        for n, row in enumerate(rows, start=2):
            if None in row:
                print(f"row {n}: more cells than header columns; extra cells ignored", file=sys.stderr)
            leads.append({clean_key(k): v for k, v in row.items() if k is not None})
        return leads
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        hint = " (use --csv for CSV input)" if "," in text.splitlines()[0] and not text.lstrip().startswith(("{", "[")) else ""
        sys.exit(f"Cannot read {name} as JSON: {e.msg} at line {e.lineno}{hint}")
    items = data if isinstance(data, list) else [data]
    leads = []
    for n, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            print(f"lead {n}: not a JSON object; skipped", file=sys.stderr)
            continue
        leads.append({str(k): v for k, v in item.items()})
    if not leads:
        sys.exit(f"No leads: {name} contains no JSON objects")
    return leads


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", help="JSON or CSV file (default: stdin)")
    parser.add_argument("--csv", action="store_true", help="read CSV with a header row (implied by a .csv file name)")
    parser.add_argument("--phone", help="normalise one phone number and exit")
    parser.add_argument("--state", help="state for --phone when the area code is missing")
    parser.add_argument("--abn", help="check one ABN and exit")
    parser.add_argument("--acn", help="check one ACN and exit")
    args = parser.parse_args()

    if args.phone or args.abn or args.acn:
        out = {}
        if args.phone:
            out["phone"] = normalise_phone(args.phone, normalise_state(args.state))
        if args.abn:
            out["abn"] = check_abn(args.abn)
        if args.acn:
            out["acn"] = check_acn(args.acn)
        json.dump(out, sys.stdout, indent=2)
        print()
        return

    as_csv = args.csv or bool(args.file and args.file.lower().endswith(".csv"))
    leads = read_leads(args.file, as_csv)
    if not any(k in RECOGNISED for lead in leads for k in lead):
        sys.exit("No recognised lead fields. Expected at least one of: " + ", ".join(RECOGNISED)
                 + ". Found: " + ", ".join(sorted({k for lead in leads for k in lead})))
    results = []
    for lead in leads:
        cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in lead.items()}
        result = normalise_lead({k: v for k, v in cleaned.items() if v not in (None, "")})
        if not any(cleaned.get(k) not in (None, "") for k in RECOGNISED):
            result["warnings"].append("no recognised lead fields filled in; nothing to normalise")
        results.append(result)
    json.dump(results if len(results) != 1 else results[0], sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
