---
name: comtech-ui-design
description: Design system, visual language, tone, and UI conventions for comtechconsulting.dk — reference before adding any new UI, copy, or page to the site.
version: "2.8.0"
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

**Hierarchy rule:** demote utility actions via opacity only — never by shrinking font or padding.

**Sizing rule:** when buttons in a group have unequal label lengths, set `min-width` so the shortest doesn't look stubby. Always pair with `text-align: center; justify-content: center`.

**Mobile rule:** stack vertically with `align-items: stretch` on the container — buttons fill equal full width. Do not use `align-items: flex-start`.

## Hero CTA buttons

1. See services (btn-primary) — primary conversion
2. Contact Anders (btn-ghost-dark) — secondary, full name intentional

Three CTAs is one too many. A third hero CTA dilutes focus and competes with conversion. If a utility action is genuinely useful, move it lower on the page (e.g. bottom of About) and give it minimal visual weight — a secondary link, not a button.

## Ask AI feature (disabled)

Implementation: ChatGPT URL with injected structured prompt covering who Anders is, services, industries, credentials, contact. Opens new tab. Pure anchor, no backend.

Feature is sound — the prompt engineering is good, the utility is real. Disabled because the hero is the wrong placement. On a trust-led site, a CTA that sends the visitor to another product in another voice loses narrative control at the highest-stakes moment. The visitor gets their first real impression of COM<tech> through ChatGPT's output, not yours.

Rule: any feature that routes the user off-platform during initial evaluation competes with the site's authority. Keep it if it has a home lower on the page. Disable it rather than leave it in the hero.

- If re-enabled: macOS ChatGPT desktop app intercepts the link — expected OS behaviour, not a bug.

## AI discoverability

- `public/llms.txt` — structured site summary for AI crawlers. Keep current when services or contact details change.
- `public/robots.txt` — allow all, sitemap pointer.
- Per-page meta descriptions: specific and unique on every page.
- Semantic HTML throughout — clean heading hierarchy, no div soup.

## Section separation

One rule, applied consistently everywhere: `1px solid var(--border)` (`#e4e4e7`). This is already the value on nav, footer, `.cta-strip`, and `.section-alt`.

- Use `.section-alt` for alternating background sections — it applies the border-top automatically.
- Use `.cta-strip` border-top for the page-bottom CTA strip — already set in global.css.
- Never add inline `style="border-top: ..."` on individual sections — put it in a class.
- Never add inline `style="background: ..."` to vary section backgrounds — use `.section-alt` or a named modifier class.
- Never create bespoke border widths (2px, 3px) for specific areas. Visual hierarchy comes from layout and spacing, not from varying border weights.
- The hairline is intentionally low-contrast. It reads as a zone marker at normal viewing distance. If it's invisible at screenshot scale, that's correct — it's not a bold divider.

If two adjacent sections feel merged, the fix is not a colour or border change. It is usually better copy structure, stronger heading, or accepting that the sections belong together.

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
- "No account managers, no intake steps" — stating what's obviously implied by being a one-person shop. The visitor already knows. Saying it signals insecurity, not confidence. Cut it.

**Contact page channel hierarchy:**
Email is the primary channel — give it full card treatment. LinkedIn belongs in the same card, same layout class, not orphaned as a plain text link below. An orphaned "Also on LinkedIn" reads as an afterthought. Keeping both in the card structure gives LinkedIn appropriate context while email still reads first.

## Testimonials — org diversity rule

Home page deliberately surfaces three org voices: KPMG, Novo Nordisk, N3O. This is intentional — it signals breadth implicitly without claiming it. Do not consolidate to fewer orgs or swap quotes without raising it with Anders first. The Janus Tøth (Novo Nordisk) quote leads the featured section on the testimonials page — keep it there.

## Full-cycle engagement framing

Anders prefers to be present from the first architectural decision through to production and value delivery — not parachute in, produce a document, and leave. This is a genuine differentiator from project-to-project advisory work and should be expressed on the about page.

Correct framing (from about.astro): "The preference is to be present from the first architectural decision through to production — and to see value delivered, not just handed over."

- "Not just handed over" carries the weight implicitly — the reader infers what the alternative is
- Do not state this defensively ("unlike other consultants who...") or colloquially ("not smart in a hurry and gone" works in conversation, not on the site)
- Place in the working style paragraph of the about intro, as a natural concluding sentence — not as a standalone callout

## Web presence as regulatory evidence (Danish Skat)

Danish tax authority examines one-person companies for signs of disguised employment. A professional web presence is direct evidence of genuine self-employment:
- Actively marketing to the general public, not just one client
- Carrying commercial risk
- Having an independent professional identity outside any engagement

