#!/usr/bin/env bash
set -euo pipefail

# HOST と PORT は環境変数で上書き可能
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if command -v uvicorn >/dev/null 2>&1; then
  exec uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
else
  echo "uvicorn not found. Install deps: pip install -r requirements.txt" >&2
  exit 1
fi

