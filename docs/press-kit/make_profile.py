"""Builds the one-page profile sheet in English and Hebrew (HTML), ready to print to PDF.
Run from the repository root: python3 docs/press-kit/make_profile.py && node docs/press-kit/make_pdf.js"""
import io
from pathlib import Path
import qrcode, qrcode.image.svg

HERE = Path(__file__).parent

def qr_svg(url):
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=1)
    buf = io.BytesIO(); img.save(buf)
    svg = buf.getvalue().decode()
    return svg[svg.index('<svg'):].replace('fill="#000000"', 'fill="#1d1813"')

QR = qr_svg('https://www.nadavfriedman.com')

T = {
 'en': dict(
  lang='en', dir='ltr', font='"EB Garamond", Garamond, serif', head='"Cormorant Garamond", Garamond, serif',
  title='Nadav Friedman · Profile',
  name='Nadav Friedman', roles='Percussionist · Composer · Bandleader', tag='Traditions in Rhythm',
  intro='Israeli percussionist, composer and bandleader specializing in Middle Eastern percussion and drum set. '
        'He plays a setup of his own that joins darbuka, frame drums and riq with the modern kit, moving between the '
        'rhythms of the Middle East and North Africa, the Balkans, Persia and Latin America. He has recorded on more than 15 albums.',
  leads_h='Leads &amp; creates',
  leads=[('Bombaras', 'Balkan-Gypsy band · leader and manager'),
         ('Alma de Bata', 'Original percussion production, FeelBeit · supported by Mifal HaPais, invited to the Israel Festival'),
         ('Mirror', 'Original production, FeelBeit, 2026 · Jewish and Palestinian musicians in dialogue'),
         ('Playground Trio', 'Co-leader · album <i>A Sign of Life</i>'),
         ('Songs for Empathy', 'Debut album as leader, 2023')],
  with_h='Performs with',
  with_='Itai Armon Ensemble · Galilee Ensemble · Shimon Buskila · Rotem Cohen · David Lavi &amp; Tamar Philosof',
  studied_h='Has performed and studied with',
  studied='Danilo Pérez · Miguel Zenón · Donny McCaslin · Dave Holland · Jason Moran · Arturo O’Farrill',
  stages_h='Stages &amp; festivals',
  stages='Panama Jazz Festival · Jerusalem Jazz Festival · Jerusalem Oud Festival · Mekudeshet · Eilat Jazz Festival · '
         'Symphony Hall &amp; Jordan Hall, Boston · Rockwood Music Hall, New York · FeelBeit · Confederation House · Barby · Zappa',
  watch_h='Watch &amp; listen',
  watch=[('Bombaras · Madhavski Horo', 'youtu.be/-KSV1RNNoXE'), ('Itai Armon · Saudi Groove', 'youtu.be/0I3hOZ31R6U'),
         ('Songs for Empathy · De Amor', 'youtu.be/IKtzq0QI3gE'), ('Solo drum set · Shalosh', 'youtu.be/frRXGKoVng0')],
  also='Also: head of the percussion department at the Kiryat Ono Conservatory · masterclasses · author of the method <i>The Middle-Eastern Drum Set</i>.',
  contact_h='Booking &amp; contact', phone='+972 54-499-1332', qr='Scan for videos, concerts and contact'),
 'he': dict(
  lang='he', dir='rtl', font='"Frank Ruhl Libre", "EB Garamond", serif', head='"Frank Ruhl Libre", serif',
  title='נדב פרידמן · פרופיל',
  name='נדב פרידמן', roles='נגן כלי הקשה · מלחין · מוביל הרכבים', tag='Traditions in Rhythm',
  intro='נגן כלי הקשה, מלחין ומוביל הרכבים, המתמחה בכלי הקשה מהמזרח התיכון ובמערכת תופים. '
        'מנגן על סט ייחודי שבנה, המשלב דרבוקה, תופי מסגרת וריק עם מערכת תופים מודרנית, ונע בין מקצבי המזרח התיכון '
        'וצפון אפריקה, הבלקן, פרס ואמריקה הלטינית. הקליט כלי הקשה ליותר מ-15 אלבומים.',
  leads_h='מוביל ויוצר',
  leads=[('בומבראס', 'להקת בלקן-צוענית · מוביל ומנהל'),
         ('אלמה דה באטה – נשמת התוף', 'מופע כלי הקשה מקורי, פילבית · בתמיכת מפעל הפיס, הוזמן לפסטיבל ישראל'),
         ('מראה', 'מופע מקורי, פילבית, 2026 · מפגש בין מוזיקאים יהודים ופלסטינים'),
         ('Playground Trio', 'מוביל שותף · האלבום <i>A Sign of Life</i>'),
         ('Songs for Empathy', 'אלבום בכורה כמוביל, 2023')],
  with_h='מופיע עם',
  with_='האנסמבל של איתי ארמון · אנסמבל גליל · שמעון בוסקילה · רותם כהן · דוד לביא ותמר פילוסוף',
  studied_h='הופיע ולמד עם',
  studied='דנילו פרז · מיגל זנון · דוני מקאסלין · דייב הולנד · ג׳ייסון מורן · ארתורו או׳פריל',
  stages_h='במות ופסטיבלים',
  stages='פסטיבל הג׳אז בפנמה · פסטיבל הג׳אז ירושלים · פסטיבל העוד · מקודשת · פסטיבל הג׳אז אילת · '
         'סימפוני הול וג׳ורדן הול, בוסטון · רוקווד, ניו יורק · פילבית · בית הקונפדרציה · בארבי · זאפה',
  watch_h='לצפייה ולהאזנה',
  watch=[('בומבראס · Madhavski Horo', 'youtu.be/-KSV1RNNoXE'), ('איתי ארמון · Saudi Groove', 'youtu.be/0I3hOZ31R6U'),
         ('Songs for Empathy · De Amor', 'youtu.be/IKtzq0QI3gE'), ('מערכת תופים סולו · שלוש', 'youtu.be/frRXGKoVng0')],
  also='גם: ראש מחלקת כלי ההקשה בקונסרבטוריון קריית אונו · כיתות אמן · מחבר שיטת הלימוד <i>The Middle-Eastern Drum Set</i>.',
  contact_h='הזמנות ויצירת קשר', phone='054-499-1332', qr='סרטונים, הופעות ויצירת קשר'),
}

