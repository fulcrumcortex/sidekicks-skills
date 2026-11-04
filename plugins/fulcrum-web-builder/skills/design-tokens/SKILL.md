---
name: design-tokens
description: Creates or refactors a design-token system in Tailwind CSS v4 using CSS-first `@theme`, with primitive, semantic and component tiers. Covers OKLCH colour with contrast-checked foreground and background pairs, a fluid clamp() type scale, spacing, radius, shadow and elevation, motion duration and easing, dark mode through semantic tokens, and migrating hard-coded values out of components. Includes a WCAG contrast checker script and a starter theme.css. Use when someone asks to "set up design tokens", "build a theme", "add dark mode", "clean up our colours", "migrate to Tailwind v4 theme", "our styles are inconsistent", or "make the brand palette accessible". Works in any Tailwind v4 project.
---

# Build a design-token system in Tailwind v4

Produces one `theme.css` that every component draws from: primitives hold raw values, semantic tokens say what a value is for, and component tokens exist only where a component needs its own knob. The endpoint is a compiled build with no hard-coded colours left in components and every text and UI pair passing WCAG AA in both light and dark.

## When to use

- Starting a site or design system and choosing tokens before components.
- A codebase with scattered hex values, arbitrary values (`text-[#3b3b3b]`, `p-[18px]`) or two competing button styles.
- Adding dark mode, rebranding, or upgrading a Tailwind v3 `tailwind.config.js` theme to v4 `@theme`.
- Not for: page layout and sections (`landing-page-build`), auditing a finished page for contrast and other WCAG issues (`accessibility-audit`), or aesthetic direction (`anti-slop-design-review`).

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Brand colours, fonts, logo | Brand guide, existing CSS, Figma variables | Extract from the live site's CSS. If there is no brand, use the neutral starter and mark it as a placeholder. |
| Current styling | `globals.css`, `tailwind.config.*`, component files | Run the inventory in step 1 before designing anything. |
| Tailwind version | `package.json` | v3 projects: plan the upgrade (`npx @tailwindcss/upgrade` or the project's package-manager equivalent) as its own step. |
| Dark mode requirement and toggle style | Product owner | Default to following the OS preference with an optional `data-theme` override. |

## Procedure

1. **Inventory before designing.** Count what exists: distinct colours, font sizes, radii, shadows, durations and arbitrary values. Use the search commands in [references/token-architecture.md](references/token-architecture.md). Expect duplicates (seven greys that should be four). Record the top values by frequency; they are your migration map.
2. **Define primitives in OKLCH.** One neutral ramp (10 to 12 steps) and one accent ramp, plus status hues (danger, success, warning). Steps are spaced by perceived lightness (`L`), with chroma reduced toward the light and dark ends. Keep every value inside sRGB; the checker warns when a value is clipped. Convert brand hex values to OKLCH and keep the brand value as one step rather than rebuilding it.
3. **Define semantic tokens by role**, not by colour name: `canvas`, `surface`, `surface-raised`, `ink`, `ink-muted`, `line`, `line-strong`, `accent`, `accent-strong`, `on-accent`, `focus`, `danger`, `success`, `warning`. Rules:
   - one accent colour carries the primary action; do not add a second unless it has a distinct job;
   - `line` is decorative and exempt from contrast; anything that identifies a control (`line-strong`, `focus`) needs 3:1;
   - every background token has a named foreground partner.
4. **Expose semantic tokens to Tailwind** with `@theme inline { --color-canvas: var(--canvas); ... }`. `inline` makes utilities reference the variable, so values switch when the theme switches. Clear the default palette with `--color-*: initial` when you want off-system colours to fail at build time; re-add `white` and `black` if used.
5. **Dark mode through semantic tokens only.** Redefine the semantic layer under `@media (prefers-color-scheme: dark)` and `[data-theme="dark"]`. Components never need `dark:` for colour. If `dark:` is needed for something else, define it with `@custom-variant` to match the same rule (see [assets/theme.css](assets/theme.css)). Dark mode is not inverted light mode: lift surfaces with lighter greys instead of shadows, lower accent chroma, and avoid pure black canvases behind long text.
6. **Type scale.** At most five sizes above body. Use `clamp(min, rem + vw, max)` with a rem component in the middle term, and keep max at or below 2.5 times min so browser zoom still enlarges text. Pair each size with `--text-*--line-height` and `--text-*--letter-spacing` (tighter tracking as sizes grow). Map `next/font` variables into `--font-sans` and `--font-display`.
7. **Spacing, radius, elevation, motion.**
   - Keep `--spacing: 0.25rem` and add layout steps (`--spacing-section`, `--spacing-gutter`), not a parallel scale.
   - Name radii by role (`--radius-control`, `--radius-card`, `--radius-pill`). Nested radius = outer radius minus padding.
   - Two or three shadows at most, tinted toward the canvas hue, layered (a tight contact shadow plus a soft ambient one).
   - Durations as plain variables (`--duration-fast` 120 to 160 ms for hovers, `--duration-base` 200 to 250 ms for small transitions, `--duration-slow` 300 to 400 ms for panels), used as `duration-(--duration-base)`; easings in `--ease-*`. Zero the durations under `prefers-reduced-motion: reduce`.
8. **Component tokens sparingly**: control height (44 px for touch-first sites), header height (feeds `scroll-padding-top`), field padding. If a component token equals a semantic token everywhere, delete it.
9. **Check contrast.** List every real pairing in a CSV (start from [assets/contrast-pairs.csv](assets/contrast-pairs.csv)) and run:
   `python3 scripts/contrast_check.py --pairs pairs.csv --css theme.css --suggest`, then again with `--scope dark`. Fix failures by moving lightness, not by adding a new colour. Thresholds: 4.5:1 text, 3:1 large text (24 px, or 18.66 px bold) and UI boundaries.
10. **Migrate hard-coded values** in this order: colours, then type, then radius and shadow, then spacing. Replace by role, not by nearest value: `text-[#6b6b6b]` in a caption becomes `text-ink-muted`. Leave a one-line note where a value had no matching role, and decide whether it earns a token or should be removed.
11. **Build and look.** Run the project's build. Inspect three representative pages in light and dark, at 320 px and desktop, and with forced colours (Windows High Contrast or the DevTools emulation) to confirm focus and borders remain visible.

## Output

- `theme.css` (or the project's global CSS) with the four labelled sections: primitives, semantic (light and dark), `@theme` mapping, component tokens. Start from [assets/theme.css](assets/theme.css).
- A token table: token, light value, dark value, role, allowed pairings.
- The contrast report from the script for both scopes, with zero AA failures or a named exception the owner accepted.
- A migration log: file, old value, new token, or "removed".

## Check before you finish

- [ ] The build compiles and a search for hex, `rgb(` and arbitrary colour classes in components returns only documented exceptions.
- [ ] Both scopes pass the contrast script; the out-of-gamut warning count is zero.
- [ ] No component uses a primitive token directly.
- [ ] Dark mode works with the OS preference and with an explicit `data-theme`, and there is no flash of the wrong theme on load (set `data-theme` before paint if you offer a toggle).
- [ ] Reduced-motion durations resolve to zero.
- [ ] Report what was migrated, what remains and any exceptions separately.

## Guardrails

- Do not change brand colours silently. If a brand value fails contrast as text, keep it for large display or decorative use and add a darker text step; tell the owner.
- Do not ship Tailwind v3 `tailwind.config.js` patterns into a v4 project unless the project already loads one with `@config`.
- Colour is never the only signal: errors also get text, links in body copy are underlined or otherwise marked.

## With Fulcrum

In Fulcrum Code, run the inventory in Plan mode so nothing changes while you agree the token map, then switch to Build for the migration, and review the diff before committing ([Plan, build and review](https://fulcrumcortex.github.io/documentation/code/plan-build-and-review/)). A token migration touches many files, so ask for an isolated worktree and a checklist of milestones (inventory, primitives, semantic layer, migration, contrast run) ([Tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)).

## Learn more

- [Fulcrum Code: files, tools and worktrees](https://fulcrumcortex.github.io/documentation/code/tools-and-worktrees/)
- [Fulcrum Code](https://fulcrumcode.app/)
