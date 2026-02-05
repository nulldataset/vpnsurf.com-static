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
# Copy content scaffold from source to public (articles, pictures, videos)
mkdir -p public/articles public/pictures public/videos
cp -r source/articles/* public/articles/ 2>/dev/null || true
cp -r source/pictures/* public/pictures/ 2>/dev/null || true
cp -r source/videos/* public/videos/ 2>/dev/null || true
python3 integrations/chatwoot/add_chatwoot.py
python3 integrations/add_ad_banners.py
# Clean URLs: move .html pages into path/index.html so URLs are /faq/, /articles/slug/, etc.
mkdir -p public/faq public/glossary
for page in faq glossary; do
  if [ -f "public/${page}.html" ]; then
    cp "public/${page}.html" "public/${page}/index.html" && rm "public/${page}.html"
  fi
done
for slug in why-use-vpn secure-browsing-tips vpn-for-streaming vpn-for-travel vpn-vs-proxy; do
  if [ -f "public/articles/${slug}.html" ]; then
    mkdir -p "public/articles/${slug}"
    cp "public/articles/${slug}.html" "public/articles/${slug}/index.html" && rm "public/articles/${slug}.html"
  fi
done
# Redirect stubs for old .html URLs (meta refresh + link for crawlers and no-JS users)
write_redirect() {
  local file="$1"
  local path="$2"
  local label="$3"
  printf '%s\n' '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url='"$path"'"><title>Redirect</title></head><body><p>Redirecting to <a href="'"$path"'">'"$label"'</a>.</p></body></html>' > "$file"
}
write_redirect "public/faq.html" "/faq/" "FAQ"
write_redirect "public/glossary.html" "/glossary/" "Glossary"
for slug in why-use-vpn secure-browsing-tips vpn-for-streaming vpn-for-travel vpn-vs-proxy; do
  write_redirect "public/articles/${slug}.html" "/articles/${slug}/" "Article"
done
echo "Build complete."