CSS = '''
@font-face { font-family: "Cormorant Garamond"; src: url("../../design/fonts/CormorantGaramond[wght].ttf"); font-weight: 300 700; }
@font-face { font-family: "EB Garamond"; src: url("../../design/fonts/EBGaramond[wght].ttf"); font-weight: 400 800; }
@font-face { font-family: "EB Garamond"; src: url("../../design/fonts/EBGaramond-Italic[wght].ttf"); font-weight: 400 800; font-style: italic; }
@font-face { font-family: "Frank Ruhl Libre"; src: url("../../design/fonts/FrankRuhlLibre[wght].ttf"); font-weight: 300 900; }
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; width: 210mm; height: 297mm; overflow: hidden; color: #1d1813; font-size: 10.3pt; line-height: 1.42; background: #fbf7f0; }
.band { position: relative; height: 92mm; background: #000; color: #c8a47e; overflow: hidden; }
.band img.photo { position: absolute; top: 0; height: 100%; width: 62%; object-fit: cover; object-position: 70% 35%;
  -webkit-mask-image: linear-gradient(var(--fade), transparent 0%, #000 38%); }
.band .title { position: absolute; top: 20mm; width: 60%; padding: 0 16mm; }
.band h1 { margin: 0; font-weight: 500; font-size: 40pt; line-height: 1; color: #c8a47e; }
.band .roles { margin-top: 5mm; font-size: 12.5pt; letter-spacing: .06em; color: #eadccb; }
.band .tag { margin-top: 2mm; font-family: "Cormorant Garamond", serif; font-style: italic; font-size: 14pt; color: #a88c6c; }
.band img.mark { position: absolute; bottom: 7mm; width: 13mm; }
main { padding: 8mm 16mm 0; }
.intro { font-size: 11.6pt; line-height: 1.5; margin: 0 0 5mm; }
.grid { display: grid; grid-template-columns: 1.05fr 1fr; gap: 0 10mm; }
h2 { font-weight: 600; font-size: 9pt; letter-spacing: .14em; text-transform: uppercase; color: #8c6a45; margin: 0 0 2mm;
  padding-bottom: 1.2mm; border-bottom: 1px solid #d9c9b3; }
.sec { margin-bottom: 4.6mm; }
.lead-item { margin: 0 0 2.1mm; }
.lead-item b { font-size: 11.6pt; font-weight: 600; }
.lead-item span { display: block; color: #6b5a48; font-size: 9.6pt; line-height: 1.32; }
.list { margin: 0; color: #2c241c; }
.watch { display: grid; gap: 1.2mm; }
.watch div { display: flex; justify-content: space-between; gap: 4mm; border-bottom: 1px dotted #d9c9b3; padding-bottom: .8mm; }
.watch .u { color: #8c6a45; font-size: 9.4pt; direction: ltr; unicode-bidi: isolate; }
.also { margin: 1mm 0 0; font-size: 9.4pt; color: #6b5a48; font-style: italic; }
footer { position: absolute; bottom: 0; left: 0; right: 0; height: 30mm; background: #0d0b09; color: #eadccb;
  display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 8mm; padding: 0 16mm; }
footer h2 { color: #c8a47e; border: 0; padding: 0; margin: 0 0 1.5mm; }
footer .lines { font-size: 10.4pt; line-height: 1.55; }
footer .lines .ltr { direction: ltr; unicode-bidi: isolate; }
footer .qr { display: flex; align-items: center; gap: 3.5mm; }
footer .qr .code { width: 21mm; height: 21mm; background: #f1e6d4; padding: 1.2mm; border-radius: 1.5mm; }
footer .qr .code svg { width: 100%; height: 100%; display: block; }
footer .qr small { width: 26mm; font-size: 8.6pt; color: #a88c6c; line-height: 1.3; }
'''

