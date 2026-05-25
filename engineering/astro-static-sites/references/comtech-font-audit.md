# comtechconsulting.dk — Font Audit (May 2026)

## Fonts loaded (after self-hosting migration)

| File | Weight | Family |
|---|---|---|
| inter-latin-400-normal.woff2 | 400 | Inter |
| inter-latin-500-normal.woff2 | 500 | Inter |
| inter-latin-600-normal.woff2 | 600 | Inter |
| inter-latin-700-normal.woff2 | 700 | Inter |
| inter-latin-800-normal.woff2 | 800 | Inter |
| jetbrains-mono-latin-600-normal.woff2 | 600 | JetBrains Mono |

## Weight usage (src/styles/global.css + pages)

| Weight | Used by |
|---|---|
| 400 | Body text (implicit — no explicit declaration) |
| 500 | nav links, .btn, .hero-eyebrow, .tag, .about-lead, .contact-link-value, .testimonial-excerpt |
| 600 | Most common (14 declarations) — h3, strong, .section-label, .wordmark .ct (mono), .bento-link, .testimonial-author strong, .strength-item h4, .award-item h4, .signal-quote, .t-author strong, .quote-details summary, .repo-name (mono) |
| 700 | h1, h2, h4, .bento-tag, .bento-stat, .award-year, .contact-link-label, .contact-process-label, .signal-label, .t-category, .svc-title |
| 800 | .wordmark (global.css:77) |

## Issues found and fixed

1. **Inter 800 declared but not loaded** — .wordmark set font-weight: 800 but only 400–700 were loaded. Fixed by adding inter-latin-800-normal.woff2.
2. **JetBrains Mono weight mismatch** — loaded 500, but .wordmark .ct and .repo-name both declare font-weight: 600. Fixed by switching to jetbrains-mono-latin-600-normal.woff2.
3. **Preconnect missing non-CORS hint** — single crossorigin preconnect was ineffective for font CSS fetch. Fixed (then made moot by self-hosting).

## Preloaded weights

Inter 400 and 600 are preloaded in Layout.astro — these are the most render-critical weights.
