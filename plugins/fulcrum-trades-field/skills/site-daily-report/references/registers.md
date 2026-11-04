# Delay, variation and RFI registers

Keep each register as a running table across the project. A daily report adds or updates rows; it never deletes them.

## Delay cause codes

| Code | Cause | Examples | Usually who bears it |
| --- | --- | --- | --- |
| WX | Weather | Rain, wet ground, high wind stopping crane lifts, extreme heat stoppages | Depends on the contract; often an allowance for expected wet days |
| CL | Client or design information | Late drawings, late selections, design change, late access | Often the client; check the contract |
| AU | Authority | Inspection not attended, utility connection delay, permit conditions | Depends on the contract |
| LC | Latent condition | Rock, contamination, hidden services, asbestos found during work | Depends on the contract |
| SU | Supply | Late or wrong delivery, out-of-stock material | Usually the builder, unless client-nominated |
| SC | Subcontractor | No-show, insufficient crew, rework | Usually the builder |
| BU | Builder | Sequencing, supervision, own plant breakdown | The builder |

Record the delay even when the builder bears it. A complete record protects the claims that are valid.

### Delay register columns

| No. | Date started | Date ended | Cause code | Description | Activities affected | Critical path? | Hours or days lost | Notice required? | Notice sent (date, ref) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

**Notice flag.** Contracts set notice requirements for delays and extension-of-time claims, often with short time limits (for example, AS 4000 requires a written extension-of-time claim within 28 days of the delay). Late notice can lose the claim. When a delay may not be the builder's responsibility, flag it in the daily report: "Check the contract's notice clause and time limit." Do not advise on entitlement.

## Variation register columns

| No. | Date raised | Raised by | Description | Instruction source (written or verbal, by whom) | Written confirmation sent | Cost impact | Time impact | Status | Approved amount | Ref |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Status values: `raised`, `priced`, `submitted`, `approved`, `rejected`, `withdrawn`, `disputed`.

Rules:

- A verbal site instruction gets a written confirmation the same day: what was instructed, by whom, when, and that cost and time will be advised. Draft it for the site manager's approval.
- Residential contracts often require variations to be agreed in writing before the work is done, and may limit what can be charged otherwise. Flag work started on a variation that is not yet approved.
- Never price a variation in the register without the estimator's figure; use "to be assessed".

### Verbal instruction confirmation (draft)

> Subject: {project}: confirmation of site instruction, variation {number}
> On {date} at {time}, {instructing_person} instructed {company} to {description}. This is a variation to the contract. We will provide the cost and time impact by {date}. Please let us know by return if this does not reflect your instruction.

## RFI register columns

| No. | Date raised | To (consultant or client) | Question | Drawing or spec ref | Response required by | Impact if late | Status | Response summary | Date closed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- One question per RFI. Include the drawing reference and a photo or markup where it helps.
- Set "response required by" from the programme: the date the information is needed, less ordering and lead time.
- An RFI overdue by more than 2 working days on critical work appears at the top of the weekly summary under "Decisions needed".
- When a response changes scope, open a variation and link the numbers.
