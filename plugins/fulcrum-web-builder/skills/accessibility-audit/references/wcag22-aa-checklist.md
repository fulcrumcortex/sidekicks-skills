# WCAG 2.2 Level A and AA checklist

WCAG 2.2 (W3C Recommendation, October 2023) has 55 Level A and AA success criteria. Compared with 2.1 it adds six at A or AA, marked **New in 2.2**, and removes 4.1.1 Parsing, which is obsolete. Mark each row Pass, Fail, Not applicable or Not tested. "Not applicable" needs a reason (for example "no video on page").

## 1. Perceivable

| SC | Level | How to test | Common failures on marketing sites |
| --- | --- | --- | --- |
| 1.1.1 Non-text Content | A | Inspect every `img`, `svg`, icon button, `input type=image`, CSS background carrying meaning | Logo `alt="logo"`; icon-only buttons without names; informative chart with no text equivalent; decorative image with descriptive alt that adds noise |
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | List media | Silent product video with no text description |
| 1.2.2 Captions (Prerecorded) | A | Play each video with sound | Auto-generated captions never corrected; hero video with speech and no captions |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | Do visuals carry information not spoken? | Demo video showing steps silently |
| 1.2.4 Captions (Live) | AA | Live streams | Webinar embed without live captions |
| 1.2.5 Audio Description (Prerecorded) | AA | As 1.2.3, AA requires audio description | Text alternative only |
| 1.3.1 Info and Relationships | A | Read the DOM: headings, lists, tables, labels, fieldsets, landmarks | Styled `div` headings; label not associated; radio groups without `fieldset`/`legend` |
| 1.3.2 Meaningful Sequence | A | Disable CSS or read with a screen reader | CSS `order` or grid placement contradicting DOM order |
| 1.3.3 Sensory Characteristics | A | Search copy for "on the right", "the green button" | Instructions relying on position or colour only |
| 1.3.4 Orientation | AA | Rotate device | Layout locked to portrait |
| 1.3.5 Identify Input Purpose | AA | Check `autocomplete` on personal-data fields | Missing `autocomplete="email"`, `"tel"`, `"name"`, `"postal-code"` |
| 1.4.1 Use of Color | A | Greyscale screenshot | Links in body text distinguished only by colour (needs 3:1 against text plus another cue on focus/hover, or underline); error state only red |
| 1.4.2 Audio Control | A | Load the page | Autoplaying audio over 3 seconds without a pause control |
| 1.4.3 Contrast (Minimum) | AA | Measure text against its actual background, including over images and gradients | Grey text on light grey; white text on mid-tone brand colour; placeholder text used as label |
| 1.4.4 Resize Text | AA | Browser zoom to 200% | Clipped text in fixed-height containers; viewport-unit-only font sizes |
| 1.4.5 Images of Text | AA | Look for text inside images | Headline baked into the hero image |
| 1.4.10 Reflow | AA | 320 CSS px wide (1280 px at 400% zoom) | Horizontal scroll from fixed-width elements, long URLs, wide tables not in a scroll container |
| 1.4.11 Non-text Contrast | AA | Measure input borders, focus rings, checkbox outlines, meaningful icons, chart lines | Light grey input borders below 3:1; focus ring same colour as button |
| 1.4.12 Text Spacing | AA | Apply line-height 1.5, paragraph spacing 2x, letter 0.12em, word 0.16em (bookmarklet or devtools) | Text cut off in buttons and cards with fixed heights |
| 1.4.13 Content on Hover or Focus | AA | Hover and focus tooltips and menus | Tooltip cannot be dismissed with Escape, or disappears when the pointer moves onto it |

## 2. Operable

