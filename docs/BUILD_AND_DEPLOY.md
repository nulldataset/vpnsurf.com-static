# Build and Deploy

This document explains how the site is built locally and how it is deployed via GitHub Actions and the Cloudron Surfer app.

---

## Local setup

- **Python 3:** Required to run the build scripts (`integrations/chatwoot/add_chatwoot.py`, `integrations/add_ad_banners.py`). Use Python 3.9 or newer.
- **Node.js (optional):** Only needed if you want to test Surfer deploy locally. Install Node.js 20+ and run `npm install -g cloudron-surfer` to use the `surfer` CLI.

---

## Build order and scripts

1. **Banner ads** — `build.sh` copies `source/banner_ads/` to `public/banner-ads/`.
2. **Chatwoot** — `integrations/chatwoot/add_chatwoot.py` injects the Chatwoot script (from `integrations/chatwoot/snippet.html`) into target HTML.
3. **Ad banners** — `integrations/add_ad_banners.py` injects top/bottom 728×90 ad banners into target HTML.

By default both scripts target `public/blog/*.html` and `public/science/*.html`. If your new template uses different paths or HTML structure, edit the scripts to match.

**Single command:**

```bash
./build.sh
```

---

## Where the live site lives

- **Live site:** The contents of the `public/` directory are what is served at your domain. The Cloudron Surfer app serves these files.
- **Local work:** Add your template content to `public/` (e.g. extract a Tailwind template zip there), run the build, then commit and push. GitHub Actions deploys `public/` to Surfer.

Flow: **Local `public/` → git push to `main`/`master` → GitHub Actions runs → Surfer CLI uploads `public/` to the Surfer app → your site serves the updated content.**

---

## Deploy (CI/CD)

- **Workflow:** `.github/workflows/deploy-surfer.yml`
- **Triggers:** Push to `main` or `master`; or run manually via **Actions → Deploy to Surfer → Run workflow**.
- **Steps:** Checkout → Setup Node.js 20 → Install `cloudron-surfer` → Verify connection (upload `public/index.html`) → Deploy by uploading root files and each top-level directory under `public/`.

The workflow uses:

- **SURFER_SERVER:** Set as a repository **variable** (e.g. `https://yourdomain.com`). If unset, the workflow uses the default in the file.
- **SURFER_TOKEN:** Stored as a GitHub Actions **repository secret**. Create it in the Surfer app (Settings → Access Token) and add it under **Settings → Secrets and variables → Actions** as `SURFER_TOKEN`. See [SURFER_TOKEN_SECURITY.md](SURFER_TOKEN_SECURITY.md).

---

## Running deploy locally (optional)

1. Put your Surfer access token in a file under `docs/temp/` (e.g. `docs/temp/surfer-token`). The folder `docs/temp/` is in `.gitignore`.
2. Install the Surfer CLI: `npm install -g cloudron-surfer`.
3. From the repo root:

   ```bash
   export SURFER_TOKEN=$(tr -d '\n\r' < docs/temp/surfer-token)
   export SURFER_SERVER=https://yourdomain.com
   surfer put --token "$SURFER_TOKEN" --server "$SURFER_SERVER" public/index.html public/*.html public/sitemap.xml public/robots.txt public/favicon.png /
   for dir in public/*/; do surfer put --token "$SURFER_TOKEN" --server "$SURFER_SERVER" "$dir" /; done
   ```

Do not commit the token file.

---

## See also

- **Surfer token:** [SURFER_TOKEN_SECURITY.md](SURFER_TOKEN_SECURITY.md) — where the secret key lives and how to set it.
- **Chatwoot:** [integrations/chatwoot/README.md](../integrations/chatwoot/README.md) — how to embed the Chatwoot widget; snippet; config; which pages.
- **Banner ads:** [BANNER_ADS.md](BANNER_ADS.md) — 728×90 top header and bottom footer; placement; how to replace assets.
