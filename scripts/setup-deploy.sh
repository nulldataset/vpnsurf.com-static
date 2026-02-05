#!/usr/bin/env bash
# Configure this repo for deploy: set SURFER_TOKEN (secret) and SURFER_SERVER (variable)
# from local/surfer-token and local/site-url.txt. Run from repo root.
# Requires: GitHub CLI (gh), and you must be logged in and in a repo with origin on GitHub.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

LOCAL_TOKEN="$ROOT/local/surfer-token"
LOCAL_URL="$ROOT/local/site-url.txt"

if ! command -v gh &>/dev/null; then
  echo "Error: GitHub CLI (gh) is not installed. Install it: https://cli.github.com/"
  exit 1
fi

if ! gh repo view &>/dev/null; then
  echo "Error: Not a GitHub repo or gh not authenticated. Run from the repo root and: gh auth login"
  exit 1
fi

if [ ! -f "$LOCAL_TOKEN" ]; then
  echo "Error: $LOCAL_TOKEN not found."
  echo "Copy local/surfer-token.sample to local/surfer-token and paste your Surfer access token (one line)."
  exit 1
fi

if [ ! -f "$LOCAL_URL" ]; then
  echo "Error: $LOCAL_URL not found."
  echo "Copy local/site-url.txt.sample to local/site-url.txt and set your site URL (one line, e.g. https://yourdomain.com)."
  exit 1
fi

# Trim newlines/carriage return (same as workflow does for token); trim trailing slash from URL
SURFER_TOKEN=$(tr -d '\n\r' < "$LOCAL_TOKEN")
SURFER_SERVER=$(tr -d '\n\r' < "$LOCAL_URL" | sed 's|/$||')

if [ -z "$SURFER_TOKEN" ]; then
  echo "Error: local/surfer-token is empty."
  exit 1
fi

if [ -z "$SURFER_SERVER" ]; then
  echo "Error: local/site-url.txt is empty."
  exit 1
fi

echo "Setting GitHub repository secret SURFER_TOKEN and variable SURFER_SERVER..."
echo "SURFER_SERVER will be: $SURFER_SERVER"

printf '%s' "$SURFER_TOKEN" | gh secret set SURFER_TOKEN
gh variable set SURFER_SERVER --body "$SURFER_SERVER"

echo "Done. You can push to main/master to deploy."
