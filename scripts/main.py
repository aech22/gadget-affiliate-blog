# scripts/main.py — エントリーポイント（リポジトリルートから `python scripts/main.py`）
from __future__ import annotations
import datetime, os, sys
from pathlib import Path

# どのCWDから実行しても scripts/ 内の同階層モジュールを import できるようにする
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml
from config import TOPICS, CATEGORIES
from fetch_products import fetch_products          # 内部で 1req/秒 のレート制御
from generate_article import build_article, rebuild_article, reusable_prose, to_markdown

# 日付は日本時間(JST)で確定する（GitHub ActionsはUTCで動くため、指定しないと日付が1日ずれる）
JST = datetime.timezone(datetime.timedelta(hours=9))

# 出力先は常にリポジトリルート直下の content/articles（scripts の1つ上）
OUT_DIR = Path(__file__).resolve().parent.parent / "content" / "articles"

def slugify(theme: str) -> str:
    # 日本語は isalnum()=True のため保持される。URLは固定（トピック単位・日付を含めない＝重複コンテンツ回避）。
    return "".join(c if c.isalnum() else "-" for c in theme).strip("-")[:60]

def _existing_frontmatter(path: Path) -> dict | None:
    """既存記事の frontmatter を読む（無い・壊れている場合は None）。"""
    if not path.exists():
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1]) or {}
    except Exception:
        return None

def _publish_date(prev: dict | None) -> str | None:
    """既存記事があれば公開日(date)を引き継ぐ（固定URLで公開日を安定させSEO評価を維持）。"""
    d = (prev or {}).get("date")
    return d.isoformat() if hasattr(d, "isoformat") else (str(d) if d else None)

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.datetime.now(JST).date().isoformat()
    generated, facts_only = 0, 0
    for topic in TOPICS:
        try:
            cat_slug = topic["cat"]
            cat = CATEGORIES.get(cat_slug, {})
            label = cat.get("label", cat_slug)
            gender = cat.get("gender", "unisex")

            products = fetch_products(topic["keyword"], topic["hits"])   # sleep はこの中
            if not products:
                print(f"[SKIP] {topic['theme']}: 商品が0件")
                continue

            path = OUT_DIR / f"{slugify(topic['theme'])}.md"
            prev = _existing_frontmatter(path)
            publish_date = _publish_date(prev) or today                   # 初回のみ today、以降は維持
            reused = reusable_prose(products, prev)
            if reused:
                # 商品が1件も入れ替わっていない → 講評文は据え置き、価格・レビューだけ最新にする
                fm = rebuild_article(products, prev, publish_date, label,
                                     category_slug=cat_slug, gender=gender, updated_str=today)
                facts_only += 1
            else:
                fm = build_article(products, topic["theme"], publish_date, label,
                                   category_slug=cat_slug, gender=gender, updated_str=today)
            path.write_text(to_markdown(fm), encoding="utf-8")
            kind = "facts-only" if reused else "generated"
            print(f"{kind} -> {path.name}（{label}/{gender}・{len(fm['products'])}商品）")
            generated += 1
        except Exception as e:
            # 1テーマ失敗しても他を継続（日次ジョブを止めない）。原因は簡潔に表示。
            print(f"[SKIP] {topic['theme']}: {type(e).__name__}: {e}")
    print(f"done: {generated}/{len(TOPICS)} 記事を生成"
          f"（うちLLM未呼び出し{facts_only}本／LLM呼び出し{generated - facts_only}回）")

if __name__ == "__main__":
    main()
