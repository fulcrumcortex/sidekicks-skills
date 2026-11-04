---
name: takeoff-to-quote
description: Turns a drawing takeoff or bill of materials into a priced draft quote. Normalises materials to the supplier catalogue, applies waste allowances by material, converts takeoff units to purchase units, adds labour from the business's own rates, checks stock on hand, drafts purchase orders for shortfalls, and separates provisional sums, prime cost items and exclusions, with validity and GST. Never invents a price and flags every missing one. Use when a builder, tradie or estimator asks to "price this takeoff", "turn the BOM into a quote", "how much stock do we need to order", "draft the POs for this job" or "quote from these drawings". Includes a CSV calculator. Works with spreadsheets, any supplier price list or pasted data; uses Fulcrum CRM when connected.
---

# Price a takeoff into a draft quote and purchase orders

Converts a measured takeoff or bill of materials into a customer quote the estimator can stand behind, plus draft purchase orders for whatever is not in stock. The endpoint is a reviewed draft quote and draft POs; nothing goes to a customer or supplier until the user approves it.

## When to use

- A takeoff from drawings, a CAD export or a BOM spreadsheet needs pricing.
- An estimator wants waste, units, labour and stock handled consistently.
- A job is won and needs material orders against what is already on hand.
- Not for: producing the drawings or the takeoff itself (`fulcrum-cad-design-brief` covers briefs for CAD work), confirming and dispatching the job once booked (`job-confirmation`), or invoicing a finished job.

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Takeoff or BOM: description, quantity, unit, category; drawing references | CAD export, estimator's sheet, pasted list | Ask for it. Do not measure from a picture of a drawing and present it as a takeoff. |
| Supplier catalogue or price list with ex-GST prices, purchase units, pack sizes and price expiry | Supplier price file, last quotes | Price what you can; list every other line as MISSING |
| Waste allowances by category | The business's own figures | Use the starting points in [references/waste-and-units.md](references/waste-and-units.md) and label them as defaults |
| Labour: hours per unit and hourly rate by category | The business's own rates | Leave labour MISSING and ask; never use an industry average as their rate |
| Stock on hand and stock already allocated to other jobs | Stock sheet, inventory system | Treat everything as needing purchase and say so |
| Markup, quote validity, payment terms, licence number | User | Markup 0% and validity 30 days, both stated as assumptions |

## Procedure

1. **Read the scope first.** List the drawings by number and revision. Note anything the takeoff does not cover that the drawings show (for example wet-area waterproofing, flashing, fixings). Those become questions or exclusions, not silent additions.
2. **Normalise each line to the catalogue.** Match by supplier code first, then by exact description. For near matches (a different thickness, grade or length) do not substitute; list the candidate and ask. Record unit mismatches (m2 versus sheets, lm versus lengths) and the coverage figure used.
3. **Classify each line.** Item (measured and priced), provisional sum (work whose extent is unknown), prime cost item (an item the customer has not selected), or exclusion. Use the table in [references/quote-structure.md](references/quote-structure.md).
4. **Run the calculator.** Put the data in the CSV shapes in `assets/`: `bom-template.csv`, `catalogue-template.csv`, `labour-rates-template.csv`, `stock-on-hand-template.csv`, and `waste-allowances.csv` (starting points to replace with the business's figures). Then run:

   ```bash
   python3 scripts/bom_to_quote.py --bom bom.csv --catalogue catalogue.csv \
     --waste waste.csv --labour labour.csv --stock stock.csv \
     --material-markup <pct> --valid-days <days> --date <YYYY-MM-DD>
   ```

   It applies waste, rounds up to purchase units and pack sizes, prices materials and labour, compares with stock, drafts PO lines by supplier and totals with GST. It exits with status 1 and prints INCOMPLETE when any price, rate or allowance is missing. Rows with unreadable numbers (or a zero coverage or pack size) are skipped and listed under the flags. Use `--format json` to feed another tool and `--columns` for the column list. Without the script, follow the same rounding rules by hand and show your working.
5. **Resolve flags, never paper over them.** For each MISSING line: get a supplier price, ask the user for the rate, or move it to a PS with the user's amount. Do not average similar items, use an old job's price without saying so, or fill a gap with an online price.
6. **Sense-check before drafting.** Compare totals with the business's own past jobs where available: materials-to-labour ratio, cost per m2 of floor area, and any line over 20% of the total. Flag anything unusual with a reason; do not adjust it yourself.
7. **Check price validity.** If any supplier price expires before the quote does, shorten the quote validity or mark that material as subject to change. Note volatile materials.
8. **Draft the quote** using [assets/quote-template.md](assets/quote-template.md): scope in plain words, priced sections, PS and PC items listed separately with what each covers, specific exclusions and assumptions, subtotal ex GST, GST and total inc GST, validity and the business's own payment terms. Keep the internal cost build-up and margin out of the customer copy.
9. **Draft purchase orders** from the shortfall list, one per supplier: supplier codes, quantities in purchase units, the job reference, the delivery address and required-by date, and the agreed prices. Do not order for a job that has not been accepted unless the user says the material is for stock.
10. **Approval gate.** Before the quote goes to the customer or any PO goes to a supplier, show: the exact document, the recipient and their address or email, the sending account, and the status line from the calculator. A quote marked INCOMPLETE cannot be sent. Wait for an explicit yes for each send.
11. **Record and verify.** Save the quote and POs where the business keeps them, with the revision number. After a send, confirm it in sent items before marking the quote "sent"; after a timeout, check before resending.

## Output

- The calculator output (or an equivalent table): lines, waste, purchase quantities, prices, labour, totals, flags.
- A customer quote draft from `assets/quote-template.md`.
- Draft POs per supplier.
- A short estimator's note: assumptions used, defaults applied, flags still open, and the sense-check result.

## Check before you finish

- [ ] Every line is priced, a PS or PC with the user's amount, an exclusion, or listed as MISSING. No silent gaps.
- [ ] Default waste figures and assumed markup or validity are labelled as such.
- [ ] GST appears once, on the subtotal; the customer sees ex GST, GST and inc GST.
- [ ] Customer copy contains no cost prices, margin or supplier names unless the business wants them shown.
- [ ] Report drafted, sent, pending and failed separately for the quote and each PO.

## Guardrails

- Never invent a price, rate, coverage figure or allowance. Missing data stays visibly missing.
- Never substitute a different product to fill a catalogue gap without the user's say-so.
- Do not present the quote as a contract. Residential work above state thresholds needs a compliant written contract; see the state checklist in [references/quote-structure.md](references/quote-structure.md).
- Keep supplier pricing confidential if the supplier's terms require it.

## With Fulcrum

- **Fulcrum CRM** keeps the customer, the deal for the job and its stage, and logs activity on the contact timeline. Its product catalogue (Settings → Product Catalog) holds the offerings used to build invoices, and invoices stay as drafts until someone selects Finalize & Send.
- Construction and Inventory & Fleet industry modules may be available in Fulcrum CRM depending on the account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.
- **Fulcrum Drive** can hold the drawings, takeoff and quote revisions, with sharing roles and expiring external links.

## Learn more

- [Invoices and the product catalogue in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/invoices-and-products/)
- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
