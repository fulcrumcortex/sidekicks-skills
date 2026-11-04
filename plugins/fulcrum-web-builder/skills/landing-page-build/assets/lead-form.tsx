'use client'

// Accessible lead form island (React 19 useActionState). Copy to app/<route>/lead-form.tsx.
// Pairs with lead-form-action.ts. Class names assume the design-tokens starter theme.

import { useActionState, useEffect, useRef, useState } from 'react'
import { submitLead, type LeadFormState } from './lead-form-action'

const initialState: LeadFormState = { status: 'idle' }

export function LeadForm({ submitLabel }: { submitLabel: string }) {
  const [state, formAction, pending] = useActionState(submitLead, initialState)
  const [renderedAt, setRenderedAt] = useState(0)
  const statusRef = useRef<HTMLDivElement>(null)

  useEffect(() => setRenderedAt(Date.now()), [])
  // Move focus to the result so screen-reader and keyboard users hear it.
  useEffect(() => {
    if (state.status !== 'idle') statusRef.current?.focus()
  }, [state])

  if (state.status === 'success') {
    return (
      <div ref={statusRef} tabIndex={-1} role="status" className="rounded-md border border-line p-6">
        <p className="font-semibold">{state.message}</p>
      </div>
    )
  }

  const err = state.fieldErrors ?? {}
  const v = state.values ?? {}

  return (
    <form action={formAction} noValidate className="grid gap-5">
      {state.status === 'error' && (
        <div ref={statusRef} tabIndex={-1} role="alert" className="rounded-md border border-danger p-4">
          {state.message}
        </div>
      )}

      <Field id="name" label="Name" error={err.name}>
        <input id="name" name="name" type="text" autoComplete="name" required defaultValue={v.name}
          aria-invalid={!!err.name} aria-describedby={err.name ? 'name-error' : undefined} className="field" />
      </Field>

      <Field id="email" label="Email" error={err.email}>
        <input id="email" name="email" type="email" autoComplete="email" required defaultValue={v.email}
          aria-invalid={!!err.email} aria-describedby={err.email ? 'email-error' : undefined} className="field" />
      </Field>

      <Field id="phone" label="Mobile (optional)" error={err.phone}>
        <input id="phone" name="phone" type="tel" autoComplete="tel" inputMode="tel" defaultValue={v.phone}
          aria-invalid={!!err.phone} aria-describedby={err.phone ? 'phone-error' : undefined} className="field" />
      </Field>

      <Field id="details" label="What do you need help with? (optional)" error={err.details}>
        <textarea id="details" name="details" rows={4} defaultValue={v.details}
          aria-invalid={!!err.details} aria-describedby={err.details ? 'details-error' : undefined} className="field" />
      </Field>

      {/* Marketing consent is separate and unticked. An enquiry is not consent to marketing. */}
      <div className="flex items-start gap-3">
        <input id="marketing" name="marketing" type="checkbox" value="yes" className="mt-1 size-5" />
        <label htmlFor="marketing" className="text-sm">Send me occasional tips and offers. Unsubscribe any time.</label>
      </div>

      {/* Honeypot and time trap. Hidden from people and assistive technology. */}
      <div aria-hidden="true" className="absolute -left-[10000px] h-px w-px overflow-hidden">
        <label htmlFor="company_website">Leave this field empty</label>
        <input id="company_website" name="company_website" type="text" tabIndex={-1} autoComplete="off" />
      </div>
      <input type="hidden" name="rendered_at" value={renderedAt} />

      <p className="text-sm text-ink-muted">
        We use these details to reply to your request. See our <a href="/privacy" className="underline">privacy policy</a>.
      </p>

      <button type="submit" disabled={pending}
        className="inline-flex min-h-11 items-center justify-center rounded-md bg-accent px-6 font-semibold text-on-accent disabled:opacity-70 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-focus">
        {pending ? 'Sending...' : submitLabel}
      </button>
    </form>
  )
}

function Field({ id, label, error, children }: { id: string; label: string; error?: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-2">
      <label htmlFor={id} className="font-medium">{label}</label>
      {children}
      {error && <p id={`${id}-error`} className="text-sm text-danger">{error}</p>}
    </div>
  )
}

// Add to your global CSS (Tailwind v4):
// @utility field { @apply min-h-11 w-full rounded-md border border-line bg-canvas px-3 text-ink focus-visible:outline-2 focus-visible:outline-focus; }
