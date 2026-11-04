# Core Web Vitals fix playbook

Thresholds at the 75th percentile of page loads, split by mobile and desktop:

| Metric | Good | Needs improvement | Poor |
| --- | --- | --- | --- |
| LCP (Largest Contentful Paint) | <= 2.5 s | 2.5 to 4.0 s | > 4.0 s |
| INP (Interaction to Next Paint) | <= 200 ms | 200 to 500 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | <= 0.1 | 0.1 to 0.25 | > 0.25 |

## Field vs lab

| Source | What it is | Use it for | Limits |
| --- | --- | --- | --- |
| CrUX (via PageSpeed Insights, Search Console, CrUX API or dashboard) | Real Chrome users, 28-day rolling p75 | The verdict; what Google uses | Needs enough traffic; lags changes by up to 28 days; Chrome only |
| Your RUM (`web-vitals` library, Next.js `useReportWebVitals`, a RUM vendor) | Your real users, any window you choose | Attribution: which element, which interaction, which page state | You must build or buy it; mind consent and privacy |
| Lighthouse / PageSpeed Insights lab | One simulated load on a throttled mid-range mobile | Debugging load performance, before/after comparison | No real interactions, so INP is replaced by TBT as a proxy; one location; variance between runs |
| DevTools Performance panel | Your machine, with throttling you set | Tracing a specific interaction or shift | Your machine is faster than your users'; always throttle CPU (4x or more) and network |

If lab passes but field fails: real users have slower devices or networks, hit uncached pages, interact during load, or see consent banners and personalised content that lab does not. If lab fails but field passes: lab is harsher than your audience; prioritise field.

## Minimal RUM in Next.js

```tsx
// app/web-vitals.tsx
'use client'
import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Send only metric data: name, value, rating, id, navigation type. No personal data.
    const body = JSON.stringify({ name: metric.name, value: metric.value, rating: metric.rating, id: metric.id, page: location.pathname })
    navigator.sendBeacon?.('/api/vitals', body)
  })
  return null
}
```

For attribution (which element or interaction), the `web-vitals` package's attribution build (`import { onINP, onLCP, onCLS } from 'web-vitals/attribution'`) reports the LCP element and its subparts, the interaction target and its phases, and the largest shift source. Gate any third-party RUM behind the site's consent rules.

## LCP

Break LCP into four subparts and fix the largest:

| Subpart | Healthy share | Causes | Fixes |
| --- | --- | --- | --- |
| Time to first byte | about 40% or less | Uncached server rendering, slow data fetches, origin far from users, redirects | Static generation or ISR for marketing pages, cache HTML at a CDN with an Australian edge, remove redirect hops (`http` to `https` to `www` should be one hop), stream with Suspense so the shell flushes early |
| Resource load delay | under 10% | LCP image discovered late: CSS background, inserted by JS, `loading="lazy"`, behind a client component | Use a real `<img>`/`next/image` in server-rendered HTML, `fetchPriority="high"` (or `preload` in Next.js 16; `priority` is deprecated there), no lazy loading above the fold, `<link rel="preconnect">` to an image CDN origin |
| Resource load duration | about 40% | Oversized image, wrong format, no `sizes` | Serve at displayed size with `sizes`, AVIF or WebP, quality around 70 to 80, crop to the visible area |
| Element render delay | under 10% | Render-blocking CSS and sync JS, web fonts blocking text, entrance animation starting at `opacity: 0`, client-side rendering | Inline or reduce critical CSS, `defer`/`async` scripts, `next/font` (swap plus fallback metrics), show the hero immediately, server components |

Text LCP (a large heading) is usually limited by fonts and render-blocking resources rather than downloads.

Also check: the LCP element differs between mobile and desktop; carousels and video posters often become the LCP; cookie banners can become the LCP on small screens (keep them compact).

## INP

An interaction's latency = input delay + processing time + presentation delay.

| Phase | Causes | Fixes |
| --- | --- | --- |
| Input delay | Main thread busy with other work: hydration, third-party scripts, timers | Reduce client JS (server components by default, `"use client"` only on leaves), `next/dynamic` for below-the-fold widgets, load third-party tags with `next/script` `strategy="lazyOnload"` or after consent, break up long tasks |
| Processing | Heavy handlers, synchronous state updates that re-render large trees, `JSON.parse` of big payloads, synchronous analytics calls | Give immediate visual feedback, then defer the rest: `startTransition`/`useTransition` for non-urgent React updates, `useDeferredValue` for filtered lists, `await scheduler.yield()` where supported with a `setTimeout(0)` fallback, memoise expensive children, move computation to a Web Worker |
| Presentation delay | Large DOM, expensive style recalculation and layout, forced synchronous layout (reading layout after writing styles) | Keep DOM small (virtualise long lists), `content-visibility: auto` on long off-screen sections, batch reads before writes, animate `transform`/`opacity` only |

Common real-world INP culprits on marketing sites: chat widgets, A/B testing scripts, tag managers firing many tags on click, mega-menus that render hundreds of links on open, accordions that animate `height` on large content, and form validation that re-renders the whole form per keystroke.

```tsx
'use client'
import { useState, useTransition } from 'react'

export function Filter({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(items)
  const [isPending, startTransition] = useTransition()
  return (
    <>
      <input value={query} onChange={(e) => {
        setQuery(e.target.value)                     // urgent: keep typing responsive
        startTransition(() => setResults(filter(items, e.target.value))) // non-urgent
      }} />
      <ResultsList items={results} dimmed={isPending} />
    </>
  )
}
```

## CLS

| Cause | Fix |
| --- | --- |
| Images, video, iframes without dimensions | `width`/`height` attributes or CSS `aspect-ratio`; `next/image` with width and height or `fill` in a sized parent |
| Web fonts swapping with different metrics | `next/font` (applies `size-adjust` fallback metrics automatically), or `@font-face` overrides (`size-adjust`, `ascent-override`, `descent-override`) for self-hosted fonts |
| Content injected above existing content (banners, consent bars, "we're hiring" strips) | Reserve the space in server HTML, or overlay at the bottom with `position: fixed` so it does not push content |
| Embeds and ads | `min-height` on the slot matching the most common size; never collapse an empty slot after load |
| Late-loading client components that change height | Render a same-size skeleton on the server; use Suspense fallbacks with matching dimensions |
| Animations of layout properties | Animate `transform` and `opacity`; shifts within 500 ms of a user input are excluded, but autoplaying ones count |
| Back/forward navigation re-renders | Keep pages eligible for the back/forward cache: no `unload` listeners, avoid `Cache-Control: no-store` on public pages |

## Third-party scripts

1. Inventory every third-party request (DevTools Network, filter by domain; Lighthouse third-party summary). List the owner and purpose of each tag.
2. Remove tags nobody owns. Load the rest after consent and after the page is interactive (`next/script` with `afterInteractive` or `lazyOnload`).
3. Replace heavy embeds with facades: a static thumbnail of a YouTube video or map that loads the real embed on click.
4. Self-host critical third-party assets (fonts) to avoid extra connections.

## Measuring before and after

- Same URL, production build, same Lighthouse version and device profile, 3 to 5 runs, report the median.
- Keep the JSON reports with the change log; `scripts/cwv_report.py before.json after.json` prints the deltas.
- A change that improves lab LCP by less than run-to-run variance (often 200 to 300 ms on mobile) is not proven; run more samples.
- After deployment, compare RUM p75 week on week, then CrUX after 28 days.
