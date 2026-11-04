// Landing page skeleton for the Next.js App Router (Next.js 15 or 16, React 19, Tailwind CSS v4).
// Copy to app/<route>/page.tsx and replace every TODO. The business below is fictional.
//
// Class names assume the semantic tokens from the design-tokens starter theme
// (bg-canvas, text-ink, text-ink-muted, border-line, bg-accent, text-on-accent,
// text-display, text-h2, py-section). Swap them for the project's own tokens.
//
// Everything here is a server component. Only <LeadForm> is a client island.

import type { Metadata } from 'next'
import Image from 'next/image'
import { LeadForm } from './lead-form'

const PAGE_URL = '/physio-same-day' // TODO: route path; metadataBase in app/layout.tsx makes it absolute
const PRIMARY_CTA = 'Book a same-day appointment' // TODO: one outcome label, reused everywhere

export const metadata: Metadata = {
  // About 50 to 60 characters. Lead with the outcome, end with the brand.
  title: 'Same-day physio appointments in Newtown | Harbourline Physio',
  // About 140 to 160 characters. Who it is for, what they get, the next step.
  description:
    'Back or neck pain that cannot wait? Book a same-day physiotherapy appointment in Newtown. Health fund rebates on the spot. Book online in two minutes.',
  alternates: { canonical: PAGE_URL },
  openGraph: {
    type: 'website',
    url: PAGE_URL,
    title: 'Same-day physio appointments in Newtown',
    description: 'Book online in two minutes. Health fund rebates on the spot.',
    images: [{ url: '/og/physio-same-day.png', width: 1200, height: 630, alt: 'Physiotherapist treating a patient' }],
    locale: 'en_AU',
  },
}

// Mark up only what is visible on the page. Validate with the Rich Results Test
// and the Schema Markup Validator before release.
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'MedicalBusiness', // TODO: the most specific LocalBusiness subtype that fits
  name: 'Harbourline Physio',
  url: 'https://www.example.com/physio-same-day',
  telephone: '+61 2 0000 0000',
  address: {
    '@type': 'PostalAddress',
    streetAddress: '1 Example Street',
    addressLocality: 'Newtown',
    addressRegion: 'NSW',
    postalCode: '2042',
    addressCountry: 'AU',
  },
}

export default function Page() {
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c') }}
      />
      <Hero />
      <ProofStrip />
      <ProblemOutcome />
      <HowItWorks />
      <Offer />
      <Faq />
      <FinalCta />
    </>
  )
}

function Hero() {
  return (
    <section aria-labelledby="hero-title" className="bg-canvas text-ink">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-section md:grid-cols-12 md:px-8">
        <div className="md:col-span-7">
          <p className="text-sm font-medium tracking-wide text-ink-muted">For desk workers in the Inner West</p>
          {/* LCP candidate: render it visible from the first paint. No opacity-0 entrance. */}
          <h1 id="hero-title" className="mt-3 text-display text-balance">
            Back pain fixed this week, not next month
          </h1>
          <p className="mt-5 max-w-prose text-lg text-ink-muted">
            Same-day appointments with a senior physiotherapist, and your health fund rebate claimed on the spot.
          </p>
          <div className="mt-8 flex flex-wrap items-center gap-4">
            <a
              href="#enquire"
              className="inline-flex min-h-11 items-center rounded-md bg-accent px-6 font-semibold text-on-accent focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus"
            >
              {PRIMARY_CTA}
            </a>
            <a href="#how-it-works" className="min-h-11 content-center underline underline-offset-4">
              See how a visit works
            </a>
          </div>
          {/* TODO: one real, attributable proof item, or delete this line */}
          <p className="mt-6 text-sm text-ink-muted">4.9 from 214 Google reviews (TODO: verify source and count)</p>
        </div>
        <div className="relative aspect-[4/5] md:col-span-5">
          <Image
            src="/images/hero-treatment.jpg" // TODO: real photo, at least 1200 px wide
            alt="A physiotherapist adjusting a patient's shoulder in a treatment room"
            fill
            sizes="(min-width: 768px) 40vw, 100vw"
            fetchPriority="high" // the LCP image: never lazy. In Next.js 16 `preload` is the alternative; `priority` is deprecated.
            className="rounded-lg object-cover"
          />
        </div>
      </div>
    </section>
  )
}

