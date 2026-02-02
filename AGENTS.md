# surfer-static — high-level plan

This repository (**surfer-static**) is the **GitHub template** for building static websites that are hosted and deployed on **Cloudron** using the **Surfer** app. Each new site uses its own Surfer app and its own GitHub repo (created from this template), with the Surfer access token stored as a repo secret and the site URL as a repo variable.

---

## Purpose

- **Template repo:** Use “Use this template” on GitHub to create a new repo for a static site.
- **Deploy target:** Cloudron Surfer app (one Surfer app per site; each app has its own domain and access token).
- **CI/CD:** GitHub Actions runs on push to `main`/`master` and uploads the contents of `public/` to the Surfer app using the `cloudron-surfer` CLI and the app’s secret key (stored as repository secret `SURFER_TOKEN`).

---

## Flow

1. **Content:** Site content lives in `public/`. Add your static HTML, CSS, JS, and assets (e.g. extract a Tailwind template into `public/`).
2. **Build (optional):** Run `./build.sh` to copy banner assets from `source/banner_ads/` to `public/banner-ads/` and to inject Chatwoot and 728×90 ad banners into target HTML (by default `public/blog/*.html` and `public/science/*.html`). If your template uses other paths, edit the integration scripts.
3. **Deploy:** Push to `main` or `master`. GitHub Actions runs the “Deploy to Surfer” workflow: it uploads `public/` to the Surfer app using the token from repo secrets. The live site is served at the URL configured in the Surfer app (and set in the repo variable `SURFER_SERVER`).

---

## Per-new-site setup

### On Cloudron

1. Install the **Surfer** app and assign it to your domain (e.g. `https://yourdomain.com`).
2. In the Surfer app, open **Settings → Access Token**, create a token, and copy it.

### On GitHub

1. Create a new repository from this template (Use this template → Create a new repository).
2. In the new repo: **Settings → Secrets and variables → Actions**.
3. Add a **repository secret** named `SURFER_TOKEN` and paste the Surfer access token.
4. Add a **repository variable** named `SURFER_SERVER` with your site URL (e.g. `https://yourdomain.com`).

GitHub Actions is enabled by default for new repos; the workflow uses these two values. No code changes are required for deploy; only the secret and variable must be set per site.

---

## Integrations (optional)

- **Chatwoot:** Embed code lives in `integrations/chatwoot/snippet.html`. The script `integrations/chatwoot/add_chatwoot.py` injects it into target pages (by default before `</body>` in `public/blog/*.html` and `public/science/*.html`). See [integrations/chatwoot/README.md](integrations/chatwoot/README.md) for how to embed and configure.
- **Banner ads:** 728×90 (leaderboard) ads for **top header** and **bottom footer**. Assets live in `source/banner_ads/`; the build copies them to `public/banner-ads/`. The script `integrations/add_ad_banners.py` injects a top banner (after `</nav>`) and a bottom banner (before the footer/script block). See [docs/BANNER_ADS.md](docs/BANNER_ADS.md) for placement and how to replace assets.

---

## Key documentation

| Doc | Purpose |
|-----|---------|
| [README.md](README.md) | Entry point: use template, full setup, build, deploy; refer here for LLM/agent context (this file, AGENTS.md, is the high-level plan). |
| [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) | Build order and deploy (Actions, Surfer CLI, local deploy). |
| [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md) | Where the Surfer secret key lives (repo secret); how to set it; do not commit. |
| [docs/BANNER_ADS.md](docs/BANNER_ADS.md) | 728×90 top header and bottom footer; where they’re placed; how to replace. |
| [integrations/chatwoot/README.md](integrations/chatwoot/README.md) | How to embed Chatwoot; snippet location; config; which pages; how to extend. |
| [ORGANIZATION.md](ORGANIZATION.md) | Folder layout and documentation index. |
