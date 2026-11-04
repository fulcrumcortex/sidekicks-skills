---
name: workshop-job-card
description: Builds and runs an automotive workshop job card from intake to handover. Captures rego, VIN, odometer and the customer's concern in their own words, records inspection findings with photo references and a red, amber, green rating, explains diagnostic trouble codes (DTCs) in plain language for the technician to confirm, gets written authorisation with an amount before any extra work, lists parts to order, and writes the completion summary, with an Australian Consumer Law checklist. Use when a mechanic, service adviser or workshop manager asks to "open a job card", "write up the inspection", "explain this P0420 to the customer", "get approval for the extra work", "order the parts" or "write the completion notes". Works with any workshop system, notes or pasted scan output; uses Fulcrum CRM and Lyre when connected.
---

# Run a workshop job card from intake to handover

Keeps a vehicle job honest and traceable: what the customer reported, what the technician found, what the customer approved and what was done. The endpoint is a complete job card, customer messages the service adviser approved, and a completion summary ready for invoicing.

## When to use

- Booking a vehicle in, or turning a technician's notes into a structured card.
- Explaining scan-tool codes and findings to a customer in plain language.
- Requesting approval for additional work found during a service or repair.
- Writing the handover summary and checking consumer-guarantee obligations.
- Not for: booking the appointment itself (`fulcrum-booking-setup`), reviewing a recorded customer call (`fulcrum-call-review`), or general follow-up after the job (`fulcrum-crm-follow-up`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Customer name, mobile, preferred contact method | Booking, CRM record | Ask at intake |
| Rego and state, VIN, make, model, year, odometer | Vehicle, rego papers, previous visits | VIN and odometer are required; ask the tech to read them off the vehicle |
| Customer concern in their own words | Booking notes, intake conversation | Ask: "What is it doing, when, and since when?" |
| Inspection notes and photos | Technician | Mark unchecked items "not inspected", never "OK" |
| Scan output: codes, status (pending, confirmed, permanent), freeze-frame | Scan tool | Record "no scan performed" |
| Labour rates, parts prices, the workshop's authorisation policy | Workshop system, price lists | Leave prices blank and ask; never estimate a part price |

## Procedure

1. **Open the card** from [assets/job-card-template.md](assets/job-card-template.md). Check the VIN is 17 characters with no I, O or Q (older vehicles may carry a shorter chassis number; record it as given). Record odometer, fuel level and existing damage with photo references, so pre-existing marks are not later blamed on the workshop.
2. **Record the concern verbatim.** Quote the customer ("grinding noise from the front left when braking, worse in the morning, started two weeks ago"). Do not translate it into a diagnosis. Add conditions: when, how often, speed, temperature, warning lights.
3. **Give the repair notice at intake where it applies.** If the workshop may use refurbished parts instead of new, or the vehicle holds personal data (paired phones, contacts, saved addresses), the customer must be told before the vehicle is accepted. See [references/acl-checklist.md](references/acl-checklist.md).
4. **Record the authorised scope.** What the customer approved at booking (for example "logbook service and inspect brake noise, diagnose up to 1 hour") and the authorised amount. Work beyond this needs step 7.
5. **Structure the findings.** For each item: system, finding, measurement where relevant (pad thickness in mm, tyre tread depth in mm, battery test result), photo reference, rating and recommendation.
   - **Red:** safety-critical or illegal now (tread at or below 1.5 mm, brake pads below the manufacturer minimum, fluid leaking onto exhaust or brakes). Recommend not driving until fixed.
   - **Amber:** needs attention soon; give a time or distance estimate from the tech.
   - **Green:** checked and fine.
6. **Explain codes.** For each DTC, use [references/dtc-guide.md](references/dtc-guide.md): code, status, the standard description, a plain-language explanation, and the common causes to check. Every explanation carries the caveat: "A code tells us what the computer saw, not which part failed. {tech_name} will confirm the cause with testing before we replace anything." Never recommend a part from a code alone.
7. **Request authorisation for additional work.** Draft the request from [references/customer-messages.md](references/customer-messages.md): each item with its rating, price inc GST (parts and labour), and what happens if it waits. Show the total the customer is being asked to approve. Red items come first.
8. **Approval gate.** Before contacting the customer by SMS, email or phone, show the service adviser the exact message, the customer's number or email, and the sending account. Wait for an explicit yes. Do not contact the customer directly from the technician's notes without this step.
9. **Record the customer's decision in writing.** Approved, declined or deferred per item, with the amount approved, who approved it, how (SMS reply, email, signed form, recorded call) and the date and time. A verbal approval on an unrecorded call is confirmed back by SMS or email before work starts. If the cost will exceed the approved amount, stop and re-authorise. Declined red items are recorded with the warning given.
10. **Order parts** only for approved work: part number, brand, genuine or aftermarket, quantity, supplier, price, expected arrival. Flag parts with long lead times to the customer through the approval gate.
11. **Write the completion summary** using the 3C structure: Concern (verbatim), Cause (confirmed by the tech), Correction (what was done, parts fitted). Add: codes cleared and whether they returned on the road test, road-test result, items declined and their advice, next service due (date and odometer), and warranty on parts and labour per the workshop's terms.
12. **Approval gate** again for the completion message and invoice: exact content, recipient, channel and sending account. The invoice must match the authorised amounts; any difference is explained or removed before sending.

## Output

- The completed job card from [assets/job-card-template.md](assets/job-card-template.md).
- The authorisation request and the completion message, as approved.
- An authorisation log: item, amount, decision, who, how, when.

## Check before you finish

- [ ] VIN, rego and odometer recorded; concern quoted in the customer's words.
- [ ] Every finding has a rating and, where possible, a measurement and photo reference.
- [ ] Every DTC explanation carries the "tech confirms" caveat; no part recommended from a code alone.
- [ ] No work beyond the authorised scope and amount without a recorded written approval.
- [ ] The ACL checklist was run where relevant.
- [ ] Report drafted, sent, pending and failed separately.

## Guardrails

- Never fabricate a measurement, test result or code. "Not inspected" is an honest entry.
- Never pressure a customer with exaggerated risk. Red means a real safety or legal issue the technician has confirmed.
- Australian Consumer Law: services carry guarantees of due care and skill, fitness for a stated purpose and reasonable time; parts supplied carry guarantees of acceptable quality. Run the full checklist in [references/acl-checklist.md](references/acl-checklist.md).
- Privacy Act and APPs: collect only what the job needs; do not copy the customer's licence or personal data held in the vehicle.
- Spam Act: service reminders that promote offers are commercial messages and need consent, sender identification and a working unsubscribe honoured within 5 working days.

This is a practical checklist, not legal advice.

## With Fulcrum

- **Fulcrum CRM** keeps the customer, logs each SMS, call and email as an activity on their timeline, holds follow-up tasks (for example the next service reminder) for a person, team or AI agent, and keeps invoices as drafts until Finalize & Send.
- **Lyre** can place a one-off call with an objective such as confirming an appointment; calls are recorded with AI and recording disclosure available, and the transcript in call history can serve as evidence of a verbal approval. Confirm that approval in writing as well.
- An Automotive industry module may be available in Fulcrum CRM depending on the account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for current modules.

## Learn more

- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
- [Call history, recordings and transcripts in Lyre](https://fulcrumcortex.github.io/documentation/lyre/call-history/)
