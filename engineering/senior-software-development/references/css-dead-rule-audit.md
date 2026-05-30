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
| Inline styles | `style=""` attributes on any element that isn't a dynamic binding — structural concerns belong in named CSS classes |

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

### Dead markup class removal (2025-06 dead-code pass)

Three more dead selectors / orphaned classes found and removed after Content Collections migration:

| File | Type | Finding | Fix |
|---|---|---|---|
| `global.css` | Dead CSS rule | `.bento-full { grid-column: 1 / -1 }` — defined, no element ever carries it | Deleted |
| `global.css` | Dead CSS rule | `.divider { border: none; border-top: 1px solid var(--border); margin: 4rem 0; }` — no `<hr>` or element uses it | Deleted |
| `testimonials.astro` | Dead CSS in media query | `.signal-grid` inside `@media (max-width: 980px)` — the grid it styled was removed by the Content Collections refactor; the selector survived alongside live `.featured-grid` | Removed the selector from the comma list |
| `contact.astro` | Dead markup class | `.contact-linkedin` on the LinkedIn `<a>` — modifier with zero CSS rules; link already fully styled by `.contact-primary-link` | Removed from class list |
| `about.astro` | Dead markup class | `.repo-grid-single-source` on the strengths `<div>` — modifier added for future differentiation, never given any styles | Removed from class list |

**Pattern: orphaned selectors inside media query comma lists.** When a layout section is removed, its CSS may survive inside a multi-selector `@media` block:

```css
@media (max-width: 980px) {
  .signal-grid,        /* ← dead — the grid is gone */
  .featured-grid {     /* ← live */
    grid-template-columns: 1fr;
  }
}
```

The block still compiles cleanly and lints pass — the dead selector is invisible noise. Include comma-separated selectors in the dead-CSS sweep.

**Pattern: anticipatory modifier classes.** A class like `.repo-grid-single-source` or `.contact-linkedin` is often added during development for future differentiation that never arrived. No visual effect, no CSS — pure dead weight. Detection: grep the class name across global.css and all local `<style>` blocks. Zero matches = delete from markup.

### Inline style elimination (2025-05 third pass)

After the above two passes, a grep for `style="` across all page files revealed 15 remaining inline attributes — all structural concerns that belonged in CSS.

**Patterns found and the right fix for each:**

| File | Inline style | Resolution |
|---|---|---|
| `about.astro` | `<h2 style="margin-bottom: 0.75rem;">` × 5 different sections | Page-local semantic classes `.section-h2`, `.section-h2-tight`, `.section-h2-snug` |
| `about.astro` | `<p style="max-width: 52ch; margin-bottom: 2rem;">` × 3 | Page-local `.section-sub`, `.section-sub-narrow`, `.section-sub-wide` |
| `about.astro` | `<div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">` | Global utility `.btn-row` added to `global.css` |
| `about.astro` | Multiple tag `<span>` with per-iteration `font-size`/`padding` | Global utility `.tag-md` added to `global.css` |
| `about.astro` | `<p style="margin-top: 1rem;">` on second body paragraph | Page-local `.about-body-spaced` |
| `about.astro` | `{a.detail && <p style="margin-top: 0.375rem;">` | Page-local `.award-detail` |
| `index.astro` | `<div style="margin-top: 1.5rem;">` (testimonial CTA wrapper) | Page-local `.hero-testimonial-cta` |
| `services.astro` | `<section ... style="padding-top: 4rem; padding-bottom: 4rem;">` | Page-local `.svc-principles-section` |

**Decision rule for each inline style found:**
- Used on >1 page, or a layout concern shared across element types → global utility (`.btn-row`, `.tag-md`)
- Used only on this page, but not a one-off — applies consistently to a recurring element within the page → page-local semantic class
- True one-off (e.g. a single element with a unique value that will never recur) → leave as-is, mark with a comment if non-obvious

**After this pass:** zero inline `style=""` attributes remain on any page. Every spacing, sizing, and color decision is expressed in CSS with a named class.

**Detection command:**
```bash
grep -rn 'style="' src/pages/ src/layouts/
```
Run this as the final check after any consolidation pass. Any hit that is not a dynamic binding (i.e. not `style={...}`) is a candidate for extraction.

## Dead class detection script (Astro/static sites)

Use this pattern for a full codebase sweep — not just style blocks, but also markup classes with no corresponding CSS.

