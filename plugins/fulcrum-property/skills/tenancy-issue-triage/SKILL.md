---
name: tenancy-issue-triage
description: "Triages a property management inbox into a ranked work queue: maintenance requests sorted urgent or routine, rent arrears at the right contact stage, strata, utility and insurance matters, and owner approvals, each with an owner, a deadline and a draft reply. Use when a property manager says 'triage the PM inbox', 'what needs doing today on the rent roll', 'sort the maintenance requests', 'who is behind on rent', 'chase arrears', or 'which owner approvals are waiting'. Applies an urgent-repairs checklist (the user confirms their state's rules) and staged arrears contact, and waits for approval before contacting tenants, owners or trades. Works with any mailbox, tenancy software export or pasted messages; uses Fulcrum Mail, CRM and Lyre when connected."
---

# Triage the property management inbox

Turns a mixed inbox of tenant, owner, trade, strata and insurer messages into a queue a property manager can work from the top: what is urgent, who owns it, when it is due, and a draft for each reply. The endpoint is an approved set of replies, work orders and owner requests, with nothing sent before the property manager says yes.

## When to use

- Start of day, after a weekend, or after leave, on a property management mailbox or a tenancy software export.
- When arrears reports land and staged contact needs to go out.
- Not for: general business inbox triage (use `fulcrum-inbox-triage`); checking whether rent billed matches the lease (use `lease-billing-check`); sales enquiries and open homes (use `open-home-follow-up`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Messages: email, SMS, portal requests, voicemail transcripts | PM mailbox, tenancy software, phone system | Work from what is provided; list sources not checked. |
| Property and tenancy details: address, tenant, owner, managing PM | Tenancy software, CRM | Ask once; queue items without a matched property as "unmatched". |
| State or territory of each property | Address | Infer from the address. Urgent repair rules depend on it. |
| Rent ledger or arrears report: days in arrears, amount, payment history | Tenancy software export | Do not stage arrears from emails alone; ask for the report. |
| Owner instructions: approval limit for repairs, preferred trades, insurer | Management agreement, owner notes | Treat every repair as needing owner approval except urgent repairs where the agreement allows the PM to act. |
| Approved trades list with after-hours contacts | Agency records | Draft the work order without a trade and flag it. |

## Procedure

1. **Collect and de-duplicate.** Group messages by property and thread. A tenant who emailed, texted and called about one leak is one item.
2. **Classify each item** into one type: Maintenance, Arrears, Strata, Utility, Insurance, Owner approval, Lease or notice, Other. If an item spans two (storm damage is Maintenance and Insurance), give it one primary type and link the other.
3. **Maintenance: urgent or routine.** Apply the [urgent repairs checklist](references/urgent-repairs-checklist.md). Read it before deciding. Any risk to safety, security or an essential service is urgent until a person confirms otherwise. Tell the user to confirm their state's definitions, response times and tenant spending limits; the checklist is a starting point, not the state's list.
4. **Arrears: stage the contact.** Read [references/arrears-stages.md](references/arrears-stages.md) and place each tenant at a stage from the ledger, not from a guess. Check for a payment in transit, a receipting error or an agreed payment plan before any message. Flag hardship, family violence or vulnerability for the PM to handle personally.
5. **Strata, utility, insurance and owner approvals.** Use the playbooks in [references/issue-playbooks.md](references/issue-playbooks.md) to set the owner, deadline and the next document needed.
6. **Set owner and deadline** for every item. Deadlines come from the rule that applies: urgent repairs same day, statutory notice dates from the state's rules, insurer claim windows from the policy, strata meeting dates from the notice. If no rule applies, use the agency's service standard (default: reply within one business day).
7. **Rank the queue**: urgent maintenance and safety first, then anything with a legal or statutory deadline in the next 3 business days, then arrears stages due today, then owner approvals blocking a repair, then the rest by deadline.
8. **Draft replies and work orders.** Tenant acknowledgements say what happens next and when; work orders give the trade the address, access arrangements, the issue, photos if supplied, the approval limit and the owner reference. Owner requests state the issue, the quotes, the recommendation and the approval needed.
9. **Approval gate.** Present the batch: for each item, the recipient, the channel and sending account, the exact text and any attachments. Wait for an explicit yes, per batch or per item. Arrears notices, breach notices and anything quoting legislation need the PM's individual approval, never a batch yes. After an uncertain send, check sent items or the SMS log before resending.
10. **Record.** Log each sent message and work order against the property and tenant, and create tasks for every promised follow-up (trade attendance confirmed, owner reply chased).

## Output

A queue table, ranked:

| Rank | Property | Type | Summary | Urgency | Owner | Deadline | Next action | Draft ready |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Then: drafts grouped by recipient type (tenants, owners, trades, strata or insurers); items needing the PM's judgement; unmatched items; sources not checked; status of sent, drafted, pending approval and failed.

## Check before you finish

- [ ] Every message is in exactly one queue item, or listed as unmatched.
- [ ] Every urgent item has a same-day owner and a named trade or a flag that none is available.
- [ ] Arrears stages come from the ledger, and payment plans and receipting were checked first.
- [ ] No statutory notice or legislation-based message is in a batch approval.
- [ ] Sent, drafted, pending and failed are reported separately.

## Guardrails

- Never issue a breach notice, termination notice or tribunal application. Draft for the PM, who checks the state's form and timing.
- Never tell a tenant they may withhold rent or arrange their own repairs; point them to the PM, who knows the state's rules.
- Keep tenants' financial, health and family information to the people who need it. Do not copy it to owners or trades.
- Do not give trades more access information than the job needs; share key codes only for the job and the day.
- Payment reminders about an existing tenancy are not marketing, but still identify the agency and the sender in every message.

This is a practical checklist, not legal advice.

## With Fulcrum

- Read and draft replies in [Fulcrum Mail](https://fulcrumcortex.github.io/documentation/fulcrum-mail/mail-basics/), log each contact and create follow-up tasks assigned to a person, team or AI agent, as in [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Lyre can send SMS and place calls for approved reminders where the agent's tools and number allow it; Lyre checks your organisation's own do-not-contact list and calling hours. See [SMS in Lyre](https://fulcrumcortex.github.io/documentation/lyre/sms-contacts-and-connections/).
- Fulcrum CRM has a Property Management industry module; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill does not depend on it.

## Learn more

- [AI for real estate agencies in Australia](https://fulcrumcortex.com/blog/ai-for-real-estate-agencies-australia)
- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
