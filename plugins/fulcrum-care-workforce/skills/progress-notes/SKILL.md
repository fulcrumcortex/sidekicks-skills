---
name: progress-notes
description: Turns voice-note transcripts, dictation or rough jottings into structured, objective progress or case notes for NDIS, disability support, allied health and community care work, using SOAP, goal-linked or shift-note format tied to the participant's plan goals. Separates what was observed from what was reported and from interpretation, flags anything that may need incident reporting, records billable times accurately and never adds content that is not in the source. Use when someone says "write up my session", "turn this voice note into a progress note", "case note", "shift note", "SOAP note", "file note" or "notes for today's clients". Works from pasted text or any files; uses Fulcrum CRM activities when connected.
---

# Write a progress note from voice or rough notes

Converts what a practitioner or support worker said or scribbled after a session into a clear, factual note that belongs in the participant's file. The endpoint is a draft the author confirms; saving it is internal, and sharing it with anyone outside the provider needs approval.

## When to use

- After a therapy session, support shift, home visit, phone call or team meeting about a participant.
- A batch of voice notes from the day needs writing up before billing.
- A late entry must be added to a file.
- Not for: writing the incident report itself (follow the provider's incident management process), reports to the NDIA or plan reviews (use `fulcrum-document-review` on the draft), or billing (use `ndis-billing-check`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The source: transcript, dictation or notes | Voice note, phone dictation, paper notes photo | Nothing to write; ask for it |
| Participant reference, date, start and end time, location, service type | Calendar entry or booking | Ask once; otherwise write `[not stated]`. Never estimate times. |
| Note format the provider uses | Provider's template or previous notes | Default: SOAP for therapy, goal-linked for capacity building, shift note for support work |
| The participant's plan goals relevant to this service | Service agreement or client file | Write the note without goal links and say so |
| Author name and role | The person asking | Ask once |

Collect the minimum. Health and disability information is sensitive information under the Privacy Act. Never paste a transcript or participant details into a public tool or a chat outside the provider's systems.

## Procedure

1. **Fix the facts of the session.** Participant reference, date, actual start and end time, location or telehealth, who was present (by role, for example "mother", "support worker"), and the service type. Use the times the author gives, not the booked times, and flag a difference greater than 10 minutes so billing uses the right one.
2. **Clean the source without changing meaning.** Remove filler and false starts. Mark any word you cannot make out as `[unclear: "..."]`. Keep the original until the author has confirmed the note.
3. **Sort every statement** into one of four buckets before writing:
   - **Observed:** what the author saw, heard or measured ("walked 20 m with a four-wheeled frame, two rest stops").
   - **Reported:** what the participant or someone else said, attributed ("Participant reported sleeping poorly this week").
   - **Interpretation:** the author's professional assessment, clearly labelled and only when the author stated it.
   - **Plan:** agreed next steps, homework, referrals, follow-ups, with owner and timing.
   If a statement could belong to two buckets, put it under Reported or Observed and leave interpretation to the author.
4. **Draft the note** using [assets/progress-note-template.md](assets/progress-note-template.md). Follow the [writing standards](references/writing-standards.md): person-first language, plain words, specific and measurable detail, direct quotes only where the exact words matter, other people identified by role.
5. **Link to plan goals.** For each goal the session touched, record what was done and the observed progress. If the source does not mention a goal, write "not addressed this session". Never infer progress.
6. **Record the billable facts** in the admin block: face-to-face time, provider travel, non-face-to-face time (such as report writing or liaison) and any cancellation, each only if the source states it. These feed `ndis-billing-check`; an inflated minute here becomes a false claim later.
7. **Screen for incidents** with [incident flags](references/incident-flags.md). If anything matches, put an **Incident flag** block at the top of the output, state the matching item in one line, and tell the author to follow the provider's incident management process now. If someone may be in immediate danger, say to call 000 first. Do not decide whether something is reportable; that is the provider's call.
8. **Run the source check.** Every sentence in the note must trace to the source. List anything you could not place under "Needs confirmation" rather than resolving it yourself. Do not add standard phrases such as "participant engaged well" unless the source says so.
9. **Hand back for confirmation.** Present the draft, the Needs confirmation list and any incident flag. The author confirms or edits. A note is not final until the author approves it. Late entries carry the date and time written as well as the session date.
10. **Approval gate.** Saving to the provider's own client record is an internal action the author can authorise once. Sending the note, or a summary of it, to a participant, nominee, plan manager, support coordinator, GP or any third party needs a separate approval: show the exact text, the recipient, the sending account, and the consent on file for sharing with that recipient. Wait for an explicit yes.

## Output

- **Incident flag** (only if triggered) at the very top.
- The note in the chosen format with the admin block.
- **Needs confirmation:** unclear words, missing times, statements with no clear bucket.
- **Follow-ups:** tasks with owner and due date, ready to add to the task list.

Example opening of a goal-linked note:

> **Goal 2: Prepare a simple meal independently.** Participant chopped vegetables using the adapted knife for 12 minutes with one verbal prompt to slow down. Participant said "my hand gets tired after the carrots." Progress: completed two of four steps without physical help (last session: one of four).

## Check before you finish

- [ ] Every sentence traces to the source; nothing invented, nothing embellished.
- [ ] Observation, report and interpretation are visibly separate.
- [ ] Times are the author's actual times, or marked `[not stated]`.
- [ ] Incident screen completed and the result stated, even when nothing was found.
- [ ] Draft, author-confirmed, saved and shared are reported as separate states.

## Guardrails

- Not clinical or legal advice. The author owns the clinical content and the decision to report.
- Respectful, person-first language. No labels ("non-compliant", "aggressive client", "attention-seeking"); describe the behaviour and context instead.
- No diagnoses, medication changes or risk ratings unless the author stated them.
- Third parties are named only by role, and their personal details stay out of the participant's note.
- NDIS Code of Conduct and Practice Standards: notes must be accurate, timely and kept private. This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum CRM activities**: save the confirmed note as a Note activity on the participant's contact so the team shares one timeline. Every text box has a microphone button for dictation, and typing @ mentions a colleague, which is a quick way to alert a supervisor to an incident flag. Create follow-ups as tasks with an owner and due date. Deleting an activity is permanent, so correct notes with a dated addendum. See [activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- **Fulcrum Docs**: use a shared template for longer reports, kept in a restricted Drive folder. See [Fulcrum Docs](https://fulcrumcortex.github.io/documentation/docs/).
- Fulcrum CRM also has a Workforce module for rostering, timesheets and payroll workflows. Availability varies by account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
- [Fulcrum Docs](https://fulcrumcortex.github.io/documentation/docs/)
