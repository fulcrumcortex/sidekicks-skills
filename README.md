# Fulcrum Sidekick skills

Practical skills for **humans + AI as one team**. This starter library contains **17 skills across nine Sidekick roles** for the Fulcrum suite: coordinate work, build software, follow up customers, prepare voice agents, organise a workspace, plan marketing and delivery, develop design briefs and draft private messages.

A Sidekick is an AI teammate. A skill is a reusable method: what context to gather, how to approach the task, what to verify and where its authority stops. **Installing a skill does not connect an app, grant permissions, create an autonomous employee or include model/phone usage.** Tools and account access come from your host environment.

[Meet the Sidekicks](https://fulcrumcortex.github.io/sidekicks/) · [Screenshots and examples](https://fulcrumcortex.com/sidekicks) · [Product documentation](https://fulcrumcortex.github.io/documentation/) · [Fulcrum Cortex](https://fulcrumcortex.com/)

## Choose a role

| Sidekick | What it helps you do | Skills |
| --- | --- | --- |
| [Coordination Sidekick](https://fulcrumcortex.github.io/sidekicks/coordinator/) | Coordinate a business request across people and tools with clear owners, dependencies and evidence. | [Coordinate a business outcome](plugins/fulcrum-sidekicks/skills/fulcrum-coordinate-work/SKILL.md) |
| [Developer Sidekick](https://fulcrumcortex.github.io/sidekicks/developer/) | Investigate code, make a bounded change, run the relevant checks and verify an authorised release. | [Make a reviewable code change](plugins/fulcrum-sidekicks/skills/fulcrum-code-change/SKILL.md), [Verify a release from source to live](plugins/fulcrum-sidekicks/skills/fulcrum-release-check/SKILL.md) |
| [Sales Sidekick](https://fulcrumcortex.github.io/sidekicks/sales/) | Prepare grounded follow-ups and keep contact data useful without inventing commitments or merging uncertain matches. | [Prepare a customer follow-up](plugins/fulcrum-sidekicks/skills/fulcrum-crm-follow-up/SKILL.md), [Review CRM data quality](plugins/fulcrum-sidekicks/skills/fulcrum-crm-data-cleanup/SKILL.md) |
| [Voice Sidekick](https://fulcrumcortex.github.io/sidekicks/voice/) | Prepare focused Lyre agents, review what callers asked and check whether promised actions actually happened. | [Configure a focused voice agent](plugins/fulcrum-sidekicks/skills/fulcrum-voice-agent-setup/SKILL.md), [Review a call and its follow-through](plugins/fulcrum-sidekicks/skills/fulcrum-call-review/SKILL.md) |
| [Workspace Sidekick](https://fulcrumcortex.github.io/sidekicks/workspace/) | Triage email, prepare booking pages, extract meeting actions, review documents and manage requested file access. | [Triage an inbox with context](plugins/fulcrum-sidekicks/skills/fulcrum-inbox-triage/SKILL.md), [Set up and check a booking page](plugins/fulcrum-sidekicks/skills/fulcrum-booking-setup/SKILL.md), [Turn a meeting into accountable actions](plugins/fulcrum-sidekicks/skills/fulcrum-meeting-actions/SKILL.md), [Review a business document](plugins/fulcrum-sidekicks/skills/fulcrum-document-review/SKILL.md), [Share a file with the intended audience](plugins/fulcrum-sidekicks/skills/fulcrum-file-sharing/SKILL.md), [Reconcile a Wallet balance question](plugins/fulcrum-sidekicks/skills/fulcrum-wallet-check/SKILL.md) |
| [Marketing Sidekick](https://fulcrumcortex.github.io/sidekicks/marketing/) | Turn verified product facts into a campaign brief, practical article and channel-specific copy. | [Prepare a grounded campaign brief](plugins/fulcrum-sidekicks/skills/fulcrum-campaign-brief/SKILL.md) |
| [Delivery Sidekick](https://fulcrumcortex.github.io/sidekicks/delivery/) | Turn a delivery brief into a practical plan with dependencies, acceptance criteria and a visible handoff. | [Plan work with acceptance evidence](plugins/fulcrum-sidekicks/skills/fulcrum-project-planning/SKILL.md) |
| [Design Sidekick](https://fulcrumcortex.github.io/sidekicks/design/) | Prepare a constrained spatial brief and, when connected, review a concept in the editable CAD model. | [Prepare an editable CAD design brief](plugins/fulcrum-sidekicks/skills/fulcrum-cad-design-brief/SKILL.md) |
| [Private communications Sidekick](https://fulcrumcortex.github.io/sidekicks/private-comms/) | Draft a private update from supplied context without assuming access to encrypted conversations or keys. | [Draft a private message](plugins/fulcrum-sidekicks/skills/fulcrum-private-message-draft/SKILL.md) |

## Install in Fulcrum Code

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

To uninstall the pack in Fulcrum Code:

```text
/marketplace remove-plugin fulcrum-sidekicks
```

## Use an individual skill in another host

Each directory under [`plugins/fulcrum-sidekicks/skills`](plugins/fulcrum-sidekicks/skills) contains `SKILL.md` and optional host display metadata. Copy the selected **skill directory**, preserving its `SKILL.md`, into your host's documented skills location. For Codex that is normally `~/.codex/skills/`; follow your installation's configuration if it differs. Do not copy this repository's README as a skill.

The `.claude-plugin` files describe the marketplace packaging. Actual automatic discovery and available tools depend on the host. No integration server or credential is bundled.

## Fulcrum suite: websites and product destinations

The first group links to product websites. Calendar, Meetings, Drive and Wallet share the Mail workspace; their links open product surfaces and may require sign-in. They are not separate invented marketing domains.

| Product | Website / product destination | Purpose |
| --- | --- | --- |
| Fulcrum Cortex | [fulcrumcortex.com](https://fulcrumcortex.com/) | AI execution layer for business |
| Fulcrum Sessions | [fulcrumcortex.com/sessions](https://fulcrumcortex.com/sessions) | Humans + AI as one team; the orchestrator |
| Fulcrum Code | [fulcrumcode.app](https://fulcrumcode.app/) | Terminal coding agent |
| Fulcrum CRM | [fulcrumcrm.app](https://fulcrumcrm.app/) | Contacts, companies, deals and business workflows |
| Lyre | [lyre.au](https://lyre.au/) | Voice agents, calling and SMS |
| Fulcrum Mail | [fulcrumail.app](https://fulcrumail.app/) | Email and the workspace suite |
| Fulcrum CAD | [fulcrumcad.app](https://fulcrumcad.app/) | Editable architectural design in the browser |
| Kyphra | [kyphra.app](https://kyphra.app/) | Private messaging |
| Fulcrum Docs | [docs.fulcrumail.app](https://docs.fulcrumail.app/) | Document editing and collaboration |
| Calendar and booking pages | [fulcrumail.app/calendar](https://fulcrumail.app/calendar) | Workspace calendar and guest booking links |
| Meetings | [fulcrumail.app/meetings](https://fulcrumail.app/meetings) | Workspace video meetings |
| Drive | [fulcrumail.app/drive](https://fulcrumail.app/drive) | Workspace files, folders and sharing |
| Wallet | [fulcrumail.app/wallet](https://fulcrumail.app/wallet) | Account credit, plans and billing |

The CRM also provides sales, project management, workforce and industry modules. Check the [CRM website](https://fulcrumcrm.app/) for current availability; these skills do not promise that every module is enabled for every account.

## Find Fulcrum Cortex

These are public profile destinations supplied for the brand. Publishing/member profiles can use personal handles; they are not all separate product websites. Some platforms restrict signed-out access or indexing. A listing or backlink is not a guarantee of search visibility.

[Gravatar](https://gravatar.com/ninjatranquil3a6a7d8b8f) · [solo.to](https://solo.to/fulcrumcortex) · [Linktree](https://linktr.ee/fulcrumcortex) · [Medium](https://medium.com/@dom_36426/about) · [F6S](https://www.f6s.com/member/dom-rutili) · [Substack](https://substack.com/@fulcrumcortex) · [Hashnode](https://hashnode.com/@fulcrumcortex) · [X](https://x.com/fulcrumcortex) · [Wakelet](https://wakelet.com/@fulcrumcortex) · [LinkedIn](https://www.linkedin.com/company/fulcrum-cortex/about/) · [Instagram](https://www.instagram.com/fulcrumcortex/)

[Profile directory](https://fulcrumcortex.github.io/profiles/) · [Latest Cortex articles](https://fulcrumcortex.com/blog)

Feedspot and Tumblr are omitted until a public profile is confirmed. This repository contains no account login URLs, passwords, private customer records or recovery information.

## What to expect from a skill

The agent should use the available tool connection and your existing authority. A request for a draft stays a draft. If you already authorised sending, saving or publishing, the skill can support that action and requires a check of its actual result. Uncertain external results should be reconciled before a retry to avoid duplicate sends, bookings or payments.

Product UI details live in the [documentation](https://fulcrumcortex.github.io/documentation/). Current account settings and product availability remain authoritative. CAD concepts require appropriate professional review before construction use; these skills do not provide certification.

## Validate and contribute

`catalog.json` is the index used by the showcase pages. Every skill name, role and path must match the actual files. Run:

```bash
python3 scripts/check_catalog.py
```

The repository contains only instructions and display metadata, not executable product integrations. The first release was also tested with the Fulcrum Code marketplace parser, installation copy and skill loader in an isolated temporary directory. That verifies packaging and discovery, not live CRM, calls, payments or message delivery.

When proposing a change, include a realistic task that shows why the instruction changes the outcome. Keep the scope narrow, references current and examples fictional. Do not add a mandatory approval step for actions the user has already authorised.
