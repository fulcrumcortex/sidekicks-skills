# Privacy Act, APP 7 and suppression hygiene: every channel

## 1. Does the Privacy Act apply?

- [ ] Most businesses with annual turnover above $3 million are covered by the Privacy Act 1988 and the Australian Privacy Principles (APPs).
- [ ] Smaller businesses are generally exempt, **except** health service providers (including allied health and many disability support providers), businesses that trade in personal information, and some others. Treat the APP checks below as the standard either way; they are what customers and regulators expect.

## 2. APP 7: direct marketing

APP 7 does not apply to the extent the Spam Act or the Do Not Call Register Act applies, so for email, SMS and telemarketing calls those Acts are the main test. APP 7 matters for other direct marketing (mail, social messaging outside the Spam Act, calls not covered by the Register Act) and as a baseline for good practice.

- [ ] Personal information used for marketing was collected from the person, and they would reasonably expect it to be used this way; or they consented.
- [ ] If the information came from a third party, or they would not expect the use, they consented (or it was impracticable to ask) and every message includes a prominent opt-out statement.
- [ ] Every marketing message gives a simple way to opt out, and opt-outs are honoured within a reasonable time and free of charge.
- [ ] If a person asks where their information came from, the business can tell them.
- [ ] **Sensitive information** (health, disability, racial or ethnic origin, religious beliefs, sexual orientation, criminal record and others) is used for marketing only with the person's consent. (Block if not.)

## 3. Collection, notice and use

- [ ] The collection notice or privacy policy shown when the details were collected mentions marketing use.
- [ ] Only the data the campaign needs is used. Merge fields do not pull in notes, health details or account information.
- [ ] Messages do not reveal that a person is a patient, client or NDIS participant to anyone who could read a shared inbox or phone. Generic wording is safer for clinics and disability providers.
- [ ] The audience export is stored only where needed and deleted after the send if it is a copy.

## 4. Suppression list hygiene

- [ ] **One suppression record per person, honoured by every tool.** Email unsubscribes, SMS STOP replies, call do-not-contact requests, spam complaints and hard bounces are merged before each send, and each tool's list is updated.
- [ ] **Suppressed people are kept as suppressed records, not deleted.** Deleting them means a later import adds them back. Keep the minimum: address or number, channel, date, source of the request.
- [ ] **Suppression applies across purposes.** An unsubscribe from one newsletter is treated as an unsubscribe from that sender's marketing on that channel, unless the person chose specific preferences.
- [ ] **New imports are checked against suppression** before they join any audience.
- [ ] **Turnaround:** suppression changes reach every sending tool within five working days, and before the next send.
- [ ] **Bounces and complaints:** hard bounces are suppressed after the first bounce; addresses that report spam are suppressed immediately.
- [ ] **Deceased and closed accounts** are suppressed with a reason.
- [ ] **Audit trail:** for each campaign, keep the audience criteria, count, suppression lists applied and the date.

This is a practical checklist, not legal advice.
