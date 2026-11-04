---
name: ux-critique
description: Produces a structured UX critique of a screen, user flow or component, scoring each issue for severity on a 0 to 4 scale and giving a concrete redesign suggestion for each, not vague advice. Uses Nielsen's ten heuristics adapted for modern web, a task-flow friction count, information hierarchy, affordances, empty, loading and error states, form UX, microcopy, consistency and accessibility touchpoints. Use when someone asks for a "UX review", "critique this screen", "heuristic evaluation", "why are users dropping off", "is this flow confusing", "review the checkout", "onboarding feedback", or shares a screenshot, Figma frame or URL and asks what to improve.
---

# Critique a screen, flow or component

Gives a design team a ranked list of usability problems with evidence and a specific fix for each, so the next iteration is obvious. The endpoint is a written critique (and, if asked, annotated screenshots or a revised wireframe description). It is an expert review, not a substitute for testing with real users; it says which findings most need user testing.

## When to use

- Reviewing a screen, a multi-step flow (sign-up, booking, checkout, onboarding) or a component before build or after poor metrics.
- A stakeholder says "it feels clunky" and the team needs specifics.
- Not for: WCAG conformance (`accessibility-audit`), copy rewriting in depth (`conversion-copy-review`), visual distinctiveness (`anti-slop-design-review`), or layout breakage across devices (`responsive-qa`).
- Hand-offs: implement the agreed fixes as a reviewable change with `fulcrum-code-change`, and verify an authorised release with `fulcrum-release-check`.

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The artefact: URL, screenshots of every step and state, Figma frames, or a running build | Requester | Ask for the missing states (error, empty, loading). Critique only what you can see and list the rest as "not reviewed". |
| The user and their goal ("a returning customer rebooking a service on mobile") | Requester, personas, analytics | State an assumed user and goal and mark it as an assumption. |
| Business goal and success metric | Requester | Infer from the primary action; say so. |
| Evidence: analytics funnel, recordings, support tickets, test notes | Product owner | Proceed as expert review; flag which findings need validation. |

## Procedure

1. **Frame the task.** Write one line: user, goal, starting point, success state. Every finding ties back to this. Critiquing "the page" without a task produces taste, not usability findings.
2. **Walk the flow as the user**, step by step, at the real device size (mobile first if most traffic is mobile). Capture each screen and state. Note where you hesitated, guessed, scrolled to find something, or re-read.
3. **Count friction** for the task using the method in [references/heuristics-rubric.md](references/heuristics-rubric.md): screens, decisions, fields, taps, waits, context switches and points where information must be remembered. Compare with the minimum the task truly needs; the gap is the redesign opportunity.
4. **Evaluate against the ten heuristics** (adapted list and probing questions in the rubric; read it during this step). For each problem, record the heuristic, where it occurs, what the user experiences, and why it matters for the goal.
5. **Check hierarchy and affordance on each screen.** The squint test: blur the screenshot; the primary action and the main message should still stand out. Is there exactly one primary action? Do clickable things look clickable and static things look static? Does the order of content match the order of the user's questions?
6. **Check every state.** First use (empty), loading (skeleton vs spinner vs nothing), partial data, error (network, validation, permission, not found), success, and the "returning user" state. Missing states are findings.
7. **Forms and microcopy.** Labels, field count, input types, inline validation timing, error wording, defaults, the button label, and what happens after submit. Use the form and microcopy checklists in the rubric.
8. **Consistency and accessibility touchpoints.** Same component, same behaviour; terminology consistent with the rest of the product; obvious accessibility issues (contrast, target size, focus, labels) noted with a pointer to `accessibility-audit` for a full pass.
9. **Score severity 0 to 4** for each issue (scale below), combining frequency, impact and persistence. Then order by severity, then by effort.
10. **Write the fix for each finding as a design change** someone can build: what moves, what is removed, the new label, the new state. "Improve clarity" is not a fix; "Replace the three equal buttons with one primary 'Confirm booking' button and move 'Change time' to a text link above the summary" is.

## Severity scale

| Score | Meaning | Typical example |
| --- | --- | --- |
| 0 | Not a usability problem (disagreement or preference) | Prefers a different illustration style |
| 1 | Cosmetic: fix if time allows | Inconsistent icon weight |
| 2 | Minor: slows users or causes brief confusion | Ambiguous secondary label, recoverable on second look |
| 3 | Major: frequent failure, abandonment or wrong outcome likely; fix before release | Error message clears the form; primary action below the fold on mobile |
| 4 | Catastrophe: blocks the task or causes harm (lost money, data, wrong booking) | Payment taken twice on retry; no way to cancel a booking |

## Output

Use [assets/critique-template.md](assets/critique-template.md). It contains:

1. Task frame and scope (screens and states reviewed, device, what was not reviewed).
2. Top three changes with the biggest expected effect, in one paragraph each.
3. Friction count table: before, and the proposed after.
4. Findings table: `# | Severity | Heuristic | Screen / state | Problem (what the user experiences) | Evidence | Redesign suggestion | Effort (S/M/L)`.
5. Missing states list.
6. What is working (brief, so it is kept in the next version).
7. Questions for user testing: the findings that rest on assumptions.

## Check before you finish

- [ ] Every finding has a severity, a location and a concrete redesign suggestion.
- [ ] Severity 3 and 4 findings are justified by the task, not personal taste.
- [ ] Missing states are listed; unreviewed screens are named.
- [ ] Assumptions about users are labelled, with a suggested way to test them.

## Guardrails

- Critique the design, not the designer. Write findings neutrally.
- Screenshots and recordings may contain customer data; use fictional test accounts and blur real names, emails and phone numbers before sharing.
- Do not prescribe a full redesign when a targeted fix solves the problem; reserve "rethink the flow" for severity 3 or 4 structural problems and explain why.

## With Fulcrum

If the screen is built in your repository, Fulcrum Code can turn agreed findings into changes. Paste a cropped screenshot of the screen for context, describe the change from the findings table, and review the diff before committing ([Voice, images and editor](https://fulcrumcortex.github.io/documentation/code/voice-images-and-editor/), [Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)).

## Learn more

- [Fulcrum Code: plan, build and review a change](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)
- [Fulcrum Code: voice, images and editor](https://fulcrumcortex.github.io/documentation/code/voice-images-and-editor/)
