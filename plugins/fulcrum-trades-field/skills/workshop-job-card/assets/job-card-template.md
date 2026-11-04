# Job card {job_number}

| Field | Value |
| --- | --- |
| Date in / promised | {date_in} / {promised_date_time} |
| Service adviser / technician | {adviser} / {technician} |
| Customer | {customer_name}, {mobile}, prefers {sms_email_call} |
| Vehicle | {year} {make} {model}, {colour} |
| Rego and state | {rego} ({state}) |
| VIN | {vin_17_chars} |
| Odometer in | {odometer} km |
| Fuel level | {fuel} |
| Existing damage | {notes} (photos {photo_refs}) |
| Repair notice given | {yes_no_na} at {time} |

## Customer concern (their words)

> "{verbatim_concern}"

When: {conditions} | Since: {since} | Warning lights: {lights}

## Authorised at booking

Scope: {booked_scope}
Authorised amount: ${authorised_amount} inc GST

## Inspection findings

| # | System | Finding | Measurement | Photo | Rating (R/A/G) | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | {system} | {finding} | {value_mm_or_result} | {photo_ref} | {rating} | {recommendation} |

Not inspected: {items_not_inspected_and_why}

## Diagnostic codes

| Code | Status | Description | Plain-language note | Confirmed cause (tech) |
| --- | --- | --- | --- | --- |
| {code} | {pending_confirmed_permanent} | {description} | {plain} | {tech_confirmation_or_pending} |

Freeze-frame recorded: {yes_no}

## Additional work authorisation log

| # | Item | Price inc GST | Decision | Approved by | How | When |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | {item} | {price} | {approved_declined_deferred} | {name} | {sms_email_signed_call} | {date_time} |

Running total approved: ${total_approved} inc GST

## Parts

| Part no. | Description | Genuine / aftermarket / refurbished | Qty | Supplier | Price ex GST | ETA | For item # |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Completion

- Concern: {verbatim_concern}
- Cause: {confirmed_cause}
- Correction: {work_done}
- Road test: {distance} km, result {result}; codes returned: {yes_no}
- Odometer out: {odometer_out} km
- Declined items and advice given: {declined}
- Next service: {date} or {km}
- Logbook stamped: {yes_no_na}
