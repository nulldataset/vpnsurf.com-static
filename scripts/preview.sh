#!/usr/bin/env bash
# Serve public/ on localhost for quick preview before deploy.
# Run from repo root after ./build.sh. Ctrl+C to stop.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
if [ ! -d public ]; then
  echo "Error: public/ not found. Run ./build.sh first." >&2
  exit 1
fi
echo "Serving public/ at http://localhost:8000 — Ctrl+C to stop."
exec python3 -m http.server 8000 --directory public
