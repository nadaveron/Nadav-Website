"""A riq (frame drum with jingles) drawn for small icons, after a real instrument and in the logo's palette:
the logo's own textured drum head, a thin bronze rim, five large hammered jingles in tan bronze, soft shadow."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S = 1024
C = S / 2

def radial(size, inner, outer, centre=(0.5, 0.5), radius=0.5):
    """An RGBA disc filled with a radial gradient from inner to outer colour."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); px = im.load()
    cx, cy = centre[0] * size, centre[1] * size; R = radius * size * 1.25
    for y in range(size):
        for x in range(size):
            t = min(1.0, math.hypot(x - cx, y - cy) / R)
            px[x, y] = tuple(int(inner[i] + (outer[i] - inner[i]) * t) for i in range(3)) + (255,)
    mask = Image.new('L', (size, size), 0); ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    im.putalpha(mask)
    return im

def jingle(r, seed, edge_w=None, bright=False):
    """A hammered brass jingle: warm gradient, dimples, a slightly darker edge."""
    d = 2 * r
    j = radial(d, (255, 236, 168) if bright else (246, 226, 186), (196, 150, 70) if bright else (150, 112, 66), centre=(0.38, 0.32))
    dr = ImageDraw.Draw(j); rnd = random.Random(seed)
    for _ in range(int(r * 0.45)):                   # hammer dimples: light and dark crescents
        a = rnd.uniform(0, 2 * math.pi); rr = r * math.sqrt(rnd.random()) * 0.9
        x, y = r + rr * math.cos(a), r + rr * math.sin(a); s = rnd.uniform(r * .06, r * .11)
        dr.arc([x - s, y - s, x + s, y + s], 200, 340, fill=(248, 232, 200, 110), width=max(2, int(s * .35)))
        dr.arc([x - s, y - s, x + s, y + s], 20, 160, fill=(110, 80, 46, 100), width=max(2, int(s * .35)))
    edge = Image.new('L', (d, d), 0); ImageDraw.Draw(edge).ellipse([0, 0, d - 1, d - 1], outline=255, width=edge_w or max(3, r // 7))
    j.paste((58, 40, 22, 255), (0, 0), edge)
    mask = Image.new('L', (d, d), 0); ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
    j.putalpha(ImageChops.multiply(j.split()[3], mask))
    return j

LOGO = 'public/assets/img/logo.webp'
TAB_GEOMETRY = (404, 414, 104)                     # frame radius, jingle centre radius, jingle radius at tab sizes

def logo_head(d, lift=1.0):
    """The drum head from the logo, cut as a disc: keeps the site's parchment texture and colour."""
    logo = Image.open(LOGO).convert('RGBA')
    head = logo.crop((215 - 74, 299 - 74, 215 + 74, 299 + 74)).resize((d, d), Image.LANCZOS)
    mask = Image.new('L', (d, d), 0); ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
    base = Image.new('RGBA', (d, d), (200, 168, 124, 255)); base.alpha_composite(head)
    if lift != 1.0:
        from PIL import ImageEnhance
        base = ImageEnhance.Brightness(base).enhance(lift)
    base.putalpha(mask)
    return base

def riq(size, n=5):
    art = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    small = size <= 48                             # tab sizes get bolder lines, brighter tones and a fuller frame
    px = S / size                                  # drawing units per screen pixel: outlines stay about one pixel wide
    k = (1.3, 0.9, 1.1) if size <= 16 else (1.9, 1.3, 1.4) if small else (0.9, 0.8, 0.75)
    edge_w = int(max(8, k[0] * px)); ring_w = int(max(10, k[1] * px)); jingle_w = int(max(4, k[2] * px))
    if small:                                      # tab sizes: a big drum, jingles standing well out from the rim
        FR, JC, JR = TAB_GEOMETRY
    else:
        FR, JC, JR = 384, 320, 130                 # frame radius, jingle centre radius, jingle radius: big jingles, tucked under the rim
    angles = [math.radians(-64 + k * 72) for k in range(n)]
    for k, a in enumerate(angles):                 # jingles behind the rim, sticking out past it
        jg = jingle(JR, k, jingle_w, bright=small)
        art.alpha_composite(jg, (int(C + JC * math.cos(a) - JR), int(C + JC * math.sin(a) - JR)))
    rim = radial(2 * FR, (230, 204, 160), (132, 98, 58), centre=(0.3, 0.25))           # warm bronze rim
    art.alpha_composite(rim, (int(C - FR), int(C - FR)))
    d = ImageDraw.Draw(art)
    d.ellipse([C - FR, C - FR, C + FR, C + FR], outline=(22, 15, 8, 255), width=edge_w)      # fine dark edge, like the logo's black gaps
    rim_w = 26                                                                            # visible bronze band of the rim
    inner = FR - edge_w - rim_w
    d.ellipse([C - inner, C - inner, C + inner, C + inner], fill=(30, 22, 14, 255))         # fine dark ring between rim and head
    HR = inner - ring_w
    head = logo_head(2 * HR, lift=1.18 if small else 1.0)                                 # the logo's textured skin
    art.alpha_composite(head, (int(C - HR), int(C - HR)))
    # soft shadow underneath, so the pale head still holds on white
    if small:                                      # no soft shadow at tab size: it only blurs the edge
        return art.resize((size, size), Image.LANCZOS)
    sh = art.split()[3].point(lambda v: int(v * .55)).filter(ImageFilter.GaussianBlur(26))
    shadow = Image.new('RGBA', (S, S), (40, 30, 20, 0)); shadow.putalpha(ImageChops.offset(sh, 0, 18))
    out = Image.alpha_composite(shadow, art)
    return out.resize((size, size), Image.LANCZOS)

if __name__ == '__main__':
    bars = [(245, 183, 200), (255, 255, 255), (222, 225, 230), (53, 54, 58)]
    sheet = Image.new('RGB', (len(bars) * 170, 70), (255, 255, 255))
    for bi, bg in enumerate(bars):
        cell = Image.new('RGB', (170, 70), bg); x = 10
        for s in (16, 32, 48):
            ic = riq(s); cell.paste(ic, (x, 35 - s // 2), ic); x += s + 12
        sheet.paste(cell, (bi * 170, 0))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(sys.argv[1])
    riq(512).save(sys.argv[1].replace('.png', '-512.png'))
