---
name: vendor-report
description: "Writes a weekly vendor campaign report for a property on the market: enquiry and inspection numbers with week-on-week change, attendee feedback themes, price feedback in buyers' own words, comparable sales the agent supplies, an honest market read and specific recommendations, ready for the agent to review and send. Use when an agent asks for 'the vendor report', 'weekly campaign update', 'what do I tell the vendor this week', 'vendor feedback report' or 'campaign summary for [address]'. Works with portal statistics, open-home notes and CRM data the agent provides; uses Fulcrum CRM records when connected. Never invents comparables or price figures."
---

# Write the weekly vendor report

Turns a week of campaign activity into a report a vendor can trust: what happened, what buyers said, what the numbers mean, and what the agent recommends next. The endpoint is a reviewed report draft, and, after approval, a sent email from the agent's mailbox.

## When to use

- Weekly during a sale campaign, usually the day after the main open home.
- Before a price or method conversation, when the agent needs the evidence in one place.
- Not for: same-day buyer follow-ups after an inspection (use `open-home-follow-up`, which produces this skill's feedback input); appraisals or listing presentations; reviewing a contract (use `fulcrum-document-review`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Property, vendor name, campaign week number, method (auction, private treaty, expressions of interest), key dates | Listing record, agent | Ask once. |
| Enquiries this week and last: portal, phone, email, walk-in | Portal statistics, CRM, call log | Report what is available and say which sources are missing. Never estimate. |
| Inspections: groups through, private appointments, second inspections | Open-home registers, `open-home-follow-up` feedback block | Ask the agent for counts. |
| Contract and disclosure requests, offers received | Agent, CRM | Ask. Offers are reported only as the agent instructs. |
| Buyer feedback and price reactions | Feedback block, agent notes | Report "no feedback recorded" rather than filling the gap. |
| Comparable sales and current competing listings | Supplied by the agent | Leave the section with "Comparables to be supplied by [agent]". Never source or invent them. |
| Price guide as published, and any change this week | Agent | Ask. |
| Last week's report | Previous email or file | Treat this as week 1 and say so. |

## Procedure

1. **Assemble the numbers** into the week-on-week table in [assets/vendor-report-template.md](assets/vendor-report-template.md). Show this week, last week and campaign total. Label any number the agent gave verbally as "agent count".
2. **Group feedback into themes.** Count how many groups raised each theme (for example "kitchen dated: 6 of 14 groups"). List at most five themes. Separate likes from objections. Quote two or three short buyer phrases verbatim; do not identify buyers by name.
3. **Price feedback.** Summarise reactions in words and as a distribution: "below guide", "around guide", "above guide", "no comment". Never turn reactions into a single number or a predicted sale price.
4. **Comparables.** Present only the sales and listings the agent supplied, with address, sale date, price, and one line on how each compares (land, condition, position). If a comparable lacks a date or price, show it as incomplete.
5. **Market read.** Read [references/market-read-guide.md](references/market-read-guide.md) and apply its decision rules to the numbers. Write three to five sentences that state what the evidence suggests, including uncomfortable news, without blaming the vendor. Separate fact ("14 groups, down from 22") from interpretation ("interest is easing as the campaign ages").
6. **Recommendations.** Give two to four specific actions with a reason and an owner, chosen from the guide's decision table (for example "adjust the price guide", "add a twilight inspection", "address the kitchen objection with a quote from a tradesperson"). Any price guide change is a recommendation for the vendor to decide, never a decision.
7. **Next week.** List confirmed inspections, marketing actions and dates.
8. **Self-check** against the checklist below, then hand the draft to the agent with a short note of gaps and assumptions.
9. **Approval gate.** If the agent asks you to send it, show the final email: recipients (vendor addresses as on file), sending mailbox, subject, body and attachments. Wait for an explicit yes. After sending, confirm it is in sent items. After a timeout, check sent items before trying again.

## Output

The filled template from [assets/vendor-report-template.md](assets/vendor-report-template.md), plus a cover note for the agent listing: missing data, figures marked "agent count", and the recommendations that need a vendor decision.

## Check before you finish

- [ ] Every number traces to a source or is labelled "agent count"; nothing is estimated.
- [ ] Comparables are only those the agent supplied, each with date and price or marked incomplete.
- [ ] No buyer is named, and no buyer's offer is disclosed unless the agent instructed it.
- [ ] The market read contains at least one sentence a vendor might not want to hear, if the evidence supports it, and no unsupported optimism.
- [ ] Recommendations each have a reason and an owner.
- [ ] Report state is clear: draft for review, approved, or sent (with sent-item check).

## Guardrails

- The report is factual campaign reporting, not a valuation. Do not state what the property is "worth".
- Keep offers and buyer identities confidential to the extent the agent's process and state law require; when in doubt, leave them out and ask.
- Any statement about price must be consistent with the published guide and the agent's estimate; underquoting rules apply in several states.
- Do not copy portal statistics screenshots into the report if the agent has not supplied them; describe the numbers instead.

## With Fulcrum

- Pull enquiry and inspection history from contacts tagged with the listing, and log the sent report as an activity on the vendor's contact. See [Contacts and companies](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/) and [Activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- Create the agent's follow-up tasks from the recommendations with owners and due dates.
- Fulcrum CRM has a Real Estate industry module; availability varies by account (check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules). This skill works from whatever data the agent provides.

## Learn more

- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
- [AI for real estate agencies in Australia](https://fulcrumcortex.com/blog/ai-for-real-estate-agencies-australia)
