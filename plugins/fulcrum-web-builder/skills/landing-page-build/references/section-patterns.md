# Landing page section patterns

Each section has one job. If you cannot say the job in one sentence, the section is not ready. Pick one layout per section; vary layouts between adjacent sections so the page does not read as a stack of identical blocks.

## Hero: one promise

**Job:** in five seconds, tell the visitor what they get, that it is for them, and what to do next.

| Element | Rule |
| --- | --- |
| Eyebrow (optional) | Audience or category, 2 to 5 words: "For physiotherapy clinics". |
| H1 | The outcome, not the product category. About 6 to 12 words. "Fill tomorrow's cancelled appointments before 9 am", not "Smart scheduling software". |
| Subhead | How, and for whom, in one sentence of at most about 25 words. Names the mechanism. |
| Primary CTA | Outcome label: "Book a 20-minute walkthrough", "Get my quote". One per hero. |
| Secondary action (optional) | Lower commitment and visually quieter: "See how it works" (anchor link). Never a second competing conversion. |
| Proof near the CTA | One real item: a rating with source and count, a client count, a regulatory registration. If none exists, omit. |
| Visual | The product or the result in use. A real screenshot or photo beats an abstract illustration. |

Layouts that work:
- **Split 7/5:** copy left, product visual right, visual bleeding off the grid edge. Good for software.
- **Type-led:** oversized H1 across 9 to 10 columns, no image, proof strip directly underneath. Good when the visual is weak.
- **Full-bleed photo with scrim:** for physical services (trades, hospitality). Keep text on a solid or 60%+ opacity scrim so contrast holds on every crop.

Avoid: centred H1 + centred paragraph + two equal buttons + floating 3D blob. That is the template look.

## Proof strip

**Job:** lower the risk of reading further.

- Use specific, attributable proof: "4.8 from 312 Google reviews", "Licensed electrician, NSW licence 000000C (fictional)", named logos with permission.
- 3 to 6 logos maximum, greyscale or one tone, same optical height. Link nothing; logos are not navigation.
- A single strong quote with a name, role and organisation beats a carousel of six vague ones. Quotes need written permission.
- Placement: immediately below the hero, and again next to the final CTA.

## Problem and outcome

**Job:** show you understand the visitor's situation in their words.

- Two columns ("Today" / "With us") or a short before/after list of 3 items each.
- Each line is concrete and measurable where possible: "Chasing three suppliers by phone for one quote" / "One form, quotes back the same day".
- Do not insult the reader or exaggerate pain.

## How it works

**Job:** remove the fear of effort.

- Exactly 3 steps (4 if a step is genuinely separate). Number them. Each has a verb-led title and one sentence.
- Use an ordered list (`<ol>`) so screen readers announce the count.
- Layout alternatives to the three-card row: a vertical timeline with a connecting rule, or a single annotated screenshot with numbered callouts.

## Feature or benefit detail (optional)

**Job:** answer "will it do the thing I need?"

- Alternate image and text rows, or one bento grid where cell size reflects importance (one large cell, two to four small). Do not make every cell equal.
- Each item: benefit headline, one sentence, a real screenshot crop.

## Offer

**Job:** make the next step and its cost clear.

- State exactly what happens after the click: "We call within one business day, then send a fixed quote."
- If prices are shown to consumers, show the total including GST and compulsory fees. If prices change often, link to the pricing page rather than duplicating figures.
- Risk reversal only if real: trial length, cancellation terms, guarantee wording approved by the client.

## Objections and FAQ

**Job:** answer the questions that stop a conversion, not pad the page.

- 4 to 8 questions sourced from sales calls, support tickets or reviews. If you have none, ask the client for the five questions prospects ask most.
- Use `<details>` and `<summary>`; the first question can be open. No JavaScript accordion needed.
- Answer in the first sentence, then add detail. Link to policy pages where relevant.
- FAQPage JSON-LD no longer earns Google rich results (retired in 2026). Add it only if another consumer of the markup needs it, and only for questions visible on the page.

## Final call to action

**Job:** catch the visitor who scrolled to the end.

- Repeat the primary CTA with the same label as the hero. Add one line restating the outcome and one proof item.
- If the form lives here, keep the hero CTA as an anchor link to it (`href="#enquire"`), with `scroll-margin-top` so a sticky header does not cover the heading.

## Footer

- Business name, ABN where the business normally displays it, contact details, privacy policy, terms. Keep NAP (name, address, phone) identical to the Google Business Profile for local businesses.

## Sticky header and mobile CTA

- A sticky header may carry the primary CTA once the hero CTA scrolls out of view. Keep it under about 64 px tall on mobile and make sure focused elements are never hidden beneath it (WCAG 2.4.11): use `scroll-padding-top` on `html`.
- A bottom sticky CTA bar on mobile must not cover form fields or the cookie notice, and must respect `env(safe-area-inset-bottom)`.
