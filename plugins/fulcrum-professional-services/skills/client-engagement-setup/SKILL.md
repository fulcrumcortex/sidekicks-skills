---
name: client-engagement-setup
description: Sets up a new professional services client engagement from won deal to first invoice. Drafts the engagement letter with in-scope and out-of-scope work, recommends a fee basis (fixed fee, time and materials, or retainer) using the firm's own rates, prompts the conflict check and any identification the firm requires, prepares the kickoff agenda and shared folder, hands the CRM deal over to a project, sets the time-tracking and billing cadence, and runs a weekly WIP and unbilled-time check. Use when a consultant, accountant, agency or adviser says "we won the work, set it up", "draft the engagement letter", "onboard this client", "fixed fee or hourly?", "set up the kickoff" or "check WIP and unbilled time". Works with any CRM, mail, calendar and file storage; uses Fulcrum CRM, Calendar and Drive when connected.
---

# Set up a client engagement and keep it billable

Turns a won opportunity into a properly documented engagement: scope and fees agreed in writing, risk checks done before work starts, the team set up, and time and billing that do not leak. The endpoint is a signed engagement letter, a project ready to work, and a weekly WIP report the engagement lead acts on.

## When to use

- A deal is won and the client needs onboarding.
- An engagement letter or scope of work needs drafting or tightening.
- The firm is choosing between fixed fee, time and materials, and a retainer.
- Weekly, to check unbilled time, budget burn and scope creep.
- Not for: winning the work or proposal follow-ups (`fulcrum-crm-follow-up`), detailed delivery planning (`fulcrum-project-planning`), meeting notes from the kickoff (`fulcrum-meeting-actions`), or legal review of the letter (`fulcrum-document-review` for an editorial check only).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Client legal entity, ABN, capacity (for example trustee), decision maker, billing contact | Proposal, CRM company record, ABN lookup by the user | Ask. Do not draft the letter to a trading name only. |
| Agreed scope, deliverables and dates | Proposal, sales notes, emails | Draft from what exists and list open scope questions |
| The firm's rate card, pricing policy and letter template | Firm's policies | Ask. Never invent a rate or fee. |
| Conflict check method and who clears conflicts | Firm's policy | Ask; do not start work until it is cleared |
| Identification or customer due diligence the firm requires | Firm's policy, AML/CTF program if the firm has one | Ask which applies |
| Team, engagement lead, time-recording and billing system | User | Ask once |

## Procedure

