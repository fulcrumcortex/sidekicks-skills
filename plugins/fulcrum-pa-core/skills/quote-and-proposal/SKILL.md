---
name: quote-and-proposal
description: Turns an enquiry, site visit notes or a scoping conversation into a ready-to-send quote or proposal with scope, inclusions, exclusions, assumptions, good/better/best options priced only from the business's own price list, GST shown correctly, validity period, terms, a clear next step and a follow-up schedule. Use when the user asks to "write a quote", "price this job", "put a proposal together", "send them a quote", "turn these notes into a quote" or "follow up the quote". Nothing is sent without approval. Works with any document tool, price list or CRM; uses the Fulcrum CRM product catalogue, Fulcrum Docs and Drive sharing when connected.
---

# Turn an enquiry into a quote or proposal

Produces a quote or proposal the customer can say yes to: a defined scope, prices taken from the business's own price list, GST handled correctly, explicit assumptions and exclusions, and one next step. The endpoint is an approved, sent document, logged on the deal, with a dated follow-up schedule.

## When to use

- A customer has asked for a price and the scope is known well enough to price.
- A larger or competitive opportunity needs a proposal (quote plus approach, timeline and reasons to choose the business).
- A sent quote needs its follow-up sequence or a revision.
- Not for: chasing payment on an issued invoice (`invoice-chasing`); reviewing a contract or someone else's document (`fulcrum-document-review`); qualifying a new enquiry before it is ready to price (`lead-capture`); reviewing the whole pipeline (`pipeline-review`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Scope source | Enquiry email, form, call notes, site visit notes, meeting transcript | Ask for it. Do not quote from a one-line request. |
| The business's own price list or rate card, with its date | Product catalogue, spreadsheet, previous approved quote template | Leave `[PRICE NEEDED]` against each line and ask. Never use market rates or guesses. |
| Whether list prices include or exclude GST, and GST registration | Price list, the user | Ask. Until answered, show prices with "GST status to confirm". |
| Customer type (consumer or business) and legal name | CRM record, enquiry | Ask; it changes how prices are displayed. |
| Business details: trading and legal name, ABN, contact | Business settings, letterhead | Ask once and reuse. |
| Standard terms, deposit and payment terms, validity period | The user's terms, previous quotes | Use 30 days validity and flag the terms section for the user to complete. |

## Procedure

