#!/usr/bin/env sh

set -e

echo "======================================="
echo "Starting MedRAG..."
echo "======================================="

exec uvicorn medrag.main:app \
    --host 0.0.0.0 \
    --port 8000