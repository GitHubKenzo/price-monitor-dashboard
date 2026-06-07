#!/bin/bash
set -euo pipefail

SERVER="ubuntu@192.168.3.121"
APP_DIR="/opt/price-monitor-dashboard"
SERVICE="price-monitor-dashboard"

echo "🚀 Starting deployment for price-monitor-dashboard..."

# 0. SSH 接続確認（失敗したら即終了）
echo "🔐 Checking SSH connection..."
if ! ssh -o BatchMode=yes -o ConnectTimeout=5 $SERVER "echo ok" >/dev/null 2>&1; then
  echo "❌ ERROR: SSH connection failed. Check network or SSH keys."
  exit 1
fi

# 1. 本番ディレクトリの存在確認
echo "📁 Checking target directory on server..."
ssh $SERVER "sudo mkdir -p $APP_DIR && sudo chown -R ubuntu:ubuntu $APP_DIR"

# 2. rsync で差分デプロイ（不要ファイル削除）
echo "📤 Syncing application files with rsync..."
rsync -avz --delete \
  --exclude="venv/" \
  --exclude="__pycache__/" \
  --exclude=".git/" \
  --exclude=".gitignore" \
  --exclude=".coverage" \
  --exclude="dev.Dockerfile" \
  --exclude="docker-compose.dev.yml" \
  ./ \
  $SERVER:$APP_DIR/

# 3. systemd 再起動（失敗時はログ表示）
echo "🔄 Restarting $SERVICE service..."
ssh $SERVER << EOF
sudo systemctl daemon-reload
if ! sudo systemctl restart $SERVICE; then
  echo "❌ ERROR: Failed to restart service. Showing logs..."
  sudo journalctl -u $SERVICE --no-pager -n 50
  exit 1
fi
EOF

echo "✅ Deployment completed successfully!"
