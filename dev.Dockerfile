# dev.Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Tokyo

WORKDIR /app

# ---- 1. 開発用依存関係インストール ----
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest ruff black

# ---- 2. アプリケーションコードをコピー ----
COPY . /app

# ---- 3. デフォルト CMD（pytest 実行）----
CMD ["pytest", "-v"]
