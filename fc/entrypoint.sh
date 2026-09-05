#!/bin/sh
set -e

# 配置和凭证通过 FC 环境变量注入（base64 编码，避免换行/特殊字符问题）
umask 077
mkdir -p /app/state/data /app/state/logs

if [ -n "$MIYOUQIAN_CONFIG_B64" ]; then
  printf '%s' "$MIYOUQIAN_CONFIG_B64" | base64 -d > /app/state/config.yaml
  echo "[fc-entrypoint] config.yaml written (${MIYOUQIAN_CONFIG_B64} chars b64)"
fi

if [ -n "$MIYOUQIAN_CREDENTIALS_B64" ]; then
  printf '%s' "$MIYOUQIAN_CREDENTIALS_B64" | base64 -d > /app/state/data/credentials.yaml
  echo "[fc-entrypoint] credentials.yaml written"
fi

# 兜底：没有注入配置时用示例配置，避免启动崩溃
if [ ! -f /app/state/config.yaml ]; then
  echo "[fc-entrypoint] WARNING: no config injected, using example config"
  cp /app/config.example.yaml /app/state/config.yaml
fi

exec "$@"
