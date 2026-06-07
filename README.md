# Price Monitor Dashboard

Yahooショッピング価格監視システム（price-monitor）が収集した
価格履歴データを可視化する Dash ベースのダッシュボードです。

SQLite に蓄積された価格データを読み込み、

- 価格推移の可視化
- 最新価格の確認
- 商品別価格分析

をブラウザ上で行えます。

---

## システム全体像

```text
Yahoo Shopping
        ↓
    price-monitor
    （価格収集）
        ↓
SQLite Database
        ↓
price-monitor-dashboard
    （本プロジェクト）
        ↓
      Browser
```

本プロジェクトはスクレイピング機能を持ちません。

price-monitor が収集したデータを
可視化するためのビューアです。

---

## 主な機能

### 価格推移グラフ

商品価格の時系列推移をグラフ表示します。

- Plotlyによるインタラクティブ表示
- ズーム対応
- ドラッグ移動対応

### 最新価格一覧

登録商品の最新価格を一覧表示します。

表示項目

- 商品名
- 商品URL
- 販売元
- 最新価格
- 更新日時

### 商品別価格分析

商品単位で価格履歴を確認できます。

---

## 技術スタック

| 分類 | 技術 |
|--------|--------|
| Language | Python |
| Framework | Dash |
| Visualization | Plotly |
| Data Processing | Pandas |
| Database | SQLite |
| WSGI | Gunicorn |
| Testing | pytest |
| Container | Docker |

---

## ディレクトリ構成

```text
.
├── app.py
├── data_loader.py
├── wsgi.py
├── gunicorn.conf.py
├── Dockerfile
├── requirements.txt
├── README.md
│
├── certs/
│
└── tests/
```

---

## クイックスタート

### 1. 仮想環境作成

```bash
python -m venv venv
source venv/bin/activate
```

### 2. 依存ライブラリ導入

```bash
pip install -r requirements.txt
```

### 3. DB配置

```text
/data/price-monitor.sqlite
```

または

```bash
export DB_PATH=/path/to/price-monitor.sqlite
```

### 4. 起動

```bash
python app.py
```

ブラウザで

```text
http://localhost:8050
```

にアクセスしてください。

---

## Docker

### ビルド

```bash
docker build -t price-monitor-dashboard .
```

### 起動

```bash
docker run \
  -d \
  --name price-monitor-dashboard \
  -p 8000:8000 \
  -v /path/to/data:/data \
  price-monitor-dashboard
```

---

## 本番運用

Gunicorn を利用して公開します。

```bash
gunicorn -c gunicorn.conf.py wsgi:server
```

---

## テスト

全テスト実行

```bash
pytest
```

カバレッジ付き

```bash
pytest --cov=.
```

---

## データベース構造

### products

| Column | Description |
|----------|----------|
| id | 商品ID |
| name | 商品名 |
| url | 商品URL |

### price_history

| Column | Description |
|----------|----------|
| id | 履歴ID |
| product_id | 商品ID |
| price | 価格 |
| scraped_at | 取得日時 |

---

## 関連プロジェクト

### price-monitor

Yahooショッピング価格監視システム本体。

本プロジェクトはその収集データを可視化します。

---

## ライセンス

Private Project