1. **Extract the scope.** List the customer's problem, the outcome they want, deliverables with quantities, location, timing, constraints and the decision-maker. List every unknown separately. If an unknown would change the price by more than about 10%, ask before quoting or price it as a stated assumption with a variation rule. If more than three such unknowns remain, recommend a paid site visit, a scoping session or an estimate with a range rather than a fixed quote.
2. **Choose the document.** A **quote** is a fixed price for a defined scope. An **estimate** is an approximate price and must say so, with a range. A **proposal** adds the problem, approach, timeline and why this business, and suits work with several stakeholders, a competitive process, or a value the user sets as the threshold. Default to a quote.
3. **Price from the price list only.** Map every scope line to a price-list item and quantity. Check the list's date and that it is the current one. Unmatched lines get `[PRICE NEEDED]`. Apply only discounts the user has approved. Never reuse another customer's quoted price.
4. **Design the options.** Offer good/better/best when the budget is unclear or there is a natural upgrade; offer one price when the scope is fixed, the customer asked for one price, or a cheaper option would be unsafe or non-compliant. Rules are in [references/pricing-and-gst.md](references/pricing-and-gst.md): same core scope in every option, each step adds a visible benefit, the middle option is the one the business would recommend, and no more than three.
5. **Calculate.** Put the lines in a CSV and run `python3 scripts/quote_totals.py lines.csv --prices ex|inc [--deposit 20] [--not-registered]`. GST is 10%: ex-GST price times 0.1, or inc-GST price divided by 11. Show prices to consumers with the GST-inclusive total most prominent. Do not hand-calculate totals.
6. **Write inclusions, exclusions and assumptions.** Use the checklists in [references/scope-and-terms.md](references/scope-and-terms.md). Every exclusion that a customer could reasonably assume is included must be written down (for example rubbish removal, making good, permits, after-hours work).
7. **Set validity and terms.** 30 days by default; 14 days when material or supplier prices are volatile. State the deposit, payment terms, how variations are priced and approved, and what happens at acceptance. Do not write terms that exclude consumer guarantees. Flag one-sided clauses for the user, as standard-form contracts with consumers and small businesses are covered by unfair contract terms laws.
8. **Draft the document** from [assets/quote-template.md](assets/quote-template.md). One clear next step ("reply 'accepted' and pay the deposit", "sign and return", "book the start date"). Then check: customer name and address, every price traced to the price list, totals from the script, dates, ABN, and no other customer's details left from an earlier quote.
9. **Approval gate.** Show the final document, the recipient and any cc, the sending account, how it is delivered (attachment, or a shared link with its permission and expiry), and the follow-up schedule. Wait for an explicit yes. Any later change to price or scope needs a fresh yes.
10. **Send and record.** Send through the approved account and confirm it appears in sent items. After a timeout, check sent items before resending. Record the quote on the deal with amount (use one basis, normally ex GST, consistently), stage and expected close date, and create the follow-up tasks.
11. **Follow up on a schedule.** Day 2: confirm it arrived (larger quotes: a call). Day 5 to 7: offer to answer questions or walk through options. Three business days before expiry: remind of the validity date. At expiry: a short close-out asking whether to re-quote, then mark the deal lost or revised. Before each follow-up, check whether the customer has replied, accepted or declined, and present the message for approval when it is due.

## Output

- The quote or proposal, using the template sections in order.
- A one-paragraph cover message for the email.
- A pricing trace: each line, price-list item and date, quantity, and any approved discount.
- An open-questions list (anything priced as an assumption or `[PRICE NEEDED]`).
- After sending: sent status, deal record updated, follow-up dates.

## Check before you finish

- [ ] Every price traces to the business's own price list; no `[PRICE NEEDED]` remains in a sent document.
- [ ] Totals and GST came from the script and the document states whether prices include GST.
- [ ] Validity date, deposit, payment terms and the next step are present.
- [ ] Sent, drafted and pending follow-ups are reported separately.

## Guardrails

- Never invent prices, lead times, warranties, certifications or availability.
- If the business is not registered for GST, do not charge or show GST.
- Do not promise outcomes the business cannot control. Label estimates as estimates.
- Residential building work, and sales that follow an uninvited approach to a consumer (door-knocking or cold calling), carry extra state and Australian Consumer Law requirements such as written contract, deposit limits and cooling-off periods. Flag them to the user. This is a practical checklist, not legal advice.

## With Fulcrum

The Fulcrum CRM **Product Catalog** (Settings → Product Catalog) holds the offerings used to build invoices; treat it as the price list and inspect the selected price on each line, since a catalogue change does not alter an invoice already finalised. Track the opportunity as a **deal** with an amount, a **Proposal** stage and an expected close date; moving the card does not send anything to the customer. Create follow-up **tasks** with due dates.

Write longer proposals in **Fulcrum Docs** (start from a Business template, wait for "Saved in Drive", check print preview). **Share** adds existing Fulcrum accounts as Editor, Commenter or Viewer; for a customer without a Fulcrum account, use a Drive **external link** with an expiry and the download setting you want, if you own the file and your workspace allows external sharing. On acceptance, prepare the deposit invoice as a CRM draft; **Finalize & Send** is an outward action that needs its own approval.

## Learn more

- [Invoices and the product catalogue](https://fulcrumcortex.github.io/documentation/crm/invoices-and-products/)
- [Create and collaborate in Fulcrum Docs](https://fulcrumcortex.github.io/documentation/docs/)
- [Files, folders and sharing in Fulcrum Drive](https://fulcrumcortex.github.io/documentation/drive/)
