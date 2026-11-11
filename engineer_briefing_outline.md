# engineer_muse_briefing.html 構成メモ（エンジニア勉強会・約20分）

## 主題

**主役は Meta の Muse。** 「流行っている」で終わらせず、**1人1台のクラウドPCを配る**という作りが何を意味するかまで読む。

背骨は1本：**AIが「話し相手」から「自分のPCを持った代理人」になった。** 流行具合（1〜2）→ できること（3〜4）→ 裏側（5）→ 他社とOS勢（6〜7）→ 仮説（8〜10）の順に、この1本を外さない。

役員版との違いは「何を話すか」ではなく「どこまで踏み込むか」：

| | 役員版 | エンジニア版 |
|---|---|---|
| 流行具合 | 40日で1,000万DL、史上12本目 | ＋DAUの推移、純増の鈍化、継続率は調査会社で評価が割れる |
| できること | 閉じても働く・自分から提案・承認制 | ＋VMの中でClaude Codeを動かした実例 |
| 裏側 | 1人1台、2コア・8GB | ＋実測スペック表、Sentinel、Tailscale、ルート7.5GB |
| 競合 | 各社が同じ方向へ | ＋各社VMの公開スペックと止まり方の違い |
| 仮説 | 結論の方向だけ | ＋試算の前提を開く（控えめに見ても約12万台が同時稼働） |

## 構成（13枚 ／ 本編12枚・約19分＋質疑、参考1枚）

| # | スライド | 時間 | 役割 |
|---|---|---|---|
| 1 | 表紙 | 0:25 | 扱う範囲を1文で |
| 2 | 40日で1,000万DL | 1:20 | 立ち上がりの速さ。ChatGPT・Grok・Claude と比較 |
| 3 | 伸びは鈍化、定着は健闘 | 1:50 | DAU推移・純増ペース・継続率・利用時間。**広告の力も正直に出す** |
| 4 | 閉じても働く・自分から動く | 1:30 | 常駐・能動・記憶・承認 |
| 5 | 中でClaude Codeが動く | 1:20 | 仮想環境で実験・開発できる実例（Qiita記事） |
| 6 | 中身はただのUbuntu | 2:00 | 実測スペックと構成図。**「1人1台」を体感させる** |
| 7 | 他社も「AIに1台」へ | 1:50 | dots・Grok Bot・Claude Code・Codex |
| 8 | OSも代理人になり始めた | 1:20 | Siri AI・Gemini Intelligence・Windows Agent Workspace |
| 9 | 仮説1　どれだけの計算資源か | 2:10 | 試算。節約しても十万台規模が同時に動く |
| 10 | 仮説1　市況のシグナル | 1:40 | メモリ・CPU価格、Metaの発言。**因果は主張しない** |
| 11 | 仮説2　OSに駆逐されるか | 1:50 | OS型とクラウドVM型の強みを対置して問いで終わる |
| 12 | まとめ | 1:00 | 問い2つを持ち帰ってもらう |
| 13 | 参考：自分で試した記録 | 任意 | **差し込み枠。素材を受け取ったら差し替える** |

## 仮説1の試算（9枚目）

前提：登録者 **1,000万人**（Meta、10/21決算説明会、米加）、米国アプリDAU **約290万人**（Similarweb、10/17）、VM **2 vCPU・8GB**（Qiita実測 7.7GiB・公式報道 8GB）。

| シナリオ | 同時に動くPC | CPU | メモリ |
|---|---|---|---|
| A 登録者全員が常時稼働 | 1,000万台 | 2,000万コア | 80 PB |
| B DAU分が常時稼働 | 290万台 | 580万コア | 23 PB |
| C DAUが1日3時間ずつ（仮定） | 約36万台 | 72万コア | 2.9 PB |
| D DAUが1日1時間ずつ（控えめな仮定） | 約12万台 | 24万コア | 約1 PB |

見せ方の方針（11/11 見直し）：

- **サーバー台数に換算しない。** 1台に128VM詰める仮定で割ると数字が1/128になり、規模感が伝わらない。「同時に動くPCの台数・コア・メモリ」で見せる。サーバー換算（A 約7.8万台〜D 約940台）は質疑用ノートにだけ残す。
- **「アプリを触る7.5分だけ稼働」のシナリオは外した。** 7.5分は画面を開いている時間で、Muse は閉じた後も働き、能動的に提案し、予約タスクも実行するので下限にならない。
- 稼働時間（3時間・1時間）は**仮定**。公開データはない。スライドにも「仮定」と書く。
- 結論は「止めて節約しても、十万台規模が同時に動く」。平均値なのでピークはこの数倍。

効いてくる観察：Qiita 記事の `free -h` では **7.7GiB中7.3GiBが使用中・スワップなし**。CPUは時分割で詰められても、**メモリは詰めにくい**可能性がある（1台の観察なので断定しない）。「閉じても働く」が売りなので、止めるほど売りが弱まる、という緊張関係もある。

Muse 単体の規模感：80PB（Aの上限）は、Next Signal の「800PB＝年間DRAMビット供給の約1%」から逆算すると **約0.1%**。**Muse単体で市況を動かす規模ではない**。各社が1人1台を配り始めたときの合算が論点、と10枚目でつなぐ。

## 10枚目で言わないこと

