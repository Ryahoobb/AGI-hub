# AGI HUB 記事パターン集

WIRED徹底分析から抽出した6種類のレイアウトパターン。各パターンは既存のAGI HUBモノトーン生成フローに追加する形で使う。

## パターン選択フロー

記事生成時、以下の順で判定する:

```
記事タイプ → パターン選択
─────────────────────────────────
論考・思想・抽象分析       → 1. Monolith（既存踏襲）
歴史・系譜・長文解説       → 2. Broadsheet
速報・発表・短いニュース   → 3. Dispatch
インタビュー・対談         → 4. Conversation
フォトエッセイ・現地ルポ   → 5. Photo Essay
調査報道・批評・論争       → 6. Investigation
```

アクセントカラーは `palette.json` の `accent` から1色だけ選ぶ。2色以上の混在禁止。

---

## Pattern 1: Monolith（既存踏襲）

**用途**: AGI HUBのコア記事（論考、アラインメント、タクオフ論争など抽象思想系）
**背景**: `#ffffff`（純白）
**アクセント**: なし（純モノトーン）
**画像アスペクト**: 16:7（既存通り）
**構成**: 5スライド（eyebrow + h1/h2 + lead段落 + 構造要素 + footer）

既存の `articles/ai-alignment.html` と同じ。変更なし。

```html
<body class="pattern-monolith">
  <div class="progress"></div>
  <nav class="nav">...</nav>
  <main>
    <section class="slide">
      <div class="eyebrow">The Long Arc</div>
      <h1>既存のヘッドライン</h1>
      <img class="hero ar-16-7" src="..." alt="">
      <p class="lead">...</p>
      <footer>...</footer>
    </section>
    <!-- 以下4スライド -->
  </main>
</body>
```

---

## Pattern 2: Broadsheet（ロングリード）

**用途**: 歴史・系譜・長文解説（10分以上の読了時間を想定）
**背景**: `#faf8f1`（クリームベース）
**アクセント**: 記事別に1色選択（例: `#2f2b92` deep blue for geopolitics）
**画像アスペクト**: 1:1ヒーロー + 16:9 本文内
**構成**: カバースライド + ドロップキャップ本文 + 2-3回の section-marker 区切り + pullquote

### 特徴
- **クリーム背景**で長文の目を守る
- **1:1ヒーロー**（スクエア）がWIRED近年のトレード
- **ドロップキャップ**で第1段落を装飾
- **セクションマーカー**（◆記号）で章を区切る
- pullquoteで議論の山場を強調

### HTML骨子
```html
<body class="pattern-broadsheet accent-deepblue">
  <main>
    <!-- Cover slide: 1:1 hero -->
    <section class="slide cover">
      <div class="eyebrow">Longread / Geopolitics</div>
      <h1 style="font-size:56px;line-height:1.0;">記事タイトル</h1>
      <p class="lead" style="font-size:20px;">サブタイトル</p>
      <img class="hero ar-1-1" src="..." alt="">
      <p class="caption">
        画像キャプション
        <span class="credit">PHOTOGRAPH: ...</span>
      </p>
    </section>

    <!-- Body with drop cap -->
    <section class="slide body">
      <p class="lead dropcap">
        Yudkowskyがアラインメントという語を鋳造したとき、
        それは現在の用法とは少し違う射程を持っていた...
      </p>

      <p>さらに続く段落...</p>

      <div class="section-marker">I</div>

      <p>次のセクション...</p>

      <blockquote class="pullquote">
        人類は既に一度、知能の設計原理を他者に委ねたことがある。
        <cite>— 本文より</cite>
      </blockquote>
    </section>
    <!-- 以下スライドが続く -->
  </main>
</body>
```

---

## Pattern 3: Dispatch（速報・短報）

**用途**: 研究発表、モデルローンチ、重要ニュースの速報
**背景**: `#ffffff`（白）
**アクセント**: `#0066ff`（WIREDブルー）固定
**画像アスペクト**: 16:9 単体ヒーロー
**構成**: 1-2スライドで完結。5スライド構成は使わない

### 特徴
- **短い**（1000-1500字）
- **情報密度が高い**
- アクセントブルーでdate/sourceを強調
- 関連リンクの横並びが末尾に入る

