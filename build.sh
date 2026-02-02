#!/usr/bin/env bash
# Build: copy banner ads to public, inject Chatwoot and ad banners into target HTML.
# Run from repo root. Ensure public/ exists (e.g. extract new template into public/ first).
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
mkdir -p public
# Copy banner ads from source to public
mkdir -p public/banner-ads
cp -r source/banner_ads/* public/banner-ads/ 2>/dev/null || true
# Copy favicon if present
if [ -f source/favicon.png ]; then cp source/favicon.png public/favicon.png; fi
python3 integrations/chatwoot/add_chatwoot.py
python3 integrations/add_ad_banners.py
echo "Build complete."
