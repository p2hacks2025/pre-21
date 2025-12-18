#!/usr/bin/env bash
set -euo pipefail

PDF_PATH="${1:?pdf path required}"
COPIES="${2:-1}"
PRINTER_NAME="${3:-}"

if command -v lp >/dev/null 2>&1; then
  if [[ -n "${PRINTER_NAME}" ]]; then
    lp -d "${PRINTER_NAME}" -n "${COPIES}" "${PDF_PATH}"
  else
    lp -n "${COPIES}" "${PDF_PATH}"
  fi
else
  echo "lp command not found (CUPS). Install/configure CUPS." >&2
  exit 1
fi
