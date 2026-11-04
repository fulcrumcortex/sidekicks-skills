---
name: fulcrum-crm-data-cleanup
description: "Find likely CRM duplicates and inconsistent fields, propose a reversible cleanup and verify authorised changes. Use before an import or when records need reconciliation."
---

# Review CRM data quality

Confirm the target organisation, record type and cleanup scope. Prefer a limited sample or filtered export to an unrestricted copy of the database. Keep personal data in the authorised workspace.

Compare stable identifiers and activity history. A shared company, office number or generic mailbox does not prove two contacts are the same person. Label uncertain matches for review instead of merging them automatically.

For imports, preserve the original file, inspect headers and field mapping, and rehearse a small sample. Determine whether the operation creates or updates records before repeating it. Use structured fields for dates and controlled categories; do not silently erase conflicting values.

Prepare the proposed surviving values and the effect on ownership, lists, activity and linked deals. Merge, delete or bulk-edit only when that action is authorised and the product supports it. Use the available backup, export or recycle-bin recovery path before destructive changes.

Verify representative changed records and reconcile created, updated, skipped and failed counts. Do not equate an accepted upload with a completed import. Report remaining ambiguous records and preserve an actionable audit trail without publishing private exports.

## Product reference

Use the [current product guide](https://fulcrumcortex.github.io/documentation/crm/) for interface details. Discover the tools available in this environment; the skill itself supplies no credentials or integration.
