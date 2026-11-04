# Fee basis, billing cadence and the weekly WIP check

## Contents

- Choosing the fee basis
- What each basis must state in the letter
- Time recording rules
- Billing cadence
- Weekly WIP check: thresholds and actions
- Scope creep signals

## Choosing the fee basis

Use the firm's own rate card and pricing policy. These rules help the engagement lead choose; they do not set prices.

| Basis | Use when | Avoid when | Main risk |
| --- | --- | --- | --- |
| Fixed fee | Scope and deliverables are well defined and the firm has done similar work (annual accounts, a defined audit, a standard strategy sprint) | The client's records or inputs are unknown quality, or scope depends on findings | Overrun absorbed by the firm |
| Time and materials (T&M) | Scope depends on what is found (investigations, disputes support, transformation discovery) | The client needs price certainty for approval | Client surprise at the bill |
| T&M with estimate or cap | The client needs a budget but scope is uncertain | | Cap reached before the work is done |
| Retainer | Ongoing access to advice or a fixed monthly capacity (fractional CFO, monthly marketing, ongoing advisory) | Work is lumpy project work better scoped separately | Unused hours or silent overage |
| Milestone or staged fixed fee | Large projects with clear phases | | A phase overrunning undermines the next |

Decision rules:

- If the firm cannot list the deliverables and the client's inputs, it is not ready for a fixed fee. Offer a paid discovery phase on T&M first.
- If the client asks for a fixed fee on uncertain scope, fix the fee for a defined phase and state the assumptions that, if wrong, trigger a change request.
- A retainer states the hours or deliverables included each month, whether unused hours roll over (default: they do not), and the rate for overage.

## What each basis must state in the letter

- **Fixed fee:** the fee, what it covers, the assumptions it depends on, what happens if they are wrong (change request), payment schedule.
- **T&M:** the rates by role from the firm's rate card, the estimate, whether the estimate is a cap, the notification point (default 80% of the estimate), and that work stops at the cap until the client approves more.
- **Retainer:** the monthly amount, inclusions, rollover rule, overage rate, notice period to end or change it, billing in advance.
- **All:** disbursements and how they are charged, GST, payment terms, what happens if invoices are unpaid.

## Time recording rules

- Time is entered daily and no later than the next working day. Late time is the main source of unbilled leakage.
- Each entry has an engagement code, a task or phase, hours, and a narrative a client could read ("Reviewed draft lease schedule; 3 queries raised with client").
- Non-billable time is still recorded against the engagement so overruns are visible.
- Never edit someone else's time entries; ask them.

## Billing cadence

| Basis | Default cadence | Notes |
| --- | --- | --- |
| Fixed fee | On the agreed schedule or milestones | Do not wait for completion if the letter allows progress billing |
| T&M | Monthly in arrears | Large engagements may bill fortnightly |
| Retainer | Monthly in advance; overage in arrears | Report hours used against the retainer each month |
| Disbursements | With the next invoice | Attach receipts if the letter says so |

## Weekly WIP check: thresholds and actions

Run `scripts/wip_check.py` (or apply these by hand) each week, then send the engagement leads a short list of decisions. The script uses these defaults:

| Signal | Threshold | Action for the engagement lead |
| --- | --- | --- |
| Fixed fee burn | 80% of fee used and percent complete more than 10 points behind | Review remaining work; consider a change request; tell the partner |
| Fixed fee over | Over 100% | Partner decides: write down, or raise a variation if scope changed |
| T&M estimate or cap | 80% | Notify the client in writing as the letter requires |
| T&M cap reached | 100% | Stop non-urgent work until the client approves more |
| Retainer use | 90% of monthly hours | Tell the client before overage |
| Retainer overage | Over 100% | Bill or discuss per the letter |
| Unbilled T&M | Older than 30 days | Bill it now; the cycle was missed |
| Aged WIP | Older than 60 days | Bill, or partner decides a write-off |
| Missing time | No entry for more than 2 working days | Ask the person to update their timesheet |
| Entry without a rate | Any | Get the firm's rate; do not assume one |

The agent reports and recommends. Write-offs, write-downs and fee changes are the partner's or engagement lead's decision.

## Scope creep signals

Watch for these in emails, meeting notes and time narratives:

- "While you're at it, could you also..."
- New stakeholders asking for their own deliverables.
- Extra rounds of review beyond those in the letter.
- Time narratives describing work not in the scope list.
- The client's inputs arriving late or incomplete, forcing rework.

When a signal appears, draft a short change request: what was asked, why it is outside the scope in the letter, the estimated fee and time impact, and a request for approval. It goes through the approval gate before it is sent.
