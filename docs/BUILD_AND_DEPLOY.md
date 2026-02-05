# Build and Deploy

This document explains how the site is built locally and how it is deployed via GitHub Actions and the Cloudron Surfer app.

---

## Local setup

- **Python 3:** Required to run the build scripts (`integrations/chatwoot/add_chatwoot.py`, `integrations/add_ad_banners.py`). Use Python 3.9 or newer.
- **Node.js (optional):** Only needed if you want to test Surfer deploy locally. Install Node.js 20+ and run `npm install -g cloudron-surfer` to use the `surfer` CLI.

---

## Build order and scripts

1. **Banner ads** — `build.sh` copies `source/banner_ads/` to `public/banner-ads/`.
2. **Favicon** — `build.sh` copies `source/favicon.png` to `public/favicon.png` if present.
3. **Content folders** — `build.sh` copies `source/articles/`, `source/pictures/`, and `source/videos/` to the corresponding `public/` paths. Add content in source and run `./build.sh` so it is reflected in public before deploy.
4. **Chatwoot** — `integrations/chatwoot/add_chatwoot.py` injects the Chatwoot script (from `integrations/chatwoot/snippet.html`) into target HTML.
5. **Ad banners** — `integrations/add_ad_banners.py` injects top/bottom 728×90 ad banners into target HTML.

By default both injector scripts target `public/articles/*.html`. If your new template uses different paths or HTML structure, edit the scripts to match.

**Single command:**

```bash
./build.sh
```

---

## Local preview (build → preview → push)

Before pushing to deploy, you can serve the built site on localhost to check it:

1. **Build** — Run `./build.sh` so `public/` is up to date.
2. **Preview** — From the repo root, run:
   ```bash
   ./scripts/preview.sh
   ```
   This serves `public/` at **http://localhost:8000**. Open that URL in your browser (e.g. http://localhost:8000/index.html). Use Ctrl+C to stop the server.
3. **Push** — When the preview looks good, commit and push to `main` or `master`. GitHub Actions will build and deploy `public/` to the Cloudron Surfer app.

The preview uses Python's built-in `http.server`, so no extra install is needed. It serves the same `public/` contents that Surfer will serve in production.

**One-liner (no script):** `python3 -m http.server 8000 --directory public` (run from repo root; ensure `public/` exists).

---

## Where the live site lives

- **Live site:** The contents of the `public/` directory are what is served at your domain. The Cloudron Surfer app serves these files.
- **Local work:** Add content in **source/** (articles, pictures, videos); run `./build.sh` to copy to **public/**. You can also add a template directly to `public/` (e.g. extract a Tailwind template zip there). Then commit and push. GitHub Actions runs the build and deploys `public/` to Surfer.

Flow: **Content in `source/` or `public/` → run `./build.sh` (copies source → public, runs injectors) → git push to `main`/`master` → GitHub Actions runs build and uploads `public/` to Surfer → your site serves the updated content.**

---

## Deploy (CI/CD)

- **Workflow:** `.github/workflows/deploy-surfer.yml`
- **Triggers:** Push to `main` or `master`; or run manually via **Actions → Deploy to Surfer → Run workflow**.
- **Steps:** Checkout → Setup Node.js 20 → Install `cloudron-surfer` → Run build → Verify connection (upload `public/index.html`) → Deploy with `surfer put public/* /` (contents of `public/` to Surfer root). The verify step expects `public/index.html` to exist; the template includes it. If you replace `public/` entirely, keep an `index.html` (or equivalent) so the verify step succeeds.

The workflow uses:

- **SURFER_SERVER:** Set as a repository **variable** (e.g. `https://yourdomain.com`). If unset, the workflow uses the default in the file.
- **SURFER_TOKEN:** Stored as a GitHub Actions **repository secret**. Create it in the Surfer app (Settings → Access Token) and add it under **Settings → Secrets and variables → Actions** as `SURFER_TOKEN`. See [SURFER_TOKEN_SECURITY.md](SURFER_TOKEN_SECURITY.md).

---

## Running deploy locally (optional)

1. Put your Surfer token in `local/surfer-token` and site URL in `local/site-url.txt` (or in `docs/temp/surfer-token`; that path is gitignored).
2. Install the Surfer CLI: `npm install -g cloudron-surfer`.
3. From the repo root, after running `./build.sh` if needed:

   ```bash
   export SURFER_TOKEN=$(tr -d '\n\r' < local/surfer-token)
   export SURFER_SERVER=$(tr -d '\n\r' < local/site-url.txt)
   surfer put --token "$SURFER_TOKEN" --server "$SURFER_SERVER" public/* /
   ```

Do not commit the token file.

---

## See also

- **Surfer token:** [SURFER_TOKEN_SECURITY.md](SURFER_TOKEN_SECURITY.md) — where the secret key lives and how to set it.
- **Chatwoot:** [integrations/chatwoot/README.md](../integrations/chatwoot/README.md) — how to embed the Chatwoot widget; snippet; config; which pages.
- **Banner ads:** [BANNER_ADS.md](BANNER_ADS.md) — 728×90 top header and bottom footer; placement; how to replace assets.
