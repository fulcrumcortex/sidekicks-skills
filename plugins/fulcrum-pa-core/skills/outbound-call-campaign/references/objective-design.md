# Designing the call objective

An objective tells the agent what a successful call looks like, what to find out, what it must never do and how to open. Write it so a new staff member could make the same call from it.

## Template

```text
Name: <campaign purpose, e.g. "Spring service reminder - lapsed customers">
Goal: <one sentence: the outcome that counts as success, e.g. "Book a service visit in the next 21 days, or record when the customer wants to be called back.">
Information to collect (3 to 5 items, in priority order):
  1. <item> - <why it is needed>
  2. ...
Guardrails:
  - <what the agent must not say or do>
Opening line: <after the disclosure; personalised with {{name}} and {{agent_name}}>
Responses:
  Not now            -> <offer a callback time; record it>
  Not interested     -> <thank them, end, record "Not interested">
  Stop calling me    -> <confirm no further calls, end, record "Do not call">
  Who is this?       -> <business name, purpose, where the number came from>
  I want a person    -> <how escalation works and when they will hear back>
  Wrong person       -> <apologise, do not explain the purpose in detail, end>
  Voicemail          -> <one message or none; see cadence reference>
Completion rule: <when the agent should wrap up>
```

## Rules for each part

**Goal.** One measurable outcome. "Have a chat about our services" is not a goal. If the user cannot say what success looks like, ask before going further.

**Information to collect.** Three to five items. Each one must be needed for the next step. Every extra question lowers completion and raises privacy risk. Order them so the most valuable answer comes first in case the call ends early.

| Use case | Typical items |
| --- | --- |
| New enquiry qualification | Need or problem, timing, budget range, decision-maker, preferred next step |
| Lapsed customer re-engagement | Still at the address or business, current need, best time for a visit, preferred contact channel |
| Appointment confirmation | Confirm date and time, any access notes, reschedule preference if not suitable |
| Event follow-up | Session attended, interest level, whether they want information or a meeting |
| Renewal reminder | Aware of renewal date, intention to renew, questions for a person |

**Guardrails.** Write them as concrete prohibitions. Good guardrails:

- Do not quote prices, discounts or availability. Say a person will confirm in writing.
- Do not promise outcomes, results or timeframes.
- Do not ask for card numbers, bank details, Medicare numbers, dates of birth or passwords.
- Do not discuss any health, disability or financial hardship matter; offer a call from a person instead.
- Do not say or imply that you are a person.
- Do not argue. After one "no", thank them and end.
- Do not call back the same day after a decline.

Weak guardrails ("be compliant", "be nice") change nothing. A guardrail written in a prompt is not proof that every calling path enforces it, so test each one in the pilot.

**Opening line.** The disclosure plays first if the platform supports it. The opening line then gives the agent's name, the business and the purpose in one or two sentences, and asks permission to continue.

- Good: "Hi {{name}}, it's {{agent_name}} from Banksia Bay Plumbing. You had a hot water service installed with us a while back, and I'm calling to see if you'd like to book this year's check. Is now an OK time?"
- Weak: "Hi {{name}}, how are you today?" (no business, no purpose, sounds like a cold call).
- Never: anything that suggests an existing relationship that does not exist, urgency that is not real, or a prize.

## Outcome definitions

Agree these before launch so the review and CRM write-back are consistent.

| Outcome | Meaning | Final? |
| --- | --- | --- |
| Booking made | A time is agreed and a calendar entry or booking record exists | Yes |
| Lead captured | Required information collected, next step is a person | Yes |
| Callback requested | The person asked to be called at a stated time | No, schedule it |
| Not the decision maker | Spoke to someone else; record who to ask for if offered | Yes for this number |
| Not interested | Clear decline | Yes |
| Do not call | Asked not to be called again | Yes, suppress |
| Escalated to human | Needs a person; record why | Yes for the agent |
| No answer / voicemail / busy | No conversation | No, eligible for retry |
| Wrong number | Number does not belong to the person | Yes, fix or remove the number |

## Worked example (fictional)

Banksia Bay Plumbing wants to re-engage 400 customers who had a hot water service installed two or more years ago.

```text
Name: Hot water service check - 2+ years
Goal: Book a service check in the next 21 days, or record a callback time.
Information to collect:
  1. Still at the installation address (yes/no)
  2. Any current issues with the system (free text, short)
  3. Preferred day and time window for a visit
Guardrails:
  - Do not quote prices; say the office confirms the price by SMS before the visit.
  - Do not diagnose faults; any leak, smell of gas or electrical issue -> tell them to call the office or emergency services now, record "Escalated to human".
  - Do not say or imply you are a person.
  - After one decline, thank them and end.
Opening line: Hi {{name}}, it's {{agent_name}} from Banksia Bay Plumbing. You had a hot water system installed with us a couple of years ago, and I'm calling to see if you'd like to book a service check. Is now an OK time?
Completion rule: once a time is booked or declined, confirm what happens next and end the call.
```

Pilot result to look for: a booking rate per connected call that the user is happy with, zero guardrail breaches, and every "gas smell" style answer escalated.
