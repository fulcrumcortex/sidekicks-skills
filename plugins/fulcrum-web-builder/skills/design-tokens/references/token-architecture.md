# Token architecture, inventory and migration

## The three tiers

| Tier | Example | Who uses it | Changes when |
| --- | --- | --- | --- |
| Primitive | `--gray-600: oklch(48% 0.008 80)` | Only the semantic layer | The brand palette changes |
| Semantic | `--ink-muted: var(--gray-600)` | Components, through Tailwind utilities (`text-ink-muted`) | Theme (light, dark, high contrast) changes |
| Component | `--button-height: 2.75rem` | One component | That component's design changes |

Rule of thumb: if you are about to type a primitive name in a component, you are missing a semantic token. If a component token always equals one semantic token, delete the component token.

## Naming

- Semantic names describe the role: `canvas`, `surface`, `ink`, `line`, `accent`, `on-accent`, `focus`, `danger`. Avoid colour words (`blue`, `light-grey`) at this tier.
- Pair every background with its foreground: `accent` / `on-accent`, `danger` / `on-danger` if a solid danger surface exists.
- States are suffixes: `accent-strong` (hover, pressed), `accent-subtle` (tinted background). Avoid `accent-2`.
- Type sizes by role (`display`, `h1`, `h2`, `h3`, `lead`) on marketing sites; app UIs often prefer a numeric scale (`text-sm`, `text-base`). Pick one convention.
- Radius and shadow by role: `radius-control`, `radius-card`; `shadow-raised`, `shadow-overlay`.

## Inventory commands

Run from the project root; adjust the source folder. These count candidates; read the results rather than trusting the numbers blindly.

```bash
# Distinct hex colours and how often each appears
grep -rhoE '#[0-9a-fA-F]{3,8}\b' src app components 2>/dev/null | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -40

# rgb(), hsl(), oklch() literals outside the theme file
grep -rnoE '(rgba?|hsla?|oklch)\([^)]*\)' src app components --include='*.tsx' --include='*.ts' --include='*.css' | grep -v theme.css | head -40

# Tailwind arbitrary values (colours, sizes, spacing)
grep -rhoE '\b[a-z-]+-\[[^]]+\]' src app components --include='*.tsx' | sort | uniq -c | sort -rn | head -40

# Default palette classes that will break if --color-*: initial is set
grep -rhoE '\b(bg|text|border|ring|fill|stroke|from|to|via|outline|decoration|shadow)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-[0-9]{2,3}\b' src app components | sort | uniq -c | sort -rn | head -40

# Inline style colours in JSX
grep -rnE 'style=\{\{[^}]*(color|background)' src app components --include='*.tsx' | head -20
```

## Building a ramp in OKLCH

- Lightness steps for a neutral ramp that works for both themes: 99, 97.5, 95, 90.5, 84, 71, 58, 48, 39, 29, 21, 15.5 (%). The jump between 84 and 71 is deliberate: it separates "surfaces" from "text-capable" greys.
- Neutral chroma 0.003 to 0.01, tinted toward the brand hue so greys feel related to the accent.
- Accent ramp: keep hue constant, lower chroma at the extremes. Maximum in-gamut chroma depends on hue and lightness; blues and cyans run out early at low lightness, yellows run out at mid lightness. The checker warns when a value leaves sRGB.
- A neutral grey reaches 4.5:1 on white at roughly OKLCH L 56% or lower, and on a 15% near-black canvas at roughly L 58% or higher. Those are minimums: body text reads better at L 45% or lower on light canvases and L 70% or higher on dark ones. Saturated hues shift the threshold, so always run the checker.
- Wide-gamut (P3) accents can be layered with `@supports (color: color(display-p3 1 1 1))`, but always check contrast on the sRGB fallback.

## Mapping hard-coded values to tokens

Build the map from the inventory, then replace by meaning:

| Found | Context | Becomes |
| --- | --- | --- |
| `#111`, `#1a1a1a`, `text-gray-900` | Body and heading text | `text-ink` |
| `#666`, `#6b7280`, `text-gray-500` | Captions, meta text | `text-ink-muted` (check contrast: `gray-400` and lighter fail on white) |
| `#e5e7eb`, `border-gray-200` | Card dividers | `border-line` |
| `border-gray-300` on inputs | Input outline | `border-line-strong` (needs 3:1) |
| `bg-blue-600 hover:bg-blue-700` | Primary button | `bg-accent hover:bg-accent-strong text-on-accent` |
| `rounded-lg` on buttons, `rounded-xl` on cards | Mixed | `rounded-control`, `rounded-card` |
| `text-[42px] leading-[1.1]` | Section heading | `text-h2` |
| `py-24 md:py-32` repeated on sections | Section rhythm | `py-section` |
| `transition duration-300` | Hover | `transition-colors duration-(--duration-fast) ease-standard` |

Work one tier and one category at a time, and build after each category so a break is easy to locate.

## Tailwind v3 to v4 notes that affect tokens

- v4 is configured in CSS: `@import "tailwindcss";` then `@theme { ... }`. There is no `tailwind.config.js` by default; a legacy one only loads through `@config`.
- Theme variables become real CSS custom properties, so components and inline styles can read `var(--color-accent)` directly.
- Namespaces drive utilities: `--color-*`, `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`, `--breakpoint-*`, `--container-*`, `--spacing-*`, `--radius-*`, `--shadow-*`, `--inset-shadow-*`, `--drop-shadow-*`, `--blur-*`, `--perspective-*`, `--aspect-*`, `--ease-*`, `--animate-*`.
- `--text-*` can carry `--line-height`, `--letter-spacing` and `--font-weight` companions (`--text-h2--line-height`).
- Use `@theme inline` when a theme variable references another variable, so the utility uses the reference rather than a value resolved at the wrong scope.
- `dark:` follows `prefers-color-scheme` by default. Redefine it with `@custom-variant dark (...)` for a class or `data-theme` toggle.
- Define `@keyframes` for `--animate-*` tokens inside `@theme`.
- Arbitrary variable shorthand is `utility-(--var)`, for example `duration-(--duration-base)`.

## Tests worth keeping

- The contrast CSV lives next to `theme.css` and runs in CI with the script's exit code.
- A visual snapshot of a "token sheet" page (all colours, type sizes, radii, shadows) in both themes catches accidental changes.
