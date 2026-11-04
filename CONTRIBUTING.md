# Contributing a Sidekick skill

A Sidekick is an AI teammate. A skill teaches it one kind of work: when the skill applies, which context to gather, which steps to follow, where a person must approve, and how to check the result. Every skill in this repository follows the conventions below so the library reads as one system.

## Layout

```text
plugins/<plugin-name>/
  .claude-plugin/plugin.json
  skills/<skill-name>/
    SKILL.md            required: frontmatter + procedure (under ~250 lines)
    references/*.md     optional: detail loaded only when needed
    assets/*            optional: templates the skill fills in (Markdown, CSV, JSON)
    scripts/*.py        optional: deterministic helpers, Python standard library only
```

- `name` is lowercase letters, digits and single hyphens, at most 64 characters, and matches the folder name.
- `description` is at most 1024 characters, written in the third person. It says what the skill produces **and** when to use it, including the phrases a person is likely to type ("chase overdue invoices", "who owes us money"). Descriptions are how an agent decides to load a skill, so be specific and slightly eager.
- Frontmatter holds only `name` and `description`. Some hosts ignore other fields.
- `SKILL.md` links to every reference file it uses, with a line saying when to read it. References link one level deep; they do not chain to further references.
- Scripts run with `python3 script.py --help`, read input from files or stdin, write to stdout, and make no network calls.

## SKILL.md template

```markdown
---
name: example-skill
description: Produces <the outcome> from <the inputs>. Use when the user asks to <typical requests>, mentions <trigger words>, or <situation>. Works with any inbox, calendar or CRM; uses Fulcrum <product> when it is connected.
---

# <Outcome-first title>

<Two or three sentences: the outcome, who it is for, and the endpoint ("a reviewed draft", "an updated record", "a sent message").>

## When to use

- <situations>
- Not for: <neighbouring tasks, naming the better skill when one exists>

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| ... | ... | Ask once, or proceed with a stated assumption |

## Procedure

1. <Concrete, ordered steps. Name the decision rules.>
2. ...
N. **Approval gate.** <Present exactly what will go out, to whom and from which account. Wait for an explicit yes.>

## Output

<The exact shape of the deliverable: a table, a draft, a checklist. Point to assets/ templates.>

## Check before you finish

- [ ] <Evidence of success the agent must confirm>
- [ ] <Report done, drafted, pending and failed separately>

## Guardrails

- <Privacy, compliance checklist, things never to invent>

## With Fulcrum

<Optional. Only features documented on the docs site, with the doc link. The skill must still work without Fulcrum.>

## Learn more

- [<Descriptive anchor>](https://fulcrumcortex.github.io/documentation/...)
- (1 to 3 links in total)
```

## Rules every skill follows

**Works without Fulcrum.** Every skill works with whatever mail, calendar, CRM or files the host has connected, or with material the person pastes in. The "With Fulcrum" section explains how Fulcrum Mail, Calendar, Lyre, Fulcrum CRM, Fulcrum Code or Sessions help, using only behaviour described in the [documentation](https://fulcrumcortex.github.io/documentation/). Do not invent product features, buttons, modules or integrations.

**Outward actions need confirmation.** Before any skill sends an email, SMS or chat message, issues an invoice, publishes content, books on someone else's behalf or places a call, it shows the exact content, recipients and sending account and waits for an explicit yes for that batch. A draft is not approval. After an uncertain result (a timeout or an unclear error), check the sent items or call history before retrying, so nothing goes twice.

**Australian compliance as checklists, not legal advice.** Where relevant, include a short checklist and the line "This is a practical checklist, not legal advice." Cover only what applies:

- Spam Act 2003 for commercial email and SMS: consent (express or inferred), identification of the sender, and a working unsubscribe that is honoured within five working days.
- Do Not Call Register Act 2006 for telemarketing calls: the person must wash call lists against the Register themselves (or through an access seeker) before calling, unless an exemption applies. **Never claim that Lyre or any Fulcrum product washes numbers against the Register.** Lyre checks your organisation's own do-not-contact list and calling hours; that is a different control.
- Telemarketing calling hours under the industry standard, and state-based call-recording consent rules.
- Privacy Act 1988 and the Australian Privacy Principles: collect only what is needed, use it for the purpose it was given, keep health and other sensitive information to the minimum.
- NDIS Practice Standards and the NDIS Code of Conduct for disability support work.

**Never write certain things.** The CRM is only ever called "Fulcrum CRM". Do not hardcode prices; link to [current plans](https://fulcrumcortex.com/pricing) instead. Do not include secrets, tokens, internal hostnames, real customer names or real customer data. Use fictional examples with obviously fictional names and `example.com` addresses, and Australian `04xx xxx xxx` numbers written as `0400 000 000`.

**Style.** Australian English (organisation, prioritise, enrol). Plain, specific sentences. No emojis, no hype ("revolutionary", "seamless", "unlock"). Prefer tables and checklists over long prose. Tell the agent what to do when information is missing or a step fails.

**Links.** End with a "Learn more" section of 1 to 3 relevant links to the documentation (`https://fulcrumcortex.github.io/documentation/...`) or the product sites (fulcrumcortex.com, fulcrumcrm.app, fulcrumail.app, lyre.au, fulcrumcode.app). Every link must return HTTP 200; `python3 scripts/validate.py` checks this.

## Validate

```bash
python3 scripts/validate.py            # structure, JSON, banned words, links
python3 scripts/validate.py --offline  # skip the link check
python3 scripts/check_catalog.py       # showcase index for the starter pack
claude plugin validate .               # if Claude Code is installed
```

When proposing a change, include a realistic task that shows why the instruction changes the outcome. Keep the scope narrow and the examples fictional.