def page(t):
    rtl = t['dir'] == 'rtl'
    side = 'left' if rtl else 'right'          # the photo sits on the far side from the text
    other = 'right' if rtl else 'left'
    fade = 'to left' if not rtl else 'to right'
    leads = ''.join(f'<p class="lead-item"><b>{a}</b><span>{b}</span></p>' for a, b in t['leads'])
    watch = ''.join(f'<div><span>{a}</span><span class="u">{u}</span></div>' for a, u in t['watch'])
    return f'''<!doctype html>
<html lang="{t['lang']}" dir="{t['dir']}"><head><meta charset="utf-8"><title>{t['title']}</title>
<style>{CSS}
body {{ font-family: {t['font']}; }}
.band h1 {{ font-family: {t['head']}; }}
.band img.photo {{ {side}: 0; --fade: {fade}; -webkit-mask-image: linear-gradient({fade}, transparent 0%, #000 38%); mask-image: linear-gradient({fade}, transparent 0%, #000 38%); }}
.band .title {{ {other}: 0; }}
.band img.mark {{ {other}: 16mm; }}
{'h2 { letter-spacing: 0; font-size: 10.6pt; } .band .roles { letter-spacing: 0; }' if rtl else ''}
</style></head>
<body>
<section class="band">
  <img class="photo" src="../../public/assets/photos/hero-cloth-black.jpg" alt="">
  <div class="title"><h1>{t['name']}</h1><div class="roles">{t['roles']}</div><div class="tag">{t['tag']}</div></div>
  <img class="mark" src="../../public/assets/img/logo.webp" alt="">
</section>
<main>
  <p class="intro">{t['intro']}</p>
  <div class="grid">
    <div>
      <div class="sec"><h2>{t['leads_h']}</h2>{leads}</div>
    </div>
    <div>
      <div class="sec"><h2>{t['with_h']}</h2><p class="list">{t['with_']}</p></div>
      <div class="sec"><h2>{t['studied_h']}</h2><p class="list">{t['studied']}</p></div>
      <div class="sec"><h2>{t['stages_h']}</h2><p class="list">{t['stages']}</p></div>
    </div>
  </div>
  <div class="sec"><h2>{t['watch_h']}</h2><div class="watch">{watch}</div></div>
  <p class="also">{t['also']}</p>
</main>
<footer>
  <div><h2>{t['contact_h']}</h2>
    <div class="lines"><span class="ltr">nadaveron@gmail.com</span> · <span class="ltr">{t['phone']}</span><br>
    <span class="ltr">www.nadavfriedman.com</span> · <span class="ltr">Instagram @nadav.friedman</span></div></div>
  <div class="qr"><div class="code">{QR}</div><small>{t['qr']}</small></div>
</footer>
</body></html>'''

for key, t in T.items():
    (HERE / f'profile-{key}.html').write_text(page(t), encoding='utf-8')
print('ok')
