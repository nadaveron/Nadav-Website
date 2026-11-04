"""A simplified riq (frame drum with jingles) drawn for tiny sizes: bold shapes, outlined so it reads on light and dark tab bars."""
import math, sys
from PIL import Image, ImageDraw

PALETTES = {
    # frame, head, jingle, outline
    'two-tone': ((86, 58, 34), (214, 186, 140), (232, 192, 92), (28, 20, 12)),
    'black':    ((17, 17, 17), (17, 17, 17), (17, 17, 17), (17, 17, 17)),
    'gold-outlined': ((200, 164, 126), (236, 222, 200), (226, 184, 80), (40, 28, 16)),
}

def riq(size, palette='two-tone', n=5):
    frame, head, jingle, ink = PALETTES[palette]
    S = 1024; c = S / 2
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R, J, JR = 330, 360, 108            # frame radius, jingle centre radius, jingle radius
    OW = 34                             # outline width
    def disc(x, y, r, fill, w=OW):
        d.ellipse([x - r, y - r, x + r, y + r], fill=ink); d.ellipse([x - r + w, y - r + w, x + r - w, y + r - w], fill=fill)
    for k in range(n):                  # jingles sit behind the frame and stick out past it
        a = -math.pi / 2 + 2 * math.pi * k / n
        disc(c + J * math.cos(a), c + J * math.sin(a), JR, jingle)
        d.ellipse([c + J * math.cos(a) - 22, c + J * math.sin(a) - 22, c + J * math.cos(a) + 22, c + J * math.sin(a) + 22], fill=ink)
    disc(c, c, R, frame)                # wooden frame
    disc(c, c, R - 78, head, w=28)      # skin head with its own rim line
    return im.resize((size, size), Image.LANCZOS)

if __name__ == '__main__':
    out = sys.argv[1]
    bars = [((255, 255, 255), 'white'), ((222, 225, 230), 'light tab'), ((53, 54, 58), 'dark tab'), ((0, 0, 0), 'black')]
    rows = list(PALETTES)
    sheet = Image.new('RGB', (len(bars) * 170, len(rows) * 70), (255, 255, 255))
    for ri, pal in enumerate(rows):
        for bi, (bg, _) in enumerate(bars):
            cell = Image.new('RGB', (170, 70), bg)
            x = 10
            for s in (16, 32, 48):
                ic = riq(s, pal); cell.paste(ic, (x, 35 - s // 2), ic); x += s + 12
            sheet.paste(cell, (bi * 170, ri * 70))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(out)
    print('rows:', rows)
