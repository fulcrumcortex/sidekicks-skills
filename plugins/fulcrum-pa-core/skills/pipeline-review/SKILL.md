---
name: pipeline-review
description: Runs a weekly sales pipeline review. It flags stale deals (no activity in N days for their stage), missing or overdue next steps, slipped and repeatedly pushed close dates, deals stuck in a stage and probabilities that do not match the stage, then forecasts best, likely and worst cases for the period and writes an action list per owner. Use when the user asks for a "pipeline review", "deal review", "forecast for the month", "which deals are stuck", "sales meeting prep", "what's going to close" or "clean up the pipeline". Includes a script that scores a deals CSV. Works with any CRM export or spreadsheet; uses Fulcrum CRM deals, pipelines, reports and activities when connected.
---

# Review the pipeline and forecast the period

Gives the owner or sales lead a clear view of which deals are real, which are drifting and what each person should do this week. The endpoint is a review document with a flag table, a three-number forecast and an action list per owner. Changes to deals are proposed, not made, unless the deal owner approves them.

## When to use

- Weekly, before a sales meeting or the Monday brief.
- Month or quarter end, to sanity-check a forecast.
- After a CRM import or a change of owner, to find gaps.
- Not for: merging duplicate deals or cleaning fields in bulk (use `fulcrum-crm-data-cleanup`); following up one customer (use `fulcrum-crm-follow-up`); quoting (use `quote-and-proposal`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Open deals with stage, amount, owner, expected close date | CRM deals board or list, or a spreadsheet | Required. Without amounts, review hygiene only and skip the forecast. |
| Last activity date per deal | CRM activity timeline | Use the last email or meeting with the contact; label it "derived". If nothing, treat the deal as stale. |
| Next step and its due date | Deal field, open task on the deal | Treat as no next step. |
| Stage history (date entered, close-date changes) | Deal history | Skip the STUCK and PUSHED checks and say so. |
| Won deals in the period | CRM, closed-won stage | Forecast without "won so far" and say so. |
| Stage probabilities and sales-cycle length | Pipeline settings, the owner | Use the defaults in [references/review-rules.md](references/review-rules.md). |
| Target for the period | The owner | Skip coverage. |

## Procedure

1. **Set scope.** Pipeline(s), owners, review date and forecast period (default: the current calendar month; quarter if the owner reviews quarterly). Confirm the filters, organisation and your visibility; you may not see every owner's deals.
2. **Get the data.** Export or read the deals into the CSV shape described in `scripts/pipeline_review.py --help` (see [assets/sample-deals.csv](assets/sample-deals.csv)). Include won deals in the period. Check a sample of three deals against the CRM before trusting the export.
3. **Tune the thresholds** to the business's sales cycle using [references/review-rules.md](references/review-rules.md). Write any overrides to a small JSON config rather than editing the script.
4. **Run the review.** `python3 scripts/pipeline_review.py deals.csv --as-of <date> --period <start>:<end> [--target <n>] [--config stages.json]`. Rows it cannot read (blank stage, bad date or amount) are listed under "Rows skipped"; fix them in the export and re-run before you trust the forecast.
5. **Apply judgement.** The script flags; you decide. Read every flagged deal's recent timeline. Clear false flags (for example, activity happened but was not logged; say so and propose logging it). Upgrade risks the script cannot see: a champion left, a competitor entered, budget frozen.
6. **Sanity-check stage against reality.** Each stage should mean something observable (proposal sent, verbal yes, contract issued). A deal at Contract with no contract sent is mis-staged. Use the stage evidence table in [references/review-rules.md](references/review-rules.md#stage-evidence).
7. **Forecast.** Report worst, likely and best with the method in [references/forecasting.md](references/forecasting.md). Name the three deals that swing the number most and any concentration risk. Never present the likely case as a commitment.
8. **Write actions per owner.** Up to seven per owner, highest weighted value first, each a verb plus a deal plus a date ("Call Orbit Freight by Tue to confirm the new close date"). Put unassigned deals under the manager.
9. **Approval gate: sharing and changes.** Before sending action lists to owners by email or chat, show each message, its recipients, channel and sending account, and wait for an explicit yes. Proposed CRM changes (close date, stage, probability, owner) are listed for the deal owner to approve; make them only after a yes, then verify each saved deal.
10. **Record the snapshot.** Keep the forecast numbers with the date so next week's review can show movement.

## Output

A review using [assets/review-template.md](assets/review-template.md): headline (forecast and the one thing that matters most), forecast table with movement since last week, flag counts, flagged-deal table, deals that swing the forecast, actions by owner, proposed CRM changes awaiting approval, and data gaps.

## Check before you finish

- [ ] Three sample deals were checked against the CRM; the export matched.
- [ ] Every flag was read in context; false flags are noted, not silently dropped.
- [ ] Forecast method and assumptions are stated; won figures come from closed-won records only.
- [ ] Every action has an owner, a deal and a date.
- [ ] No deal was moved, re-dated or reassigned without the owner's approval.

## Guardrails

- Do not "fix" the forecast by changing close dates or probabilities. Propose changes; the deal owner decides.
- Keep individual performance commentary out of shared messages; send each owner only their own list unless the manager asks otherwise.
- Customer names and amounts are confidential. Do not post the review in a channel wider than the sales team without approval.

## With Fulcrum

Fulcrum CRM deals sit in pipelines with stages and win percentages; a new pipeline starts with Lead (10%), Qualified (20%), Proposal (40%), Negotiation (60%), Contract (80%), Closed Won (100%) and Closed Lost (0%). The board can filter by owner, priority and close date (any, overdue or none), and each card turns amber after 3 days and red after 7 days in its stage. Stages named with "Won" and "Lost" never show as overdue. Every stage change is written to the contact's timeline ([Deals and pipelines](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)). Activities and the organisation-wide timeline show what was logged and when ([Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)). Deals cannot be exported yet, so build the CSV from the board or list view, or read deals through a connected tool. When a count looks wrong, check organisation, role, filters and date range before comparing ([Reports and workflows](https://fulcrumcortex.github.io/documentation/crm/reports-and-workflows/)).

## Learn more

- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
- [Reports and everyday CRM workflows](https://fulcrumcortex.github.io/documentation/crm/reports-and-workflows/)
- [Design a follow-up queue that gets done](https://fulcrumcortex.com/blog/crm-follow-up-queue)