### HTML骨子
```html
<body class="pattern-dispatch">
  <main>
    <section class="slide dispatch">
      <div class="eyebrow" style="color:var(--accent);">Dispatch / 2026.04.09</div>
      <h1 style="font-size:44px;">速報：Anthropicが新モデルを発表</h1>

      <img class="hero ar-16-9" src="..." alt="">
      <p class="caption">写真の説明</p>

      <p class="lead">
        第1段落は要約。<span class="accent-underline">重要な固有名詞</span>にはアクセント下線。
      </p>

      <p>第2段落以降はファクト。</p>

      <!-- Key facts grid -->
      <div class="grid-3">
        <div class="card">
          <div class="num" style="color:var(--accent);">01</div>
          <p>ファクト1</p>
        </div>
        <div class="card">...</div>
        <div class="card">...</div>
      </div>

      <footer>
        <p class="eyebrow">Related Dispatches</p>
        <ul>...</ul>
      </footer>
    </section>
  </main>
</body>
```

---

## Pattern 4: Conversation（インタビュー・対談）

**用途**: 研究者インタビュー、CEO対談、想像上の論者対論
**背景**: `#f9f7ef`（クリーム・ウォーム）
**アクセント**: `#e96700`（バーントオレンジ）で質問を強調
**画像アスペクト**: 3:4 ポートレート（人物単独）
**構成**: Q/Aスタイル + pullquote多用 + 冒頭のポートレート

### 特徴
- **pullquoteを5-8回**使う（WIRED Big Interviewに倣う）
- Q&Aは `<dt>` で質問、`<dd>` で回答
- 質問は小さめ、回答は大きめ
- 人物ポートレート（3:4縦長）

### HTML骨子
```html
<body class="pattern-conversation accent-orange">
  <main>
    <section class="slide cover">
      <div class="eyebrow">The Big Interview</div>
      <h1>人物名×テーマ</h1>
      <p class="lead">リード文。この対話がどういう文脈で行われたか</p>
      <img class="hero ar-3-4" src="..." alt="人物ポートレート">
      <p class="caption">PHOTOGRAPH: ...</p>
    </section>

    <section class="slide qa">
      <dl class="qa-list">
        <dt class="q">Q. あなたが最初にアラインメント問題を意識したのはいつですか？</dt>
        <dd class="a">
          <p>2010年の論文を読んだときです。当時は誰も...</p>
        </dd>
      </dl>

      <blockquote class="pullquote">
        われわれは今もなお、問題を正しく定義する段階にいる。
        <cite>— インタビュイー</cite>
      </blockquote>

      <dl class="qa-list">
        <dt class="q">Q. 次の質問...</dt>
        <dd class="a">...</dd>
      </dl>
    </section>
  </main>
</body>

<style>
.qa-list dt.q {
  font-family: var(--ff-mono);
  font-size: 14px;
  letter-spacing: 0.05em;
  color: var(--accent);
  text-transform: uppercase;
  margin-top: 32px;
  margin-bottom: 12px;
}
.qa-list dd.a {
  font-size: 18px;
  line-height: 1.7;
  margin: 0 0 24px;
}
</style>
```

---

## Pattern 5: Photo Essay（フォトエッセイ）

**用途**: 現地ルポ、AGI開発拠点訪問記、研究所巡礼、ビジュアル主役の記事
**背景**: `#000000`（純黒・ダーク反転）
**アクセント**: `#e6ff00`（ネオンイエロー）
**画像アスペクト**: ギャラリーで複数比率を混在（1:1, 16:9, 3:4）
**構成**: テキスト最小 + 写真ギャラリー中心

### 特徴
- **ダークモード反転**で写真が主役になる
- eyebrow/caption のみネオンイエロー
- 2x2 または 4列ギャラリー
- テキストは各写真のキャプション程度

### HTML骨子
```html
<body class="pattern-photoessay">
  <main>
    <section class="slide essay-cover">
      <div class="eyebrow">Photo Essay</div>
      <h1 style="font-size:56px;color:#fff;">タイトル</h1>
      <p class="lead" style="color:#aaa;">サブタイトル</p>
    </section>

    <section class="slide gallery">
      <img class="hero ar-1-1 hero-color" src="slide1.jpg">
      <p class="caption">1枚目キャプション<span class="credit">PHOTO: ...</span></p>

      <div class="gallery-grid-2">
        <figure>
          <img class="ar-3-4" src="slide2.jpg" style="width:100%;object-fit:cover;">
          <p class="caption">2枚目</p>
        </figure>
        <figure>
          <img class="ar-3-4" src="slide3.jpg" style="width:100%;object-fit:cover;">
          <p class="caption">3枚目</p>
        </figure>
      </div>

      <p style="font-size:18px;color:#ccc;max-width:640px;">
        本文は最小限。写真が語る。
      </p>

      <img class="ar-16-9 hero-color" src="slide4.jpg" style="width:100%;">
      <p class="caption">4枚目</p>
    </section>
  </main>
</body>
```

