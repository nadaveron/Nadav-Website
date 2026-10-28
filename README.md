# nadavfriedman.com

Nadav Friedman's website, built to replace the Squarespace site. No framework
and no monthly fee: plain HTML, CSS and a little JavaScript, in the look of the
original site (black ground, tan type, Cormorant Garamond and Garamond, pill
buttons, centred logo).

## Layout

```
build.py            assembles src/ into public/
src/layout.html     shared header, WhatsApp band, footer, floating player
src/pages/*.html    page content (first line = title, description, nav)
public/             the deployable site (this folder goes online)
  assets/js/concerts.js   concert list, generated from the Gigim calendar
  assets/js/site.js       concert list, videos, player, contact form
  assets/css/site.css
  _redirects              /whatsapp short link + old Squarespace URLs
gigs.json           rules for turning calendar entries into concerts
tools/sync_gigim.py reads the Gigim calendar and writes concerts.js
.github/workflows/sync-gigs.yml   runs the sync every morning
```

Pages: Home · Live · Projects · About · Media · Study · Contact.

## Everyday updates

- **Concerts** come from the Gigim calendar. A GitHub Action runs every morning,
  reads the calendar and commits `concerts.js` when something changed (it can
  also be run by hand from the Actions tab). It needs the repository secret
  `GIGIM_ICS_URL`: the calendar's public iCloud link. Keep that link out of
  the code, because the calendar also holds private entries.
- **Which calendar entries appear** is decided in `gigs.json`: words that mark
  non-performances (recordings, rehearsals, meetings), private shows (listed
  with the act and city only), English names for acts and venues, and
  per-event overrides such as ticket links. Entries the sync cannot place are
  printed in the Action's log under "needs a decision".
- **Page text:** edit `src/pages/<page>.html`, then run `python3 build.py`.

To run the sync locally: `GIGIM_ICS_URL=... python3 tools/sync_gigim.py`.

## Going live (Cloudflare Pages, free)

1. Cloudflare dashboard → Workers & Pages → Create → Pages → connect this repository.
2. Build command: `python3 build.py` · Output directory: `public`.
3. Custom domains → add `nadavfriedman.com` and `www.nadavfriedman.com`, and follow the
   DNS steps. If the domain is registered at Squarespace, either point its DNS at
   Cloudflare or transfer the domain. Keep any email records (MX) as they are.
4. Cancel the Squarespace site plan only after the new site is live on the domain.

## Contact form

Until a form service is connected, the form opens the visitor's email app. To receive
messages directly, create a free form at formspree.io and put its endpoint URL in
`FORM_ENDPOINT` at the top of `public/assets/js/site.js`.
