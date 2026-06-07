import sys
import os
import sqlite3
import pytest

# ① プロジェクトルートを追加
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ② DB_PATH を “import 前に” 上書きする（最重要）
TEST_DB = os.path.abspath("tests/test_db.sqlite")
os.environ["DB_PATH"] = TEST_DB  # ← これが決定的に重要


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # 既存のテストDBを削除
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    # 本番と同じテーブル構造
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE price_history (
            product_id INTEGER,
            price INTEGER,
            scraped_at TEXT
        )
    """)

    # テストデータ投入
    cursor.executemany(
        """
        INSERT INTO products (id, name, url)
        VALUES (?, ?, ?)
    """,
        [
            (1, "Test Product A", "http://example.com/a"),
            (2, "Test Product B", "http://example.com/b"),
        ],
    )

    cursor.executemany(
        """
        INSERT INTO price_history (product_id, price, scraped_at)
        VALUES (?, ?, ?)
    """,
        [
            (1, 1200, "2024-01-01 10:00:00"),
            (2, 980, "2024-01-02 12:00:00"),
        ],
    )

    conn.commit()
    conn.close()

    yield

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
