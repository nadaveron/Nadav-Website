// Prints the profile sheets to PDF: node docs/press-kit/make_pdf.js (needs Playwright)
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [k, out] of [['en', 'Nadav-Friedman-Profile-EN.pdf'], ['he', 'Nadav-Friedman-Profile-HE.pdf']]) {
    await p.goto('file://' + path.resolve(__dirname, `profile-${k}.html`), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.resolve(__dirname, out), format: 'A4', printBackground: true, preferCSSPageSize: true });
  }
  await b.close(); console.log('ok');
})();
