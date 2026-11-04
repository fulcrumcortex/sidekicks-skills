# Catalogue of slop patterns and fixes

Each entry: how to spot it, why it reads as generated or templated, and what to do instead. A pattern is not always wrong; it becomes slop when it is the default rather than a decision.

## Colour and surface

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Purple-to-blue (or violet-to-pink) gradient | Hero backgrounds, buttons, headings with `from-purple`/`to-indigo` | The default of generated SaaS sites since 2023; signals "AI product" regardless of what the business does | Derive the palette from the brand and the business. Near-neutral canvas, one accent used only for actions and key data. If a gradient stays, it belongs to the brand and is used in one place. |
| Gradient text on headings | `bg-clip-text text-transparent` | Decoration standing in for a typographic idea; often fails contrast at the light end | Solid heading colour; get emphasis from size, weight, a typeface change or a single underlined word. |
| Glassmorphism everywhere | `backdrop-blur` with `bg-white/10` on every card | Flattens hierarchy (everything floats), costs GPU time, unreadable over busy backgrounds | Solid surfaces with a clear elevation system; keep blur for one overlay (a sticky header over content) if at all. |
| Neon glows and blurred orbs | `blur-3xl` circles behind content, glowing borders | Fills empty space instead of content; looks identical across sites | Remove. Use real imagery, a texture derived from the product (a grid, a map, a schematic) or plain space. |
| Dark mode as the only mode with purple accents | Black canvas, violet highlights | The "AI startup" uniform | Choose light or dark for a reason (product context, photography); support both via tokens. |
| Too many tints | Ten pastel badge colours | No colour means anything | Colour encodes meaning (status, action) or brand. Everything else is neutral. |

