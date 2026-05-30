# CSS Dead Rule Audit — technique

Use when: any CSS/style review task, consolidation pass, or "inconsistent styling" complaint.

## Why incremental reading fails

Reading files one at a time while patching misses:
- Classes renamed in markup but not CSS (orphaned selector)
- Sections removed from HTML whose styles stayed
- `:hover` rules permanently shadowed by a more-specific sibling (e.g. `.card:hover` beaten by `.svc-card:hover` on every element carrying both classes)
- Duplicate chrome split across global and page-local blocks

## Correct sequence

1. **Read every relevant file in full first** — global CSS + every page/component that has a local style block.
2. **Build a finding list before touching anything** — map: selector → where it is defined → does it appear in markup → is it superseded by a more specific rule.
3. **For each CSS rule, verify the selector fires**: search the template/HTML for at least one element carrying that class or matching that element selector. If none exists, it is dead.
4. **Check specificity traps**: if two rules target overlapping class sets, confirm which wins. A rule that is always beaten by another is functionally dead even if its selector matches.
5. **Only then patch** — file by file, build after each file, confirm clean.

## Comtech-site patterns found (2025-05)

| File | Dead rule | Reason |
|---|---|---|
| `testimonials.astro` | `.signal-grid`, `.signal-card`, `.signal-label`, `.signal-quote`, `.signal-source` | Section removed from markup; no element in HTML |
| `about.astro` | `.repo-card:hover` | Every `.repo-card` also carries `.repo-card-static`; `.repo-card-static:hover` is defined later and wins; the `:hover` rule never fired |
| `services.astro` | `background`, `border`, `border-radius`, `box-shadow`, `transition`, `:hover` on `.svc-card` | Duplicate of global `.card` chrome; svc-card was not inheriting `.card` base class |

## Shared-class pattern (consolidation signal)

When multiple elements (`.card`, `.bento-card`, `.svc-card`, `.featured-card`, etc.) carry identical chrome declarations, the correct fix is:
1. Add the shared base class (`card`) to the markup element.
2. Strip the duplicated properties from the local rule, keeping only genuinely unique values (padding, grid placement, gradient background, etc.).
3. Hover and transition then come from one canonical rule.
