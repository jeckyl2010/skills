---
name: astro-static-sites
description: Build, review, and extend Astro static sites — config, integrations, SEO, deployment to GitHub Pages.
version: "1.10.0"
tags: [astro, static-site, github-pages, seo, deployment, css]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
---

# Astro static sites

Use when working on an Astro project: reviewing, extending, debugging, or setting up common integrations like sitemap, OG tags, and GitHub Pages deployment.

## Typical project shape

- `src/layouts/Layout.astro` — shared page shell (head, nav, footer). All SEO meta goes here.
- `src/pages/*.astro` — route-based pages. Pages own their content; the layout owns the shell.
- `src/styles/global.css` — design tokens and shared components.
- `public/` — static assets copied verbatim; CNAME lives here for GitHub Pages custom domains.
- `astro.config.mjs` — must set `site:` for OG URLs, canonical links, and sitemap to resolve correctly.
- `.github/workflows/deploy.yaml` — build + upload-pages-artifact + deploy-pages pattern.

## Resource hints (Layout.astro)

For any third-party font or asset host, pair dns-prefetch with preconnect. The dns-prefetch acts as a fallback for browsers without preconnect support and costs nothing:

```html
<link rel="dns-prefetch" href="//fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin />
```

The `crossorigin` attribute is required on preconnect for any CORS resource (fonts, cross-origin scripts, cross-origin API calls). Without it, the browser performs the preconnect but then opens a second connection when the resource actually fires — defeating the purpose entirely. This fails silently; no console error, no warning.

Order: place dns-prefetch before preconnect. Place both before the font stylesheet `<link>`.

## SEO baseline (Layout.astro)

Every Layout.astro should carry:

1. `<meta name="description">` — already standard
2. `<link rel="canonical">` — derive from `new URL(Astro.url.pathname, Astro.site)`
3. Open Graph: `og:type`, `og:url`, `og:title`, `og:description`, `og:image`, `og:locale`, `og:site_name`
4. Twitter/X Card: `twitter:card` (summary_large_image), `twitter:title`, `twitter:description`, `twitter:image`
5. `ogImage` prop on Layout with a sensible default (e.g. `/og-default.png`); individual pages can override
6. `<link rel="icon" type="image/svg+xml" href="/favicon.svg" />` — place before font preconnects. Text-based favicons (`<text>` element in SVG) collapse unreadably at 16px tab size; use drawn SVG polyline or path geometry instead.

See `templates/layout-head.astro` for a ready-to-copy head block.

## Sitemap

Install: `npm install @astrojs/sitemap`

Wire into config:
```js
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://example.com',
  integrations: [sitemap()],
});
```

Outputs `sitemap-index.xml` and `sitemap-0.xml` into `dist/` on every build. No further config needed for a simple static site. Never commit these files — they are regenerated automatically and belong only in `dist/`.

## astro.config.mjs baseline

```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yourdomain.com',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
});
```

`trailingSlash: 'always'` keeps URLs consistent with GitHub Pages behaviour and avoids redirect chains.

## GitHub Pages deployment pattern

