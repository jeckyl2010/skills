---
name: comtech-ui-design
description: Design system, visual language, tone, and UI conventions for comtechconsulting.dk — reference before adding any new UI, copy, or page to the site.
version: "2.2.0"
tags: [comtech, ui, design-system, astro, brand]
tool_agnostic: true
authors: [Anders Hybertz]
---

# COM<tech> UI Design Reference

Reference this skill before touching comtechconsulting.dk. Guiding principle: simplicity, cleanliness, consistency. Every inconsistency removed earns trust.

## Brand posture

- One-person senior consultancy. Anders Hybertz is the product.
- Tone: calm, credible, craftsmanship-focused. Danish understatement — serious first, quiet twist welcome if it doesn't undermine credibility.
- No hype, no superlatives, no buzzword stacking.
- Copy is restrained. If a sentence can be cut without losing meaning, cut it.
- "Anders Hybertz" is load-bearing — use it where a visitor needs to know there is a real person. "Contact Anders" beats "Contact".
- Content bar is high: only material that directly serves a client evaluating whether to hire Anders.

## Design tokens (src/styles/global.css)

| Token | Value |
|---|---|
| --bg | #f9f9f8 |
| --surface | #ffffff |
| --surface-2 | #f4f4f5 |
| --border | #e4e4e7 |
| --accent | #5352cc |
| --accent-hover | #4340b0 |
| --accent-text | #7c7bef |
| --accent-dim | rgba(83,82,204,0.08) |
| --text | #111112 |
| --text-2 | #52525b |
| --text-3 | #a1a1aa |
| --radius | 8px base — cards use calc(--radius * 1.5) = 12px |
| --max-w | 1100px |
| --nav-h | 64px |

Dark sections (hero, footer): --dark-bg #0d0d10 / --dark-surface #17171c / --dark-border #2a2a35 / --dark-text #f4f4f5

## Typography

- Body: Inter (400–800), self-hosted woff2. Base 16px, line-height 1.75.
- Mono: JetBrains Mono 600 — only for the `<tech>` wordmark suffix.
- Section labels: small uppercase, letter-spaced, muted (--text-3).

## Motion

- Subtle fade-in on scroll (`.fade-up`) — opacity + translateY only.
- No slides, bounces, staggers, or entrance theatrics.
- Hover: `all 0.15s ease` maximum.

## Layout

- Hero: full-width dark, two-column — headline/CTA left, social proof right. Aurora blobs decorative, aria-hidden.
- Bento grid on home services overview.
- Section label → H2 → body copy is the standard block pattern.
- CTA strip at page bottom (dark, single action).
- Footer: dark, compact — wordmark + CVR left, email right.

## Buttons

Three tiers, all sharing the same `.btn` base — identical height, padding (0.625rem 1.25rem), font-size. Never override these per-button.

1. **btn-primary** — filled accent. One per hero max.
2. **btn-ghost-dark** — transparent, muted border. Secondary on dark sections.
3. **btn-ghost** — transparent, light border. Secondary on light sections.

**Utility modifier: btn-ai-summary** — extends btn-ghost-dark. `opacity: 0.6` at rest, `1` on hover. Signals tertiary without disappearing. Font size must match siblings.

**Hierarchy rule:** demote utility actions via opacity only — never by shrinking font or padding.

**Sizing rule:** when buttons in a group have unequal label lengths, set `min-width` so the shortest doesn't look stubby. Always pair with `text-align: center; justify-content: center`.

**Mobile rule:** stack vertically with `align-items: stretch` on the container — buttons fill equal full width. Do not use `align-items: flex-start`.

## Hero CTA buttons

1. See services (btn-primary) — primary conversion
2. Contact Anders (btn-ghost-dark) — secondary, full name intentional
3. Ask AI (btn-ghost-dark + btn-ai-summary) — utility, demoted via opacity

## Cards

- All cards use `border-radius: calc(var(--radius) * 1.5)` = 12px. No exceptions — consistency is the point.
- Pills (`.tag`, `.bento-tag`) use `border-radius: 999px` — fully rounded is intentional, signals label/category vs container.
- Pills use `display: inline-flex; align-items: center; justify-content: center` for correct text centering.
- When a card has icon above title, wrap them in a header element with `gap: 0.4rem`. Do not tighten the outer card gap — it also compresses body and tag spacing.
- Do not put icon inline with title when titles vary in length — they wrap inconsistently across cards.

