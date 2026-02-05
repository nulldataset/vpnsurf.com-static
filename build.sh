#!/usr/bin/env bash
# Build: copy banner ads to public, inject Chatwoot and ad banners into target HTML.
# Run from repo root. Ensure public/ exists (e.g. extract new template into public/ first).
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
mkdir -p public
# Sanitize image metadata in source/pictures so public gets zero-metadata assets
if ! command -v exiftool >/dev/null 2>&1; then
  echo "Error: exiftool is required. Install e.g. libimage-exiftool-perl (Debian/Ubuntu) or https://exiftool.org/install.html" >&2
  exit 1
fi
shopt -s nullglob
picfiles=( source/pictures/*.png source/pictures/*.gif source/pictures/*.jpg source/pictures/*.jpeg )
if [ ${#picfiles[@]} -gt 0 ]; then
  exiftool -all= -overwrite_original "${picfiles[@]}"
fi
shopt -u nullglob
# Copy banner ads from source to public
mkdir -p public/banner-ads
cp -r source/banner_ads/* public/banner-ads/ 2>/dev/null || true
# Copy favicon if present
if [ -f source/favicon.png ]; then cp source/favicon.png public/favicon.png; fi
# Copy content scaffold from source to public (articles, pictures, videos)
mkdir -p public/articles public/pictures public/videos
cp -r source/articles/* public/articles/ 2>/dev/null || true
cp -r source/pictures/* public/pictures/ 2>/dev/null || true
cp -r source/videos/* public/videos/ 2>/dev/null || true
python3 integrations/chatwoot/add_chatwoot.py
python3 integrations/add_ad_banners.py
echo "Build complete."
