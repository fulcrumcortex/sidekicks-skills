'use server'

// Server Action for the landing page lead form. Copy next to lead-form.tsx.
// Validates on the server every time, rejects obvious bots, and never logs personal data.
// TODO: replace deliverLead() with the destination the business already uses (CRM, help desk, inbox).

export type LeadFormState = {
  status: 'idle' | 'error' | 'success'
  message?: string
  fieldErrors?: Partial<Record<'name' | 'email' | 'phone' | 'details', string>>
  values?: { name?: string; email?: string; phone?: string; details?: string }
}

const MIN_FILL_MS = 3000
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/

function normaliseAuPhone(raw: string): string | null {
  const digits = raw.replace(/[\s()-]/g, '')
  if (/^\+61[2-478]\d{8}$/.test(digits)) return digits
  if (/^0[2-478]\d{8}$/.test(digits)) return `+61${digits.slice(1)}`
  return null
}

export async function submitLead(_prev: LeadFormState, formData: FormData): Promise<LeadFormState> {
  // Spam controls: honeypot and time trap. Bots get the same success state as people.
  const honeypot = String(formData.get('company_website') ?? '')
  const renderedAt = Number(formData.get('rendered_at') ?? 0)
  if (honeypot || !renderedAt || Date.now() - renderedAt < MIN_FILL_MS) {
    return { status: 'success', message: 'Thanks. We will be in touch shortly.' }
  }
  // TODO: add a per-IP and per-email rate limit using the host's KV store.

  const name = String(formData.get('name') ?? '').trim()
  const email = String(formData.get('email') ?? '').trim().toLowerCase()
  const phoneRaw = String(formData.get('phone') ?? '').trim()
  const details = String(formData.get('details') ?? '').trim()
  const values = { name, email, phone: phoneRaw, details }

  const fieldErrors: LeadFormState['fieldErrors'] = {}
  if (!name) fieldErrors.name = 'Enter your name.'
  else if (name.length > 100) fieldErrors.name = 'Use 100 characters or fewer.'
  if (!EMAIL_RE.test(email)) fieldErrors.email = 'Enter an email like name@example.com.'
  const phone = phoneRaw ? normaliseAuPhone(phoneRaw) : null
  if (phoneRaw && !phone) fieldErrors.phone = 'Enter an Australian number like 0400 000 000.'
  if (details.length > 2000) fieldErrors.details = 'Use 2000 characters or fewer.'

  if (Object.keys(fieldErrors).length > 0) {
    return { status: 'error', message: 'Check the highlighted fields.', fieldErrors, values }
  }

  try {
    await deliverLead({ name, email, phone, details, marketingConsent: formData.get('marketing') === 'yes' })
  } catch {
    console.error('lead delivery failed') // no personal data in logs
    return {
      status: 'error',
      message: 'We could not send your request. Call us on 02 0000 0000 or email hello@example.com.',
      values,
    }
  }
  return { status: 'success', message: 'Thanks. We will text you within 15 minutes during opening hours.' }
}

async function deliverLead(lead: {
  name: string
  email: string
  phone: string | null
  details: string
  marketingConsent: boolean
}): Promise<void> {
  // TODO: server-side call with credentials from process.env. Throw on a non-2xx response.
  void lead
  throw new Error('deliverLead not implemented')
}
