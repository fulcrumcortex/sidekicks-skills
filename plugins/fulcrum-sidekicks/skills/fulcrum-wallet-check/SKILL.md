---
name: fulcrum-wallet-check
description: "Explain Fulcrum Wallet balance, holds, credit lots and history for the selected account. Use for read-only billing investigation, not purchases or plan changes."
---

# Reconcile a Wallet balance question

Confirm the account or workspace, service, amount and time range in question. Inspect the current balance, held or overdrawn credit, credit lots and relevant history using authorised tools.

Distinguish a top-up, subscription allocation, promotional lot, hold, settled service charge and refund. Use each lot’s displayed expiry and the current checkout or billing source for prices. Do not assume all credit is permanent or that every connected app bills identically.

Reconcile the transaction reference and timing with the connected app's usage where available. A payment redirect is not proof that credit was applied, and a hold is not necessarily the final charge. State missing evidence explicitly.

Do not purchase credit, change a plan, issue a refund or retry a payment as part of this read-only skill. If the user separately authorises one of those actions, use its supported workflow and verify the final transaction before doing anything twice.

Return the reconciled entries, explanation and concrete next diagnostic action. Include references useful to the user but omit payment card data, tokens and unrelated account history.

## Product reference

Use the [current product guide](https://fulcrumcortex.github.io/documentation/fulcrum-mail/) for interface details. Discover the tools available in this environment; the skill itself supplies no credentials or integration.
