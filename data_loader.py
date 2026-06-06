# data_loader.py
import os
import sqlite3
import pandas as pd

# --- DBパスを相対パスで安全に解決 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "price-monitor", "data", "price.db")


# ① 価格推移グラフ用（全件）
def load_price_history():
    query = """
    SELECT 
        ph.product_id,
        p.name AS product_name,
        ph.price,
        ph.scraped_at AS date
    FROM price_history ph
    JOIN products p ON ph.product_id = p.id
    ORDER BY ph.scraped_at ASC;
    """

    # with構文で接続リークを完全防止
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    return df


# ② 最新価格一覧用（真の最新1件を取得）
def load_latest_prices():
    # SQLite 3.25+ で使える ROW_NUMBER() を使用
    query = """
    WITH latest AS (
        SELECT
            product_id,
            price,
            scraped_at,
            ROW_NUMBER() OVER (
                PARTITION BY product_id
                ORDER BY scraped_at DESC
            ) AS rn
        FROM price_history
    )
    SELECT
        p.name AS name,
        p.url AS url,
        l.price AS price,
        l.scraped_at AS last_update
    FROM latest l
    JOIN products p ON p.id = l.product_id
    WHERE l.rn = 1
    ORDER BY last_update ASC;
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    return df
