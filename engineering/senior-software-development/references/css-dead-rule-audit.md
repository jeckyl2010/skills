# CSS Dead Rule Audit — technique

Use when: any CSS/style review task, consolidation pass, or "inconsistent styling" complaint.

## Why incremental reading fails

Reading files one at a time while patching misses:
- Classes renamed in markup but not CSS (orphaned selector)
- Sections removed from HTML whose styles stayed
- `:hover` rules permanently shadowed by a more-specific sibling (e.g. `.card:hover` beaten by `.svc-card:hover` on every element carrying both classes)
- Duplicate chrome split across global and page-local blocks
- Element selectors (`blockquote {}`, `a {}`) applying visual chrome to elements that never opted in — forcing consumers to explicitly reset those properties

The user has explicitly called out that a "detailed review" still missed numerous elements. The lesson: cards are not the only element type to audit. Every element type — buttons, blockquotes, labels, inline styles, icon containers, markup class lists — must be in scope from the start.

## Full audit scope — cover ALL of these

| Category | What to look for |
|---|---|
| Cards | Duplicate chrome (bg, border, radius, shadow) vs global `.card` base |
| Buttons | Dead variants defined in global but used nowhere |
| Blockquotes / pull-quotes | Element selector styles applying globally; consumers overriding instead of opting in |
| Labels / caps | Repeated font-size/weight/tracking/transform across contextual rules vs shared base class |
| Icon containers | Hardcoded `border-radius: 8px` instead of `var(--radius)` |
| Inline styles | Any `style=""` on an element that belongs in CSS — no-op defaults, dark-section overrides, max-width constraints |
| Markup classes | Classes on elements that have zero CSS rules (dead markup classes) |
| Contextual overrides | `.dark-section .thing` rules missing from global, being substituted with inline styles |
| Hover rules | `:hover` rules on selectors always beaten by a sibling rule with higher specificity |

## Correct sequence

1. **Read every relevant file in full first** — global CSS + every page/component that has a local style block. Do not start patching until this is complete.
2. **Build a complete finding list across all categories above** — not just cards. Map: selector → where defined → used in markup → superseded by another rule.
3. **For each CSS rule, verify the selector fires**: search the template/HTML for at least one element carrying that class or matching that element selector. If none, it is dead.
4. **For each inline style, decide**: does this belong in CSS? If it is a structural rule (dark-section color, max-width, default background), move it to CSS.
5. **Check specificity traps**: if two rules target overlapping class sets, confirm which wins. A rule always beaten by another is functionally dead.
6. **Only then patch** — file by file, build after each file, confirm clean.

## Comtech-site patterns found

### Cards (2025-05)

| File | Dead rule | Reason |
|---|---|---|
| `testimonials.astro` | `.signal-grid`, `.signal-card`, `.signal-label`, `.signal-quote`, `.signal-source` | Section removed from markup |
| `about.astro` | `.repo-card:hover` | Every `.repo-card` also carries `.repo-card-static`; `.repo-card-static:hover` defined later wins; rule never fires |
| `services.astro` | `background`, `border`, `border-radius`, `box-shadow`, `transition`, `:hover` on `.svc-card` | Duplicate of global `.card` chrome; fixed by adding `card` base class to markup |
| `testimonials.astro` | `.featured-card` chrome | Same as above; fixed by adding `card` base class |

### Beyond cards (2025-05 second pass)

| File | Issue | Fix |
|---|---|---|
| `global.css` | `.btn-accent-outline` defined, used nowhere | Deleted |
| `global.css` | `blockquote {}` element selector applied card chrome to all blockquotes | Renamed to `.blockquote-card`; opted in at usage sites; overrides in testimonials removed |
| `global.css` | `.award-item .award-year` duplicated `.section-label` typography verbatim | Stripped to differing values only; `section-label` class added to markup |
| `global.css` | `.dark-section .testimonial-author` missing | Was being substituted with inline `style="color: var(--dark-text-2)"` on two elements |
| `index.astro` | `class="home-cta-strip"` on section with zero CSS rules | Dead markup class; removed |
| `index.astro` | `style="background: var(--bg)"` on section | No-op inline style (page default); removed |
| `index.astro` | `style="color: var(--dark-text-2)"` on `.testimonial-author` and inner `<strong>` | Structural dark-section rule; moved to global CSS |
| `index.astro` | `style="max-width: 68ch"` on blockquote | Layout constraint; moved to local CSS rule `.index-pull-quote` |
| `services.astro` | `.svc-icon { border-radius: 8px }` | Hardcoded; replaced with `var(--radius)` |
| `contact.astro` | `.step-icon { border-radius: 8px }` | Same |

## Shared-class pattern (consolidation signal)

When multiple elements (`.card`, `.bento-card`, `.svc-card`, `.featured-card`, etc.) carry identical chrome declarations:
1. Add the shared base class (`card`) to the markup element.
2. Strip the duplicated properties from the local rule, keeping only genuinely unique values (padding, grid placement, gap, etc.).
3. Hover and transition come from one canonical rule.

## Element selector pollution pattern

When a global CSS file styles a raw HTML element (`blockquote`, `a`, `table`, etc.) with visual chrome that only some instances should have:
1. Rename the rule to a class (e.g. `blockquote {}` → `.blockquote-card {}`).
2. Add the class to elements that should have the chrome.
3. Remove the explicit resets from elements that were fighting it off.

This is always better than the alternative — consumers should opt in to visual treatments, not opt out.
