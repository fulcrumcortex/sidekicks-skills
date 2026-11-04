# Compliance, award and fatigue checklist

Read this when setting up `compliance-rules.json` and before the approval gate. The agent flags; the employer decides. Check every item against the applicable Modern Award (for most disability and home care work, the Social, Community, Home Care and Disability Services Industry Award, often called SCHADS), any enterprise agreement, employment contracts and organisational policy. Clause numbers and amounts change, so this list asks questions rather than giving answers.

## Worker checks (configurable list)

Use the key names in your `compliance-rules.json`. Typical items:

| Key | Check | Usually required for | Notes |
| --- | --- | --- | --- |
| `ndis_worker_screening` | NDIS Worker Screening Check clearance | Risk-assessed roles with NDIS participants | Record the clearance expiry; a pending or barred status means not rostered |
| `wwcc` | Working with children check for the worker's state (names differ, for example Blue Card in Queensland) | Work with children or young people | State-specific; some states accept the NDIS check for some roles, check yours |
| `first_aid` | First aid certificate | Most direct support roles | Many organisations renew every 3 years |
| `cpr` | CPR | Most direct support roles | Many organisations refresh annually |
| `ndis_orientation` | NDIS Worker Orientation Module completed | NDIS support workers | No expiry, but record completion |
| `driver_licence` | Current driver licence | Transport and community access | Add vehicle insurance and registration if the worker drives clients in their own car |
| `manual_handling` | Manual handling training, hoist use | Personal care with transfers | Client-specific competency may also be needed |
| `medication` | Medication assistance training | Medication prompts or administration | Follow the client's medication plan |
| `peg_feeding`, `epilepsy`, `behaviour_support` | High-intensity or client-specific training | Clients whose plan requires it | Treat as a skill or compliance item with an expiry if it has one |
| `police_check` | National police check | Aged care and some funders | Aged care screening rules differ from NDIS rules; check current requirements |
| `work_rights` | Visa work rights and hour limits | Workers on visas | Weekly hour limits affect the maximum hours setting |

Set `warn_within_days` so renewals show up early enough to book training (30 days is a common starting point).

## Fatigue and rest

- [ ] Minimum break between the end of one shift and the start of the next (SCHADS sets one; the sample file uses 10 hours as a placeholder to confirm)
- [ ] Maximum shift length and how sleepovers and active overnight shifts are counted
- [ ] Maximum consecutive days and days off per roster cycle
- [ ] Meal breaks within long shifts
- [ ] Travel time between back-to-back clients is realistic for the distance and traffic

## Award and pay questions to flag

- [ ] Minimum engagement per shift for casual and part-time staff
- [ ] Broken shifts: how many breaks are allowed, the maximum span, and any allowance
- [ ] Overtime triggers: daily hours, weekly hours, hours beyond the agreed roster for part-time staff, short rest between shifts
- [ ] Penalty rates for evenings, nights, weekends and public holidays
- [ ] Sleepovers and 24-hour care rules
- [ ] Notice required to change a published roster, and when the worker's agreement is needed
- [ ] Payment when a client cancels a shift at short notice
- [ ] Travel time between clients, and vehicle or kilometre allowance
- [ ] Remote work, on-call and higher duties
- [ ] Part-time minimum guaranteed hours and agreed patterns

## Before publishing

- [ ] No hard constraint broken without a recorded owner decision
- [ ] Every flagged award question has an owner
- [ ] Staff messages contain only what the worker needs for the shift
- [ ] Clients affected by a worker or time change are told before the shift, after approval

This is a practical checklist, not legal or industrial relations advice.
