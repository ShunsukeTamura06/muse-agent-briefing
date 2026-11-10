// 資料のHTMLから、表示が崩れたとき用のバックアップPDFを書き出す。
// バーの伸び・カウントアップは IntersectionObserver 依存で印刷時に発火しないため、
// 最終値に揃えてから出力する（印刷用CSSでもバーの幅は固定してある）。
// 実行（プロジェクトルートから）:
//   node tools/export_pdf.mjs exec_muse_briefing.html
//   → exec_muse_briefing_backup.pdf
// Chrome の場所は CHROME 環境変数で上書きできる。
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const deck = process.argv[2] || 'exec_muse_briefing.html';
const out = path.join(root, path.basename(deck, '.html') + '_backup.pdf');

const candidates = [
  process.env.CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome',
].filter(Boolean);
const executablePath = candidates.find((p) => fs.existsSync(p));

const b = await chromium.launch(executablePath ? { executablePath } : {});
const p = await b.newPage();
await p.goto('file://' + path.join(root, deck));
await p.emulateMedia({ media: 'print' });

await p.evaluate(() => {
  document.querySelectorAll('[data-count-to]').forEach((el) => {
    const dec = parseInt(el.getAttribute('data-decimals') || '0', 10);
    el.textContent = parseFloat(el.getAttribute('data-count-to')).toFixed(dec);
    el.dataset.counted = '1';
  });
  document.querySelectorAll('section').forEach((s) => s.classList.add('in'));
});
await p.waitForTimeout(1200);

await p.pdf({
  path: out,
  width: '1600px',
  height: '900px',
  printBackground: true,
  margin: { top: '0', bottom: '0', left: '0', right: '0' },
});
await b.close();
console.log('pdf ok ->', out);
