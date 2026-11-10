// 全スライドを 1600×900 の PNG にして、レイアウト崩れを目視確認する。
// 実行（プロジェクトルートから）:
//   node tools/render_screenshots.mjs engineer_muse_briefing.html
//   node tools/render_screenshots.mjs exec_muse_briefing.html
// Chrome の場所は CHROME 環境変数で上書きできる（未指定なら OS ごとの既定パスを探す）。
import { chromium } from 'playwright';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const deck = process.argv[2] || 'engineer_muse_briefing.html';
const outDir = path.join(root, 'tools', '_screenshots', path.basename(deck, '.html'));
fs.mkdirSync(outDir, { recursive: true });

const candidates = [
  process.env.CHROME,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  '/usr/bin/google-chrome',
].filter(Boolean);
const executablePath = candidates.find((p) => fs.existsSync(p));

const b = await chromium.launch(executablePath ? { executablePath } : {});
const p = await b.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
await p.goto('file://' + path.join(root, deck));
await p.waitForTimeout(600);

const n = await p.locator('section').count();
const overflow = [];
for (let i = 0; i < n; i++) {
  await p.evaluate(
    (idx) => document.querySelectorAll('section')[idx].scrollIntoView({ behavior: 'instant', block: 'start' }),
    i
  );
  await p.waitForTimeout(1500); // バーの伸び・カウントアップが落ち着くのを待つ
  await p.screenshot({ path: path.join(outDir, `s${String(i).padStart(2, '0')}.png`) });
  // 中身が 1 画面に収まっているか（section は overflow:hidden なので、はみ出しは見えなくなる）
  const over = await p.evaluate((idx) => {
    const s = document.querySelectorAll('section')[idx];
    const w = s.querySelector('.wrap') || s;
    return Math.round(w.getBoundingClientRect().height - s.clientHeight);
  }, i);
  if (over > -10) overflow.push(`s${i}: 余白 ${-over}px`);
}
console.log('sections:', n, '-> saved to', outDir);
if (overflow.length) console.log('はみ出し・余白不足:', overflow.join(', '));
await b.close();
