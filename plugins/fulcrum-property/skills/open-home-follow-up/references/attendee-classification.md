# Attendee classification

Classify on observable signals. Write the deciding signal next to each class. If the agent has no notes for someone, use register data only and mark the class `provisional`.

## Classes

| Class | Meaning | Follow-up window |
| --- | --- | --- |
| Hot | Likely to make an offer or register for auction within two weeks | SMS within 1 hour of close, agent call same day |
| Warm | Genuinely in the market and this property is on their list, but something is unresolved | Same day, before 7pm |
| Cold | In the market, but this property does not fit | Same day or next morning |
| Just looking | Not buying now: neighbours, curious locals, very early browsers | One thank-you, no cadence |

## Signals

**Hot (any two, or one strong signal marked with a star)**
- Asked for the contract or vendor disclosure documents (star).
- Asked how offers are being handled, the auction terms or the deposit (star).
- Second inspection, or brought a builder, parent or partner on a return visit (star).
- Has finance approval or has sold, and said so unprompted.
- Asked about settlement period, building and pest timing or strata records.
- Stayed well over the average time and measured rooms or checked specific fittings.

**Warm**
- Asked a specific question that needs an answer (council rates, strata levies, school zone, noise).
- Positive about the property but named a blocker: price, layout, needs to sell first.
- First visit, but has been at other comparable open homes the agent knows of.

**Cold**
- Said the property does not fit (too small, wrong street, needs too much work) without a way round it.
- Price reaction well above their stated budget.

**Just looking**
- Lives in the street or nearby and said so.
- Said they are "just starting to look" with no timeframe.
- Investor "keeping an eye on the area" with no question about this property.

## Tie-breaks and edge cases

- Conflicting signals: take the lower class and note the higher signal, so the agent can override.
- Couples who signed in separately: one record, one class, one message to the person whose mobile was given for contact.
- A known buyer from the CRM who missed out on another listing: raise one class if they asked anything specific.
- Nearby owner who mentions selling: class Just looking for this property, but create a separate task for the agent ("possible appraisal lead"). Do not send an appraisal pitch unless they have consented to marketing.
- Builder, developer or buyer's agent: class on their stated intent, and note the role; buyer's agents get a professional email, not a consumer SMS.
- No notes, contract not requested, first visit: Warm (provisional) if they left both mobile and email, otherwise Cold (provisional).

## Recording price feedback

- Record what was said, in words: "felt the guide was on the high side", "comparing with the house on the next street that sold last month".
- Never convert a reaction into a number. If the attendee named a figure, record it exactly with the attendee's own words and mark it "attendee figure".
- Do not share one attendee's price feedback with another attendee.
