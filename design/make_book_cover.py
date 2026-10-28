"""Draws the cover of The Middle-Eastern Drum Set. Run from the repository root."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2                      # supersample
W, H = 1600 * S, 2400 * S
F = 'fonts/'  # Cormorant Garamond and EB Garamond variable TTFs from Google Fonts
LOGO = 'public/assets/img/logo.webp'
TAN = (200, 164, 126); SOFT = (168, 140, 108); CREAM = (234, 220, 203); BG = (8, 7, 6)

def font(name, size, wght):
    f = ImageFont.truetype(F + name, size * S)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f

# background: black with a warm glow behind the drums
img = Image.new('RGB', (W, H), BG)
glow = Image.new('L', (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([W*0.12, H*0.33, W*0.88, H*0.86], fill=70)
glow = glow.filter(ImageFilter.GaussianBlur(260 * S))
img = Image.composite(Image.new('RGB', (W, H), (60, 40, 22)), img, glow)
d = ImageDraw.Draw(img)

def P(v): return v * S
def ring(cx, cy, r, w=1.5, col=TAN):
    d.ellipse([P(cx-r), P(cy-r), P(cx+r), P(cy+r)], outline=col, width=max(1, int(P(w))))
def disc(cx, cy, r, col):
    d.ellipse([P(cx-r), P(cy-r), P(cx+r), P(cy+r)], fill=col)
def line(a, b, w=1.2, col=TAN):
    d.line([P(a[0]), P(a[1]), P(b[0]), P(b[1])], fill=col, width=max(1, int(P(w))))
def polar(cx, cy, r, ang): return (cx + r * math.cos(ang), cy + r * math.sin(ang))
def dim(c, k): return tuple(int(x * k) for x in c)

def cymbal(cx, cy, r):
    disc(cx, cy, r, (22, 17, 12))
    for i in range(int(r // 7)):
        rr = r - i * 7
        ring(cx, cy, rr, 0.8, dim(TAN, 0.35 + 0.35 * ((i % 3) == 0)))
    ring(cx, cy, r, 2.2)
    disc(cx, cy, r * 0.22, (40, 31, 22)); ring(cx, cy, r * 0.22, 1.6)
    disc(cx, cy, 6, TAN)

def drum(cx, cy, r, lugs=8):
    disc(cx, cy, r + 10, (18, 14, 10))
    ring(cx, cy, r + 10, 2.2); ring(cx, cy, r, 1.4, SOFT)
    disc(cx, cy, r - 2, (30, 24, 18))
    for k in range(lugs):
        x, y = polar(cx, cy, r + 10, 2 * math.pi * k / lugs + 0.2)
        disc(x, y, 6, TAN)

def riq(cx, cy, r):
    disc(cx, cy, r + 16, (18, 14, 10)); ring(cx, cy, r + 16, 2.2)
    disc(cx, cy, r, (36, 29, 21)); ring(cx, cy, r, 1.2, SOFT)
    for k in range(5):  # pairs of zills in their slots
        a = 2 * math.pi * k / 5 - math.pi / 2
        for off in (-0.13, 0.13):
            x, y = polar(cx, cy, r + 8, a + off)
            disc(x, y, 9, (70, 56, 40)); ring(x, y, 9, 1.4)

def darbuka(cx, cy, r):
    disc(cx, cy, r + 26, (16, 12, 9)); ring(cx, cy, r + 26, 2.2)
    for i in range(1, 4): ring(cx, cy, r + 26 - i * 7, 0.8, dim(TAN, 0.45))
    disc(cx, cy, r, (40, 32, 24)); ring(cx, cy, r, 1.4, SOFT)
    # inlay of small diamonds around the body
    for k in range(18):
        x, y = polar(cx, cy, r + 13, 2 * math.pi * k / 18)
        d.regular_polygon((P(x), P(y), P(4)), 4, rotation=45, fill=TAN)

def rosette(cx, cy, r):
    """Eight-pointed star of two squares, with an inner star and petals."""
    for rad, w, col in ((r, 2.2, TAN), (r * 0.62, 1.4, SOFT)):
        for rot in (0, math.pi / 4):
            pts = [polar(cx, cy, rad, rot + k * math.pi / 2 + math.pi / 4) for k in range(4)]
            d.polygon([(P(x), P(y)) for x, y in pts], outline=col, width=int(P(w)))
    ring(cx, cy, r * 0.30, 1.4); disc(cx, cy, r * 0.12, TAN)
    for k in range(16):
        a = 2 * math.pi * k / 16
        line(polar(cx, cy, r * 0.30, a), polar(cx, cy, r * 0.44, a), 1.0, SOFT)

# --- the kit, seen from above, around a frame drum ---
CX, CY = 800, 1340
cymbal(1235, 1000, 215)        # ride
cymbal(355, 1025, 150)         # hi-hat
drum(1215, 1600, 150, 8)       # floor tom
riq(385, 1640, 112)
darbuka(820, 1900, 118)        # darbuka where the kick would sit, its head facing up

# central frame drum with the rhythm wheel (maqsum: dum tek . tek dum . tek .)
disc(CX, CY, 330, (24, 19, 14))
ring(CX, CY, 330, 3.0); ring(CX, CY, 318, 1.0, SOFT); ring(CX, CY, 300, 1.0, dim(TAN, 0.5))
rosette(CX, CY, 250)
WHEEL = 392
ring(CX, CY, WHEEL, 1.0, dim(TAN, 0.55))
maqsum = 'DT.TD.T.'
for k, s in enumerate(maqsum * 2):
    a = -math.pi / 2 + 2 * math.pi * k / 16
    x, y = polar(CX, CY, WHEEL, a)
    if s == 'D': disc(x, y, 17, TAN)
    elif s == 'T': disc(x, y, 9, CREAM)
    else: ring(x, y, 5, 1.2, SOFT)

# fine grain, so the black reads as paper rather than screen
noise = Image.effect_noise((W // 4, H // 4), 18).resize((W, H)).convert('L')
img = Image.blend(img, Image.merge('RGB', (noise, noise, noise)), 0.035)
d = ImageDraw.Draw(img)

# --- type ---
def text_c(y, s, f, col, track=0):
    if track:
        widths = [d.textlength(ch, font=f) for ch in s]
        total = sum(widths) + P(track) * (len(s) - 1)
        x = (W - total) / 2
        for ch, w in zip(s, widths):
            d.text((x, P(y)), ch, font=f, fill=col); x += w + P(track)
    else:
        w = d.textlength(s, font=f); d.text(((W - w) / 2, P(y)), s, font=f, fill=col)

text_c(150, 'NADAV FRIEDMAN', font('EBGaramond[wght].ttf', 34, 500), SOFT, track=9)
text_c(300, 'THE MIDDLE-EASTERN', font('CormorantGaramond[wght].ttf', 74, 500), TAN, track=7)
text_c(380, 'Drum Set', font('CormorantGaramond[wght].ttf', 230, 500), CREAM)
d.line([P(700), P(670), P(900), P(670)], fill=SOFT, width=P(1))
sub = font('EBGaramond-Italic[wght].ttf', 40, 400)
text_c(2075, 'Bringing the oral traditions of rhythm', sub, TAN)
text_c(2127, 'to the modern drum set', sub, TAN)

# logo mark at the foot
logo = Image.open(LOGO).convert('RGBA')
lh = P(120); logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
img.paste(logo, ((W - logo.width) // 2, P(2215)), logo)

# frame
d = ImageDraw.Draw(img)
d.rectangle([P(48), P(48), W - P(48), H - P(48)], outline=dim(TAN, 0.55), width=P(1))

out = img.resize((1600, 2400), Image.LANCZOS)
out.save('design/book-cover-middle-eastern-drum-set.png')
print('ok')
