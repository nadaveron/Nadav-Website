#!/usr/bin/env python3
"""Builds the classic-design site: src/pages/*.html + src/layout.html -> public/*.html.

Each page starts with a one-line JSON comment holding its title, description,
nav key and canonical path. Run `python3 build.py` after editing anything in
src/. Concert dates live in public/assets/js/concerts.js and need no rebuild.
"""
import hashlib
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
NAV = [("home", "index.html"), ("live", "live.html"), ("projects", "projects.html"), ("about", "about.html"),
       ("media", "media.html"), ("study", "study.html"), ("contact", "contact.html")]

SITE = "https://www.nadavfriedman.com"

# One entry per language. English is the main site at the root; the others live in /he/ and /es/,
# built from src/pages/<lang>/. The text here fills the {{t:...}} keys in src/layout.html.
LANGS = {
    "en": dict(dir="ltr", prefix="", label="EN", name="English", og_locale="en_US", fonts="",
        nav=dict(home="Home", live="Live", projects="Projects", about="About", media="Media", study="Study", contact="Contact"),
        skip="Skip to content", menu="Menu", menu_open="Open menu", nav_aria="Main", home_aria="Nadav Friedman, home",
        lang_aria="Language", job="Percussionist", name_full="Nadav Friedman",
        wa_updates="WhatsApp updates", wa_kicker="Nadav's WhatsApp group", wa_title="Shows worth leaving the house for",
        wa_text="Join to hear about Nadav's upcoming concerts and new productions first, along with his personal recommendations for boutique world-music concerts around Israel. A few messages a month, announcements only.",
        wa_join="Join the group", wa_qr_alt="QR code that opens the WhatsApp updates group", wa_scan="or scan it with your phone camera",
        roles="Percussionist · Composer · Educator", press="Press kit", play="Play music",
        track="Shalosh", track_sub="Zohar Fresco · drum set arrangement by Nadav"),
    "he": dict(dir="rtl", prefix="he/", label="עב", name="עברית", og_locale="he_IL", fonts="&family=Frank+Ruhl+Libre:wght@400;500;600",
        nav=dict(home="בית", live="הופעות", projects="פרויקטים", about="אודות", media="מדיה", study="לימוד", contact="צור קשר"),
        skip="דילוג לתוכן", menu="תפריט", menu_open="פתיחת התפריט", nav_aria="ראשי", home_aria="נדב פרידמן, דף הבית",
        lang_aria="שפה", job="נגן כלי הקשה", name_full="נדב פרידמן",
        wa_updates="עדכונים בוואטסאפ", wa_kicker="קבוצת הוואטסאפ של נדב", wa_title="הופעות ששווה לצאת מהבית בשבילן",
        wa_text="הצטרפו כדי לשמוע ראשונים על ההופעות וההפקות החדשות של נדב, יחד עם ההמלצות האישיות שלו להופעות בוטיק של מוזיקת עולם ברחבי הארץ. כמה הודעות בחודש, הודעות בלבד.",
        wa_join="הצטרפות לקבוצה", wa_qr_alt="קוד QR שפותח את קבוצת העדכונים בוואטסאפ", wa_scan="או סרקו אותו במצלמת הטלפון",
        roles="נגן כלי הקשה · מלחין · מורה", press="ערכת עיתונות", play="ניגון המוזיקה",
        track="שלוש", track_sub="זהר פרסקו · עיבוד למערכת תופים: נדב"),
    "es": dict(dir="ltr", prefix="es/", label="ES", name="Español", og_locale="es_ES", fonts="",
        nav=dict(home="Inicio", live="Conciertos", projects="Proyectos", about="Biografía", media="Multimedia", study="Clases", contact="Contacto"),
        skip="Saltar al contenido", menu="Menú", menu_open="Abrir el menú", nav_aria="Principal", home_aria="Nadav Friedman, inicio",
        lang_aria="Idioma", job="Percusionista", name_full="Nadav Friedman",
        wa_updates="Novedades por WhatsApp", wa_kicker="El grupo de WhatsApp de Nadav", wa_title="Conciertos que valen la pena",
        wa_text="Únete para enterarte antes que nadie de los próximos conciertos y las nuevas producciones de Nadav, junto con sus recomendaciones personales de conciertos boutique de músicas del mundo en Israel. Pocos mensajes al mes, solo anuncios.",
        wa_join="Unirse al grupo", wa_qr_alt="Código QR que abre el grupo de novedades en WhatsApp", wa_scan="o escanéalo con la cámara del teléfono",
        roles="Percusionista · Compositor · Educador", press="Dossier de prensa", play="Reproducir la música",
        track="Shalosh", track_sub="Zohar Fresco · arreglo para batería de Nadav"),
}


