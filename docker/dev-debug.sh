#!/bin/bash
# dev-debug.sh — Launch Frigate backend under debugpy for DAP attach
# =================================================================
# Run from inside the container:
#   cd /workspace/frigate && bash docker/dev-debug.sh
#
# debugpy listens on 0.0.0.0:5678 (mapped to host port 5678).
# In Emacs, use dap-debug → "PYTHON FRIGATE ATTACH" to connect.
#
# Pass --wait to pause until a debugger attaches before executing:
#   cd /workspace/frigate && bash docker/dev-debug.sh --wait
#
# Binds Frigate to 127.0.0.1:5001 (behind nginx, matching production layout).
# Run dev-start-nginx.sh separately to expose port 5000.
#
set -euo pipefail

DEBUG_ARGS="--listen 0.0.0.0:5678"
if [[ "${1:-}" == "--wait" ]]; then
    DEBUG_ARGS="$DEBUG_ARGS --wait-for-client"
    echo "=== debugpy will wait for debugger to attach before starting ==="
fi

echo "=== Starting Frigate backend under debugpy on 0.0.0.0:5678 ==="
echo "    (Frigate binds 127.0.0.1:5001)"
cd /workspace/frigate
export PYTHONPATH=/workspace/frigate
export FRIGATE_API_HOST=127.0.0.1
export FRIGATE_API_PORT=5001

exec python3 -m debugpy $DEBUG_ARGS -m frigate