1. **Confirm the client.** Legal entity name, ABN, capacity and the person authorised to sign. Check the CRM for an existing company or contact before creating one; merge rather than duplicate.
2. **Conflict check prompt.** List the parties to search: the client, related entities, directors or principals, and known counterparties or competitors in the matter. Ask the user to run the firm's conflict search (or run it if the host provides the conflict register), and record the result, the date and who cleared it. A possible conflict goes to the person the firm designates; the agent never clears one.
3. **Identification and due diligence.** Ask what the firm requires for this client: for example tax practitioner client verification, an adviser licensee's client identification, or customer due diligence under an AML/CTF program if the firm provides services regulated under the AML/CTF Act. Request documents through the firm's secure channel; never ask for ID images in chat or ordinary email, and do not store them in the general project folder.
4. **Shape the scope.** Write deliverables as observable outputs with dates. Write an out-of-scope list from what the client might reasonably assume is included (extra review rounds, additional entities, implementation, travel). List the assumptions the fee depends on and the client's responsibilities.
5. **Recommend the fee basis** with the rules in [references/fee-basis-and-wip.md](references/fee-basis-and-wip.md). Price only from the firm's rate card or the fee the user gives. For T&M, set the estimate, whether it is a cap, and the notification point (default 80%). For a retainer, state inclusions, rollover and overage. Show the engagement lead the reasoning; they choose.
6. **Draft the engagement letter** from the firm's template, or [assets/engagement-letter-outline.md](assets/engagement-letter-outline.md) if there is none. Include the conflict-check statement, fees, change process, privacy and records, and the firm's own limitation-of-liability wording. Include a professional standards scheme statement only if the firm participates in one.
7. **Approval gate.** Before the letter is sent for signature, show the engagement lead the exact letter, the recipient (the authorised signatory), any copy recipients and the sending account. Wait for an explicit yes. Unless the firm's policy says otherwise, no billable work starts before the letter is accepted and identification is complete.
8. **Hand over from deal to project** once the letter is accepted: move the deal to the won stage (not before), record the signed letter's location, and create the project with the engagement lead, team, milestones and the first tasks. Copy the handover notes from sales: what the client cares about, sensitivities, promises made during the sale.
9. **Set up the shared folder.** Structure: `01 Engagement` (letter, scope changes), `02 Client inputs`, `03 Working`, `04 Deliverables`, `05 Correspondence`. Internal working papers and client-visible deliverables are kept apart. Share the client-visible folder only with named client contacts, with the narrowest role and an expiry on external links. ID documents stay in the firm's restricted location.
10. **Prepare the kickoff** from [assets/kickoff-agenda.md](assets/kickoff-agenda.md), with the information-request list attached. Propose two or three times from the calendars; inviting the client is an outward action and goes through the approval gate.
11. **Set time and billing.** Create the engagement code and phases in the time system, confirm the team records time daily, and set the billing cadence for the fee basis (see the reference). Diary the 80% budget check and the first invoice date.
12. **Weekly WIP check.** Export time entries and engagement settings to CSV and run:

    ```bash
    python3 scripts/wip_check.py --time time.csv --engagements engagements.csv --date <YYYY-MM-DD>
    ```

    It reports unbilled hours and value with 0–30, 31–60, 61–90 and 90+ day buckets, budget burn, retainer use and timesheet gaps, and flags overrun risk, caps reached and aged WIP (column templates: `assets/time-entries-template.csv` and `assets/engagements-template.csv`). Add scope-creep signals from recent emails and notes. Send each engagement lead their decisions: bill now, notify the client, raise a change request, or consider a write-off. Client notifications and change requests go through the approval gate.

## Output

- Conflict and identification record: what was checked, result, date, who cleared it.
- Engagement letter draft, then the approved and sent version.
- Project and folder set up, with handover notes and a kickoff invitation draft.
- Weekly WIP report with one decision per flagged engagement.

## Check before you finish

- [ ] The letter is addressed to the correct legal entity and authorised signatory.
- [ ] Every fee figure comes from the firm's rate card or the user; none is assumed.
- [ ] Conflict check and required identification are recorded before work starts.
- [ ] The deal moved to won only after acceptance; the project has an owner and first tasks.
- [ ] Report drafted, sent, signed, pending and failed separately.

## Guardrails

- Privacy Act and APPs checklist: collect only the personal information the engagement needs; tell the client how it is handled (the firm's privacy policy); keep ID documents and sensitive information in restricted storage; retain and destroy records according to the firm's policy and legal retention periods. This is a practical checklist, not legal advice.
- The agent does not provide the professional advice itself (tax, legal, financial product or accounting opinions) in the letter or kickoff; it records what the firm will provide.
- Never clear a conflict, waive identification or agree a fee on the firm's behalf.
- Marketing emails to the new client (newsletters, event invitations) need consent and a working unsubscribe under the Spam Act; engagement correspondence does not become marketing by adding offers.

## With Fulcrum

- **Fulcrum CRM** holds the company and contacts, the deal and its stage (every stage change is written to the timeline), dated tasks for the team or an AI agent, email templates with merge fields, and invoices as drafts until Finalize & Send. Its projects workspace holds the engagement's issues and milestones where the account has module access.
- **Fulcrum Calendar** creates the kickoff event with guests and a Fulcrum meeting link; guests receive an invitation email.
- **Fulcrum Drive** holds the engagement folders, with company drives, Viewer, Commenter and Editor roles, and external links with expiry and download controls.
- A Consultation industry module may be available in Fulcrum CRM depending on the account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
- [Projects, boards, issues and sprints](https://fulcrumcortex.github.io/documentation/crm/projects-and-issues/)
- [Files, folders and sharing in Fulcrum Drive](https://fulcrumcortex.github.io/documentation/drive/)
