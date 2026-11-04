---
name: ndis-client-onboarding
description: Prepares a new-participant onboarding pack for an NDIS provider from the plan and intake details the provider supplies, including a draft service agreement, a schedule of supports whose item numbers and prices the user verifies against the current NDIS Support Catalogue and Pricing Arrangements, consent forms, a note on how the funding management type (NDIA-managed, plan-managed or self-managed) changes invoicing, and a missing-information checklist. Use when someone says "new NDIS client", "onboard a participant", "prepare a service agreement", "schedule of supports", "intake pack", "client pack" or "consent forms". Works from pasted or uploaded documents with any files or CRM; uses Fulcrum Docs, Drive and Fulcrum CRM when connected. Nothing goes to a participant, nominee or plan manager without approval.
---

# Prepare an NDIS new-participant pack

Turns a participant's plan and intake notes into a ready-to-review onboarding pack for a sole practitioner or small NDIS provider: service agreement, schedule of supports, consent forms and a list of what is still missing. The endpoint is a reviewed draft pack and, only after explicit approval, a send to the participant or their representative.

## When to use

- A new participant has accepted a place and the provider needs the agreement paperwork.
- A plan has been reassessed or renewed and the agreement and schedule must be redone.
- The participant changes funding management type, for example from self-managed to plan-managed.
- Not for: writing session notes (use `progress-notes`), checking what has been billed (use `ndis-billing-check`), or a general contract review (use `fulcrum-document-review`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Plan details: start and end dates, funding management type per budget, relevant goals | The plan or plan extract the participant shares | Ask once. Without plan dates and funding type, stop at a draft marked "not ready". |
| Intake: who signs (participant, nominee, guardian or parent), contact preferences, supports requested, frequency | Intake form, referral, first call notes | Add to the missing-information checklist |
| Provider details: legal name, ABN, registration status and number if registered, cancellation policy, complaints process | Provider's own template or settings | Ask once; never invent an ABN or registration number |
| Support items and agreed prices | The current NDIS Support Catalogue and Pricing Arrangements, checked by the user | Leave `[VERIFY: support item]` and `[VERIFY: price]` placeholders |
| Plan manager name and invoice address (plan-managed only) | The participant or the plan | Checklist item; do not guess from a web search |

Collect the minimum. Health and disability information is sensitive information under the Privacy Act. Take only what the agreement needs: plan dates, relevant goals, funding type and the budget the participant chooses to allocate. A diagnosis belongs in the pack only if the support cannot be described without it.

## Procedure

1. **Confirm the parties and authority.** Record who the participant is (use an internal reference such as `P-0142` in working files), who has legal authority to sign, and how they want to receive documents. If a nominee, guardian or parent signs, note the evidence of authority on the checklist. An adult participant who can consent signs for themselves, even when a family member made the enquiry.
2. **Read the plan and extract only what is needed.** Plan start and end dates, the funding management type for each relevant budget, the goals the supports will address, and any stated supports. Plans can be mixed: Capacity Building may be plan-managed while Core is NDIA-managed. Record each budget's type separately.
3. **Choose the invoicing route per budget.** Use [funding types and invoicing](references/funding-types-and-invoicing.md). Key decisions: an NDIA-managed budget needs a registered provider and is claimed through the NDIA provider portal; plan-managed means invoices to the plan manager, with price limits still applying; self-managed means invoices to the participant or nominee. If the provider is unregistered and the budget is NDIA-managed, stop and tell the user: the provider cannot be paid from that budget.
4. **Build the schedule of supports** in [assets/schedule-of-supports.csv](assets/schedule-of-supports.csv). One row per support item: item number and name copied exactly from the current Support Catalogue, unit, agreed price, frequency, quantity, total and budget. Rules:
   - Never invent an item number or a price. If the user has not confirmed one, keep the `[VERIFY]` placeholder and list it on the checklist.
   - For NDIA-managed and plan-managed budgets, the agreed price must not exceed the current price limit for the participant's location. Note that price limits are usually reviewed from 1 July each year and say in the agreement how a change is handled.
   - Add provider travel, non-face-to-face time, report writing or short-notice cancellation lines only if the participant agrees and the current Pricing Arrangements allow them for that support.
   - Total the schedule. If it exceeds the funds the participant has chosen to allocate, flag it and propose a lower frequency. Do not quietly trim.
5. **Draft the service agreement** from [assets/service-agreement-draft.md](assets/service-agreement-draft.md). Plain English, short sentences, and an offer of an Easy Read version or interpreter if the intake suggests it. Fill only what the inputs support; leave visible placeholders for the rest. See [pack contents](references/pack-contents.md) for the clauses that must be present.
6. **Prepare consent forms** from [assets/consent-form.md](assets/consent-form.md). Separate, specific consents that can be withdrawn: collecting and storing information, sharing with named people (plan manager, support coordinator, GP, school), reminders by SMS or email, photos or recordings (optional and separate), and use of transcription or AI tools to prepare notes if the provider uses them. Never bundle optional consents with the service itself.
7. **Complete the missing-information checklist** in [assets/missing-information-checklist.md](assets/missing-information-checklist.md). Every placeholder in the pack must appear on it with who will supply it.
8. **Self-check the pack.** Dates inside the plan period; funding type stated per budget; schedule total matches the agreement; every `[VERIFY]` listed; the participant's name, NDIS number and date of birth appear only where the document needs them; no other participant's details copied from a previous pack.
9. **Approval gate.** Show the user the full pack, the exact recipients (participant, nominee or guardian; never the plan manager or support coordinator unless the participant has agreed), the sending account and the method (a restricted share link or a password-protected attachment, not an open link). Wait for an explicit yes for this pack. A draft is not approval.
10. **Send and record.** After approval, send once. If the result is unclear, check sent items before resending. Record the agreement status (sent, signed, declined), plan end date and a review reminder about 8 weeks before the plan ends.

## Output

1. A summary table: participant reference, signer, plan dates, funding type per budget, invoicing route, schedule total, status (draft, ready for review, sent, signed).
2. The draft service agreement, schedule of supports CSV and consent forms.
3. The missing-information checklist, grouped by who must supply each item.
4. A short "verify before sending" list of every item number, price and clause the user must confirm.

## Check before you finish

- [ ] No support item number, price, ABN or registration number was invented; each one is confirmed or still marked `[VERIFY]`.
- [ ] Funding type and invoicing route are stated for every budget used.
- [ ] Optional consents are separate and unticked by default.
- [ ] Nothing was sent, shared or uploaded outside the provider's own storage without approval.
- [ ] Report drafted, approved, sent and signed as separate states.

## Guardrails

- Not legal, financial or clinical advice. The provider is responsible for the agreement; suggest a review by their adviser for anything unusual.
- Never paste plan contents or participant details into a public tool, search engine or chat outside the provider's systems.
- Use person-first, respectful language throughout. Describe supports and goals in the participant's own words where the plan or intake gives them.
- A participant can choose and change providers. Do not write lock-in terms, exit fees or notice periods longer than the provider's policy states.
- Compliance checklist: [pack contents](references/pack-contents.md) holds the NDIS Practice Standards, Code of Conduct and Privacy Act checks for this pack. This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum Docs**: draft the agreement and consent forms as documents, share with colleagues as Commenter for review, and check print preview before exporting. See [Fulcrum Docs](https://fulcrumcortex.github.io/documentation/docs/).
- **Fulcrum Drive**: keep packs in a company drive with restricted membership. Use an external link with an expiry only if the workspace allows external sharing, and revoke it once the signed copy is back. See [Drive](https://fulcrumcortex.github.io/documentation/drive/).
- **Fulcrum CRM**: store the participant as a contact with [custom fields](https://fulcrumcortex.github.io/documentation/crm/custom-fields/) such as plan end date (Date Picker) and funding type (Dropdown Menu), log the pack as an activity and create a task for the plan review. Prepare invoices as drafts under Sales → Invoices; Finalize & Send is an outward action.
- Fulcrum CRM also has a Workforce module for rostering, timesheets and payroll workflows. Availability varies by account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Fulcrum Docs: create and share documents](https://fulcrumcortex.github.io/documentation/docs/)
- [Custom fields in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/custom-fields/)
- [Fulcrum Drive: files and sharing](https://fulcrumcortex.github.io/documentation/drive/)
