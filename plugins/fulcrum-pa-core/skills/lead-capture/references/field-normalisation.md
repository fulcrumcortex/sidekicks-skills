# Field normalisation rules

`scripts/normalise_lead.py` applies these rules. Use this page to resolve its warnings or when you normalise by hand.

## Phone numbers

Store in E.164 (`+61` then the number without its leading 0). Show people the national format.

| Typed | Type | Store | Display |
| --- | --- | --- | --- |
| `0400 000 000`, `0400-000-000`, `400000000` | Mobile (04, rarely 05) | `+61400000000` | `0400 000 000` |
| `(02) 9000 0000`, `02 9000 0000` | Landline, NSW/ACT | `+61290000000` | `(02) 9000 0000` |
| `03 ...` | VIC/TAS | `+613...` | `(03) ...` |
| `07 ...` | QLD | `+617...` | `(07) ...` |
| `08 ...` | SA/WA/NT | `+618...` | `(08) ...` |
| `+61 (0)400 000 000`, `0061 400 000 000`, `0011 61 ...`, `61400000000` | Already international | drop the `(0)` and prefixes: `+61400000000` | national format |
| `9000 0000` (8 digits) | Landline without area code | Infer area code from the state only with a "confirm" note; otherwise ask | |
| `1300 000 000`, `1800 000 000`, `13 00 00` | Inbound or local-rate | Keep the national format; no E.164 | as typed, spaced |
| `+64 ...`, `+44 ...` | Overseas | Keep `+` and digits | Flag before any call |

Rules:

- A mobile goes in the mobile field, a landline in the phone field. If unsure, use the phone field.
- Extensions go in a note ("ext 214"), not the number.
- Never "fix" a number by guessing a digit. A wrong number is worse than a missing one.
- One person, one mobile. A shared office line does not prove two contacts are the same person.

## Email

- Trim spaces and angle brackets, remove `mailto:`, lower-case the whole address.
- Free webmail domains (gmail.com, outlook.com, bigpond.com, icloud.com and similar) say nothing about the company. Do not create or match a company from them.
- Role addresses (info@, admin@, accounts@, sales@, hello@, enquiries@, office@, reception@, bookings@) belong to a team, not a person. Never merge two contacts on a role address alone. Prefer a personal address if the message includes one.
- A plus address (`name+quote@`) is kept as typed; match on the part before the plus as a possible duplicate.

## Names

- If the person typed their name in mixed case, keep it exactly. People spell their own names correctly: `DeShawn`, `McKenzie`, `di Stefano`.
- If they typed all upper or all lower case, title-case it with these exceptions:
  - `Mc` + capital: `McAllister`.
  - `Mac`: do not guess (`MacDonald` and `Macdonald` are both common); flag to confirm.
  - Apostrophes and hyphens: `O'Neill-Ryan`, `D'Souza`.
  - Particles in surnames stay lower case: `van der Berg`, `de Silva`, `da Costa`. Confirm when it matters (a formal letter).
- Split a full name only on the first space; flag multi-part given names ("Mary Anne") and single names.
- Never infer gender, title (Mr, Ms, Dr) or ethnicity from a name. Use a title only if the person used one.

## Company names

- Standardise the legal suffix: `Pty. Ltd.`, `PTY LTD`, `P/L`, `Proprietary Limited` become `Pty Ltd`; `Limited` becomes `Ltd`.
- Keep the company's own styling when typed in mixed case: `eBay`, `KPMG`. When typed all in one case, title-case and flag acronyms to confirm.
- Lower-case small words in the middle: `and`, `of`, `the`, `for`. Keep `&`.
- Match companies on the website domain first, then the name without its legal suffix.
- Trading name and legal name differ often. Store the trading name as the company name and the legal name in a note or custom field if you have one.

## ABN and ACN

- ABN: 11 digits, shown `NN NNN NNN NNN`. Checksum: subtract 1 from the first digit, multiply the digits by 10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, add them up; the total must divide by 89.
- ACN: 9 digits, shown `NNN NNN NNN`. Checksum: weights 8 down to 1 on the first eight digits; `(10 - total mod 10) mod 10` must equal the ninth digit.
- For a company, the last 9 digits of the ABN are usually its ACN.
- A failed checksum is almost always a typo: ask the person, or check the public ABN Lookup with the owner's permission. A valid checksum does not prove the ABN is registered or active.
- Example that passes the checksum: `51 824 753 556` (the Australian Taxation Office's own published ABN, used here because it is public). The example `12 345 678 901` fails.

## Addresses

- States as `NSW`, `VIC`, `QLD`, `SA`, `WA`, `TAS`, `NT`, `ACT`.
- Postcodes are 4 digits; NT and some ACT postcodes start with 0, so store them as text.
- Postcode ranges: NSW 1000 to 2599, 2619 to 2899, 2921 to 2999; ACT 0200 to 0299, 2600 to 2618, 2900 to 2920; VIC 3000 to 3999 and 8000 to 8999; QLD 4000 to 4999 and 9000 to 9999; SA 5000 to 5999; WA 6000 to 6999; TAS 7000 to 7999; NT 0800 to 0999. A mismatch means one of them is wrong: confirm.
- Suburb in title case; street abbreviations as the person wrote them.

## Dates and times

- Store dates as ISO (`2026-11-10`). Display `Tue 10 Nov 2026`.
- When an enquiry says "next Tuesday", resolve it against the date the message was sent, not today, and show the resolved date for confirmation.
