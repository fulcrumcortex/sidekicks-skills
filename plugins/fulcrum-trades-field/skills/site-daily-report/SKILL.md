---
name: site-daily-report
description: Writes a construction site diary or daily report from voice notes, photos, chat messages and dockets, then rolls the week into a client summary. Covers weather and lost time, labour on site by trade, plant, work completed by area, deliveries, delays and their causes, inspections, safety observations and incidents (with notifiable WHS incidents escalated under the user's own process), variations raised and RFIs. Use when a site manager, foreman or builder asks to "write up today's site diary", "turn my voice notes into the daily report", "log the delay", "what RFIs are open", or "send the client the weekly update". Works with any chat, files or pasted notes; uses Fulcrum Drive, Fulcrum CRM and Sessions channels when connected.
---

# Write the site daily report and the weekly client summary

Turns scattered site input into a dated, factual record the builder can rely on later for delay claims, variations and safety, and a weekly summary the client can read in two minutes. The endpoint is a daily report the site manager has checked, and a weekly summary approved before it is sent.

## When to use

- End of each site day, from whatever the team sent: voice notes, photos, group-chat messages, delivery dockets.
- When a delay, variation, RFI or incident needs to be logged the same day.
- Weekly, to send the client or superintendent a progress summary.
- Not for: planning the programme or tasks (`fulcrum-project-planning`), extracting actions from a site meeting (`fulcrum-meeting-actions`), or pricing a variation in detail (`takeoff-to-quote`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Project name, address, contract or job number, report date | Project record | Ask once and reuse |
| Voice notes, photos, chat messages, dockets for the day | Site chat, phone uploads, files | Report only what was supplied; list gaps under "Not reported" |
| Labour on site by trade and company, with headcount and hours | Sign-in sheet, subcontractor messages | Record "not provided"; never estimate headcount |
| Weather | Site observation; a weather service if the host has one | Ask the site manager for rain and stoppages; label any looked-up data with its source |
| Open registers: variations, RFIs, delays | Previous reports, project files | Start new registers and say so |
| The user's incident notification process and the responsible person | Company WHS procedure | Ask before the first report; until known, escalate any incident to the user immediately |

## Procedure

1. **Collect and date-stamp the inputs.** Transcribe voice notes. For each photo, record time, location (level, grid or room) and what it shows. Keep a source reference for every fact (for example "voice note 14:32, J. Example").
2. **Separate facts from intentions.** "Slab poured on level 2" is a fact. "Should pour tomorrow" goes under Planned for next day. Anything uncertain is marked "to confirm".
3. **Fill the daily report** using [assets/daily-report-template.md](assets/daily-report-template.md):
   - **Weather:** conditions morning and afternoon, rain in mm if known, and hours lost with the reason ("wet ground, no excavation 07:00 to 11:00"). Lost time is what matters for an extension-of-time claim.
   - **Labour:** company, trade, headcount, hours. Flag a trade that was programmed but did not attend.
   - **Plant and equipment** on site, including hired plant on standby.
   - **Work completed** by area and activity, with a percentage only when the site manager gave one.
   - **Deliveries:** supplier, docket number, items, received by, and any shortage or damage.
   - **Inspections and hold points:** who inspected, what, result.
   - **Visitors:** name, company, purpose (not personal details beyond that).
4. **Log delays with a cause code** from [references/registers.md](references/registers.md): weather, client or design information, authority, latent condition, supply, subcontractor, builder. Record start, finish or "ongoing", what was affected, and whether the work is on the critical path if the site manager knows. If the cause is outside the builder's control, add a flag: "Check the contract's notice clause and time limit for an extension-of-time notice." Do not decide entitlement.
5. **Log variations and RFIs** in their registers: number, date raised, description, who instructed or who it is addressed to, whether the instruction is in writing, cost and time impact (or "to be assessed"), and status. A verbal instruction on site is logged with "written confirmation required" and a draft confirmation email for the site manager.
6. **Record safety.** Toolbox talks, observations, near misses and incidents, with actions taken. For any incident, apply [references/whs-incidents.md](references/whs-incidents.md):
   - If it might be a notifiable incident (a death, a serious injury or illness, or a dangerous incident), stop drafting and alert the user immediately with the facts known. The user follows their own process for notifying the regulator and preserving the site. The skill does not decide notifiability and does not contact the regulator.
   - Keep injured people's health details to the minimum the report needs; use a role or initials rather than a full name in anything shared beyond the WHS record.
7. **Note what is missing.** A "Not reported" list (for example "no sign-in from the electrician", "no photos from level 3") so the site manager can fill gaps the same day, while memories are fresh.
8. **Site manager review.** Present the report for checking. Amendments after sign-off are added as dated corrections, never silent edits, because the diary may become evidence.
9. **Weekly client summary.** At the end of the week, build [assets/weekly-client-summary-template.md](assets/weekly-client-summary-template.md) from the signed-off dailies: progress against programme, milestones, weather days lost, open variations and RFIs awaiting the client, decisions needed and their dates, safety in summary (no personal or health details), look-ahead for next week, and 4 to 8 representative photos.
10. **Approval gate.** Before the weekly summary, a variation confirmation, an RFI or any message goes to the client, superintendent, consultant or a subcontractor, show the exact content, attachments, recipients and sending account. Wait for an explicit yes. Internal daily reports are saved, not sent, unless the user says otherwise.
11. **File and verify.** Save the signed-off report to the project folder with the date in the filename (`YYYY-MM-DD daily report.md`). After a send, check sent items before marking it sent.

## Output

- The daily report, from `assets/daily-report-template.md`.
- Updated delay, variation and RFI registers (formats in [references/registers.md](references/registers.md)).
- The weekly client summary, from `assets/weekly-client-summary-template.md`.
- A short list of items needing the site manager's action today.

## Check before you finish

- [ ] Every fact traces to a voice note, message, photo or docket; nothing is invented to fill a section.
- [ ] Lost time and delays have causes and times; contract-notice flags raised where relevant.
- [ ] Every incident was escalated to the user, and possible notifiable incidents were flagged immediately.
- [ ] The client summary contains no health information or workers' personal details.
- [ ] Report drafted, saved, sent, pending and failed separately.

## Guardrails

- WHS checklist: the model WHS laws apply in every state and territory except Victoria, which has its own OHS Act; both require the person conducting the business to notify the regulator immediately of notifiable incidents and to preserve the site. The user's process governs who notifies and how. This is a practical checklist, not legal advice.
- Never record speculation about blame for an incident or a delay in the client-facing summary.
- Privacy Act and APPs: collect worker and visitor details only as the site needs them; keep health information in the WHS record with restricted access.
- Photos of people: use them only for site records; check the business's policy before sending identifiable images to the client.

## With Fulcrum

- **Fulcrum Drive** can hold each project's folder of reports, photos and registers, with roles (Viewer, Commenter, Editor) and expiring external links for the client.
- **Fulcrum CRM** projects and issues can track RFIs and defects as issues with an owner and acceptance criteria, and activities record client communications on the contact timeline.
- **Sessions** works through Discord, Telegram, WhatsApp or Slack, so site staff can send voice notes and photos to the assigned conversation, depending on the configured channel.
- A Construction industry module may be available in Fulcrum CRM depending on the account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Files, folders and sharing in Fulcrum Drive](https://fulcrumcortex.github.io/documentation/drive/)
- [Projects, boards, issues and sprints](https://fulcrumcortex.github.io/documentation/crm/projects-and-issues/)
- [Fulcrum Cortex and Sessions](https://fulcrumcortex.github.io/documentation/sessions/)
