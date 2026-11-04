---
name: fulcrum-code-change
description: "Investigate and implement a bounded software change in Fulcrum Code, preserving project conventions and validating the requested behaviour. Use for coding tasks in an existing project."
---

# Make a reviewable code change

Read the project's applicable instructions and inspect the working tree before editing. Preserve unrelated changes. Identify the actual trigger and expected behaviour; reproduce a bug where practical and inspect the affected call paths.

For a change with meaningful uncertainty, propose a concise plan or use Plan mode before Build. Keep a small reversible change in the existing architecture and package manager. Inspect dependency or runtime documentation when the API is uncertain; do not invent a function or command.

Use available file, search, code-intelligence and shell tools. Review any command with effects outside the repository against the user's authorised scope. A coding request does not automatically authorise publishing, messaging or changing a hosted environment.

Run the checks that exercise the behaviour being changed. Inspect the diff for unrelated changes, missing error paths and accidental private data. If checks fail, distinguish an implementation defect from an environment failure and resolve recoverable causes.

Return the changed behaviour, relevant files, actual validation and any material limitation. If a release was requested, use the established project release procedure and record the live evidence; a local build alone does not establish deployment.

## Product reference

Use the [current product guide](https://fulcrumcortex.github.io/documentation/code/) for interface details. Discover the tools available in this environment; the skill itself supplies no credentials or integration.