| SC | Level | How to test | Common failures |
| --- | --- | --- | --- |
| 2.1.1 Keyboard | A | Complete the task with keyboard only | Click handlers on `div`; custom selects; carousels with mouse-only arrows |
| 2.1.2 No Keyboard Trap | A | Tab into and out of every widget, embed and modal | Third-party embeds (maps, video, chat) that swallow focus |
| 2.1.4 Character Key Shortcuts | A | Press single letters | Single-key shortcuts with no way to turn off or remap |
| 2.2.1 Timing Adjustable | A | Look for timeouts | Session or offer timers that cannot be extended |
| 2.2.2 Pause, Stop, Hide | A | Watch for moving content | Auto-advancing carousel or marquee with no pause |
| 2.3.1 Three Flashes or Below Threshold | A | Review video and animation | Strobe effects in hero video |
| 2.4.1 Bypass Blocks | A | First Tab press | No skip link and no landmarks |
| 2.4.2 Page Titled | A | Check `<title>` | Same title on every page |
| 2.4.3 Focus Order | A | Tab order vs visual order | Modal opens but focus stays behind it; positive `tabindex` |
| 2.4.4 Link Purpose (In Context) | A | List links out of context | "Read more" repeated with no context in the surrounding text or accessible name |
| 2.4.5 Multiple Ways | AA | Site-level: nav plus search or sitemap | Applies to sets of pages: a multi-page site needs two ways (for example navigation plus search or a sitemap page). Pages that are steps in a process are exempt |
| 2.4.6 Headings and Labels | AA | Read headings and labels alone | Vague headings ("Welcome"), labels like "Field 1" |
| 2.4.7 Focus Visible | AA | Tab through | `outline: none` without replacement |
| 2.4.11 Focus Not Obscured (Minimum) **New in 2.2** | AA | Tab with sticky header, cookie banner, chat bubble open | Focused element entirely hidden under a sticky header or bottom bar. Fix with `scroll-padding-top`/`scroll-padding-bottom` or by not overlapping. Partially hidden passes AA; fully hidden fails |
| 2.5.1 Pointer Gestures | A | Find pinch, swipe, multi-point gestures | Map or gallery needing two-finger gestures with no buttons |
| 2.5.2 Pointer Cancellation | A | Press and drag off before release | Actions firing on `mousedown`/`pointerdown` |
| 2.5.3 Label in Name | A | Compare visible label with accessible name | Button shows "Book now" but `aria-label="Submit form"` |
| 2.5.4 Motion Actuation | A | Shake or tilt features | Shake-to-undo with no button alternative |
| 2.5.7 Dragging Movements **New in 2.2** | AA | Any drag interaction | Sliders, sortable lists, before/after image comparers, map panning without click or button alternatives |
| 2.5.8 Target Size (Minimum) **New in 2.2** | AA | Measure targets | Targets under 24 by 24 CSS px that also fail the spacing exception (a 24 px circle centred on each target must not overlap another target or its circle). Exceptions: inline links in text, an equivalent larger control elsewhere, browser-default controls, essential presentation |

## 3. Understandable

| SC | Level | How to test | Common failures |
| --- | --- | --- | --- |
| 3.1.1 Language of Page | A | `<html lang>` | Missing or wrong (`lang="en"` is fine; `en-AU` is more precise) |
| 3.1.2 Language of Parts | AA | Passages in other languages | Te reo, Mandarin or other passages without `lang` |
| 3.2.1 On Focus | A | Tab onto controls | Focus opens a new page or submits |
| 3.2.2 On Input | A | Change selects and radios | Selecting an option navigates without warning |
| 3.2.3 Consistent Navigation | AA | Compare pages | Menu items reorder between pages |
| 3.2.4 Consistent Identification | AA | Same function, same name | Search called "Search", "Find" and a magnifier with different names |
| 3.2.6 Consistent Help **New in 2.2** | A | Help mechanisms across pages | Phone number in header on some pages, footer on others; chat widget present on only some pages in a different place |
| 3.3.1 Error Identification | A | Submit invalid data | Error shown only by red border; generic "Something went wrong" |
| 3.3.2 Labels or Instructions | A | Inspect inputs | Placeholder-only labels; format hints missing (date, phone) |
| 3.3.3 Error Suggestion | AA | Submit invalid data | "Invalid email" with no example of the right format |
| 3.3.4 Error Prevention (Legal, Financial, Data) | AA | Purchases, bookings, legal commitments | No review step or undo before a payment or binding booking |
| 3.3.7 Redundant Entry **New in 2.2** | A | Multi-step forms | Asking for the same address twice in one process without auto-fill or a "same as" option |
| 3.3.8 Accessible Authentication (Minimum) **New in 2.2** | AA | Sign-in, sign-up, password reset | Paste blocked in password or code fields; puzzle CAPTCHA without an alternative; "type the characters you see" with no other method. Allowed: password managers, copy and paste, email links, passkeys, object-recognition CAPTCHA |

## 4. Robust

| SC | Level | How to test | Common failures |
| --- | --- | --- | --- |
| 4.1.1 Parsing | - | Removed in WCAG 2.2 (always satisfied for HTML) | Do not report it |
| 4.1.2 Name, Role, Value | A | Inspect the accessibility tree (DevTools) and listen with a screen reader | Custom toggles without `aria-expanded`; tabs without roles; unnamed `iframe`s |
| 4.1.3 Status Messages | AA | Trigger async messages | "Added", "Sent", search result counts not announced (`role="status"` or `aria-live="polite"`) |

## Quick test set for one landing page (about 20 checks)

1. axe: zero Critical or Serious after manual confirmation.
2. Skip link visible on focus and works.
3. Tab order follows reading order; nothing focusable is invisible.
4. Focus always visible and never fully covered by sticky elements.
5. One `h1`; heading outline makes sense read alone.
6. All images: alt decision justified.
7. Body text and muted text pass 4.5:1; buttons and inputs pass 3:1 boundaries.
8. Links in paragraphs are distinguishable without colour.
9. 320 px: no horizontal scroll.
10. 200% zoom: no clipped text.
11. Text-spacing override: nothing cut off.
12. Targets at least 24 by 24 CSS px or spaced.
13. Form: labels, `autocomplete`, errors in text, linked, announced, focus moved.
14. Success message announced.
15. Accordions and menus announce expanded state and work with Enter and Space.
16. Modal: focus moves in, is contained, Escape closes, focus returns.
17. Carousel or auto-motion: pause control; respects reduced motion.
18. Video: captions present and accurate.
19. Help and contact link in the same place on every page.
20. `<html lang>` and a unique `<title>`.
