# Scheduling decision rules

## Direct invite, proposed slots or booking link

| Situation | Method | Why |
| --- | --- | --- |
| Internal meeting, calendars visible to you | Direct invite at the best free slot, after the approval gate | Asking for preferences wastes a round. |
| First meeting with a senior or important external person | Propose 2 to 3 slots in a short personal message | A bare booking link can read as offhand. |
| Group of three or more external people | Propose 2 to 3 slots, or one poll message | A booking link only works for one guest's calendar. |
| One external person, routine meeting type (intro call, quote visit, check-in) and a matching booking page exists | Send the booking link | They pick from live availability; no back-and-forth. |
| Two rounds of proposals have failed | Switch to a booking link, plus one direct option | Stops the email ping-pong. |
| The other side sent their own booking link | Use it, after the approval gate (booking on the owner's behalf is an outward action) | Respect their process. |
| Urgent (today or tomorrow) | A phone call or a single specific time, not a list | Lists slow urgent decisions down. |

If no booking page exists for the meeting type and the owner wants one, hand over to `fulcrum-booking-setup`.

## Slot quality

Rank options in this order:

1. Inside every required person's working hours, with buffers clear.
2. Not in anyone's first or last working hour, not 12:00 to 13:00 local.
3. Not Monday before 10:00 or Friday after 15:00 for external guests.
4. Two or more business days ahead for external guests; same or next day only for internal or urgent meetings.
5. Owner's protected time (focus blocks, school pick-up, travel) is busy even if the calendar shows it as free; ask the owner once what they protect and remember it for the session.

Buffers:

| Meeting | Before | After |
| --- | --- | --- |
| Video, back to back | 5 to 10 min | 5 to 10 min |
| External sales or client meeting | 10 min | 15 min (notes and follow-up) |
| In person, same suburb | 20 to 30 min | 20 to 30 min |
| In person, across town | estimate travel time plus 15 min | same |

A free period must fit the whole meeting **and** its buffers.

## Holds

- Only on the owner's calendar, never on a guest's.
- Title `HOLD: <meeting> (option n of 3)`, no guests, marked busy.
- Release all holds within one hour of a confirmed choice, or after 2 business days without a reply, and tell the owner.

## Reschedules

| Who asks | What to do |
| --- | --- |
| Guest asks to move | Offer 2 options in the next 5 business days, or the booking page's reschedule link if it was a booking. Keep the original event until the new time is accepted. |
| Owner asks to move | Draft an apology plus 2 options. Do not move the event until the guest agrees, unless the owner says to move it and notify. |
| Third reschedule of the same meeting | Flag to the owner: the meeting may not be a priority for one side. Suggest asking whether to continue. |
| Booking made through a booking page | Use the booking's own reschedule or cancel action so the guest stays informed; do not edit the calendar event directly. |

Never cancel and re-create an event as a "reschedule" when the calendar supports moving it; guests lose the thread and may see two invitations.

## No-shows

| Time after start | Action |
| --- | --- |
| +3 to 5 min | Check the meeting link, the invitation's time zone and the guest's response. A wrong zone causes most no-shows. |
| +5 min (external) | Short "I'm in the room" message on the channel the guest used, after approval. Approval can be given in advance when the owner asks you to handle no-shows. |
| +10 to 15 min | Leave. Draft a no-blame follow-up with 2 new options or the booking link. |
| Same day | Log the no-show on the CRM record and set a follow-up task. |
| Second no-show by the same person | Do not offer specific times again. Send the booking link once and flag to the owner. |

## When data is missing

- External calendar not visible: propose from the owner's free time inside the guest's likely working hours, and say so.
- Guest's zone unknown: ask, or write options with two zones ("10:00 Sydney / 07:00 Perth") so the guest can correct you.
- Calendar connection error or "reconnect required": do not schedule from stale data; tell the owner which account needs reconnecting.
