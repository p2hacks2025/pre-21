#!/usr/bin/env bash
set -euo pipefail

if command -v pytest >/dev/null 2>&1; then
  exec pytest -q "$@"
else
  echo "pytest not found. Install deps: pip install -r requirements.txt" >&2
  exit 1
fi