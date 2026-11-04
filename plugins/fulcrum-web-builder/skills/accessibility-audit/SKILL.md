---
name: accessibility-audit
description: Audits a web page, flow or component against WCAG 2.2 Level AA and returns findings ranked by severity, each with the success criterion, the element, the user impact, a fix and a code snippet. Combines automated scans (axe, Lighthouse) with the manual checks automation misses, including keyboard operation, focus visibility and Focus Not Obscured, screen-reader names, roles and states, headings and landmarks, forms and errors, contrast, target size, motion, 320 px reflow and the criteria added in 2.2. Use when someone asks for an "accessibility audit", "WCAG check", "a11y review", "is this accessible", "screen reader test", "WCAG 2.2 compliance", or before launching a public site or form.
---

# Audit accessibility against WCAG 2.2 AA

Produces an evidence-based findings list for one page, flow or component, ranked so the team fixes what blocks people first. The endpoint is a report (and, if asked, the fixes in code with a re-test). It is a practical audit, not a legal certification.

## When to use

- Before launch, after a redesign, or when a complaint or procurement checklist mentions accessibility.
- Reviewing a component library piece (modal, menu, form, carousel, tabs).
- Not for: contrast tuning of a whole palette (`design-tokens`), general usability (`ux-critique`), or a responsive layout pass (`responsive-qa`), though findings from those often overlap.

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| URL or local route, plus the user task to test ("submit an enquiry") | Requester | Ask for the key task; without one, audit the page's primary action path. |
| Access to the running page | Local `pnpm dev`/`next start`, preview or production URL | Code-only audits miss rendered states; say so in the report. |
| Source code | Repository | Findings still work from the rendered page; snippets are then generic. |
| Tools available | axe DevTools or `@axe-core/cli`, Lighthouse, a browser, a screen reader | Use what exists; list what was not available under "Not tested". |

## Procedure

1. **Scope.** Write down the pages, states (empty, error, success, logged in, open menu, open modal) and the task flow. Note browser, viewport and assistive technology used. Untested states are listed, never implied.
2. **Automated pass.** Run axe (browser extension, `@axe-core/cli <url>`, or `@axe-core/playwright` in an existing suite) and the Lighthouse accessibility category on each state. Record rule IDs and node counts. Treat these as leads: automated tools catch only a minority of WCAG failures and produce some false positives. Confirm each by inspection.
3. **Keyboard pass** (no mouse, no trackpad). Tab and Shift+Tab through the whole flow; use Enter, Space, arrows and Escape where the pattern expects them. Check:
   - every interactive element is reachable and operable, in an order that matches reading order (2.1.1, 2.4.3);
   - no keyboard trap, and modals return focus to their trigger on close (2.1.2);
   - focus is always visible (2.4.7) and never fully hidden by a sticky header, cookie banner or chat widget (2.4.11);
   - a skip link reaches `main` (2.4.1).
