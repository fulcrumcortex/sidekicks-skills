# Breakpoint matrix, overflow hunting and browser quirks

## Matrix

| Width (CSS px) | Represents | Look for |
| --- | --- | --- |
| 320 | Smallest phones; equals 1280 px at 400% zoom (WCAG 1.4.10 reflow) | Horizontal scroll, clipped buttons, headings breaking mid-word, nav overflowing |
| 360 | Common Android phones | Two-column grids that should be one; cramped form rows |
| 375 | Small iPhones (SE, mini) | Hero text wrapping to too many lines; sticky bars eating height (667 px tall) |
| 390 to 430 (test 414) | Current standard and large phones | Over-stretched single columns; images cropped badly |
| 667 to 932 × 375 to 430 | Phones in landscape | Header + banner leaving under 250 px of content; modals taller than viewport; safe-area notches on the sides |
| 768 | Tablet portrait; Tailwind `md` (48rem) | Layout switching awkwardly at exactly the breakpoint; test 767 and 768 |
| 1024 | Tablet landscape, small laptops; Tailwind `lg` (64rem) | Desktop nav squeezed; hover-only menus on touch screens |
| 1280 | Laptops; Tailwind `xl` (80rem) | Content width and line length (aim for 60 to 80 characters for body text) |
| 1440 | Common desktop | Max-width container behaviour, empty sides |
| 1920 and 2560 | Large and ultra-wide monitors | Backgrounds and images ending abruptly; text lines too long; hero images upscaled and blurry |

Tailwind v4 default breakpoints: `sm` 40rem (640 px), `md` 48rem (768 px), `lg` 64rem (1024 px), `xl` 80rem (1280 px), `2xl` 96rem (1536 px). Projects can redefine them with `--breakpoint-*` in `@theme`; read the project's theme first.

## Finding what overflows (paste in the browser console)

```js
(() => {
  const vw = document.documentElement.clientWidth
  const hits = [...document.querySelectorAll('body *')].filter((el) => {
    const r = el.getBoundingClientRect()
    return r.width && (r.right > vw + 1 || r.left < -1)
  })
  hits.forEach((el) => (el.style.outline = '2px solid red'))
  console.table(hits.slice(0, 30).map((el) => ({ el, right: Math.round(el.getBoundingClientRect().right), vw })))
})()
```

Read the list from the outermost element inward; the first culprit is usually the parent.

## Common causes and fixes

| Cause | Fix |
| --- | --- |
| `w-screen` / `100vw` on a full-bleed section (includes the vertical scrollbar width on desktop) | `w-full`, or a full-bleed grid technique without `vw` |
| Fixed `width` or `min-width` in px on cards, tables, images | `max-w-full`, `min-w-0` on flex and grid children, fluid widths |
| Flex or grid child with long content refusing to shrink | `min-w-0` on the child; `overflow-wrap: anywhere` for URLs and emails |
| Long words, URLs, email addresses | `break-words` (overflow-wrap: break-word) or `wrap-anywhere`; `hyphens-auto` with `lang` set |
| Decorative absolutely positioned shapes | Clip inside the section (`overflow-hidden` or `overflow-clip` on the section, not on body) |
| Negative margins on full-bleed rows | Match the container padding exactly, or restructure |
| Carousels and marquees | Contain inside `overflow-x-auto` or `overflow-hidden` wrapper with a fixed width |
| `grid-template-columns` with fixed tracks | `minmax(0, 1fr)` tracks; `repeat(auto-fit, minmax(min(16rem, 100%), 1fr))` |

## Safari and iOS checklist

- [ ] `100vh` includes the area behind the browser toolbar on iOS. Use `dvh` (changes as the toolbar moves), `svh` (smallest, stable) or `lvh`. Tailwind v4: `h-dvh`, `min-h-svh`.
- [ ] Inputs, selects and textareas with `font-size` below 16 px make iOS Safari zoom on focus. Use 16 px or larger on mobile.
- [ ] `position: fixed` bottom bars move or overlap when the on-screen keyboard opens. Hide them while an input is focused, or use the `visualViewport` API.
- [ ] `position: sticky` fails inside any ancestor with `overflow` other than `visible` (all engines; often noticed first on iOS).
- [ ] Notched devices with `viewport-fit=cover`: pad fixed elements with `env(safe-area-inset-top/right/bottom/left)`; check landscape, where the notch is on the side.
- [ ] Body scroll locking for modals: `overflow: hidden` on `body` alone was historically unreliable on iOS; the native `<dialog>` element with `showModal()` is the simplest robust option.
- [ ] Autofill: iOS and Chrome paint autofilled fields with their own background; check contrast of the text in both themes.
- [ ] Date and time inputs render native pickers that differ per platform; test the form flow, not just the look.
- [ ] `backdrop-filter` needed the `-webkit-` prefix in older Safari versions; check the project's browser targets and keep a solid fallback background for readability.
- [ ] Tap highlight: `-webkit-tap-highlight-color` may need setting so custom buttons do not flash grey.
- [ ] Smooth scrolling with a sticky header: set `scroll-padding-top` so anchors land below the header.
- [ ] `:hover` styles stick after tap on touch devices. Tailwind v4's `hover:` variant only applies where `(hover: hover)` matches; custom CSS should use `@media (hover: hover)` too.

## Cross-engine checklist (Chromium, Firefox, WebKit)

- [ ] Fonts render with similar metrics; check that headings do not wrap differently enough to break layout.
- [ ] Scrollbars: Firefox and Windows Chrome show classic scrollbars that take width; macOS overlays them by default. Test at least one engine with "always show scrollbars".
- [ ] Form controls: native `select`, checkboxes and range inputs differ; `accent-color` and `appearance: none` styling hold up.
- [ ] CSS features in use (container queries, `:has()`, subgrid, `text-wrap: balance`, view transitions, anchor positioning) are supported by the project's targets, or degrade gracefully.
- [ ] Print stylesheet, if the page is likely to be printed (quotes, invoices, itineraries).

## Preferences checklist

- [ ] Dark mode: logos and transparent PNGs readable; shadows replaced by lighter surfaces; borders visible; `color-scheme` set so native controls and scrollbars match.
- [ ] `prefers-reduced-motion: reduce`: parallax, auto-play and large transitions off; no content left invisible because its entrance animation never ran.
- [ ] Browser zoom 200% and a larger default font size: layout reflows, no clipped text in fixed-height elements.
- [ ] Forced colours (Windows High Contrast): focus outlines and borders still visible (use `outline`, not only `box-shadow`, for focus).

## Screenshot naming

`<route-slug>/<viewport>-<scheme>[-<state>].png`, for example `pricing/375-dark-menu-open.png`. Reference this path in the issue log. Store screenshots outside the repository or in an ignored folder unless the team wants them committed.
