# Muse ― 1人1台のPCを持ったAI　ブリーフィング資料

Meta のパーソナルAIエージェント「Muse」（2026年9月8日 米国公開、10月23日 日本提供開始）を題材にした発表資料。対象別に2本ある。どちらもブラウザで開けばそのまま発表でき、`↓`/`PageDown` で送り、`N` キーで発表者ノートを表示する。外部リソースは読み込まないので、オフラインでも開ける。

| ファイル | 対象 | 枚数 | 時間 | 主張 |
|---|---|---|---|---|
| `engineer_muse_briefing.html` | エンジニア勉強会 | 13（うち1枚は参考） | 約18分＋質疑 | AIが「話し相手」から「自分のPCを持った代理人」になった。その作りは回し続けられるのか、OSに置き換えられないか |
| `exec_muse_briefing.html` | 役員 | 7 | 約5分 | 同じ主張を、論点2つ（コスト・居場所）に絞って |

## 構成（エンジニア版）

1. 表紙
2. 流行具合 ①　40日で1,000万DL（ChatGPT・Grok・Claude と比較）
3. 流行具合 ②　DAU推移・純増の鈍化・継続率・利用時間
4. できること ①　常駐・能動・記憶・承認
5. できること ②　VMの中で Claude Code を動かした例
6. 裏側　実測スペック（2 vCPU・約8GB・150GB）と構成図
7. 競合　dots・Grok Bot・Claude Code（クラウド）・Codex（クラウド）
8. 競合　OS勢（Siri AI・Gemini Intelligence・Windows Agent Workspace）
9. 仮説 ①　必要な計算資源の試算（同時稼働台数で約660倍変わる）
10. 仮説 ①　メモリ・CPU市況と Meta 自身の発言
11. 仮説 ②　アプリ型は OS 型に駆逐されるか
12. まとめ
13. 参考：自分で試した記録（**差し込み枠。未作成**）

構成の理由、試算の前提、言わないことにした点、出典の一覧は `engineer_briefing_outline.md` にまとめてある。

## 発表原稿

読み上げ用に、発表者ノートだけを切り出したテキストを置いてある。**手で編集せず、資料を直したら再生成すること。**

| ファイル | 対象 | 読み上げ時間 |
|---|---|---|
| `engineer_briefing_script.md` | エンジニア版 13ページ | 約18分15秒 |
| `exec_briefing_script.md` | 役員版 7ページ | 約5分5秒 |

```bash
uv run tools/extract_script.py engineer_muse_briefing.html engineer_briefing_script.md
uv run tools/extract_script.py exec_muse_briefing.html     exec_briefing_script.md
```

`*_backup.pdf` は表示が崩れた場合の保険（`node tools/export_pdf.mjs <html>` で再生成）。

## 自分で試した記録の差し込み方

エンジニア版の最後のページ（`id="s12"`）が差し込み枠になっている。

1. スクリーンショットや音声を `assets/` に置く
2. `<div class="slot">…</div>` を画像などに差し替え、見出しの〔ここに試した内容〕を書き換える
3. そのページの `data-note`（発表者ノート）を書き直し、発表原稿を再生成する

## 数値の扱い

- ダウンロード数・DAU・継続率は **調査会社の推計**（Sensor Tower・Similarweb・Apptopia・TickerTrends）。同じ時期の累計でも会社ごとにかなり差があるので、スライドにも出典を併記してある。
- Muse の **MAU（月間アクティブユーザー）は Meta も調査会社も公表していない**。代わりに DAU と継続率で比較している。
- VM のスペックは Qiita 記事の著者が1人の環境で実測した値（2026/10/26〜27）。公式報道は 2 vCPU・8GB・100GB。
- 9枚目の試算は概算。前提（1台 2 vCPU・8GB、サーバー1台に128台、平均値で計算）はスライドと構成メモに明記してある。
- メモリ・CPUの値上がりを **Muse のせいにはしていない**（主因は AI サーバー・HBM への生産振り替え）。

## 検証

レイアウト崩れの確認は、各 `<section>` を 1600×900 のヘッドレス Chrome でレンダリングして行う。

```bash
cd tools && npm install && npm run shots   # → tools/_screenshots/
```

Chrome の場所は `CHROME` 環境変数で指定できる（未指定なら macOS・Windows・Linux の既定パスを探す）。
