# Claim rules and file formats

Read this when normalising exports for the reconciler, assessing cancellations, or building the claim file. Rules come from the NDIS Pricing Arrangements and Price Limits and the NDIA's provider portal guidance, which change, usually from 1 July. The user confirms current values; nothing here replaces them.

## Reconciler input columns

`sessions.csv`: one row per billable line.

| Column | Meaning | Mapping tips |
| --- | --- | --- |
| `session_id` | Stable ID for the appointment | Calendar event ID or booking reference |
| `participant_ref` | Internal participant reference | Not the NDIS number |
| `date` | Service date, `YYYY-MM-DD` | |
| `start`, `end` | Actual times, `HH:MM` | Use the note's times, not the booked times |
| `status` | `completed`, `cancelled`, `no_show` or `scheduled` | Map "attended", "DNA", "late cancel" before running |
| `notice_at` | When the cancellation was received, `YYYY-MM-DD HH:MM` | From the call log, SMS or email time |
| `support_item` | Item number from the agreement | Exactly as in the current Support Catalogue |
| `unit` | `hour`, `each` or `km` | |
| `quantity` | Blank to derive hours from start and end | Set it for travel, report writing and cancellations |
| `unit_price` | Agreed price | |
| `note_ref` | Progress note ID; blank if none | |
| `worker` | Who delivered | Optional |

`claims.csv`: invoices and portal claims together, with `claim_ref`, `participant_ref`, `date`, `support_item`, `quantity`, `unit_price`, `session_id` (blank if unknown), `status` (`draft`, `submitted`, `paid`, `rejected`, `void`) and `claim_type` (`standard`, `cancellation`, `other`).

`budgets.csv` (optional): `participant_ref`, `support_item` (exact item, or a prefix ending in `_` to cover a group of items), `agreed_amount`, `period_start`, `period_end`, `funding_type` (`ndia`, `plan`, `self`).

The sample item codes in `assets/` (`TH_SESSION`, `TH_TRAVEL`, `TH_REPORT`) and prices are placeholders, not real support items or price limits.

## Minutes to decimal hours

| Minutes | Hours | Minutes | Hours |
| --- | --- | --- | --- |
| 5 | 0.08 | 35 | 0.58 |
| 10 | 0.17 | 40 | 0.67 |
| 15 | 0.25 | 45 | 0.75 |
| 20 | 0.33 | 50 | 0.83 |
| 25 | 0.42 | 55 | 0.92 |
| 30 | 0.50 | 60 | 1.00 |

Claim the time actually delivered. Do not round up to the next block unless the agreement and the Pricing Arrangements say so.

## Short-notice cancellations

The Pricing Arrangements define when a cancellation counts as short notice (measured in clear business days before the support, with different rules for longer or more expensive supports) and how much of the agreed price may be claimed. The reconciler's default of fewer than 2 clear business days is a setting to confirm, not a rule. Clear business days exclude the day notice was given, the day of the support, weekends and public holidays.

Before claiming one, confirm:

- [ ] The service agreement includes a cancellation clause the participant agreed to
- [ ] The notice given was shorter than the current threshold, or the participant did not attend or was not at the agreed place within a reasonable time
- [ ] The support item allows a cancellation claim under the current Pricing Arrangements
- [ ] Any condition the Pricing Arrangements set is met (for example, that the worker could not be given other billable work)
- [ ] The amount is no more than the share of the agreed price currently allowed
- [ ] The cancellation is recorded in the participant's file with the time notice was received
- [ ] The claim uses the cancellation claim type in the portal template, not a standard service line

A provider-initiated cancellation is never claimable.

## NDIA portal bulk upload

The NDIA provider portal accepts a bulk payment request file in a fixed CSV layout. Download the current template from the portal each time; column names and order have changed before and may change again. Fields commonly include the provider's registration number, the participant's NDIS number, service start and end dates, support item number, a claim reference, quantity or hours, unit price, GST code, claim type and, for cancellations, a reason. Map from `claim-candidates.csv` like this:

| Candidate column | Template field (check the current name) |
| --- | --- |
| `participant_ref` | Replace with the NDIS number from the provider's secure record at the last step |
| `date_from`, `date_to` | Service start and end dates, in the template's date format |
| `support_item` | Support item number |
| `session_id` | Claim reference (keep it unique per line so duplicates can be traced) |
| `quantity` | Quantity or hours, decimals as above |
| `unit_price` | Unit price, at or below the current price limit |
| `claim_type` | Standard service, or the cancellation claim type with a reason |

Before upload:

- [ ] Only rows for NDIA-managed budgets
- [ ] No row with a `hold_reason`
- [ ] Dates inside the plan and agreement period
- [ ] Each claim reference unique, and not already used in a previous upload
- [ ] Row count and total match the approved summary

After upload, download the results, match each line by claim reference, and fix and resubmit failed lines only.

## Plan manager invoices

Group candidates by participant. Include the details listed in the onboarding skill's funding reference: provider name and ABN, participant name and NDIS number, invoice number and date, service dates, support item number and name, quantity, unit price, line total and GST treatment. Send to the plan manager's invoice address on file, after approval.

This is a practical checklist, not legal or financial advice.
