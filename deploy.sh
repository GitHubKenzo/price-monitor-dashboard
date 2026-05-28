#!/bin/bash

SERVER="ubuntu@192.168.3.121"
APP_DIR="/opt/price-monitor-dashboard"

echo "🚀 Starting deployment for price-monitor-dashboard..."

# 1. rsync で差分デプロイ（不要ファイルは削除）
echo "📤 Syncing application files with rsync..."
rsync -avz --delete \
  --exclude="venv/" \
  --exclude="__pycache__/" \
  --exclude=".git/" \
  --exclude=".gitignore" \
  ./ \
  $SERVER:$APP_DIR/

# 2. systemd 再起動
echo "🔄 Restarting price-monitor-dashboard service..."
ssh -tt $SERVER << 'EOF'
sudo systemctl daemon-reload
sudo systemctl restart price-monitor-dashboard
EOF

echo "✅ Deployment completed successfully!"