- メモリやCPUの値上がりを **Muse のせいにしない**。TrendForce が挙げている主因はAIサーバー・HBMへの生産振り替え・CSPの先行確保。
- 言えるのは「CPUを多く食う使い方（エージェント）が増えている」と Intel 自身が言っていること（CPU:GPU 1:8→1:4、エージェント用途で1:1も）と、Meta自身が「計算資源を相当食う」と認めていること。

## 仮説2（11枚目）の置き方

結論は出さない。**同じ週に日本で両方が始まった**（Muse 10/23、Siri AI 日本語 10/27）ことを入口にして、

- OS型の強み：画面・アプリ・個人データに最初から触れる／標準搭載で配布コストゼロ／端末で動く分はサーバー代がかからない
- クラウドVM型の強み：端末を閉じても動き続ける／自前のブラウザ・ファイル・端末で長い作業や開発ができる／OSをまたげる
- Meta は OS を持たない → WhatsApp（ファミリー全体でDAU 36億人）と自社デバイス（Muse Charm、AIグラス）で入口を確保しようとしている

を並べ、「駆逐か、棲み分けか」を会場に問う。

## 出典

数値はすべて下記から。推計値（Sensor Tower・Similarweb・Apptopia・TickerTrends）は会社ごとに差がある旨をスライドにも書く。

- Meta「Introducing Muse」2026/09/08 https://about.fb.com/news/2026/09/introducing-muse
- Meta「Museを日本で提供開始」2026/10/23 https://about.fb.com/ja/news/2026/10/muse-personal-ai-agent/
- TechCrunch「Muse hits 10M US downloads in 40 days」2026/10/20 https://techcrunch.com/?p=3179696
- TechCrunch「Meta says Muse has over 10M users」2026/10/21 https://techcrunch.com/2026/10/21/meta-says-muse-has-over-10m-users-with-shopping-a-top-activity/
- TechCrunch「Muse is outpacing ChatGPT's early mobile launch」2026/09/21 https://techcrunch.com/2026/09/21/metas-muse-is-outpacing-chatgpts-early-mobile-launch/
- TechCrunch「Meta is putting its muscle behind Muse」2026/09/25 https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off
- 9to5Mac「Muse crosses 5 million downloads」 https://9to5mac.com/?p=1072173
- FourWeekMBA（Similarweb 10/27 レポートの要約） https://fourweekmba.com/ai-muse-vs-chatgpt-users-give-it-7-5-minutes-a-day-vs-23/
- Benzinga／TradingView（Hunterbrook・TickerTrends） https://www.benzinga.com/markets/tech/26/10/62283588/meta-muse-downloads-are-slowing-and-hunterbrook-is-short
- AP（Meta Q3決算） https://www.wdbo.com/news/business/meta-q3-revenue-tops/LJSNKSJRPQ4XHC7YWQH2BFT3LE/
- Qiita @hirokn「Museの中身を覗いたら、ただのUbuntuマシンだった」2026/10/26 https://qiita.com/hirokn/items/31f5403b1fd9d8cbba3c
- TestingCatalog「Meta introduces Muse as a proactive personal agent」 https://www.testingcatalog.com/meta-introduces-muse-as-a-proactive-personal-agent/
- 財聯社（東方財富）2026/09/25 Wang 発言・2vCPU/8GB/100GB https://finance.eastmoney.com/a/202609253884291917.html
- SiliconANGLE「OpenAI launches dots」2026/09/29 https://siliconangle.com/2026/09/29/openai-launches-dots-always-on-ai-agents-in-chatgpt-with-their-own-cloud-computers/
- Interesting Engineering「Grok Bot」 https://interestingengineering.com/ai-robotics/xai-grok-bot-computer-agent
- Claude Code Docs「Use Claude Code in the cloud」「Configure cloud environments」 https://code.claude.com/docs/en/claude-code-on-the-web ／ https://code.claude.com/docs/en/cloud-environments
- OpenAI「Codex Cloud environments」 https://learn.chatgpt.com/docs/environments/cloud-environment
- Apple「Siri AI is here」2026/09 https://www.apple.com/newsroom/2026/09/siri-ai-a-profoundly-more-capable-and-personal-assistant-is-here/
- gori.me「Siri AI、ついに日本語対応」 https://gori.me/ios/ios-news/171770
- Business Standard「Gemini Intelligence」2026/05/13 https://www.business-standard.com/technology/tech-news/gemini-intelligence-may-push-apps-into-android-s-background-explained-126051300577_1.html
- Petri「Windows 11 agent workspaces」 https://petri.com/windows-11-agentic-computing-workspaces/
- Next Signal「What It Takes to Give Every Personal Agent a Computer」2026/09/24 https://nextsignalprediction.substack.com/p/what-it-takes-to-give-every-personal
- Tech Insider（Daytona CEO 試算） https://tech-insider.org/meta-muse-2-8-billion-compute-100-million-users-2026/
- TrendForce 2026/03/31（2Q26 DRAM +58〜63%） https://www.trendforce.com/presscenter/news/20260331-12995.html
- InfotechLead（TrendForce 3Q26 サーバーDRAM +13〜18%） https://infotechlead.com/networking/server-dram-prices-to-jump-18-in-q3-2026-as-ai-demand-and-supply-constraints-tighten-memory-market-trendforce-97002
- Tom's Hardware 2026/04/24（サーバーCPU価格・CPU:GPU比） https://www.tomshardware.com/pc-components/cpus/shifting-need-for-cpus-in-ai-workloads-drives-intensifying-shortages-price-hikes
