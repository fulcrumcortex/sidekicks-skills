---
name: process-to-skill
description: Turns a recurring business process into a reusable Sidekick skill. It interviews the owner (or reads an existing SOP, checklist or recorded walkthrough), maps the trigger, inputs, decisions, approvals, exceptions and checks, then writes a SKILL.md with references and templates in this repository's conventions, scores it against a quality rubric and dry-runs it on a realistic case. Use when the user says "teach the assistant how we do X", "turn this SOP into a skill", "write a skill for our quoting process", "make this repeatable", "document how I onboard clients so the AI can do it" or "create a Sidekick skill". Works in any host that loads Agent Skills; can install the result as a local Fulcrum Code skill.
---

# Teach a process once, as a Sidekick skill

Captures how this business does a recurring job, in enough detail that a Sidekick can do it the same way next time and knows where to stop and ask. The endpoint is a reviewed skill folder (or a single local skill file) that passes the quality rubric and one dry run, saved where the owner approved.

## When to use

- A task the owner or team does at least monthly, with a clear trigger and a clear finished state.
- An SOP, checklist, training document, screen recording transcript or long chat explanation that should become repeatable.
- Improving an existing skill after it produced a wrong result.
- Not for: doing the process right now (do the task, then offer to capture it); one-off projects (use `fulcrum-project-planning`); processes that are mostly personal judgement with no rules (capture a checklist instead and say why).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The process name and who does it today | The owner | Ask. |
| A source of truth | The owner's answers, an SOP document, a past example | Interview using the question bank. |
| One or two real past examples | Email threads, CRM records, files | Ask for one; replace all names and figures with fictional ones in the skill. |
| Where the skill will live | The owner | Ask: this skills repository (public library) or a private local skill. |
| Tools available to the Sidekick | Connected mail, calendar, CRM, files | The skill must still work with pasted material. |

## Procedure

1. **Check fit.** Confirm the process recurs, has a trigger, a finished state and some rules. If it fails two of these, stop and offer a checklist instead.
2. **Collect the method.**
   - From an owner: run the interview in rounds of no more than five questions, using [references/interview-question-bank.md](references/interview-question-bank.md). Start with "walk me through the last time you did this", not with abstractions.
   - From an SOP: read it fully, then list gaps using the SOP gap check in the same file (vague thresholds, missing owners, unstated approvals, no definition of done). Ask only about the gaps.
3. **Map it** on [assets/process-map.md](assets/process-map.md): trigger, inputs and their sources, ordered steps, decision rules with numbers, outward actions, exceptions and what to do when data is missing, verification, output, and neighbouring tasks that are out of scope.
4. **Teach back.** Show the owner a one-page summary in plain words: "When X happens, I will..., I will stop and ask you before..., I will know it worked when...". Correct it until the owner says it is right. This is the most important step; do not skip it.
5. **Write the skill** from [assets/skill-template.md](assets/skill-template.md) following [references/skill-conventions.md](references/skill-conventions.md): a name that matches the folder, a third-person description that covers what and when with trigger phrases, a short SKILL.md (aim for 80 to 200 lines), long material in `references/`, fill-in templates in `assets/`, and a `scripts/*.py` helper only where deterministic logic helps (calculations, date maths, validation).
6. **Add approval gates.** Every step that sends email, SMS or chat, publishes, invoices, books for someone else or places a call becomes a bold **Approval gate** step that shows exact content, recipients and sending account and waits for a yes. Add "check sent items or history before retrying" after any send.
7. **Add compliance where it applies** as a checklist that ends with "This is a practical checklist, not legal advice." Only the rules that touch this process (Spam Act, Do Not Call Register, calling hours, recording consent, Privacy Act and APPs, NDIS standards).
8. **Sanitise.** Replace real people, businesses, addresses, phone numbers and amounts with obviously fictional ones (`example.com`, `0400 000 000`). Remove credentials, internal hostnames and customer data. Point to the source of truth for prices and rates instead of copying them in, so the skill does not go stale.
9. **Score it** with [references/quality-rubric.md](references/quality-rubric.md). Fix every failed gate and anything scoring 0, then re-score.
10. **Dry run.** Run the skill on one normal case and one edge case, using fictional inputs, with all outward actions held as drafts. Compare the result with what the owner would have done. Also check one request that should not trigger the skill. Fix and repeat once if needed.
11. **Approval gate: saving and publishing.** Show the file tree and the full SKILL.md, plus where it will be written. For this repository, prepare the change for review; opening a pull request or publishing is an outward action that needs an explicit yes. For a private skill, write it only to the folder the owner approved.
12. **Verify the install.** For a local Fulcrum Code skill, start a new session and check that it appears in `/skills`. For this repository, run `python3 scripts/validate.py` from the repository root if it exists, and check every link returns HTTP 200.

## Output

- The skill folder or file, ready for review.
- A short handover: what the skill covers, its approval gates, rubric score, dry-run results, and known limits or questions for the owner.

## Check before you finish

- [ ] The owner confirmed the teach-back summary.
- [ ] Every outward action in the process has an approval gate.
- [ ] Decision rules contain real thresholds, not "if urgent" or "when appropriate".
- [ ] The skill works without Fulcrum connected.
- [ ] No real names, customer data, prices or secrets remain (search the files before saving).
- [ ] The rubric gates pass and the dry run matched the owner's expected outcome.

## Guardrails

- A skill describes a method. It does not grant permissions, create credentials or install the tools it mentions; say so in the skill if the process depends on access the Sidekick may not have.
- Never encode a workaround for a control (skipping an approval, bypassing an unsubscribe, calling outside permitted hours) even if the owner does it that way today. Flag it instead.
- Keep the owner's private business knowledge out of the public repository; a process specific to one business belongs in a private skill.

## With Fulcrum

Fulcrum Code loads user skills from Markdown files in `~/.fulcrum/skills/`; the skill loader supports a name, description and body. Enter `/skills` to see available skills, and start a new session after changing skill files if they do not appear. Do not put tokens or customer details into a reusable skill ([Skills, Sidekicks and specialist agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/)). For a private local skill, write one self-contained Markdown file and fold short reference material into its body. Give Sidekicks clear tasks that name the outcome, the source of truth and the actions needing approval ([Cortex and Sessions](https://fulcrumcortex.github.io/documentation/sessions/)).

## Learn more

- [Skills, Sidekicks and specialist agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/)
- [Approval gates: when agents act and when humans decide](https://fulcrumcortex.com/blog/approval-gates-for-autonomous-agents)
- [Cortex and Sessions: directing your AI team](https://fulcrumcortex.github.io/documentation/sessions/)
