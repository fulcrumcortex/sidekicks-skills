---
name: ndis-billing-check
description: Reconciles delivered NDIS sessions from the calendar, bookings and progress notes against invoices and NDIA portal claims, then prepares a claim file or draft invoices for review. Finds completed work that was never billed, missing line items such as provider travel, duplicate claims, sessions without notes, claims outside the service agreement period or beyond the agreed budget, quantity and price mismatches, rejected claims and short-notice cancellations to assess against the current Pricing Arrangements. Use for "what haven't I billed", "reconcile my NDIS claims", "month-end billing", "bulk claim file", "bulk payment request", "check invoices against sessions" or "why was this claim rejected". Includes a two-CSV reconciler script. Works with any calendar, notes and accounting exports; uses Fulcrum Calendar and Fulcrum CRM invoices when connected. Nothing is submitted or sent without approval.
---

# Reconcile NDIS sessions against claims and invoices

Matches what was delivered against what was billed for a period, explains every gap, and prepares the next claim file or invoices for a provider to approve. Built for sole practitioners and small teams who claim through the NDIA provider portal, invoice plan managers, or both. The endpoint is an exception report plus a reviewed claim file; submission happens only after explicit approval.

## When to use

- Weekly or month-end billing run.
- Before a bulk upload to the NDIA provider portal.
- A plan manager or participant queries an invoice, or a claim was rejected.
- A plan is ending and every delivered session must be billed before the end date.
- Not for: writing the missing notes (use `progress-notes`), setting up a new participant's agreement (use `ndis-client-onboarding`), or chasing overdue plan-manager invoices (use `fulcrum-crm-follow-up`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Delivered sessions for the period, with status and actual times | Calendar or booking export, roster, timesheets | Cannot reconcile; ask for it |
| Progress note reference per session | Client records system | Treat as no note; the session is held |
| Invoices and claims for the same period plus one month either side | Accounting system, CRM invoices, portal payment request history | Ask once; without claims every session shows as unbilled |
| Service agreement lines: items, agreed price, budget, period, funding type | Service agreements or `ndis-client-onboarding` output | Skip budget checks and say so |
| Current price limits and cancellation rules | NDIS Pricing Arrangements and Price Limits, checked by the user | Use the script default only as a placeholder and say it needs verifying |
| The portal's current bulk upload template (NDIA-managed only) | Downloaded fresh from the portal by the user | Prepare the neutral claim candidates file; do not guess columns |

Use internal participant references in working files. Add NDIS numbers only at the last step, in the provider's own system, and never paste participant data into a public tool.

## Procedure

1. **Set the period and pull data one month wider** on both sides, so late claims and early invoices still match.
2. **Normalise to the script's columns.** See [claim rules and file formats](references/claim-rules.md) for the column list and a mapping from common exports. One row per billable line: a session with therapy plus provider travel is two rows sharing a `session_id`. Convert minutes to decimal hours (45 minutes = 0.75).
3. **Run the reconciler:**
   ```bash
   python3 scripts/reconcile.py --sessions sessions.csv --claims claims.csv \
     --budgets budgets.csv --as-of 2026-11-30 --out-claims claim-candidates.csv
   ```
   Add `--holidays holidays.txt` with the public holidays for the participant's state, and set `--short-notice-days` to the value the user has confirmed. Sample inputs are in [assets/](assets/).