```python
import re

files = {
    "global.css": open("src/styles/global.css").read(),
    "Layout.astro": open("src/layouts/Layout.astro").read(),
    # add all pages/components
}

def extract_defined_classes(css_text):
    return set(re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]+)', css_text))

def extract_used_classes(html_text):
    used = set()
    for m in re.findall(r'class=["\']([^"\']+)["\']', html_text):
        used.update(m.split())
    for m in re.findall(r"class[=:{][^>]+", html_text):
        used.update(re.findall(r'["\']([a-zA-Z][a-zA-Z0-9_-]+)["\']', m))
    return used

# For each .astro file, extract only the <style> block for CSS parsing
def get_css(fname, content):
    if fname.endswith(".astro"):
        m = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        return m.group(1) if m else ""
    return content

all_defined = set()
for fname, content in files.items():
    all_defined.update(extract_defined_classes(get_css(fname, content)))

all_used = set()
for content in files.values():
    all_used.update(extract_used_classes(content))

# JS-managed classes — not dead even though absent from static HTML
js_managed = {"js", "fade-up", "visible", "open", "page"}
# False positives from font @font-face URLs
noise = {"woff2", "w3", "org"}

dead_css = all_defined - all_used - js_managed - noise
dead_markup = all_used - all_defined - js_managed - noise

print("Dead CSS rules (defined, never used in markup):")
for c in sorted(dead_css):
    print(f"  .{c}")

print("\nDead markup classes (used in HTML, no CSS rule):")
for c in sorted(dead_markup):
    print(f"  .{c}")
```

**False positive filter:**
- `js`, `visible`, `open`, `fade-up`, `page` — set dynamically by JavaScript; not dead.
- Font URL fragments (`woff2`, `w3`, `org`) — picked up from `@font-face src:` strings; not class names.
- Structural/semantic containers (`.about-intro-left`, `.hero-content`) — present in markup, no CSS intentional; acceptable as long as it is a conscious choice.

**Astro-specific false positives — filter these before acting:**

1. **`class:list` dynamic classes not captured by static regex.** Astro's conditional class syntax:
   ```astro
   <div class:list={['award-item', { 'award-item--featured': a.data.featured }]}>
   ```
   The regex `class=[\"\\']([^\"\\']+)[\"\\']` does not match `class:list={...}` — so dynamic
   classes appear absent from `all_used`. They look dead in CSS but are live. Supplement the
   detection script to also parse `class:list` occurrences:
   ```python
   for fname, content in files.items():
       for m in re.findall(r"class:list=\{[^}]+\}", content):
           all_used.update(re.findall(r"'([a-zA-Z][a-zA-Z0-9_-]+)'", m))
   ```

2. **`role=` attribute values.** Some regex variants using `class` as a substring match
   `role="navigation"` etc. The string `navigation` then appears as a dead class. Always
   anchor to `class=` (not just the substring `class`) and verify matches are actual `class=`
   attributes before acting.

3. **`class:list` boolean literal keys.** If the regex accidentally matches inside the JS object
   literal body, the tokens `true` and `false` appear as class names. Add them to the noise set:
   ```python
   noise = {"woff2", "w3", "org", "true", "false"}
   ```

**Workflow implication:** after running the script, always classify every finding manually —
dead CSS (remove the rule), dead markup class (remove from markup), or false positive (document
and skip). Do not patch before the full classification pass is complete.

**What is genuinely dead:**
- A class defined in CSS that never appears in any `class=` attribute → delete the rule.
- A class in a `class=` attribute that has zero matching CSS rules → either a dead modifier (remove from markup) or a structural container (leave, document why).

## CSS quality audit — Project Wallace

URL: `https://www.projectwallace.com/css-code-quality?url=<your-domain>&prettify=1`

Run this after any significant CSS consolidation pass. It surfaces four metrics: Maintainability, Complexity, Performance, Selector Uniqueness.

### How to interpret the findings

| Metric / Finding | Typical cause | Act? |
|---|---|---|
| **Large ruleset (26+ declarations)** | `:root {}` with design tokens | No — that's where they belong |
| **High declaration duplication (40–55%)** | Token-driven stylesheet — `display: flex`, `gap`, `color` repeat across rules | No — expected at this scale |
| **Embedded content (small bytes)** | Inline SVG for a decorative asset (noise texture, icon) | No — saves one HTTP request |
| **Complex selectors (attribute + :nth-child)** | Hamburger/nav-toggle CSS animation | No — correct pattern, no simpler alternative without JS |
| **`!important` > 0** | See `!important` audit below — often redundant | Yes — verify each one |
| **Very high duplication (60%+)** | Real duplication, not token reuse | Yes — audit with the shared-class pattern |

A score of 90+ across all four dimensions is the target for a token-driven static marketing site. Scores below that warrant investigation before dismissal.

### `!important` audit

For every `!important` declaration found, verify it is actually fighting a competing rule:

1. Identify what property it is setting (e.g. `margin-top: 0 !important`).
2. Check whether a universal reset (`*, ::before, ::after { margin-top: 0 }`) already sets it to the same value.
3. Check whether any other rule at the same or lower specificity sets it to a different value.
4. If nothing is being fought — the `!important` is redundant. Remove it.

A universal reset (`* { margin-top: 0; margin-bottom: 0; }`) covers most spacing defaults. A defensive `!important` added before the reset existed is a common leftover. The browser computed value confirms it — `window.getComputedStyle(el).marginTop` should be `0px` with or without the `!important` if the reset is in place.

```bash
# Quick grep: find all !important declarations
grep -n '!important' src/styles/global.css src/pages/*.astro src/layouts/*.astro
```

Each hit needs a comment explaining what it's overriding, or it should be removed.

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
