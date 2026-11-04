---
name: anti-slop-design-review
description: Reviews a website or interface for the generic "AI template" look and redirects it toward an intentional, agency-grade design. Detects default purple-blue gradients, glassmorphism everywhere, emoji used as icons, centred-everything layouts, identical three-card grids, generic stock illustrations, placeholder or hype copy ("Unlock", "Elevate", "Seamless"), one radius and shadow on every element, a timid type scale and meaningless motion, then proposes one strong typographic idea, a constrained palette with one accent, real content and proof, asymmetric layout, purposeful motion and craft details. Outputs a findings list and a three-move redirection plan. Includes a source scanner and a catalogue of slop patterns with fixes. Use when someone says "this looks AI-generated", "make it look less generic", "it looks like a template", "design review", "make it feel premium", or "kill the AI slop".
---

# Kill the AI-slop look

Names exactly what makes a site look generated or templated, and gives a short, opinionated plan to make it look designed for this business. The endpoint is a findings list with evidence and a three-move redirection plan the team can execute, plus, if asked, the first move implemented. It does not impose any brand: the direction comes from the client's own business, content and brand assets.

## When to use

- A site or prototype "looks like every other AI startup", feels cheap, or the client cannot say why it does not feel premium.
- After a fast AI-assisted build, before showing it to a client.
- Not for: usability problems (`ux-critique`), WCAG conformance (`accessibility-audit`), copy rewriting in depth (`conversion-copy-review`), or token plumbing (`design-tokens`, which implements the palette and type decisions made here).
- Hand-offs: implement the agreed fixes as a reviewable change with `fulcrum-code-change`, and verify an authorised release with `fulcrum-release-check`.

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| The site: URL, build or screenshots of key pages at desktop and mobile | Requester | Ask for at least the home page and one inner page at both sizes. |
| Source code (optional) | Repository | Without it, skip the scanner and work from screenshots. |
| Brand assets: logo, colours, typefaces, photography, guidelines | Client | Work from the logo and the business itself; say that the direction is a proposal. |
| What the business actually is: customers, proof, product screenshots, team, place | Client, existing materials | Real content is the strongest anti-slop tool. List what to collect. |
| Two or three reference sites the client admires (and why) | Client | Propose references by direction, not by industry. |

## Procedure

1. **Look first, at full size.** Review each page as a visitor at 1440 px and 390 px. Note your first impression in one sentence; if the sentence could describe a thousand other sites, that is the core finding.
2. **Scan the source** if available: `python3 scripts/slop_scan.py src` (or the project's source folders). It counts template signals (purple gradients, gradient text, glass, emoji, centred text, three-column grids, radius and shadow uniformity, type scale, decorative motion, placeholder and hype copy) and lists the files. Treat counts as evidence to inspect, not as verdicts.
3. **Identify findings** using the catalogue in [references/slop-catalogue.md](references/slop-catalogue.md); read it during this step. For each, record what it is, where (page, section, screenshot or file), why it reads as template, and the fix. Rate each **Strong** (defines the impression), **Medium** (adds to it) or **Low** (polish).
4. **Find the real material.** List what is specific to this business and unused: product UI, real photos of people and places, numbers, customer quotes, process artefacts, the founder's voice, the location. Generic design fills the space where this material should be.
5. **Choose a direction** in one sentence that a designer could execute and a client could reject: for example "Technical and exact: a strict 12-column grid, a grotesk with monospaced data accents, near-monochrome with one signal colour for actions." Derive it from the business (what it does, who buys, the price point), not from trends. Offer two directions only if the brief is genuinely open.
6. **Write the three-move plan.** Pick the three changes with the most leverage, usually from: one strong typographic idea; a constrained palette with one accent; real content and proof replacing decoration; an asymmetric, content-driven layout; purposeful motion; craft details. Each move states the change, where it applies first, what is removed, and how to tell it worked. Fewer, bigger moves beat many small fixes.
7. **Sketch the first move concretely** for the hero or the most visible section: type sizes and weights, palette tokens, layout columns, what content goes where. If implementing, hand palette and type decisions to `design-tokens` so they live in the theme, not in one-off classes.
8. **Check that the redirection does not cost accessibility or speed:** contrast still passes, motion respects reduced-motion, new fonts are subset and limited to two families, large imagery is optimised.

## Output

1. **Impression:** one sentence now; one sentence for the target.
2. **Findings:**

| # | Rating | Pattern | Where (page, section, file) | Why it reads as template | Fix |
| --- | --- | --- | --- | --- | --- |
| 1 | Strong | Purple-to-blue gradient hero with gradient-text H1 | Home hero, `components/Hero.tsx` | The default palette of generated SaaS sites; says nothing about this business | Solid canvas, H1 in the display face at 80 px with tight tracking; accent reserved for the CTA |

3. **Direction statement** and two or three reference sites with what to borrow from each (a quality, not a look).
4. **Three-move plan:**

| Move | Change | Apply first to | Remove | Done when |
| --- | --- | --- | --- | --- |
| 1. Typographic idea | ... | Hero and section headings | Gradient text, five competing sizes | Headings alone carry the hierarchy in greyscale |
| 2. Constrained palette | ... | Global theme | Purple gradient, decorative blur | One accent used only for actions and key data |
| 3. Real proof | ... | Hero visual and feature rows | Stock illustrations, emoji icons | Every visual shows the product, the people or the result |

5. **Content to collect** from the client to make the moves possible.
6. **Craft details** worth doing after the three moves (short list from the catalogue).

## Check before you finish

- [ ] Every finding points at a specific place and has a fix; nothing says only "make it more premium".
- [ ] The direction comes from the business and its brand assets, not from a default palette or the reviewer's taste alone.
- [ ] The plan has exactly three moves, each with a "done when" test.
- [ ] Accessibility and performance implications of the moves are noted.

## Guardrails

- Do not replace one default with another (swapping purple gradients for a trendy font and dark mode is still templated). Each choice needs a reason tied to the business.
- Do not use competitor brand assets or copy a reference site's layout wholesale; borrow qualities (restraint, density, rhythm), not identity.
- Never invent proof to fill the "real content" move; list what to collect instead.
- Keep fixes within the client's brand guidelines; flag conflicts rather than overriding them.

## With Fulcrum

Fulcrum Code can run the scanner in your repository and implement the moves one at a time. Use Plan mode to agree the direction and the three moves before any edits, then Build for move one, and review the result in the browser and the diff before continuing ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)). Save the direction and moves as a local skill so later pages follow the same rules ([Skills and agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/)).

## Learn more

- [Fulcrum Code: skills and agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/)
- [Fulcrum Code](https://fulcrumcode.app/)
