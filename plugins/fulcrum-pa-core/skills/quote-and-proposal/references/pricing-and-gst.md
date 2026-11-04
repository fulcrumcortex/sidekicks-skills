# Pricing, options and GST

## Price sources, in order of authority

1. The business's current price list, rate card or product catalogue (check its date).
2. A pricing rule the user states in this conversation ("labour is $X an hour, materials at cost plus 20%").
3. Nothing else. Previous quotes for other customers, competitor prices and "typical market rates" are not price sources. Use `[PRICE NEEDED]` and ask.

If two sources disagree (for example the catalogue and a rate card), quote neither: show both to the user and ask which is current.

## Good, better, best

Use three options when the customer's budget is unknown or there is a natural upgrade. Use one price when the scope is fixed, the customer asked for a single price, or a lower option would be unsafe, non-compliant or likely to fail.

| Rule | Why |
| --- | --- |
| Every option delivers the customer's core requirement | An option that does not solve the problem is a trap, not a choice. |
| Each step up adds a benefit the customer can see (longer warranty, faster delivery, better materials, more hours) | Customers compare benefits, not line items. |
| The middle option is the one the business would recommend, and is labelled as such | Most buyers choose the middle; make it the right one. |
| The gap between options is explained in one line each | "Better adds X, which means Y for you." |
| Maximum three options; no hidden fourth | More options slow decisions. |
| Optional extras are listed separately with their own price | Keeps the core options comparable. |

## GST

| Situation | What to show |
| --- | --- |
| Business registered for GST, customer is a consumer | Prices including GST. The total including GST is the most prominent figure. You may also show the GST component. |
| Business registered, customer is a business | Usually subtotal excluding GST, GST, and total including GST. Always say which basis each figure uses. |
| Business not registered for GST | No GST anywhere. Do not add 10%. A line such as "No GST is included" avoids confusion. |
| Line is GST-free (some health, education, food or export supplies) | Mark the line GST-free only if the user or their accountant confirms it. Default to taxable. |

Arithmetic (GST rate 10%):

- From an ex-GST price: GST = price x 0.10; inc-GST = price x 1.10.
- From an inc-GST price: GST = price / 11; ex-GST = price - GST.
- Round GST to the cent, half up. `scripts/quote_totals.py` rounds per line and sums; keep the same method across the quote.

Worked example: an ex-GST labour line of $382.00 has GST of $38.20 and is $420.20 including GST. An inc-GST price of $616.00 contains GST of $56.00 ($616.00 / 11).

Businesses must register for GST once their turnover reaches the registration threshold. If the user is unsure whether they are registered, ask them to check their ABN record or ask their accountant before the quote goes out.

A quote is not a tax invoice. When the work is invoiced, the tax invoice needs its own required details; that is handled at invoicing.

## Consumers and displayed prices

When a price is shown to a consumer, the Australian Consumer Law expects a single total price that includes GST and any unavoidable charges, shown at least as prominently as any part price. Do not advertise "from" prices in a quote; quote the actual scope.

## Deposits and payment terms

| Item | Default | Notes |
| --- | --- | --- |
| Validity | 30 days | 14 days when material or supplier prices are volatile. |
| Deposit | As the user's policy states | Residential building work has state limits on deposits and written-contract requirements; check before setting one. |
| Payment terms | As the user's policy states (7 or 14 days are common for small jobs) | Must match what will be printed on the invoice. |
| Progress payments | Tied to visible milestones | Each milestone says what is complete when it is billed. |
| Variations | Written, priced and approved before the work | State the rate used to price variations. |
