---
name: reservation-desk
description: "Runs a restaurant's reservations desk: turns booking requests from email, phone notes, web chat and social DMs into confirmed bookings checked against seats, kitchen pacing and service periods; keeps a waitlist; records dietary and allergy notes safely; sends confirmations and 24-hour reminders; applies the venue's own deposit and no-show policy; and produces the daily run-sheet for floor staff. Use when someone says 'book a table', 'can we fit 8 at 7pm Saturday', 'check tonight's bookings', 'confirm tomorrow's reservations', 'add them to the waitlist', 'cut no-shows' or 'print the run-sheet'. Works with any booking system, inbox or a pasted list; uses Fulcrum tools when connected."
---

# Run the reservations desk

Keeps the book full without overbooking the room or the kitchen. Every request gets a fast, accurate answer, every booking a confirmation and a reminder, and the floor team gets a run-sheet with the notes that matter. The endpoint is an updated booking list, approved guest messages sent, and a run-sheet for the service.

## When to use

- New booking, change or cancellation requests arriving by email, phone note, chat or DM.
- The afternoon before service (confirmations and reminders) and the morning of service (run-sheet).
- Not for: functions, private dining and catering quotes (use `function-enquiry-quote`); hotel guest messages (use `guest-stay-communications`); setting up a public booking page (use `fulcrum-booking-setup`); configuring a phone answering agent (use `fulcrum-voice-agent-setup`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Venue rules: service periods and last seating, seats, table plan and combinations, kitchen pacing (covers per 15 minutes), turn times | Venue manager, booking system settings | Ask once and record them. Without seats and pacing, take requests as "pending confirmation by the venue" only. |
| Venue policies: large-group threshold, deposit or card guarantee, cancellation window, late-arrival hold, children, BYO, set menus | Venue's published policy | Never invent a policy. If none exists, apply no deposit and tell the manager. |
| Current bookings for the date | Booking system, export or pasted list | Do not confirm any request until you have them. |
| The request: name, contact, date, time, party size, occasion, dietary and allergy notes | Message, phone note | Ask for missing essentials in one message: date, time, party size, name, mobile. |
| Sending identity: venue name, phone, mailbox or SMS number | Venue | Ask. |

## Procedure

1. **Parse each request** into: name, mobile, email, date, time, covers, occasion, dietary and allergy notes, seating preference, source channel. Flag ambiguous dates ("next Friday" sent on a Thursday) and confirm them rather than guess.
2. **Check fit** using the rules in [references/booking-rules.md](references/booking-rules.md). For a quick check run `python3 scripts/covers_check.py bookings.csv --seats N --pacing N --service 17:30-21:00 --try 19:00,6`, which tests seats and pacing for the request and suggests times within an hour. A cover count that fits still needs a table that fits: check combinations for groups of 7 or more.
3. **Decide**:
   - Fits: hold the booking as "pending" and draft the confirmation.
   - Fits at another time: offer up to three alternatives, earliest first, within an hour of the request.
   - Does not fit: offer the waitlist and the nearest available service.
   - Large group (venue threshold, often 8 or more): apply the venue's set menu, deposit or card guarantee and cancellation terms exactly as written.
4. **Dietary and allergy notes.** Record them in the guest's words. Allergies go on the booking as "ALLERGY: [item], [severity if stated]". Never write or say "allergen-free", "safe for coeliacs" or similar. The standard reply is: "We have noted the [allergy] and will pass it to the kitchen. Our team will confirm what they can prepare; we cannot guarantee any dish is free of allergens." Anything the kitchen has not confirmed is described as "noted, to be confirmed by the kitchen".
5. **Waitlist.** Add with name, mobile, covers, acceptable time range and the time they were added. When a table frees up, offer it to the first guest whose party size and window fit, not simply the first on the list. Give a reply deadline (default 15 minutes on the day, 2 hours otherwise) before moving to the next guest.
6. **Confirmations and reminders.** Use [references/message-templates.md](references/message-templates.md). Send the confirmation when the booking is made, and a reminder about 24 hours before asking the guest to confirm or cancel. For unconfirmed bookings, follow the venue's policy; the default is one call attempt by staff before service, never automatic release without the manager's say-so.
7. **No-shows and late arrivals.** Hold tables for the venue's late-arrival period (default 15 minutes), then call. Record no-shows on the guest's history. Apply a deposit forfeit or card charge only as the venue's written policy allows and only after manager approval.
8. **Approval gate.** Before sending confirmations, reminders, waitlist offers or deposit requests, show the batch: guest, mobile or email, sending number or mailbox, and exact text. Wait for an explicit yes for that batch. Routine confirmations and reminders can be approved as one daily batch; deposit requests, waitlist offers and anything about money are approved individually. After a timeout or unclear send result, check the SMS or email history before resending.
9. **Run-sheet.** On the morning of service, fill [assets/run-sheet-template.md](assets/run-sheet-template.md): covers by 15-minute slot, pacing pressure points, large groups, allergies and dietary notes highlighted, occasions, VIP or regular notes, deposits held, and the waitlist.

## Output

- For each request: decision, booking details, draft message.
- For each service: the run-sheet, plus a list of unconfirmed bookings and the waitlist.
- Status report: confirmed, pending, waitlisted, declined, messages sent, drafted, failed.

## Check before you finish

- [ ] No slot exceeds seats or pacing, or the manager has approved the exception.
- [ ] Every allergy appears on the run-sheet and the kitchen copy, in the guest's words.
- [ ] No message promises a dish is allergen-free or quotes a policy the venue has not written.
- [ ] Every booking for tomorrow has had a reminder or is listed as unreminded.
- [ ] Sent, drafted, pending and failed messages are reported separately.

## Guardrails

- Allergy and dietary details are health information. Collect only what the kitchen needs, keep it on the booking, and do not reuse it for marketing.
- Booking confirmations and reminders are transactional. Any promotional content (specials, events) makes the message commercial: it needs consent, the venue's identity and a working unsubscribe honoured within 5 working days.
- Do not charge, forfeit or refund money; draft the request for the manager.

This is a practical checklist, not legal advice.

## With Fulcrum

- Keep guests as contacts so regulars, occasions and no-show history follow them, and log each confirmation as an activity. See [Contacts and companies](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/) and [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Lyre can send SMS reminders and place reminder calls where the agent's tools and number allow it; Lyre checks your organisation's own do-not-contact list and calling hours. See [SMS in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/).
- Fulcrum CRM has a Resto industry module for restaurant table bookings, reservations and catering; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill works with any booking system.

## Learn more

- [SMS, contacts and connections in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/)
- [Missed-call text-back](https://fulcrumcortex.com/blog/missed-call-text-back-automation)
