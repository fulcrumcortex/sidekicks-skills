# Skill conventions for this repository

Summary of `CONTRIBUTING.md` at the repository root. Read that file when it is available; it wins if the two differ.

## Layout

```text
plugins/<plugin-name>/
  .claude-plugin/plugin.json
  skills/<skill-name>/
    SKILL.md            required: frontmatter and procedure
    references/*.md     optional: detail loaded only when needed
    assets/*            optional: templates the skill fills in (Markdown, CSV, JSON)
    scripts/*.py        optional: deterministic helpers, Python standard library only
```

- SKILL.md links to every reference file it uses, with a line saying when to read it. References link one level deep.
- Scripts run with `python3 script.py --help`, read from files or stdin, write to stdout and make no network calls. Test them with sample input.

## SKILL.md sections, in order

1. Frontmatter: `name`, `description` only.
2. Outcome-first title and two or three sentences: the outcome, who it is for, the endpoint.
3. `## When to use`, including `Not for:` with the better skill named.
4. `## What you need`: a table of input, usual source, and what to do if missing.
5. `## Procedure`: numbered steps with decision rules; **Approval gate** steps for outward actions.
6. `## Output`: the exact deliverable shape, pointing to assets.
7. `## Check before you finish`: a checklist of evidence.
8. `## Guardrails`: privacy, compliance, things never to invent.
9. `## With Fulcrum` (optional): only documented features, with docs links.
10. `## Learn more`: 1 to 3 links that return HTTP 200.

## Rules

- Works without Fulcrum.
- Outward actions need confirmation; after an uncertain result, check sent items or history before retrying.
- Australian compliance as checklists that end with "This is a practical checklist, not legal advice."
- Never claim that any Fulcrum product washes numbers against the Do Not Call Register.
- The CRM is only called "Fulcrum CRM". No prices; link to the pricing page instead.
- Fictional examples only: `example.com` addresses and numbers written as `0400 000 000`.
- Australian English, no emojis, no hype words.

## Private local skills (Fulcrum Code)

- Location: a Markdown file in `~/.fulcrum/skills/`.
- The loader supports a name, description and body, so keep one self-contained file: fold short references into the body and keep long material in a document the skill points to.
- Start a new session after changing the file, then check `/skills`.
- The same rules about secrets and customer details apply.
