# Run-sheet rules

Use these rules to order each technician's day. They work from suburbs alone; when the host provides coordinates or a mapping tool, use real travel times instead of the default buffers and say so on the sheet.

## Order of decisions

1. **Anchor fixed times first.** Jobs with an exact time or a narrow window (for example "must be 07:30 before the café opens") are fixed points. Everything else fits around them.
2. **Respect windows.** AM window jobs (07:00 to 12:00) go before 12:00; PM window jobs (12:00 to 17:00) after. A window is the arrival window, not the finish.
3. **Cluster by suburb.** Group the flexible jobs into clusters of the same or neighbouring suburbs. Do the whole cluster before moving on. Never cross the same part of the city twice in a day.
4. **Direction of travel.** Start with the cluster nearest the tech's start point (home or depot) and work outwards, finishing near home or the next morning's first job where known.
5. **Hard jobs early.** Within a cluster, put the longest, most diagnostic or least predictable job first, while there is slack in the day.
6. **Parts runs.** If a job needs a supplier pick-up, place it after the supplier opens and on the way to that job. List the parts on the sheet.
7. **Buffers.** Default travel: 10 minutes within a suburb, 25 minutes between neighbouring suburbs, 45 minutes across the metro area. Add 15 minutes for strata or basement access. Add a 30-minute break around the middle of the day.
8. **Capacity.** Sum job durations plus buffers. If the day runs more than 30 minutes past the tech's finish time, flag the lowest-priority flexible job as a candidate to move, and tell the user. Do not move it without approval.

## Conflicts to flag rather than solve silently

- Two fixed-time jobs that cannot both be reached with the travel buffer.
- A job whose customer is unconfirmed at 17:00 the day before.
- A job needing a licence or ticket the assigned tech does not hold (for example gas fitting, working at heights, asbestos removal).
- A job needing two people assigned to one tech.
- A job whose access requires a key collection the office has not arranged.

## What stays off the sheet

- Payment card details.
- Customer notes unrelated to the job (complaints history belongs on the CRM record).
- Lockbox, alarm and gate codes go only on the tech's personal copy, never in a shared channel. Mark them "remove after the job".