S = 'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
ICONS = [
    ("Instagram", "https://www.instagram.com/nadav.friedman/",
     f'<svg viewBox="0 0 24 24" {S}><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6" fill="currentColor"/></svg>'),
    ("Facebook", "https://www.facebook.com/nadav.friedman.5/",
     '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>'),
    ("YouTube", "https://www.youtube.com/@nadavfriedmanmusic",
     '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4a2.5 2.5 0 0 0-1.8 1.8C2 8.8 2 12 2 12s0 3.2.4 4.8a2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8c.4-1.6.4-4.8.4-4.8s0-3.2-.4-4.8zM10 15V9l5.2 3z"/></svg>'),
    ("Spotify", "https://open.spotify.com/artist/2chajUYdkxp1uYYrN9xVXb",
     f'<svg viewBox="0 0 24 24" {S}><circle cx="12" cy="12" r="9.5"/><path d="M7 9.3c3.4-1 7.2-.7 10.2 1M7.6 12.6c2.8-.8 5.8-.5 8.3.9M8.2 15.7c2.2-.6 4.4-.4 6.4.7"/></svg>'),
    ("Apple Music", "https://music.apple.com/artist/nadav-friedman/1515865116",
     f'<svg viewBox="0 0 24 24" {S}><path d="M9 18V5.5l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="15.5" r="2.5"/></svg>'),
    ("SoundCloud", "https://soundcloud.com/nadavfriedmanmusic",
     f'<svg viewBox="0 0 24 24" {S}><path d="M10 17V8.5a5 5 0 0 1 8.6 3.2A3 3 0 0 1 19.5 17zM7.5 17v-6M5 17v-4.5M2.5 17v-2.5"/></svg>'),
    ("Email", "mailto:nadaveron@gmail.com",
     f'<svg viewBox="0 0 24 24" {S}><rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>'),
]

ICON_SVG = {name.lower().replace(" ", ""): svg for name, _, svg in ICONS}
ICON_SVG["bandcamp"] = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 18 9.5 6H21l-6.5 12z"/></svg>'
ICON_SVG["play"] = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
ICON_SVG["doc"] = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14 3H6v18h12V7z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>'

def icons_html():
    external = ' target="_blank" rel="noopener"'
    return "".join(
        f'<a href="{href}" aria-label="{name}"{"" if href.startswith("mailto") else external}>{svg}</a>'
        for name, href, svg in ICONS)

def nav_html(active, lang):
    current = ' aria-current="page"'
    labels = LANGS[lang]["nav"]
    return "".join(f'<a href="{href}"{current if key == active else ""}>{labels[key]}</a>' for key, href in NAV)

def to_root(lang):
    """Relative way back to the site root from a page in this language."""
    return "../" if LANGS[lang]["prefix"] else ""

def page_href(from_lang, to_lang, name):
    target = "" if name == "index.html" else name
    return to_root(from_lang) + LANGS[to_lang]["prefix"] + target or "./"

def page_url(lang, path):
    return SITE + "/" + LANGS[lang]["prefix"] + path.lstrip("/")

