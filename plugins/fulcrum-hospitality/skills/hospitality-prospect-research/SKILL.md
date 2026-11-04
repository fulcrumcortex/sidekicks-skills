---
name: hospitality-prospect-research
description: "Researches hotels, motels, resorts, restaurants and event venues as sales prospects and delivers an evidence-backed spreadsheet: agreed criteria, public evidence with a source URL and date for every claim, a scoring rubric (booking system maturity, target-market fit, size, recent activity), de-duplication, tiers, and an optional load into the CRM after confirmation. Use when someone asks to 'build a prospect list of hotels', 'find restaurants in [area] that take bookings by phone', 'research venues for outreach', 'score these hospitality leads', or 'load the prospects into the CRM'. Uses only public information, never guesses email addresses, and checks Spam Act and Do Not Call obligations before any outreach. Works with web search and a spreadsheet; uses Fulcrum CRM when connected."
---

# Research hospitality prospects with evidence

Builds a list of hospitality businesses worth contacting, where every claim can be checked by clicking its source. A smaller list with evidence beats a long list of guesses: the sales team can open each row and see why it scored the way it did. The endpoint is a scored, de-duplicated CSV or spreadsheet and, after confirmation, records in the CRM.

## When to use

- Building a new territory or segment list (for example "motels with 20 to 60 rooms on the north coast with no online booking").
- Scoring or cleaning a list someone else compiled, before outreach.
- Not for: writing the outreach campaign itself (use `fulcrum-campaign-brief`); cleaning existing CRM records (use `fulcrum-crm-data-cleanup`); calling the prospects (use `fulcrum-voice-agent-setup` for the agent, and the compliance checklist below first).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| What is being sold and to whom (ideal customer) | The user | Ask once. The rubric depends on it. |
| Geography, categories, size range, exclusions (existing customers, chains, competitors' clients) | The user | Propose defaults from the ideal customer and confirm before researching. |
| Target list size and time budget | The user | Default to 25 qualified rows, then check in. |
| Existing CRM records or customer list, for exclusion and de-duplication | CRM export | Warn that duplicates against the CRM cannot be checked. |
| Web search and page access | Host tools | Without them, score only a list the user supplies. |

## Procedure

1. **Agree the criteria and rubric.** Write the ideal customer in one paragraph, the must-haves (category, region, size band), the exclusions, and the rubric from [references/scoring-rubric.md](references/scoring-rubric.md) with any weight changes. Get a yes before researching.
2. **Find candidates** from public sources: the business's own website, its booking page, state tourism and visitor-centre directories, industry association member lists, local council business listings, maps listings and online travel agency or dining platform listings. Record each source URL.
3. **Gather evidence per dimension.** For each claim, record what was observed, the URL and the date viewed. Observed means seen on the page ("Book now button opens a third-party booking engine"; "Conference page lists 3 meeting rooms"), not inferred. When evidence is missing, leave the score blank, not zero, and note "not found".
4. **Contact details.** Record only contact details the business itself publishes (phone, general email, contact form URL), with the page they came from. Never construct or guess an email address from a name or a pattern, never use paid or scraped personal lists, and do not record personal mobile numbers of staff found on social media.
5. **Fill the sheet** using [assets/prospects-template.csv](assets/prospects-template.csv). One row per business location. Chains: one row per property, with the group noted.
6. **De-duplicate and score.** Run `python3 scripts/dedupe_score.py prospects.csv > scored.csv`. It merges rows with the same website or the same name and postcode, keeps every source URL, scores with the agreed weights, and holds rows with scores lacking evidence, emails without a source, or stale evidence. Also compare against the CRM export: existing contacts and companies are marked "existing", not re-added.
7. **Review the holds and the top tier by hand.** Open three random A-tier rows and confirm the evidence still says what the sheet says. Fix or downgrade anything that does not hold up.
8. **Deliver** the scored sheet with a one-page summary: criteria, sources used, row counts (found, excluded, duplicates merged, held, by tier), and caveats.
9. **Approval gate (CRM load).** Before loading, show: the number of records, the fields mapped, the owner they will be assigned to, the list or tag they go into, and which rows are excluded as existing or held. Wait for an explicit yes. Load a sample of 5 first, check them in the CRM, then load the rest. After a timeout, check what was created before retrying, because a repeated import can create duplicates.
10. **Before outreach** (not part of this skill's sending): hand over the compliance checklist below with the list.

## Output

- `scored.csv`: template columns plus total score, percentage, tier (A, B, C, HOLD), merged rows and flags.
- Summary: criteria, sources, counts, top 10 with one-line reasons, caveats.
- After an approved load: records created, skipped and failed, with the list or tag name.

## Check before you finish

- [ ] Every scored dimension has a URL and a date; blank means not found, not zero.
- [ ] No email address appears without the page it was published on.
- [ ] Duplicates are merged and existing CRM records are excluded.
- [ ] Three A-tier rows were spot-checked against their sources.
- [ ] The CRM load (if any) was approved, sampled and verified, with counts reported.

## Outreach compliance checklist

- [ ] Email: the Spam Act needs consent. For a cold email, inferred consent can rest on an address the business conspicuously published, only when the message relates to the business's or role's function and the publication does not say unsolicited messages are unwanted. Otherwise, do not email.
- [ ] Every commercial message identifies the sender and has a working unsubscribe honoured within 5 working days.
- [ ] Calls: wash numbers against the Do Not Call Register yourself or through an access seeker unless an exemption applies. Business numbers can be registered too.
- [ ] Telemarketing hours: weekdays 9am to 8pm, Saturday 9am to 5pm, no Sundays or national public holidays, in the recipient's time zone.
- [ ] Recording: follow state call-recording consent rules and disclose recording at the start of the call.
- [ ] Privacy: keep only business contact details needed for the outreach; record where each came from.

This is a practical checklist, not legal advice.

## Guardrails

- Public information only. Do not log in, bypass paywalls, or use data from a source whose terms forbid this use.
- Record what a page says, not what you assume. "No online booking found on the website" is evidence; "they have no booking system" is a guess.
- Do not describe a prospect negatively in fields that may be shared ("outdated", "struggling"); use neutral observations.

## With Fulcrum

- Add companies from their website addresses, and contacts only for published business contacts. See [Contacts and companies](https://fulcrumcortex.github.io/documentation/crm/contacts-and-companies/).
- Fulcrum CRM's CSV import creates a new contact for every row and does not check for duplicates; you become the owner; the company column goes into the contact's description rather than linking a company record. De-duplicate first and merge afterwards if needed. See [Import, export and duplicates](https://fulcrumcortex.github.io/documentation/crm/import-export-and-duplicates/).
- Put the researched cohort in a static list so it stays fixed for the campaign. See [Lists](https://fulcrumcortex.github.io/documentation/crm/lists/).
- If calling, Lyre checks your organisation's own do-not-contact list and calling hours; it does not wash numbers against the Do Not Call Register.

## Learn more

- [AI prospect research: build a list from evidence](https://fulcrumcortex.com/blog/ai-prospect-research)
- [Import, export and duplicates in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/import-export-and-duplicates/)
