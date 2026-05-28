# AI summary — CSS and assets reference

## Footer row CSS (current preferred pattern)

The AI discovery row lives inside `<footer>`, below the main footer content, separated by a hairline border.

```css
.footer-ai {
  max-width: var(--max-w);
  margin: 1.25rem auto 0;
  padding-top: 1rem;
  border-top: 1px solid var(--dark-border);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.footer-ai-label {
  font-size: 0.6875rem;
  color: var(--dark-text-3);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.footer-ai-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.footer-ai-sep {
  color: var(--dark-text-3);
  font-size: 0.75rem;
}
.footer-ai-link {
  font-size: 0.75rem;
  color: var(--dark-text-2);
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: color 0.15s ease;
}
.footer-ai-link:hover { color: var(--dark-text); }
```

## Hero CTA button CSS

Used when adding an "AI Summary" button alongside the primary hero CTAs.

```css
.btn-ai-summary { display: inline-flex; align-items: center; gap: 0.4em; }
.btn-ai-icon    { width: 1em; height: 1em; flex-shrink: 0; }
```

Use `btn btn-ghost-dark btn-ai-summary` on the `<a>` element.

## ChatGPT SVG logo (inline)

Full path for the official ChatGPT logomark. Use `fill="currentColor"` so it inherits button text colour including hover state. Size is controlled by `btn-ai-icon` (1em × 1em).

```html
<svg class="btn-ai-icon" viewBox="0 0 24 24" fill="currentColor"
     aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.9 6.046 6.046 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.9A5.985 5.985 0 0 0 13.26 24a6.056 6.056 0 0 0 5.772-4.206 5.99 5.99 0 0 0 3.997-2.9 6.056 6.056 0 0 0-.747-7.073zM13.26 22.43a4.476 4.476 0 0 1-2.876-1.04l.141-.081 4.779-2.758a.795.795 0 0 0 .392-.681v-6.737l2.02 1.168a.071.071 0 0 1 .038.052v5.583a4.504 4.504 0 0 1-4.494 4.494zM3.6 18.304a4.47 4.47 0 0 1-.535-3.014l.142.085 4.783 2.759a.771.771 0 0 0 .78 0l5.843-3.369v2.332a.08.08 0 0 1-.033.062L9.74 19.95a4.5 4.5 0 0 1-6.14-1.646zM2.34 7.896a4.485 4.485 0 0 1 2.366-1.973V11.6a.766.766 0 0 0 .388.676l5.815 3.355-2.02 1.168a.076.076 0 0 1-.071 0l-4.83-2.786A4.504 4.504 0 0 1 2.34 7.872zm16.597 3.855l-5.833-3.387L15.119 7.2a.076.076 0 0 1 .071 0l4.83 2.791a4.494 4.494 0 0 1-.676 8.105v-5.678a.79.79 0 0 0-.407-.667zm2.01-3.023l-.141-.085-4.774-2.782a.776.776 0 0 0-.785 0L9.409 9.23V6.897a.066.066 0 0 1 .028-.061l4.83-2.787a4.5 4.5 0 0 1 6.68 4.66zm-12.64 4.135l-2.02-1.164a.08.08 0 0 1-.038-.057V6.075a4.5 4.5 0 0 1 7.375-3.453l-.142.08L8.704 5.46a.795.795 0 0 0-.393.681zm1.097-2.365l2.602-1.5 2.607 1.5v2.999l-2.597 1.5-2.607-1.5z"/>
</svg>
```

## Design notes

- Footer row uses dark-background tokens (`var(--dark-*)`) because the footer sits on a dark section.
- Hero CTA button uses `btn-ghost-dark` — same as secondary CTAs — so it reads as a peer option, not a feature callout.
- Both buttons open in a new tab (`target="_blank" rel="noopener noreferrer"`).
- No JavaScript required — pure anchor elements with encoded query strings.

## Legacy: standalone section CSS (superseded)

An earlier iteration placed a standalone `.ai-summary` section between `<main>` and `<footer>`. This was removed because it looked bolted on. The CSS below is kept for reference only — do not re-introduce the standalone section.

```css
.ai-summary { background: var(--surface); border-top: 1px solid var(--border); padding: 2.5rem 0; }
.ai-summary-inner { display: flex; align-items: center; justify-content: space-between; gap: 2rem; flex-wrap: wrap; }
.ai-summary-heading { font-size: 0.9375rem; font-weight: 600; color: var(--text-2); letter-spacing: -0.01em; margin: 0; }
.ai-summary-buttons { display: flex; gap: 0.75rem; flex-shrink: 0; flex-wrap: wrap; }
.ai-btn { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5625rem 1.125rem; font-size: 0.875rem; font-weight: 600; color: var(--text); background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius); text-decoration: none; transition: border-color 0.15s ease, box-shadow 0.15s ease, color 0.15s ease; white-space: nowrap; }
.ai-btn:hover { border-color: var(--accent); color: var(--accent); box-shadow: var(--shadow-sm); }
```
