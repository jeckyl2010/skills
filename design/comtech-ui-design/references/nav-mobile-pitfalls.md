# Mobile Nav Pitfalls

## Active state bleed (fixed 2026-05-28)

### Symptom
The accent-dim background on the active `<a>` bleeds into the adjacent menu item.
Visually looks like two items are selected simultaneously. The border-radius bridges
the gap between items.

### Root cause
`<a>` elements are inline by default. In a flex column container, the background box
is not constrained to the row. With `gap: 0.25rem` the rounded corners of the fill
visually merge with the item below.

### Fix
```css
@media (max-width: 680px) {
  .nav-links li { display: block; }
  .nav-links a { display: block; padding: 0.875rem 1rem; }
}
```

Both `display: block` rules are required. The `<li>` block ensures the flex child
is full-width; the `<a>` block constrains the background fill to the row.

### Minimum safe padding
`0.875rem` vertical. At `0.75rem` the bleed reappears on devices with larger default
font scaling (iPhone Accessibility → Larger Text).

### How to catch it
The critique script captures mobile screenshots but at a fixed simulated viewport —
it does not replicate real device font scaling or Safari's rendering engine.
Always verify nav changes on a real device or Safari + Responsive Design Mode after
any nav styling change.
