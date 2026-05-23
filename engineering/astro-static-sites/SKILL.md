---
name: astro-static-sites
description: Build, review, and extend Astro static sites — config, integrations, SEO, deployment to GitHub Pages.
version: "1.0"
tags: [astro, static-site, github-pages, seo, deployment, css]
tool_agnostic: true
authors: [Anders Hybertz]
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

## Pitfalls

- Page header bleed in flex section containers: if a section uses `display: flex; flex-direction: column; gap: Xrem`, the gap also applies between section-label, h1, and lead text. Fix: wrap the header group in a single `.page-header` div.
- Nav layout shift between pages: if one page has a scrollbar and another doesn't, the page width shifts ~15px. Fix: add `scrollbar-gutter: stable` to the `html` rule in global.css.
- Fade-up flash on page load: if `.fade-up { opacity: 0 }` is in plain CSS (not gated), the browser renders sections visible first, then JS hides them, then fades them in — a visible jump. Fix: add `<script is:inline>document.documentElement.classList.add('js');</script>` in `<head>` and gate the hidden state behind `.js .fade-up`.
- Always check whether `astro.config.mjs` exists before calling it absent — it is not in the `src/` tree.
- `@astrojs/sitemap` requires `site:` to be set; without it the sitemap URLs are relative and useless.
- `og:image` must be an absolute URL. Use `new URL(ogImage, Astro.site)` — not string concatenation.
- `og:site_name` is easy to miss. If the brand name contains `<` or `>`, use HTML entities (`COM&lt;tech&gt;`).
- ViewTransitions replaces the head on page navigation; confirm meta tags are in the persistent layout, not page-level slots.
