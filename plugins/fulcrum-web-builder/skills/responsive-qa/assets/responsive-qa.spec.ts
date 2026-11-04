// Responsive QA sweep for Playwright Test. Copy to tests/responsive-qa.spec.ts.
// Run against a production build:  BASE_URL=http://localhost:3000 npx playwright test tests/responsive-qa.spec.ts
// (or the project's package-manager equivalent, for example `pnpm exec playwright test ...`).
// Screenshots land in test-results/responsive/<page>/<viewport>-<scheme>.png and are referenced in the issue log.
// The checks report problems as soft assertions so one run lists every issue.

import { test, expect, type Page } from '@playwright/test'

const BASE_URL = process.env.BASE_URL ?? 'http://localhost:3000'
const PAGES = ['/', '/pricing', '/contact'] // TODO: the routes in scope

const VIEWPORTS = [
  { name: '320', width: 320, height: 640 },
  { name: '360', width: 360, height: 780 },
  { name: '375', width: 375, height: 667 },
  { name: '414', width: 414, height: 896 },
  { name: '667x375-landscape', width: 667, height: 375 },
  { name: '768', width: 768, height: 1024 },
  { name: '1024', width: 1024, height: 768 },
  { name: '1280', width: 1280, height: 800 },
  { name: '1440', width: 1440, height: 900 },
  { name: '1920', width: 1920, height: 1080 },
]

const SCHEMES = ['light', 'dark'] as const

async function overflowingElements(page: Page) {
  return page.evaluate(() => {
    const vw = document.documentElement.clientWidth
    const out: string[] = []
    for (const el of Array.from(document.querySelectorAll('body *'))) {
      const r = el.getBoundingClientRect()
      if (r.width === 0 || r.height === 0) continue
      if (r.right > vw + 1 || r.left < -1) {
        // Skip children of elements that intentionally scroll horizontally.
        let p = el.parentElement
        let insideScroller = false
        while (p) {
          const ox = getComputedStyle(p).overflowX
          if (ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip') { insideScroller = true; break }
          p = p.parentElement
        }
        if (!insideScroller) {
          const id = el.id ? `#${el.id}` : ''
          const cls = typeof el.className === 'string' && el.className ? `.${el.className.trim().split(/\s+/).slice(0, 3).join('.')}` : ''
          out.push(`${el.tagName.toLowerCase()}${id}${cls} right=${Math.round(r.right)} vw=${vw}`)
        }
      }
    }
    return out.slice(0, 20)
  })
}

async function smallTargets(page: Page) {
  return page.evaluate(() => {
    const sel = 'a[href], button, input:not([type=hidden]), select, textarea, [role=button], [tabindex]:not([tabindex="-1"])'
    const out: string[] = []
    for (const el of Array.from(document.querySelectorAll<HTMLElement>(sel))) {
      const r = el.getBoundingClientRect()
      if (r.width === 0 || r.height === 0) continue
      // Inline links inside running text are exempt from WCAG 2.5.8.
      const inlineText = el.tagName === 'A' && getComputedStyle(el).display === 'inline' && el.closest('p, li')
      if (inlineText) continue
      if (r.width < 24 || r.height < 24) {
        out.push(`${el.tagName.toLowerCase()} "${(el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 30)}" ${Math.round(r.width)}x${Math.round(r.height)}`)
      }
    }
    return out.slice(0, 20)
  })
}

for (const path of PAGES) {
  for (const vp of VIEWPORTS) {
    for (const scheme of SCHEMES) {
      test(`${path} @ ${vp.name} ${scheme}`, async ({ page }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height })
        await page.emulateMedia({ colorScheme: scheme, reducedMotion: 'reduce' })
        await page.goto(BASE_URL + path, { waitUntil: 'networkidle' })

        const slug = path === '/' ? 'home' : path.replace(/\W+/g, '-').replace(/^-|-$/g, '')
        await page.screenshot({ path: `test-results/responsive/${slug}/${vp.name}-${scheme}.png`, fullPage: true })

        const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth)
        const clientWidth = await page.evaluate(() => document.documentElement.clientWidth)
        expect.soft(scrollWidth, `horizontal scroll at ${vp.name}: ${(await overflowingElements(page)).join(' | ')}`).toBeLessThanOrEqual(clientWidth)

        if (vp.width < 1024) {
          const small = await smallTargets(page)
          expect.soft(small, `targets under 24x24 at ${vp.name}`).toEqual([])
        }
      })
    }
  }
}
