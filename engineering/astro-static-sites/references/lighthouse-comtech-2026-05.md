# Lighthouse audit — comtechconsulting.dk — 30.05.2026

Tested against local production build (`npm run build` + `npm run preview`) on macOS 26.5.
Tool: `npx lighthouse@13.3.0` via Brave Browser 148.1.90.124.

## Scores

| Category       | Score |
|----------------|-------|
| Performance    | 99    |
| Accessibility  | 100   |
| Best Practices | 100   |
| SEO            | 100   |

## Core Web Vitals

| Metric                      | Value  | Score |
|-----------------------------|--------|-------|
| First Contentful Paint      | 1.5 s  | 0.96  |
| Largest Contentful Paint    | 1.7 s  | 0.99  |
| Total Blocking Time         | 0 ms   | 1.0   |
| Cumulative Layout Shift     | 0      | 1.0   |
| Speed Index                 | 1.5 s  | 1.0   |
| Time to Interactive         | 1.7 s  | 1.0   |

## Opportunities

None. No opportunities with measurable savings were flagged.

## Diagnostics

- Render-blocking requests: flagged but score=null (below penalty threshold). Likely a stylesheet
  load order detail. Not actionable at current score level.

## Notes

- Self-hosted fonts with preload (Inter 400/600) contributed to the clean TBT and LCP numbers.
- FCP at 1.5s is the soft target for future improvement. LCP element was not separately identified
  in this run — worth checking with `--extra-headers` or a follow-up run with element capture.
- Zero CLS confirms the font-display:swap implementation is stable.
