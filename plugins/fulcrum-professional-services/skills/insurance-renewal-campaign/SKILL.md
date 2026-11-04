---
name: insurance-renewal-campaign
description: Runs an insurance renewal pipeline for brokers and agents at 60, 30, 14 and 7 days before expiry. Schedules each policy's next touch, drafts needs-change prompts and document requests, sets the email, call and SMS cadence, records instructions to renew, change or lapse, and tracks every step in the CRM. Keeps strictly to factual messages and routes any "should I" question to the licensee's authorised people, so it never gives financial product advice. Covers opt-outs, the Spam Act, Do Not Call and calling hours. Use when a broker says "work this month's renewals", "who's expiring in the next 60 days", "chase renewal documents", "draft the renewal reminders" or "set up the renewal cadence". Works with any broking system export, CRM or spreadsheet; uses Fulcrum CRM and Lyre when connected.
---

# Run the insurance renewal pipeline

Keeps every renewal moving from 60 days out to written instructions, without lapses caused by silence and without the agent straying into advice. The endpoint is an up-to-date pipeline, approved and logged client touches, and a recorded instruction for every policy before expiry or a clear escalation where there is none.

## When to use

- Monthly or weekly renewal runs from a broking system or CRM export.
- Drafting renewal emails, SMS and call scripts for the licensee's approval.
- Chasing documents and instructions as expiry approaches.
- Not for: claims handling, quoting new business, or recommending cover. Not for one-off client follow-ups (`fulcrum-crm-follow-up`), reviewing a renewal call after the fact (`fulcrum-call-review`), or configuring a voice agent (`fulcrum-voice-agent-setup`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Policy list: policy number, client, class, insurer, expiry, status, account manager | Broking system export, CRM | Ask for it; do not work from memory |
| Contact preferences, opt-outs and the do-not-contact list | CRM, previous replies | Treat the channel as unavailable until confirmed |
| Licensee-approved templates, general advice warning wording, disclosure duty wording | Licensee compliance | Use the drafts in the reference marked "for licensee approval"; send nothing until approved |
| Who the authorised person is for advice questions, per client | Licensee or account manager | Ask; route to the account manager meanwhile |
| Insurer renewal terms and documents (schedule, PDS, TMD) | Insurer, broking system | Do not describe terms you have not seen |
| The licensee's position on Do Not Call and consent for renewal calls | Licensee compliance | Ask before the first calling run |

## Procedure

1. **Build the pipeline.** Load the policies into the tracker shape in [assets/renewal-tracker.csv](assets/renewal-tracker.csv) and run:

   ```bash
   python3 scripts/renewal_stage.py --policies renewals.csv --date <YYYY-MM-DD>
   ```

   It places each policy at upcoming, D-60, D-30, D-14, D-7 or expired, applies minimum gaps between touches, respects channel opt-outs and drops policies that already have instructions. Without the script, apply the same bands by hand.
2. **Triage before any contact.** Pull out and hand to the account manager first: expired or D-7 policies without instructions, declined or significantly changed insurer terms, open claims, complaints, and clients flagged as vulnerable or in hardship. These do not get templated messages.
3. **Prepare each touch** from [references/cadence-and-templates.md](references/cadence-and-templates.md): the D-60 email with the needs-change prompts for the client's classes and a document request; the D-30 call; the D-14 SMS; the D-7 call and SMS. Personalise only with facts from the record. Ask factual questions about changes; never suggest a cover level, sum insured or product.
4. **Check the advice boundary** in every draft against [references/advice-boundary.md](references/advice-boundary.md). Remove any sentence that recommends, compares or reassures about cover. If a sentence might be general advice, it needs the licensee's general advice warning and the authorised person's approval, or it goes.
5. **Check permission to contact.** For each recipient and channel: no opt-out, not on the do-not-contact list, and, for calls the licensee treats as telemarketing, the number has been washed against the Do Not Call Register by the user or their access seeker unless consent or an exemption applies. Calls only in the permitted hours in the client's local time.
6. **Approval gate.** Show the batch: each recipient, channel, exact message or call script, attachments, the sending account or number, and the policy it relates to. Wait for an explicit yes from the user. Approval covers that batch only. A template approved by the licensee still needs the batch approved.
7. **Send or call, then verify.** Send within the approved batch. Check delivery in sent items or message history and call outcomes in call history; a completed call does not prove an SMS went. After a timeout or unclear status, check before retrying.
8. **Handle replies the same day.** Instruction to renew, change or lapse: confirm it back in writing (gate), update the record and stop the cadence. Changes reported: record them in the client's words and pass them to the account manager for the insurer. "Should I" questions, claims, complaints, hardship or vulnerability: route to the authorised person with the thread, and pause automated touches. Opt-outs: record them at once and honour them within 5 working days at most; an opt-out from marketing does not stop factual notices the licensee must give.
9. **Log everything in the CRM.** Each touch as an activity with outcome; follow-up tasks with owner and due date; the renewal deal or record moved to the stage that reflects an observable fact (terms sent, instructions received, renewed, lapsed).
10. **Weekly pipeline report** to the account managers: counts by stage, policies without instructions inside 14 days, documents outstanding, premium changes above the licensee's threshold, opt-outs and complaints.

## Output

- Pipeline table by stage with the next action per policy.
- Approved message batches and call scripts, with send and delivery status.
- Updated CRM records and tasks.
- Weekly report and an escalation list for the account managers.

## Check before you finish

- [ ] No message recommends, compares or reassures about cover; every "should I" question went to an authorised person.
- [ ] Every contact respected opt-outs, the do-not-contact list, Do Not Call washing by the user where it applies, and calling hours.
- [ ] Every policy inside 7 days has written instructions or an escalation to a named person.
- [ ] Each instruction is confirmed in writing and recorded.
- [ ] Report sent, drafted, pending and failed separately.

## Guardrails

Compliance checklist:

- [ ] Advice: the skill gives no financial product advice; the licensee's authorised people do. General advice, if used at all, carries the licensee's warning.
- [ ] Anti-hawking: no offers of other products in renewal contact; new needs go to the authorised person.
- [ ] Spam Act: renewal invitations by email or SMS identify the brokerage, are sent with consent (express or inferred from the existing relationship), and any marketing content carries a working unsubscribe honoured within 5 working days.
- [ ] Do Not Call Register: the user washes call lists themselves or through an access seeker where the calls are telemarketing, unless consent or an exemption applies.
- [ ] Calling hours: weekdays 09:00 to 20:00 and Saturday 09:00 to 17:00 in the client's local time; no Sundays or national public holidays.
- [ ] Call recording: disclose recording at the start of the call; consent rules vary by state.
- [ ] Privacy Act and APPs: use claims and personal details only for the renewal; health information (for example on sickness and accident cover) only as the policy requires.

This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum CRM** can run a separate pipeline for renewals alongside new business; deal cards show time in stage (amber after 3 days, red after 7). Custom fields such as a renewal date can drive active lists that refresh every 15 minutes, and tasks can be assigned to a person, a team or an AI agent. Email campaigns include an unsubscribe link and stop sending to anyone who unsubscribes; AI assistants cannot send bulk email.
- **Lyre** can run call or SMS campaigns with an objective, within the organisation's calling window, checking each dial against the organisation's own do-not-contact list; an SMS reply of STOP or UNSUBSCRIBE stops further SMS. Lyre does not wash numbers against the Do Not Call Register. AI and recording disclosure can play at the start of every call.

## Learn more

- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
- [Calling compliance in Lyre](https://fulcrumcortex.github.io/documentation/lyre/compliance/)
- [ACMA rules for AI outbound calls in Australia](https://fulcrumcortex.com/blog/acma-compliant-ai-calling-australia)
