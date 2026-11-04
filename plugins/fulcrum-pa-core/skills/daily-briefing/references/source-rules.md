# Source rules for the brief

Read this while collecting data for a morning brief or weekly review. Each section says what to include, what to drop and what to do when the source is incomplete.

## Inbox: "waiting on you"

A thread is waiting on the owner when **all** of these are true:

- The latest message is inbound and from a person, not an automated sender (no-reply addresses, notifications, newsletters, receipts, calendar responses).
- The owner is in To, not only Cc, or the sender asks the owner by name.
- No reply, draft-in-progress or scheduled send from the owner exists after it. A scheduled message in Outbox counts as handled; a draft does not.
- It asks a question, requests a decision or approval, or contains a deadline.

Rank by:

1. VIP senders (the owner's list), current customers with an open deal or open complaint, and anyone the owner promised a reply to.
2. Stated deadline today or tomorrow, verified against the thread rather than the sender's urgency words.
3. Age: older first. Over 2 business days old moves up one place; over 5 business days becomes a risk.

Cap at five lines. Show `+n more` with a count by type (for example "+6 more: 4 suppliers, 2 recruiters").

Do not count: threads the owner snoozed until a later date, mail in Spam, and threads already assigned to a colleague who replied.

## Calendar: meetings and prep status

| Status | Meaning |
| --- | --- |
| Ready | A brief, agenda or notes exist, and the link or address is in the event. |
| Partial | Something is missing: no agenda, unknown attendee, no link, attachment not read. Name the gap. |
| None | External meeting with nothing prepared. Offer `meeting-prep`. |
| Not needed | Internal recurring meeting, personal block, focus time. |

Flags to raise on the meeting line:

- Clash with another event, or back-to-back with less than 5 minutes when one is in person.
- Guest still "awaiting response" within 24 hours of the start.
- Invitation time zone differs from the attendee's city.
- In-person meeting without travel time in the calendar.
- A booking-page booking with a failed, reserved or rescheduling status.

Show at most six meetings. If there are more, show the external ones and write "+n internal".

## CRM tasks

- Include tasks due today and overdue tasks owned by the owner.
- Overdue by more than 7 days: list once under Risks as "n tasks overdue > 7 days", not one by one.
- Tasks assigned to a team the owner leads: include only if overdue and unclaimed.
- Never mark tasks complete while building the brief.

## Deals

Include a deal in the brief only if one of these is true:

- Expected close date is within the next 7 days or already passed while the deal is open.
- No logged activity for 14 days in an open stage at 40% probability or higher.
- A customer reply on the deal is waiting on the owner.
- The deal moved to won or lost since the last brief (goes under Handled or Wins).

For a full stale-deal sweep, use `pipeline-review`.

## Money

| Line | Rule |
| --- | --- |
| Received | Payments recorded since the last brief, total and count. |
| Due today | Invoices with a due date today, still open. |
| Overdue | Total open past due, count, and the oldest in days. Split 1 to 30 days and 31+ days if both exist. |
| Bills out | Supplier bills and known scheduled payments due in the next 7 days. |
| Cash flag | If bills due in 7 days exceed money expected in 7 days and you know the bank balance is not connected, say "cash position unknown", not "cash shortfall". |

Use the currency and figures in the source. Do not convert currencies. An open invoice is not proof of non-payment if payment sync failed; say "sync status unclear" when the source shows an error. Hand chasing to `invoice-chasing`.

## Decisions

A candidate decision must need the owner's judgement, authority or relationship. Score each candidate and take the top three:

| Factor | Points |
| --- | --- |
| Deadline today | 3 |
| Deadline within 48 hours | 2 |
| Money at stake above the owner's threshold (ask once; default $5,000) | 3 |
| Blocks a colleague, a customer or a delivery | 2 |
| Customer or reputational risk (complaint, public review, legal letter) | 3 |
| Reversible later at low cost | -2 |

Ties go to the older item. Write each decision as a question with the options and your recommendation when the facts support one:

`Approve the Harbour Gate variation ($4,200, +3 days)? Options: approve / ask for split / decline. Draft reply ready.`

Typical decisions: approving a quote, discount or refund; a hiring or rostering call; responding to a complaint; signing a contract; choosing between clashing meetings; approving spend.

Not decisions: anything you can draft and the owner only needs to glance at (put it under Handled), FYI updates and newsletters.

## Risks

Pick at most three. Prefer risks that are new since the last brief or getting worse. Each line ends with a next action and who owns it.

Good sources: complaints and negative reviews, deals slipping, overdue tasks over 7 days, unpaid invoices over 60 days, a key supplier delay, an expiring licence or insurance mentioned in mail, a disconnected mailbox or calendar.

## Missing or partial sources

- Name every unavailable source in the footer: `Not included: bills (accounting not connected)`.
- If the mailbox or calendar needs reconnecting, that is a Risk line with the account name.
- If a source returned an error, do not reuse yesterday's figures. Say "not refreshed".
