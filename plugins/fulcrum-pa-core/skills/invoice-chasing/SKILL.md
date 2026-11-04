---
name: invoice-chasing
description: Builds an aged-receivables view (current, 1-30, 31-60, 61-90, 90+ days), checks each debt for disputes, unreconciled payments and wrong contacts, then drafts staged follow-up from a friendly nudge through firm reminder, phone call, statement and final notice, payment plan and external options, with tone set by the relationship. Use when the user asks "who owes us money", "chase overdue invoices", "debtor follow-up", "aged receivables", "send payment reminders", "collections" or uploads an aged receivables export from Xero, MYOB or another tool. Nothing is sent or called without approval. Works from any invoice CSV or accounting export; uses Fulcrum CRM invoices when connected.
---

# Chase overdue invoices without damaging the relationship

Produces an aged-receivables table, a checked list of debts that are genuinely ready to chase, and approved reminders or call notes for each debtor at the right stage. The endpoint is a sent, logged follow-up for each approved debtor, and a list of debts on hold with the reason.

## When to use

- The user wants to know who owes money, how much and for how long.
- Regular debtor run (weekly is typical), or one customer's overdue account needs a plan.
- Not for: issuing a new invoice or quote (`quote-and-proposal`); reviewing the pipeline of unsigned deals (`pipeline-review`); a general customer follow-up that is not about payment (`fulcrum-crm-follow-up`); paying the business's own bills.

## What you need

| Input | Where it usually comes from | If missing |
| --- | --- | --- |
| Open invoices with debtor, invoice number, invoice or due date, amount outstanding | Accounting export (aged receivables detail or outstanding invoices report, as CSV), CRM invoice list, spreadsheet | Ask for the export. Do not build ageing from memory or from emails alone. |
| Payment terms | Invoice terms, customer agreement | Use 30 days from invoice date and say so. Use `--eom` for "end of month" terms. |
| Recent payments not yet matched | Bank feed, payment provider, remittance emails | Ask; list the risk that some debts are already paid. |
| Billing contact per debtor | Accounting contact, CRM accounts contact | Flag "no billing contact"; do not send to a project contact without checking. |
| Disputes, complaints, payment arrangements | Inbox, CRM notes, the user | Ask the user to name any before sending. |
| Relationship notes | The user or CRM | Default to the "new or standard customer" tone. |
| Sending account and signatory | The user | Ask once. |

## Procedure

1. **Age the ledger.** Run `python3 scripts/ageing.py export.csv --as-of YYYY-MM-DD --detail`. It skips paid, void and draft rows, puts disputed rows on hold, flags credits and part payments, and suggests a stage from the oldest overdue invoice. Report the bucket totals first; anything over 30% of the total in 61+ days is a cash-flow risk worth saying out loud.
2. **Check before chasing.** For each debtor with a suggested stage of 1 or more, run the pre-chase checks in [references/escalation-ladder.md](references/escalation-ladder.md): dispute or complaint, already paid but unreconciled (search the bank feed, payment provider and inbox for the amount, invoice number and "remittance" over the last five business days), wrong or bounced contact, invoice errors (PO number, entity, GST, terms), credit on account, an agreed payment plan or promised date, and insolvency notices. Any hit moves the debtor to **On hold** with the reason. Do not chase a held debt.
3. **Set the stage and tone.** Start from the suggested stage, then adjust with the relationship rules in [references/escalation-ladder.md](references/escalation-ladder.md): a long-standing customer late for the first time stays one stage softer; a repeat late payer moves one stage faster; government and large corporates get a process-focused message to accounts payable. Never skip the final notice before external options, and never escalate more than one stage per contact.
4. **Respect contact limits.** Leave at least five business days between contacts on the same debt unless the debtor promised a date (then contact the business day after it passes). Phone calls only on weekdays 7.30am to 9pm and weekends 9am to 9pm in the debtor's time zone, never on national public holidays, and no more than three contacts a week or ten a month in total. These follow the ACCC and ASIC debt collection guideline.
5. **Draft the follow-up.** Use [assets/templates.md](assets/templates.md) for the stage. Every message names the business, the invoice numbers, amounts and due dates, how to pay, and one clear ask (pay by a date, or reply with a payment date). Attach or link the invoice or statement. Keep promotions out of reminders. For a call, prepare a call note: amount, invoices, what to ask, what you can offer (payment plan limits the user has set), and how to record the outcome.
6. **Approval gate.** Present a batch table: debtor, contact and channel, stage, amount, the exact message or call note, and the sending account. List held debts separately with reasons. Wait for an explicit yes for the batch; the user may approve some rows and hold others. Final notices and anything mentioning a collection agency or legal action need the user's specific approval for that debtor, and the stated next step must be one the user really intends to take.
7. **Send or call, then verify.** Send through the approved account. Check the sent items (or call history) for each one; after a timeout, check before resending so no one gets the same reminder twice. Log each contact on the customer record with the date, stage and next contact date.
8. **Handle replies.** Promise to pay: record the date, pause the ladder until the next business day after it. Dispute: put on hold, acknowledge within one business day, route to the user. Hardship or a request for time: offer the payment plan template within the limits the user set, and confirm any plan in writing. "Already paid": thank them, ask for the remittance or date and amount, and check before replying again.
9. **Never mark an invoice paid** because a customer said so. Mark it paid only when the payment is matched in the bank feed or payment provider.

