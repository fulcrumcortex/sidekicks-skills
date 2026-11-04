---
name: recruitment-pipeline
description: Runs a recruitment agency's two pipelines together, clients and jobs on one side and candidates on the other. Covers job intake with essential and desirable criteria, sourcing notes, screening call summaries, an evidence-based shortlist against the criteria, interview scheduling, reference checks with consent, the offer stage and placement, with candidate privacy (collection notice, consent log, retention) built in. Assesses only against job criteria, never protected attributes, and never sends candidate details to a client without the candidate's consent for that role. Use when a recruiter asks to "take a job brief", "write up the screening call", "build the shortlist", "send the client our candidates", "book interviews", "do reference checks" or "where are we on this role". Works with any ATS, CRM, mail and calendar; uses Fulcrum CRM, Calendar and Lyre when connected.
---

# Run the client and candidate pipelines

Keeps each role and each candidate moving with evidence, consent and a clear next step, so the client gets a defensible shortlist and candidates are treated fairly and lawfully. The endpoint is an up-to-date pair of pipelines, approved outgoing messages, and a placement (or a closed role) with every consent and decision recorded.

## When to use

- A new role comes in, or a client brief needs turning into assessable criteria.
- After screening calls, to summarise evidence and update the candidate pipeline.
- Before presenting candidates, booking interviews, checking references or managing an offer.
- A weekly view of both pipelines: roles without candidates, candidates without next steps.
- Not for: bulk job-alert or marketing campaigns (`fulcrum-campaign-brief`), reviewing a recorded call's quality (`fulcrum-call-review`), or inbox sorting (`fulcrum-inbox-triage`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Signed terms of business with the client | Contract records | Take the brief, but present no candidates until signed |
| Job brief: duties, essential and desirable criteria, salary, location, process | Hiring manager call, position description | Use [assets/job-intake-template.md](assets/job-intake-template.md) to ask for the gaps |
| Candidate CVs, sourcing source, screening notes or call transcript | ATS, inbox, call notes | Summarise only what exists; mark gaps "Unknown" |
| Consent records per candidate, role and client | ATS or CRM consent log | Treat as no consent |
| The agency's privacy policy link and retention period | Agency policy | Ask before the first collection notice |
| Calendars for the hiring panel | Client, host calendar | Ask for windows; never invent availability |

## Procedure

**Client and job pipeline**

1. **Take the intake** with [assets/job-intake-template.md](assets/job-intake-template.md). Turn every "must have" into an essential criterion with how it will be evidenced. Separate desirable criteria. Record inherent requirements (licences, checks required by law, physical requirements, hours). Confirm terms of business are signed.
2. **Screen the brief for bias.** Any requirement that refers to, or stands in for, a protected attribute (age, sex, family status, origin and the others in [references/bias-guardrails.md](references/bias-guardrails.md)) is declined with the suggested response and recorded. Escalate if the client insists.
3. **Move the job through stages** that reflect observable facts: brief taken, terms signed, sourcing, shortlist sent, interviewing, offer, placed, closed (with reason).

**Candidate pipeline**

