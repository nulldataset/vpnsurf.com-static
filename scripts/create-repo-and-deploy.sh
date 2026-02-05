#!/usr/bin/env bash
# Create the GitHub repo (if missing), push, and configure deploy (SURFER_TOKEN + SURFER_SERVER).
# Use this when you have a local repo with content and local/surfer-token + local/site-url.txt
# but no GitHub repo yet, or when you want one command to "create repo + configure Actions + push".
#
# Requires: GitHub CLI (gh) installed and authenticated (run 'gh auth login' once, or set GH_TOKEN).
# Cursor IDE: "Connected to GitHub" does not log in the gh CLI; see docs/CURSOR_GITHUB_AUTOMATION.md.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

REPO_NAME="${1:-}"

if ! command -v gh &>/dev/null; then
  echo "Error: GitHub CLI (gh) is not installed. Install: https://cli.github.com/"
  exit 1
fi

if ! gh auth status &>/dev/null; then
  echo "Error: GitHub CLI is not logged in. The script needs 'gh' to create the repo and set secrets."
  echo ""
  echo "  Option A — Log in once in your terminal:"
  echo "    gh auth login"
  echo ""
  echo "  Option B — Use a token (e.g. for Cursor/automation):"
  echo "    Create a token at https://github.com/settings/tokens (scope: repo)"
  echo "    Then run:  export GH_TOKEN=your_token"
  echo "    Then run this script again."
  echo ""
  echo "  See docs/CURSOR_GITHUB_AUTOMATION.md for Cursor IDE and automation."
  exit 1
fi

# Default repo name from directory name
if [ -z "$REPO_NAME" ]; then
  REPO_NAME="$(basename "$(realpath "$ROOT")")"
fi

# Ensure we're in a git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Error: Not a git repository. Run 'git init' in $ROOT first."
  exit 1
fi

# Create GitHub repo and add remote if no origin
if ! git remote get-url origin &>/dev/null; then
  echo "No remote 'origin' found. Creating GitHub repo '$REPO_NAME' and adding origin..."
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --description "Static site deployed to Cloudron Surfer"
  echo "Repo created and remote 'origin' set."
else
  echo "Remote 'origin' already set. Skipping repo creation."
fi

# Configure deploy (SURFER_TOKEN + SURFER_SERVER) from local/
if [ -f "$ROOT/scripts/setup-deploy.sh" ]; then
  echo "Configuring deploy (SURFER_TOKEN and SURFER_SERVER from local/)..."
  "$ROOT/scripts/setup-deploy.sh"
else
  echo "Warning: scripts/setup-deploy.sh not found. Set SURFER_TOKEN and SURFER_SERVER in GitHub repo Settings → Actions."
fi

# Push to trigger the workflow
echo "Pushing to origin (this will trigger the Deploy to Surfer workflow)..."
if git push -u origin main 2>/dev/null; then
  echo "Pushed 'main'. GitHub Actions should run the deploy workflow."
elif git push -u origin master 2>/dev/null; then
  echo "Pushed 'master'. GitHub Actions should run the deploy workflow."
else
  echo "Push failed or no commits to push. If you have uncommitted changes:"
  echo "  git add . && git commit -m 'Add site' && git push -u origin main"
fi
