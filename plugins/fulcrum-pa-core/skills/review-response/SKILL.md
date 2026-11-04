---
name: review-response
description: Drafts replies to public customer reviews on Google, Facebook and industry sites in the brand's voice, after classifying each review as praise, mixed, complaint, fake or suspicious, or containing private information, and flags anything that needs escalation. Never discloses private or health information in a public reply, which matters most for clinics and NDIS providers; complaints are taken offline. Also covers asking customers for reviews ethically, with no incentives tied to reviews and no review gating, as a checklist based on ACCC guidance. Use when the user asks to "reply to our reviews", "respond to this Google review", "handle a bad review", "deal with a fake review" or "get more reviews". Nothing is posted or sent without approval.
---

# Reply to public reviews and ask for them fairly

Produces a reviewed set of public replies, one per review, each matched to the review's type and the brand's voice, plus an escalation list for anything that should not be handled in public. The endpoint is replies approved and posted (or handed to the user to post), and complaints moved to a private channel with an owner.

## When to use

- New reviews have arrived and need replies, or there is a backlog.
- One difficult review: a complaint, an allegation, a suspected fake, or a review that exposes private information.
- The business wants to start or tidy up asking customers for reviews.
- Not for: replying to a private email or message from a customer (`fulcrum-inbox-triage`); a customer follow-up that is not about a review (`fulcrum-crm-follow-up`); a marketing campaign that quotes reviews (`fulcrum-campaign-brief`, then `outreach-compliance-check`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The review text, star rating, reviewer display name, platform, date and link | Pasted, exported, or read through a connected tool | Ask for it. Do not reply to a paraphrase. |
| Business type | The user | Ask once. Health, disability, legal and financial services follow the stricter privacy rules below. |
| Brand voice: two or three past replies the user liked, or a short description | The user | Use warm, plain Australian English, first person plural, signed with a first name and role. |
| Who handles complaints, and the private contact channel to offer | The user | Ask once; never invent a phone number or email address. |
| Whether the reviewer is a known customer | CRM or booking records, checked privately | Treat as unknown. Never state either way in public. |
| Posting account | The user | The reply drafts are handed over for the user to post. |

## Procedure

1. **Classify each review** with the table in [references/reply-playbook.md](references/reply-playbook.md): praise, mixed, complaint, fake or suspicious, contains private information, or serious allegation. A review can carry two labels (for example complaint and private information); the stricter rule wins.
2. **Escalate before drafting** when the review alleges harm, abuse, neglect, discrimination, a safety issue, professional misconduct or a legal threat, or comes from someone who appears to be at risk. Send it to the owner or the person who runs incidents, with the link. For an NDIS provider, an allegation about a participant may be a reportable incident with short notification deadlines under the provider's incident management system. Draft only a short holding reply, and post nothing until the user decides.
3. **Check privately.** Look the reviewer up in the CRM or booking system only to decide who should contact them. Whatever you find stays out of the public reply.
4. **Draft the reply** using the pattern for its class in [references/reply-playbook.md](references/reply-playbook.md):
   - Praise: one to three sentences, thank them, mention a non-private detail they raised, no sales pitch.
   - Mixed: thank them, acknowledge the issue plainly, state a change only if it has really happened, invite them to get in touch.
   - Complaint: acknowledge and apologise for the experience without arguing facts or admitting liability, give a named private contact channel, and say who will follow up. Three to five sentences.
   - Fake or suspicious: do not accuse. Report it through the platform's own process with the evidence, and if a public reply is needed, use the neutral version.
   - Private information: never repeat it. Ask the platform to remove a review that exposes someone else's information, and reply generically.
5. **Apply the privacy rule for confidential services.** For clinics, allied health, disability support, legal, financial and similar services, the reply must neither confirm nor deny that the reviewer is or was a client, and must not mention appointments, treatment, diagnoses, funding, plans or dates. Write "We can't discuss anyone's care publicly" rather than "We have no record of you" or "As we discussed at your appointment".
6. **Vary and check.** No two replies in a batch should be identical. Check spelling of the reviewer's display name (first name only), remove staff surnames, remove offers and discount codes, and make sure every promise in the reply is something the business will do.
7. **Approval gate.** Present a table: platform, review link, star rating, class, the exact reply, the posting account, and any escalation or private follow-up proposed. Wait for an explicit yes for each reply or for the batch. Serious allegations and legal threats need the owner's yes specifically.
8. **Post or hand over, then verify.** Post through the approved account if a connected tool allows it, otherwise give the user the final text. Confirm each reply is visible on the platform. If a post fails or times out, check the review page before trying again so the reply does not appear twice.
9. **Follow through.** For complaints, create a task for the named person to contact the customer privately within one business day, and log the review and the reply on the customer's record where there is one.
10. **Requesting reviews.** If the user wants more reviews, run the checklist in [references/requesting-reviews.md](references/requesting-reviews.md) and draft requests from [assets/review-request-templates.md](assets/review-request-templates.md). Requests by email or SMS are outward messages and go through their own approval gate.

## Output

| Platform | Review (link, stars, date) | Class | Draft reply | Escalation or private follow-up |
| --- | --- | --- | --- | --- |

Below the table: escalations with owner and reason, reviews reported to the platform with the reason given, and reviews deliberately left without a reply.

## Check before you finish

- [ ] No reply contains health, disability, financial or other private information, or confirms someone is a client.
- [ ] Every complaint has a named private contact route and an owner with a due date.
- [ ] Every escalated review is with the owner and has no public reply beyond an approved holding statement.
- [ ] Posted replies are confirmed visible; drafted, posted and held replies are reported separately.

## Guardrails

- Never write, buy, swap or post reviews for the business, and never review competitors.
- Never offer a refund, discount or gift in exchange for removing or changing a review.
- Do not argue, blame the customer, or reveal anything a customer told the business privately.
- Do not reply to a review that names a staff member's personal details; report it to the platform and tell the user.
- Registered health practitioners have advertising rules that restrict using testimonials; do not reuse a review in advertising without checking current Ahpra guidance.
- The checklists here are practical checklists, not legal advice.

## With Fulcrum

No Fulcrum product is documented as connecting to review platforms, so replies are posted on the platform or through whatever tool the host provides. Fulcrum CRM helps with the private side: find the customer by name, email or phone, log the review and your reply as a **Note** on the contact's timeline, and create a **task** assigned to the person who will call, with a due date and priority. Send the private follow-up from the CRM email composer with a connected mailbox; after **Send** there is a 30-second **Stop send** window for a last check. Review requests sent as a CRM campaign include an unsubscribe link automatically; a person sends campaigns, as AI assistants cannot send bulk email.

## Learn more

- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
- [Contacts and companies in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/)