## Typography

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Timid scale | Largest heading `text-4xl`, headings and body too close in size | No hierarchy, no voice | A display size 2.5 to 4 times body on desktop (fluid with `clamp`), tight tracking on large sizes, generous line length control. Fewer sizes, bigger jumps. |
| Default typeface without a decision | One common sans for everything at regular and bold | Fine for interfaces; invisible on a marketing page | One strong typographic idea: a display face with character for headings (serif, grotesk with distinctive shapes, condensed, or mono for technical brands) with a calm text face. Two families maximum. |
| Everything bold or everything medium | Weight used as the only emphasis | Monotone | Contrast in weight and size together; body at regular, headings at one chosen weight. |
| Title Case Every Heading | Marketing headings in title case | Reads like a template's placeholder | Sentence case, unless the brand uses title case on purpose. |
| Ragged, orphaned headings | One word alone on the last line | Unconsidered | `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs; check at each breakpoint. |

## Layout

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Centred everything | Every section centred: heading, paragraph, buttons | Static, symmetrical, no reading path | Left-aligned text on a grid; centre only short, ceremonial moments (a final CTA). Use asymmetric splits (7/5, 8/4) and let one element break the grid. |
| Identical three-card grids | Icon, title, two lines of text, three times, repeated for features, benefits and values | The most recognisable template block | Vary by content: a numbered process list, one large feature with two small, a table, an annotated screenshot, a bento grid with unequal cells. If three cards remain, make their content unequal and real. |
| Section stack with equal spacing | Every section the same height and padding | No rhythm, no emphasis | Vary density: a dense proof strip, a spacious statement, a full-bleed image. Spacing follows importance. |
| Hero with floating 3D object | Abstract shape or isometric illustration beside the headline | Says nothing about the product | Show the product in use, the result, the people, or let type carry the hero. |
| Logo cloud of fake or unlicensed logos | "Trusted by" with generic marks | Dishonest and obvious | Only real, permitted logos; otherwise a single specific proof line. |

## Imagery and icons

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Emoji as icons | Emoji in headings, list bullets, feature cards | Inconsistent rendering across platforms, unprofessional, noisy for screen readers | One icon set with consistent stroke and size, or no icons; numbers or short labels often work better. |
| Sparkle, rocket and lightning icons | Lucide `Sparkles`, `Rocket`, `Zap` on AI features | The visual cliche of AI marketing | Icons that depict the actual object or action, or none. |
| Stock illustration libraries | Flat people with oversized limbs, isometric offices | Seen on thousands of sites | Real photography (commission or use the client's), product screenshots, diagrams drawn for this product. |
| Generated imagery with tells | Waxy skin, impossible hands, unreadable signage | Erodes trust, especially for local businesses | Real photos of the business. If generated images remain, they are abstract and checked closely. |
| Fake product UI | Generic dashboard mock with random charts | Visitors cannot tell what the product does | Real screenshots, cropped to the relevant part, annotated. |

## Copy

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Hype verbs | Unlock, unleash, elevate, empower, supercharge, transform, revolutionise | Interchangeable; signals that the writer did not know the specifics | The specific outcome with a number or a mechanism. |
| Smoothness words | Seamless, effortless, frictionless, streamline | Universal claims nobody believes | Name the step removed or the integration. |
| "It's not just X, it's Y" cadence and triplets | Rhythmic three-part lists of abstract nouns | A recognisable generated cadence | One concrete sentence. |
| Placeholder content left in | Lorem ipsum, John Doe, Acme, "Feature 1" | Unfinished | Real content or a visible TODO that blocks release. |
| Labels as headings | "Features", "Why choose us", "Our values" | Says nothing | Headings that make a claim the section proves. |

## Motion

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| Fade-up on every section | Every block slides up 20 px on scroll | Motion without meaning; delays content; can hurt LCP | Animate only what explains: order of steps, state changes, the product in action. Content is visible without JavaScript. |
| Hover lift on every card | `hover:scale-105`, `hover:-translate-y-1` with shadow growth | Suggests clickability where there is none | Hover feedback only on interactive elements, subtle (colour, underline, 1 to 2 px), with `(hover: hover)` guarding. |
| `transition-all` | On many elements | Animates layout properties and causes jank | Transition named properties (`transition-colors`, `transition-transform`) with token durations. |
| Bounce, pulse, ping as decoration | Arrows bouncing, dots pulsing | Distracting; fails reduced-motion expectations | Reserve for real status (a live indicator). Respect `prefers-reduced-motion`. |
| Parallax and scroll-jacking | Smooth-scroll libraries overriding native scroll | Disorienting, accessibility and performance cost | Native scroll; a single scroll-linked moment if it tells the product story. |

## Components and details

| Pattern | Spot it | Why it reads as template | Fix |
| --- | --- | --- | --- |
| One radius plus shadow on everything | `rounded-xl shadow-lg` on cards, buttons, inputs, images | Soft, toy-like, no hierarchy | Radius by role (controls small, cards medium, images none or matching); most surfaces without shadow; elevation only for overlays. |
| Pill badges above every heading | "New", "AI-powered", "Beta" chips | Eyebrow inflation | One eyebrow style used sparingly, as text, not a pill. |
| Two equal CTAs | "Get started" and "Learn more" both prominent | No decision made | One primary per view; secondary as a text link. |
| Default focus and form styles | Browser outline removed, grey inputs | Craft stops at the visible layer | Designed focus rings (2 px, offset, accent), clear input borders that pass 3:1, designed error states. |

## Craft details (do after the big moves)

- Optical alignment: icons and large type aligned to the text edge, not the box edge.
- Typographic correctness: curly quotes and apostrophes, en dashes in ranges (9–5), non-breaking space between number and unit (`15&nbsp;min`), tabular figures (`tabular-nums`) in tables and prices.
- Consistent icon size and stroke; icons centred optically with text.
- Hairlines at 1 px with enough contrast to see, consistent colour.
- Images share one treatment (crop ratios, colour grading, corner radius).
- Line length 60 to 80 characters for body text.
- Hover, focus, active, disabled and loading states designed for every interactive element.
- Favicon, Open Graph image and 404 page designed, not defaulted.
- Numbers and proof formatted consistently (4.8/5, 312 reviews, source named).
- Empty space used deliberately: generous around the primary message, tighter in dense proof areas.

## Directions to choose from (examples, not presets)

| Direction | Typography | Palette | Layout | Fits |
| --- | --- | --- | --- | --- |
| Editorial | High-contrast serif display, quiet sans text, large numerals | Paper-tone neutrals, ink, one accent | Asymmetric columns, pull quotes, generous margins | Professional services, hospitality, publishers |
| Swiss and exact | Grotesk throughout, strong size contrast, tight tracking | Near-monochrome, one signal colour | Strict grid, left-aligned, dense information | B2B software, finance, engineering |
| Technical | Grotesk with monospaced data and labels | Dark or light neutrals, one status-like accent | Schematics, annotated product UI, tables | Developer tools, infrastructure, data |
| Warm and crafted | Humanist sans or soft serif | Earthy, photographic | Full-bleed photography, texture, handwritten or stamped details sparingly | Trades, food, local retail, health |
| Type-led bold | Condensed or extended display at very large sizes | Two colours with strong contrast | Oversized headlines, minimal imagery | Events, campaigns, creative agencies |

Pick by the business and its buyers; then let the client's brand assets set the actual values.