This informs content priorities:
- Testimonials from multiple named clients across different organisations and sectors → primary evidence of multiple customers
- The court appointment → third-party institutional recognition of independent expert status
- Long tenures (5y Novo, 5y Codan/RSA, 5y SDC) read as client satisfaction and retention, not hidden employment — especially when Novo ended in a mass restructuring, not a performance issue
- A second case study from a different sector, or a second long-term client testimonial, is not just marketing — it is documentation

Do not reduce client diversity on the home page or testimonials page for editorial tidiness. Three distinct org voices on the home page (KPMG, Novo, N3O) serve this purpose directly.

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

1. Run `npm run critique` (or `critique:fast` to skip build). This captures 20 screenshots: every page × desktop + mobile × fold + full. The scroll simulation (20 steps, 120ms each, pause at bottom, 900ms settle before capture) ensures all IntersectionObserver animations fire. If deep sections appear blank, the scroll step count or delay may need increasing.
2. Load each screenshot via vision_analyze with a specific critique question referencing the brand.
3. Report as FAIL / ADVISORY / PASS. State which rule each FAIL violates.
4. Apply all fixes in one agreed pass. Rebuild and confirm clean before done.

**Stage, don't ship.** When the user has not explicitly asked for deployment, apply all changes to a local working branch and run `critique:fast` to show rendered screenshots for verification. Only push to `main` after explicit user sign-off. This is the default workflow — not an exception.

See `astro-static-sites` skill for the canonical `critique.js` template and the IntersectionObserver pitfall.

See `references/nav-mobile-pitfalls.md` for known mobile nav rendering issues and their fixes.

## Mobile nav active state bleed (known pitfall)

The `.nav-links a[aria-current="page"]` rule applies a background fill with `border-radius`. In the mobile dropdown, `<a>` elements are inline by default — their background box is not constrained to the row height, and with `gap: 0.25rem` the rounded fill visually bleeds into the adjacent item, making it look like two items are selected.

Fix (both lines required):
```css
.nav-links li { display: block; }
.nav-links a { display: block; padding: 0.875rem 1rem; }
```
`display: block` on both `<li>` and `<a>` fully contains the background to the row. Vertical padding of `0.875rem` gives the border-radius enough clearance from the item below. Do not go below `0.75rem` — the bleed reappears.

## Known structural issues to check on every review

**Mobile nav active-state bleed:** On mobile, the `aria-current="page"` background (`--accent-dim`) bleeds into the adjacent menu item because `.nav-links a` is not `display: block` inside the flex column. Fix: add `display: block` to both `.nav-links li` and `.nav-links a` in the mobile media query, and set vertical padding to at least `0.875rem` so the border-radius can't visually bridge to the next item. Without `display: block`, the inline/flex anchor's background box is unconstrained and the rounded rect merges with the row below.

**Nav z-index / scroll-offset overlap:** The sticky nav overlaps content mid-page across multiple pages. Section anchors do not compensate for `--nav-h` (64px). Check that `scroll-margin-top: var(--nav-h)` is set on all scrollable sections.

**Contact page interactivity:** Email and LinkedIn entries must be real links — `mailto:` and `href` respectively. Plain text is a functional failure on a contact page. Add a visible CTA button ("Send an email →") with the mailto href.

**About page:** Always verify a CTA strip exists below the last content section. Removing it leaves a dead whitespace void before the footer.

**Testimonials page:** Only one card format should be used — the expanded card (italic quote, bold name, role below, "Read full recommendation +" link). Multiple competing formats read as errors. Duplicate testimonials across format variants must be removed.

**Card height consistency:** Two-column card rows need equal heights. Enforce with `align-items: stretch` on the grid container and `height: 100%` on cards if needed. Do not rely on copy length to balance heights naturally.

**Page-lead width:** `.page-lead` max-width is 68ch — not 52ch. Narrower values create an asymmetric gap between the intro paragraph and the full-width layout below it. Also set `margin-bottom: 2rem` so page headers breathe before grid content starts.

**Single testimonial section:** If only one quote is shown, ensure it earns the canvas — strong quote, credible attribution, appropriate label. "CLIENT PERSPECTIVE" (singular) reads oddly; prefer "What clients say" or omit the section label.

**CTA strip visual differentiation:** When a testimonial section and a CTA strip share a light background they can appear to merge. Do not attempt to fix this with colour — neither `--surface-2` (too similar to `--bg`), `--accent-dim` (8% opacity, invisible at scale), nor a dark background (creates a heavy dark mass before the dark footer) solves it cleanly. The right answer: accept natural flow. A testimonial followed by a CTA is one thought — social proof into action. They are allowed to read as a continuation. Consistent `1px solid var(--border)` hairlines via `.section-alt` and `.cta-strip` are sufficient. Do not add bespoke separators or background overrides for this transition.

**Testimonials page format:** Two formats are intentional — featured cards (expanded: italic quote + attribution) for primary testimonials, list rows for secondary ones. This reads as hierarchy, not inconsistency. Do not collapse to one format.
