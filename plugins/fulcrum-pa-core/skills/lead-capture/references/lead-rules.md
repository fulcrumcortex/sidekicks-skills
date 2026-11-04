# Lead rules: triage, duplicates, consent, deals and speed to lead

## Not a lead

| Type | Signals | What to do |
| --- | --- | --- |
| Existing customer, support issue | Matches a customer; refers to a job, order or invoice | Log on their record and hand to support or the account owner. No deal. |
| Existing customer, new need | Matches a customer; asks about something new | Treat as a lead on the existing contact; a new deal if the deal rules are met. |
| Supplier or sales pitch | Offers services to us, "partnership opportunity", SEO and lead-gen offers | Do not create a contact unless the owner wants supplier records. Note it in the brief. |
| Job applicant | CV attached, "position", "role" | Hand to the hiring process; not a CRM lead. |
| Student or researcher | Survey, assignment, interview request | Owner decides; no deal. |
| Spam or suspicious | Mismatched sender, link-only body, payment-change request, urgent wire request | Do not reply, click or create. Report as suspicious to the owner. |
| Out of service area or out of scope | Location or need the business does not serve | Create a contact only if the owner wants a record; draft a polite decline, ideally with a referral. |

## Duplicates

Search in this order and stop at the first confident match:

| Match | Confidence | Action |
| --- | --- | --- |
| Same email (case-insensitive), not a role address | High | Update the existing contact. |
| Same mobile in E.164 and same or similar name | High | Update the existing contact. |
| Same mobile, different name | Low | Could be a shared or recycled number. Create new, flag "possible duplicate" with both records. |
| Same landline only | Low | Shared office line. Treat as different people unless the name matches. |
| Same company domain and same surname | Medium | Show both to the owner; do not merge. |
| Same name and company, no shared contact detail | Medium | Show both; ask. |
| Role address only (info@) | None | Never match on it alone. |

When updating an existing contact: do not overwrite non-empty fields with different values; add the new value to a note ("New mobile given 10 Nov: 0400 000 001") and flag it. Do not change the owner of an existing contact unless the routing rules or the owner say so.

## Consent

Record what the person actually agreed to, by channel.

| Situation | What it supports |
| --- | --- |
| They sent an enquiry | Replying to that enquiry about what they asked, on that channel. Not marketing. |
| Ticked an unticked opt-in box with clear wording | Express consent for the channels named in the wording. Save the wording and date. |
| Pre-ticked box, or no wording shown | Nothing beyond replying. Record "consent wording unknown". |
| Asked to be called back | Consent to call them about this enquiry. Not ongoing telemarketing. |
| Handed over a business card | May support inferred consent for messages relevant to the conversation you had; record where and when. Do not add to a newsletter without asking. |
| Said yes to an AI voice call | AI call consent, recorded with date and how it was given. |
| Said "don't call", "stop", "unsubscribe" | Suppress that channel immediately and note it. |

Checklist:

- [ ] Every commercial email or SMS identifies the business and includes a working unsubscribe, honoured within 5 working days (Spam Act 2003).
- [ ] Consent type, channel, evidence and date are on the record.
- [ ] Marketing lists only include people with express consent or a clear inferred basis.
- [ ] Before any telemarketing call to a number that did not ask to be called, the list has been washed against the Do Not Call Register by the business itself or through an access seeker, unless an exemption applies.
- [ ] Calls happen within permitted telemarketing calling hours, and recording consent rules for the states involved are followed.
- [ ] Only the details needed for the enquiry are collected (Privacy Act 1988, APPs).

This is a practical checklist, not legal advice.

## When to create a deal

Create a deal only when **all** of these hold:

1. The person describes a need the business sells to.
2. They are a likely buyer or acting for one (not a student, supplier or job seeker).
3. At least one buying signal: asked for a quote or price, gave a timeframe, gave a budget, asked for a meeting or site visit, or named a quantity or scope.
4. No open deal already exists for the same need with this contact or company. If one does, update it and log the new touch.

Do **not** create a deal when:

- They only asked a general question ("do you work weekends?") or downloaded something.
- It is a support issue, complaint or warranty claim from a customer.
- It is a duplicate enquiry for a need that already has an open deal.
- The service area or scope is outside what the business does.
- Key facts are missing and one call would supply them: create a task "Qualify" instead and decide after the call.

When you create one: name it `<Company or surname> - <need>`; amount only if the person gave a budget or a standard price applies (otherwise leave it blank, do not guess); first stage of the pipeline; expected close date from their timeframe, or 30 days out if none, marked as an assumption; owner = the lead's owner.

## Speed to lead

| Lead | First response target | Task due |
| --- | --- | --- |
| Asked for a call, quote or booking, during business hours | Within 5 minutes; no later than 1 hour | Today, within 1 business hour |
| General enquiry during business hours | Within 1 business hour | Today |
| Any lead after hours or on a weekend | First thing next business day, 09:00 owner's time | Next business day 09:00 |
| Missed call or voicemail with a callback request | Call back within 15 minutes in business hours | Today |
| Referral from a customer | Same day, and thank the referrer (with approval) | Today |

Owner assignment: routing rule if one exists; otherwise the person who owns the service area or product; otherwise the business owner. A task assigned to a team needs someone to claim it; mention that in the brief.

Fast replies still go through the approval gate. Have the draft ready the moment the record is saved so approval is one tap.
