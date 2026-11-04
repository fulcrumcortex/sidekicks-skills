---
name: roster-planner
description: Builds or repairs a weekly roster for a disability, aged care, community care or allied health workforce. Matches client needs and preferences to worker availability, skills and in-date compliance (NDIS Worker Screening, first aid, CPR, working with children checks and others from a configurable list), protects continuity of care, travel time and minimum breaks between shifts, flags award and overtime questions for checking against the applicable Modern Award such as SCHADS, fills open shifts and handles swaps and sick calls. Use for "build next week's roster", "fill this shift", "who can cover", "shift swap", "sick call", "roster conflicts" or "check the roster". Includes a roster checker script. Works with spreadsheets or any rostering export; Fulcrum CRM has a Workforce module on some accounts. Nothing is published or sent to staff or clients without approval.
---

# Build or repair a care roster

Produces a weekly roster that covers every client's supports with eligible, available workers, plus a clear list of conflicts and decisions for the roster owner. Built for coordinators in small and mid-sized care providers. The endpoint is a reviewed roster and conflict list; publishing it and notifying staff or clients happen only after explicit approval.

## When to use

- Building next week's roster from client needs and staff availability.
- Repairing a roster after leave, a sick call, a new client or a client change.
- Filling an open shift or approving a shift swap.
- Checking a draft roster for compliance expiry, fatigue and continuity problems.
- Not for: payroll calculation or timesheet approval (use the payroll system), client onboarding paperwork (use `ndis-client-onboarding`), or general team scheduling for non-care work (use `fulcrum-project-planning`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Shifts or client support needs: client, times, location, required skills | Service agreements, recurring schedule, last week's roster | Cannot roster; ask for it |
| Workers: skills, contracted or maximum hours, availability | HR records, availability forms | Treat availability as unknown and confirm before offering |
| Compliance records with expiry dates | HR or compliance register | Treat as missing; the worker cannot be rostered for shifts that require it |
| Client preferences and exclusions | Client file, intake, feedback | Use continuity of care as the default preference |
| Rules: minimum rest, maximum shift length, required checks | Organisation policy, the applicable Modern Award or enterprise agreement | Use [assets/compliance-rules.json](assets/compliance-rules.json) as placeholders and say they need confirming |

Use client references, not names, in working files. A roster shows workers only what they need: client reference or first name, address, times, and the support required. Health details stay in the client file.

## Procedure

1. **Confirm the rules first.** Load or agree the settings in `compliance-rules.json`: required checks for all shifts, extra checks per shift type, minimum rest between shifts, maximum shift length, maximum consecutive days, travel buffer, and the most workers a client should see in a week. The list is configurable; see [award and fatigue checklist](references/award-and-fatigue-checklist.md) for common items.
2. **Separate hard constraints from preferences.**
   - Hard (never broken without a documented decision by the roster owner): compliance in date on the shift date, required skills and client-specific training, client exclusions, no double booking, availability, minimum rest.
   - Soft, in this order: continuity of care (the same small team), client preferences (gender, language, culture, interests), travel, fair hours against contracted hours, worker preferences, cost such as overtime and penalty rates.
3. **Place the hardest shifts first.** Specialised skills (for example PEG feeding, complex behaviour support, manual handling with a hoist), overnights and sleepovers, weekends and public holidays, remote locations. Then copy last week's pattern for regular clients to keep continuity. Then fill the rest, preferring workers below their contracted hours.
4. **Check the draft with the script:**
   ```bash
   python3 scripts/roster_check.py --shifts shifts.csv --workers workers.csv \
     --clients clients.csv --rules compliance-rules.json
   ```
   Sample inputs are in [assets/](assets/). The report lists conflicts by severity, ranked candidates for open or conflicting shifts, hours per worker and continuity per client.
5. **Resolve conflicts in severity order.** Expired or missing compliance: remove the worker from the shift and tell the roster owner, who follows up the renewal. Double booking or short rest: move the later shift. `BROKEN_SHIFT_CHECK`, `OVER_MAX_HOURS`, `LONG_SHIFT` and `CONSECUTIVE_DAYS`: check against the award and policy before accepting. `CONTINUITY`: swap to a worker already in the client's team where possible. Re-run until no high-severity conflicts remain, or each remaining one has an owner decision recorded.
6. **Fill open shifts** with [open shifts, swaps and sick calls](references/open-shifts-and-swaps.md): offer to the client's regular team first, then part-time workers under contracted hours, then casuals, then agency. Offer only to workers the checker shows as eligible.
7. **Handle swaps and sick calls** with the same reference. A swap is approved only if the incoming worker passes every hard constraint and no new conflict appears. For a same-day gap, triage by client risk: personal care, medication support and clients living alone come first; community access may be rescheduled with the client's agreement.
8. **Run the award and fatigue checklist** in [award and fatigue checklist](references/award-and-fatigue-checklist.md) on the final draft and list every item that needs a payroll or award check.
9. **Approval gate.** Show the roster owner the final roster, the conflict list with decisions, the exact messages to staff (shift offers, roster published, changes) and to clients (change of worker or time), the recipients and the sending account or channel. Wait for an explicit yes for this batch. Then publish and send once. If a send result is unclear, check sent messages before resending.
10. **Close the loop.** Track acknowledgements. Any shift not acknowledged 24 hours before start gets a phone call from the coordinator. Record changes with the reason.

## Output

1. Roster by day: date, time, client reference, location, worker, skills required, status (confirmed, offered, open).
2. Conflicts table: severity, type, shift, worker, detail, decision and owner.
3. Open shift plan: candidates in offer order and the message to send.
4. Hours per worker against contracted or maximum hours, with award items to check.
5. Continuity per client: number of different workers this week.

## Check before you finish

- [ ] No worker rostered on a shift whose required checks expire or are missing by the shift date.
- [ ] No double bookings; rest gaps meet the confirmed setting or have an owner decision.
- [ ] Every client's required supports are covered, or the gap is listed with an action.
- [ ] Award and overtime items are flagged for checking, not decided by the agent.
- [ ] Drafted, approved, published and acknowledged are reported as separate states.

## Guardrails

- Not legal, industrial relations or payroll advice. The agent flags award questions; the employer checks the applicable Modern Award (for example the Social, Community, Home Care and Disability Services Industry Award), enterprise agreement and contracts.
- Never roster a worker without a current NDIS Worker Screening clearance (or the applicable state check) where the role requires it. Expired means off the shift, even for one day.
- Clients choose who supports them. Respect exclusions and preferences, and tell clients about changes before the shift, not at the door.
- Staff details (availability, leave reasons, health) are personal information; share only what the roster needs.
- NDIS Practice Standards and Code of Conduct: supports delivered by suitably skilled, screened workers, with continuity and the client's choice respected. This is a practical checklist, not legal advice.

## With Fulcrum

- Fulcrum CRM has a Workforce module for rostering, timesheets and payroll workflows. Availability varies by account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules. This skill works the same from a spreadsheet export.
- **Fulcrum CRM tasks**: post an open shift as a task assigned to a team. It shows for every member until one of them picks it up, and the coordinator still confirms the pick-up against the checker. See [activities and tasks](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/).
- **Fulcrum CRM custom fields and lists**: keep compliance expiry dates on worker contact records as Date Picker fields, and build an active list filtered on an expiry date so renewals due in the next 30 days are visible. See [custom fields](https://fulcrumcortex.github.io/documentation/crm/custom-fields/) and [lists](https://fulcrumcortex.github.io/documentation/crm/lists/).

## Learn more

- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
- [Lists in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/lists/)
- [Fulcrum CRM](https://fulcrumcrm.app/)
