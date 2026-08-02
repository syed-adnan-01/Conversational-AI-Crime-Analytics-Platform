#!/bin/sh
set -e

# Detect Python binary
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Error: Python interpreter not found in PATH" >&2
    exit 1
fi

PORT="${X_ZOHO_CATALYST_LISTEN_PORT:-${PORT:-9000}}"

echo "=================================================="
echo "Starting CrimeSphere AI Backend on port $PORT using $PYTHON_BIN"
echo "=================================================="

exec "$PYTHON_BIN" -m uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
