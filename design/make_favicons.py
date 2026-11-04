"""Writes the browser-tab and search icons (run from the repository root).
Small sizes use the simplified riq from riq_icon.py, which stays clear on light and dark tab bars;
the home-screen icons keep the full logo."""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
sys.path.insert(0, str(Path(__file__).parent))
from riq_icon import riq

P = Path('public')
riq(48).save(P / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)], append_images=[riq(16), riq(32)])
riq(48).save(P / 'assets/img/favicon.png', optimize=True)
riq(96).save(P / 'assets/img/favicon-96.png', optimize=True)
riq(192).save(P / 'assets/img/icon-192.png', optimize=True)

logo = Image.open(P / 'assets/img/logo.webp').convert('RGBA')
cut = ImageEnhance.Brightness(logo.convert('RGB')).enhance(1.05).convert('RGBA'); cut.putalpha(logo.split()[3])
wide = cut.crop((10, 88, 420, 498))
wide.resize((512, 512), Image.LANCZOS).save(P / 'assets/img/icon-512.png', optimize=True)
bg = Image.new('RGBA', (180, 180), (0, 0, 0, 255)); bg.alpha_composite(wide.resize((180, 180), Image.LANCZOS))
bg.convert('RGB').save(P / 'assets/img/apple-touch-icon.png', optimize=True)
print('icons written')