4. **Triage every finding** with the table below. Work high severity first. Never resolve a finding by editing the source data to make it match.

   | Finding | Action |
   | --- | --- |
   | `NO_NOTE` | Hold the claim. Ask the practitioner to write the note from their own record. The agent never writes a note to justify a claim. |
   | `UNBILLED` | Becomes a claim candidate once the note exists and the agreement covers it. |
   | `MISSING_LINE_ITEM` | Usually provider travel, non-face-to-face time or report writing. Check the agreement allows it and the note records it, then add it. |
   | `DUPLICATE_CLAIM` | Keep the earliest valid claim. Cancel the duplicate in the portal or issue a credit note to the plan manager. If both were paid, arrange repayment. |
   | `QUANTITY_MISMATCH` | Under-billed: claim the difference as a separate line. Over-billed: correct before payment, or cancel and re-claim if paid. |
   | `PRICE_MISMATCH` | Compare with the agreement and the current price limit for the location. Never claim above the price limit for NDIA-managed or plan-managed budgets. |
   | `CLAIM_WITHOUT_SESSION` or `ITEM_NOT_DELIVERED` | Find the evidence or withdraw the claim. Do not keep a claim the records do not support. |
   | `SHORT_NOTICE_CANCELLATION` | Claimable only if the agreement allows it and the current Pricing Arrangements conditions are met. Use [the cancellation checklist](references/claim-rules.md#short-notice-cancellations). |
   | `CANCELLATION_CLAIMED_WITH_NOTICE` | Enough notice was given, so the cancellation is usually not claimable. Withdraw unless the user has a documented reason. |
   | `OVER_BUDGET` or `NEAR_BUDGET` | Stop new claims on that line. Tell the user to talk with the participant (and plan manager) about the remaining funds. Never split or relabel items to fit another budget. |
   | `OUTSIDE_AGREEMENT_PERIOD` | Check whether a new plan or agreement covers the date. Claims against an ended plan are usually refused. |
   | `REJECTED_CLAIM` | Read the rejection reason, fix the cause (provider link, item, dates, price, funds), then resubmit only that line. |
   | `STATUS_NOT_UPDATED` or `CANCELLATION_NOTICE_MISSING` | Ask the practitioner what happened and update the source record first. |

5. **Prepare what goes out, by funding route.** From `claim-candidates.csv`, drop rows with a `hold_reason` and anything the user has not cleared.
   - NDIA-managed: map rows to the portal's current bulk upload template (see [claim rules](references/claim-rules.md)). Item numbers and prices exactly as in the current Support Catalogue.
   - Plan-managed: one draft invoice per participant per plan manager, with the details the plan manager requires.
   - Self-managed: one draft invoice per participant to the person on the agreement.
6. **Check totals.** Sum by participant and funding route; the totals must match the candidates file. Spot-check three lines against the notes.
7. **Approval gate.** Show the exception summary, the totals per participant and route, the exact file or invoices, the destination (portal account, plan manager email, participant or nominee email) and the sending account. Wait for an explicit yes for this batch. A prepared file is not approval.
8. **Submit and verify.** After approval, upload or send once. Download the portal's results file and reconcile it line by line. If some lines fail, fix and resubmit only those lines; never re-upload the whole file. If a send or upload result is unclear, check the portal history or sent items before retrying.
9. **Record the outcome.** Mark sessions as billed with the claim or invoice reference, and keep the results file with the period's records.

## Output

1. Exception report: summary counts, then a table of findings by severity with participant reference, line, detail, value and the action agreed.
2. Value at stake: unbilled total, held total and over-claim total, stated separately.
3. The claim file or draft invoices for approval, with totals by participant and funding route.
4. A follow-up list: notes to write, agreements to renew, budget conversations to have, claims to withdraw.

## Check before you finish

- [ ] Every finding has an action or an owner; none silently dropped.
- [ ] No claim line lacks a note, an agreement covering the date, or a verified item number and price.
- [ ] No claim exceeds the agreement, the remaining budget or the current price limit.
- [ ] Short-notice cancellations claimed only where the agreement and current rules allow.
- [ ] Prepared, approved, submitted and paid are reported as separate states.

## Guardrails

- Not financial, legal or tax advice. The provider is responsible for every claim made under their registration or ABN.
- A claim is a statement that the support was delivered as described. Never claim for an undelivered support, round up time, or use a different item to reach a higher price.
- Keep participant details out of email bodies and public tools; send claim files only through the portal or the provider's secure method.
- Compliance checklist: claims match delivered supports and notes; prices within current price limits for NDIA-managed and plan-managed budgets; cancellations claimed only under current rules; records kept as the NDIS Practice Standards and Code of Conduct expect. This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum Calendar**: read booking-page bookings as the list of planned sessions. A `confirmed` booking is an appointment, not proof it was delivered, so confirm attendance from the note; `cancelled` bookings go to the cancellation checks. See [manage bookings](https://fulcrumcortex.github.io/documentation/calendar/manage-bookings/).
- **Fulcrum CRM invoices**: prepare plan-managed and self-managed invoices as drafts under Sales → Invoices, filter the list by draft, open, paid, void and uncollectible states to build the claims file, and treat Finalize & Send as the outward action behind the approval gate. A saved invoice is not proof it was received, and an open invoice is not proof of payment. See [invoices and products](https://fulcrumcortex.github.io/documentation/crm/invoices-and-products/).
- **Fulcrum CRM activities**: progress notes saved as Note activities give the `note_ref` evidence for each session.
- Fulcrum CRM also has a Workforce module for rostering, timesheets and payroll workflows. Availability varies by account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Invoices and the product catalogue in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/invoices-and-products/)
- [Manage bookings in Fulcrum Calendar](https://fulcrumcortex.github.io/documentation/calendar/manage-bookings/)
