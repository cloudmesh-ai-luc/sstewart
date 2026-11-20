#!/usr/bin/env bash

# ---------------------------------------------------------------
# Entrypoint for the FastAPI container.
# ---------------------------------------------------------------
# It waits for the MariaDB service to accept TCP connections before
# launching the Uvicorn server. This avoids race conditions where the
# app starts and immediately fails to connect to the database.
# ---------------------------------------------------------------

set -e

HOST="${MARIADB_HOST:-localhost}"
PORT="${MARIADB_PORT:-3306}"

echo "Waiting for MariaDB at ${HOST}:${PORT}..."
while ! nc -z "$HOST" "$PORT"; do
  sleep 1
done
echo "MariaDB is up – starting FastAPI."

# Use environment variable FASTAPI_PORT if supplied, otherwise default to 8000
FASTAPI_PORT="${FASTAPI_PORT:-8000}"

exec uvicorn src.backend.app.main:app --host 0.0.0.0 --port "$FASTAPI_PORT"
