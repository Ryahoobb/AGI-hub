# WIRED徹底分析レポート

AGI HUBの記事パターン拡張のため、WIRED（wired.com）の実際の記事を徹底分析した結果。
分析日: 2026-04-09

## 分析対象記事（8本）

ニュース・解説系:
1. [Boston Dynamics Led a Robot Revolution](https://www.wired.com/story/boston-dynamics-led-a-robot-revolution-now-its-machines-are-teaching-themselves-new-tricks/) — テック解説
2. [Anthropic's World-First Hybrid Reasoning AI Model](https://www.wired.com/story/anthropic-world-first-hybrid-reasoning-ai-model/) — プロダクトローンチ報道
3. [Why Beating China in AI Brings Its Own Risks](https://www.wired.com/story/why-beating-china-in-ai-brings-its-own-risks/) — 地政学オピニオン
4. [Databricks Has a Trick That Lets AI Models Improve Themselves](https://www.wired.com/story/databricks-has-a-trick-that-lets-ai-models-improve-themselves/) — 研究解説
5. [Botto the Millionaire AI Artist](https://www.wired.com/story/botto-the-millionaire-ai-artist-is-getting-a-personality/) — カルチャー

ロングフォーム・特集系:
6. [China AI Boyfriends](https://www.wired.com/story/china-ai-boyfriends/) — フィーチャー/ルポ
7. [Big Interview: Tarek Mansour, Kalshi](https://www.wired.com/story/big-interview-tarek-mansour-kalshi/) — インタビュー特集
8. [China Adoption: Birth Parents](https://www.wired.com/story/china-adoption-birth-parents/) — ナラティブ・ジャーナリズム

## 1. 色味の発見

### WIREDカラーシステム（CSSから実抽出）

すべての記事で同一のカラートークンセットが読み込まれている。これはWIREDが「記事ごとに色を変える」のではなく「固定パレットの中から特集ごとに強調色を選ぶ」設計であることを示す。

#### ベース（モノトーン）
| 用途 | HEX | 備考 |
|---|---|---|
| 純黒（見出し・本文） | `#000000` | H1・ロゴ |
| ダークグレー（本文） | `#1a1a1a` | Body text |
| ミッドグレー（メタ情報） | `#585858` | Byline、日付 |
| ライトグレー（補助） | `#757575` | Caption |
| ボーダー | `#e5e5e5` | 区切り線 |
| 背景グレー | `#f7f7f7` | セクション背景 |
| 白 | `#FFFFFF` | ベース背景 |

#### クリーム系背景（特集記事で採用）
ロングリードや特集記事では純白ではなくクリーム系背景が使われる。これが「紙っぽさ」と「長文の読みやすさ」を両立する秘訣。

| HEX | 性格 |
|---|---|
| `#faf8f1` | 最も使用頻度が高い基本クリーム |
| `#f9f7ef` | やや暗めのクリーム |
| `#fefcf5` | 極薄クリーム（ほぼ白） |
| `#f3f1e9` | 濃いめのクリーム（特集カバー向け） |

#### アクセントカラー（記事カテゴリや特集ごとに選択）
WIREDは全記事で以下のアクセントを**ライブラリとして読み込み**、特集テーマに応じて使い分ける。

| HEX | 通称 | 用途 |
|---|---|---|
| `#0066ff` | **WIRED Blue** | リンク・ロゴ・CTAボタン。全記事共通 |
| `#00FFFF` | ネオンシアン | サイバー・AI系特集のハイライト |
| `#00FF00` | ネオングリーン | テック・コード系特集 |
| `#E6FF00` | ネオンイエロー | カルチャー特集 |
| `#FF00FF` | ネオンマゼンタ | フューチャー系・音楽系 |
| `#f6b6f7` | ピンクパステル | カルチャー・ソフト系 |
| `#f7c442` | イエローゴールド | 経済・金融系 |
| `#e96700` | バーントオレンジ | 警告・規制系 |
| `#d00000` / `#eb0000` | アラートレッド | リスク・論争系 |
| `#00c559` / `#298552` | グリーン2段 | サステナ・自然系 |
| `#2f2b92` | ディープブルー | 政治・地政学系 |
| `#057dbc` | セカンダリーブルー | 科学系 |
| `#231927` | ダークパープル | ミステリアス・ダークストーリー |

**重要な発見**: WIREDは1つの記事で多色を使わない。背景クリーム + 黒文字 + **1〜2色**のアクセントに抑制する。アクセントは見出しのハイライト下線、pull-quoteのボーダー、CTAボタン、数字強調などピンポイントに配置。

## 2. タイポグラフィの階層

### フォント5種の使い分け

| フォント | 用途 |
|---|---|
| **WIRED Display** / **WIRED Display Slab** | ヒーロー見出し・記事タイトル（大サイズ） |
| **Breve Text** | 本文（セリフ系。長文読解を支える） |
| **Apercu** | キャプション・ラベル・UIテキスト（グロテスクサンセリフ） |
| **Proxima Nova** | 代替サンセリフ |
| **WIRED Mono** | 数字強調・コード・eyebrow |
| **Lab Grotesque** | セクションラベル |

AGI HUBは日本語環境なので完全移植は不要。代わりに以下の2軸で再現する:
- **Display**: 既存のHelvetica Neue + 游ゴシック（太字）
- **Body**: 既存のHelvetica Neue + 游ゴシック（regular）
- **Mono/Eyebrow**: SF Mono / Fira Code（既存踏襲）
- **アクセント**: 英文見出しだけWIRED Display風にSerif系（Playfair Display, Noto Serif JP）を採用する選択肢あり

### フォントサイズスケール（実抽出）
```
10, 11, 12, 13, 14, 16, 17, 19, 20, 24, 28, 34, 38, 44, 52, 54, 56 (px)
```

見出しは `28 → 34 → 44 → 52 → 56` のステップ。本文は `16/1.5em`。キャプションは `11-13px/1.23em`。
AGI HUBの現状は 16→20→28→44 あたりで足りているが、**ヒーロー級H1を56pxまで上げる余地**がある。

## 3. 画像・写真のパターン

### アスペクト比の使い分け（WIRED CDN URLから実抽出）

全記事共通の出現頻度:

| 比率 | 用途 | 典型的な使い方 |
|---|---|---|
| **16:9** | 関連記事サムネイル・本文インライン画像 | 最も多い。小〜中サイズ |
| **1:1** | ヒーロー画像・特集カバー | ニュース記事のトップを飾る正方形。**近年のWIREDの特徴** |
| **3:2** | セカンダリー画像 | インタビューのポートレート |
| **3:4** | 縦長ポートレート | 人物単独・製品単独 |
| **2:3** | さらに縦長のポートレート | フルページ紙面風 |
| **4:3** | 旧規格・古い写真 | アーカイブ画像 |
| **191:100** | OGP用 | Twitterカード |

**重要**: AGI HUBは全スライドで `16/7` を使っているが、これは単調。WIREDに倣って **ヒーロー=1:1 / 本文中=16:9 / 人物=3:4** と使い分けると視覚的バリエーションが増える。

### 画像の配置パターン

記事で観察されたパターン:

1. **Hero Lede（スプリットスクリーン）**: 画面左半分に画像、右半分に見出し。1:1ヒーローで最も多い
2. **Full Bleed Hero**: 画面幅いっぱいの画像に見出しオーバーレイ
3. **Inline Asset Embed**: 本文カラム幅に収まる画像。16:9が標準
4. **Carousel/Gallery**: スワイプ可能な写真列。フォトエッセイ系で多用
5. **Side-by-Side**: 2枚並び。比較や対比を示すとき
6. **Ledeなし**: 画像なし開始。インタビューや短報で稀に採用

### キャプション書式
- フォント: Apercu（サンセリフ）
- サイズ: 11-13px
- 色: `#757575`
- 位置: 画像直下、左寄せ
- 長さ: 1-2行（簡潔）
- クレジット: `PHOTOGRAPH: JOHN DOE` のように**オールキャップス**で末尾に配置

## 4. レイアウト構造の発見

### Pull-quote（引用オーバーレイ）
- ニュース記事には**ほぼ使わない**
- インタビュー記事（Big Interview）では頻繁に使用（1記事あたり10-13回）
- スタイル: 左ボーダー（アクセントカラー）+ 大きめフォント（28-34px）+ 太字 + 発話者クレジット
- クラス構造: `PullQuoteEmbedWrapper > PullQuoteDecorativeBorder + PullQuoteEmbedContent + PullQuoteEmbedCredit`

### Drop Cap（頭文字装飾）
- 長文記事の冒頭で時々使用
- 本文の最初の1文字を3-4行分の高さに拡大
- WIRED Display Slab（太めセリフ）で表現

### Section Divider
- 単純な水平線ではなく、**1文字だけのマーカー**（◆ や ❋ や ※）を中央配置するパターン
- セクション番号（I / II / III）をeyebrow的に使う書式

### Grid/Carousel（ギャラリー）
- フォトエッセイ系記事で `Gallery-` / `Carousel-` クラスが58箇所・26箇所と多用
- 2〜4枚の写真を横並びグリッドで配置
- スマホではスワイプ可能なカルーセルに変形

## 5. AGI HUBへの適用方針

### 維持するもの（モノトーン基調）
- ベースは `#000 / #1a1a1a / #757575 / #e5e5e5 / #fff`
- 本文カラム・ナビゲーション・footer
- `palt` カーニング、游ゴシック系日本語フォント

### 拡張するもの（WIREDから導入）
1. **クリーム背景オプション**: 長文記事やインタビューではクリーム背景を選択できる
2. **アクセントカラー1色**: 記事カテゴリに応じて1色だけ差し色として使える。多色禁止
3. **アスペクト比バリエーション**: 16/7固定をやめ、1:1 / 16:9 / 3:4 を使い分け
4. **Pull-quote**: インタビュー系記事で使えるpull-quoteスタイルを用意
5. **Drop Cap**: ロングリードで使えるドロップキャップ
6. **Gallery Grid**: 2-4枚グリッドレイアウト

### 禁止を継続
- box-shadow
- 多色ミックス（1記事3色以上）
- WIREDロゴ・WIRED文字列そのもの
- ブランド固有の装飾

## 6. 抽出した5つの記事パターン

詳細は `PATTERNS.md` を参照。

| # | 名称 | 用途 | ベース背景 | アクセント |
|---|---|---|---|---|
| 1 | Monolith | 既存の5スライド型（論考・分析） | `#fff` | なし（純モノトーン） |
| 2 | Broadsheet | ロングリード・解説記事 | `#faf8f1` | 1色（記事別に選択） |
| 3 | Dispatch | ニュース速報・短報 | `#fff` | `#0066ff` |
| 4 | Conversation | インタビュー・対談 | `#f9f7ef` | `#e96700`（Q&A強調） |
| 5 | Photo Essay | フォトエッセイ・現地ルポ | `#000`（ダーク反転） | `#E6FF00` |
| 6 | Investigation | 調査報道・批評 | `#f3f1e9` | `#d00000`（警告色） |

## 7. カラーパレット定義

詳細は `palette.json` および `palette.css` を参照。

## 参考
- 分析元の全8記事のHTMLを `/tmp/wired-analysis/` に一時保存した
- WIREDのCSSはstyled-components方式で圧縮されているため、クラス名は可読性が低い。色・サイズ・フォントは`grep`で直接抽出した
