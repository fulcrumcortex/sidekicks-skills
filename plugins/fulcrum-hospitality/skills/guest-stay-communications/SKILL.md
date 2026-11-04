---
name: guest-stay-communications
description: "Plans and drafts guest messages for a hotel, motel, serviced apartment or resort across the whole stay: pre-arrival, check-in details, upsells limited to what the property actually offers, in-stay requests, amendments and cancellations under the property's own policy, post-stay thank-you and review requests, and complaint recovery. Use when someone says 'send the pre-arrival emails', 'who is arriving tomorrow', 'reply to this guest', 'the guest wants to change dates', 'cancellation request', 'ask for reviews', or 'a guest complained about the room'. Produces a daily message plan and drafts for approval. Works with any property management system export, inbox or SMS tool; uses Fulcrum tools when connected."
---

# Look after guests from booking to review

Sends the right message at each point of a stay, answers guests quickly, and recovers problems before they become a one-star review. Every message uses only facts the property has confirmed: its policies, its facilities and its offers. The endpoint is a daily message plan with approved messages sent, and a log of requests and complaints with owners.

## When to use

- Each morning, to plan arrivals, in-house and departure messages from the arrivals list.
- When a guest writes in with a question, request, change, cancellation or complaint.
- Not for: restaurant table bookings at an on-site restaurant (use `reservation-desk`); weddings, conferences and group functions (use `function-enquiry-quote`); general inbox clean-up (use `fulcrum-inbox-triage`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Arrivals, in-house and departures: guest, contact, dates, room type, rate plan, booking channel, notes | Property management system export | Ask for the export. Do not message guests from memory. |
| Property fact sheet: check-in and check-out times, early and late options, parking, access, Wi-Fi, facilities and hours, local tips | Front office manager | Ask once and keep it. Never describe a facility not on the sheet. |
| Policies: amendment, cancellation, deposit, pets, children, smoking, damage | Property's terms and the rate plan booked | Quote only the written policy for the rate booked. If unclear, escalate. |
| Upsell list: what is offered, price, availability rules | Manager | No upsells until supplied. |
| Recovery authority: what staff may offer (late check-out, a drink, a credit) and the approver above that | Manager | Offer an apology and a manager follow-up only. |
| Sending identity: property name, mailbox, SMS number, sign-off | Manager | Ask. |

## Procedure

1. **Build the daily plan** from the arrivals, in-house and departures lists using the timing table below. One row per guest per message, with the template from [assets/stay-message-templates.md](assets/stay-message-templates.md).
2. **Check the booking channel.** Guests booked through an online travel agency may have a masked email address and the agency's own policies. Reply through the channel the booking came from, and apply the cancellation policy of the rate the guest actually booked.
3. **Personalise from facts only**: name, dates, room type, stated occasion, stated arrival time. Do not guess the purpose of the trip.
4. **Upsells**: offer at most one or two items, only from the manager's upsell list, only if available for the guest's dates (room upgrade inventory, late check-out on a quiet day), and never to a guest with an open complaint.
5. **In-stay requests**: acknowledge within the property's response standard (default 15 minutes during staffed hours), route to housekeeping, maintenance or front office with a room number and deadline, then confirm completion with the guest.
6. **Amendments and cancellations**: compare the request with the rate's policy and the date. Within policy: draft the confirmation. Outside policy (fee applies, non-refundable rate): draft a reply that states the policy clearly and offers what the policy allows (a date change instead of a refund, if the property permits). Waivers and refunds need the manager's approval. Never imply a guest has no rights; Australian Consumer Law protections apply regardless of the policy.
7. **Complaints**: follow [references/complaint-recovery.md](references/complaint-recovery.md). Acknowledge fast, fix what can be fixed during the stay, offer recovery within the staff authority, and escalate above it. Log every complaint with an owner.
8. **Post-stay**: thank-you on the day after departure, and the same review request to every departed guest. A guest with an unresolved complaint gets the manager's follow-up first and the review request afterwards; nobody is left out because they might write a poor review.
9. **Approval gate.** Show each batch: guest, address or number, sending account, exact text and the reason for each message. Wait for an explicit yes for that batch. Routine pre-arrival, departure and thank-you messages can be approved as one daily batch; anything about money, policies, complaints or access codes is approved one by one. After a timeout or unclear send, check sent items or SMS history before retrying.

## Timing

| Message | When | Channel |
| --- | --- | --- |
| Pre-arrival | 3 to 7 days before arrival (next day for short-lead bookings) | Email |
| Check-in details and access | Day before or morning of arrival, after the booking is confirmed paid or guaranteed | SMS and email |
| Welcome and settle-in check | 1 to 2 hours after check-in | SMS |
| Departure reminder | Evening before departure | SMS |
| Thank-you | Day after departure | Email |
| Review request | 1 to 3 days after departure | Email |

## Output

- Daily message plan: guest, stage, channel, send time, template, approval status.
- Drafts for approval, grouped by stage.
- Request and complaint log: guest, room, issue, owner, deadline, status, recovery offered.
- Status: sent, drafted, pending approval, failed.

## Check before you finish

- [ ] Every fact in a message (times, facilities, prices, policies) comes from the fact sheet, policy or booking.
- [ ] Access codes and room numbers go only to the booked guest's verified contact, close to arrival.
- [ ] Every open complaint has an owner and a deadline; guests with an open complaint had the manager follow-up before their review request.
- [ ] Sent, drafted, pending and failed messages are reported separately.

## Guardrails

- Stay messages about the booking are transactional. Upsells and post-stay offers are commercial: identify the property, include a working unsubscribe honoured within 5 working days, and send post-stay marketing only to guests who consented.
- Reviews: ask all departed guests in the same way, do not offer anything in exchange for a positive review, and do not write or edit reviews on a guest's behalf.
- Collect only the guest details the stay needs. Treat identity documents, health information (allergies, mobility) and payment details as sensitive; never repeat card numbers in messages.

This is a practical checklist, not legal advice.

## With Fulcrum

- Keep guests as contacts so preferences and stay history carry over, and log complaints and requests as activities with assigned tasks. See [Contacts and companies](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/) and [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Lyre can send SMS where the agent's tools and number allow it; check message status in the history. See [SMS in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/).
- Fulcrum CRM has a Stay industry module for hotel and resort reservations; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill works with any property management system.

## Learn more

- [SMS, contacts and connections in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/)
- [SMS follow-up after a call](https://fulcrumcortex.com/blog/sms-follow-up-after-every-ai-call)
