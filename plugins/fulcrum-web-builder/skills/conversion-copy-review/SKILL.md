---
name: conversion-copy-review
description: Reviews and rewrites website and landing-page copy and calls to action for clarity and conversion, returning a before/after table with the reason for each change. Applies the five-second clarity test (what it is, who it is for, why act now), specificity over adjectives, one primary call to action per view, outcome-based button labels, objection handling, proof placement, reading level and scannable headings, plus an Australian Consumer Law check for misleading claims, unsubstantiated superlatives and GST-inclusive consumer prices. Includes a ban list of generic AI-sounding phrases and a copy-lint script. Use when someone asks to "review our copy", "rewrite the hero", "improve conversions", "better CTA", "make this less generic", "does this headline work", or "check our claims".
---

# Review and rewrite conversion copy

Turns vague, self-focused or risky marketing copy into specific copy that tells the right reader what they get and what to do next, and that the business can stand behind. The endpoint is a before/after table with rationale, a list of claims needing evidence, and the rewritten copy ready to drop into the page. Publishing the copy is a separate, approved step.

## When to use

- A hero, landing page, product page, pricing page, email capture or ad landing page needs review before launch or after poor results.
- Copy reads as generic, written by a template or an AI, or makes claims nobody has checked.
- Not for: campaign planning across channels (`fulcrum-campaign-brief`), long-form article editing (`fulcrum-document-review`), visual design (`anti-slop-design-review`), or page structure from scratch (`landing-page-build`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The copy, in page order, including buttons, form labels, microcopy and meta title | Page source, CMS, design file, pasted text | Ask for the full page; a headline alone cannot be judged in context. |
| Audience and the one action wanted | Brief, owner | Ask once; otherwise infer from the primary button and state the assumption. |
| Real proof: numbers, reviews, case results, credentials | Owner, CRM, review platforms | Mark proof slots `[PROOF NEEDED]`; never invent. |
| Customer language: reviews, sales-call notes, support tickets, search terms | Owner, CRM, review sites | Without it, mark rewrites as hypotheses to test. |
| Prices and offer terms | Pricing page, owner | Do not restate prices; reference the pricing page. |

## Procedure

1. **Run the five-second test** on the first screen only. Write down what a stranger would answer to: What is this? Who is it for? Why act now (or what happens if I click)? Any blank or wrong answer is the first finding.
2. **Lint the draft.** Run `python3 scripts/copy_lint.py copy.md`. It flags phrases from [references/slop-phrases.md](references/slop-phrases.md), claims needing evidence, long sentences, reading level and the "you" to "we" balance. Treat the output as leads; judge each in context.
3. **Review section by section** against these rules (details and patterns in [references/rewrite-patterns.md](references/rewrite-patterns.md); read it before rewriting):
   - **Specific beats adjectives.** Replace every adjective that could describe a competitor ("fast", "easy", "powerful") with the fact behind it ("quotes back in 4 business hours").
   - **One primary action per view.** One visually primary button per screenful. Secondary actions are quieter and lower commitment.
   - **CTA label = outcome.** Button text completes "I want to...": "Get my fixed quote", not "Submit". The same action keeps the same label everywhere.
   - **Headings scan as a story.** Read only the headings; they should carry the argument (problem, outcome, how, proof, offer). Replace label headings ("Features", "Why us") with claims.
   - **Objections answered where they arise.** Price near the price, risk near the button, effort near "how it works".
   - **Proof next to the claim it supports**, attributed and specific: name, role or suburb (with permission), number with source and date.
   - **Reader first.** More "you" than "we"; benefits first, features as evidence.
   - **Reading level.** Consumer pages at about Year 8 or lower; specialist B2B can go higher but sentences stay under about 25 words.
4. **Check claims** against the Australian Consumer Law checklist in Guardrails. Every superlative, comparison, "free", "guaranteed", environmental or origin claim either has evidence on file, is rewritten, or is removed.
5. **Rewrite.** Keep the brand's voice and any legally required wording. Give two options for the hero headline and primary CTA when the right answer depends on a test.
6. **Approval gate.** If asked to publish the copy to a CMS, site or ad platform, show the exact text per location, the account or environment, and any claims still awaiting evidence; wait for an explicit yes.

## Output

1. Five-second test result (three answers, then the verdict).
2. Before/after table:

| # | Location | Before | After | Rule applied | Why it should convert better |
| --- | --- | --- | --- | --- | --- |
| 1 | Hero H1 | Unlock seamless scheduling for your business | Fill tomorrow's cancellations before 9 am | Specific outcome, no slop | Names the result and the moment of value; the visitor can picture it |
| 2 | Hero button | Submit | Book a 15-minute demo | CTA = outcome | Sets expectation of time and next step |

3. Claims register: claim, location, evidence needed, status (supported, rewrite, remove).
4. Rewritten copy in page order, ready to paste, with `[PROOF NEEDED]` markers where applicable.
5. Test suggestions: the one or two changes worth A/B testing, with the metric.

## Check before you finish

- [ ] Every "after" line is more specific than its "before", or shorter with no loss of meaning.
- [ ] No banned phrase remains unless justified in the table.
- [ ] No invented numbers, quotes, logos or results; every proof slot is real or marked.
- [ ] Every claim in the register has a status.
- [ ] Drafted and published are reported separately; nothing was published without approval.

## Guardrails

Australian Consumer Law checklist for marketing copy:

- [ ] No statement is likely to mislead the reader overall, including through the headline, the image or what is left out. Fine print does not contradict the headline.
- [ ] Superlatives and comparisons ("fastest", "cheapest", "#1", "best-rated") have current evidence the business can produce; otherwise they are removed.
- [ ] Prices shown to consumers display the single total price including GST and any compulsory fees, at least as prominently as any part-price.
- [ ] "Free" offers state any conditions clearly next to the claim. "Was/now" or savings claims use genuine former prices.
- [ ] Testimonials and reviews are genuine, from real customers, not edited to change meaning, and used with permission. Negative reviews are not hidden selectively in a way that misleads.
- [ ] Guarantees do not imply that customers lose their consumer guarantee rights.
- [ ] Environmental, health and "Australian made/owned" claims are specific and substantiated.
- This is a practical checklist, not legal advice.

## With Fulcrum

If the copy lives in a code repository, Fulcrum Code can apply the agreed rewrites. Ask it to change only the text you approved, keep the existing design, and show the diff before committing ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)).

## Learn more

- [Building landing pages via Cortex](https://fulcrumcortex.com/blog/building-landing-pages-via-cortex)
- [Fulcrum Code: plan, build and review a change](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)
