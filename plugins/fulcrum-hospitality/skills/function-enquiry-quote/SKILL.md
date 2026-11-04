---
name: function-enquiry-quote
description: "Handles an event, function or catering enquiry from first message to signed booking: qualifies date, guest numbers, budget, style, dietary needs, AV and minimum spend; checks the space is free; builds a quote only from the venue's own packages and terms; sets the deposit and payment schedule from the venue's policy; prepares the banquet event order (BEO) and run-sheet; and runs a follow-up cadence until the client books or releases the hold. Use when someone says 'quote this function', 'private dining enquiry', 'birthday for 40', 'corporate lunch catering', 'wedding reception enquiry', 'chase the quote', or 'prepare the BEO'. Waits for approval before any quote or message goes out. Works with any inbox, calendar or files; uses Fulcrum tools when connected."
---

# Quote and book a function

Turns a function or catering enquiry into an accurate quote, a held date, and, once the client signs, a BEO the kitchen and floor can work from. Speed matters: the first venue to send a clear, correct quote usually wins. The endpoint is an approved quote sent, a tentative hold with an expiry, and follow-ups scheduled.

## When to use

- New enquiries for private dining, exclusive hire, cocktail functions, corporate catering, wakes, weddings and celebrations.
- Following up quotes that have gone quiet, and preparing the BEO for a confirmed event.
- Not for: standard table bookings, including groups within the venue's normal large-group policy (use `reservation-desk`); marketing campaigns for events (use `fulcrum-campaign-brief`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Venue packages and price list: per-head menus, canapé counts, beverage packages by duration, room hire, minimum spends by room and day, surcharges | Function pack, events manager | Stop. Never quote from memory or invent a package. Ask for the current function pack. |
| Terms: deposit amount or percentage, due dates for final numbers and final payment, cancellation scale, tentative hold period | Venue's terms and conditions | Use only what is written. If a term is missing, leave it out and tell the events manager. |
| Space availability for the date | Events diary, booking system | Quote as "subject to availability" and flag it. |
| Enquiry details | Email, form, phone note | Ask for missing essentials in one reply (see step 1). |
| Sending identity and approver | Events manager | Ask. |

## Procedure

1. **Qualify** using [references/qualification-and-quote.md](references/qualification-and-quote.md). Essentials before any quote: date (and a back-up date), guest numbers (minimum and maximum), event type, style (seated, cocktail, buffet, drop-off catering), start and finish times, budget or spend expectation. Second-round details: dietary and allergy needs, AV, accessibility, entertainment, theming, children, who pays and invoicing details. Ask all missing essentials in one message.
2. **Check fit**: room capacity for the style (seated versus standing), minimum spend for that room, day and session, licensing hours, noise or curfew limits, kitchen capacity for the menu style, and conflicts in the diary. If the date is taken, offer the back-up date or another room before declining.
3. **Choose packages**: recommend one primary and at most one alternative from the venue's own packages that fit the budget and style. Explain the choice in one line each.
4. **Build the quote** with [assets/quote-template.md](assets/quote-template.md). Line items: package per head times guaranteed numbers, beverage package by hours, room hire or minimum spend, AV and extras, surcharges the venue's policy names (public holiday, Sunday, late finish), and GST shown as the venue's price list shows it. If food and beverage spend falls short of the minimum, show the shortfall line and how it can be met. Check arithmetic twice.
5. **Set deposit and terms** exactly as the venue's terms state: deposit to confirm, final numbers deadline, final payment date, cancellation scale, what happens if numbers fall below the guaranteed minimum. Quote expiry and tentative hold expiry (default: hold 7 days unless the venue says otherwise).
6. **Approval gate.** Show the events manager the full quote, the covering email, recipient, sending mailbox and attachments. Wait for an explicit yes. Changes produce a new version number. After an uncertain send, check sent items before resending.
7. **Follow up** on the cadence in the reference: day 2 check-in, day 5 hold-expiry reminder, hold release on the expiry date with the manager's approval. Each follow-up adds something useful (an answer, a menu sample, a floor plan) rather than "just checking in". Every follow-up is also shown for approval.
8. **On confirmation**: record deposit receipt (as confirmed by the venue, never assumed), convert the hold to confirmed in the diary, and prepare the BEO with [assets/beo-template.md](assets/beo-template.md): timings, menu with dietary breakdown, beverage service, room set, AV, staffing notes, client contacts, supplier arrivals, billing. Send the BEO to the internal team only.
9. **Final numbers**: at the deadline, confirm numbers and dietary breakdown with the client, update the BEO and the final invoice draft for approval.

## Output

- Qualification summary with gaps.
- Quote (versioned), covering email and hold expiry, for approval.
- Follow-up schedule with dates and drafts.
- BEO and event run-sheet for confirmed events.
- Status: enquiry, quoted, on hold (expiry date), confirmed (deposit received), released, lost (with reason).

## Check before you finish

- [ ] Every price and term traces to the venue's current function pack or terms.
- [ ] Totals reconcile: line items, minimum spend shortfall, surcharges and GST.
- [ ] Capacity fits the style, and licensing or curfew limits are respected.
- [ ] Every allergy is in the BEO with the guest count it applies to.
- [ ] Quote, hold and follow-up status is reported, with sent and drafted items separate.

## Guardrails

- Never promise dishes are allergen-free; use "the kitchen will confirm what it can prepare" until the head chef confirms in writing.
- Do not offer discounts, waive minimum spends or extend holds without the events manager's approval.
- Responsible service of alcohol and licensing conditions apply to beverage packages and finish times; do not quote service beyond licensed hours.
- Follow-up emails about a quote the client asked for are part of the enquiry. Adding the client to newsletters or event promotions needs their consent and a working unsubscribe.

This is a practical checklist, not legal advice.

## With Fulcrum

- Track each function as a deal in a functions pipeline with the event date as the expected close date, and the client as a contact. See [Deals and pipelines](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/).
- Create follow-up tasks with due dates and owners, and log each quote email as an activity, as in [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Offer a site visit through a Fulcrum Calendar booking page. See [Booking pages](https://fulcrumcortex.github.io/documentation/calendar/booking-pages/).
- Fulcrum CRM has a Resto industry module that covers catering management; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill works from the venue's function pack alone.

## Learn more

- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
- [Create a booking page](https://fulcrumcortex.github.io/documentation/calendar/booking-pages/)
