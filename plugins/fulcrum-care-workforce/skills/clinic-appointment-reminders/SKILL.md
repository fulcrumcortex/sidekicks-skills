---
name: clinic-appointment-reminders
description: Plans and drafts appointment reminders, confirmations, no-show and cancellation follow-ups, waitlist backfill and routine recall for health and allied health clinics and practices, by SMS, email or an AI voice agent confirmation call. Sets reminder timing, keeps messages to the minimum (no clinical details in SMS), honours STOP and calling hours, discloses AI and recording on calls, and routes clinical questions to staff. Use for "set up appointment reminders", "reduce no-shows", "confirm tomorrow's patients", "fill a cancellation from the waitlist", "recall patients due for a review", "reminder SMS wording" or "confirmation calls". Works with any practice system, SMS tool or calendar; uses Lyre calls and SMS, Fulcrum Calendar booking pages and Fulcrum CRM when connected. Nothing is sent and no call is placed without approval.
---

# Run clinic reminders, confirmations and recall

Sets up and runs the messages that keep a clinic's diary full: reminders, confirmations, no-show and cancellation follow-up, waitlist offers and routine recall. Built for practice managers and reception teams in general practice, allied health, dental and specialist clinics. The endpoint is an approved reminder plan and, batch by batch after approval, sent messages or placed calls with their outcomes recorded.

## When to use