def langs_html(lang, name, available):
    links = []
    for code in available:
        cur = ' aria-current="true"' if code == lang else ""
        links.append(f'<a href="{page_href(lang, code, name)}" lang="{code}" hreflang="{code}" title="{LANGS[code]["name"]}"{cur}>{LANGS[code]["label"]}</a>')
    return f'<nav class="langs" aria-label="{LANGS[lang]["lang_aria"]}">{"".join(links)}</nav>'

def alternates_html(path, available):
    out = [f'<link rel="alternate" hreflang="{code}" href="{page_url(code, path)}">' for code in available]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{page_url("en", path)}">')
    return "\n".join(out)

# Files browsers keep for hours: their links get ?v=<content hash>, so a changed file is fetched fresh.
VERSIONED = ["assets/css/site.css", "assets/js/site.js", "assets/js/concerts.js", "/favicon.ico",
             "assets/img/favicon-96.png", "assets/img/icon-192.png", "assets/img/apple-touch-icon.png"]

def fingerprint(html):
    for ref in VERSIONED:
        digest = hashlib.md5((ROOT / "public" / ref.lstrip("/")).read_bytes()).hexdigest()[:8]
        html = html.replace(f'"{ref}"', f'"{ref}?v={digest}"')
    return html

def source(lang, name):
    return ROOT / "src/pages" / (name if lang == "en" else f"{lang}/{name}")

def build():
    layout = (ROOT / "src/layout.html").read_text(encoding="utf-8")
    names = sorted(p.name for p in (ROOT / "src/pages").glob("*.html"))
    sitemap = []
    for name in names:
        available = [code for code in LANGS if source(code, name).exists()]
        for lang in available:
            L = LANGS[lang]
            raw = source(lang, name).read_text(encoding="utf-8")
            m = re.match(r"<!--\s*(\{.*?\})\s*-->\n", raw)
            meta = json.loads(m.group(1))
            html = (layout.replace("{{body}}", raw[m.end():].rstrip())  # first, so pages can use {{icons}} too
                          .replace("{{title}}", meta["title"])
                          .replace("{{description}}", meta["description"])
                          .replace("{{canonical}}", page_url(lang, meta["path"]))
                          .replace("{{alternates}}", "" if name == "404.html" else alternates_html(meta["path"], available))
                          .replace("{{lang}}", lang).replace("{{dir}}", L["dir"])
                          .replace("{{langs}}", langs_html(lang, name, available))
                          .replace("{{nav}}", nav_html(meta["nav"], lang))
                          .replace("{{icons}}", icons_html()))
            html = html.replace("{{t:name}}", L["name_full"])
            html = re.sub(r"\{\{t:([a-z_]+)\}\}", lambda mm: L[mm.group(1)], html)
            # Pages that already invite to the WhatsApp group can drop the closing band
            if meta.get("whatsapp", True):
                html = html.replace("<!--wa-->", "").replace("<!--/wa-->\n", "")
            else:
                html = re.sub(r"<!--wa-->.*?<!--/wa-->\n", "", html, flags=re.S)
            # {{icon:spotify}} etc. inside page bodies
            html = re.sub(r"\{\{icon:([a-z]+)\}\}", lambda mm: ICON_SVG[mm.group(1)], html)
            html = fingerprint(html)
            if L["prefix"]:  # pages in /he/ and /es/ reach the shared assets one level up
                html = re.sub(r'="assets/', '="../assets/', html)
            if name == "404.html":  # served at any missing address, so resolve links from the language root
                html = html.replace("<head>", f'<head>\n<base href="/{L["prefix"]}">', 1)
            out = ROOT / "public" / L["prefix"] / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print("built", L["prefix"] + name)
            if name != "404.html":
                sitemap.append((meta["path"], lang, available))
    urls = []
    for path, lang, available in sitemap:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{c}" href="{page_url(c, path)}"/>' for c in available)
        urls.append(f"  <url><loc>{page_url(lang, path)}</loc>{alts}</url>")
    (ROOT / "public/sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")

if __name__ == "__main__":
    build()
