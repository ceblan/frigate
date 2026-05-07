#!/bin/bash
# dev-start.sh — Launch full dev stack (Frigate + nginx + Vite)
# ==============================================================
# Run from inside the container:
#   cd /workspace/frigate && bash docker/dev-start.sh
#
# Starts Frigate on 127.0.0.1:5001, nginx on 0.0.0.0:5000, and
# Vite frontend dev server on 0.0.0.0:5173.
#
# Endpoints match production: nginx adds /api prefix, VOD HLS, auth proxying.
#     Backend:  http://localhost:5000/api/...
#     VOD HLS:  http://localhost:5000/vod/.../index.m3u8
#     Frontend: http://localhost:5173 (Vite hot-reload, proxies API to :5000)
#
set -euo pipefail

FRIGATE_PID=""
NGINX_PID=""
FRONTEND_PID=""

cleanup() {
    echo ""
    echo "=== Shutting down ==="
    [ -n "$NGINX_PID" ]     && kill "$NGINX_PID" 2>/dev/null     && echo "nginx stopped (PID $NGINX_PID)"
    [ -n "$FRIGATE_PID" ]   && kill "$FRIGATE_PID" 2>/dev/null   && echo "Frigate stopped (PID $FRIGATE_PID)"
    [ -n "$FRONTEND_PID" ]  && kill "$FRONTEND_PID" 2>/dev/null  && echo "Vite stopped (PID $FRONTEND_PID)"
    exit 0
}
trap cleanup EXIT INT TERM

# --- Frigate backend (127.0.0.1:5001) ---
echo "=== Starting Frigate backend on 127.0.0.1:5001 ==="
cd /workspace/frigate
export PYTHONPATH=/workspace/frigate
export FRIGATE_API_HOST=127.0.0.1
export FRIGATE_API_PORT=5001
python3 -u -m frigate &
FRIGATE_PID=$!
echo "    Frigate PID: $FRIGATE_PID"

# Wait for backend to be ready
echo "    Waiting for backend..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:5001/ > /dev/null 2>&1; then
        echo "    Backend ready!"
        break
    fi
    if ! kill -0 "$FRIGATE_PID" 2>/dev/null; then
        echo "!!! Backend failed to start. Check output above."
        wait "$FRIGATE_PID" 2>/dev/null
        exit 1
    fi
    sleep 1
done

# --- nginx (0.0.0.0:5000) ---
echo "=== Starting nginx on 0.0.0.0:5000 ==="
bash /workspace/frigate/docker/dev-start-nginx.sh &
NGINX_PID=$!
echo "    nginx PID: $NGINX_PID"
sleep 1

if ! kill -0 "$NGINX_PID" 2>/dev/null; then
    echo "!!! nginx failed to start."
    exit 1
fi
echo "    nginx ready!"

# --- Frontend (Vite dev server on 0.0.0.0:5173) ---
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
echo "    Frigate:  http://127.0.0.1:5001 (internal, no /api prefix)"
echo "    nginx:    http://localhost:5000 (adds /api, VOD HLS, auth)"
echo "    Frontend: http://localhost:5173 (Vite hot-reload, proxies to :5000)"
echo ""
echo "    Edit code in ~/git-hub/frigate on host — changes reflect immediately."
echo "    Frontend: Vite hot-reloads .tsx/.ts changes."
echo "    Backend:  kill (Ctrl+C) and re-run this script."
echo ""
echo "    Press Ctrl+C to stop all services."
echo ""

wait