4. **Screen-reader pass.** Use one pairing at minimum (VoiceOver with Safari on macOS or iOS, or NVDA with Firefox or Chrome on Windows). Navigate by headings, landmarks and form controls. Every control announces a name, role and state (4.1.2): buttons that toggle say expanded or collapsed, the current page link has `aria-current="page"`, icon buttons have names. Dynamic messages (form errors, "added to cart", loading) are announced (4.1.3).
5. **Structure.** One `h1`, no skipped levels used for styling, headings describe their section (1.3.1, 2.4.6). Landmarks: `header`, `nav` (labelled if more than one), `main` (exactly one), `footer`. Lists are lists, tables have header cells. `<html lang>` is set (3.1.1).
6. **Forms.** Visible labels tied to inputs (1.3.1, 3.3.2); `autocomplete` on personal fields (1.3.5); errors identified in text and linked to the field, with a suggestion (3.3.1, 3.3.3); required state not conveyed by colour alone; no information the user already gave is asked for again in the same process unless essential (3.3.7); login does not require a cognitive test, and password fields allow paste and password managers (3.3.8).
7. **Visual.** Text contrast 4.5:1 (3:1 for large text) (1.4.3); UI boundaries, focus indicators and meaningful icons 3:1 (1.4.11); colour not the only signal (1.4.1); content reflows at 320 CSS px width without horizontal scrolling, except data tables, maps and similar (1.4.10); text spacing overrides do not clip content (1.4.12); 200% zoom keeps everything usable (1.4.4).
8. **Pointer and motion.** Targets at least 24 by 24 CSS px or with enough spacing (2.5.8); anything done by dragging also works with a single pointer (2.5.7); no content flashes more than three times a second (2.3.1); auto-moving content over five seconds can be paused (2.2.2); motion respects `prefers-reduced-motion` (best practice; 2.3.3 is AAA).
9. **Consistency and help.** If help (phone, chat, contact link) appears on several pages, it is in the same relative place (3.2.6). Navigation is consistent (3.2.3).
10. **Media.** Captions for prerecorded video with speech (1.2.2), audio description or a text alternative where visuals carry meaning (1.2.5), transcripts for audio. Decorative images `alt=""`; informative images described (1.1.1).
11. **Rate and write up.** Use the severity scale below and the full checklist in [references/wcag22-aa-checklist.md](references/wcag22-aa-checklist.md). Use [references/fix-patterns.md](references/fix-patterns.md) for tested code fixes; read it when writing the snippets.
12. **If asked to fix:** fix Critical and Serious first, re-run the automated pass and the specific manual check for each fix, and mark each finding fixed, partially fixed or open.

## Severity scale

| Severity | Meaning | Examples |
| --- | --- | --- |
| Critical | A user group cannot complete the task | Keyboard trap in a modal; submit button with no accessible name; CAPTCHA with no alternative; focus moved off-screen on error |
| Serious | The task is possible but very hard, or a common AA failure on a key path | Inputs without labels; body text at 3:1; focus outline removed; error shown only in red |
| Moderate | Friction or a failure off the main path | Heading levels skipped; 20 px targets in a footer; missing `autocomplete` |
| Minor | Best-practice gaps with low impact | Redundant `title` attributes; decorative SVG not hidden |

## Output

A report with: scope and method (pages, states, tools, browsers, assistive technology, date); a summary count by severity; then one row per finding:

| # | Severity | WCAG SC | Page / state | Element (selector or description) | Problem and who it affects | Fix | Snippet |
| --- | --- | --- | --- | --- | --- | --- | --- |

Then "Passed checks" (brief), "Not tested" (explicit), and a re-test plan. Group duplicate failures (the same component on 12 pages is one finding with 12 locations).

## Check before you finish

- [ ] Every finding names a success criterion, a specific element and a concrete fix; nothing says only "improve accessibility".
- [ ] Automated results were confirmed manually; false positives were removed and noted.
- [ ] Keyboard and at least one screen-reader pass were done, or listed under "Not tested" with the reason.
- [ ] The report states that it is not a conformance certification.
- [ ] Fixed, open and not-tested items are reported separately.

## Guardrails

- Do not claim a page "complies with WCAG" from an automated score. A Lighthouse 100 is not conformance.
- Do not add ARIA where a native element works; bad ARIA is worse than none.
- Do not use accessibility overlays as a fix.
- In Australia the Disability Discrimination Act 1992 applies to websites, and WCAG 2.2 AA is the practical benchmark. This is a practical checklist, not legal advice.

## With Fulcrum

Fulcrum Code can run the automated part and apply fixes in your repository. Ask it in Plan mode to list the components behind each finding before editing, then Build to fix, and review the diff and test output ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)). You can paste a cropped screenshot of a focus or contrast problem into the prompt for visual context. You can also save this audit as a reusable local skill, as in the form-review example in [Skills and agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/).

## Learn more

- [Fulcrum Code: skills and agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/)
- [Fulcrum Code: plan, build and review a change](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)
