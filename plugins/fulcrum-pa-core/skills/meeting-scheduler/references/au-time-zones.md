# Australian time zones and daylight saving

Read this when a meeting crosses states or countries, or when the meeting date is near a daylight-saving change. Always work in IANA zone names and let the calendar or `scripts/find_slots.py` do the arithmetic on the actual meeting date.

## Zones by state and territory

| Place | IANA zone | Standard | Daylight saving | Observes DST? |
| --- | --- | --- | --- | --- |
| NSW (most), ACT | `Australia/Sydney` | AEST UTC+10 | AEDT UTC+11 | Yes |
| Victoria | `Australia/Melbourne` | AEST UTC+10 | AEDT UTC+11 | Yes |
| Tasmania | `Australia/Hobart` | AEST UTC+10 | AEDT UTC+11 | Yes |
| Queensland | `Australia/Brisbane` | AEST UTC+10 | none | **No** |
| South Australia | `Australia/Adelaide` | ACST UTC+9:30 | ACDT UTC+10:30 | Yes |
| Broken Hill (NSW) | `Australia/Broken_Hill` | ACST UTC+9:30 | ACDT UTC+10:30 | Yes, follows SA |
| Northern Territory | `Australia/Darwin` | ACST UTC+9:30 | none | **No** |
| Western Australia | `Australia/Perth` | AWST UTC+8 | none | **No** |
| Lord Howe Island | `Australia/Lord_Howe` | UTC+10:30 | UTC+11 | Yes, a half-hour shift |
| Eucla area (WA) | `Australia/Eucla` | UTC+8:45 | none | No, informal zone |
| Norfolk Island | `Pacific/Norfolk` | UTC+11 | UTC+12 | Yes |

Australian daylight saving runs from **2:00 am on the first Sunday in October to 3:00 am (daylight time) on the first Sunday in April**.

## What that means in practice

- **Summer (October to April): five mainland times.** At 12:00 in Sydney it is 11:00 in Brisbane, 11:30 in Adelaide, 10:30 in Darwin and 09:00 in Perth.
- **Winter (April to October): three mainland times.** Sydney and Brisbane match, Adelaide and Darwin match, Perth is two hours behind the east coast.
- **Brisbane vs Sydney** is the classic trap. A recurring 09:00 Brisbane meeting moves from 10:00 to 09:00 Sydney time in April and back in October. Recurring events must be anchored to one organiser's zone; tell the other side when their local time will change.
- **Perth vs east coast** is 2 hours in winter and 3 hours in summer. A 16:00 Sydney summer slot is 13:00 in Perth; a 09:00 Sydney summer slot is 06:00 in Perth, which is not offerable.
- "AEST" in a summer invitation is usually wrong for Sydney or Melbourne. Write "Sydney time (AEDT)" or "Brisbane time (AEST)" and name the city as well as the abbreviation.

## Common overseas pairs

| Pair | Gap | When it changes |
| --- | --- | --- |
| Sydney to Auckland | NZ ahead 2 hours; 3 hours for about a week | NZ starts DST on the last Sunday in September, a week before NSW. Both end on the first Sunday in April. |
| Sydney to London | 11 h (Australian summer), 9 h (Australian winter), 10 h in between | UK changes on the last Sunday in March and the last Sunday in October, so the gap shifts four times a year. |
| Sydney to US West Coast | 19 h when Sydney is on AEDT and the US on standard time; 17 h in the Australian winter; 18 h in between | US changes on the second Sunday in March and the first Sunday in November. |
| Sydney to Singapore | 3 h (summer), 2 h (winter) | Singapore has no DST. |

Overlap windows with Europe and the US are thin. A 09:00 to 17:00 Sydney day and an 08:00 to 18:00 London day never overlap: 08:00 in London is 17:00 in Sydney in the Australian winter and 19:00 in the Australian summer. Someone has to stretch. Offer early-morning or evening Sydney slots only with the owner's agreement, and say which side is stretching.

## Dates and the international date line

- Monday afternoon in Los Angeles is Tuesday morning in Sydney. Always write the weekday and date for each zone.
- Confirm public holidays for every state involved; they differ (for example, Queensland and Western Australia have their own holiday dates). Treat a public holiday as a day off unless the person says otherwise.

## Writing times in messages

- Lead with the recipient's zone: "Tuesday 10 November, 10:00 to 10:45 Brisbane time (11:00 Sydney time)".
- Use 24-hour times or am/pm consistently within one message.
- For a group across three or more zones, attach a table instead of stacking brackets.
