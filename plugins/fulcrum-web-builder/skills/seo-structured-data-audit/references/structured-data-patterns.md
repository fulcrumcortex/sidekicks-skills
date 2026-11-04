# Structured data patterns and Next.js implementation

All examples are fictional. Replace every value; never ship placeholder data. Use absolute URLs.

## Google support status (checked November 2026)

| Type | Google rich result? | Notes |
| --- | --- | --- |
| Organization | Yes (logo, knowledge panel details) | Put on the home page or about page, once. `logo` at least 112 × 112 px. `sameAs` lists official profiles. |
| LocalBusiness (and subtypes) | Yes | Use the most specific subtype (`Electrician`, `Dentist`, `Restaurant`). Must match the Google Business Profile. |
| Product with Offer | Yes (price, availability, shipping, returns) | Only on pages for a specific product. Prices in `AUD` as shown on the page. |
| Article / BlogPosting | Yes | `headline`, `image`, `datePublished`, `dateModified`, `author` with a name and URL. |
| BreadcrumbList | Yes on desktop | Since January 2025 Google shows only the domain on mobile results; desktop still shows breadcrumbs. Markup unchanged. |
| FAQPage | No | Google stopped showing FAQ rich results in 2026 (deprecation announced for 7 May 2026). Earlier, from 2023, they were limited to well-known government and health sites. Markup is harmless; it earns no Google snippet. |
| HowTo | No | Removed from Google results in 2023. |
| Review snippets on your own business | No | Self-serving reviews on LocalBusiness or Organization are not shown. |

Other search engines and AI assistants may read schema.org markup differently; that is a reason to keep markup accurate, not to add types for their own sake.

## Organization (site-wide, once)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.example.com/#organization",
  "name": "Example Joinery",
  "legalName": "Example Joinery Pty Ltd",
  "url": "https://www.example.com/",
  "logo": "https://www.example.com/logo-512.png",
  "sameAs": ["https://social.example.com/example-joinery"],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+61 3 0000 0000",
    "contactType": "customer service",
    "areaServed": "AU",
    "availableLanguage": "en"
  }
}
```

## LocalBusiness for an Australian storefront

```json
{
  "@context": "https://schema.org",
  "@type": "Bakery",
  "@id": "https://www.example.com/#business",
  "name": "Example Bakehouse",
  "url": "https://www.example.com/",
  "image": "https://www.example.com/images/shopfront.jpg",
  "telephone": "+61 8 0000 0000",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "12 Example Lane",
    "addressLocality": "Fremantle",
    "addressRegion": "WA",
    "postalCode": "6160",
    "addressCountry": "AU"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": -32.0000, "longitude": 115.0000 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:00", "closes": "16:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "07:00", "closes": "13:00" }
  ]
}
```

- `addressRegion` uses the state or territory abbreviation: NSW, VIC, QLD, WA, SA, TAS, ACT, NT.
- `telephone` in international format `+61` without the leading 0 of the area code.
- Public holiday hours: add an `OpeningHoursSpecification` with `validFrom`/`validThrough`, and update the Google Business Profile special hours too.
- `taxID` can carry an ABN if the business already shows it on the site. It is optional and not used for Google rich results.

## Service-area business (no public address)

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Example Plumbing",
  "url": "https://www.example.com/",
  "telephone": "+61 7 0000 0000",
  "address": { "@type": "PostalAddress", "addressLocality": "Logan", "addressRegion": "QLD", "postalCode": "4114", "addressCountry": "AU" },
  "areaServed": [
    { "@type": "City", "name": "Logan" },
    { "@type": "City", "name": "Ipswich" },
    { "@type": "AdministrativeArea", "name": "Gold Coast" }
  ]
}
```

Omit `streetAddress` when the business hides its address on Google Business Profile.

## Product with Offer

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Example Oak Bench, 1.8 m",
  "image": ["https://www.example.com/images/bench-1x1.jpg", "https://www.example.com/images/bench-16x9.jpg"],
  "description": "Solid Victorian ash bench, oiled finish.",
  "sku": "EX-BENCH-180",
  "brand": { "@type": "Brand", "name": "Example Joinery" },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/products/oak-bench",
    "priceCurrency": "AUD",
    "price": "1290.00",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