```yaml
permissions:
  contents: read
  id-token: write
  pages: write

jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: npm }
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with: { path: ./dist }
  deploy:
    needs: build
    environment: { name: github-pages, url: '${{ steps.deployment.outputs.page_url }}' }
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

`concurrency.cancel-in-progress: false` on the pages group prevents a mid-flight deploy from being cancelled by a fast follow-up push.

Node.js 24 Actions runner: to suppress the Node 20 deprecation warning from the Actions runner itself, add this to both `build` and `deploy` jobs:

```yaml
env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true
```

Both jobs need it independently — the runner machinery is per-job, not inherited from a top-level env block. This is an official GitHub opt-in.

## Common review signals

- Missing `site:` in astro.config.mjs → OG URLs and sitemap will be broken or absent
- Page-local `<style>` blocks that duplicate patterns already in global.css → maintenance split
- Inline `style=""` attributes used more than once → belong in classes
- After any CSS cleanup pass, run `grep -rn 'style="' src/pages/ src/layouts/` — any hit that is not a dynamic binding (`style={...}`) is a candidate for extraction. Target state: zero inline `style=""` attributes. Every spacing, size, and color decision should live in a named CSS class. Decision rule: >1 page or shared layout concern → global utility; single page recurring element → page-local semantic class; true one-off with a non-obvious value → keep but add a comment.
- No OG/Twitter meta → unfurled links on LinkedIn/Slack show nothing
- Dead CSS in global.css from superseded layouts → run the detection pattern below
- Hardcoded color values in page-local `<style>` blocks — scan for `rgba(`, `#[0-9a-fA-F]` and replace with CSS custom properties
- Class names that survive a redesign but describe the old context — e.g. `.repo-name` repurposed for service area card titles after GitHub section was removed. The class still renders, so it won't appear dead, but it carries wrong semantics and can mislead font/style audits. When auditing, check class names against what they actually render, not just whether they're referenced.
- Hugo migration artifacts left in repo → see pitfalls section

## CSS consolidation — card chrome pattern

Astro sites accumulate duplicate card chrome across page-local `<style>` blocks. The typical set: `.card`, `.bento-card`, `.strength-item`, `.award-item`, `.svc-card`, `.featured-card` — all sharing the same `background: var(--surface); border: 1px solid var(--border); border-radius: ...; padding: ...; box-shadow: ...; transition: ...`. Changing hover shadow or border-radius means finding six definitions.

**Fix:** define a shared selector rule in `global.css` for the classes that are always identical:

```css
.card,
.bento-card,
.strength-item,
.award-item {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: calc(var(--radius) * 1.5);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
.card:hover,
.bento-card:hover,
.strength-item:hover,
.award-item:hover {
  box-shadow: var(--shadow);
  border-color: #d4d4d8;
}
```

Page-local classes that live inside Astro's scoped `<style>` blocks **cannot** participate in global selectors. Two approaches depending on whether the element is conceptually a card:

**Option A — element IS a card:** add the global `card` class directly to the markup element alongside the page-local class. Strip background/border/radius/shadow/transition from the local `<style>`. The local class then holds only differential layout (padding overrides, gap, flex direction, etc.).

```astro
<!-- before -->
<div class="repo-card repo-card-static">

<!-- after — local style block shrinks to layout-only -->
<div class="card repo-card repo-card-static">
```

**Option B — element is NOT a card (e.g. a wrapper with `overflow: hidden`):** keep chrome local, but use the design token (`calc(var(--radius) * 1.5)`) — never hardcode `12px` or any value that duplicates a token.

Prefer Option A whenever the element and the shared `.card` class are semantically equivalent — it reduces local CSS and keeps token usage consistent automatically.

**Rule: never hardcode `border-radius: 12px` (or any value that is already a design token).** A raw px value survives a token rename; the token does not.

Hardcoded radius hides in container/clip wrappers too — not just card-shaped elements. Selectors like `.contact-links { overflow: hidden; border-radius: 12px }` or `.modal-inner { border-radius: 8px }` are easy to miss in a card-focused audit. Extend the audit scan to any selector containing `overflow: hidden` or `border-radius`:

**Quick dead CSS audit before and after consolidation:**

```bash
# For each class name you're about to remove from a page-local block:
grep -r 'class-name' src/ | grep -v 'global.css'
# If no match in markup → safe to remove or centralize
```

## CSS consolidation — label/caps pattern

Uppercase label styles (`font-size: 0.6875rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase`) accumulate across page-local `<style>` blocks with invisible drift — typically in `letter-spacing` (0.08em vs 0.1em) or `font-weight` (600 vs 700). These render nearly identically but are not the same expression.

**Fix:** define two base utility classes in `global.css`:

```css
.label-caps {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.label-caps-muted {
  font-size: 0.6875rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-3);
}
```

Add the base class to the markup element alongside the existing page-local class:

```astro
<span class="contact-link-label label-caps-muted">Email</span>
<p class="t-category label-caps-muted">{t.category}</p>
<p class="contact-process-label label-caps">How it usually starts</p>
```

Reduce the page-local rule to override-only declarations — just `color`, `margin-bottom`, `min-width`, or whatever genuinely differs. Strip all declarations that are now covered by the base class.

Align any related global rules (e.g. `.section-label`, `.award-item .award-year`) to use the same canonical values — weight 700, tracking 0.1em, size 0.6875rem — to keep `section-label` consistent with the utility classes.

**Pitfall:** drift hides in `letter-spacing` and `font-weight`. `0.08em` vs `0.1em` and `600` vs `700` are invisible at a glance but inconsistent in output. Always check these two properties when auditing label-like classes.

**Pitfall:** search for CSS class definitions that are never used in markup before and after the refactor. A class like `.signal-label` may be defined in a `<style>` block but not present on any element — delete it rather than consolidating it.

```bash
# Detect dead CSS classes in page-local style blocks
grep -n "class=" src/pages/testimonials.astro | grep -oP 'class="[^"]+"' | \
  grep -oP '"[^"]+"' | tr ' ' '\n' | sort -u
# Then cross-check each class name against the style block definitions
```

## Dead CSS detection

When reviewing global.css, extract class names and check which ones are actually referenced in src/:

```bash
# For a candidate class name:
grep -r 'class-name' /path/to/src/ 2>/dev/null | grep -v 'global.css'
# No output = dead.
```

Common dead CSS groups after a redesign:
- Old service layout: `.service-entry`, `.service-left`, `.service-num`, `.service-name`, `.service-body`, `.service-tags`
- Old contact layout: `.contact-grid`, `.contact-item`, `.contact-label`, `.contact-value`
- Old page intro: `.page-intro`

Also check for undeclared classes — classes used in pages but absent from global.css and any local `<style>` block.

## Page transitions and scroll animations

### Page fade (CSS only)

```css
@keyframes page-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
::view-transition-old(root) { animation: 150ms ease-out both page-fade-in reverse; }
::view-transition-new(root) { animation: 200ms ease-out both page-fade-in; }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) { animation: none; }
}
```

150ms out / 200ms in. No JS needed for the page fade — Astro's `<ViewTransitions />` handles the lifecycle.

### Scroll-triggered fade-up (IntersectionObserver)

Add to the `astro:page-load` handler in Layout.astro:

```ts
function initFadeUp() {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const observer = new IntersectionObserver(
    (entries) => entries.forEach(entry => {
      if (entry.isIntersecting) {
        (entry.target as HTMLElement).classList.add('visible');
        observer.unobserve(entry.target);
      }
    }),
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  );
  document.querySelectorAll('section').forEach(el => {
    if (el.classList.contains('hero')) {
      el.classList.add('fade-up', 'visible'); // already in viewport — skip animation
    } else {
      el.classList.add('fade-up');
      observer.observe(el);
    }
  });
}
```

CSS (gate behind `.js` class — see pitfalls):

```css
@keyframes fade-up {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.js .fade-up          { opacity: 0; }
.js .fade-up.visible  { animation: fade-up 420ms cubic-bezier(0.22, 1, 0.36, 1) both; }
```

Opacity-only. 420ms, natural ease-out. Single pass — never re-triggers on re-entry. Hero excluded (already visible on load).

**No Y-axis translate.** Even a small `translateY(18px)` violates the motion policy for this site (calm, no entrance theatrics) and can cause layout jank on mobile during scroll. If the name `fade-up` is already in use and removing the translate feels like a rename — leave the class name, change only the CSS.

### Animation tone

Keep animation imperceptible to a distracted eye — craft, not spectacle. No slides, stagger cascades, bounce, or spring overshoot. If someone notices the animation before the content, dial it back.

## Hugo-to-Astro migration pitfalls

Check for leftover artifacts that Astro never uses:
- `/static/` directory — Hugo's asset folder; Astro uses `/public/`
- `.hugo_build.lock` — Hugo lock file
- `hugo_stats.json` — Hugo build stats
- `config.toml` or `config.yaml` at project root — Hugo site config

None of these break Astro builds (silently ignored), but they confuse future contributors. Safe to delete if nothing in `src/` references `static/`.

## Featured card in an auto-fit grid

When one card in an `auto-fit minmax()` grid has significantly more content than its peers, use `grid-column: 1 / -1` to span full width. Keep the inner layout identical to sibling cards (stacked, no inner grid) — a two-column inner layout (e.g. year left / content right) breaks visual consistency with the other cards and looks odd.

```css
.award-item--featured {
  grid-column: 1 / -1;
  /* no inner grid — use the same stacked layout as sibling cards */
}
```

Apply the modifier class conditionally in Astro:

```astro
<div class={`award-item${a.featured ? ' award-item--featured' : ''}`}>
  <div class="award-year">{a.year}</div>
  <div class="award-content">
    <h4>{a.title}</h4>
    <p>{a.issuer}</p>
    {a.detail && <p>{a.detail}</p>}
  </div>
</div>
```

Mark the entry with `featured: true` in the data array. This pattern is useful for any list where one item carries significantly more content — recognition sections, service cards, case studies.

Do not add a `max-width` to the inner content div — the card's own padding and border already frame the content. A `max-width` just creates awkward empty space on the right inside a bordered card.

## Resource hints

For any third-party font or CDN host in the `<head>`, always pair dns-prefetch with preconnect, and always add `crossorigin` to the preconnect for CORS resources (fonts, stylesheets). Without `crossorigin`, the browser opens a second connection when the actual font request fires — the preconnect does nothing.

```html
<link rel="dns-prefetch" href="//fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin />
```

Decision rules for a small static marketing site:
- `preconnect` — critical third-party origins you know will be hit on every page (fonts, CDN)
- `dns-prefetch` — fallback alongside every preconnect; costs nothing
- `prefetch` — not worth adding on a 5-page site with fast static assets
- `prerender` — Chrome/Edge only, resource-intensive; skip
- `preload` — only if profiling reveals a critical render-path resource being fetched late

Do not add hints speculatively. Each one is a real browser instruction — noise here hurts more than silence.

## Resource hints for third-party fonts

A single `preconnect` with `crossorigin` is not enough for a font CDN. The first request to the CDN is the CSS stylesheet — not a CORS request — so the browser opens a second non-CORS connection and the crossorigin preconnect sits idle until the font files arrive. Use three hints in this order:

```html
<link rel="dns-prefetch" href="//fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin />
```

- dns-prefetch: fallback for browsers without preconnect support
- preconnect without crossorigin: covers the CSS stylesheet request
- preconnect with crossorigin: covers the actual woff2 font file requests

PageSpeed will report "Unused preconnect — check crossorigin attribute" if you only have the crossorigin variant. Est. savings ~300ms LCP.

## Font weight audit

Each font weight is a separate woff2 file (~24 KiB each), all chained off a blocking CSS request. Audit actual usage before loading multiple weights. Dropping one unused weight saves ~25 KiB and one round trip. Check what Inter weights are actually applied in global.css before defaulting to 400,500,600,700.

## GitHub Pages HTTP response headers

GitHub Pages does not support custom HTTP response headers. Security headers (X-Frame-Options, X-Content-Type-Options, Content-Security-Policy) cannot be set from the repo. The only path is to proxy through Cloudflare (free tier):

- Add domain to Cloudflare, update nameservers at registrar
- Set proxy mode to orange-cloud (proxied) on DNS records
- Add headers via Rules > Transform Rules > Modify Response Header
- Set SSL/TLS encryption mode to Full (not Flexible — Flexible causes redirect loops with GitHub Pages)

Cache TTL on Astro assets (default 10 minutes on GitHub Pages) also improves automatically with Cloudflare.

## Font loading

### Preconnect for third-party font services

A single `preconnect` with `crossorigin` is not enough. The first request to a font CDN is the CSS stylesheet, which is NOT a CORS request — so the browser opens a second connection, and your preconnect sits idle until the font files arrive.

Use two preconnect hints:

```html
<link rel="dns-prefetch" href="//fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin />
```

The non-crossorigin hint handles the stylesheet; the crossorigin hint handles the woff2 files. This matches what PageSpeed Insights flags as "Unused preconnect" when only the crossorigin version is present.

### Font weight verification

Before shipping a font URL, verify that every `font-weight` value declared in CSS is actually loaded. Mismatches are silent — the browser falls back to the nearest available weight with no warning.

Common traps with the default Inter + JetBrains Mono setup on fonts.bunny.net:

- `.wordmark` often gets `font-weight: 800` but the default URL only loads up to 700. Add `800` to the Inter weight list or change the declaration to 700.
- JetBrains Mono is typically loaded at `500` but CSS rules using `var(--font-mono)` often declare `font-weight: 600`. Either load `600` or change the declarations to `500`.

Detection: scan all CSS and page files for `font-weight` values, group by font-family context, and cross-check against the weights in the `fonts.bunny.net` URL.

## Self-hosting fonts

When third-party font latency shows up in PageSpeed (chain: HTML → CSS → woff2), self-hosting eliminates the dependency and collapses the critical path to one hop.

### Steps

1. Download woff2 files into `public/fonts/` — use the exact URLs from the browser network trace or PageSpeed waterfall.
2. Add `@font-face` blocks at the top of `global.css`, one per weight, with `font-display: swap` and correct `unicode-range`.
3. Remove all `dns-prefetch`, `preconnect`, and third-party `<link rel="stylesheet">` font references from Layout.astro.
4. Add `<link rel="preload">` hints for the two most critical weights (typically 400 and 600) — these fire before CSS is parsed.
5. Remaining weights load on demand as the browser processes the @font-face rules in CSS.

### Preload pattern (Layout.astro)

```html
<link rel="preload" href="/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin />
<link rel="preload" href="/fonts/inter-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin />
```

### @font-face pattern (global.css)

```css
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/inter-latin-400-normal.woff2') format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

Repeat for each weight. Place @font-face blocks at the very top of global.css, before `:root`.

### Font weight audit before downloading

  - `references/comtech-font-audit.md` for a worked example from comtechconsulting.dk.
- `references/llms-txt-template.md` — template for llms.txt on a personal consulting site.
- `references/ai-summary-css.md` — full CSS block for the AI summary section and buttons.


Before choosing which weights to download, scan the codebase for all `font-weight` declarations:
- Check global.css and all page/layout .astro files
- Note: `font-weight: 800` (or any weight) has no effect if that weight isn't loaded — browser silently falls back to nearest available
- Check that `font-family: var(--font-mono)` call sites declare a weight that is actually loaded
- `font-weight: 400` is rarely declared explicitly but is used implicitly for all body text — always include it

### Preconnect fix for third-party fonts (if not self-hosting)

If staying on a third-party font CDN, the `crossorigin` preconnect must be paired with a non-crossorigin preconnect. The font CSS request is not CORS, but woff2 requests are — without both hints, the browser opens a second connection:

```html
<link rel="dns-prefetch" href="//fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" />
<link rel="preconnect" href="https://fonts.bunny.net" crossorigin />
```

A single `<link rel="preconnect" ... crossorigin />` is not sufficient — the non-CORS CSS request will open a second connection anyway.

## AI discovery optimization

Two complementary additions that improve how AI assistants (ChatGPT browsing, Gemini, Perplexity, Bing Copilot) understand and represent a site.

### llms.txt

A plain-text file at `/public/llms.txt` that AI crawlers with retrieval use directly. Structure it as:

```
# Brand — domain

## Who
One paragraph: who the person/company is, location, positioning.

## What [brand] does
Sub-sections per service area with plain-prose descriptions.

## Industries / Clients

## Selected recognition

## What clients say
2–3 short quotes with attribution.

## Contact

## Site structure
- /path/ — one-line description per page
```

Keep it factual, scannable, no marketing fluff. This is machine-read first. See `references/llms-txt-template.md` for a worked example.

Add a pointer in robots.txt (already standard to have sitemap there; llms.txt is self-discoverable via crawl).

### AI summary section (deep-link buttons)

A lean section placed between `<main>` and `<footer>` in Layout.astro — appears on every page. No backend, no API keys, pure static.

Providers that support pre-populated prompts via query string (as of 2025):
- ChatGPT: `https://chatgpt.com/?q=<encoded prompt>`
- Google AI Mode: `https://www.google.com/search?q=<encoded prompt>&udm=50`

Both have web search enabled by default. Skip Claude — it does not browse by default, so accuracy suffers. Skip Gemini (`gemini.google.com/app?q=`) — the query string is silently dropped in practice; the prompt does not pre-populate. Google AI Mode is the clean Google-ecosystem alternative: standard search URL, reliable injection, opens in a browser tab.

Prompt pattern — ask for structure explicitly:
> "Based on https://domain.com, give me a structured overview of [Brand]. Use clear headings for: Who [Full Name] is, Services offered, Industries served, Recognition and credentials, and How to get in touch."

Explicit URL gives browsing AIs a direct target. Full name adds a personal search hook. **Asking for headings matters** — an open-ended prompt produces a prose blob. Naming each section in the prompt produces formatted output with those exact headings in both ChatGPT and Google AI Mode.

**Placement: hero CTA button is the primary entry point.** A footer row is too easy to miss — visitors who would actually use it are gone before they reach it. The right treatment is a third button in the hero actions row: ChatGPT logo inline SVG + label, same ghost-dark style as secondary CTAs. This keeps it discoverable without making AI the headline feature.

A footer row (quiet secondary row with hairline border-top, muted link text) is optional and worth adding if you want the action on every page. But if you have to choose one, choose the hero button. A standalone `<section>` between `<main>` and `<footer>` looks bolted on — avoid it entirely.

**Button label: "Ask AI" over "AI Summary".** "Summary" implies a result delivered on the page; the button actually hands the visitor off to ChatGPT. "Ask AI" is verb-led, honest about what it does, and shorter. If the footer row is present alongside the hero button, "Ask AI" also reads more naturally in a footer context than "AI Summary".

```astro
<a
  href={`https://chatgpt.com/?q=${encodeURIComponent('...')}`}
  target="_blank" rel="noopener noreferrer"
  class="btn btn-ghost-dark btn-ai-summary"
  aria-label="Get an AI summary via ChatGPT"
>
  <svg class="btn-ai-icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"
       xmlns="http://www.w3.org/2000/svg">
    <!-- ChatGPT logo path — see references/ai-summary-css.md -->
  </svg>
  AI Summary
</a>
```

CSS for the icon-text button:
```css
.btn-ai-summary { display: inline-flex; align-items: center; gap: 0.4em; opacity: 0.6; }
.btn-ai-summary:hover { opacity: 1; }
.btn-ai-icon    { width: 1em; height: 1em; flex-shrink: 0; }
```

**Demoting a tertiary button visually: use opacity alone, not font-size.** Reducing `font-size` on one button in a row breaks vertical alignment and makes the button look broken rather than subordinate. `opacity: 0.6` with `opacity: 1` on hover achieves the same hierarchy signal without disrupting the row's geometry. The button inherits the same size, padding, and border as its siblings — only the weight of presence differs.

The full ChatGPT SVG path is in `references/ai-summary-css.md`.

Footer row pattern in Layout.astro (inside `<footer>`, below the main footer content):

```astro
<div class="footer-ai">
  <span class="footer-ai-label">Ask an AI about COM&lt;tech&gt;</span>
  <div class="footer-ai-links">
    <a
      href={`https://chatgpt.com/?q=${encodeURIComponent('...')}`}
      target="_blank" rel="noopener noreferrer"
      class="footer-ai-link"
    >ChatGPT</a>
    <span class="footer-ai-sep" aria-hidden="true">·</span>
    <a
      href={`https://www.google.com/search?q=${encodeURIComponent('...')}&udm=50`}
      target="_blank" rel="noopener noreferrer"
      class="footer-ai-link"
    >Google AI</a>
  </div>
</div>
```

CSS: small uppercase label left, links right, same muted text color as `footer-email`. Use `var(--dark-text-3)` for label and separator, `var(--dark-text-2)` for links, `var(--dark-text)` on hover. Border-top to visually separate from main footer row. See `references/ai-summary-css.md` for the full CSS block.


## CSS quality audit (Project Wallace)

After any significant CSS consolidation pass, run:

```
https://www.projectwallace.com/css-code-quality?url=<domain>&prettify=1
```

Target: Maintainability 90+, Complexity 95+, Performance 90+. Scores are directional, not literal — each flagged item needs contextual assessment before acting. Most findings on a token-driven static site are expected, not actionable. Full interpretation guide and `!important` audit pattern in `senior-software-development/references/css-dead-rule-audit.md`.

## Lighthouse performance audit

Run against the local production build, not the dev server — `npm run dev` skips optimisations that affect real scores.

### Workflow

```bash
# 1. Build
npm run build

# 2. Start preview server in background
npm run preview -- --port 4321 &   # or use terminal(background=true)

# 3. Confirm it's up
curl -s -o /dev/null -w "%{http_code}" http://localhost:4321   # expect 200

# 4. Run Lighthouse
CHROME_PATH="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
npx lighthouse http://localhost:4321 \
  --output=json \
  --output-path=/tmp/lh-output.json \
  --chrome-flags="--headless=new --no-sandbox --disable-gpu" \
  --only-categories=performance,accessibility,best-practices,seo

# 5. Kill preview server when done
```

### macOS: no Chrome installed

Lighthouse requires a Chromium-family browser. On macOS without Chrome, Brave works — but the `--chrome-path` CLI flag is not honoured reliably. Use the `CHROME_PATH` environment variable instead:

```bash
CHROME_PATH="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
npx lighthouse <url> --chrome-flags="--headless=new --no-sandbox --disable-gpu" ...
```

`--headless=new` is required for Brave 148+ (old headless mode was removed in Chromium 112).

### Parsing results

Key fields in the JSON output:

```python
import json
data = json.load(open('/tmp/lh-output.json'))

# Category scores (0–100)
for k, v in data['categories'].items():
    print(v['title'], round(v['score'] * 100))

# Core Web Vitals
metrics = ['first-contentful-paint', 'largest-contentful-paint',
           'total-blocking-time', 'cumulative-layout-shift', 'interactive']
for m in metrics:
    a = data['audits'][m]
    print(a['title'], a.get('displayValue'), a.get('score'))

# Opportunities with savings
for k, a in data['audits'].items():
    if a.get('details', {}).get('type') == 'opportunity' and (a.get('score') or 1) < 1:
        ms = a.get('details', {}).get('overallSavingsMs', 0)
        print(a['title'], f'~{round(ms)}ms')
```

### comtechconsulting.dk baseline (30.05.2026)

Performance 99 · Accessibility 100 · Best Practices 100 · SEO 100

- FCP 1.5s · LCP 1.7s · TBT 0ms · CLS 0 · TTI 1.7s
- One diagnostic flag: render-blocking requests (score null — below penalty threshold)
- Self-hosted fonts with preload eliminated font-chain latency

See `references/lighthouse-comtech-2026-05.md` for full metric dump.

## Visual Review & Critique

The site ships a `scripts/critique.js` Playwright script that captures every page at desktop (1440×900) and mobile (390×844) viewports — both above-the-fold and full-page — then writes a manifest at `screenshots/critique/manifest.json`.

Run it:\n```\nnpm run critique        # full build + capture\nnpm run critique:fast   # skip build, use existing dist/\n```\n\n`critique:fast` serves the existing `dist/` — CSS or markup changes made after the last build will NOT be visible in the screenshots. Always run `npm run critique` (full build) when verifying a CSS or layout change. Use `critique:fast` only when re-capturing after a build you just ran.

After capture, load each screenshot via vision_analyze and ask for a strict UX/UI critique against the brand's design system. See `templates/critique.js` for the canonical script.

### Pitfall: IntersectionObserver / fade-up animations invisible in headless Playwright

Astro sites commonly use `.fade-up` animations gated on `.js` class and triggered via IntersectionObserver. Headless Playwright never scrolls, so the observer never fires — content stays at `opacity: 0` and screenshots show blank voids where sections should be.

**Fix:** Before taking screenshots, run a scroll simulation inside `page.evaluate()`. Use at least 20 steps and 120ms per step — 10 steps at 80ms is not enough for deep pages with many sections (e.g. about pages with 6+ sections below fold).

```js
await page.evaluate(async () => {
  const delay = (ms) => new Promise(r => setTimeout(r, ms));
  const scrollHeight = document.body.scrollHeight;
  const step = Math.ceil(scrollHeight / 20);
  for (let y = 0; y <= scrollHeight; y += step) {
    window.scrollTo(0, y);
    await delay(120);
  }
  // Pause at the bottom to ensure deep sections are fully revealed
  await delay(300);
  window.scrollTo(0, 0);
  await delay(500);
});
// Extra settle time after returning to top
await page.waitForTimeout(400);
```

This triggers all IntersectionObserver callbacks, then resets to top so fold captures are correct. The pause at the bottom matters — IntersectionObserver callbacks are async and the 120ms per step alone is not sufficient for sections at the very end of a long page.

---

## Pitfalls

- Page header bleed in flex section containers: if a section uses `display: flex; flex-direction: column; gap: Xrem`, the gap also applies between section-label, h1, and lead text. Fix: wrap the header group in a single `.page-header` div.
- Nav layout shift between pages: if one page has a scrollbar and another doesn't, the page width shifts ~15px. Fix: add `scrollbar-gutter: stable` to the `html` rule in global.css.
- Fade-up flash on page load: if `.fade-up { opacity: 0 }` is in plain CSS (not gated), the browser renders sections visible first, then JS hides them, then fades them in — a visible jump. Fix: add `<script is:inline>document.documentElement.classList.add('js');</script>` in `<head>` and gate the hidden state behind `.js .fade-up`.
- Always check whether `astro.config.mjs` exists before calling it absent — it is not in the `src/` tree.
- `@astrojs/sitemap` requires `site:` to be set; without it the sitemap URLs are relative and useless.
- `og:image` must be an absolute URL. Use `new URL(ogImage, Astro.site)` — not string concatenation.
- `og:site_name` is easy to miss. If the brand name contains `<` or `>`, use HTML entities (`COM&lt;tech&gt;`).
- ViewTransitions replaces the head on page navigation; confirm meta tags are in the persistent layout, not page-level slots.
- **macOS app URL interception overrides `target="_blank"`.** When a user has a desktop app installed (ChatGPT, Spotify, Slack), macOS registers it as the OS-level URL handler for that domain. Even with `target="_blank"`, clicking a link to `chatgpt.com` opens the app, not a browser tab. This is OS behaviour — there is nothing to fix in the HTML. Visitors without the app installed get a browser tab as expected. Do not add workarounds; mention it as expected behaviour if the user raises it.
- **Orphaned CSS after markup refactor causes invisible elements on dark backgrounds.** When a layout section is moved or replaced, its CSS class names often disappear silently — the markup renders but elements are unstyled. On a dark background (`var(--dark-bg)`), unstyled links and text become invisible with no error. After any structural refactor, search `global.css` for the new class names to confirm styles exist before assuming the feature is working. The symptom is "I don't see the buttons" with a clean build.
- **Preview server serves stale `dist/`.** After patching markup or CSS, restart the preview server — it serves the already-built `dist/`, not the new source. The symptom is confirming a visual change in the browser while it was built from the prior build. Pattern: kill the server, run `npm run build`, start a fresh server on a new port. Avoid reusing ports across a session — a zombie process may be bound to the old one silently.
- **DOM queries are more reliable than browser vision for correctness checks.** The vision tool captures only one viewport height; deep content (e.g. a section at offset 2400px) shows blank. Use `browser_console` with `document.querySelectorAll('.class').length` + `window.getComputedStyle(el)` to verify that elements exist and have the right computed values. Reserve vision captures for layout-level sanity checks on content that is in the initial viewport.
- patch mode corruption in .astro files: `mode=patch` (V4A format) is unreliable in `.astro` files — the diff tool can leak git diff headers (`+++ b/src/pages/about.astro`) verbatim into the file content, corrupting both frontmatter data arrays and template markup. This has triggered twice in practice: once editing a JS data array in the frontmatter block, once editing a `.map()` render section in the template. Recovery is always a `mode=replace` with a clean old/new pair that includes the corrupted diff-header text. Prevention: always use `mode=replace` for `.astro` files. The only exception where `mode=patch` is safe is small, isolated CSS additions in `<style>` blocks at the bottom of the file, where context lines are stable and the edit is additive-only.