- Setting up or reviewing a reminder and confirmation cadence.
- Preparing tomorrow's confirmation batch or a confirmation call list.
- Following up no-shows and late cancellations, and offering freed slots to the waitlist.
- Sending routine recall to patients due for a review.
- Not for: clinical recall of abnormal results or overdue critical follow-up (a clinician owns that), designing the voice agent itself (use `fulcrum-voice-agent-setup`), reviewing call transcripts (use `fulcrum-call-review`), or creating the booking page (use `fulcrum-booking-setup`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Appointment list: date, time, practitioner, location or telehealth, appointment category | Practice management system or calendar export | Cannot run; ask for it |
| Patient first name, mobile, preferred channel, opt-outs | Patient record | No mobile or opted out: email or a staff call instead; never guess a number |
| Clinic policies: cancellation notice, fees, no-show rule, recall intervals | Practice policy | Ask once; never mention a fee that is not in written policy |
| Rebooking method: phone number, booking link | Clinic | Use the phone number only |
| Sensitive-service status | Practice manager | Assume the clinic name could reveal health information and use the neutral sender name |
| Clinician risk flags (patients who must not get automated follow-up) | Clinician or practice manager | Ask before any no-show automation |

Work from the minimum. Health information is sensitive information under the Privacy Act. Never paste patient lists into public tools.

## Procedure

1. **Agree the cadence** using [timing and compliance](references/timing-and-compliance.md). Default for a standard consult: booking confirmation at the time of booking; a reminder 2 business days before asking the patient to reply Y or N; for patients who have not replied by the next morning, a confirmation call or second SMS between 10:00 and 16:00 the day before. Add a 7-day reminder for appointments booked more than 4 weeks ahead and for long or prepared appointments (procedures, fasting, equipment).
2. **Write minimal messages** from [message templates](references/message-templates.md). Allowed: patient first name, clinic or neutral sender name, date, time, address or "telehealth", how to confirm, cancel or rebook. Not allowed in SMS or voicemail: reason for visit, practitioner specialty if it reveals the condition, test results, medication, Medicare, DVA or NDIS numbers, fees owed. Preparation instructions go by email or a patient portal; the SMS says only "check your email for preparation instructions".
3. **Check each recipient** before a batch: mobile on file and current, the patient (or parent or guardian for a minor) is the right recipient, no opt-out recorded, no clinician risk flag, not already contacted for this appointment. Shared or landline numbers get a call, not an SMS with details.
4. **Handle replies with fixed rules.**

   | Reply | Action |
   | --- | --- |
   | Y, yes, confirm | Mark confirmed. No reply needed beyond a short thank-you if the clinic wants one. |
   | N, cancel, can't make it | Mark cancelled with the time received, send the rebooking option, release the slot to the waitlist (step 6). |
   | Reschedule or a new time | Offer the booking link or ask staff to call. Do not move the appointment by guessing. |
   | STOP, unsubscribe | Stop SMS to that number at once, record the opt-out, and use calls or email for essential appointment messages only if the clinic's policy allows. |
   | Symptoms, clinical questions, distress | Do not answer. Reply once: "Thanks, a member of our team will contact you. If you need urgent help, call 000." Alert staff straight away. |
   | Wrong number | Apologise, stop, remove the number from the record and flag it for staff. |

5. **Confirmation calls by voice agent** (optional). The agent says it is an AI and that the call may be recorded at the start of every call, confirms it is speaking to the patient by first name before mentioning the appointment, and shares only date, time and location. If someone else answers, it leaves the clinic's name and number only. On voicemail, use the minimal voicemail script. Maximum two call attempts per appointment, within calling hours in the patient's time zone. Escalate to staff on any clinical question or request for a person.
6. **No-shows and cancellations.**
   - No-show: one SMS within 2 hours offering to rebook. No fee mention unless the fee is in written policy, was communicated at booking, and the practice manager approves the wording. A second no-show within 6 months goes to a staff call instead of automation.
   - Clinician risk flags (for example mental health, child protection, palliative or post-operative care): no automated message. Put the patient on the clinician's list the same day.
   - Freed slot more than 2 hours away: offer it to the waitlist in order of clinician-set priority, then appointment type and length match, then time waiting. More than 24 hours away: offer to one patient at a time with a 30-minute hold in business hours. Within 24 hours: offer to the top three at once, first to reply gets it, and tell the others it has gone.
7. **Routine recall.** Only for reviews the clinic has already scheduled as routine (annual check, care plan review, dental check). First message 2 weeks before due; a second 3 weeks later; a staff or voice agent call 3 weeks after that; then close as "no response" and record it. Recall that promotes a new service is commercial: treat it under the Spam Act (consent, sender identified, working unsubscribe).
8. **Approval gate.** For each batch, show the message text with merged values for three sample recipients, the total count, the recipient list or criteria, exclusions applied, the sending number or account, and the send time or call window. Wait for an explicit yes for that batch. A drafted batch is not approval.
9. **Send and verify.** Send once. Check delivery status and replies; a completed call does not prove an SMS was delivered, and a spoken agreement does not prove a booking exists. If a result is unclear, check the sent log or call history before retrying. Record each outcome on the patient or appointment record.
10. **Report weekly:** confirmation rate, no-show rate against the previous month, waitlist fills, opt-outs and replies escalated to staff.

## Output

1. Reminder plan: a table of message type, timing, channel, template and exclusions.
2. The batch for approval: template, three merged samples, count, recipients, sending account and time.
3. After sending: sent, delivered, failed, replied, confirmed, cancelled, opted out and escalated, as separate counts.
4. A staff list: clinical replies, wrong numbers, second no-shows and risk-flagged patients.

## Check before you finish

- [ ] No SMS or voicemail contains clinical details or identifiers beyond first name, date, time and place.
- [ ] Opt-outs, risk flags and already-contacted patients were excluded.
- [ ] Calls placed only within calling hours in the patient's time zone, with AI and recording disclosure.
- [ ] Every clinical reply reached a person.
- [ ] Drafted, approved, sent, delivered and replied are reported as separate states.

## Guardrails

- Not clinical or legal advice. Clinicians own clinical recall, triage and anything a patient says about symptoms.
- Never invent appointment times, availability or fees. Never confirm a booking until the calendar shows it.
- Compliance checklist in [timing and compliance](references/timing-and-compliance.md) covers the Spam Act, calling hours, call-recording consent, AI disclosure and the Privacy Act. This is a practical checklist, not legal advice.

## With Fulcrum

- **Lyre confirmation calls**: create an objective for confirming an appointment, with the information to collect (confirmed, cancel, reschedule) and guardrails (no clinical details). Run it as a one-off call or a call campaign. Turn on AI disclosure on the agent's Compliance tab and word it to cover recording. Outbound calls are checked against the organisation's calling hours (by default Monday to Friday 09:00 to 20:00 and Saturday 09:00 to 17:00, Sydney time, never Sunday) and against the organisation's own do-not-contact list. That is not a Do Not Call Register wash. Check the window against the patient's local time zone. See [Lyre compliance](https://fulcrumcortex.github.io/documentation/lyre/compliance/).
- **Lyre SMS**: campaigns can use the SMS channel. Replies of STOP or UNSUBSCRIBE stop further SMS from you. Call outcomes such as Callback requested and Do not call show in call history.
- **Fulcrum Calendar booking pages**: give patients a rebooking link with sensible minimum notice and booking window. Guests confirm by email before the booking is confirmed, so patients without email need a phone rebooking path. Reschedule or cancel from Manage booking so the patient is kept informed. See [booking pages](https://fulcrumcortex.github.io/documentation/calendar/booking-pages/).
- **Fulcrum CRM**: a Date Picker custom field for the recall due date and an active list filtered on it gives the recall cohort; log each reminder as an activity. Call with AI Agent is only available for contacts with AI Call Consent recorded.

## Learn more

- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [Create a booking page in Fulcrum Calendar](https://fulcrumcortex.github.io/documentation/calendar/booking-pages/)
- [Lyre outbound calls, objectives and campaigns](https://fulcrumcortex.github.io/documentation/lyre/outbound-calls-and-campaigns/)
