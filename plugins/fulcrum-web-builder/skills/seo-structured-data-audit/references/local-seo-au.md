# Local SEO for Australian small businesses

## NAP consistency

Name, address and phone must read the same everywhere a customer or search engine sees them.

| Source | Name | Address | Phone | Hours | Website URL |
| --- | --- | --- | --- | --- | --- |
| Website footer and contact page | | | | | |
| LocalBusiness JSON-LD | | | | | |
| Google Business Profile | | | | | |
| Apple Business Connect / Apple Maps | | | | | |
| Bing Places | | | | | |
| Facebook page | | | | | |
| Industry directories the business uses | | | | | |

Rules:
- Use the trading name customers know, consistently. Do not add keywords or suburbs to the business name on Google Business Profile ("Example Plumbing | Emergency Plumber Logan") unless that is the registered trading name; it breaches Google's guidelines.
- One address format: unit and street, suburb, state abbreviation, postcode (`Unit 3, 12 Example Street, Logan QLD 4114`).
- One primary phone. Tracking numbers on the website are acceptable if the profile lists the main number as primary and the tracking number as additional.
- Same website URL (protocol, `www` or not, trailing slash) on every profile, ideally the canonical home or location page.

## Service-area businesses

- Trades and mobile services without a customer-facing premises hide the address on Google Business Profile and set service areas instead.
- On the site, list the real service area in text and in `areaServed`. A map of the area helps people more than a list of 80 suburbs.
- One page per genuinely different location or service is fine. Pages that differ only by suburb name are doorway pages and can be demoted.

## Multi-location businesses

- One location page per physical location with its own NAP, hours, photos, staff or team details and directions; one Google Business Profile per location linked to that page.
- LocalBusiness markup on each location page, with a `parentOrganization` reference to the Organization `@id`.

## Reviews

- Ask every genuine customer, in the same way. Do not offer incentives for positive reviews only, gate requests to happy customers, or write reviews for the business.
- Under the Australian Consumer Law, fake or misleading testimonials and reviews, or suppressing negative ones, can be misleading conduct. Display reviews faithfully, including when quoting them on the site.
- Respond to reviews without revealing a customer's personal or health information.

This is a practical checklist, not legal advice.

## Details that often go wrong

- Holiday hours: update Google Business Profile special hours before public holidays, including state-specific ones (for example the King's Birthday date differs in Queensland and Western Australia).
- Business categories: the primary category on Google Business Profile drives which searches the profile appears for; match it to the main service, and mirror it with the LocalBusiness subtype.
- ABN: show it where the business normally does (footer, invoices, terms). It is not required in schema; `taxID` is optional.
- Licence numbers (builders, electricians, plumbers): display them as required by the state regulator; they are trust signals but not schema requirements.
- `lang="en-AU"` on `<html>`, Australian spelling, prices in AUD including GST for consumers, and local phone formats in visible text (`03 0000 0000`) with `+61` in `tel:` links and schema.
