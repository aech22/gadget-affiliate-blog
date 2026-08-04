# CLAUDE.md — ガジェナビ

**⚠️ 作業前に共通正本を必ず読むこと:**
`/Users/hiroshi/Documents/Obsidian Vault/Projects/アフィリエイト/AFFILIATE.md`

技術スタック・デプロイ手順・禁止事項・ハマりどころは全て共通正本にある。このファイルには**ガジェナビ固有の情報だけ**を書く。picknavi のクローンなので、迷ったら `rakuten-affiliate-blog` の実装を見る。

---

## サイト固有情報

| 項目 | 内容 |
|---|---|
| ブランド | ガジェナビ |
| 本番URL | https://gagetnavi.net（独自ドメイン・ルート配信） |
| GitHub | `aech22/gadget-affiliate-blog`（public） |
| 収益モデル | 楽天アフィリエイト（物販・ガジェット） |
| 由来 | picknavi のクローン（2026-08-03構築） |

⚠️ **ドメインの綴りは "gaget"**（"gadget" ではない）。打ち間違いではなく、この綴りで登録済み。

## カテゴリ（8種・全て unisex）

earphones / charging / pc-peripheral / smart-home / camera-gear / gaming / wearable / home-gadget

`scripts/config.py` と `src/data/taxonomy.ts` の slug 一致は `tests/test_taxonomy_parity.py`（unittest）で担保している。**カテゴリを増やすときは両方を直してテストを通す。**

## 楽天API 設定

| 項目 | 値 |
|---|---|
| `applicationId` | `325f9fac-0d26-4884-99c4-af4ca0baa9e0` |
| `accessKey`(pk_) | GitHub Secrets |
| `AFFILIATE_ID` | GitHub Secrets（**picknavi とは別の楽天アフィリエイトID**＝ダッシュボードでの収益分離のため） |
| Allowed websites | `aech22.github.io` |

⚠️ Allowed websites は **APIリクエストの Origin/Referer 照合用**で、サイトの公開ドメインとは別物。workflow の `RAKUTEN_ORIGIN` / `RAKUTEN_REFERER` は github.io のままでよい（独自ドメイン移行後も楽天への再登録は不要）。

## DNS

Cloudflare 管理。A レコード4本（185.199.108-111.153）・**グレー雲（DNS only）必須**（オレンジ雲だと GitHub Pages の証明書が発行できない）。HTTPS enforce 済み。

## 固有のハマりどころ

- **base パス（最重要・解決済み）**: GitHub プロジェクトページのサブパス配信（`/gadget-affiliate-blog/`）では、Astro の `base` 未設定だと CSS/JS 資産も内部リンクも全てルート絶対で404＝「開くがスタイル崩れ＋全リンク404」。picknavi は独自ドメインのルート配信なので露呈しない問題。対策として**内部リンクを全て `import.meta.env.BASE_URL` 方式**にしてある（`base` 行を消すだけで両対応＝手戻りゼロ）。`base` 指定は末尾スラッシュ必須
- **bot が記事を main にコミットする**ので、再 push の前に `git pull --rebase`

## 残ポリッシュ

- [ ] `public/ogp.png` が picknavi ブランドのまま（差し替え要）
- [ ] ヘッダーの「ユニセックス系」タブが単独で残っている（記事一覧と冗長）
- [ ] `tests/test_quality_check.py` の2件失敗は picknavi 由来の既存事象（別タスク起票済み）
