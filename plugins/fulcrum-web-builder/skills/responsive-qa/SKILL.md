---
name: responsive-qa
description: Runs a responsive and cross-browser QA pass on a website or web app and returns an issue list with the viewport, a screenshot reference and the fix. Uses a breakpoint matrix (320, 375, 414, 768, 1024, 1280, 1440 and wider), checks touch targets, hunts horizontal overflow, safe-area insets on notched phones, dynamic viewport units (dvh, svh), image art direction, tables on mobile, landscape phones, Safari and iOS quirks, reduced motion and dark mode. Includes a Playwright spec template that captures screenshots and flags overflow and small targets. Use when someone asks to "check it on mobile", "responsive test", "cross-browser check", "it breaks on iPhone", "QA before launch", "horizontal scroll on mobile", or "test on Safari".
---

# Run a responsive and cross-browser QA pass

Checks that a site works and looks intentional at every common width, in the main browser engines, with touch, dark mode and reduced motion. The endpoint is an issue log where every row has a viewport, a screenshot reference and a concrete fix, and, if asked, the fixes applied and re-checked.

## When to use

- Before launch, after a layout change, or when users report "it is broken on my phone".
- Checking a component library across container sizes.
- Not for: WCAG conformance (`accessibility-audit`; reflow and target size overlap and are cross-referenced), speed (`core-web-vitals-pass`), or visual taste (`anti-slop-design-review`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| URLs or routes, including key states (menu open, form error, modal, logged in) | Requester, sitemap | Test home, the main conversion page and one long content page. |
| A production build or preview | `next build && next start`, preview URL | Do not QA `next dev` for final sign-off; dev overlays and unminified CSS differ. |
| Browsers and devices available | Local Chrome, Firefox, Safari; Playwright engines; real phones | Playwright WebKit approximates Safari but is not iOS Safari; mark iOS items "emulated" unless a real device was used. |
| Analytics device and browser mix | Analytics | Default priority: mobile Safari and Chrome on Android first, desktop Chrome second. |

## Procedure

1. **Plan the matrix.** Use the breakpoint matrix in [references/breakpoint-matrix.md](references/breakpoint-matrix.md) (read it for the device list and what to look for at each width). Add the project's own breakpoints and test 1 px either side of each (for example 767 and 768).
2. **Automated sweep.** If Playwright is available, copy [assets/responsive-qa.spec.ts](assets/responsive-qa.spec.ts), set the routes and run it against the production build in Chromium, Firefox and WebKit projects. It saves full-page screenshots per viewport and colour scheme, and soft-fails on horizontal overflow and targets under 24 × 24 px with the offending selectors. Without Playwright, use browser responsive mode and capture screenshots manually with the same file naming.
3. **Overflow hunt.** For any horizontal scroll, find the widest element (the spec lists them; manually, paste the snippet from the reference into the console). Common causes: fixed widths, `100vw` (includes the scrollbar), long URLs or words, wide tables, negative margins, absolutely positioned decorations, carousels. Fix the cause; do not hide it with `overflow-x: hidden` on `body`, which can also break `position: sticky`.
4. **Touch and input.** Targets at least 24 × 24 CSS px (aim for 44 × 44 for primary actions) with spacing; hover-only interactions have a tap equivalent; input `font-size` at least 16 px so iOS Safari does not zoom on focus; correct `type` and `inputmode` bring up the right keyboard; the on-screen keyboard does not cover the focused field or a sticky submit button.
5. **Viewport units and safe areas.** Full-height sections use `min-h-dvh` (or `svh` to avoid jumps as the toolbar shows and hides) instead of `100vh`. If the site uses `viewport-fit=cover` (in Next.js, `export const viewport = { viewportFit: 'cover' }`), fixed headers, bottom bars and side gutters respect `env(safe-area-inset-*)`; check in landscape on a notched phone.
6. **Images and media.** Correct `sizes` so phones do not download desktop images; art direction for crops that lose the subject on mobile (`<picture>` or Next.js `getImageProps`); video has a poster and does not autoplay with sound; embeds are responsive (`aspect-ratio`).
7. **Tables and dense content.** Wide tables sit in a scroll container that is keyboard-focusable and labelled (`role="region"`, `aria-label`, `tabIndex={0}`), or are restructured as stacked cards below `md`. Code blocks and long strings wrap or scroll inside their box.
8. **Landscape phones** (about 667 × 375 to 932 × 430): sticky header plus cookie banner can leave too little room; modals and menus need `max-height: 100dvh` and internal scroll.
9. **Browser quirks.** Work through the Safari and cross-browser list in the reference: sticky inside overflow ancestors, `position: fixed` with the keyboard open, date and select styling, `backdrop-filter`, `gap` and `aspect-ratio` fallbacks for older targets, smooth scrolling, form autofill colours.
10. **Preferences.** Dark mode (images with transparent backgrounds, logos, borders, form controls via `color-scheme`), reduced motion (no essential content hidden behind animation), 200% zoom and larger default text size.
11. **Log every issue** with the template below, attach the screenshot path, and group the same defect across viewports into one row with all viewports listed.
12. **If asked to fix:** fix by component, rerun the sweep for the affected routes in all three engines, and attach before and after screenshots.

## Output

| # | Severity | Page / state | Viewport(s) and browser | Screenshot | Issue | Cause | Fix |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | High | `/pricing` | 320-414, all engines | `test-results/responsive/pricing/375-light.png` | Page scrolls sideways | Comparison table `min-width: 720px` outside a scroll container | Wrap in `overflow-x-auto` region with `tabIndex={0}` and an `aria-label`; stack below `md` |

Severity: **High** blocks a task or hides content, **Medium** clearly broken layout or hard-to-use control, **Low** cosmetic. Finish with the matrix actually tested (engines, real devices vs emulation) and anything not tested.

## Check before you finish

- [ ] Every width in the matrix was checked in at least Chromium and WebKit, and every issue has a screenshot.
- [ ] Emulated iOS results are labelled as emulated; real-device checks are named.
- [ ] No fix used `overflow-x: hidden` on `html` or `body` to mask an overflow.
- [ ] Fixed, open and not tested items are reported separately.

## Guardrails

- Screenshots can capture personal data in logged-in states. Use fictional test accounts and crop or blur anything real before sharing.
- Do not change breakpoints globally to fix one component; prefer container queries (`@container`, built into Tailwind v4) or component-level fixes.

## With Fulcrum

Fulcrum Code can run the Playwright sweep with its shell tools and follow the output, then fix components in an isolated worktree ([Tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)). Paste a cropped screenshot of a layout problem into the prompt to give it visual context, with account names, tabs and unrelated windows cropped out ([Voice, images and editor](https://fulcrumcortex.github.io/documentation/code/voice-images-and-editor/)).

## Learn more

- [Fulcrum Code: voice, images and editor](https://fulcrumcortex.github.io/documentation/code/voice-images-and-editor/)
- [Fulcrum Code: files, tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)