## Ask AI feature

- ChatGPT only. URL: `https://chatgpt.com/?q=${encodeURIComponent(prompt)}`
- Opens new tab. Pure anchor tag — no backend, no JS.
- Inline ChatGPT SVG logo (fill="currentColor", 1em × 1em). Label: "Ask AI".
- macOS ChatGPT desktop app intercepts the link — expected OS behaviour, not a bug.

## AI discoverability

- `public/llms.txt` — structured site summary for AI crawlers. Keep current when services or contact details change.
- `public/robots.txt` — allow all, sitemap pointer.
- Per-page meta descriptions: specific and unique on every page.
- Semantic HTML throughout — clean heading hierarchy, no div soup.

## Copy conventions

- English with Danish professional register — direct, credible, understated.
- No em-dashes. Use a comma, full stop, or restructure.
- No superlatives, no filler openers, no US warmth performance ("excited to", "feel free to", "that is fine").
- Active voice. Short sentences. Specifics over vague claims.
- If it doesn't add meaning, remove it.

**Anti-patterns caught in the wild:**
- "feel free to reach out" → write the action: "write" or "send a message"
- "That is fine." as reassurance → cut it, the visitor didn't ask for it
- "available inline below" → redundant, the thing is visually there
- Em-dash in body copy, including data arrays and component props — not just prose

## What does not belong

- Personal GitHub projects
- LinkedIn-appropriate credentials not directly relevant to hiring Anders
- Taglines or subtext that explain what the content above already shows

## Decision process for site changes

Challenge before building. This site should not accumulate features or drift in tone.

1. Load `grill-me` and interview Anders one question at a time.
2. Push back if the idea adds noise, weakens brand, or doesn't serve a client evaluating whether to hire.
3. Only proceed when scope and decision are solid.

Bar: does this directly serve a potential client? "Maybe" or "nice touch" means push back.

## How to run a site review

1. Run `npm run critique` (or `critique:fast` to skip build). This captures 20 screenshots: every page × desktop + mobile × fold + full. The scroll simulation ensures all IntersectionObserver animations fire before capture.
2. Load each screenshot via vision_analyze with a specific critique question referencing the brand.
3. Report as FAIL / ADVISORY / PASS. State which rule each FAIL violates.
4. Apply all fixes in one agreed pass. Rebuild and confirm clean before done.

**Stage, don't ship.** When the user has not explicitly asked for deployment, apply all changes to a local working branch and run `critique:fast` to show rendered screenshots for verification. Only push to `main` after explicit user sign-off. This is the default workflow — not an exception.

See `astro-static-sites` skill for the canonical `critique.js` template and the IntersectionObserver pitfall.

## Known structural issues to check on every review

**Nav z-index / scroll-offset overlap:** The sticky nav overlaps content mid-page across multiple pages. Section anchors do not compensate for `--nav-h` (64px). Check that `scroll-margin-top: var(--nav-h)` is set on all scrollable sections.

**Contact page interactivity:** Email and LinkedIn entries must be real links — `mailto:` and `href` respectively. Plain text is a functional failure on a contact page. Add a visible CTA button ("Send an email →") with the mailto href.

**About page:** Always verify a CTA strip exists below the last content section. Removing it leaves a dead whitespace void before the footer.

**Testimonials page:** Only one card format should be used — the expanded card (italic quote, bold name, role below, "Read full recommendation +" link). Multiple competing formats read as errors. Duplicate testimonials across format variants must be removed.

**Card height consistency:** Two-column card rows need equal heights. Enforce with `align-items: stretch` on the grid container and `height: 100%` on cards if needed. Do not rely on copy length to balance heights naturally.

**Page-lead width:** `.page-lead` max-width is 68ch — not 52ch. Narrower values create an asymmetric gap between the intro paragraph and the full-width layout below it. Also set `margin-bottom: 2rem` so page headers breathe before grid content starts.

**Single testimonial section:** If only one quote is shown, ensure it earns the canvas — strong quote, credible attribution, appropriate label. "CLIENT PERSPECTIVE" (singular) reads oddly; prefer "What clients say" or omit the section label.

**CTA strip visual differentiation:** When a testimonial section and a CTA strip appear on the same light background, they merge into one block. Differentiate with a subtle top border, a tint change, or tighter padding to mark the zone break.
