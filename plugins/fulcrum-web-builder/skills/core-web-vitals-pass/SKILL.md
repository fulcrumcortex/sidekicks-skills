---
name: core-web-vitals-pass
description: Diagnoses and fixes Core Web Vitals (LCP, INP, CLS) on a site or page, measuring before and after. Separates field data (CrUX, PageSpeed Insights, Search Console, real-user monitoring) from lab data (Lighthouse, DevTools), finds the cause behind each failing metric, and applies targeted fixes such as LCP image priority and preload, font loading, server response, render-blocking CSS and JS, third-party scripts, long tasks, hydration cost, useTransition and code splitting, and reserved space for images, fonts and embeds. Includes a script that summarises Lighthouse or PageSpeed Insights JSON and compares two runs. Use when someone says "the site is slow", "fix Core Web Vitals", "LCP is too high", "poor INP", "layout shift", "PageSpeed score", "Search Console says poor URLs", or "improve Lighthouse".
---

# Pass Core Web Vitals

Moves a page's real-user p75 metrics into the "good" band: LCP at or below 2.5 s, INP at or below 200 ms, CLS at or below 0.1 (INP replaced FID as a Core Web Vital in March 2024). The endpoint is a before/after record with the causes found, the changes made and the measured effect. Field data confirms the result over the following 28 days; lab data shows direction immediately.

## When to use

- Search Console's Core Web Vitals report lists poor or "needs improvement" URLs.
- PageSpeed Insights shows failing field data, or a launch needs a performance check.
- Not for: a generic Lighthouse score chase with passing field data (say so and stop), server infrastructure sizing, or SEO markup (`seo-structured-data-audit`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| URLs or URL groups to fix | Search Console CWV report, analytics top landing pages | Start with the home page and the top three landing pages by traffic. |
| Field data | PageSpeed Insights (CrUX), Search Console, the project's RUM (for example `web-vitals` reporting) | Low-traffic pages have no CrUX data: use origin-level data, add RUM, and rely on lab data meanwhile. |
| A production build to test | `next build && next start`, preview or production URL | Never measure `next dev`; it is unoptimised. |
| Source code and third-party tag list | Repository, tag manager | Fixes become recommendations only. |

## Procedure

1. **Baseline field data.** For each URL record p75 LCP, INP and CLS from PageSpeed Insights (URL and origin), with the date. Note the device split; mobile usually fails first. If field data passes, report that and stop unless the owner wants lab improvements anyway.
2. **Baseline lab data.** Run Lighthouse mobile 3 to 5 times on the production build and keep the median (save JSON: `lighthouse URL --output=json --output-path=before.json`, or save the PageSpeed Insights API response). Summarise with `python3 scripts/cwv_report.py before.json`. It prints field and lab metrics, the LCP element and the failing audits or insights ranked by estimated savings.
3. **Work on the worst metric first**, using [references/fix-playbook.md](references/fix-playbook.md). Read the matching section before changing code.
   - **LCP:** identify the LCP element and split the time into TTFB, resource load delay, resource load duration and element render delay (DevTools Performance panel or the Lighthouse LCP breakdown). Fix the largest part. Typical: the hero image is lazy-loaded or discovered late (fix with `fetchPriority="high"` or `preload`, never `loading="lazy"`), it is a CSS background (move to `<img>`), it is oversized (correct `sizes`), render-blocking CSS or fonts delay paint, the hero animates in from `opacity: 0`, or TTFB is high (cache the HTML, use static or ISR rendering, a CDN close to Australian users).
   - **INP:** find the slow interaction (field attribution from `web-vitals/attribution`, or DevTools Performance with 4x CPU throttling while clicking the main controls). Split into input delay, processing and presentation delay. Typical: long tasks from hydration or third-party scripts during load, heavy event handlers, large re-renders, layout thrashing. Fix by yielding, `useTransition` for non-urgent updates, smaller client components, code splitting with `next/dynamic`, and moving or deferring third-party scripts.
   - **CLS:** find the shifting elements (Lighthouse layout-shift culprits, DevTools Layout Shift regions). Typical: images and iframes without dimensions, web fonts swapping with different metrics, banners or cookie bars injected above content, embeds and ads without reserved space, animations of `top`/`height` instead of `transform`.
4. **One change at a time where possible.** After each change, rebuild and rerun the lab median. Keep a change log: change, expected effect, measured effect.
5. **Check side effects.** Run the build, lint and tests. Confirm the page still looks and works the same (visual check at mobile and desktop), analytics and consent still fire, and accessibility did not regress (focus, reduced motion).
6. **Compare.** `python3 scripts/cwv_report.py before.json after.json` prints the deltas. Claim only what the medians show.
7. **Approval gate.** Deploying the changes, changing CDN or caching rules, or removing a third-party tag that marketing relies on needs explicit approval. Show the diff, the tags affected and the expected effect, and wait for a yes.
8. **Field follow-up.** CrUX is a rolling 28-day window. Re-check field data after 7 days for direction and after 28 days for the verdict; in Search Console use "Validate fix" on the issue group.

## Output

| Metric | Field p75 before | Lab median before | Cause found | Change made | Lab median after | Field status |
| --- | --- | --- | --- | --- | --- | --- |
| LCP | 3.9 s | 4.2 s | Hero image lazy-loaded, 1.8 MB | `fetchPriority="high"`, correct `sizes`, AVIF | 2.1 s | re-check on (date + 28 days) |

Plus: URLs covered, test conditions (device profile, throttling, number of runs, build), the change log, items not fixed with the reason, and the field re-check dates.

## Check before you finish

- [ ] Before and after were measured the same way (same URL, device profile, build type, number of runs).
- [ ] Field and lab numbers are labelled as such; no field improvement is claimed before the data window has passed.
- [ ] The build and existing tests pass; nothing visible or functional regressed.
- [ ] Third-party changes were agreed with the owner of each tag.
- [ ] Done, pending deploy, pending field confirmation and not fixed are reported separately.

## Guardrails

- Do not game lab scores (for example hiding content from Lighthouse's user agent or delaying all scripts until interaction in ways that break analytics or consent).
- Do not remove consent or privacy tooling to improve metrics; load it efficiently instead.
- Do not set `loading="lazy"` on above-the-fold images or `preload` on more than one or two critical resources.

## With Fulcrum

In Fulcrum Code, the Bash and Monitor tools can run the production build, start the server and run Lighthouse while you watch the output, and the LSP tools find every caller before you change a shared component ([Tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)). Ask for a checklist with measurable milestones (baseline, LCP fix, INP fix, CLS fix, comparison) so completion is backed by numbers. Stop before deploying and review the diff ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)).

## Learn more

- [Fulcrum Code: files, tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)
- [Fulcrum Code: plan, build and review a change](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)