4. **Source and record.** For each candidate: source (job board, referral, database, direct approach), date, and the collection notice given at first contact (template in [references/privacy-and-consent.md](references/privacy-and-consent.md)). Approach notes record skills and experience only.
5. **Summarise screening calls** with [assets/screening-summary-template.md](assets/screening-summary-template.md): right to work for this role, availability and notice, salary expectation, interest, other processes, adjustments needed, and evidence against each criterion as a quote or CV line. Rate Met, Partly, Not met or Unknown. Leave out anything about protected attributes the candidate mentioned, unless they asked for an adjustment; then record only the adjustment.
6. **Build the shortlist** with [assets/shortlist-matrix-template.md](assets/shortlist-matrix-template.md). Essential criteria decide who is presented; desirable ones order them. Every rating cites evidence. Unknown is not Not met: ask, then rate. Run the pattern check in the bias reference before the shortlist goes anywhere.
7. **Get consent to present.** For each shortlisted candidate, ask: "May we put you forward to {client} for the {role} role?" Record the answer, date, channel and words in the consent log. Check they have not already been put forward for this role by another agency. No consent, no submission.
8. **Approval gate: candidate details to a client.** Before any CV, profile or candidate name goes to a client, show: each candidate, the consent record for this role and client, the exact content (photo, date of birth, home address and referee details removed), the client recipients and the sending account. Wait for an explicit yes. Do not send if any consent is missing or older than this role.
9. **Schedule interviews.** Offer slots from the panel's real availability. Ask every candidate the same question about adjustments. Confirm in writing with time zone, format, address or link, panel names and what to bring. Invitations and confirmations go through the approval gate.
10. **Reference checks.** Only referees the candidate nominated, after consent, and never a current employer without separate explicit consent. Ask the same job-related questions for each candidate; record answers close to verbatim; note how the referee knows the candidate. Do not ask about health, family or other protected attributes.
11. **Offer stage.** Record the offer exactly as the client approved it (salary, super, start date, conditions). Relay it to the candidate (gate), track acceptance, resignation and any counter-offer, and confirm the start. Check that conditions such as a police check have consent and are required for the role.
12. **Placement and close.** Mark placed with start date and the guarantee period per terms of business; raise the invoice draft for the user's approval. Tell every unsuccessful candidate the outcome, with feedback based on the criteria. Close the role with a reason if it ends without a placement.
13. **Retention.** Set a review date on each candidate record per the agency's policy. List records past review for a person to decide; never delete them yourself.

## Output

- Job intake record and the job's stage.
- Screening summaries and a shortlist matrix with evidence and consent dates.
- Approved messages to clients and candidates, with delivery checked.
- A weekly two-pipeline view: roles by stage with days in stage, candidates by stage, missing consents, overdue feedback, records past retention review.

## Check before you finish

- [ ] Every assessment is against the intake criteria with cited evidence; no protected attribute or proxy was used.
- [ ] Every candidate presented has consent recorded for this role and this client.
- [ ] Client copies contain no photo, date of birth, home address or referee details.
- [ ] Reference checks were with nominated referees after consent.
- [ ] Report sent, drafted, pending and failed separately.

## Guardrails

- Anti-discrimination: assess only against job criteria and inherent requirements; see [references/bias-guardrails.md](references/bias-guardrails.md).
- Privacy Act and APPs: collection notice at first contact; collect only what the role needs; sensitive information only with consent and when necessary; consent per role and client before disclosure; retention review and disposal per policy; access and correction requests routed the same day. See [references/privacy-and-consent.md](references/privacy-and-consent.md).
- Spam Act: job alerts and marketing to candidates or clients need consent, identify the agency, and carry a working unsubscribe honoured within 5 working days.
- Do Not Call Register: calls that offer the agency's services to prospective clients are telemarketing; the user washes those numbers themselves or through an access seeker, unless consent or an exemption applies. Calling hours apply; disclose call recording.
- Labour hire: if the agency supplies workers as labour hire in a state or territory with a licensing scheme, check the licence before placing.

This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum CRM** can run separate pipelines, for example one for client roles and one for candidates, with deal cards showing time in stage (amber after 3 days, red after 7) and every stage change written to the contact timeline. Custom fields (for example notice period or consent date) can filter active lists; tasks can be assigned to a person, team or AI agent.
- **Fulcrum Calendar** sends interview invitations to guests, with a Fulcrum meeting link when chosen; booking pages let candidates pick a time themselves and reschedule through their confirmation link.
- **Lyre** can place screening or reference calls with an objective listing the information to collect; calls are recorded and transcribed in call history, AI and recording disclosure can play at the start, and outbound calls respect the organisation's do-not-contact list and calling window.

## Learn more

- [Deals and pipelines in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/deals-and-pipelines/)
- [How guests book, and how to manage bookings](https://fulcrumcortex.github.io/documentation/calendar/manage-bookings/)
- [The Privacy Act and AI in 2026](https://fulcrumcortex.com/blog/privacy-act-ai-australia)
