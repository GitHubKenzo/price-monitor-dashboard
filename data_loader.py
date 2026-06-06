# data_loader.py
import os
import sqlite3
import pandas as pd


def get_db_path():
    # pytest では DB_PATH を上書きする
    return os.getenv("DB_PATH", "/data/price-monitor.sqlite")


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

    with sqlite3.connect(get_db_path()) as conn:
        df = pd.read_sql_query(query, conn)

    return df


# ② 最新価格一覧用（真の最新1件を取得）
def load_latest_prices():
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

    with sqlite3.connect(get_db_path()) as conn:
        df = pd.read_sql_query(query, conn)

    return df
