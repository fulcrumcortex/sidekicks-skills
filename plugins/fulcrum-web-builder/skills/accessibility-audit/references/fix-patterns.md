# Fix patterns with code

Snippets use React/TSX and Tailwind v4 classes but the HTML is what matters. Prefer the native element; reach for ARIA only when no native element fits.

## Icon-only button has no name (4.1.2, 1.1.1)

```tsx
// Before
<button onClick={openMenu}><MenuIcon /></button>

// After
<button type="button" onClick={openMenu} aria-expanded={open} aria-controls="site-menu">
  <MenuIcon aria-hidden="true" focusable="false" />
  <span className="sr-only">Menu</span>
</button>
```

## Clickable div (2.1.1, 4.1.2)

```tsx
// Before
<div className="card" onClick={() => router.push(href)}>...</div>

// After: the heading link is the target; the whole card is clickable through a pseudo-element
<article className="relative">
  <h3><a href={href} className="after:absolute after:inset-0">Kitchen renovations</a></h3>
  <p>...</p>
</article>
```

## Focus removed or invisible (2.4.7, 1.4.11)

```css
/* Before */
button:focus { outline: none; }

/* After: visible on keyboard focus, 3:1 against adjacent colours */
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
```

## Focus hidden under a sticky header or bottom bar (2.4.11)

```css
html { scroll-padding-top: calc(var(--header-height) + 1rem); scroll-padding-bottom: 5rem; }
/* For in-page anchors as well */
[id] { scroll-margin-top: calc(var(--header-height) + 1rem); }
```

Also: cookie banners and chat launchers must not cover the focused element; dock the banner without overlaying content, or move focus into it when it appears.

## Skip link (2.4.1)

```tsx
<a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-canvas focus:px-4 focus:py-2">
  Skip to content
</a>
...
<main id="main" tabIndex={-1}>...</main>
```

## Form error not identified or announced (3.3.1, 3.3.3, 4.1.3)

```tsx
<label htmlFor="email">Email</label>
<input id="email" name="email" type="email" autoComplete="email"
  aria-invalid={!!error} aria-describedby={error ? 'email-error' : 'email-hint'} />
<p id="email-hint" className="text-sm text-ink-muted">We reply to this address.</p>
{error && <p id="email-error" className="text-sm text-danger">Enter an email like name@example.com.</p>}

{/* After a failed submit: summary that receives focus */}
<div role="alert" tabIndex={-1} ref={summaryRef}>
  <p>2 fields need attention:</p>
  <ul><li><a href="#email">Email</a></li><li><a href="#phone">Mobile</a></li></ul>
</div>
```

## Radio group without a group label (1.3.1)

```tsx
<fieldset>
  <legend>Preferred contact time</legend>
  <label><input type="radio" name="time" value="am" /> Morning</label>
  <label><input type="radio" name="time" value="pm" /> Afternoon</label>
</fieldset>
```

## Accordion or disclosure (4.1.2)

Native first:

```tsx
<details><summary>Do you service the Blue Mountains?</summary><p>Yes, ...</p></details>
```

Custom when design requires it:

```tsx
<h3>
  <button type="button" aria-expanded={open} aria-controls="faq-1" onClick={() => setOpen(!open)}>
    Do you service the Blue Mountains?
  </button>
</h3>
<div id="faq-1" hidden={!open}>...</div>
```

## Modal dialog (2.1.2, 2.4.3)

Use the native `<dialog>` with `showModal()`: it provides focus containment, Escape to close and an inert background.

```tsx
const ref = useRef<HTMLDialogElement>(null)
<button type="button" onClick={() => ref.current?.showModal()}>Request a quote</button>
<dialog ref={ref} aria-labelledby="quote-title" onClose={() => triggerRef.current?.focus()}>
  <h2 id="quote-title">Request a quote</h2>
  ...
  <button type="button" onClick={() => ref.current?.close()}>Close</button>
</dialog>
```

## Small targets (2.5.8)

```tsx
// Before: 16px icon link
<a href="/facebook-page"><FacebookIcon className="size-4" /></a>

// After: 24px minimum hit area (44px on touch-first layouts) without changing the icon size
<a href="/facebook-page" className="inline-grid size-11 place-items-center">
  <FacebookIcon className="size-4" aria-hidden="true" />
  <span className="sr-only">Our Facebook page</span>
</a>
```

## Dragging with no alternative (2.5.7)

A before/after slider or a range input built from a draggable handle also needs click-to-position or step buttons:

```tsx
<input type="range" min={0} max={100} value={pos} onChange={(e) => setPos(+e.target.value)} aria-label="Before and after comparison" />
```

A native range input is operable with arrow keys and by clicking the track, which satisfies the single-pointer requirement.

## Auto-advancing carousel (2.2.2)

Provide a visible Pause button before the slides, stop on hover and focus, and do not auto-advance when `prefers-reduced-motion: reduce` is set. Better: do not auto-advance at all.

## Status message (4.1.3)

```tsx
<p role="status" aria-live="polite" className="sr-only">{resultCount} results</p>
```

Render the live region on page load (empty), then change its text; regions inserted at the same time as their text are often not announced.

## Reduced motion (2.3.3 is AAA; still expected practice)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
}
```

Use Tailwind `motion-safe:` for entrance animations so they only run when allowed.

## Accessible authentication (3.3.8)

- Never block paste: remove `onPaste={e => e.preventDefault()}` from password and one-time-code fields.
- `autoComplete="current-password"`, `"new-password"`, `"one-time-code"` let password managers and SMS autofill work.
- Offer an email magic link or passkey as an alternative to puzzle CAPTCHAs.
