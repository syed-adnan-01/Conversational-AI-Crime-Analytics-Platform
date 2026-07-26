#!/usr/bin/env bash
set -e

PORT="${X_ZOHO_CATALYST_LISTEN_PORT:-9000}"

echo "=== CrimeSphere AppSail Start ==="
echo "PORT=$PORT"
echo "PYTHON=$(python3 --version 2>&1)"
echo "PWD=$(pwd)"
echo "================================="

# Try importing the full app first
python3 -c "
import sys
import traceback
try:
    from app.main import app
    print('APP IMPORT: OK')
except Exception as e:
    print('APP IMPORT FAILED:', str(e))
    traceback.print_exc()
    sys.exit(1)
"

echo "Starting uvicorn on port $PORT..."
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port "$PORT" \
  --workers 1 \
  --log-level info \
  --timeout-keep-alive 75