function ProofStrip() {
  return (
    <section aria-label="What clients say" className="border-y border-line">
      <figure className="mx-auto max-w-3xl px-4 py-10 text-center md:px-8">
        <blockquote className="text-xl text-balance">
          {/* TODO: real quote, with written permission */}
          &ldquo;Booked at 8 am, treated by lunch, back at my desk the next day.&rdquo;
        </blockquote>
        <figcaption className="mt-3 text-sm text-ink-muted">Alex Example, Newtown</figcaption>
      </figure>
    </section>
  )
}

function ProblemOutcome() {
  return (
    <section aria-labelledby="problem-title" className="mx-auto max-w-7xl px-4 py-section md:px-8">
      <h2 id="problem-title" className="text-h2 text-balance">Waiting two weeks makes most back pain worse</h2>
      <div className="mt-10 grid gap-8 md:grid-cols-2">
        <div>
          <h3 className="font-semibold">Usually</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-ink-muted">
            <li>The earliest booking is ten days away</li>
            <li>You pay in full, then claim the rebate later</li>
            <li>You leave without a plan for the next week</li>
          </ul>
        </div>
        <div>
          <h3 className="font-semibold">At Harbourline</h3>
          <ul className="mt-3 list-disc space-y-2 pl-5">
            <li>Same-day appointments, 7 am to 7 pm</li>
            <li>Rebate claimed on the spot</li>
            <li>A written three-exercise plan before you leave</li>
          </ul>
        </div>
      </div>
    </section>
  )
}

function HowItWorks() {
  const steps = [
    { title: 'Book online', body: 'Pick a time today. It takes about two minutes.' },
    { title: 'Get assessed', body: 'A 45-minute assessment and first treatment.' },
    { title: 'Follow the plan', body: 'Three exercises, a check-in message, and a review if you need one.' },
  ]
  return (
    <section id="how-it-works" aria-labelledby="how-title" className="bg-surface py-section">
      <div className="mx-auto max-w-7xl px-4 md:px-8">
        <h2 id="how-title" className="text-h2">How a visit works</h2>
        <ol className="mt-10 grid gap-8 md:grid-cols-3">
          {steps.map((step, i) => (
            <li key={step.title} className="border-t border-line pt-6">
              <span className="font-mono text-sm text-ink-muted" aria-hidden="true">
                {String(i + 1).padStart(2, '0')}
              </span>
              <h3 className="mt-2 text-lg font-semibold">{step.title}</h3>
              <p className="mt-2 text-ink-muted">{step.body}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}

function Offer() {
  return (
    <section aria-labelledby="offer-title" className="mx-auto max-w-3xl px-4 py-section md:px-8">
      <h2 id="offer-title" className="text-h2">What happens after you book</h2>
      <p className="mt-4 text-lg text-ink-muted">
        {/* TODO: exact next steps. Consumer prices must include GST and compulsory fees. */}
        You get a confirmation text straight away and a reminder two hours before. Cancel up to two hours ahead at no cost.
      </p>
    </section>
  )
}

function Faq() {
  // TODO: 4 to 8 real questions from calls, reviews or support.
  const faqs = [
    { q: 'Do I need a referral?', a: 'No. You can book directly.' },
    { q: 'Can I claim on my health fund?', a: 'Yes. We claim eligible rebates on the spot with most funds.' },
  ]
  return (
    <section aria-labelledby="faq-title" className="mx-auto max-w-3xl px-4 py-section md:px-8">
      <h2 id="faq-title" className="text-h2">Questions before you book</h2>
      <div className="mt-8 divide-y divide-line border-y border-line">
        {faqs.map((item) => (
          <details key={item.q} className="group py-4">
            <summary className="flex min-h-11 cursor-pointer items-center justify-between gap-4 font-semibold">
              {item.q}
              <span aria-hidden="true" className="transition-transform motion-reduce:transition-none group-open:rotate-45">+</span>
            </summary>
            <p className="mt-2 text-ink-muted">{item.a}</p>
          </details>
        ))}
      </div>
    </section>
  )
}

function FinalCta() {
  return (
    <section id="enquire" aria-labelledby="enquire-title" className="scroll-mt-24 bg-surface py-section">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 md:grid-cols-12 md:px-8">
        <div className="md:col-span-5">
          <h2 id="enquire-title" className="text-h2">{PRIMARY_CTA}</h2>
          <p className="mt-4 text-ink-muted">Tell us when suits you. We confirm by text within 15 minutes during opening hours.</p>
        </div>
        <div className="md:col-span-7">
          <LeadForm submitLabel={PRIMARY_CTA} />
        </div>
      </div>
    </section>
  )
}
