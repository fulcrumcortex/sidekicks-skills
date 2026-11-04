---
name: outbound-call-campaign
description: Plans, pilots and runs an outbound call campaign with an AI voice agent, from objective and success definition through list cleaning, a pre-dial compliance check, call objective design, concurrency and retry cadence, SMS follow-up, outcome review and CRM write-back. Use when the user asks to "call this list", "run a call campaign", "get the AI to ring our leads", "re-engage old customers by phone", "confirm appointments by phone" or "set up outbound calling". Applies Australian calling hours, AI and recording disclosure and opt-out handling, and requires the user to wash the list against the Do Not Call Register themselves. Works with any voice-agent platform or a pasted list; uses Lyre objectives, campaigns and call history when Fulcrum is connected.
---

# Run an outbound AI call campaign

Turns "call these people" into a campaign that has one purpose, a clean and lawful list, a tested call objective and a cadence the team can follow up. The endpoint is an approved campaign plan, a monitored run, and outcomes written back to the CRM with opt-outs suppressed the same day.

## When to use

- A list of people needs calling for one purpose: qualify new enquiries, re-engage lapsed customers, confirm or reschedule appointments, remind about renewals, follow up an event.
- A campaign has run and needs outcome review, a retry wave or CRM write-back.
- Not for: building or tuning the agent's persona, voice, knowledge or tools (`fulcrum-voice-agent-setup`); reviewing one call in depth (`fulcrum-call-review`); a compliance review of an email or SMS send on its own (`outreach-compliance-check`); chasing overdue invoices (`invoice-chasing`); capturing and routing inbound enquiries (`lead-capture`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Purpose and success definition | The user | Ask once. Do not start without one primary success outcome. |
| Call list with name, number, state, source and consent basis | CRM list, CSV export, spreadsheet | Proceed with name and number only, but treat unknown state as the most restrictive time zone and unknown consent as "no consent". |
| Do Not Call Register wash result and its date | The user, through their own Register account or an access seeker | Block telemarketing calls until the user supplies it, unless every number has recorded consent or an exemption applies. |
| Internal do-not-contact and unsubscribe lists | CRM suppression, voice platform, previous campaign outcomes | Ask. Never assume the list is already clean. |
| Voice agent with a phone number, AI and recording disclosure | Voice platform | Hand over to `fulcrum-voice-agent-setup` before continuing. |
| Follow-up capacity | Who takes escalations, callbacks and bookings, and when | Default to concurrency 1 and business-hours-only runs. |
| Destination CRM and field for outcomes | The user | Produce a write-back file for manual import instead. |

## Procedure

1. **Fix the purpose.** One campaign has one purpose and one primary success outcome (for example "booking made"), plus at most two secondary outcomes ("callback requested", "lead captured"). Split mixed requests such as "qualify and upsell and survey" into separate campaigns. Classify the call: if it offers, promotes or advertises anything, treat it as a telemarketing call with the full Register and calling-hours rules. A pure service call to an existing customer (appointment confirmation, delivery window) still follows calling hours and disclosure, and becomes telemarketing the moment the script adds an offer.
2. **Clean the list.** Run `python3 scripts/clean_call_list.py list.csv --suppress dnc.csv --dncr-registered wash_hits.csv --wash-date YYYY-MM-DD --consent-col consent`. It normalises numbers to +61 format, removes duplicates and suppressed numbers, applies the user's wash result and assigns a time-zone group. Also remove by hand: open complaints or disputes, closed or deceased accounts, staff, competitors and anyone who said "Not interested" in the last 90 days. If more than 10% of numbers are invalid or more than 20% have no recorded source, stop and report a list-quality problem instead of calling.
3. **Run the pre-dial checklist** in [references/pre-dial-compliance.md](references/pre-dial-compliance.md). Mark each line pass, fix or block. Any block stops the campaign. For an email or SMS leg, or a wider review, use `outreach-compliance-check`.
4. **Design the call objective** with [references/objective-design.md](references/objective-design.md): goal, three to five items of information to collect, guardrails, an opening line, and a defined response for "not now", "not interested", "stop calling me", "who is this?", "I want a person" and "wrong person".
5. **Pilot before volume.** Place test calls to numbers the user controls covering acceptance, refusal, a stop request, voicemail and an interruption. Then run 10 to 20 real recipients at concurrency 1 or 2. Review every pilot transcript (use `fulcrum-call-review` for depth). Go only if disclosure played on every call, no guardrail was breached and outcomes were classified correctly on a spot check of at least five calls.
6. **Set concurrency and schedule.** Size concurrency to follow-up capacity, not to list size, using the table in [references/cadence-and-follow-up.md](references/cadence-and-follow-up.md). Split the list by time-zone group and use `python3 scripts/calling_windows.py --date YYYY-MM-DD` to get each group's permitted window in the platform's time zone. Schedule each group so the whole batch can finish inside its window.
7. **Plan retries and SMS.** At most three attempts per number per campaign, on different days and at different times of day, and one voicemail at most. Never retry a number whose call reached a final outcome. Build each retry wave from the recipient statuses of the previous wave, never by rerunning the whole list. SMS follow-up rules and templates are in [references/cadence-and-follow-up.md](references/cadence-and-follow-up.md).
8. **Approval gate.** Present the plan from [assets/campaign-plan.md](assets/campaign-plan.md): final recipient count with five sample rows, exclusions by reason, checklist result, objective and opening line word for word, agent and calling number, concurrency, schedule in each recipient group's local time, retry plan, SMS text and sending number, and where the report goes. Wait for an explicit yes. Each retry wave and each SMS batch needs its own yes. A draft plan is not approval.
9. **Monitor the first 30 minutes.** Read the first five to ten completed calls. Cancel the campaign at once and report if disclosure is missing, the agent states something untrue or outside its guardrails, a call lands outside a recipient's local hours, or more than 5% of connected calls end in "do not call" or a complaint.
10. **Review outcomes.** Report the funnel defined in [references/cadence-and-follow-up.md](references/cadence-and-follow-up.md) against the success definition. Check promises independently: if the agent said it would send a link or book a meeting, confirm the SMS or calendar entry exists. A created campaign is not proof that individual calls succeeded.
11. **Write back and suppress.** Apply the outcome mapping in [references/cadence-and-follow-up.md](references/cadence-and-follow-up.md). Add every "do not call" or stop request to the do-not-contact list and CRM suppression the same day, and remove the person from other active campaigns and follow-up tasks. Show the proposed bulk changes before applying more than 50 record updates.

