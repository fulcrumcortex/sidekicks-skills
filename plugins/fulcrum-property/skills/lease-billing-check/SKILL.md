---
name: lease-billing-check
description: "Compares a signed commercial or residential lease against what the tenant is actually being billed: base rent, review and escalation dates (fixed percentage, CPI or market), outgoings, GST, bond or security, incentive and rent-free periods, and options. Produces a discrepancy register with clause references, dollar impact and a confidence rating, plus a correction draft for approval. Use when someone asks to 'check the lease against the rent roll', 'audit tenant billing', 'was the rent review applied', 'is the CPI increase right', 'reconcile outgoings', or 'why is this tenant charged GST'. Works from a lease PDF or text and a ledger, invoice or rent-roll export. Not legal advice."
---

# Check a lease against what is being billed

Finds the gaps between what a signed lease says the tenant should pay and what the ledger, rent roll or invoices actually charge. The endpoint is a discrepancy register a property manager can act on and, after approval, a correction notice or ledger adjustment request. Missed rent reviews and mis-applied incentives are the most common findings, and they compound every month they go unnoticed.

## When to use

- Rent roll audits, new management takeovers, lease renewals, and any tenant query about a charge.
- After a rent review date has passed, to confirm the increase was applied correctly.
- Not for: drafting or interpreting a lease for negotiation (refer to a solicitor); general contract review (use `fulcrum-document-review`); chasing a tenant who is in arrears (use `tenancy-issue-triage`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The signed lease, all schedules, and every variation, extension, option exercise or deed of assignment | Property file, document store | Stop and ask. A lease without its variations gives wrong answers. Record which documents you saw. |
| What is billed: tenant ledger, rent roll export or invoices for the period under review | Trust accounting or property management software export | Ask for at least the last 13 months and the periods around each review date. |
| CPI index numbers for each CPI review (the exact series the lease names) | The user, from the official published series | Ask for them. Do not look up or assume CPI figures; mark the review "unverified" until supplied. |
| Outgoings budget and last reconciliation, with the tenant's proportion | Property manager, owner's accountant | Check rent and GST only, and list outgoings as "not checked". |
| Bond or security records: amount held, lodgement receipt, bank guarantee | Bond authority receipt, guarantee copy | List as "not checked". |
| State the property is in, and whether a retail lease applies | Lease, user | Ask; several rules below depend on it. |

## Procedure

1. **Extract the lease terms** using [references/lease-terms-checklist.md](references/lease-terms-checklist.md). Read it before extracting. Record each term with its clause number and page, and quote the operative words. Where clauses conflict (a variation overrides the original), follow the latest signed document and note the override.
2. **Build the expected schedule.** Fill a terms file shaped like [assets/lease-terms-example.json](assets/lease-terms-example.json) and run `python3 scripts/rent_schedule.py terms.json --billed billed.csv --only-mismatches`. The script applies fixed, CPI (with floor, cap and ratchet) and market reviews, incentive percentages and pro-rating by days, and compares with billed amounts. If the lease uses a method the script does not model (for example rent calculated per square metre on a remeasured area, turnover rent, or a different pro-rating rule), calculate those periods by hand, show the working, and say so.
3. **Check each area** against the rules below and note every mismatch, including those in the tenant's favour.
4. **Rate confidence** for each finding:
   - High: the clause is unambiguous, the billed figure is clear, and the difference exceeds the tolerance.
   - Medium: depends on an interpretation (for example which CPI quarter applies) or on a document you did not see.
   - Low: possible issue worth asking about; information incomplete.
5. **Quantify impact**: per-period difference, number of periods affected, cumulative total, and GST on it where applicable. Note limitation or "no back-charge" clauses the lease contains, without deciding their effect.
6. **Write the discrepancy register and correction draft** using [assets/discrepancy-register.md](assets/discrepancy-register.md). Corrections are proposals; the property manager and owner decide whether to back-charge, refund or waive.
7. **Approval gate.** Before anything goes to a tenant or owner, or any ledger change is requested: show the exact notice or request, the recipient, the sending mailbox and the figures. Wait for an explicit yes. Never adjust a trust ledger yourself; produce the adjustment request for the person authorised to make it. After sending, confirm the item is in sent items; after a timeout, check before resending.

## Area rules

| Area | Check | Common mismatch |
| --- | --- | --- |
| Base rent | Starting rent, basis (annual, monthly, per square metre), payment frequency, due day, commencement versus rent start date | Rent started at lease commencement although the lease gives a later rent commencement date |
| Reviews | Every review date in the term and option terms; type; formula; floor, cap, ratchet; notice requirements | Review never applied; applied to the wrong base (compounding missed); wrong CPI quarters |
| Residential increases | Frequency limits and notice periods set by the state | Increase applied without valid notice or within the restricted period. Check the state's rules. |
| Outgoings | Which outgoings are recoverable, tenant proportion, budget and reconciliation timing | Items charged that the lease does not list; proportion wrong after a remeasure; reconciliation never done. Some states' retail lease laws restrict recovery of land tax and certain costs: flag, do not decide. |
| GST | Commercial rent: GST added when the lease says rent is GST-exclusive and the landlord is registered. Residential rent is input-taxed. | GST charged on residential rent; GST charged twice on a GST-inclusive figure; GST missing on commercial outgoings |
| Bond and security | Amount, form, lodgement, top-up on review | Residential bond above the state limit or not lodged; bank guarantee not increased when the lease requires it |
| Incentives | Rent-free or abated periods, fit-out contributions, how they unwind | Abatement continued past its end date; rent-free applied to outgoings when the lease says rent only |
| Options | Exercise window, conditions, rent on exercise | Option term billed at old rent without the review on exercise; option exercised late or not documented |

## Output

1. The discrepancy register (asset template): one row per finding with clause, expected, billed, difference, periods, cumulative impact, confidence, recommended action.
2. A short summary: total under-billed, total over-billed, findings by confidence, documents not seen, areas not checked.
3. Correction drafts for approved items only.

## Check before you finish

- [ ] Every finding cites a clause and page from a document you actually read.
- [ ] Over-billing findings are reported as prominently as under-billing.
- [ ] CPI figures came from the user, and the series and quarters are stated.
- [ ] Areas not checked are listed, not silently skipped.
- [ ] Draft, approved, sent and pending items are reported separately.

## Guardrails

- This is a practical billing check, not legal advice. Disputes about interpretation, retail lease legislation, or back-charging go to the owner's solicitor.
- Do not contact a tenant directly unless the property manager approves the exact message.
- Lease and ledger data is personal and commercial information: share only the findings needed with each recipient.

## With Fulcrum

- Log the check as a note on the tenant contact's timeline, and create tasks with an owner and due date for each approved correction, as in [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Fulcrum CRM has Real Estate and Property Management industry modules; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill works from the lease and a ledger export alone.

## Learn more

- [AI for real estate agencies in Australia](https://fulcrumcortex.com/blog/ai-for-real-estate-agencies-australia)
- [Fulcrum CRM documentation](https://fulcrumcortex.github.io/documentation/crm/)
