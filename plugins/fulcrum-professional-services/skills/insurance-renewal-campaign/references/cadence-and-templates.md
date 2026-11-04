# Renewal cadence and message templates

Use the licensee's approved templates where they exist; these are a starting point for the licensee to approve. All names and numbers are fictional placeholders.

## Contents

- Cadence at a glance
- Needs-change prompts by class
- Document requests
- Templates: D-60 email, D-30 call, D-14 SMS, D-7 SMS and call, instructions confirmation, after expiry
- Stop rules

## Cadence at a glance

| Stage | Days to expiry | Touches | Goal | Escalate when |
| --- | --- | --- | --- | --- |
| D-60 | 60 to 31 | Email with needs-change prompts and document request | Changes and documents in before the insurer's terms | Large or complex risk: tell the account manager now |
| D-30 | 30 to 15 | Call; email chase for documents | Changes discussed; terms requested or received | No response to D-60 and D-30 |
| D-14 | 14 to 8 | SMS reminder; call if no response in 2 working days | Terms with the client; instructions requested | Premium increase over the threshold the licensee sets, or declined terms |
| D-7 | 7 to 1 | Call and SMS; account manager informed | Written instructions to renew, change or lapse | Always escalate at D-7 without instructions |
| Expired | 0 or less | Account manager decides | Confirm cover status with the insurer | Always |

Minimum gap between touches: 5 days at D-60, 4 at D-30, 3 at D-14, 2 at D-7. The `scripts/renewal_stage.py` helper applies these.

Insurer renewal notices: for prescribed consumer classes (such as motor vehicle, home buildings and contents, sickness and accident, consumer credit and travel), the insurer must give written notice at least 14 days before expiry. Know whether the insurer or the broker sends it in each arrangement, and do not rely on the campaign to meet that obligation.

## Needs-change prompts by class

Ask only the questions for the client's classes. Each is factual: it asks what has changed, never what they should buy.

Business:

- Has your turnover, wage roll or number of staff changed by more than 10%?
- New premises, a move, or changes to your building, security or fire protection?
- New products, services, activities, or work interstate or overseas?
- New vehicles, equipment or stock levels?
- Any claims, incidents or circumstances that could lead to a claim since last renewal?
- Changes to directors, ownership or business structure?

Home and contents:

- Renovations, extensions, a pool or other changes to the building?
- New valuables over the single-item limit in your policy (jewellery, art, equipment)?
- Is the home still owner-occupied, or is it now rented, vacant for long periods, or used for business?
- Changes to security (alarm, locks)?

Motor:

- Changes to drivers, especially drivers under 25?
- Modifications, accessories, or change of use (for example business use or ride-share)?
- A change of garaging address?

Landlord:

- Change of tenant, rent amount, or property manager?
- Periods of vacancy?

## Document requests

| Class | Common documents |
| --- | --- |
| Business | Updated turnover and wage figures, asset and stock values, vehicle schedule, contracts requiring specific cover, claims history |
| Property | Rebuild cost estimate or valuation, tenancy details |
| Professional indemnity | Proposal form, fee income split, contracts |
| Motor fleet | Vehicle list with values, driver list |

Request documents through the licensee's secure channel or portal, not as SMS replies.

## D-60 email

Subject: Your {policy_class} insurance renews on {expiry_date}

> Hi {first_name},
>
> Your {policy_class} policy with {insurer} (policy {policy_number}) renews on {expiry_date}. To give the insurer accurate information, please let us know about any changes since your last renewal:
>
> {needs_change_prompts_for_class}
>
> {documents_requested_with_due_date}
>
> {disclosure_duty_wording_approved_by_licensee}
>
> Reply to this email or call {adviser_name} on {office_phone}. Once we have the insurer's renewal terms, we'll send them to you.
>
> {adviser_name}, {brokerage_name}, AFSL or authorised representative no. {licence_number}
> {unsubscribe_line_for_marketing_content_if_any}

## D-30 call script

1. "Hi, it's {caller_name} from {brokerage_name}. Is that {first_name}?" Identity check per the licensee's process before discussing the policy.
2. Recording and AI disclosure if applicable: "This call is recorded."
3. "I'm calling about your {policy_class} policy, which renews on {expiry_date}. Have there been any changes we should tell the insurer about?" Work through the prompts for the class.
4. Any "should I" question: "That's one for {adviser_name}; I'll have them call you by {day}." (See the advice boundary reference.)
5. Close: confirm outstanding documents and the date terms will be sent.
6. Log: outcome, changes reported in the client's words, documents promised, follow-up task.

## D-14 SMS

> Hi {first_name}, {brokerage_name} here. Your {policy_class} policy renews on {expiry_date}. We've emailed your renewal terms. Please reply or call {office_phone} to confirm you'd like to renew or to discuss changes.

## D-7 SMS

> Hi {first_name}, {brokerage_name} here. Your {policy_class} cover ends on {expiry_date} and we haven't received your instructions yet. Please call {adviser_name} on {office_phone} today.

Do not say the client "will be uninsured": whether cover continues depends on the insurer and the policy.

## Instructions confirmation

> Thanks {first_name}. Confirming your instruction on {date}: {renew_as_quoted / renew_with_changes / do_not_renew}. {next_steps_and_payment_details}. If this isn't right, reply to this message.

An instruction not to renew is confirmed in writing, and the account manager is told.

## After expiry

The account manager decides. The agent drafts only once cover status is confirmed with the insurer:

> Hi {first_name}, your {policy_class} policy with {insurer} expired on {expiry_date} and we have not received instructions to renew. {status_confirmed_by_insurer}. Please call {adviser_name} on {office_phone} if you'd like to arrange cover.

## Stop rules

Stop the cadence immediately when:

- the client gives instructions (renew, change or lapse);
- the client opts out of a channel (stop that channel; record it within the day; honour unsubscribes within 5 working days at most);
- the client asks not to be called (add to the organisation's do-not-contact list);
- a complaint is raised (route to the licensee's complaints process; pause automated touches);
- the client is deceased, in hardship or vulnerable (a person takes over).