```

The `price` must equal the price shown to consumers on the page, which in Australia includes GST.

## Article

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to choose timber for an outdoor bench",
  "image": ["https://www.example.com/blog/timber-16x9.jpg"],
  "datePublished": "2026-10-02T09:00:00+10:00",
  "dateModified": "2026-10-20T09:00:00+11:00",
  "author": [{ "@type": "Person", "name": "Sam Example", "url": "https://www.example.com/about/sam" }],
  "publisher": { "@id": "https://www.example.com/#organization" }
}
```

Use the correct offset for daylight saving (+10:00 or +11:00 for Sydney and Melbourne; Brisbane stays +10:00).

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Services", "item": "https://www.example.com/services" },
    { "@type": "ListItem", "position": 2, "name": "Kitchen joinery", "item": "https://www.example.com/services/kitchens" }
  ]
}
```

The last item may omit `item`. The trail must match the visible breadcrumb.

## Combining with @graph

Use one script tag with `@graph` and `@id` references to avoid repeating the organisation on every page:

```json
{ "@context": "https://schema.org", "@graph": [ { "@type": "Organization", "@id": "https://www.example.com/#organization", "name": "Example Joinery" }, { "@type": "WebPage", "@id": "https://www.example.com/services/kitchens#webpage", "url": "https://www.example.com/services/kitchens", "publisher": { "@id": "https://www.example.com/#organization" } } ] }
```

## Validation routine

1. Rich Results Test (search.google.com/test/rich-results) on the live or preview URL, or on pasted code: checks Google feature eligibility.
2. Schema Markup Validator (validator.schema.org): checks schema.org syntax for every type, including ones Google ignores.
3. After release, Search Console Enhancements reports show errors across the site over the following days.

## Next.js App Router implementation

Root layout:

```tsx
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://www.example.com'),
  title: { default: 'Example Joinery', template: '%s | Example Joinery' },
  openGraph: { siteName: 'Example Joinery', locale: 'en_AU', type: 'website' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en-AU">
      <body>{children}</body>
    </html>
  )
}
```

Data-driven route:

```tsx
// app/services/[slug]/page.tsx
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getService } from '@/lib/services'

type Props = { params: Promise<{ slug: string }> }

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const service = await getService(slug)
  if (!service) return {}
  return {
    title: service.seoTitle,
    description: service.seoDescription,
    alternates: { canonical: `/services/${slug}` },
    openGraph: { title: service.seoTitle, description: service.seoDescription, url: `/services/${slug}` },
  }
}

export default async function Page({ params }: Props) {
  const { slug } = await params
  const service = await getService(slug)
  if (!service) notFound()
  const jsonLd = { '@context': 'https://schema.org', '@type': 'Service', name: service.name, provider: { '@id': 'https://www.example.com/#organization' } }
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c') }} />
      {/* page */}
    </>
  )
}
```

`params` is a Promise in current Next.js versions; await it. `generateMetadata` and the page share fetches when they use the same cached data function.

Hreflang alternates (only when real alternates exist):

```ts
alternates: {
  canonical: '/pricing',
  languages: { 'en-AU': '/pricing', 'en-NZ': 'https://www.example.co.nz/pricing', 'x-default': '/pricing' },
}
```

robots and sitemap:

```ts
// app/robots.ts
import type { MetadataRoute } from 'next'
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/', disallow: ['/api/', '/account/'] }],
    sitemap: 'https://www.example.com/sitemap.xml',
  }
}

// app/sitemap.ts
import type { MetadataRoute } from 'next'
import { getAllServices } from '@/lib/services'
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const services = await getAllServices()
  return [
    { url: 'https://www.example.com/', lastModified: new Date('2026-10-01') },
    ...services.map((s) => ({ url: `https://www.example.com/services/${s.slug}`, lastModified: s.updatedAt })),
  ]
}
```

Open Graph image: add `app/opengraph-image.tsx` (or a static `opengraph-image.png`) at the route level; Next.js emits the `og:image` tags with dimensions.

Preview and staging deployments should send `noindex` (for example `robots: { index: false }` in metadata when an environment variable says so) so they never compete with production. Check that this switch is off in production before launch.
