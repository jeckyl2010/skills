---
name: slidev-presentations
description: Author, review, and fix Slidev presentations — visual inspection, design consistency, frontmatter hygiene, Carbon icons, rewrite vs patch decisions.
version: "1.0.0"
tags: [slidev, presentations, markdown, ux, carbon-icons]
tool_agnostic: true
authors: [Anders Hybertz]
---

# Slidev Presentations

Use when authoring, reviewing, or fixing a Slidev deck — design consistency, icon selection, layout patterns, visual inspection, or structural improvements.

## Project shape

- Single `.md` file with YAML frontmatter + slide content separated by `---`
- `package.json` with `@slidev/cli`, a theme, and optionally `playwright-chromium` for export
- `layouts/` for custom Vue layout components
- `global-bottom.vue` for persistent bottom bar content

## Visual inspection workflow

Before reviewing or after making changes, export to PNG for visual critique:

```bash
# Install playwright if not present
npm i -D playwright-chromium

# Export all slides to PNG
node_modules/.bin/slidev export mds-slides.md --format png --output /tmp/slides-preview
```

Then load key slides with `vision_analyze` — at minimum: title, a representative content slide, and the last slide. Ask specifically: "Visual design critique — layout, typography, color, modern or dated?"

## Design review checklist

- **Header consistency** — every slide should use the same header pattern. Raw markdown `# Title / ## Subtitle` and custom badge+eyebrow headers must not coexist across the deck.
- **Icon semantics** — icons must match the concept of the card, not be reused generics. `carbon-document` is not "delivery". `carbon-rule` is not "operations". See Carbon icons reference below.
- **Color overuse** — if the brand accent appears on badges, eyebrows, border accents, card tints, icons, AND bullet icons simultaneously, it stops being an accent. Audit and thin.
- **Audience navigation** — for decks with 5+ thematic sections, add an overview slide before the first section. Numbered badges + one-line intent per item. This is the audience's map.
- **Typography contrast** — if the deck loads two typefaces (e.g. IBM Plex Sans + Source Serif 4), the serif must be used intentionally and noticeably, not just in one place.
- **Card monotony** — if every card has identical `rounded-2xl border shadow-sm`, the deck has no visual hierarchy. Use radius and shadow to signal level, not as a blanket rule.

## Frontmatter hygiene

- `zoom: 1.0` is the default — remove it, it is noise.
- `zoom: 0.9` on a content slide signals the slide is overloaded. Note it in review.
- Only set `zoom` when you actually need non-default behavior.

## Carbon icon semantics (common cases)

| Concept | Good icon | Avoid |
|---|---|---|
| Delivery / distribution | `carbon-delivery` | `carbon-document` |
| Operations / platform ops | `carbon-settings-adjust` | `carbon-rule` |
| Identity / access | `carbon-user-identification` | `carbon-user` |
| Security / compliance | `carbon-security` | `carbon-warning-filled` |
| Connectivity / networking | `carbon-wifi` | `carbon-network-4` |
| Applications / runtime | `carbon-application` | `carbon-document` |
| Data / integration | `carbon-data-connected` | `carbon-document` |
| Monitoring / observability | `carbon-activity` | `carbon-chart-line` |
| Scope / list | `carbon-list` | `carbon-document` |
| Classification / taxonomy | `carbon-tag` | `carbon-classification` (does not exist) |

All Carbon icons are available via `@iconify/json` which Slidev pulls automatically — no separate install.

## Rewrite vs patch

Prefer a full file rewrite when:
- The same structural change applies to 5+ slides (e.g. all epic headers need updating)
- Multiple independent issues need fixing in the same pass
- The file is < ~600 lines

Prefer targeted patch when:
- Isolated single-slide fixes
- Frontmatter-only changes

Do NOT use patch mode on Slidev `.md` files when the change touches HTML/component blocks — the diff context can be ambiguous and corrupt the slide boundary markers (`---`). Full rewrite is safer.

## Consistent branded header pattern

The pattern used across this deck — apply to every non-title slide for consistency:

```html
<div class="mb-6 flex items-center gap-3">
  <div class="flex h-12 w-12 items-center justify-center rounded-2xl bg-[#BRANDCOLOR] text-white shadow-sm">
    <carbon-ICON class="text-2xl" />
  </div>
  <div>
    <div class="text-xs font-semibold uppercase tracking-[0.2em] text-[#BRANDCOLOR]">Eyebrow Label</div>
    <h1 class="m-0 text-4xl text-slate-950">Slide Title</h1>
  </div>
</div>
```

## Epic / section overview slide pattern

Use before a group of thematic slides to give the audience a map:

```html
<div class="mt-4 grid grid-cols-[auto_1fr] gap-x-5 gap-y-3">
  <div class="flex h-8 w-8 items-center justify-center rounded-xl bg-[#BRANDCOLOR] text-xs font-bold text-white">01</div>
  <div class="flex items-center text-base text-slate-700">
    <span class="font-semibold text-slate-950 mr-2">Section Title</span> — one-line intent
  </div>
  <!-- repeat for each section -->
</div>
```

## CTA / next steps slide

Numbered badges outperform identical checkmark icons on CTA slides. A checkmark reads as "done". Use numbered red badges to signal sequence:

```html
<div class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-[#BRANDCOLOR] text-xs font-bold text-white">1</div>
```

## Design modernisation signals

When a client asks if the deck looks dated, check:
- Is the theme adding a background texture? (seriph theme does — it ages the deck)
- Is border-radius used at a single size everywhere? (visual monotony)
- Is the brand accent color doing more than 3 jobs simultaneously? (overuse)
- Is the serif typeface barely visible? (wasted differentiator)
- Does the overview slide have dead whitespace on one side? (layout weakness)

## Pitfalls

- `playwright-chromium` is not installed by default — `npm i -D playwright-chromium` before first export.
- The seriph theme renders a subtle background texture that reads as dated at full-screen. For a cleaner modern look, override the background in custom CSS or switch to the default theme.
- Carbon icon names are kebab-case in Slidev UnoCSS: `carbon-user-identification`, `carbon-data-connected`. Verify unusual ones render and don't fall back to a box glyph.
- `carbon-classification` does NOT exist — use `carbon-tag` for classification/taxonomy concepts. Always cross-check unfamiliar icon names before committing.
- **Three-column card grids with nested sub-boxes (e.g. "Why it matters" sections) will overflow the slide boundary if you use standard `text-sm` / `p-4` sizing.** Step everything down: `p-3`, `gap-3`, `text-xs` for body, `text-[9px]` for eyebrows, `h-8 w-8` icons, `leading-4/5` line-heights. Export to PNG and verify before delivering.
- Two-column `layout: two-cols` gives equal 50/50 split. For asymmetric splits, use a `layout: default` with a CSS grid (`grid-cols-[1.2fr_0.8fr]` etc.).
- The `figure-side` custom layout uses a `figurePos` prop defaulting to `left` — pass `:figurePos="'right'"` to flip.
