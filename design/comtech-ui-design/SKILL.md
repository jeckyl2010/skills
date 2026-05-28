---
name: comtech-ui-design
description: Design system, visual language, tone, and UI conventions for comtechconsulting.dk — reference before adding any new UI, copy, or page to the site.
version: "1.6.0"
tags: [comtech, ui, design-system, astro, brand]
tool_agnostic: true
authors: [Anders Hybertz]
---

# COM<tech> UI Design Reference

Reference this skill before adding any new UI, page section, copy, or component to comtechconsulting.dk. It captures the live design system and the decisions behind it.

## Brand posture

- One-person senior consultancy. Anders Hybertz is the product.
- Tone: calm, credible, craftsmanship-focused. Danish understatement — serious first, a quiet twist is welcome if it doesn't undermine credibility.
- No hype, no superlatives, no buzzword stacking.
- Copy is restrained. If a sentence can be cut without losing meaning, cut it.
- The name "Anders Hybertz" is load-bearing — use it where a visitor needs to know there is a real person on the other end. "Contact Anders" is better than "Contact".
- Content bar is high: only material that directly serves a client evaluating whether to hire Anders.

## Design tokens (src/styles/global.css)

### Light (default)
| Token | Value |
|---|---|
| --bg | #f9f9f8 |
| --surface | #ffffff |
| --surface-2 | #f4f4f5 |
| --border | #e4e4e7 |
| --border-subtle | #f0f0ef |
| --accent | #5352cc |
| --accent-hover | #4340b0 |
| --accent-text | #7c7bef |
| --accent-dim | rgba(83,82,204,0.08) |
| --text | #111112 |
| --text-2 | #52525b |
| --text-3 | #a1a1aa |
| --radius | 8px — base unit only; cards use calc(--radius * 1.5) = 12px |
| --max-w | 1100px |
| --nav-h | 64px |

### Dark sections (hero, footer)
| Token | Value |
|---|---|
| --dark-bg | #0d0d10 |
| --dark-surface | #17171c |
| --dark-border | #2a2a35 |
| --dark-text | #f4f4f5 |
| --dark-text-2 | #a1a1aa |
| --dark-text-3 | #7c7c7c |

## Typography

- Body: Inter (400/500/600/700/800), self-hosted woff2
- Mono: JetBrains Mono 600 — used only for the `<tech>` wordmark suffix
- Base: 16px, line-height 1.75
- Headings are bold, large, white on dark sections; near-black on light
- Section labels: small uppercase, letter-spaced, muted (--text-3 or --dark-text-3)

## Motion and animation

- Subtle fade-in on scroll (`.fade-up` utility) — opacity + translateY, short duration
- No slides, bounces, staggers, or entrance theatrics
- Hover transitions: `all 0.15s ease` maximum

## Sections and layout

- Hero: full-width dark section (`--dark-bg`), two-column — headline/CTA left, social proof right
- Aurora background blobs in hero — decorative, aria-hidden
- Bento grid for services overview on home page
- Section label → H2 → body copy is the standard content block pattern
- CTA strip at bottom of home page (dark section, single action)
- Footer: dark, compact — wordmark + CVR left, email right

## Buttons

Three tiers, all consistent height and padding (0.625rem 1.25rem):

