#!/bin/bash
# dev-start.sh — Launch Frigate backend + Vite frontend dev server
# ================================================================
# Run from inside the container:
#   cd /workspace/frigate && bash docker/dev-start.sh
#
# Backend  → http://localhost:5000
# Frontend → http://localhost:5173 (Vite hot-reload, proxies API to backend)
#
set -euo pipefail

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo ""
    echo "=== Shutting down ==="
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null && echo "Backend stopped (PID $BACKEND_PID)"
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null && echo "Frontend stopped (PID $FRONTEND_PID)"
    exit 0
}
trap cleanup EXIT INT TERM

# --- Backend ---
echo "=== Starting Frigate backend on 0.0.0.0:5000 ==="
cd /workspace/frigate
export PYTHONPATH=/workspace/frigate
export FRIGATE_API_HOST=0.0.0.0
export FRIGATE_API_PORT=5000
python3 -u -m frigate &
BACKEND_PID=$!
echo "    Backend PID: $BACKEND_PID"

# Wait for backend to be ready
echo "    Waiting for backend..."
for i in $(seq 1 30); do
    if curl -s http://localhost:5000/ > /dev/null 2>&1; then
        echo "    Backend ready!"
        break
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo "!!! Backend failed to start. Check output above."
        wait "$BACKEND_PID" 2>/dev/null
        exit 1
    fi
    sleep 1
done

# --- Frontend (Vite dev server) ---
echo "=== Starting Vite frontend dev server on 0.0.0.0:5173 ==="
cd /workspace/frigate/web
if [ ! -d "node_modules" ]; then
    echo "    Installing npm dependencies..."
    npm install
fi
npx vite --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
echo "    Frontend PID: $FRONTEND_PID"

echo ""
echo "=== Ready ==="
echo "    Backend:  http://localhost:5000"
echo "    Frontend: http://localhost:5173"
echo ""
echo "    Edit code in ~/git-hub/frigate on host — changes reflect immediately."
echo "    Frontend: Vite hot-reloads .tsx/.ts changes."
echo "    Backend:  kill (Ctrl+C) and re-run this script."
echo ""
echo "    Press Ctrl+C to stop both."
echo ""

wait