---

## Pattern 6: Investigation（調査報道・批評）

**用途**: 論争の論理的解剖、誤りの指摘、構造批判、調査ノート
**背景**: `#f3f1e9`（クリーム・ディープ）
**アクセント**: `#d00000`（アラートレッド）
**画像アスペクト**: 4:3 ドキュメント風
**構成**: タイムライン + エビデンスグリッド + 対比テーブル + 批判的pullquote

### 特徴
- クリーム背景が**調査資料の紙面**を思わせる
- 赤アクセントで**問題箇所をハイライト**
- タイムライン（時系列で事実整理）
- エビデンステーブル（主張 vs 反証）
- 警告ボックス（左ボーダー太め）

### HTML骨子
```html
<body class="pattern-investigation">
  <main>
    <section class="slide cover">
      <div class="eyebrow" style="color:var(--accent);">Investigation</div>
      <h1>見出し：何が間違っているか</h1>
      <p class="lead">リード文</p>
      <img class="hero ar-4-3" src="..." alt="">
    </section>

    <section class="slide body">
      <!-- Timeline -->
      <div class="timeline">
        <div class="item">
          <div class="num">2022</div>
          <p>最初の主張が公表される</p>
        </div>
        <div class="item">
          <div class="num">2024</div>
          <p>反証が登場</p>
        </div>
      </div>

      <!-- Evidence table -->
      <table class="compare">
        <thead><tr><th>主張</th><th>検証</th><th>結論</th></tr></thead>
        <tbody>
          <tr><td>...</td><td>...</td><td style="color:var(--accent);">反証</td></tr>
        </tbody>
      </table>

      <!-- Warning callout -->
      <aside class="warning-box">
        <strong>Critical:</strong> ここで議論が破綻している。
      </aside>

      <blockquote class="pullquote">
        論理の飛躍は、権威によって隠蔽される。
      </blockquote>
    </section>
  </main>
</body>

<style>
.warning-box {
  border-left: 4px solid var(--accent);
  padding: 20px 24px;
  background: rgba(208, 0, 0, 0.04);
  margin: 32px 0;
  font-size: 17px;
}
.warning-box strong { color: var(--accent); }
</style>
```

---

## 共通ルール

### やっていいこと
- パターンを跨いだ要素借用（Investigationのタイムラインを Monolith で使う等）
- アクセント色のフィルム的使用（下線、左ボーダー、数字のみ）
- 1:1 / 16:9 / 3:4 のアスペクト比使い分け

### やってはいけないこと
- 1記事で2色以上のアクセント併用
- 背景全体をアクセントで塗る
- box-shadow, gradient
- WIREDロゴやWIRED文字列
- パターン5以外でダーク反転を使う

### 画像配置の原則
- **ヒーローは1枚**。複数ヒーローは avoid
- **キャプションは必須**（画像の説明 + credit）
- **記事内で複数のアスペクト比を混ぜてよい**（変化を付ける）
- **サイズと配置は10種類のユーティリティから選ぶ**（下記 Image Placement Gallery）
- フィルター `grayscale(0.6) contrast(1.1)` がAGI HUBデフォルト。パターン5のみカラー

---

## Image Placement Gallery（10種）

記事本文は `--content-width: 680px`（約62ch）を基準幅とする。画像はこの本文幅との関係で10通りの配置をとる。`palette.css` の `.img-*` ユーティリティで実装。

| # | クラス | 幅 | 配置 | 主な用途 |
|---|---|---|---|---|
| 1 | `.img-fullbleed` | 100vw | 画面端まで | セクション切替、視覚的休符、特集オープナー |
| 2 | `.img-wide` | 1080px / 100vw-48px | 中央（本文超え） | 主要ヒーロー、引きのある資料画像 |
| 3 | `.img-content` | 680px | 本文と同幅 | 標準配置。説明的な図版 |
| 4 | `.img-center-small` | 420px | 中央・小 | 補助図、ポートレート縮小、アイコン的図版 |
| 5 | `.img-float-left` | 44% / 340px | 左寄せ・本文回り込み | 人物紹介、小カット、注釈図 |
| 6 | `.img-float-right` | 44% / 340px | 右寄せ・本文回り込み | サイドノート、引用画像、補助資料 |
| 7 | `.img-side-by-side` | 本文幅内2分割 | 2枚並列 | Before/After、対比、Diptych |
| 8 | `.img-grid-3` / `.img-grid-4` | 本文幅3-4分割 | 3-4枚グリッド | フォトエッセイ、研究拠点群、作例一覧 |
| 9 | `.img-overlay` | 1080px / 100vw-48px | 中央・テキスト重ね | 特集カバー、パート扉 |
| 10 | `.img-inline` / `.img-inline-thumb` | 1.4em / 96px | 段落内 | アイコン、ロゴ、段落先頭サムネ |