## Output

- Before launch: the filled [assets/campaign-plan.md](assets/campaign-plan.md), ending in the approval request.
- After each wave: a results note with the funnel table, outcome counts, five notable calls (best, worst, any complaint), promised actions verified or missing, records updated, numbers suppressed, and the proposed next wave or stop.

## Check before you finish

- [ ] The wash result is dated within 30 days for every telemarketing call, or the exemption or consent basis is written down.
- [ ] No call was placed outside the recipient's local calling window or on a national public holiday.
- [ ] Every stop request and "do not call" outcome is on the do-not-contact list and removed from active campaigns.
- [ ] Promised SMS, links and bookings were checked in their destination, not inferred from the summary.
- [ ] Report sent, scheduled, completed, failed and cancelled calls separately; say which records were updated and which are pending.

## Guardrails

- Never tell the user a product has washed their list against the Do Not Call Register. The user, or an access seeker they engage, does that.
- The agent must never claim or imply that it is a person. Disclosure of AI and recording plays at the start of every campaign call.
- Collect only the information the objective needs. Do not collect health, financial hardship or other sensitive details on a marketing call.
- If the person sounds distressed, confused, vulnerable or under 18, the agent ends politely and flags the call for a person. No retry.
- After an uncertain result (timeout, unclear error), check call history before dialling anyone again.

## With Fulcrum

In **Lyre**, an **Objective** holds the goal, information to collect, guardrails and an opening line that can use `{{name}}`, `{{agent_name}}`, `{{date}}` and `{{time}}`. A **Campaign** sets the channel (call, SMS or email), an outbound number with an agent assigned, **Concurrent calls** (1 to 10), the objective, recipients, a schedule in your local time and an optional report email; each recipient's status, outcome and attempt time are visible, and **Cancel campaign** stops it. Use **Journeys** for multi-step flows.

Lyre checks every outbound dial against your organisation's calling hours (by default Monday to Friday 09:00 to 20:00 and Saturday 09:00 to 17:00, Sydney time, never Sunday) and against your organisation's do-not-contact list; if that check cannot complete, the call does not go ahead. **These controls do not wash numbers against the Do Not Call Register, the window is in Sydney time rather than the recipient's, and national public holidays are your responsibility.** Use **Override calling hours** only for testing or for contacts who agreed to out-of-hours calls. Turn on **AI disclosure** in the agent's Compliance tab and watch the **Disclosure rate** on its Quality tab. "Do not call" outcomes are flagged in call history; the do-not-contact list itself is managed through Lyre's tools for connected AI assistants. New calls are blocked when the credit balance runs low, so check it before launch.

In **Fulcrum CRM**, **Call with AI Agent** is available only when the contact's **AI Call Consent** is recorded, and every call is logged on the contact's timeline. A Lyre agent can also log activity to a connected CRM through **Activity logging** in its Tool access tab.

## Learn more

- [Outbound calls, objectives and campaigns in Lyre](https://fulcrumcortex.github.io/documentation/lyre/outbound-calls-and-campaigns/)
- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [Call history, recordings and transcripts](https://fulcrumcortex.github.io/documentation/lyre/call-history/)
