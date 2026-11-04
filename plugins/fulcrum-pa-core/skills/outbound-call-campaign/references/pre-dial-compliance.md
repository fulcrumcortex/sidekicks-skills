# Pre-dial compliance checklist

Read this before any outbound call campaign. Mark every line **pass**, **fix** (can be corrected before launch) or **block** (the campaign does not start). Missing evidence is not a pass.

## 1. What kind of call is this?

| Question | If yes |
| --- | --- |
| Does the call offer, advertise or promote goods, services, land, a business opportunity, or ask for a donation? | It is a telemarketing call. Sections 2 to 6 all apply. |
| Is it only about an existing transaction (appointment confirmation, delivery time, a service the person already bought)? | Calling hours, identification, disclosure and opt-out still apply as good practice. If any offer is added to the script, treat it as telemarketing. |
| Is it market or social research with no selling? | Different rules apply (research calls have their own hours). Confirm with the user before proceeding. |

## 2. Do Not Call Register

- [ ] **The user has washed the list** against the Do Not Call Register, through their own Register account or an access seeker. No Fulcrum product does this. (Block if missing for telemarketing calls.)
- [ ] **The wash is current.** A wash result is valid for 30 days. Re-wash before any call made more than 30 days after the wash date, including retry waves. (Block if expired.)
- [ ] **Registered numbers are removed** unless the person has given consent that is recorded (source, date, what they agreed to). Consent to "be contacted" about one thing does not cover calls about something else. (Block per number.)
- [ ] **Exemptions are checked narrowly.** Only certain senders are exempt from the Register, such as some government bodies, registered charities, political parties and candidates, religious organisations, and educational institutions calling current or former students' households. A business that is not one of these is not exempt because a call is "only a courtesy call". Exempt callers still follow the calling-hours and identification rules.
- [ ] **Business and mobile numbers are washed too.** Do not assume a number is exempt from the wash because it looks like a business line or a mobile.

## 3. Consent and source

- [ ] Every number has a recorded source (form, purchase, enquiry, event registration). Numbers with no source are excluded, not "probably fine".
- [ ] Purchased or rented lists have consent evidence that names your business or clearly covers your call. A vendor's assurance alone is not evidence.
- [ ] Consent records are kept with the campaign: who, when, how, wording shown.

## 4. Calling hours (Telemarketing and Research Calls Industry Standard)

- [ ] Telemarketing calls only in the **recipient's local time**: Monday to Friday 9am to 8pm, Saturday 9am to 5pm. No calls on Sunday or on a national public holiday, unless the person has agreed to calls at that time.
- [ ] National public holidays are blocked: 1 January, 26 January, Good Friday, Easter Monday, 25 April, 25 December and 26 December. Check the current standard for how substitute days are treated, and avoid local public holidays as a courtesy.
- [ ] The list is split by time zone. A platform window set in Sydney time is not the recipient's window: at 9am in Sydney during daylight saving it is 6am in Perth. Use `scripts/calling_windows.py` for the date.
- [ ] Recipients with unknown state are scheduled inside the window that is valid in every Australian time zone.

| Recipient state | Time zone | Offset from Sydney, April to October | Offset from Sydney, October to April (daylight saving) |
| --- | --- | --- | --- |
| NSW, ACT, VIC, TAS | Sydney/Melbourne/Hobart | 0 | 0 |
| QLD | Brisbane (no daylight saving) | 0 | -1 hour |
| SA | Adelaide | -30 min | -30 min |
| NT | Darwin (no daylight saving) | -30 min | -1 hour 30 min |
| WA | Perth (no daylight saving) | -2 hours | -3 hours |

## 5. On the call

- [ ] The call opens with AI disclosure and recording notice, then the caller's name, the business name and the purpose, before any pitch.
- [ ] The calling number is shown (caller ID not withheld) and can be called back.
- [ ] The agent ends the call promptly when asked, and on a stop request confirms the person will not be called again.
- [ ] The agent can say where the business got the number if asked, from the recorded source.
- [ ] The agent never says or implies it is a person. Misleading conduct rules under the Australian Consumer Law apply to what the agent says.

## 6. Recording

- [ ] Recording consent rules differ between states, and some require every party to agree. Announcing the recording at the start of every call is the practical way to meet them all.
- [ ] If the person objects to recording, the agent ends the call and a person calls back. Do not continue a recorded call after an objection.
- [ ] "Skip disclosure" settings for known callers are not used on campaign calls to people who have not already given recording consent.

## 7. Opt-out handling

- [ ] Stop requests during a call are added to the do-not-contact list the same day and removed from every active campaign, journey and follow-up task.
- [ ] SMS replies of STOP or UNSUBSCRIBE are honoured for SMS; that does not by itself stop calls, so add the person to the call do-not-contact list as well.
- [ ] Email unsubscribes from any linked email leg are actioned within five working days.

## 8. Privacy

- [ ] The objective collects only what the stated purpose needs.
- [ ] No health or other sensitive information is collected or mentioned on a marketing call. Where the business is a clinic or disability provider, the agent does not confirm to anyone else that a person is a client.
- [ ] Wrong-person calls end without revealing the purpose in detail.
- [ ] Recordings and transcripts are kept and shared under the business's privacy policy.

## 9. People who may be vulnerable

- [ ] The agent ends politely and flags for a person if the recipient seems confused, distressed, unwell or under 18. These numbers are not retried.

This is a practical checklist, not legal advice.
