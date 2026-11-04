---
name: landing-page-build
description: Builds a production conversion landing page in Next.js (App Router), TypeScript and Tailwind CSS v4, from brief to a verified local build. Covers section architecture (one-promise hero, proof, problem and outcome, how it works, offer, FAQ, final call to action), server components by default, metadata and JSON-LD, next/font and sized images, accessibility and reduced motion, a validated and spam-protected lead form, and an analytics consent note. Use when someone asks to "build a landing page", "make a campaign page", "create a page for this offer", "turn this brief into a page", or "ship a lead-gen page for an ad". Works in any Next.js project; uses Fulcrum Code when it is the coding agent.
---

# Build a conversion landing page

Turns a brief into one landing page that makes one promise to one audience and asks for one action. The endpoint is a page that builds, lints, passes a keyboard and Lighthouse check locally, and is ready for an approved deploy. Deploying is a separate, approved step.

## When to use

- A new campaign, offer, product or service page in an existing or new Next.js App Router project.
- Rebuilding a slow or underperforming landing page section by section.
- Not for: a whole multi-page site with navigation (plan it first with `fulcrum-project-planning`), a bounded bug fix (`fulcrum-code-change`), the token system itself (`design-tokens`), copy-only work (`conversion-copy-review`), or release tracking (`fulcrum-release-check`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Audience and offer (who, what they get, what it costs them) | Brief, campaign plan, sales notes | Ask once. Do not build a page for "everyone". |
| Primary action (book, enquire, buy, download) and where submissions go | Brief, CRM or inbox owner | Ask. Without a destination the form is a dead end. |
| Real proof: numbers, quotes with permission, logos with permission, certifications | Client, case studies | Leave a visible `TODO: proof` slot. Never invent proof. |
| Brand tokens, fonts, logo | Existing `globals.css` / `@theme`, brand kit | Use the project's tokens; if none, run `design-tokens` first or ship a neutral system and say so. |
| Project conventions | `package.json`, lockfile, `app/` structure, lint config | Read before writing. Match the package manager the lockfile shows. |
| Analytics and consent posture | Client privacy policy, existing tags | Default to no non-essential tracking until confirmed. |

## Procedure

1. **Read the project.** Identify the Next.js version, the package manager (from the lockfile), the Tailwind entry CSS (`@import "tailwindcss"` and `@theme`), existing layout, fonts, and components. Reuse what exists; do not add a second button or heading system.
2. **Write the page contract before code** (five lines): audience, single promise, primary action, the proof you have, the objection most likely to stop the visitor. If any line is blank, stop and ask.
3. **Choose sections** from [references/section-patterns.md](references/section-patterns.md). Default order: hero, proof strip, problem and outcome, how it works (3 steps), offer and pricing or what happens next, objections and FAQ, final call to action. Drop any section you cannot fill with real content rather than padding it. Read that file when choosing layouts for each section.
4. **Set the rendering model.** `page.tsx` and every section are server components. Add `"use client"` only to leaf islands that need state or browser APIs (the form, a tabbed demo). FAQ uses native `<details>`/`<summary>`, which needs no client JavaScript. Start from [assets/page-skeleton.tsx](assets/page-skeleton.tsx).
5. **Metadata and structured data.** Export `metadata` (or `generateMetadata` when the page is data-driven) with a title of about 50 to 60 characters, a description of about 140 to 160 characters, `alternates.canonical`, and Open Graph (1200 × 630 image, or an `opengraph-image.tsx` file). Make sure `metadataBase` is set in the root layout. Render JSON-LD in a native `<script type="application/ld+json">`, escaping `<` as `<`. Mark up only what is visible on the page. FAQ rich results no longer appear in Google Search (retired in 2026), so FAQPage markup is optional and earns no snippet there.
6. **Fonts.** Load at most two families with `next/font` (variable fonts preferred, `subsets: ['latin']`), expose them as CSS variables and map them in `@theme inline`. Keep the default `display: 'swap'` and fallback metric adjustment; they prevent invisible text and reduce layout shift.
7. **Images.** Every `next/image` gets `width`/`height`, or `fill` inside a parent with a fixed aspect ratio, plus `sizes` that matches the layout. The single largest above-the-fold image gets `fetchPriority="high"` (or `preload` in Next.js 16; `priority` is deprecated there) and is never lazy-loaded. Decorative images get `alt=""`; informative images describe the content, not the file.
8. **Accessibility floor.** One `<h1>`, sequential headings, `header`/`main`/`footer` landmarks, a skip link, visible `:focus-visible` styles that are not hidden by sticky headers, text contrast of at least 4.5:1 (3:1 for large text and UI boundaries), targets at least 24 × 24 CSS px (aim for 44 on touch CTAs), and reflow without horizontal scroll at 320 px.
9. **Motion.** Use motion only to explain order or state. Wrap it in `motion-safe:` or a `prefers-reduced-motion` check. Never start the hero heading or LCP image at `opacity: 0`; an invisible element cannot be the LCP and the metric waits for the animation.
10. **Form.** Build from [assets/lead-form.tsx](assets/lead-form.tsx) and [assets/lead-form-action.ts](assets/lead-form-action.ts), and read [references/forms-and-consent.md](references/forms-and-consent.md) for validation, spam controls and the collection notice. Ask for no more than the follow-up needs (name, email, one qualifying question is a strong default). Validate on the server even when the browser validates too.
11. **Analytics.** Load nothing non-essential until the consent rules in the forms reference are settled. Never send form field values, email addresses or phone numbers in analytics events or URLs.
12. **Verify locally** (see the checklist below). Fix, then rerun the failing check.
13. **Approval gate.** Before any deploy, publish, `git push`, preview link shared outside the team or DNS change, show: the branch and commit, the target (preview or production, which host and project), the domain, the environment variables the form needs (names only), and the check results. Wait for an explicit yes. After an uncertain deploy result, check the host's deployment list before running it again.

## Output

1. The page contract (five lines) and the section list with any dropped sections and why.
2. The code changes (files created or edited).
3. A verification report:

| Check | Command or method | Result |
| --- | --- | --- |
| Build | `pnpm build` (or the project's package manager) | pass / fail + first error |
| Lint and types | `pnpm lint`, `pnpm exec tsc --noEmit` | pass / fail |
| Lighthouse, mobile | Chrome DevTools Lighthouse panel, or the CLI `lighthouse <url> --output=html --output=json` (mobile is the default), on the production build | Performance, Accessibility, SEO, LCP, CLS, TBT |
| Keyboard pass | Tab through the whole page | order logical, focus always visible, form operable |
| 320 px reflow | Responsive mode at 320 px | no horizontal scroll |
| Form | Fictional submission plus empty, invalid and duplicate cases | lands in the destination, errors announced |

4. Open items: missing proof, unconfirmed claims, consent decisions, anything not verified.

## Check before you finish

- [ ] `pnpm build` passed on the final code. Next.js 16 no longer lints during `next build` and has removed `next lint`, so the lint script ran separately.
- [ ] Lighthouse ran against a production build (`next start` or a preview), not `next dev`.
- [ ] Exactly one `<h1>`, one primary call to action per viewport, and the same action label everywhere it appears.
- [ ] A test submission reached its destination; a success message alone is not proof.
- [ ] No placeholder text, fake testimonials, stock "trusted by" logos or invented numbers remain.
- [ ] Done, drafted, pending (for example "awaiting deploy approval") and failed items are reported separately.

## Guardrails

- Never invent proof, ratings, client logos, awards or statistics. Comparative or superlative claims ("fastest", "#1") need evidence the client can produce.
- Consumer-facing prices show the total price including GST and any compulsory fees.
- Keep secrets in environment variables; never commit API keys or form endpoints with embedded tokens.
- Privacy checklist for the form and analytics:
  - [ ] Collect only the fields the follow-up needs.
  - [ ] A collection notice near the submit button says who collects the data, why, and links the privacy policy.
  - [ ] Marketing email or SMS consent is a separate, unticked checkbox, not bundled with the enquiry.
  - [ ] Non-essential analytics and advertising tags respect the consent decision and receive no personal information.
  - [ ] If the site targets EU or UK visitors, prior consent for non-essential cookies is obtained.
  - This is a practical checklist, not legal advice.

## With Fulcrum

Fulcrum Code can carry this procedure in your repository. Use Plan mode to read the project and agree the page contract before any file changes, then Build mode for the implementation, and review the diff and test output before committing ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)). Ask it to use an isolated Git worktree so the page lives on its own branch ([Tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)). To send enquiries straight into Fulcrum CRM instead of building your own form back end, embed a Fulcrum CRM lead form, list your domain under Allowed Domains, and test a fictional submission end to end ([Lead forms and routing](https://fulcrumcortex.github.io/documentation/crm/lead-forms-and-routing/)).

## Learn more

- [Building landing pages via Cortex](https://fulcrumcortex.com/blog/building-landing-pages-via-cortex)
- [Fulcrum Code: plan, build and review a change](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)
- [Fulcrum CRM lead forms and routing](https://fulcrumcortex.github.io/documentation/crm/lead-forms-and-routing/)
