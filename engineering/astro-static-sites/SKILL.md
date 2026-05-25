---
name: astro-static-sites
description: Build, review, and extend Astro static sites — config, integrations, SEO, deployment to GitHub Pages.
version: "1.0.6"
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
- No OG/Twitter meta → unfurled links on LinkedIn/Slack show nothing
- Dead CSS in global.css from superseded layouts → run the detection pattern below
- Hardcoded color values in page-local `<style>` blocks — scan for `rgba(`, `#[0-9a-fA-F]` and replace with CSS custom properties
- Hugo migration artifacts left in repo → see pitfalls section

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
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
.js .fade-up          { opacity: 0; transform: translateY(18px); }
.js .fade-up.visible  { animation: fade-up 420ms cubic-bezier(0.22, 1, 0.36, 1) both; }
```

18px rise, 420ms, natural ease-out. Single pass — never re-triggers on re-entry. Hero excluded (already visible on load).

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

See `references/comtech-font-audit.md` for a worked example from comtechconsulting.dk.


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

## Pitfalls

- Page header bleed in flex section containers: if a section uses `display: flex; flex-direction: column; gap: Xrem`, the gap also applies between section-label, h1, and lead text. Fix: wrap the header group in a single `.page-header` div.
- Nav layout shift between pages: if one page has a scrollbar and another doesn't, the page width shifts ~15px. Fix: add `scrollbar-gutter: stable` to the `html` rule in global.css.
- Fade-up flash on page load: if `.fade-up { opacity: 0 }` is in plain CSS (not gated), the browser renders sections visible first, then JS hides them, then fades them in — a visible jump. Fix: add `<script is:inline>document.documentElement.classList.add('js');</script>` in `<head>` and gate the hidden state behind `.js .fade-up`.
- Always check whether `astro.config.mjs` exists before calling it absent — it is not in the `src/` tree.
- `@astrojs/sitemap` requires `site:` to be set; without it the sitemap URLs are relative and useless.
- `og:image` must be an absolute URL. Use `new URL(ogImage, Astro.site)` — not string concatenation.
- `og:site_name` is easy to miss. If the brand name contains `<` or `>`, use HTML entities (`COM&lt;tech&gt;`).
- ViewTransitions replaces the head on page navigation; confirm meta tags are in the persistent layout, not page-level slots.
- **patch mode corruption in .astro files**: `mode=patch` (V4A format) is unreliable in `.astro` files — the diff tool can leak git diff headers (`+++ b/src/pages/about.astro`) verbatim into the file content, corrupting both frontmatter data arrays and template markup. This has triggered twice in practice: once editing a JS data array in the frontmatter block, once editing a `.map()` render section in the template. Recovery is always a `mode=replace` with a clean old/new pair that includes the corrupted diff-header text. Prevention: always use `mode=replace` for `.astro` files. The only exception where `mode=patch` is safe is small, isolated CSS additions in `<style>` blocks at the bottom of the file, where context lines are stable and the edit is additive-only.
