# Pipeline review rules

## Default thresholds

These suit a sales cycle of roughly 30 to 90 days. The script matches stages by keyword in the stage name.

| Stage | Default probability | Stale after (days without activity) | Stuck after (days in stage) |
| --- | --- | --- | --- |
| Lead | 10% | 21 | 45 |
| Qualified | 20% | 14 | 30 |
| Proposal | 40% | 10 | 30 |
| Negotiation | 60% | 7 | 21 |
| Contract | 80% | 5 | 21 |
| Closed Won / Closed Lost | 100% / 0% | not checked | not checked |

Adjust to the business:

| Sales cycle | Change |
| --- | --- |
| Under 2 weeks (trades call-outs, small retail jobs) | Halve stale and stuck days. |
| 30 to 90 days (most B2B services) | Defaults. |
| Over 90 days (fit-outs, enterprise, government) | Double stale and stuck days. |
| Seasonal or tender-driven | Set stuck days per stage from the tender timeline; stale still applies. |

Custom stage names: map each to the nearest default, or set it in a config file:

```json
{"stages": {"Site visit booked": {"probability": 30, "stale_days": 7, "stuck_days": 21}}}
```

## Flags

| Flag | Rule | Why it matters |
| --- | --- | --- |
| PAST_CLOSE | Open, expected close date before the review date | The forecast is already wrong for this deal. |
| STALE | Days since last logged activity above the stage limit, or no activity at all | Deals that go quiet late in the cycle are usually lost. |
| NO_NEXT_STEP | Next-step field empty and no open task | Nobody owns moving it forward. |
| NEXT_STEP_OVERDUE | Next step due date passed | A promise to the customer may have been missed. |
| PUSHED | Close date moved two or more times | Repeated slippage predicts loss better than stage does. |
| STUCK | Days in current stage above the stage limit | The stage no longer describes reality. |
| PROB_MISMATCH | Deal probability 20 points or more away from the stage default | Either the stage or the probability is wrong. |
| MISSING_AMOUNT / MISSING_CLOSE / NO_OWNER | Field empty | The deal cannot be forecast or chased. |
| CLOSE_TOO_FAR | Close date more than 12 months out | Usually a placeholder date. |

A deal is treated as **gone cold** (excluded even from the best case) when its idle days are more than twice the stale limit, or it has no activity and has been pushed twice.

## Reading flags in context

Before reporting a flag, open the deal's timeline:

- Activity happened but was not logged (a call in someone's phone log, a meeting not recorded): note "activity not logged" and propose logging it. The flag stands until it is logged.
- The customer asked for a pause with a date: change the action to "re-contact on <date>" and propose moving the close date.
- A deal waiting on the customer (for example, board approval on a known date) is not stale if a dated follow-up task exists.
- Two deals for the same need: flag as a possible duplicate for `fulcrum-crm-data-cleanup`.

## Stage evidence

A stage should describe something the team can verify. Ask for the evidence when a flagged deal sits in a late stage.

| Stage | Evidence expected |
| --- | --- |
| Qualified | Need, timing and decision maker known; logged discovery call or meeting. |
| Proposal | Proposal or quote sent, with date. |
| Negotiation | Customer has responded to the proposal with questions or changes. |
| Contract | Contract or acceptance document issued, awaiting signature. |
| Closed Won | Signed acceptance, purchase order or payment. |

Mis-staged deals get the action "Move to <stage> (evidence: <missing item>)", proposed to the owner.

## Probability sanity

- Late stages with no activity for more than a week: the stated probability is optimistic; the likely forecast halves it.
- A Lead or Qualified deal above 50%: either it should move stage or the number is a hope.
- A won-rate history beats defaults: if the business has 6 months of closed deals, compute each stage's actual conversion and propose new stage probabilities to the owner.
