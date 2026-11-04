---
name: open-home-follow-up
description: "Turns an open home or private inspection attendee register into a sorted follow-up plan: each attendee classed hot, warm, cold or just looking, same-day SMS and email drafts, contract and vendor disclosure requests logged, feedback captured for the vendor report, and an optional voice-agent call list. Use when an agent says 'follow up the open home', 'who came through on Saturday', 'send the inspection follow-ups', 'sort the attendee list' or pastes a sign-in register or inspection notes. Checks Spam Act consent on the register and waits for approval before anything is sent. Works with any CRM, mail or SMS tool, or pasted notes; uses Fulcrum CRM and Lyre when connected."
---

# Follow up an open home the same day

Sorts every attendee from an open home or private inspection by buying intent, drafts a personal same-day follow-up for each, and records what they said so it feeds the vendor report. The endpoint is an approved batch of messages sent (or saved as drafts), a call list for the agent or a voice agent, and a feedback summary.

## When to use

- After an open home, twilight inspection or private appointment, ideally within three hours of the doors closing.
- When an agent pastes a sign-in register, a photo transcript of the paper sheet, or their own notes ("couple with pram, loved the yard, asked about strata").
- Not for: the weekly vendor campaign report (use `vendor-report`, which takes this skill's feedback summary as input); building a voice agent (use `fulcrum-voice-agent-setup`); reviewing calls after they happen (use `fulcrum-call-review`); general CRM follow-ups unrelated to a listing (use `fulcrum-crm-follow-up`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Attendee register: name, mobile, email, consent tick or wording | Sign-in app, paper sheet, CRM open-home record | Ask once. Without contact details there is nothing to send; produce the feedback summary only. |
| Agent notes per attendee | Agent's notes, voice memo transcript | Classify from register data only and mark every class "provisional". |
| Listing facts: address, price guide as published, contract status, next inspection times, auction or closing date | Listing copy, agent | Ask. Never invent a price figure or an inspection time. |
| Sending identity: agent name, agency, mobile, email signature | Agent | Ask once; do not send without a named sender. |
| The state the property is in | Listing address | Infer from the address; it decides the vendor disclosure document's name. |

## Procedure

1. **Load and clean the register.** Merge duplicates (same mobile or email, couples signed in twice). Flag unreadable or obviously fake entries ("Mickey Mouse", 0400 000 000) as `unverified` and do not message them. Note anyone who already exists in the CRM and their history: a known buyer from another listing changes the tone.
2. **Check consent per attendee** using the checklist below. Record one of: `property-only` (contact about this property), `similar-listings` (express opt-in to alerts), `no-contact` (ticked "do not contact" or gave no consent wording), `unknown`. Only `property-only` and `similar-listings` attendees get drafts. `unknown` goes to the agent to decide.
3. **Classify intent** using [references/attendee-classification.md](references/attendee-classification.md). Read it before classifying. Apply the signals, not a gut feel, and write the one-line reason next to each class. When signals conflict, choose the lower class and say why.
4. **Capture feedback** for every attendee who said anything: price reaction (in words, never as a number the agent did not hear), likes, objections, comparison properties named. Keep exact phrases in quotes where the agent recorded them.
5. **Draft follow-ups** from [references/message-templates.md](references/message-templates.md):
   - Hot: personal SMS within the hour, email with the contract or disclosure offer, proposed call time.
   - Warm: SMS or email the same day answering the question they asked, plus the next inspection time.
   - Cold: short thank-you email, next inspection time, no pressure.
   - Just looking (neighbours, early-stage browsers): one thank-you; offer a market appraisal only if the register says they own nearby and the agency's process allows it.
   Each draft names the sender, the agency and, for anything promotional, a working opt-out.
6. **Contract and disclosure requests.** Where an attendee asked for the contract, offer it. Use the generic phrase "the contract of sale and the vendor disclosure documents" unless the agent tells you the state's document name (for example a Section 32 vendor statement in Victoria). Never attach or send a contract yourself unless the agent supplies the current version and confirms it may go out.
7. **Price guide wording.** Quote only the price guide exactly as the agency has published it. If an attendee asks "what will it go for?", draft the published guide plus an offer to talk, never a different figure. Several states have underquoting rules; the agent owns any price conversation.
8. **Voice-agent calls (optional).** Ask the agent whether hot and warm attendees should get a call from them or from a voice agent. Before any call list is used: attendees must have given a number for contact about this property, the list is washed against the Do Not Call Register unless an exemption or consent applies, calls fall within telemarketing hours, and the call opens with an AI and recording disclosure. If any of these is unclear, keep those attendees on the agent's own call list.
9. **Approval gate.** Show the batch as a table: recipient, channel, sending account (mobile number or mailbox), exact message text, class, consent status. Ask for an explicit yes for the batch or per row. Edits come back as a new version for approval. A draft or a thumbs-up on the classification is not approval to send.
10. **Send or save, then verify.** After approval, send through the connected tool or save as drafts if sending is not connected. Check the sent items or SMS history for each message. After a timeout or unclear error, check history before resending so no one gets two texts. Log each send as an activity on the contact with the listing address.
11. **Hand the feedback on.** Produce the feedback block for `vendor-report` and create tasks for any promised actions (send strata report, call back Tuesday) with an owner and due date.

## Consent checklist for the attendee register

- [ ] The register shows what the attendee agreed to, for example "contact me about this property" or "send me similar listings". Keep the wording.
- [ ] Follow-up about the inspected property fits the reason they gave their details. Adding them to listing alerts or newsletters needs express consent.
- [ ] Every commercial message identifies the agency and agent and includes a working unsubscribe; opt-outs are honoured within 5 working days and recorded in the CRM.
- [ ] Anyone who ticked "do not contact" or who previously unsubscribed is excluded, even if the agent wants to call them.
- [ ] Phone calls: wash the list against the Do Not Call Register yourself or through an access seeker unless an exemption or consent applies; call within telemarketing hours (weekdays 9am to 8pm, Saturday 9am to 5pm, no Sundays or national public holidays); follow your state's call-recording consent rules.
- [ ] Collect and keep only what the follow-up needs. Do not record finance status, health or family details beyond what the attendee volunteered for the purchase.

This is a practical checklist, not legal advice.

## Output

1. **Attendee table**: name, contact, consent, class, one-line reason, next action, owner, due.
2. **Message batch** for approval (see step 9), grouped by class.
3. **Call list** for the agent or voice agent, hot first, with the question each person asked.
4. **Feedback block** for the vendor report: attendee count (groups, not heads, unless the agent counted heads), class split, price reactions, top three likes, top three objections, comparison properties named.
5. **Status report**: sent, saved as draft, pending approval, failed, excluded (with reason).

## Check before you finish

- [ ] Every attendee appears exactly once with a class and a consent status.
- [ ] No message quotes a price other than the published guide or promises anything the agent did not confirm.
- [ ] No message went to `no-contact`, `unknown` or `unverified` attendees.
- [ ] Sent, drafted, pending and failed are reported separately, and sends were checked in history.

## Guardrails

- Do not infer or record protected attributes (ethnicity, religion, age guesses) in classifications or notes.
- Do not tell one buyer what another buyer offered or said about price.
- Do not describe a property feature that is not in the listing copy or the agent's notes.
- Hot leads go back to the agent; the skill never negotiates or accepts an offer.

## With Fulcrum

- Store attendees as contacts with the listing in a tag or custom field, and use a static list for this open home's attendees so the cohort stays fixed. See [Lists](https://fulcrumcortex.github.io/documentation/crm/lists/) and [Contacts and companies](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/).
- Log each SMS, email and call, and create follow-up tasks with owners and due dates, as in [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Lyre can place the calls through an outbound objective, and send SMS where the agent's tools and number allow it. Lyre checks your organisation's own do-not-contact list and calling hours; it does not wash numbers against the Do Not Call Register. "Call with AI Agent" on a contact is only available when the contact has AI Call Consent recorded. See [Outbound calls and campaigns](https://fulcrumcortex.github.io/documentation/lyre/outbound-calls-and-campaigns/) and [SMS in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/).
- Fulcrum CRM also has a Real Estate industry module; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill does not depend on it.

## Learn more

- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [AI for real estate agencies in Australia](https://fulcrumcortex.com/blog/ai-for-real-estate-agencies-australia)
