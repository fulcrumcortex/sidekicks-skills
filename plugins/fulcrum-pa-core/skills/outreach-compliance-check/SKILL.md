---
name: outreach-compliance-check
description: Runs a pre-flight compliance review of an email, SMS or call campaign, or a single bulk message, against Australian rules and returns a pass, fix or block report with the evidence checked and the exact fix for each gap. Covers the Spam Act (express or inferred consent, sender identification, a working unsubscribe honoured within five working days, no harvested addresses), the Do Not Call Register (the user's own wash, its 30-day validity, narrow exemptions), telemarketing calling hours, AI and call-recording disclosure, the Privacy Act and APP 7 direct marketing, and suppression list hygiene. Use when the user asks "is this campaign compliant", "can we send this", "check this before it goes out", "Spam Act check", "DNCR check" or "review our outreach". A practical checklist, not legal advice.
---

# Pre-flight compliance check for outreach

Reviews a planned email, SMS or call campaign, or one bulk message, before it goes out, and returns a report that says **pass**, **fix** or **block** for each requirement, with the evidence seen and the change needed. The endpoint is a written report; this skill never sends anything.

## When to use

- Before any marketing email, SMS or newsletter to more than a handful of people, or any outbound call campaign.
- When a list has come from somewhere new (a purchase, an event, a partner, a scrape, an old system).
- When a message template, sender or audience changes on a running campaign.
- After a complaint, to check what went wrong.
- Not for: planning and running a call campaign end to end (`outbound-call-campaign`, which calls this check); writing the campaign itself (`fulcrum-campaign-brief`); one-to-one replies to a person who wrote in (`fulcrum-inbox-triage`); requesting customer reviews (`review-response` has its own checklist).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The exact message: subject, body, sender name and address or number, links, or the call script and disclosure | Draft, template, campaign tool | Ask. A check without the real content can only cover the audience. |
| Audience definition and size | List, segment, filter | Ask. |
| Where each contact came from and the consent wording shown at collection | Form, CRM consent field, import notes | Mark consent as unverified, which is a block for commercial messages. |
| Unsubscribe and suppression lists, and which tools have them | Email tool, SMS provider, CRM, voice platform | Ask which lists exist; a missing list is a fix or block. |
| For calls: Do Not Call Register wash result and date, calling schedule, recipient states | The user | Block until supplied. |
| Business type (clinic, disability provider, financial services, other) | The user | Ask; it changes the sensitive-information checks. |

## Procedure

1. **Define the scope.** Record channel(s), sender, purpose, audience size, send date and time, and the tool used. A campaign with email, SMS and call legs gets every relevant section.
2. **Classify each message.** Is any purpose to offer, advertise or promote goods, services, land, an opportunity or the business? Then an email or SMS is a commercial electronic message and a call is a telemarketing call. Factual or transactional messages (receipts, appointment confirmations, invoice reminders) without promotional content are usually not, but one promotional line changes that. Note whether the sender may fall within a narrow exemption (for example a registered charity or a government body); exemptions still require sender identification.
3. **Collect evidence.** For lists over 50 contacts, inspect at least 10 random records plus at least one record from every distinct source; a source with any record lacking consent evidence is flagged as a whole. Test the unsubscribe or STOP path yourself where you can. Read the full message, including the footer and the landing page.
4. **Run the checklists.** Use [references/spam-act.md](references/spam-act.md) for email and SMS, [references/dncr-and-telemarketing.md](references/dncr-and-telemarketing.md) for calls, and [references/privacy-and-suppression.md](references/privacy-and-suppression.md) for every channel.
5. **Rate each item.**
   - **Pass**: evidence seen and it meets the requirement.
   - **Fix**: a gap that can be corrected before sending; state the exact change.
   - **Block**: likely breach or high-risk gap; the send must not go ahead until resolved.
   Missing evidence is never a pass. Missing evidence for consent, the Register wash, a working unsubscribe, calling hours, AI disclosure or sensitive information is a block.
6. **Apply the automatic blocks.** Block if any of these are true: no consent basis for a commercial email or SMS; a bought, scraped or harvested list without consent evidence that covers this sender; a message whose purpose is to ask for consent sent to people who have not consented; no functional unsubscribe; sender not identified or disguised; telemarketing numbers not washed or washed more than 30 days before the call date with no exemption or recorded consent; calls scheduled outside the recipient's local calling hours; an AI voice agent without disclosure or one that could claim to be a person; health or other sensitive information used for marketing without consent; previously unsubscribed or do-not-contact people in the audience; misleading content such as false urgency, a fake prior relationship, "you've won", or a deceptive subject line.
7. **Give the verdict.** Overall **block** if any item is a block, **fix** if any item is a fix, otherwise **pass**. After the user makes fixes, re-run only the affected items and update the report.
8. **Hand back.** If the user then wants to send, the sending skill or tool runs its own approval gate. A passed check is not approval to send.

## Output

Use [assets/compliance-report.md](assets/compliance-report.md): scope, overall verdict, blocks first, then fixes, then passes, each with the evidence checked and the exact change, and a re-check list. Keep it short enough to read in two minutes; put sample record IDs, not personal details, in the evidence column.

## Check before you finish

- [ ] Every item has a status and the evidence behind it; nothing is marked pass on assumption.
- [ ] Every fix and block names the change and who makes it.
- [ ] The report ends with "This is a practical checklist, not legal advice."

## Guardrails

- Use cautious, accurate wording: "likely breach", "does not meet", "evidence not supplied". Do not say a campaign is "legal" or "fully compliant"; say it passed this checklist on the evidence seen.
- Never say a product has washed a list against the Do Not Call Register. Only the user, or an access seeker acting for them, does that.
- Do not copy personal information into the report beyond record IDs and counts.
- If the business is in a regulated sector (health, disability support, financial services, gambling, alcohol), say that sector rules may add requirements and recommend the user checks them.
- This is a practical checklist, not legal advice. For a disputed or high-stakes campaign, recommend the user gets professional advice.

## With Fulcrum

Fulcrum CRM **campaigns and newsletters** include an unsubscribe link in every send and stop sending to anyone who unsubscribes; you remain responsible for having consent. Members can build campaigns but not send them, and AI assistants can never send bulk email. Use **Send test** to an address you control to check sender, merge fields, links and unsubscribe. A contact's **Campaign emails** card shows delivered, opened, clicked, bounced, unsubscribed or spam-reported, and since when the address has been suppressed. List membership does not override suppression, unsubscribe state or contact permissions.

In **Lyre**, every outbound dial is checked against your organisation's **calling hours** (default Monday to Friday 09:00 to 20:00 and Saturday 09:00 to 17:00, Sydney time, never Sunday) and its **do-not-contact list**; **AI disclosure** is set per agent. SMS replies of STOP or UNSUBSCRIBE stop SMS from you. These are organisation controls; Lyre does not wash numbers against the Do Not Call Register, and its calling window is in Sydney time rather than the recipient's. In Fulcrum CRM, **Call with AI Agent** requires the contact's **AI Call Consent**.

## Learn more

- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [Email, campaigns and unsubscribes in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/email/)
- [Lists in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/lists/)
