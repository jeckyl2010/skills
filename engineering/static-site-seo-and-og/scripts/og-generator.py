"""
og-generator.py — 1200x630 Open Graph image for dark B2B consultancy sites.
Run from repo root: python3 scripts/gen-og.py
Output: public/og-default.png

EDIT THESE to customise for a new site:
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), '../public/og-default.png')

# ── Brand colours (RGB tuples) ────────────────────────────────────────────────
BG      = (13,  13,  16)
ACCENT  = (83,  82, 204)
ACCENT2 = (99,  98, 220)
TEXT_1  = (244, 244, 245)
TEXT_2  = (161, 161, 170)
TEXT_3  = (100, 100, 112)
BORDER  = (42,  42,  53)

# ── Content ───────────────────────────────────────────────────────────────────
WORDMARK_MAIN = 'COM'
WORDMARK_MONO = '<tech>'          # rendered in accent colour
HEADLINE      = 'Software architecture built for the places where it has to work.'
SUBTITLE      = 'Senior Software Architect & Technical Lead · Copenhagen'
TAGS          = ['Pharma', 'Finance', 'Energy', 'Azure', 'Regulated systems']
STATS         = [
    ('30 years',      'of industry experience'),
    ('8 industries',  'from pharma to public sector'),
    ('Direct contact','no account managers'),
]
FOOTER_URL    = 'comtechconsulting.dk'

# ── Column geometry ───────────────────────────────────────────────────────────
M       = 36          # frame margin
LEFT_X  = 76
LEFT_W  = 590         # max text width for left column
SPLIT_X = LEFT_X + LEFT_W + 40   # = 706
RIGHT_X = SPLIT_X + 40           # = 746

# ── Canvas ────────────────────────────────────────────────────────────────────
img  = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img, 'RGBA')

# ── Aurora blobs — pushed into frame corners, away from all text ──────────────
for r in range(220, 0, -4):
    alpha = int(20 * (r / 220) ** 1.9)
    draw.ellipse([W - r, -r, W + r, r], fill=(*ACCENT, alpha))
for r in range(160, 0, -4):
    alpha = int(12 * (r / 160) ** 2.1)
    draw.ellipse([M - r, H - M - r, M + r, H - M + r], fill=(*ACCENT2, alpha))

# ── Border frame ──────────────────────────────────────────────────────────────
draw.rectangle([M, M, W - M, H - M], outline=(*BORDER, 200), width=1)
draw.rectangle([M, M, W - M, M + 3], fill=ACCENT)

# ── Right column tinted panel + vertical rule ─────────────────────────────────
draw.rectangle([SPLIT_X, M + 3, W - M, H - M], fill=(20, 20, 26, 200))
draw.line([(SPLIT_X, M + 3), (SPLIT_X, H - M)], fill=(*BORDER, 220), width=1)

# ── Fonts ─────────────────────────────────────────────────────────────────────
def load(size, bold=False):
    for p in [
        f'/System/Library/Fonts/Supplemental/{"Arial Bold" if bold else "Arial"}.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
    ]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

f_wordmark = load(52, bold=True)
f_tech     = load(52)
f_headline = load(40, bold=True)
f_sub      = load(20)
f_tag      = load(13, bold=True)
f_stat_num = load(28, bold=True)
f_stat_lbl = load(14)
f_footer   = load(13)

def tw(text, font):
    return int(draw.textlength(text, font=font))

# ── Wordmark ──────────────────────────────────────────────────────────────────
Y0 = 88
draw.text((LEFT_X, Y0), WORDMARK_MAIN, font=f_wordmark, fill=TEXT_1)
com_w = tw(WORDMARK_MAIN, f_wordmark)
draw.text((LEFT_X + com_w, Y0), WORDMARK_MONO, font=f_tech, fill=ACCENT)
draw.line([(LEFT_X, 164), (SPLIT_X - 20, 164)], fill=(*BORDER, 220), width=1)

# ── Headline — programmatically word-wrapped to LEFT_W ───────────────────────
# NEVER hand-break with \n — Pillow won't auto-advance Y per line
words = HEADLINE.split()
lines, cur = [], ''
for word in words:
    test = (cur + ' ' + word).strip()
    if tw(test, f_headline) <= LEFT_W:
        cur = test
    else:
        if cur: lines.append(cur)
        cur = word
if cur: lines.append(cur)

hy = 188
for line in lines:
    draw.text((LEFT_X, hy), line, font=f_headline, fill=TEXT_1)
    hy += 52

# ── Subtitle + tags ───────────────────────────────────────────────────────────
sub_y = hy + 18
draw.text((LEFT_X, sub_y), SUBTITLE, font=f_sub, fill=TEXT_2)

tx, ty = LEFT_X, sub_y + 36
px, py = 11, 5
for tag in TAGS:
    bw = tw(tag, f_tag) + px * 2
    bh = int(f_tag.size) + py * 2
    draw.rounded_rectangle([tx, ty, tx + bw, ty + bh],
                            radius=5,                 # rectangular with soft corners — NOT pill (999)
                            fill=(*ACCENT, 36),
                            outline=(*ACCENT, 110), width=1)
    draw.text((tx + px, ty + py), tag, font=f_tag, fill=(*ACCENT2, 255))
    tx += bw + 8

# ── Right column stats — centred in panel, vertically centred ─────────────────
rw = W - M - RIGHT_X
stat_block_h = len(STATS) * (28 + 34) + (len(STATS) - 1) * 22
ry = (M + 3) + ((H - M) - (M + 3) - stat_block_h) // 2

for num, label in STATS:
    nw = tw(num, f_stat_num)
    lw = tw(label, f_stat_lbl)
    draw.text((RIGHT_X + (rw - nw) // 2, ry),      num,   font=f_stat_num, fill=TEXT_1)
    draw.text((RIGHT_X + (rw - lw) // 2, ry + 34), label, font=f_stat_lbl, fill=TEXT_2)
    ry += 28 + 34 + 22

# ── Centred footer URL ────────────────────────────────────────────────────────
fw = tw(FOOTER_URL, f_footer)
draw.text(((W - fw) // 2, H - 60), FOOTER_URL, font=f_footer, fill=TEXT_3)

# ── Save ─────────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
img.save(OUT, 'PNG', optimize=True)
print(f'Saved: {os.path.abspath(OUT)}  ({W}x{H})')
