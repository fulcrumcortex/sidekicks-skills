#!/usr/bin/env python3
"""Price a bill of materials (BOM) against a supplier catalogue.

Reads CSV files, applies waste allowances by category, converts BOM units to
purchase units, adds labour from the business's own rates, compares the
purchase quantities with stock on hand, and prints a draft quote with GST plus
draft purchase-order lines for any shortfall.

It never invents a price, a waste figure or a labour rate. A line without a
price or rate is reported as missing and the totals are marked INCOMPLETE.

Standard library only. No network access.

Input columns (header row required; extra columns are ignored):

  BOM (--bom):        description, qty, unit
                      optional: line, code, category, type (item|PS|PC),
                                allowance (PS/PC amount ex GST), notes
  Catalogue (--catalogue):
                      code, description, unit_price_ex_gst
                      optional: supplier, purchase_unit,
                                coverage (BOM units per purchase unit, default 1),
                                pack_size (purchase units per pack, default 1),
                                price_valid_until (YYYY-MM-DD)
  Waste (--waste):    category, waste_pct
  Labour (--labour):  category, unit, hours_per_unit, rate_per_hour_ex_gst
  Stock (--stock):    code, on_hand   optional: allocated

Example:
  python3 bom_to_quote.py --bom bom.csv --catalogue catalogue.csv \\
      --waste waste.csv --labour labour.csv --stock stock.csv \\
      --material-markup 15 --valid-days 30 --date 2026-11-05
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Any, Optional

CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def fmt(value: Decimal) -> str:
    return f"{money(value):,.2f}"


def norm(text: str | None) -> str:
    return " ".join((text or "").lower().replace(",", " ").split())


def dec_opt(raw: str | None, field: str, where: str) -> Decimal | None:
    """Parse a number; blank gives None, anything else unparseable raises ValueError."""
    raw = (raw or "").strip().replace("$", "").replace(",", "")
    if raw == "":
        return None
    try:
        value = Decimal(raw)
    except InvalidOperation:
        raise ValueError(f"{where}: '{field}' is not a number: {raw!r}") from None
    if not value.is_finite():
        raise ValueError(f"{where}: '{field}' is not a number: {raw!r}")
    return value


def dec(raw: str | None, field: str, where: str) -> Decimal:
    """Parse a required number; blank or unparseable raises ValueError."""
    value = dec_opt(raw, field, where)
    if value is None:
        raise ValueError(f"{where}: '{field}' is blank")
    return value


def read_csv(path: str | None, required: list[str], label: str) -> list[tuple[int, dict[str, str]]]:
    """Return (line number, row) pairs with lower-cased keys; cells beyond the header are ignored."""
    if not path:
        return []
    try:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if not [h for h in (reader.fieldnames or []) if h and h.strip()]:
                raise SystemExit(f"{label} file {path} is empty: expected a header row with {', '.join(required)}")
            headers = {h.strip().lower() for h in (reader.fieldnames or []) if h}
            missing = [c for c in required if c not in headers]
            if missing:
                raise SystemExit(f"{label} file {path} is missing columns: {', '.join(missing)}")
            rows: list[tuple[int, dict[str, str]]] = []
            for row in reader:
                clean = {k.strip().lower(): (v or "").strip() for k, v in row.items() if isinstance(k, str)}
                if any(clean.values()):
                    rows.append((reader.line_num, clean))
            return rows
    except FileNotFoundError:
        raise SystemExit(f"{label} file not found: {path}") from None
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise SystemExit(f"{label} file {path} could not be read: {exc}") from None


@dataclass
class CatalogueItem:
    code: str
    description: str
    supplier: str
    purchase_unit: str
    coverage: Decimal
    pack_size: Decimal
    price: Decimal | None
    valid_until: str


def build_catalogue(rows: list[tuple[int, dict[str, str]]],
                    problems: list[str]) -> tuple[dict[str, CatalogueItem], dict[str, CatalogueItem]]:
    by_code: dict[str, CatalogueItem] = {}
    by_desc: dict[str, CatalogueItem] = {}
    for i, r in rows:
        where = f"catalogue row {i}"
        try:
            price = dec_opt(r.get("unit_price_ex_gst"), "unit_price_ex_gst", where)
            coverage = dec_opt(r.get("coverage"), "coverage", where)
            pack_size = dec_opt(r.get("pack_size"), "pack_size", where)
        except ValueError as exc:
            problems.append(f"{exc}. Catalogue row skipped.")
            continue
        coverage = Decimal(1) if coverage is None else coverage
        pack_size = Decimal(1) if pack_size is None else pack_size
        if coverage <= 0 or pack_size <= 0:
            problems.append(f"{where}: coverage and pack_size must be greater than zero. Catalogue row skipped.")
            continue
        item = CatalogueItem(
            code=r.get("code", ""),
            description=r.get("description", ""),
            supplier=r.get("supplier") or "Unspecified supplier",
            purchase_unit=r.get("purchase_unit") or "each",
            coverage=coverage,
            pack_size=pack_size,
            price=price,
            valid_until=r.get("price_valid_until", ""),
        )
        if item.code:
            by_code[item.code.lower()] = item
        if item.description:
            by_desc[norm(item.description)] = item
    return by_code, by_desc


def ceil_to(value: Decimal, step: Decimal) -> Decimal:
    """Round value up to a whole multiple of step (both Decimal)."""
    if value <= 0:
        return Decimal(0)
    return Decimal(math.ceil(value / step)) * step


def run(args: argparse.Namespace) -> dict[str, Any]:
    today: dt.date = args.date or dt.date.today()
    quote_expiry = today + dt.timedelta(days=args.valid_days)
    problems: list[str] = []

    bom = read_csv(args.bom, ["description", "qty", "unit"], "BOM")
    by_code, by_desc = build_catalogue(read_csv(args.catalogue, ["code", "description", "unit_price_ex_gst"], "Catalogue"),
                                       problems)
    waste: dict[str, Decimal | None] = {}
    for i, r in read_csv(args.waste, ["category", "waste_pct"], "Waste"):
        try:
            waste[norm(r["category"])] = dec_opt(r.get("waste_pct"), "waste_pct", f"waste row {i}")
        except ValueError as exc:
            problems.append(f"{exc}. Treated as no waste allowance for '{r['category']}'.")
            waste[norm(r["category"])] = None
    labour: dict[tuple[str, str], tuple[Optional[Decimal], Optional[Decimal]]] = {}
    for i, r in read_csv(args.labour, ["category", "unit", "hours_per_unit", "rate_per_hour_ex_gst"], "Labour"):
        where = f"labour row {i}"
        try:
            labour[(norm(r["category"]), norm(r["unit"]))] = (
                dec_opt(r["hours_per_unit"], "hours_per_unit", where),
                dec_opt(r["rate_per_hour_ex_gst"], "rate_per_hour_ex_gst", where),
            )
        except ValueError as exc:
            problems.append(f"{exc}. Treated as no labour rate for '{r['category']}' per '{r['unit']}'.")
            labour[(norm(r["category"]), norm(r["unit"]))] = (None, None)
    stock: dict[str, Decimal] = {}
    for i, r in read_csv(args.stock, ["code", "on_hand"], "Stock"):
        where = f"stock row {i}"
        try:
            on_hand = dec(r["on_hand"], "on_hand", where)
            allocated = dec_opt(r.get("allocated"), "allocated", where)
        except ValueError as exc:
            problems.append(f"{exc}. Item treated as not in the stock file.")
            continue
        stock[r["code"].lower()] = on_hand - (allocated or Decimal(0))

    mat_markup = Decimal(str(args.material_markup)) / 100
    lab_markup = Decimal(str(args.labour_markup)) / 100
    gst_rate = Decimal(str(args.gst)) / 100

    lines: list[dict[str, Any]] = []
    flags: list[str] = list(problems)
    po_lines: list[dict[str, str]] = []
    for problem in problems:
        print(f"warning: {problem}", file=sys.stderr)
    if not bom:
        flags.append("The BOM has no lines: nothing to price.")
    totals = {k: Decimal(0) for k in ("materials_cost", "materials_sell", "labour_cost", "labour_sell", "ps", "pc")}
    missing_count = 0

    for idx, (_, row) in enumerate(bom, start=1):
        ref = row.get("line") or str(idx)
        desc = row["description"]
        where = f"BOM line {ref}"
        kind = (row.get("type") or "item").upper()
        if kind in ("PS", "PC"):
            try:
                amount = dec_opt(row.get("allowance"), "allowance", where)
            except ValueError as exc:
                flags.append(f"{exc}. Treated as no amount.")
                amount = None
            if amount is None:
                flags.append(f"Line {ref} ({desc}): {kind} allowance has no amount. Ask the user; do not estimate it.")
                missing_count += 1
                amount_out = None
            else:
                totals["ps" if kind == "PS" else "pc"] += amount
                amount_out = money(amount)
            lines.append({"line": ref, "type": kind, "description": desc, "allowance_ex_gst": None if amount_out is None else str(amount_out)})
            continue

        try:
            qty = dec(row.get("qty"), "qty", where)
            if qty < 0:
                raise ValueError(f"{where}: 'qty' is negative: {qty}")
        except ValueError as exc:
            flags.append(f"{exc}. Line skipped.")
            missing_count += 1
            continue
        unit = row["unit"]
        category = row.get("category", "")
        code = row.get("code", "")
        item = by_code.get(code.lower()) if code else None
        if item is None:
            item = by_desc.get(norm(desc))
        out: dict[str, Any] = {"line": ref, "type": "ITEM", "description": desc, "category": category,
               "qty": str(qty), "unit": unit}

        # Waste
        wpct = waste.get(norm(category)) if category else None
        if wpct is None:
            flags.append(f"Line {ref} ({desc}): no waste allowance for category '{category or 'blank'}'. Priced at 0% waste; confirm with the user.")
            wpct = Decimal(0)
        qty_with_waste = qty * (1 + wpct / 100)
        out["waste_pct"] = str(wpct)
        out["qty_with_waste"] = str(qty_with_waste.quantize(Decimal("0.001")))

        # Materials
        if item is None:
            flags.append(f"Line {ref} ({desc}): not found in the catalogue (code '{code or 'blank'}'). Map it to a supplier item.")
            missing_count += 1
            out.update({"supplier": "", "purchase_qty": "", "unit_price_ex_gst": "MISSING", "material_sell_ex_gst": "MISSING"})
        else:
            purchase_qty = ceil_to(qty_with_waste / item.coverage, item.pack_size)
            out.update({"supplier": item.supplier, "supplier_code": item.code,
                        "purchase_qty": str(purchase_qty), "purchase_unit": item.purchase_unit})
            if item.price is None:
                flags.append(f"Line {ref} ({desc}): catalogue item {item.code} has no price. Get a supplier price; do not estimate.")
                missing_count += 1
                out.update({"unit_price_ex_gst": "MISSING", "material_sell_ex_gst": "MISSING"})
            else:
                cost = purchase_qty * item.price
                sell = cost * (1 + mat_markup)
                totals["materials_cost"] += cost
                totals["materials_sell"] += sell
                out.update({"unit_price_ex_gst": str(money(item.price)), "material_sell_ex_gst": str(money(sell))})
                if item.valid_until:
                    try:
                        valid_until = dt.date.fromisoformat(item.valid_until)
                        if valid_until < quote_expiry:
                            flags.append(f"Line {ref} ({desc}): supplier price valid until {valid_until}, before the quote expires on {quote_expiry}. Shorten validity or re-confirm the price.")
                    except ValueError:
                        flags.append(f"Line {ref} ({desc}): price_valid_until '{item.valid_until}' is not YYYY-MM-DD.")
            # Stock
            if args.stock:
                available = stock.get(item.code.lower())
                if available is None:
                    available = Decimal(0)
                    out["stock_note"] = "not in stock file"
                short = purchase_qty - max(available, Decimal(0))
                if short > 0:
                    order_qty = ceil_to(short, item.pack_size)
                    po_lines.append({"supplier": item.supplier, "code": item.code, "description": item.description,
                                     "order_qty": str(order_qty), "purchase_unit": item.purchase_unit,
                                     "unit_price_ex_gst": "MISSING" if item.price is None else str(money(item.price)),
                                     "line_ex_gst": "MISSING" if item.price is None else str(money(order_qty * item.price)),
                                     "for_bom_line": ref})
                out["available"] = str(available)

        # Labour
        lab = labour.get((norm(category), norm(unit))) if category else None
        if args.labour:
            hours_per_unit, rate = lab if lab is not None else (None, None)
            if hours_per_unit is None or rate is None:
                flags.append(f"Line {ref} ({desc}): no labour rate for category '{category or 'blank'}' per '{unit}'. Ask for the business's rate.")
                missing_count += 1
                out["labour_sell_ex_gst"] = "MISSING"
            else:
                hours = qty * hours_per_unit
                lcost = hours * rate
                lsell = lcost * (1 + lab_markup)
                totals["labour_cost"] += lcost
                totals["labour_sell"] += lsell
                out.update({"labour_hours": str(hours.quantize(Decimal("0.01"))), "labour_sell_ex_gst": str(money(lsell))})
        lines.append(out)

    if not args.labour:
        flags.append("No labour file supplied: labour is excluded from these totals. Add the business's own rates or price labour separately.")
    subtotal = totals["materials_sell"] + totals["labour_sell"] + totals["ps"] + totals["pc"]
    gst = money(subtotal * gst_rate)
    result = {
        "status": "INCOMPLETE" if missing_count else "COMPLETE",
        "missing_count": missing_count,
        "quote_date": str(today),
        "valid_until": str(quote_expiry),
        "lines": lines,
        "flags": flags,
        "purchase_order_drafts": po_lines,
        "totals_ex_gst": {
            "materials": str(money(totals["materials_sell"])),
            "labour": str(money(totals["labour_sell"])),
            "provisional_sums": str(money(totals["ps"])),
            "prime_cost_items": str(money(totals["pc"])),
            "subtotal": str(money(subtotal)),
        },
        "gst": str(gst),
        "total_inc_gst": str(money(subtotal) + gst),
        "internal_cost_ex_gst": {
            "materials": str(money(totals["materials_cost"])),
            "labour": str(money(totals["labour_cost"])),
        },
    }
    return result


def to_markdown(r: dict[str, Any]) -> str:
    out: list[str] = []
    out.append(f"# Draft quote calculation ({r['status']})\n")
    out.append(f"Quote date {r['quote_date']} | valid until {r['valid_until']}")
    if r["missing_count"]:
        out.append(f"\n**INCOMPLETE: {r['missing_count']} missing price, rate or allowance item(s). Totals below exclude them. Do not send this quote.**")
    out.append("\n## Lines\n")
    out.append("| Line | Type | Description | Qty | Unit | Waste % | Purchase qty | Supplier | Unit price ex GST | Materials ex GST | Labour hrs | Labour ex GST |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for l in r["lines"]:
        if l["type"] in ("PS", "PC"):
            amount = l["allowance_ex_gst"] or "MISSING"
            out.append(f"| {l['line']} | {l['type']} | {l['description']} | | | | | | | {amount} | | |")
            continue
        purchase = f"{l.get('purchase_qty', '')} {l.get('purchase_unit', '')}".strip()
        out.append(f"| {l['line']} | item | {l['description']} | {l['qty']} | {l['unit']} | {l.get('waste_pct', '')} | {purchase} | "
                   f"{l.get('supplier', '')} | {l.get('unit_price_ex_gst', '')} | {l.get('material_sell_ex_gst', '')} | "
                   f"{l.get('labour_hours', '')} | {l.get('labour_sell_ex_gst', '')} |")
    t = r["totals_ex_gst"]
    out.append("\n## Totals\n")
    out.append("| | Amount |\n| --- | --- |")
    out.append(f"| Materials (ex GST) | {fmt(Decimal(t['materials']))} |")
    out.append(f"| Labour (ex GST) | {fmt(Decimal(t['labour']))} |")
    out.append(f"| Provisional sums (ex GST) | {fmt(Decimal(t['provisional_sums']))} |")
    out.append(f"| Prime cost items (ex GST) | {fmt(Decimal(t['prime_cost_items']))} |")
    out.append(f"| **Subtotal (ex GST)** | **{fmt(Decimal(t['subtotal']))}** |")
    out.append(f"| GST | {fmt(Decimal(r['gst']))} |")
    out.append(f"| **Total (inc GST)** | **{fmt(Decimal(r['total_inc_gst']))}** |")
    c = r["internal_cost_ex_gst"]
    out.append(f"\nInternal only, not for the customer: materials cost {fmt(Decimal(c['materials']))}, labour cost {fmt(Decimal(c['labour']))}.")
    if r["flags"]:
        out.append("\n## Flags to resolve\n")
        out.extend(f"- {f}" for f in r["flags"])
    if r["purchase_order_drafts"]:
        out.append("\n## Draft purchase-order lines (shortfall against stock)\n")
        suppliers = sorted({p["supplier"] for p in r["purchase_order_drafts"]})
        for s in suppliers:
            out.append(f"### {s}\n")
            out.append("| Code | Description | Order qty | Unit | Unit price ex GST | Line ex GST | For BOM line |")
            out.append("| --- | --- | --- | --- | --- | --- | --- |")
            for p in r["purchase_order_drafts"]:
                if p["supplier"] == s:
                    out.append(f"| {p['code']} | {p['description']} | {p['order_qty']} | {p['purchase_unit']} | "
                               f"{p['unit_price_ex_gst']} | {p['line_ex_gst']} | {p['for_bom_line']} |")
            out.append("")
    return "\n".join(out)


def iso_date(raw: str) -> dt.date:
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a YYYY-MM-DD date: {raw!r}") from None


def percent(raw: str) -> float:
    try:
        value = float(raw)
    except ValueError:
        value = math.nan
    if not math.isfinite(value):
        raise argparse.ArgumentTypeError(f"not a percentage: {raw!r}")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n")[0],
        epilog="Column details are in the module docstring; run with --columns to print them.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bom", help="BOM or takeoff CSV")
    parser.add_argument("--catalogue", help="Supplier catalogue CSV with ex-GST prices")
    parser.add_argument("--waste", help="Waste allowance CSV (category, waste_pct)")
    parser.add_argument("--labour", help="Labour rate CSV (category, unit, hours_per_unit, rate_per_hour_ex_gst)")
    parser.add_argument("--stock", help="Stock on hand CSV (code, on_hand, allocated)")
    parser.add_argument("--material-markup", type=percent, default=0.0, help="Markup %% on materials (default 0)")
    parser.add_argument("--labour-markup", type=percent, default=0.0, help="Markup %% on labour cost (default 0)")
    parser.add_argument("--gst", type=percent, default=10.0, help="GST rate %% (default 10)")
    parser.add_argument("--valid-days", type=int, default=30, help="Quote validity in days (default 30)")
    parser.add_argument("--date", type=iso_date, help="Quote date YYYY-MM-DD (default today)")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="Output format (default md)")
    parser.add_argument("--columns", action="store_true", help="Print the expected CSV columns and exit")
    args = parser.parse_args(argv)
    if args.columns:
        print(__doc__)
        return 0
    if not args.bom or not args.catalogue:
        parser.error("--bom and --catalogue are required")
    try:
        result = run(args)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2) if args.format == "json" else to_markdown(result))
    return 1 if result["status"] == "INCOMPLETE" else 0


if __name__ == "__main__":
    sys.exit(main())
