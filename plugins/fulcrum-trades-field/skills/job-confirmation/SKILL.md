---
name: job-confirmation
description: Confirms and dispatches trade and field-service jobs. Drafts day-before confirmations by SMS or call, handles replies and reschedules, captures access, pet and parking notes, builds a run-sheet per technician grouped by suburb, sends on-the-way and running-late messages, and closes the job with completion notes and an invoice trigger. Use when a plumber, electrician, HVAC, cleaning, pest or other field business asks to "confirm tomorrow's jobs", "text the customers", "build the run sheet", "send the on my way text", "reschedule a job" or "close out today's jobs". Works with any calendar, job list or CRM, or a pasted schedule; uses Lyre, Fulcrum Calendar and Fulcrum CRM when they are connected.
---

# Confirm, dispatch and close field jobs

Turns tomorrow's job list into confirmed appointments, a run-sheet each technician can follow, timely customer updates on the day, and a clean hand-off to invoicing. The endpoint is a confirmed schedule, sent messages the user approved, and a completion record for every job.

## When to use

- The day before: confirm jobs, collect access details, chase non-responders.
- The morning of: publish run-sheets, send on-the-way and running-late messages.
- The end of the day: record completion, raise follow-up jobs, trigger invoices.
- Not for: setting up a public booking page (`fulcrum-booking-setup`), reviewing a confirmation call after the fact (`fulcrum-call-review`), pricing a job (`takeoff-to-quote`), or marketing campaigns to past customers (`fulcrum-campaign-brief`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Job list for the date: customer, mobile, address and suburb, job type, time window, estimated duration, assigned tech | Calendar, job system, CRM, pasted list | Ask for it once. Do not build a run-sheet from memory. |
| Access, pet and parking notes | Job notes, previous visits, the confirmation reply | Ask in the confirmation message |
| Contact preference and opt-outs | CRM record, previous STOP replies | Default to SMS; never contact anyone marked do-not-contact |
| Sending number or mailbox, and business name as it should appear | User | Ask before drafting the first message |
| Business rules: confirmation window, late-cancel or call-out fee wording, tech start time | User or existing terms | Leave fee wording out; never invent a fee |

## Procedure

1. **Load and check the list.** Flag before anything else: jobs with no mobile number, numbers not in `04xx` or `+61` format, missing suburb, two jobs overlapping for one tech, a fixed-time job that cannot be reached from the previous one, and customers on the do-not-contact list. Fix or ask; do not silently drop a job.
2. **Pick the confirmation channel per job.**
   - SMS first for everyone with a mobile.
   - Call instead of SMS for: jobs over a threshold the user sets (for example a full-day install), first-time customers with access complexity (strata, gated estates, basements), and anyone who has not answered SMS before.
   - Landline only: call.
3. **Draft day-before confirmations** from [references/message-templates.md](references/message-templates.md). Each message names the business, the date, the arrival window (not an exact time), the job in plain words, and asks the customer to reply YES, or to call or reply to change it. Ask for access, pet and parking details only when the job record lacks them.
4. **Approval gate.** Show the batch as a table: customer, number, channel, exact message text, and the sending number or account. Wait for an explicit yes. Approval covers this batch only.
5. **Send in calling hours.** Send confirmations between 09:00 and 17:00 the working day before (Friday for Monday jobs). Place calls within the telemarketing-style window even though a confirmation is not a sales call: weekdays 09:00 to 20:00, Saturday 09:00 to 17:00, no Sundays or national public holidays, in the customer's local time.
6. **Handle replies** using the reply table in the templates reference: YES confirms; a time change goes to step 7; STOP or "don't text me" is recorded as an opt-out at once; anything else (a question, a complaint, a quote dispute) goes to a person. Record access, pet and parking details on the job, not only in the message thread.
7. **Reschedule.** Offer two or three real slots from the calendar, never invented ones. Hold nothing until the customer picks. Update the calendar entry, the job record and the run-sheet, then send a new confirmation (gate again). Record the reason. Apply a late-change or call-out fee only if the business's own terms state one and the user tells you to.
8. **Chase non-responders.** No reply by 15:00: one call (or a second SMS if calls are not allowed). Still unconfirmed by 17:00: list them for the user with a recommendation (keep, call first thing at 09:00, or swap with a standby job). Never cancel a job because the customer did not reply.
9. **Build the run-sheet per tech** following [references/run-sheet-rules.md](references/run-sheet-rules.md) and [assets/run-sheet-template.md](assets/run-sheet-template.md): fixed-time jobs anchor the day, the rest cluster by suburb, travel buffers between clusters, parts pick-ups placed after suppliers open. Access codes go on the tech's sheet only, never in a customer message or group channel.
10. **On the day.** Draft an on-the-way message when the tech leaves the previous job, with a 30-minute arrival window. If the tech will be more than 15 minutes outside the confirmed window, send a running-late update; more than 60 minutes, call the customer and offer to rebook. Each message goes through the approval gate, or under a standing approval the user has given for that exact template and day.
11. **Close each job.** Record: work done, materials and parts used, time on site, photos taken (before and after), customer sign-off or "customer not home", and whether a return visit is needed. Then choose one route:
    - Complete and priced (fixed quote or agreed rates): draft the invoice.
    - Complete, variation or extra work done: draft the invoice with the extra items listed separately and flag them for the user to check against what the customer approved.
    - Incomplete: create the follow-up job and a task, and tell the customer when they will hear from you.
12. **Approval gate.** Before any invoice is issued or sent, show the customer, line items, amounts and GST, the sending account and the delivery channel. Wait for an explicit yes. A drafted invoice is not an issued invoice.
13. **Log and verify.** Log each confirmation, call outcome and reply as an activity on the customer record. After any send that timed out or returned an unclear status, check sent items or call history before retrying so nobody gets the same message twice.

## Output

- A confirmation status table: job, customer, channel, sent at, reply, status (`confirmed`, `rescheduled`, `unconfirmed`, `opted out`, `needs a person`).
- One run-sheet per tech, filled from [assets/run-sheet-template.md](assets/run-sheet-template.md).
- A close-out table: job, outcome route, invoice draft reference or follow-up job, open issues.

## Check before you finish

- [ ] Every job on the list has a status; none was dropped.
- [ ] Every outgoing message was approved and its delivery checked in sent items or history.
- [ ] Opt-outs are recorded on the customer record, not only in the thread.
- [ ] Run-sheets have no overlapping jobs and no access codes outside the tech's own sheet.
- [ ] Report sent, drafted, pending and failed separately.

## Guardrails

- Keep confirmation, on-the-way and running-late messages purely factual. Adding a promotion or "refer a friend" line turns them into commercial messages that need consent and an unsubscribe.
- Spam Act checklist for any commercial SMS or email: consent (express, or inferred from an existing relationship); the business clearly identified; a working unsubscribe honoured within 5 working days.
- Do Not Call Register: confirmation calls about an existing booking are not telemarketing. If a call will also offer a new service, the user must wash the number against the Register themselves or through an access seeker first, unless an exemption applies.
- Call recording: recording rules differ by state. Tell the customer at the start of a recorded call that it is recorded.
- Privacy Act and APPs: collect only what the job needs. Gate and lockbox codes are security information; store them on the job record with restricted access and delete them from message drafts.
- Never invent arrival times, prices, fees or availability.

This is a practical checklist, not legal advice.

## With Fulcrum

- **Lyre** can place a one-off outbound call or run a call or SMS campaign with an objective such as confirming an appointment. Outbound calls are checked against the organisation's own do-not-contact list and calling window (by default weekdays 09:00 to 20:00 and Saturday 09:00 to 17:00 Sydney time, never Sunday), and an SMS reply of STOP or UNSUBSCRIBE stops further SMS. Lyre does not wash numbers against the Do Not Call Register. Check the time zone for customers outside New South Wales, Victoria, Tasmania and the ACT. Outcomes such as Callback requested or Do not call appear in call history; a completed call does not prove an SMS was delivered.
- **Fulcrum Calendar** holds the job events; bookings made through a booking page are rescheduled through Manage booking so the customer is kept informed.
- **Fulcrum CRM** logs calls and SMS as activities on the contact, holds follow-up tasks for a person, team or AI agent, and keeps invoices as drafts until someone selects Finalize & Send.
- Industry modules such as Construction may be available in Fulcrum CRM depending on the account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Outbound calls, objectives and campaigns in Lyre](https://fulcrumcortex.github.io/documentation/lyre/outbound-calls-and-campaigns/)
- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [Tradie job confirmations by call and text](https://fulcrumcortex.com/blog/tradie-job-confirmations-by-call-and-text)
