# Heuristics rubric, friction count and checklists

## Nielsen's ten heuristics, adapted for modern web

| # | Heuristic | Probing questions | Typical web failures and fixes |
| --- | --- | --- | --- |
| 1 | Visibility of system status | Does every action get feedback within about 100 ms? Does the user know where they are in a multi-step flow and what is still loading? | Button gives no pressed or pending state, so users double-submit: show "Sending..." and disable. Steps without a progress indicator: add "Step 2 of 3". Silent background saves: show "Saved" briefly. |
| 2 | Match with the real world | Are labels in the user's words, not internal or technical terms? Do units, dates and currency follow local conventions? | "Instance", "entity", "submit ticket" for customers: use their words. US date formats on an Australian site: use DD/MM/YYYY or "5 Nov 2026"; prices in AUD with GST. |
| 3 | User control and freedom | Can users go back, undo, cancel or edit without losing work? | Back button loses form data: persist state. Destructive actions with no undo: offer undo for 5 to 10 seconds instead of a confirmation dialog where possible. Modal with no close button or Escape. |
| 4 | Consistency and standards | Do the same things look and behave the same across the product and match platform conventions? | Two button styles for the same priority; links styled as buttons and buttons as links; a logo that does not go home; custom scrollbars or form controls that behave unexpectedly. |
| 5 | Error prevention | Does the design stop errors before they happen? | Free-text date fields: use a date picker or constrained input. Allowing booking of unavailable times then rejecting: show only available slots. Confirm only irreversible, high-impact actions, and say what will happen. |
| 6 | Recognition rather than recall | Must the user remember information from one screen to use on another? | Order summary hidden at payment: keep it visible. Icons without labels for infrequent actions: add labels. Search with no recent or suggested queries. |
| 7 | Flexibility and efficiency | Can frequent users go faster without confusing new users? | No saved details for returning customers; no keyboard shortcuts in a dense tool; no bulk actions in tables; no deep links to filtered views. |
| 8 | Aesthetic and minimalist design | Does every element earn its place relative to the task? | Three competing CTAs; decorative content pushing the form below the fold; walls of text where a table would do; badges and banners stacked above the content. |
| 9 | Help users recognise, diagnose and recover from errors | Do error messages say what happened, why, and how to fix it, in plain language, next to the problem? | "Error 422" or "Something went wrong": explain and offer the next step. Errors only at the top of a long form: show inline and summarise. Clearing valid fields after an error. |
| 10 | Help and documentation | Is help available at the point of need, without leaving the task? | Help only in a separate centre: add inline hints, "What's this?" disclosures and a visible contact route. Consistent placement of help across pages (also WCAG 3.2.6). |

## Friction count method

For one task, from start to success, count:

| Measure | How to count | Notes |
| --- | --- | --- |
| Screens / steps | Each page or modal the user must pass | Merging steps is not always better; count decisions too |
| Decisions | Each choice the user must make (including "which button?") | The strongest predictor of hesitation |
| Fields | Every input, including optional ones the user must evaluate | Optional fields still cost attention |
| Taps or clicks | Minimum interactions on the happy path | Include opening pickers and dismissing banners |
| Waits | Loads or processing over about 1 second | Note spinners with no progress information |
| Context switches | Leaving the flow: email verification, another tab, a phone call, finding a document | Usually the biggest drop-off points |
| Memory load | Information the user must carry between screens | Reference numbers, prices, times |
| Interruptions | Cookie banners, pop-ups, chat prompts during the task | Count each one |

Present as before and after columns. A good redesign usually removes decisions and context switches first, then fields.

## State checklist

- [ ] Empty (first use, no results, cleared filters): explains what goes here and offers the first action.
- [ ] Loading: skeletons matching the final layout for content; inline spinners for actions; nothing for under about 300 ms.
- [ ] Partial: some data failed or is still loading; the rest is usable.
- [ ] Error: network, validation, permission, not found, timeout, payment declined. Each has wording and a recovery action.
- [ ] Success: confirms what happened, what happens next and when; offers the logical next action.
- [ ] Edge content: very long names, zero and very large numbers, missing images, right-to-left or non-Latin names in user content.
- [ ] Returning user: remembered choices, resumed progress.
- [ ] Offline or slow network on mobile.

## Form UX checklist

- [ ] Only the fields the next step needs; optional fields marked "(optional)" rather than required fields marked with asterisks only.
- [ ] One column on mobile; related short fields (postcode and state) may share a row on desktop.
- [ ] Visible labels above fields; placeholders only for examples.
- [ ] Correct input types, `autocomplete` and `inputmode`; Australian formats (mobile `04xx xxx xxx`, postcode 4 digits, state select).
- [ ] Validation on blur or on submit, not on every keystroke; never clear valid input.
- [ ] Errors next to the field, in words that explain the fix; a summary on submit for long forms.
- [ ] Defaults that match the most common choice, when a default is safe.
- [ ] The button label states the outcome; the button stays in the same place across steps.
- [ ] After submit: clear confirmation, and a receipt by email or SMS when money, bookings or personal data are involved.

## Microcopy checklist

- [ ] Buttons are verbs naming the outcome ("Confirm booking"), not "OK" or "Submit".
- [ ] Destructive actions name the object ("Delete invoice INV-0042"), and the safe option is the easier one.
- [ ] Error messages: what happened, why (if known), what to do. No blame ("You entered an invalid...").
- [ ] Empty states: one sentence of explanation and one action.
- [ ] Consistent terms: one word per concept across the product.
- [ ] Tone fits the moment: plain and calm for errors and money; lighter only where nothing is at stake.

## Hierarchy tests

- **Squint test:** blur the screen; the primary action and key message remain identifiable.
- **Five-second test:** show the screen briefly; can a person say what it is for and what to do?
- **Heading-only read:** the headings alone tell the story of the page.
- **Thumb zone:** on mobile, the primary action sits where a thumb reaches it without scrolling back up.
