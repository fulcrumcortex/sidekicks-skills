# Workshop customer messages

Each message goes through the approval gate: the service adviser sees the exact text, the recipient and the sending account and says yes before it is sent. All names, numbers and prices below are placeholders.

## Authorisation request (SMS, short form)

> Hi {first_name}, it's {workshop_name} about your {make_model} ({rego}). During the {booked_work} we found:
> 1. {item_1} – {rating_1} – ${price_1} inc GST
> 2. {item_2} – {rating_2} – ${price_2} inc GST
> Details and photos: {link_or_email_note}. Reply with the numbers you approve (for example "1" or "1 and 2"), or call {workshop_phone}. We won't do any extra work without your OK.

## Authorisation request (email, full form)

Subject: Approval needed for your {make_model} ({rego}), job {job_number}

> Hi {first_name},
>
> While carrying out the {booked_work}, {tech_first_name} found the following. Photos are attached.
>
> | # | Item | Rating | What we found | If it waits | Price inc GST |
> | --- | --- | --- | --- | --- | --- |
> | 1 | {item} | Red: safety | {finding with measurement} | {consequence} | {price} |
>
> Red items affect safety or roadworthiness now. Amber items need attention soon. Prices include parts, labour and GST.
>
> {dtc_explanations_if_any}
>
> Please reply with the items you approve. We will not go beyond the amount you approve; if anything changes, we will contact you first.
>
> {adviser_name}, {workshop_name}, {workshop_phone}

## Reading the reply

| Reply | Record as |
| --- | --- |
| "Yes", "go ahead" with no item numbers when several were offered | Unclear. Ask which items. Do not assume all. |
| "1 and 3" | Items 1 and 3 approved at the quoted amounts; item 2 declined unless they say "later" |
| "Just do the safety stuff" | Red items approved only; confirm the list and total back to them |
| "How much for just the parts?" | Not an approval. Answer through the approval gate. |
| A phone approval | Send a confirmation: "Thanks {first_name}, confirming you approved {items} for ${total} inc GST on the phone at {time}." |
| Declines a red item | Record it with the warning given; send a short written note of the safety advice |

## Ready for pick-up

> Hi {first_name}, your {make_model} ({rego}) is ready at {workshop_name}. Total ${amount} inc GST, invoice {invoice_number} attached. We're open until {closing_time}. {declined_items_note}

## Completion summary (for the invoice or handover sheet)

> **Concern:** "{customer_words}"
> **Cause:** {confirmed_cause}
> **Correction:** {work_done}; parts fitted: {parts_list}.
> **Codes:** {codes_found} cleared; {did_or_did_not} return on a {distance} km road test.
> **Declined or deferred:** {items_with_advice}
> **Next service due:** {date} or {odometer} km, whichever comes first.
> **Warranty:** {workshop_warranty_terms}
