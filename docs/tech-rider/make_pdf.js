// Prints tech-rider.html to PDF: node docs/tech-rider/make_pdf.js (needs Playwright)
const path = require('path');
const { chromium } = require(process.env.PLAYWRIGHT || 'playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, 'tech-rider.html'), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: path.resolve(__dirname, 'Nadav-Friedman-Tech-Rider.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
  console.log('ok');
})();
