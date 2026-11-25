#!/usr/bin/env python3
"""src/ の Claude Slides ソースから、ブラウザで単体で開ける発表用HTMLを作る。

実行（このフォルダで）:
    python3 build.py
    → trust_boundary_briefing.html

外部ライブラリは使わない。フォントは Google Fonts を読みに行き、
オフラインなら手元の日本語フォントで表示される。
矢印（x-shape）は「→」の文字で代用している。
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
OUT = HERE / "trust_boundary_briefing.html"

BASE_CSS = """
* { margin: 0 }
body { font: 32px/1.2 sans-serif }
section { width: 1920px; height: 1080px; overflow: hidden; box-sizing: border-box; position: relative; isolation: isolate }
h1 { font-size: 96px; font-weight: 600 } h2 { font-size: 64px; font-weight: 600 } h3 { font-size: 44px; font-weight: 600 }
p, li, h1, h2, h3, td, th { overflow-wrap: break-word; text-wrap: pretty }
table { width: 100%; border-collapse: separate; border-spacing: 0; border: solid #0003; border-width: 2px 0 0 2px }
th, td { padding: .35em .6em; text-align: left; border: solid #0003; border-width: 0 2px 2px 0 }
x-shape, x-icon { display: block } x-connector { display: block; position: absolute }
"""

STANDALONE_CSS = """
body, section { font-family: 'IBM Plex Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', 'Yu Gothic', sans-serif }
x-shape.arrow { background: none !important; width: auto !important; height: auto !important;
  display: flex; align-items: center; justify-content: center; min-width: 64px }
x-shape.arrow::before { content: "\\2192"; font-size: 56px; line-height: 1; color: #8A949E }
x-shape.arrow.sm::before { font-size: 36px }
.pageno::before { content: none !important }

/* 画面表示：1枚ずつ、ウィンドウに合わせて拡大縮小 */
html, body { height: 100%; background: #0d141b; overflow: hidden }
.stage { position: fixed; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: 0 0 }
.stage > section[hidden] { display: none !important }
.help { position: fixed; right: 16px; bottom: 12px; font: 14px sans-serif; color: #8a96a3 }

/* 印刷・PDF：全ページを1枚ずつ */
@page { size: 1920px 1080px; margin: 0 }
@media print {
  html, body { height: auto; overflow: visible; background: none }
  .stage { position: static; transform: none !important; width: auto; height: auto }
  .stage > section, .stage > section[hidden] { display: flex !important; break-after: page }
  .help { display: none }
}
"""

SCRIPT = """
(function () {
  // x-connector（図の線）を SVG に置き換える。座標は親要素の左上からの px。
  var NS = 'http://www.w3.org/2000/svg';
  Array.prototype.slice.call(document.querySelectorAll('x-connector[x1]')).forEach(function (c) {
    var g = function (k) { return parseFloat(c.getAttribute(k)); };
    var x1 = g('x1'), y1 = g('y1'), x2 = g('x2'), y2 = g('y2');
    var cs = getComputedStyle(c), col = cs.color, w = parseFloat(cs.borderTopWidth) || 2;
    var dash = cs.borderTopStyle === 'dashed';
    var route = c.getAttribute('route') || 'straight', head = c.getAttribute('head') || 'end';
    var pts = [[x1, y1], [x2, y2]];
    if (route === 'hv') pts = [[x1, y1], [x2, y1], [x2, y2]];
    if (route === 'vh') pts = [[x1, y1], [x1, y2], [x2, y2]];
    var svg = document.createElementNS(NS, 'svg');
    svg.style.cssText = 'position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible;pointer-events:none';
    var pl = document.createElementNS(NS, 'polyline');
    pl.setAttribute('points', pts.map(function (p) { return p.join(','); }).join(' '));
    pl.setAttribute('fill', 'none'); pl.setAttribute('stroke', col); pl.setAttribute('stroke-width', w);
    if (dash) pl.setAttribute('stroke-dasharray', (3 * w) + ' ' + (2 * w));
    svg.appendChild(pl);
    var addHead = function (a, b) {
      var ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = 4 * w, W = 2.2 * w;
      var bx = b[0] - L * Math.cos(ang), by = b[1] - L * Math.sin(ang);
      var p = document.createElementNS(NS, 'polygon');
      p.setAttribute('points', [b[0] + ',' + b[1], (bx + W * Math.sin(ang)) + ',' + (by - W * Math.cos(ang)), (bx - W * Math.sin(ang)) + ',' + (by + W * Math.cos(ang))].join(' '));
      p.setAttribute('fill', col); svg.appendChild(p);
    };
    if (head === 'end' || head === 'both') addHead(pts[pts.length - 2], pts[pts.length - 1]);
    if (head === 'both') addHead(pts[1], pts[0]);
    c.replaceWith(svg);
  });

  var stage = document.querySelector('.stage');
  var slides = Array.prototype.slice.call(stage.children);
  var cur = 0;
  function fit() {
    var s = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    stage.style.transform = 'scale(' + s + ') translate(-50%, -50%)';
  }
  function go(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (el, k) { el.hidden = k !== cur; });
    history.replaceState(null, '', '#' + (cur + 1));
  }
  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ') { e.preventDefault(); go(cur + 1); }
    else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') { e.preventDefault(); go(cur - 1); }
    else if (k === 'Home') { go(0); } else if (k === 'End') { go(slides.length - 1); }
  });
  document.addEventListener('click', function () { go(cur + 1); });
  window.addEventListener('resize', fit);
  fit();
  go((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
"""


def main():
    deck = json.loads((SRC / "deck.json").read_text(encoding="utf-8"))
    deck_css = (SRC / "deck.css").read_text(encoding="utf-8")
    fonts = "\n".join(
        f'<link rel="stylesheet" href="{f["href"]}">' for f in deck.get("faces", {}).values()
    )
    sections = []
    for n, sid in enumerate(deck["order"], start=1):
        html = (SRC / "slides" / f"{sid}.html").read_text(encoding="utf-8").strip()
        html = re.sub(r'<p class="pageno"></p>', f'<p class="pageno">{n}</p>', html)
        sections.append(html)
    title = deck.get("title", "slides")
    out = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{fonts}
<style>{BASE_CSS}
{deck_css}
{STANDALONE_CSS}</style>
</head>
<body>
<div class="stage">
{chr(10).join(sections)}
</div>
<div class="help">→ / ↓ / PageDown / クリックで次へ　← / ↑ / PageUp で前へ</div>
<script>{SCRIPT}</script>
</body>
</html>
"""
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.name} ({len(deck['order'])} slides)")


if __name__ == "__main__":
    main()
