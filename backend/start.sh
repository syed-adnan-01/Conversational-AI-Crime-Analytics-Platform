#!/usr/bin/env bash
set -e

# Zoho Catalyst AppSail injects X_ZOHO_CATALYST_LISTEN_PORT at runtime.
# Fall back to 9000 for local testing.
PORT="${X_ZOHO_CATALYST_LISTEN_PORT:-9000}"

echo "Starting CrimeSphere backend on port $PORT"

exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
