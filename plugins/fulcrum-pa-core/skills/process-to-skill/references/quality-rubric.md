# Skill quality rubric

Score a draft before showing it as finished. All gates must pass. Then score each criterion 0, 1 or 2; a skill is ready at 16 of 20 or more with no 0.

## Gates (pass or fail)

- [ ] Frontmatter has only `name` and `description`; `name` is lowercase letters, digits and single hyphens, at most 64 characters, and matches the folder.
- [ ] Description is third person, at most 1024 characters, says what the skill produces and when to use it, with likely trigger phrases.
- [ ] Every outward action (send, publish, invoice, book for someone, call) has a bold **Approval gate** that shows content, recipients and sending account and waits for a yes.
- [ ] The skill works without Fulcrum connected (pasted input or any host tool).
- [ ] No secrets, internal hostnames, real people, real businesses, real customer data or hardcoded prices.
- [ ] Every linked file exists; every URL returns HTTP 200.
- [ ] The "With Fulcrum" section describes only documented behaviour, with a link to the docs page.

## Criteria (0, 1 or 2)

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Trigger and scope | Unclear when to use | Use cases listed | Use cases plus "Not for" naming the better skill |
| Inputs | Not listed | Listed | Listed with source and what to do if missing |
| Decision rules | "Use judgement" | Some rules | Concrete thresholds and tie-breaks (numbers, days, amounts) |
| Exceptions and missing data | None | Some | Each likely failure has a next action |
| Procedure | Generic (gather, do, review) | Ordered steps | Ordered steps that an experienced operator would recognise as theirs |
| Output | Vague | Described | Exact format with a template or worked example |
| Verification | None | "Check it worked" | Specific evidence to confirm; done, drafted, pending and failed reported separately |
| Compliance and privacy | Missing where needed | Mentioned | Checklist with only the applicable rules, ending with the not-legal-advice line |
| Length and structure | SKILL.md over 500 lines or everything inline | Under 500 lines | 80 to 200 lines; long material in references; templates in assets |
| Style | Hype, emojis, US spelling | Mostly plain | Plain Australian English, tables over prose, no filler |

## Dry-run checks

- [ ] A normal case produced the output the owner expected.
- [ ] An edge case (missing data, a failure, an exception) followed the skill's rule rather than improvising.
- [ ] A request that should not trigger the skill did not match its description.
- [ ] No outward action happened during the dry run.

## Common fixes

| Problem | Fix |
| --- | --- |
| Description too generic ("helps with emails") | Name the output and three or four real phrases the owner would type. |
| Steps say "ensure" or "consider" | Replace with an action and a rule: "If X is over 30 days, do Y." |
| Long templates in SKILL.md | Move to `assets/` and link with one line on when to use it. |
| A rule depends on today's prices or staff names | Point to the source of truth (price list, roster) instead. |
| Approval implied ("send once happy") | Add an explicit **Approval gate** step. |