## Output

1. Aged-receivables summary table (bucket totals and shares) and the by-debtor table from the script.
2. Action list: debtor, stage, channel, amount, draft or call note, next contact date.
3. On-hold list: debtor, amount, reason, who resolves it.
4. After sending: a log of sent, called, failed and still pending items, kept separate.

## Check before you finish

- [ ] Every chased debt passed the pre-chase checks; held debts have a reason and an owner.
- [ ] Amounts and invoice numbers in each message match the ledger on the day of sending.
- [ ] No debtor received more than one contact for the same stage, and contact limits were respected.
- [ ] Each send is confirmed in sent items or call history and logged on the customer record.
- [ ] No invoice was marked paid without a matched payment.

## Guardrails

- Do not threaten action the user has not decided to take, imply a court judgment or credit listing that cannot happen, or add fees or interest the agreed terms do not allow.
- Do not discuss the debt with anyone other than the debtor or their authorised representative (accounts payable, a financial counsellor, a lawyer). Leave voicemails and SMS that do not reveal amounts to a shared or unknown number.
- If the debtor says they are in financial hardship, unwell, or asks to deal in writing only, follow that and tell the user.
- If a company debtor is in administration or liquidation, or a person is bankrupt, stop all contact and tell the user; the claim goes through the appointed administrator or trustee.
- The debt collection points here are a practical checklist, not legal advice. See [references/escalation-ladder.md](references/escalation-ladder.md) for the full list.

## With Fulcrum

Fulcrum CRM invoices live under **Sales → Invoices** and can be filtered by draft, open, paid, uncollectible and void. An **open** invoice is not proof of payment, and a saved invoice is not proof the customer received it. When an invoice is connected to Stripe, review the provider-backed invoice details and sync status before chasing; if sync failed, inspect the existing provider invoice rather than creating a replacement. **Do not mark an invoice paid to clear a warning** when the payment has not been reconciled; **Void Invoice**, deleting a draft and marking paid have different effects. Log each reminder or call as an activity on the contact's timeline and create a dated task for the next contact. Send reminders from the CRM email composer with a connected mailbox and an email template; after **Send** there is a 30-second **Stop send** window for a last check.

For Xero or MYOB, export the outstanding or aged receivables report at invoice level as CSV and run the script on it; the column names are matched automatically.

## Learn more

- [Invoices and the product catalogue in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/invoices-and-products/)
- [Activities and tasks in Fulcrum CRM](https://fulcrumcortex.github.io/documentation/crm/activities-and-tasks/)
