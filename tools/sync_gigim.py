"""Write public/assets/js/concerts.js from the Gigim calendar.

The Gigim calendar (iCloud) holds everything: concerts, recordings, rehearsals,
weddings, meetings. This keeps the public concerts only and turns them into the
site's English concert list, using the rules in gigs.json:

  exclude   words that mark an event as not a performance (recordings, meetings)
  private   words that mark a private show (weddings, corporate events): listed
            with the act and a general location only, noted "Private event"
  artists   Hebrew patterns that name the act -> English title and project
  places    Hebrew patterns -> English venue and/or city
  events    per-event overrides by calendar UID ("hide": true, or any field)
  extra     shows to list that are not in the calendar
  phrases   Hebrew and Spanish for recurring words ("Private event", "Album launch")

Any rule or override can carry "he" and "es" objects with translated fields, e.g.
{"match": "פילבית", "venue": "FeelBeit", "city": "Jerusalem", "he": {"venue": "פילבית", "city": "ירושלים"}}.
They become title_he, venue_es, ... in concerts.js; the site shows them on the Hebrew and Spanish pages.

An event is listed when it matches an artist (or has an override) and no
exclude word. Anything else that looks like it could be a gig is printed under
"needs a decision" so it can be added to gigs.json.

Usage:
  GIGIM_ICS_URL=https://... python3 tools/sync_gigim.py     # fetch live
  python3 tools/sync_gigim.py --ics gigim.ics                # from a file
The calendar link is private: keep it in an environment variable or secret,
never in the repository.
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("Asia/Jerusalem")


def read_calendar():
    if "--ics" in sys.argv:
        return Path(sys.argv[sys.argv.index("--ics") + 1]).read_text(encoding="utf-8")
    url = os.environ.get("GIGIM_ICS_URL", "").replace("webcal://", "https://")
    if not url:
        sys.exit("Set GIGIM_ICS_URL to the calendar's public link, or pass --ics FILE.")
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8")


def parse_ics(text):
    text = re.sub(r"\r?\n[ \t]", "", text)  # unfold long lines
    events, cur = [], None
    for line in text.splitlines():
        if line == "BEGIN:VEVENT":
            cur = {}
        elif line == "END:VEVENT":
            events.append(cur)
            cur = None
        elif cur is not None and ":" in line:
            key, value = line.split(":", 1)
            name, *params = key.split(";")
            value = value.replace("\\n", "\n").replace("\\,", ",").replace("\\;", ";")
            if name not in cur:
                cur[name] = value
                cur[name + "@"] = params
    return events


def local_date(event):
    """The event's date in Israel time (UTC and other zones are converted)."""
    raw, params = event.get("DTSTART", ""), event.get("DTSTART@", [])
    if len(raw) == 8:
        return dt.date(int(raw[:4]), int(raw[4:6]), int(raw[6:8]))
    stamp = dt.datetime.strptime(raw[:15], "%Y%m%dT%H%M%S")
    tzid = next((p[5:] for p in params if p.startswith("TZID=")), None)
    if raw.endswith("Z"):
        stamp = stamp.replace(tzinfo=dt.timezone.utc)
    elif tzid:
        stamp = stamp.replace(tzinfo=ZoneInfo(tzid))
    else:
        stamp = stamp.replace(tzinfo=TZ)
    return stamp.astimezone(TZ).date()


def first(rules, text, field):
    return pick(rules, text, field)[0]


def pick(rules, text, field):
    """The first rule that sets `field` and matches `text`: (English value, rule)."""
    for rule in rules:
        if field in rule and re.search(rule["match"], text):
            return rule[field], rule
    return "", {}


LANGS = ("he", "es")
FIELDS = ("title", "project", "venue", "city", "note")


def translate(gig, sources, phrases):
    """Adds title_he, venue_es, ... from the rules that produced each field, then from the phrase list.
    The site falls back to English where a translation is missing."""
    for lang in LANGS:
        for field in FIELDS:
            value = next((src.get(lang, {}).get(field) for src in sources.get(field, []) if src.get(lang, {}).get(field)), None)
            if value is None and gig[field] in phrases:
                value = phrases[gig[field]].get(lang)
            if value:
                gig[f"{field}_{lang}"] = value


def main():
    cfg = json.loads((ROOT / "gigs.json").read_text(encoding="utf-8"))
    today = dt.datetime.now(TZ).date()
    since = today - dt.timedelta(days=int(cfg.get("past_days", 183)))
    exclude = re.compile("|".join(cfg["exclude"]))
    private = re.compile("|".join(cfg["private"]))
    gigs, undecided, seen = [], [], set()

    for ev in parse_ics(read_calendar()):
        if "RRULE" in ev or "DTSTART" not in ev:
            continue
        day = local_date(ev)
        if day < since:
            continue
        summary = ev.get("SUMMARY", "").strip()
        text = summary + " " + ev.get("LOCATION", "")
        override = cfg["events"].get(ev.get("UID", ""), {})
        if override.get("hide"):
            continue
        title = first(cfg["artists"], summary, "title")
        is_private = bool(private.search(summary))
        if not override and (exclude.search(summary) or not (title or is_private)):
            if not exclude.search(summary):
                undecided.append(f"{day}  {summary}  [{ev.get('UID', '')}]")
            continue
        title_rule = pick(cfg["artists"], summary, "title")[1]
        venue, venue_rule = pick(cfg["places"], text, "venue")
        city, city_rule = pick(cfg["places"], text, "city")
        gig = {
            "date": day.isoformat(), "time": "",
            "title": title, "project": first(cfg["artists"], summary, "project"),
            "venue": venue, "city": city,
            "tickets": "", "info": "", "note": "",
        }
        sources = {"title": [override, title_rule], "project": [override, title_rule],
                   "venue": [override, venue_rule], "city": [override, city_rule], "note": [override]}
        if is_private:  # act and city only
            gig.update(title=title or "Private event", venue="", note="Private event" if title else "")
            sources["venue"] = [override]
            if not title:
                sources["title"] = [override]
        gig.update({k: v for k, v in override.items() if k in gig})
        translate(gig, sources, cfg.get("phrases", {}))
        key = (gig["date"], gig["title"], gig["venue"], gig["city"])
        if key in seen:  # the same show entered twice
            continue
        seen.add(key)
        gigs.append(gig)

    for extra in cfg.get("extra", []):
        if extra["date"] >= since.isoformat():
            gigs.append({"time": "", "project": "", "venue": "", "city": "", "tickets": "", "info": "", "note": "", **extra})

    gigs.sort(key=lambda g: g["date"], reverse=True)
    out = ROOT / "public/assets/js/concerts.js"
    head = out.read_text(encoding="utf-8").split("window.CONCERTS", 1)[0]
    body = json.dumps(gigs, ensure_ascii=False, indent=2)
    out.write_text(head + "window.CONCERTS = " + body + ";\n", encoding="utf-8")
    print(f"wrote {len(gigs)} concerts since {since} to {out.relative_to(ROOT)}")
    if undecided:
        print("\nneeds a decision (add an artist rule, or an override by UID in gigs.json):")
        print("\n".join(sorted(undecided)))


if __name__ == "__main__":
    main()
