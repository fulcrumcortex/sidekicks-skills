# Job confirmation message templates

Fill the `{placeholders}` from the job record. Keep every message factual: no offers, no review requests, no referral lines. Keep SMS under 320 characters (two segments) where possible. Use the business name exactly as the customer knows it. All names and numbers below are fictional.

## Contents

- Day-before confirmation (SMS)
- Confirmation call script
- Reply handling table
- Reschedule
- On the way, running late
- Completion and invoice cover note

## Day-before confirmation (SMS)

Record has access, pet and parking details:

> Hi {first_name}, it's {business_name}. Confirming {job_type} at {street_address} on {day} {date}, arriving between {window_start} and {window_end}. Reply YES to confirm, or reply or call {business_phone} to change the time.

Record is missing them (add only the questions you need):

> Hi {first_name}, it's {business_name}. We're booked for {job_type} at {street_address} on {day} {date}, arriving {window_start}–{window_end}. Reply YES to confirm. Also helpful: any gate or access instructions, pets we should know about, and where our van can park.

Strata, basement or high-rise job:

> ... Our van is {van_height} m high. Is there visitor parking or a loading bay, and do we need to collect a key or swipe from building management?

Do not ask the customer to text a lockbox or alarm code. Ask them to call, or to leave it with the office by phone.

## Confirmation call script

Use for long or high-value jobs, landlines and non-responders.

1. "Hi, it's {caller_name} from {business_name}. Is that {first_name}?" If it is not the customer, do not discuss the job details; ask for a good time to reach them.
2. If the call is recorded: "This call is recorded for quality."
3. "I'm calling to confirm {job_type} tomorrow, {date}, with arrival between {window_start} and {window_end}. Does that still work?"
4. Collect only what is missing: access, pets, parking, who will be home, anything that has changed since the booking (for example the fault has stopped).
5. Close: "Thanks. {tech_first_name} will text when on the way."

Voicemail (no job detail beyond the date):

> Hi {first_name}, it's {business_name} about your booking on {date}. Please call us on {business_phone} or reply to our text. Thanks.

## Reply handling table

| Reply | Status | Action |
| --- | --- | --- |
| YES, Y, confirmed, thumbs up, "see you then" | confirmed | Record it. No reply needed unless the business sends a thank-you. |
| A different time or day | reschedule | Offer 2 or 3 real slots (see below). |
| Access, pet or parking detail | confirmed if also confirming, otherwise unchanged | Copy the detail to the job record and the tech's run-sheet. |
| "Fault has fixed itself", "don't need it now" | needs a person | Do not cancel. Ask the user whether to keep, convert to an inspection, or cancel. |
| Question about price or scope | needs a person | Hand to the user with the quote reference. Do not quote. |
| STOP, unsubscribe, "don't text me" | opted out | Record the opt-out on the contact at once. The job itself stands; confirm by phone if needed. |
| Complaint or anger | needs a person | Escalate the same day. Send nothing automated. |
| Wrong number | needs a person | Flag the record; do not send the job details again. |
| No reply by 15:00 | unconfirmed | One call or a second SMS, then list for the user at 17:00. |

## Reschedule

> No problem, {first_name}. We can do {slot_1}, {slot_2} or {slot_3}. Reply 1, 2 or 3, or suggest another day.

After the pick:

> Thanks {first_name}, you're now booked for {day} {date}, arriving {window_start}–{window_end}. Reply or call {business_phone} if anything changes.

Only quote a late-change or call-out fee if the business's terms include one and the user asks for it to be mentioned, using their exact wording.

## On the way, running late

On the way (send when the tech leaves the previous job):

> Hi {first_name}, {tech_first_name} from {business_name} is on the way and should arrive between {eta_start} and {eta_end}.

Running late (more than 15 minutes outside the confirmed window):

> Hi {first_name}, {tech_first_name} is running about {minutes} minutes behind and now expects to arrive between {eta_start} and {eta_end}. Sorry for the delay. Reply if this no longer suits.

More than 60 minutes late: call, apologise, offer to keep the slot or rebook. Do not send an automated SMS instead of the call.

## Completion and invoice cover note

> Hi {first_name}, thanks for having us today. {tech_first_name} completed {work_summary}. Your invoice {invoice_number} for {amount_inc_gst} (incl. GST) is attached / at {invoice_link}. Payment is due by {due_date}. Questions: {business_phone}.

Return visit needed:

> Hi {first_name}, {tech_first_name} has {work_done_so_far}. We need to come back to {remaining_work} because {reason}. We'll call you by {date} to book a time.
