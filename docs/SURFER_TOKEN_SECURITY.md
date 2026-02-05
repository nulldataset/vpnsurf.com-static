# Surfer Token Security

This document explains where the Cloudron Surfer access token **must not** go, where it **does** go, and how to set it up once for a new Surfer app.

---

## Where the token must NOT go

- **Not in the repository:** Never commit the token. Do not add it to any tracked file (e.g. config files, env files, or scripts that get committed).
- **Not in unignored files:** Do not store the token in a file under a path that is tracked by git, unless that path is in `.gitignore`.
- **Not in logs or output:** The GitHub Actions workflow never echoes or logs the token. When running Surfer locally, do not `echo` or `print` the token.

---

## Where the token DOES go

- **GitHub Actions (CI):** The token is supplied as a **repository secret** named `SURFER_TOKEN`. In the workflow it is passed to the job via `env: SURFER_TOKEN: ${{ secrets.SURFER_TOKEN }}`. It is only used in the shell as an environment variable and is never written to logs. GitHub masks secret values in job output.
- **Local use (optional):** Store the token in **`local/surfer-token`** (in [.gitignore](../.gitignore)) to run **`./scripts/setup-deploy.sh`** — the script reads it and sets the GitHub repo secret via the GitHub CLI, so you don’t have to add the secret manually in Settings. You may also store it in `docs/temp/` for local `surfer put` commands; do not commit either file or move them to a tracked location.

---

## One-time setup for a new Surfer app

When you create a new static site using this repo as a template and a new Cloudron Surfer app:

1. In the **Surfer app** (Cloudron): Open **Settings → Access Token**, create a new token, and copy it.
2. In **GitHub**: Either run **`./scripts/setup-deploy.sh`** (with the token in `local/surfer-token` and the site URL in `local/site-url.txt`) so the script sets the secret and variable via the GitHub CLI, or do it manually: open your repo → **Settings → Secrets and variables → Actions** → add a **repository secret** named `SURFER_TOKEN` and a **repository variable** named `SURFER_SERVER` (e.g. `https://yourdomain.com`). Do not add the token to the repo in any other way.

After that, every run of the deploy workflow (on push to `main`/`master` or manual) will use the secret without you re-entering the token. For new sites, create a new token in the Surfer app and a new `SURFER_TOKEN` secret (or use a different repo with its own secret).

---

## What the workflow does with the token

- **Trimming:** The workflow runs `SURFER_TOKEN=$(printf '%s' "$SURFER_TOKEN" | tr -d '\n\r')` so that if the token was copy-pasted with trailing newlines, the CLI still receives a single line. This does not expose the token; it only normalizes it.
- **Usage:** The token is passed to `surfer put` as `--token "$SURFER_TOKEN"`. It is never written to disk in the runner or echoed.

Only one secret is required: `SURFER_TOKEN`. The server URL (`SURFER_SERVER`) can be set in the workflow or as a repository variable and does not need to be a secret.