### CSSスニペット早見表

```html
<!-- 1. Full-bleed -->
<figure class="img img-fullbleed">
  <img src="hero.jpg" alt="">
  <figcaption class="caption">全画面幅の視覚的休符<span class="credit">PHOTO: UNSPLASH</span></figcaption>
</figure>

<!-- 2. Wide（コンテンツ幅超え） -->
<figure class="img img-wide">
  <img src="wide.jpg" alt="">
  <figcaption class="caption">本文幅を超える主要画像</figcaption>
</figure>

<!-- 3. Content-width -->
<figure class="img img-content">
  <img src="body.jpg" alt="">
  <figcaption class="caption">標準配置</figcaption>
</figure>

<!-- 4. Center small -->
<figure class="img img-center-small">
  <img src="small.jpg" alt="">
  <figcaption class="caption">補助図</figcaption>
</figure>

<!-- 5. Float left -->
<figure class="img img-float-left">
  <img src="portrait.jpg" alt="">
  <figcaption class="caption">人物カット</figcaption>
</figure>
<p>この段落は画像の右側に回り込む。floatを解除したい段落には <code>class="clear-floats"</code> を付ける。</p>

<!-- 6. Float right -->
<figure class="img img-float-right">
  <img src="sidenote.jpg" alt="">
</figure>

<!-- 7. Side by side -->
<div class="img-side-by-side">
  <figure><img src="a.jpg"><figcaption class="caption">Before</figcaption></figure>
  <figure><img src="b.jpg"><figcaption class="caption">After</figcaption></figure>
</div>

<!-- 8. Grid 3 / Grid 4 -->
<div class="img-grid-3">
  <img src="1.jpg"><img src="2.jpg"><img src="3.jpg">
</div>

<!-- 9. Overlay -->
<figure class="img img-overlay">
  <img src="cover.jpg" alt="">
  <div class="overlay-text">
    <div class="eyebrow">Longread</div>
    <h1>計算の神殿</h1>
  </div>
</figure>

<!-- 10. Inline -->
<p>このロジックは <img class="img-inline" src="logo.svg" alt=""> の初期版で既に見られた。</p>
<p><img class="img-inline-thumb" src="thumb.jpg" alt="">段落先頭にサムネイルを置き、本文が右側に回り込む短い紹介ブロック。</p>
```

### パターン別・推奨画像配置マッピング

各レイアウトパターンで主に使う画像配置クラスの推奨。必須ではなく、パターンを跨いだ借用は自由。

| パターン | 主力配置 | 補助配置 | 使わない |
|---|---|---|---|
| 1. Monolith | `img-content`（16:7） | `img-wide` / `img-center-small` | `img-overlay`（純モノトーンに反する） |
| 2. Broadsheet | `img-wide`（1:1 hero）+ `img-float-right` | `img-content` / `img-inline-thumb` | `img-grid-4`（情報密度が合わない） |
| 3. Dispatch | `img-content`（16:9） | `img-inline` | `img-fullbleed` / `img-overlay`（短報に不要） |
| 4. Conversation | `img-float-left`（3:4ポートレート） | `img-content` / `img-center-small` | `img-grid-3` |
| 5. Photo Essay | `img-fullbleed` + `img-grid-3` / `img-grid-4` | `img-side-by-side` / `img-overlay` | `img-inline`（テキスト最小で役割なし） |
| 6. Investigation | `img-content`（4:3） + `img-side-by-side`（対比） | `img-float-right`（資料）/ `img-inline-thumb` | `img-overlay`（調査資料の紙面感に反する） |

### 運用ルール
- 1記事で使う画像配置は**3種類以内**。多用するとノイズになる
- `img-fullbleed` と `img-overlay` は**記事に1回まで**（視覚的休符の価値が消える）
- `img-float-*` の直後の段落は最低3段落以上続ける。1段落だけで float を終えるとレイアウトが崩れる
- モバイル（768px未満）では `img-float-*` は自動で `float: none; width: 100%;` に落ちる（追加CSS必要時は記事側で指定）

## 運用

1. 新規記事作成時、記事タイプから自動でパターンを選択
2. `<body class="pattern-[name] accent-[color]">` で切り替え
3. palette.cssを記事HTMLの `<style>` にインライン展開（CDN依存を避ける）
4. 生成後、`design-system/SAMPLES/` に各パターンの実例HTMLを保存
