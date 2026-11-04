# Fulcrum Sidekick skills

Practical skills for **humans + AI as one team**. This library has **57 skills in 8 plugins**. They cover everyday personal-assistant work, the industries Fulcrum serves, and building websites and UX.

A **Sidekick** is an AI teammate. A **skill** is a reusable set of instructions that teaches that teammate one kind of work. It says when the skill applies, what context to gather, which steps to follow, where a person must approve, and how to check the result. Teach the method once and every Sidekick can repeat it.

Skills guide behaviour. **Installing a skill does not connect an app, grant permissions or give access to your inbox, customer data or production systems.** What an agent can actually read or change comes from the tools and account permissions in your host.

[Fulcrum Cortex on GitHub](https://fulcrumcortex.github.io/) · [Product documentation](https://fulcrumcortex.github.io/documentation/) · [Fulcrum Cortex](https://fulcrumcortex.com/) · [Fulcrum CRM](https://fulcrumcrm.app/) · [Lyre](https://lyre.au/) · [Fulcrum Mail](https://fulcrumail.app/) · [Fulcrum Code](https://fulcrumcode.app/)

## Install

### Install in Claude Code

Add this repository as a plugin marketplace, then install the packs you want:

```text
/plugin marketplace add fulcrumcortex/sidekicks-skills
/plugin install fulcrum-pa-core@fulcrum-sidekicks
/plugin install fulcrum-web-builder@fulcrum-sidekicks
```

The marketplace is named `fulcrum-sidekicks`. Install only the industry packs you need, for example `fulcrum-property@fulcrum-sidekicks` or `fulcrum-care-workforce@fulcrum-sidekicks`. Run `/plugin` to browse, update or remove them. Plugin skills are namespaced, for example `fulcrum-pa-core:invoice-chasing`.

### Install in Fulcrum Code

In a Fulcrum Code session:

```text
/marketplace add https://github.com/fulcrumcortex/sidekicks-skills
/marketplace install fulcrum-sidekicks
/skills
```

The marketplace name and plugin name are both `fulcrum-sidekicks`. Review the skills before installing. Start a new session if the installed skills are not yet listed. These commands are verified against the current Fulcrum Code marketplace implementation; they are not generic commands for every agent host.

For example:

```text
Use the fulcrum-crm-follow-up skill.
Read the latest enquiry for the contact I selected.
Prepare a reply and a next-action suggestion. Do not send it.
```

The other packs install the same way by plugin name, for example `/marketplace install fulcrum-pa-core` or `/marketplace install fulcrum-web-builder`.

To uninstall the pack in Fulcrum Code:

```text
/marketplace remove-plugin fulcrum-sidekicks
```

See [Skills, Sidekicks and specialist agents](https://fulcrumcortex.github.io/documentation/code/skills-and-agents/).

### Copy individual skills

Each folder under `plugins/<plugin>/skills/` is a self-contained skill. Copy the whole folder, not just `SKILL.md`, because skills read files from their own `references/`, `assets/` and `scripts/`.

```bash
git clone https://github.com/fulcrumcortex/sidekicks-skills.git
cp -R sidekicks-skills/plugins/fulcrum-pa-core/skills/invoice-chasing ~/.claude/skills/
```

For a project-only install, use `.claude/skills/` in the project. Other hosts have their own skills folder; Codex, for example, normally uses `~/.codex/skills/`. Fulcrum Code reads single-file user skills from `~/.fulcrum/skills/`.

### Use a skill

Ask for the outcome. The agent loads the matching skill from its description, or you can name the skill:

```text
Use the invoice-chasing skill. Here is our receivables export.
Show me who to chase this week and draft the reminders. Do not send anything.
```

## Skills

### fulcrum-pa-core: personal assistant for any business

| Skill | What it does |
| --- | --- |
| [daily-briefing](plugins/fulcrum-pa-core/skills/daily-briefing/SKILL.md) | A morning brief that fits on one phone screen (decisions, meetings, replies waiting, money, risks), plus a Friday weekly review. |
| [meeting-scheduler](plugins/fulcrum-pa-core/skills/meeting-scheduler/SKILL.md) | Finds times across people and Australian time zones, proposes 2–3 slots, and sends the invite after approval. Covers reschedules and no-shows. |
| [meeting-prep](plugins/fulcrum-pa-core/skills/meeting-prep/SKILL.md) | A one-page brief before an external meeting: attendees, history, open deals, goal, questions, likely objections and the next step to ask for. |
| [lead-capture](plugins/fulcrum-pa-core/skills/lead-capture/SKILL.md) | Turns an enquiry from any channel into a clean CRM record, with a duplicate check, source, consent, next task and a speed-to-lead reply draft. |
| [pipeline-review](plugins/fulcrum-pa-core/skills/pipeline-review/SKILL.md) | A weekly review of stale, slipped and stuck deals, with a best, likely and worst forecast and actions for each owner. |
| [outbound-call-campaign](plugins/fulcrum-pa-core/skills/outbound-call-campaign/SKILL.md) | Plans, pilots and runs an AI voice call campaign: list cleaning, pre-dial compliance, objective design, retries, SMS follow-up and CRM write-back. |
| [invoice-chasing](plugins/fulcrum-pa-core/skills/invoice-chasing/SKILL.md) | Builds an aged-receivables view, checks for disputes and unmatched payments, and sends staged reminders after approval. |
| [quote-and-proposal](plugins/fulcrum-pa-core/skills/quote-and-proposal/SKILL.md) | Turns an enquiry into a quote or proposal priced only from your own price list, with correct GST, validity, terms and a follow-up schedule. |
| [outreach-compliance-check](plugins/fulcrum-pa-core/skills/outreach-compliance-check/SKILL.md) | A pre-flight pass/fix/block check of an email, SMS or call campaign against the Spam Act, Do Not Call Register, calling hours, disclosure and APP 7. |
| [review-response](plugins/fulcrum-pa-core/skills/review-response/SKILL.md) | Classifies public reviews and drafts replies that never disclose private information. Escalates serious reviews and requests new ones without incentives or gating. |
| [process-to-skill](plugins/fulcrum-pa-core/skills/process-to-skill/SKILL.md) | Interviews you about a recurring process, or reads an SOP, and writes a new Sidekick skill with approval gates and checks. |

### fulcrum-property: real estate and property management

| Skill | What it does |
| --- | --- |
| [open-home-follow-up](plugins/fulcrum-property/skills/open-home-follow-up/SKILL.md) | Sorts open-home attendees by intent, checks consent on the register, drafts same-day follow-ups and feeds feedback to the vendor report. |
| [vendor-report](plugins/fulcrum-property/skills/vendor-report/SKILL.md) | A weekly vendor campaign report: enquiry and inspection numbers, feedback themes, price reactions, comparables, an honest market read and recommendations. |
| [lease-billing-check](plugins/fulcrum-property/skills/lease-billing-check/SKILL.md) | Compares a signed lease with what is actually billed and lists mismatches with clause references, confidence ratings and a correction draft. |
| [tenancy-issue-triage](plugins/fulcrum-property/skills/tenancy-issue-triage/SKILL.md) | Turns a property management inbox into a ranked queue (repairs, arrears, strata, utilities, insurance, owner approvals) with owners, deadlines and drafts. |

### fulcrum-hospitality: restaurants, venues and accommodation

| Skill | What it does |
| --- | --- |
| [reservation-desk](plugins/fulcrum-hospitality/skills/reservation-desk/SKILL.md) | Handles booking requests against seats, kitchen pacing and service periods, plus the waitlist, allergy notes, reminders, no-shows and the daily run-sheet. |
| [function-enquiry-quote](plugins/fulcrum-hospitality/skills/function-enquiry-quote/SKILL.md) | Qualifies function and catering enquiries, quotes from the venue's own packages, holds the date, follows up and prepares the event order. |
| [guest-stay-communications](plugins/fulcrum-hospitality/skills/guest-stay-communications/SKILL.md) | Guest messages from pre-arrival to the post-stay review request, including changes and cancellations under property policy and complaint recovery. |
| [hospitality-prospect-research](plugins/fulcrum-hospitality/skills/hospitality-prospect-research/SKILL.md) | A de-duplicated, scored list of hospitality prospects with a source for every claim, loaded into the CRM after confirmation. |

### fulcrum-care-workforce: NDIS practices, care teams and clinics

| Skill | What it does |
| --- | --- |
| [ndis-client-onboarding](plugins/fulcrum-care-workforce/skills/ndis-client-onboarding/SKILL.md) | A new-participant pack from the plan and intake details: a service agreement draft, a schedule of supports you verify, consent forms and a missing-information checklist. |
| [progress-notes](plugins/fulcrum-care-workforce/skills/progress-notes/SKILL.md) | Turns voice or rough notes into objective SOAP, goal-linked or shift notes, flags possible incidents and never adds anything not in the source. |
| [ndis-billing-check](plugins/fulcrum-care-workforce/skills/ndis-billing-check/SKILL.md) | Reconciles delivered sessions against invoices and claims, finds unbilled work, duplicates and over-budget lines, and prepares a claim file for approval. |
| [roster-planner](plugins/fulcrum-care-workforce/skills/roster-planner/SKILL.md) | Builds or repairs a weekly care roster against skills, compliance expiry, availability, continuity, travel and rest breaks, and flags award questions. |
| [clinic-appointment-reminders](plugins/fulcrum-care-workforce/skills/clinic-appointment-reminders/SKILL.md) | Minimal-information reminders, confirmations, no-show follow-up, waitlist backfill and recall by SMS or AI call. |

### fulcrum-trades-field: trades, construction and automotive

| Skill | What it does |
| --- | --- |
| [job-confirmation](plugins/fulcrum-trades-field/skills/job-confirmation/SKILL.md) | Day-before confirmations by SMS or call, reschedules, a run-sheet per technician by suburb, on-the-way messages and job close-out. |
| [takeoff-to-quote](plugins/fulcrum-trades-field/skills/takeoff-to-quote/SKILL.md) | Prices a takeoff or bill of materials into a draft quote and purchase orders: waste, labour, stock shortfalls, provisional sums and GST. Flags every missing price. |
| [workshop-job-card](plugins/fulcrum-trades-field/skills/workshop-job-card/SKILL.md) | An automotive job card from intake to handover, with plain-language fault codes, written approval before extra work and an Australian Consumer Law checklist. |
| [site-daily-report](plugins/fulcrum-trades-field/skills/site-daily-report/SKILL.md) | Turns voice notes, photos and messages into a site diary (labour, delays, variations, RFIs, WHS escalation) and a weekly client summary. |

### fulcrum-professional-services: consultants, brokers and recruiters

| Skill | What it does |
| --- | --- |
| [client-engagement-setup](plugins/fulcrum-professional-services/skills/client-engagement-setup/SKILL.md) | Takes a won client to a signed engagement (scope, fee basis, conflict check, kickoff, handover) and then runs a weekly unbilled WIP check. |
| [insurance-renewal-campaign](plugins/fulcrum-professional-services/skills/insurance-renewal-campaign/SKILL.md) | Runs renewals at 60, 30, 14 and 7 days out with factual messages, and passes advice questions to the licensee's authorised people. |
| [recruitment-pipeline](plugins/fulcrum-professional-services/skills/recruitment-pipeline/SKILL.md) | Runs the job and candidate pipelines with evidence-based shortlists, bias guardrails and candidate consent before any submission. |

### fulcrum-web-builder: websites, UX and UI

| Skill | What it does |
| --- | --- |
| [landing-page-build](plugins/fulcrum-web-builder/skills/landing-page-build/SKILL.md) | Builds a conversion landing page in Next.js App Router, TypeScript and Tailwind v4, with metadata, JSON-LD and an accessible form. Deploys only after approval. |
| [design-tokens](plugins/fulcrum-web-builder/skills/design-tokens/SKILL.md) | A primitive → semantic → component token system in Tailwind v4 `@theme`, with OKLCH colour, fluid type, dark mode and a contrast checker. |
| [accessibility-audit](plugins/fulcrum-web-builder/skills/accessibility-audit/SKILL.md) | A WCAG 2.2 AA audit combining automated scans with keyboard and screen-reader checks. Findings come with criterion, fix and code. |
| [seo-structured-data-audit](plugins/fulcrum-web-builder/skills/seo-structured-data-audit/SKILL.md) | A technical SEO and JSON-LD audit with a prioritised fix list, Next.js Metadata API code and an Australian local-business focus. |
| [core-web-vitals-pass](plugins/fulcrum-web-builder/skills/core-web-vitals-pass/SKILL.md) | Diagnoses and fixes LCP, INP and CLS from field and lab data, measuring before and after. |
| [conversion-copy-review](plugins/fulcrum-web-builder/skills/conversion-copy-review/SKILL.md) | Reviews and rewrites marketing copy and calls to action, with a before/after table, a claims register and an Australian Consumer Law checklist. |
| [responsive-qa](plugins/fulcrum-web-builder/skills/responsive-qa/SKILL.md) | Responsive and cross-browser QA across a breakpoint matrix, with Playwright screenshots and an issue log. |
| [ux-critique](plugins/fulcrum-web-builder/skills/ux-critique/SKILL.md) | A structured UX critique using adapted Nielsen heuristics, a friction count, 0–4 severity and concrete redesigns. |
| [anti-slop-design-review](plugins/fulcrum-web-builder/skills/anti-slop-design-review/SKILL.md) | Detects the generic AI-template look and redirects it with findings and a three-move plan, backed by a source scanner. |

### fulcrum-sidekicks: starter pack for the Fulcrum suite

| Skill | What it does |
| --- | --- |
| [fulcrum-coordinate-work](plugins/fulcrum-sidekicks/skills/fulcrum-coordinate-work/SKILL.md) | Coordinates a business outcome across people and tools, with owners, dependencies and evidence. |
| [fulcrum-code-change](plugins/fulcrum-sidekicks/skills/fulcrum-code-change/SKILL.md) | Makes a reviewable code change that keeps project conventions and validates the behaviour. |
| [fulcrum-release-check](plugins/fulcrum-sidekicks/skills/fulcrum-release-check/SKILL.md) | Verifies an authorised release from source to live. |
| [fulcrum-crm-follow-up](plugins/fulcrum-sidekicks/skills/fulcrum-crm-follow-up/SKILL.md) | Prepares a customer follow-up grounded in the CRM record and the agreed next step. |
| [fulcrum-crm-data-cleanup](plugins/fulcrum-sidekicks/skills/fulcrum-crm-data-cleanup/SKILL.md) | Reviews CRM data quality without merging uncertain matches. |
| [fulcrum-voice-agent-setup](plugins/fulcrum-sidekicks/skills/fulcrum-voice-agent-setup/SKILL.md) | Configures a focused Lyre voice agent. |
| [fulcrum-call-review](plugins/fulcrum-sidekicks/skills/fulcrum-call-review/SKILL.md) | Reviews a call and checks that the promised actions happened. |
| [fulcrum-inbox-triage](plugins/fulcrum-sidekicks/skills/fulcrum-inbox-triage/SKILL.md) | Triages an inbox with context. |
| [fulcrum-booking-setup](plugins/fulcrum-sidekicks/skills/fulcrum-booking-setup/SKILL.md) | Sets up and checks a booking page. |
| [fulcrum-meeting-actions](plugins/fulcrum-sidekicks/skills/fulcrum-meeting-actions/SKILL.md) | Turns a meeting into accountable actions. |
| [fulcrum-document-review](plugins/fulcrum-sidekicks/skills/fulcrum-document-review/SKILL.md) | Reviews a business document. |
| [fulcrum-file-sharing](plugins/fulcrum-sidekicks/skills/fulcrum-file-sharing/SKILL.md) | Shares a file with the intended audience. |
| [fulcrum-wallet-check](plugins/fulcrum-sidekicks/skills/fulcrum-wallet-check/SKILL.md) | Reconciles a Wallet balance question. |
| [fulcrum-campaign-brief](plugins/fulcrum-sidekicks/skills/fulcrum-campaign-brief/SKILL.md) | Prepares a campaign brief from verified product facts. |
| [fulcrum-project-planning](plugins/fulcrum-sidekicks/skills/fulcrum-project-planning/SKILL.md) | Plans work with acceptance evidence. |
| [fulcrum-cad-design-brief](plugins/fulcrum-sidekicks/skills/fulcrum-cad-design-brief/SKILL.md) | Prepares an editable CAD design brief. |
| [fulcrum-private-message-draft](plugins/fulcrum-sidekicks/skills/fulcrum-private-message-draft/SKILL.md) | Drafts a private message from supplied context. |

## What to expect from a skill

- **Works with or without Fulcrum.** Every skill works with whatever mail, calendar, CRM or files your host has connected, or with material you paste in. Where a Fulcrum product helps, the skill says how and links to the matching guide.
- **Approval before anything goes out.** Skills that send email, SMS or chat messages, issue invoices, publish, deploy or place calls show you the exact content, recipients and sending account first, then wait for your yes. A draft is not approval. After an uncertain result, the skill checks sent items or call history before retrying, so nothing goes out twice.
- **Australian checklists, not legal advice.** Where it applies, a skill includes a checklist for the Spam Act, the Do Not Call Register, telemarketing calling hours, call-recording consent, the Privacy Act and the NDIS Practice Standards. You stay responsible for compliance. In particular, **you must wash call lists against the Do Not Call Register yourself**, directly or through an access seeker. Lyre checks your organisation's own do-not-contact list and calling hours, which is a different control.
- **No invented facts.** Skills price only from your own price lists, cite a source for every research claim, and ask for anything they cannot find. For current Fulcrum plans and inclusions, see the [pricing page](https://fulcrumcortex.com/pricing).

## The Fulcrum suite

| Product | Website | Purpose |
| --- | --- | --- |
| Fulcrum Cortex | [fulcrumcortex.com](https://fulcrumcortex.com/) | The AI execution layer for business |
| Fulcrum Sessions | [fulcrumcortex.com/sessions](https://fulcrumcortex.com/sessions) | The orchestrator: humans + AI as one team |
| Fulcrum Code | [fulcrumcode.app](https://fulcrumcode.app/) | Coding agent for building and running software |
| Fulcrum CRM | [fulcrumcrm.app](https://fulcrumcrm.app/) | Contacts, companies, deals and industry modules |
| Lyre | [lyre.au](https://lyre.au/) | Voice agents, calling and SMS |
| Fulcrum Mail | [fulcrumail.app](https://fulcrumail.app/) | Email, calendar, booking pages and the workspace suite |
| Fulcrum CAD | [fulcrumcad.app](https://fulcrumcad.app/) | Editable architectural design in the browser |
| Kyphra | [kyphra.app](https://kyphra.app/) | Private messaging |

Product guides for all of these are in the [documentation](https://fulcrumcortex.github.io/documentation/). Fulcrum CRM industry modules vary by account; check [fulcrumcrm.app](https://fulcrumcrm.app/) for what is currently available. Find Fulcrum Cortex elsewhere through the [profile directory](https://fulcrumcortex.github.io/profiles/) and the [Cortex blog](https://fulcrumcortex.com/blog).

## Repository layout

```text
.claude-plugin/marketplace.json     marketplace "fulcrum-sidekicks", lists every plugin
plugins/<plugin>/.claude-plugin/    plugin.json for each pack
plugins/<plugin>/skills/<skill>/    SKILL.md plus optional references/, assets/, scripts/
catalog.json                        showcase index for the starter pack
scripts/validate.py                 repository checks (standard library only)
scripts/check_catalog.py            starter-pack showcase index check
tests/smoke/, tests/fixtures/       smoke cases and sample inputs for every helper script
```

## Validate and contribute

```bash
python3 scripts/validate.py            # front matter, manifests, JSON, banned words, links, script smoke tests
python3 scripts/validate.py --offline  # everything except the live link check
python3 scripts/validate.py --no-smoke # skip the helper-script smoke tests
python3 scripts/check_catalog.py
```

Read [CONTRIBUTING.md](CONTRIBUTING.md) for the folder layout, the SKILL.md template and the rules every skill follows. Keep examples fictional and never include credentials, internal hostnames or customer data. Helper scripts use the Python standard library and make no network calls.

## Licence

[MIT](LICENSE). The skills are instructions, not professional advice. Check the outputs before you rely on them.

## Practical articles

- [What a Sidekick skill actually gives your AI teammate — Hashnode](https://fulcrumcortex.hashnode.dev/what-a-sidekick-skill-actually-gives-your-ai-teammate)
- [Turn a customer enquiry into an accountable next action — LinkedIn](https://www.linkedin.com/pulse/turn-customer-enquiry-accountable-next-action-fulcrum-cortex-mvhye/)
- [A practical first week with Cortex Chat](https://fulcrumcortex.github.io/articles/first-week-cortex-chat/)

Some platforms limit signed-out viewing; publication does not guarantee indexing.