1. **btn-primary** — filled accent (#5352cc), white text. One per hero max.
2. **btn-ghost-dark** — transparent, muted border, light text. Secondary action on dark sections.
3. **btn-ghost** — transparent, light border, --text-2. Secondary on light sections.

### Utility modifier: btn-ai-summary
Used on the Ask AI hero button. Extends btn-ghost-dark with:
- `opacity: 0.6` at rest, `opacity: 1` on hover
- `display: inline-flex; align-items: center; gap: 0.4em` for icon + text
- Font size must match sibling buttons — do not downsize
- Purpose: signals tertiary/utility without disappearing

## Hero CTA button pattern

Three buttons in the hero:
1. See services (btn-primary) — primary conversion
2. Contact Anders (btn-ghost-dark) — secondary conversion, full name intentional
3. Ask AI (btn-ghost-dark + btn-ai-summary) — utility, visually demoted via opacity

Rule: utility or off-site actions are demoted visually (opacity), never by shrinking font or padding.

## Button sizing and alignment rules

These are baseline — apply to any button group on the site:

- All buttons in a group share the same height and font-size via the `.btn` base class. Never override these per-button.
- When buttons in a row have unequal label lengths, set `min-width` on the group so the shortest label doesn't look stubby. `9rem` works for the current hero trio.
- Whenever `min-width` or `width` is set on a button, also set `text-align: center` and `justify-content: center` — otherwise text drifts left inside the padded box.
- On mobile (column stack), use `align-items: stretch` on the container so all buttons fill the same width. Pair with `text-align: center; justify-content: center` on the buttons.

```css
/* Desktop: consistent minimum width, centered content */
.hero-actions .btn {
  min-width: 9rem;
  text-align: center;
  justify-content: center;
}

/* Mobile: full width, centered content */
@media (max-width: 480px) {
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-actions .btn { text-align: center; justify-content: center; }
}
```

## Mobile button layout

On narrow viewports (max-width: 480px), hero action buttons must stack vertically at equal full width:

```css
@media (max-width: 480px) {
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-actions .btn { text-align: center; justify-content: center; }
}
```

Do not use `align-items: flex-start` — it lets buttons take their natural (unequal) widths and looks broken. Tested and confirmed — reducing font-size on a sibling button makes it read as an afterthought rather than a quiet option. Opacity alone is sufficient and correct.

## Ask AI feature

- Single button in the hero, ChatGPT only (ChatGPT and Google AI Mode both support query-string prompt injection)
- Opens in a new tab (`target="_blank" rel="noopener noreferrer"`)
- URL pattern: `https://chatgpt.com/?q=${encodeURIComponent(prompt)}`
- Prompt asks for structured output with explicit headings: Who Anders Hybertz is / Services / Industries / Recognition / Contact
- ChatGPT desktop app on macOS will intercept the link and open the app instead of a browser tab — expected OS behaviour, not a bug
- No backend, no clipboard workaround, no JS required — pure anchor tag
- Inline ChatGPT SVG logo left of text (fill="currentColor", 1em × 1em)
- Button label: "Ask AI" — verb-led, honest about the handoff to an external tool

## AI discoverability

- `public/llms.txt` — structured plain-text site summary for AI crawlers and retrieval. Keep it current when services, recognition, or contact details change.
- `public/robots.txt` — allow all + sitemap pointer
- Per-page meta descriptions: specific, not generic. Each page has a unique description written to serve both search snippets and AI retrieval context.
- Semantic HTML throughout — clean heading hierarchy, no div soup

## Copy and language conventions

- Language is English, written with a Danish professional register — direct, credible, understated
- No em-dashes (—) in copy. Use a comma, a full stop, or restructure the sentence
- No superlatives: not "highly experienced", not "world-class", not "passionate about"
- No filler openers: not "At COM<tech>...", not "We believe...", not "I am committed to..."
- No US-style warmth performance: no "excited to", no "thrilled", no "amazing"
- Sentences earn their place. If it doesn't add meaning, remove it
- Active voice. Short sentences preferred over compound ones
- Numbers and specifics over vague claims — "three decades" beats "extensive experience"
- The brand voice is calm confidence, not self-promotion

## Decision-making process for site changes

Any proposed change to the site — new section, new copy, new feature, visual change — must be challenged before implementation. This is not a site that should accumulate features or drift in tone.

Before building anything:
1. Load the `grill-me` skill and use it — interview Anders one question at a time to stress-test the idea
2. Give honest feedback if the idea weakens the brand, adds noise, or doesn't serve a client evaluating whether to hire Anders
3. Only proceed once the decision is solid and the scope is clear

The bar: does this change directly serve a potential client? If the answer is "maybe" or "it's a nice touch", push back.

## Copy anti-patterns found in the wild

These passed initial review but were caught on audit — apply the conventions checklist to all copy including data arrays and component props, not just prose blocks:

- "feel free to reach out" — US softener, removes directness. Replace with the action: "write", "send a message", or restructure
- "That is fine." as reassurance opener — patronising, assumes anxiety the visitor did not express. Cut it
- "available inline below" — redundant when the thing is visually below. Cut the whole clause
- Em-dash (—) in running body copy — use a comma or full stop instead

## What does not belong on this site

- Personal GitHub projects
- Advertorial content
- LinkedIn-appropriate credentials that are not directly relevant to hiring Anders
- Those belong on LinkedIn (Featured section or experience entries)

## How to run a site review against this skill

1. Read every page in `src/pages/*.astro` in full — not just the meta or copy, but all inline data arrays, bento cards, CTA copy, and component props. Copy violations appear in data arrays and props as often as in prose blocks.
2. Take a visual screenshot of the hero at desktop and mobile viewport before filing findings.
3. Deliver findings as a structured report: FAIL (must fix), ADVISORY (worth flagging), PASS. Be explicit about which copy rule each FAIL violates.
4. Apply all fixes in a single pass after the report is agreed. Do not apply incrementally without confirmation.
5. Rebuild and confirm clean before marking done.
