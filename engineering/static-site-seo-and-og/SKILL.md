---
name: static-site-seo-and-og
description: Add SEO meta tags, Open Graph, Twitter Card, canonical URLs, sitemap, and a generated OG image to a static site.
version: "1.0"
tags: [seo, open-graph, sitemap, astro, static-site, social-sharing]
tool_agnostic: true
authors: [Anders Hybertz]
tested_on: []
---

# Static site SEO and Open Graph setup

Use this skill when a static marketing or consultancy site needs OG tags, a sitemap, canonical URLs, or a generated social sharing image.

## Trigger conditions

- Site has no og:title / og:image / og:description tags
- Unfurled links on LinkedIn / Slack / iMessage show blank or wrong previews
- No sitemap.xml in the build output
- Canonical URL tag is missing (duplicate content risk)
- Need a 1200x630 social card image to complete the og:image reference

## Recommended workflow

### 1. Audit first

Check the shared layout/shell for existing meta tags before adding anything. Look for:
- `<meta name="description">` — usually already present
- `<link rel="canonical">` — usually missing
- `og:*` and `twitter:*` tags — usually missing on marketing sites
- Whether `Astro.site` (or equivalent) is set in the framework config

### 2. Framework config

For Astro: ensure `astro.config.mjs` has `site` set to the canonical domain and `output: 'static'`. Add `@astrojs/sitemap` integration here.

```js
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://yourdomain.com',
  output: 'static',
  trailingSlash: 'always',
  integrations: [sitemap()],
});
```

Install: `npm install @astrojs/sitemap`

### 3. Layout meta block

Add to the `<head>` of the shared layout. See `templates/layout-og-block.astro` for the full block.

Key points:
- Build `canonicalURL` from `new URL(Astro.url.pathname, Astro.site)` — do not manually concatenate strings
- Build `og:image` URL from `new URL(ogImage, Astro.site)` — same reason
- Add `ogImage` as an optional prop with a sensible default (`/og-default.png`)
- Set `og:locale` to match the site's language/region (`en_DK` for Danish-English)
- `twitter:card` should be `summary_large_image` when an og:image exists
- Add `og:site_name` — used by LinkedIn and some scrapers to display the brand name separately from the page title
- Add `<link rel="icon" type="image/svg+xml" href="/favicon.svg" />` — often missing entirely. Place it before font preconnects.

### 4. OG image generation

Use the Pillow-based Python generator in `scripts/og-generator.py`. It produces a 1200x630 PNG suitable for `summary_large_image`.

Design spec that works for senior B2B consultancy sites:
- Dark background (#0d0d10) with two soft aurora blobs (accent colour, low opacity)
- Top accent bar (3px, accent colour)
- Wordmark top-left, thin divider below
- Large bold headline (the site's primary value proposition)
- Sub-line (role + location), then tag pills immediately below
- Right column: 3 punchy trust signals (years / industries / contact model), centred in panel
- URL centred at the bottom at readable-but-subtle contrast

Two-column layout geometry (critical — see pitfalls):
- LEFT_X=76, LEFT_W=590, SPLIT_X=706, RIGHT_X=746
- Right column gets a tinted background panel (subtle) + vertical rule on its left edge
- Aurora blobs placed fully outside content area (top-right corner, bottom-left corner)
- Headline word-wrapped programmatically to LEFT_W — never hand-broken with \n

Run: `python3 scripts/gen-og.py` from the repo root. Output goes to `public/og-default.png`.

Fonts: Use system Arial Bold / Arial from `/System/Library/Fonts/Supplemental/`. Always provide a fallback to Helvetica and then `ImageFont.load_default()`.

### 5. robots.txt

Add to `public/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap-index.xml
```

Without this, Google is guessing at crawl permissions and may not discover the sitemap automatically.

### 6. Verify

```bash
npm run build
ls dist/og-default.png       # image copied verbatim from public/
cat dist/sitemap-0.xml       # all pages present, trailing slashes match config
grep og:image dist/index.html  # absolute URL, not a relative path
```

## Pitfalls

- `og:image` must be an absolute URL. `new URL(ogImage, Astro.site)` handles this. A relative path renders nothing on social platforms.
- `@astrojs/sitemap` requires `site` in the Astro config — it will silently produce nothing without it.
- Pillow on macOS may not be installed by default. Install with `pip3 install pillow`.
- Do not store the generated PNG in the repo — keep it in `public/` and regenerate from the script.
- CRITICAL: never hand-break the headline with `\n`. Pillow renders both parts as separate layout lines — overprinting or bleed. Always word-wrap programmatically by testing `draw.textlength()` against LEFT_W.
- CRITICAL: text in Pillow has no column clipping. Define column geometry constants (LEFT_X, LEFT_W, SPLIT_X, RIGHT_X) at the top and word-wrap every multi-line text block against LEFT_W.
- Aurora blobs must be placed outside the content area. A blob near stats text will reduce contrast even at low alpha. Keep blobs in frame corners.
- Tag pills: use `radius=5` (rounded rectangle). `radius=999` produces pill shapes — acceptable visually, but rectangular with softened corners is preferred.
- Right column stats should be centred within the panel, not left-aligned. Compute `nx = RIGHT_X + (rw - nw) // 2` per stat.
- Footer URL: centre it horizontally at the bottom (`(W - fw) // 2`). Bottom-left placement reads as an afterthought.
- Favicon: a text-based SVG favicon (using a `<text>` element) collapses at 16px tab size. Use drawn SVG paths or polylines. For a `<>` mark, polyline chevrons work well: `<polyline points="13,9 7,16 13,23" />` (left) and `<polyline points="19,9 25,16 19,23" />` (right) on a `0 0 32 32` viewBox. Asymmetric opacity helps — left chevron full white, right at 55% opacity.

## Verification

After deploying, verify OG tags with one of these — do NOT use opengraph.xyz alone, it occasionally returns Bad Request for valid pages:

- LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/inspect/<URL> (most reliable)
- metatags.io: https://metatags.io/?url=<URL>
- Facebook debugger: https://developers.facebook.com/tools/debug/?q=<URL>

If a checker reports bad request but `curl <URL> | grep og:image` returns a valid absolute URL, the checker is wrong — the tags are fine.

## Support files

- `templates/layout-og-block.astro` — drop-in Astro Layout head block with OG, Twitter Card, canonical
- `scripts/og-generator.py` — Pillow-based 1200x630 OG image generator, dark B2B style
