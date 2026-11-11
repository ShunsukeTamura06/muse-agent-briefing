# Muse ― 1人1台のPCを持ったAI　ブリーフィング資料

Meta のパーソナルAIエージェント「Muse」（2026年9月8日 米国公開、10月23日 日本提供開始）を題材にした発表資料。対象別に2本ある。どちらもブラウザで開けばそのまま発表でき、`↓`/`PageDown` で送り、`N` キーで発表者ノートを表示する。外部リソースは読み込まないので、オフラインでも開ける。

| ファイル | 対象 | 枚数 | 時間 | 主張 |
|---|---|---|---|---|
| `engineer_muse_briefing.html` | エンジニア勉強会 | 14（うち1枚は参考） | 約20分＋質疑 | AIが「話し相手」から「自分のPCを持った代理人」になった。その作りは回し続けられるのか、OSに置き換えられないか |
| `exec_muse_briefing.html` | 役員 | 7 | 約5分 | 同じ主張を、論点2つ（コスト・居場所）に絞って |

## 構成（エンジニア版）

1. 表紙
2. 流行具合 ①　40日で1,000万DL（ChatGPT・Grok・Claude と比較）
3. 流行具合 ②　DAU推移・純増の鈍化・継続率・利用時間
4. できること ①　常駐・能動・記憶・承認（やり取りのイメージ図つき）
5. できること ②　VMの中で Claude Code を動かした例
6. 裏側　なぜクラウドに1台要るのか、実測スペック（2 vCPU・約8GB・150GB）と構成図
7. 他社動向　AIの稼働環境をクラウドに持たせるサービス（dots・Grok Bot・Claude Duet・Claude Code・Codex）
8. 仮説 ①　必要な計算資源の試算（控えめに見ても約12万台が同時に動く）
9. 仮説 ①　メモリ・CPUの需要増。常駐AIはその一因では？
10. 仮説 ②　Meta は先行投資を負っている（設備投資・無料・広告）
11. 仮説 ②　一方で OS 勢（Siri AI・Gemini Intelligence・Windows Agent Workspace）
12. 仮説 ②　アプリ型は OS 型に駆逐されないか。その時 Meta は？
13. まとめ
14. 参考：自分で試した記録（**差し込み枠。未作成**）

構成の理由、試算の前提、言わないことにした点、出典の一覧は `engineer_briefing_outline.md` にまとめてある。

## 発表原稿

読み上げ用に、発表者ノートだけを切り出したテキストを置いてある。**手で編集せず、資料を直したら再生成すること。**

| ファイル | 対象 | 読み上げ時間 |
|---|---|---|
| `engineer_briefing_script.md` | エンジニア版 14ページ | 約20分 |
| `exec_briefing_script.md` | 役員版 7ページ | 約5分半 |

```bash
uv run tools/extract_script.py engineer_muse_briefing.html engineer_briefing_script.md
uv run tools/extract_script.py exec_muse_briefing.html     exec_briefing_script.md
```

`*_backup.pdf` は表示が崩れた場合の保険（`node tools/export_pdf.mjs <html>` で再生成）。

## 自分で試した記録の差し込み方

エンジニア版の最後のページ（`id="s12"`、最後のページ）が差し込み枠になっている。

1. スクリーンショットや音声を `assets/` に置く
2. `<div class="slot">…</div>` を画像などに差し替え、見出しの〔ここに試した内容〕を書き換える
3. そのページの `data-note`（発表者ノート）を書き直し、発表原稿を再生成する

## 図について

「できること」のページにあるスマホ画面は、やり取りの流れを説明するための**イメージ図**（実際の Muse の画面ではない）。実物のスクリーンショットが手に入ったら差し替える。

## 数値の扱い

- ダウンロード数・DAU・継続率は **調査会社の推計**（Sensor Tower・Similarweb・Apptopia・TickerTrends）。同じ時期の累計でも会社ごとにかなり差があるので、スライドにも出典を併記してある。
- Muse の **MAU（月間アクティブユーザー）は Meta も調査会社も公表していない**。代わりに DAU と継続率で比較している。
- VM のスペックは Qiita 記事の著者が1人の環境で実測した値（2026/10/26〜27）。公式報道は 2 vCPU・8GB・100GB。
- 9枚目の試算は概算。前提（1台 2 vCPU・8GB、平均値で計算、稼働時間は仮定）はスライドと構成メモに明記してある。
- メモリ・CPUの値上がりを **Muse のせいにはしていない**（主因は AI サーバー・HBM への生産振り替え）。

## 検証

レイアウト崩れの確認は、各 `<section>` を 1600×900 のヘッドレス Chrome でレンダリングして行う。

```bash
cd tools && npm install && npm run shots   # → tools/_screenshots/
```

Chrome の場所は `CHROME` 環境変数で指定できる（未指定なら macOS・Windows・Linux の既定パスを探す）。
