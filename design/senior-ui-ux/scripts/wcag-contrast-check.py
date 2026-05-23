#!/usr/bin/env python3
"""
WCAG AA contrast ratio checker.
Edit the TOKENS list below with your colour pairs, then run:
    python3 wcag-contrast-check.py
"""

def linearize(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(r, g, b):
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast(c1, c2):
    l1, l2 = luminance(*c1), luminance(*c2)
    if l1 < l2: l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Edit this table ──────────────────────────────────────────────────────────
# (label, fg_hex, bg_hex)
TOKENS = [
    ("--text on --bg",              "#f4f4f5", "#0d0d10"),
    ("--text-2 on --bg",            "#a1a1aa", "#0d0d10"),
    ("--dark-text-3 on --bg",       "#7c7c7c", "#0d0d10"),
    ("--accent on light nav",       "#5352cc", "#f9f9f8"),
    ("--accent-text on --bg",       "#7c7bef", "#0d0d10"),
    ("dark label #818cf8 on --bg",  "#818cf8", "#0d0d10"),
]
# ─────────────────────────────────────────────────────────────────────────────

print(f"{'Token / usage':<40} {'Ratio':>6}  {'Normal AA':>10}  {'Large AA':>9}")
print("-" * 72)
for label, fg, bg in TOKENS:
    r = contrast(hex_to_rgb(fg), hex_to_rgb(bg))
    aa_n = "PASS" if r >= 4.5 else "FAIL"
    aa_l = "PASS" if r >= 3.0 else "FAIL"
    print(f"{label:<40} {r:>6.2f}  {aa_n:>10}  {aa_l:>9}")
