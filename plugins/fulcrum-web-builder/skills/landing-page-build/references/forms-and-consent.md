# Lead forms: validation, spam control and consent

## Field budget

| Goal | Fields |
| --- | --- |
| Call-back or quote | Name, phone, suburb or postcode, one job description field |
| Demo or consultation | Name, work email, organisation, one qualifying select (team size or use case) |
| Download or newsletter | Email only (plus separate marketing consent) |

Each extra required field must be justified by the follow-up. Phone is optional unless the follow-up is a call.

## Markup rules

- Every input has a visible `<label>`; placeholders are examples, not labels.
- Use the right `type` and `autocomplete`: `name`, `email`, `tel`, `organization`, `postal-code`. This also satisfies WCAG 3.3.7 Redundant Entry for returning visitors whose browser fills fields.
- Mark required fields in text ("required"), not only with colour or an asterisk.
- Errors: inline under the field, linked with `aria-describedby`, `aria-invalid="true"` on the field, plus a summary at the top of the form with `role="alert"` or focus moved to it after a failed submit. Error text says how to fix it: "Enter an email like name@example.com".
- The submit button keeps its label and shows a pending state ("Sending...") with `aria-disabled` or `disabled` while the request runs, to prevent double submits.
- On success, replace the form with a message that says what happens next and when, and move focus to that message.

## Validation

- Validate on the server in the Server Action or route handler, every time. Client validation is a convenience.
- If the project already uses a schema library (zod, valibot), use it. Otherwise validate by hand: trim, check length limits (name at most 100, message at most 2000), a pragmatic email pattern, and Australian phone normalisation (strip spaces; accept `04xxxxxxxx`, `+614xxxxxxxx`, landlines with area code).
- Return field-level errors and the submitted values (minus anything sensitive) so the form re-renders without losing input.

## Spam control, in escalating order

1. **Honeypot:** a hidden text field (`tabIndex={-1}`, `autoComplete="off"`, visually hidden with CSS, `aria-hidden="true"` on its wrapper). Reject silently when filled.
2. **Time trap:** a signed or server-checked timestamp; reject submissions faster than about 3 seconds after render.
3. **Rate limit:** per IP and per email, for example 5 per 10 minutes, using the host's KV store or an in-memory limiter for a single instance.
4. **Challenge:** only if 1 to 3 are not enough, add a privacy-respecting challenge (for example Cloudflare Turnstile or hCaptcha). Disclose it in the privacy policy. Never block keyboard or screen-reader users; prefer invisible or managed modes.

Never show a different response to bots than to people in a way that reveals the rule; return the same success state.

## Where submissions go

- Write to the system the business already uses (CRM, help desk, shared inbox) through a server-side call with credentials in environment variables.
- Log failures server-side without the personal data. If delivery fails, show the visitor a fallback (phone number or email address) rather than a false success.
- Test with fictional details (`Test Person`, `test@example.com`, `0400 000 000`) and confirm the record in the destination.

## Consent and privacy notes (Australia first)

- **Collection notice:** near the submit button: who is collecting, why, who it may be shared with, and a link to the privacy policy. Example: "We use these details to reply to your enquiry. See our privacy policy."
- **Marketing consent:** a separate, unticked checkbox for newsletters or SMS offers. An enquiry is not consent to marketing.
- **Analytics:** Australia has no cookie-banner statute, but the Privacy Act and the Australian Privacy Principles apply to organisations covered by the Act (generally those with turnover above $3 million, plus some smaller businesses such as health service providers). Disclose analytics and advertising tools in the privacy policy, minimise identifiers, and do not pass personal information to them.
- **EU or UK audiences:** non-essential cookies and similar storage need prior opt-in consent. Gate the analytics script behind the consent decision and load it with `next/script` `strategy="afterInteractive"` (or `lazyOnload`) only after consent.
- **Session replay and heatmaps:** mask all form inputs by default or do not use them on form pages.

This is a practical checklist, not legal advice.
