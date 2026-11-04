# Concurrency, retries, SMS follow-up, review and CRM write-back

## Concurrency

Concurrency is how many calls run at once. Size it to the people who must act on the results, not to the list.

| Situation | Concurrency |
| --- | --- |
| Test calls and pilot (first 10 to 20 recipients) | 1, then 2 |
| Bookings go straight into a calendar and need no person | Up to the platform limit, once the pilot passes |
| Calls produce callbacks or escalations a person must handle the same day | No more than the number of people available to handle them during the run |
| Live warm transfers to staff | Equal to the number of staff free to take a transfer |
| Sensitive purpose (renewals with price changes, collections, health-related service) | 1 or 2, with a person reviewing every call that day |

Raise concurrency one step at a time and only after reading a sample of calls from the previous level.

## Retry cadence

- Maximum three attempts per number per campaign.
- Attempt 2 no earlier than the next business day, at a different time of day from attempt 1 (for example morning, then late afternoon).
- Attempt 3 three to five business days after attempt 2.
- Leave at most one voicemail per campaign, on the first or last attempt. Content: agent name, business, short purpose, callback number. No amounts, health details or account information.
- Retry only "No answer", "Busy", "Voicemail" or failed calls. Never retry a number with a final outcome, a stop request, a complaint or a wrong-number result.
- Build each retry wave from the recipient statuses of the previous wave. Do not rerun the whole list until you know who has already been called.
- If the wash result will be older than 30 days on the retry date, the list must be re-washed first.

## SMS follow-up

SMS is covered by the Spam Act, not the Do Not Call Register. Run the SMS leg through `outreach-compliance-check` if it promotes anything.

| Trigger | Send? | Notes |
| --- | --- | --- |
| Booking made on the call | Yes, confirmation | Factual: date, time, address, how to change. Identify the business. |
| Person asked for a link or information | Yes, only what they asked for | Check the SMS was actually delivered; a completed call does not prove it. |
| Callback requested | Optional confirmation of the agreed time | One message. |
| No answer after attempt 1 | Only with consent to receive marketing SMS | Counts as a commercial message: identify the sender and include an opt-out. |
| Not interested, Do not call, wrong number | No | Sending after a decline invites complaints. |

At most one SMS per attempt cycle and no more than two SMS per person per campaign.

Templates (fill the brackets; keep under 160 characters where possible):

```text
Booking confirmation:
[Business]: you're booked for [day date] at [time], [address]. To change, reply or call [number].

Requested information:
[Business]: here's the [item] you asked for on our call: [link]. Questions? Call [number].

Callback confirmation:
[Business]: thanks [first name], we'll call you back [day] around [time] as discussed.

No-answer follow-up (only with marketing consent):
[Business]: sorry we missed you, [first name]. We called about [purpose]. Book at [link] or call [number]. Reply STOP to opt out.
```

## Outcome review

Report these for each wave, with counts and rates:

| Measure | Definition |
| --- | --- |
| Dialled | Calls attempted |
| Connected | A person answered (excludes voicemail, busy, no answer, failed) |
| Connect rate | Connected / dialled |
| Primary success | Calls ending in the primary success outcome |
| Success per connect | Primary success / connected |
| Callbacks requested | Count, and how many are scheduled |
| Escalations | Count, and how many a person has handled |
| Do not call and complaints | Count and rate per connected call; above 5% means stop and review the objective |
| Disclosure rate | Calls where disclosure played / connected; anything under 100% is a fault |
| Promised actions verified | SMS delivered, bookings existing, against what the agent said |

Read low-scoring calls first, then a random sample of five successful ones. A quality score is a prompt to listen, not a verdict.

## CRM write-back mapping

| Outcome | CRM action |
| --- | --- |
| Booking made | Log the call; confirm the calendar entry exists; move the deal or lifecycle stage only if the user's pipeline defines that step |
| Lead captured | Log the call with the collected answers in fields, not only in notes; create a task for the owner due the next business day |
| Callback requested | Task for the agreed time, assigned to a person or the agent |
| Not the decision maker | Log; record the named decision-maker if offered; no further calls to this number in this campaign |
| Not interested | Log; tag with campaign and date; exclude from this purpose for at least 90 days |
| Do not call | Add to the do-not-contact list and CRM suppression the same day; remove from active campaigns and tasks |
| Escalated to human | Task due the same day for a named person, with the reason |
| Wrong number | Clear or flag the number on the record; do not delete the contact |
| No answer after final attempt | Log attempts; leave in nurture if consent allows |

Write collected answers into structured fields where the CRM has them, so they can be filtered later. Do not paste full transcripts into notes; link to the call instead.
