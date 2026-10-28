"""Draws the cover of The Middle-Eastern Drum Set (run from the repository root).
Cover v2: Nadav's own percussion set seen from above, on a Persian rug, drawn in the site's palette."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(7)
S = 2
W, H = 1600 * S, 2400 * S
F = 'fonts/'  # Cormorant Garamond and EB Garamond variable TTFs from Google Fonts
LOGO = 'public/assets/img/logo.webp'
OUT = 'design/book-cover-middle-eastern-drum-set.png'
TAN = (200, 164, 126); SOFT = (168, 140, 108); CREAM = (234, 220, 203); BG = (8, 7, 6)
BRONZE = (120, 92, 58); WOOD = (92, 66, 42); SKIN = (58, 46, 34); INK = (24, 30, 44)

def font(name, size, wght):
    f = ImageFont.truetype(F + name, size * S)
    try: f.set_variation_by_axes([wght])
    except Exception: pass
    return f
def dim(c, k): return tuple(int(x * k) for x in c)
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# photo coordinates (2000 x 1390) -> cover
K, OX, OY = 0.70, 100, 850
def X(x): return (OX + K * x) * S
def Y(y): return (OY + K * y) * S
def R(r): return K * r * S
def circ(x, y, r, **kw): d.ellipse([X(x) - R(r), Y(y) - R(r), X(x) + R(r), Y(y) + R(r)], **kw)
def ring(x, y, r, w=1.5, col=TAN): circ(x, y, r, outline=col, width=max(1, int(w * S)))
def polar(x, y, r, a): return (x + r * math.cos(a), y + r * math.sin(a))

# --- the rug: border bands, a field of small motifs, a central medallion ---
RX0, RY0, RX1, RY1 = 0, 0, 2000, 1390
d.rectangle([X(RX0), Y(RY0), X(RX1), Y(RY1)], fill=(24, 19, 15))
d.rectangle([X(RX0 + 132), Y(RY0 + 132), X(RX1 - 132), Y(RY1 - 132)], fill=(30, 24, 19))
for inset, w, col in ((14, 2, dim(TAN, .5)), (40, 1, dim(TAN, .35)), (118, 1, dim(TAN, .35)), (132, 2, dim(TAN, .5))):
    d.rectangle([X(RX0 + inset), Y(RY0 + inset), X(RX1 - inset), Y(RY1 - inset)], outline=col, width=w * S)
# border motifs
step = 46
for x in range(70, 2000 - 60, step):
    for y in (79, 1390 - 79):
        d.regular_polygon((X(x), Y(y), R(15)), 4, rotation=45, outline=dim(TAN, .38), width=S)
        circ(x, y, 4, fill=dim(TAN, .32))
for y in range(70 + step, 1390 - 60, step):
    for x in (79, 2000 - 79):
        d.regular_polygon((X(x), Y(y), R(15)), 4, rotation=45, outline=dim(TAN, .38), width=S)
        circ(x, y, 4, fill=dim(TAN, .32))
# field: a lattice of small eight-pointed stars
for gx in range(230, 1800, 120):
    for gy in range(220, 1200, 120):
        for rot in (0, 45):
            d.regular_polygon((X(gx), Y(gy), R(20)), 4, rotation=rot, outline=(52, 64, 92), width=S)
        circ(gx, gy, 5, fill=dim(TAN, .35))
        d.regular_polygon((X(gx + 60), Y(gy + 60), R(9)), 4, rotation=45, fill=dim(TAN, .22))
# medallion
for rr, col in ((330, dim(TAN, .4)), (250, dim(TAN, .32)), (170, (60, 74, 104))):
    pts = [polar(1000, 695, rr * (1 if k % 2 == 0 else .62), k * math.pi / 8) for k in range(16)]
    d.polygon([(X(x), Y(y)) for x, y in pts], outline=col, width=S)

# --- instruments ---
def shadow(x, y, r):
    sh = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(sh)
    sd.ellipse([X(x) - R(r) + 10 * S, Y(y) - R(r) + 16 * S, X(x) + R(r) + 10 * S, Y(y) + R(r) + 16 * S], fill=150)
    return sh.filter(ImageFilter.GaussianBlur(14 * S))
shadows = Image.new('L', (W, H), 0)
for x, y, r in ((505, 470, 225), (260, 680, 110), (1048, 500, 168), (1205, 893, 210), (1530, 325, 385),
                (1655, 1035, 345), (215, 1105, 210), (420, 1020, 100)):
    shadows = Image.composite(Image.new('L', (W, H), 255), shadows, shadow(x, y, r))
img = Image.composite(Image.new('RGB', (W, H), (0, 0, 0)), img, shadows.point(lambda v: int(v * .55)))
d = ImageDraw.Draw(img)

def hide_drum(x, y, r, head, lugs=8):
    circ(x, y, r, fill=WOOD); ring(x, y, r, 2.2, TAN)
    circ(x, y, r - 18, fill=head); ring(x, y, r - 18, 1.2, SOFT)
    for k in range(lugs):
        px, py = polar(x, y, r - 9, 2 * math.pi * k / lugs + .3)
        circ(px, py, 5, fill=CREAM)

# frame drum with inner snares, played as the kick
circ(505, 470, 222, fill=mix(WOOD, TAN, .2)); ring(505, 470, 222, 2.4)
circ(505, 470, 206, fill=(54, 46, 38)); ring(505, 470, 206, 1, SOFT)
for i, yy in enumerate((395, 408, 421, 434, 447)):
    half = math.sqrt(206 ** 2 - (yy - 470) ** 2) - 25
    d.line([X(505 - half), Y(yy), X(505 + half), Y(yy)], fill=dim(CREAM, .55), width=S)
circ(485, 520, 46, fill=BRONZE); ring(485, 520, 46, 1.2, TAN)
d.line([X(470), Y(545), X(430), Y(650)], fill=TAN, width=7 * S)

# riq
circ(260, 680, 108, fill=WOOD); ring(260, 680, 108, 2.2)
circ(260, 680, 86, fill=(70, 62, 52)); ring(260, 680, 86, 1, SOFT)
for k in range(5):
    a = 2 * math.pi * k / 5 + .5
    for off in (-.14, .14):
        px, py = polar(260, 680, 97, a + off)
        circ(px, py, 13, fill=(150, 120, 60)); ring(px, py, 13, 1.2, CREAM)

# bass drum pedal
pts = [(805, 360), (845, 360), (850, 470), (868, 560), (858, 655), (812, 655), (800, 560), (815, 470)]
d.polygon([(X(a), Y(b)) for a, b in pts], fill=(70, 66, 62), outline=TAN, width=S * 2)
d.line([X(826), Y(360), X(826), Y(300)], fill=SOFT, width=4 * S)
circ(826, 300, 16, fill=SOFT)

# two hide drums: a white goat skin and a spotted one
hide_drum(1048, 500, 168, (176, 160, 138))
hide_drum(1205, 893, 210, (150, 128, 102), 10)
for _ in range(16):  # spots
    a = random.uniform(0, 2 * math.pi); rr = random.uniform(0, 140)
    px, py = polar(1205, 893, rr, a); w_, h_ = random.uniform(20, 55), random.uniform(14, 40)
    d.ellipse([X(px - w_), Y(py - h_), X(px + w_), Y(py + h_)], fill=(52, 36, 24))

# cajon
d.rectangle([X(600), Y(850), X(945), Y(1225)], fill=mix(WOOD, TAN, .45), outline=TAN, width=2 * S)
for k in range(1, 9):
    yy = 850 + k * 41
    d.line([X(612), Y(yy), X(933), Y(yy + random.uniform(-6, 6))], fill=mix(WOOD, CREAM, .55), width=S)
d.rectangle([X(612), Y(862), X(933), Y(1213)], outline=mix(WOOD, TAN, .2), width=S)

# clay pot and the lit frame drum
circ(420, 1020, 98, fill=(120, 74, 46)); ring(420, 1020, 98, 2, TAN)
for k in range(9):
    a = -1.0 + k * .25
    d.line([X(420), Y(1020), *[X(v) if i == 0 else Y(v) for i, v in enumerate(polar(420, 1020, 92, a))]], fill=dim(CREAM, .5), width=S)
glow = Image.new('RGB', (W, H), (0, 0, 0)); gm = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(gm)
for i in range(40):
    rr = 200 * (1 - i / 40)
    gd.ellipse([X(215) - R(rr), Y(1105) - R(rr), X(215) + R(rr), Y(1105) + R(rr)], fill=int(90 + 160 * i / 40))
gm = gm.filter(ImageFilter.GaussianBlur(10 * S))
circ(215, 1105, 210, fill=(96, 62, 34)); ring(215, 1105, 210, 2.4)
img.paste(Image.new('RGB', (W, H), (238, 178, 92)), (0, 0), gm.point(lambda v: int(v * .9)))
d = ImageDraw.Draw(img)
ring(215, 1105, 188, 1.2, CREAM)

def sheen(x, y, r):
    global img, d
    from PIL import ImageChops
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    md.ellipse([X(x - r * .75), Y(y - r * .8), X(x + r * .15), Y(y + r * .05)], fill=110)
    m = m.filter(ImageFilter.GaussianBlur(R(r * .25)))
    clip = Image.new('L', (W, H), 0); ImageDraw.Draw(clip).ellipse([X(x) - R(r), Y(y) - R(r), X(x) + R(r), Y(y) + R(r)], fill=255)
    m = ImageChops.multiply(m, clip)
    img.paste(Image.new('RGB', (W, H), (246, 222, 178)), (0, 0), m)
    d = ImageDraw.Draw(img)

def cymbal(x, y, r, holes=0, splash=0):
    circ(x, y, r, fill=BRONZE)
    for i in range(int(r // 9)):
        ring(x, y, r - i * 9, .8, mix(BRONZE, TAN, .5 if i % 4 == 0 else .25))
    ring(x, y, r, 2.4, TAN)
    if splash:
        circ(x - 30, y - 25, splash, fill=mix(BRONZE, TAN, .35)); ring(x - 30, y - 25, splash, 2, CREAM)
        for i in range(int(splash // 10)): ring(x - 30, y - 25, splash - i * 10, .7, mix(BRONZE, TAN, .55))
    for _ in range(int(r * 1.4)):  # hammer marks
        a = random.uniform(0, 2 * math.pi); rr = random.uniform(r * .2, r * .95)
        px, py = polar(x, y, rr, a)
        if holes and any(math.dist((px, py), polar(x, y, r * .72, 2 * math.pi * k / holes + .2)) < r * .13 for k in range(holes)): continue
        d.arc([X(px) - R(7), Y(py) - R(7), X(px) + R(7), Y(py) + R(7)], 200, 330, fill=mix(BRONZE, CREAM, .35), width=S)
    sheen(x, y, r)
    for k in range(holes):
        px, py = polar(x, y, r * .72, 2 * math.pi * k / holes + .2)
        circ(px, py, r * .1, fill=(16, 13, 11)); ring(px, py, r * .1, 1.2, TAN)
    circ(x - (30 if splash else 0), y - (25 if splash else 0), r * .17, fill=mix(BRONZE, TAN, .45))
    circ(x - (30 if splash else 0), y - (25 if splash else 0), 8, fill=CREAM)

cymbal(1530, 325, 385, splash=120)
cymbal(1655, 1035, 345, holes=8)

# brushes
for dx in (0, 22):
    d.line([X(1055 + dx), Y(1165), X(1175 + dx), Y(1265)], fill=(214, 176, 72), width=9 * S)
    for k in range(9):
        a = math.radians(38 + k * 3)
        d.line([X(1175 + dx), Y(1265), X(1175 + dx + 110 * math.cos(a)), Y(1265 + 110 * math.sin(a))], fill=dim(CREAM, .8), width=S)

# keep the drawing inside the rug and soften its edge into the page

# grain
noise = Image.effect_noise((W // 4, H // 4), 18).resize((W, H)).convert('L')
img = Image.blend(img, Image.merge('RGB', (noise, noise, noise)), 0.03)
d = ImageDraw.Draw(img)

def text_c(y, s, f, col, track=0):
    widths = [d.textlength(ch, font=f) for ch in s] if track else None
    if track:
        x = (W - (sum(widths) + track * S * (len(s) - 1))) / 2
        for ch, w in zip(s, widths):
            d.text((x, y * S), ch, font=f, fill=col); x += w + track * S
    else:
        d.text(((W - d.textlength(s, font=f)) / 2, y * S), s, font=f, fill=col)

text_c(150, 'NADAV FRIEDMAN', font('EBGaramond[wght].ttf', 34, 500), SOFT, track=9)
text_c(300, 'THE MIDDLE-EASTERN', font('CormorantGaramond[wght].ttf', 74, 500), TAN, track=7)
text_c(380, 'Drum Set', font('CormorantGaramond[wght].ttf', 230, 500), CREAM)
d.line([700 * S, 670 * S, 900 * S, 670 * S], fill=SOFT, width=S)
sub = font('EBGaramond-Italic[wght].ttf', 40, 400)
text_c(1930, 'Bringing the oral traditions of rhythm', sub, TAN)
text_c(1983, 'to the modern drum set', sub, TAN)
logo = Image.open(LOGO).convert('RGBA'); lh = 125 * S
logo = logo.resize((int(logo.width * lh / logo.height), lh), Image.LANCZOS)
img.paste(logo, ((W - logo.width) // 2, 2120 * S), logo)
d.rectangle([48 * S, 48 * S, W - 48 * S, H - 48 * S], outline=dim(TAN, .55), width=S)

img.resize((1600, 2400), Image.LANCZOS).save(OUT)
print('ok')
