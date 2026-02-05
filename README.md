# surfer-static — Cloudron Surfer static site template

This repo is the **surfer-static** GitHub template for building static websites that are hosted and deployed on **Cloudron** using the **Surfer** app, with **GitHub Actions** for deploy. Optional integrations: **Chatwoot** chat widget and **728×90** ad banners (top header and bottom footer). Create a new repo from it via **Use this template**.

**For AI/LLM context:** See [AGENTS.md](AGENTS.md) for the high-level plan, flow, and per-repo config for this template.

---

## Use this template

1. **Create a repo:** Click **Use this template** → **Create a new repository**.
2. **Add your site:** Put your static content in **`public/`** (e.g. extract a Tailwind or other template zip into `public/`).
3. **Configure deploy:** On **Cloudron**, install the Surfer app and assign your domain; create an access token (Surfer app → Settings → Access Token). On **GitHub**, in your new repo go to **Settings → Secrets and variables → Actions** and add:
   - **Secret** `SURFER_TOKEN` — paste the Surfer access token.
   - **Variable** `SURFER_SERVER` — your site URL (e.g. `https://yourdomain.com`).
4. **Deploy:** Push to `main` or `master`. GitHub Actions runs and uploads `public/` to your Surfer app.

**First-time checklist:** [ ] Use template → create repo. [ ] Add content to `public/`. [ ] Set **SURFER_TOKEN** (secret) and **SURFER_SERVER** (variable) in repo Settings → Actions. [ ] Push to `main` or `master`. Optional: [ ] Run `./build.sh` if using Chatwoot or banner ads.

**Quick start from the command line:** Use **`local/`** (token + site URL) and **`./scripts/setup-deploy.sh`** to configure deploy in one step. See [docs/QUICKSTART_CLI.md](docs/QUICKSTART_CLI.md).

**New site flow (full stack):** GoDaddy → Cloudflare (DNS) → Cloudron (add domain, install Surfer, create token) → new repo from this template → fill `local/surfer-token` and `local/site-url.txt` → run `./scripts/setup-deploy.sh` → push to deploy. Manual vs automated breakdown: [docs/NEW_SITE_FLOW.md](docs/NEW_SITE_FLOW.md).

---

## What’s included

- **Static site** — Placeholder content in `public/`. **`template/`** holds the example site template (e.g. Tailwind 4 CSS + HTML) — add your theme there; an LLM can use it with content from **`source/`** (articles, pictures, videos) to build the complete site in `public/`. Run **`./build.sh`** to copy source content to `public/`. See [template/README.md](template/README.md).
- **Cloudron Surfer** — Serves the contents of `public/` at your domain.
- **GitHub Actions** — On push to `main`/`master`, runs the deploy workflow and uploads `public/` to the Surfer app via the `cloudron-surfer` CLI.
- **Chatwoot** — `integrations/chatwoot/` holds the snippet; `integrations/chatwoot/add_chatwoot.py` injects it into target HTML. See [integrations/chatwoot/README.md](integrations/chatwoot/README.md) for how to embed and configure.
- **Ad banners** — `integrations/add_ad_banners.py` injects 728×90 top/bottom banners; `source/banner_ads/` is copied to `public/banner-ads/` by the build. See [docs/BANNER_ADS.md](docs/BANNER_ADS.md) for placement and how to replace assets.

---

## One-time setup (detailed)

1. **Create a Cloudron Surfer app**  
   In Cloudron, add a Surfer app and assign it to your domain (e.g. `https://yourdomain.com`).

2. **Create a Surfer access token**  
   In the Surfer app → **Settings → Access Token**, create a token and copy it.

3. **Add the token as a repository secret**  
   In your repo → **Settings → Secrets and variables → Actions** → **New repository secret**. Name: `SURFER_TOKEN`. Value: the token. Never commit the token.

4. **Set the Surfer server URL**  
   Add a **repository variable** `SURFER_SERVER` = `https://yourdomain.com` (or edit the workflow file default). See the workflow file for the variable.

5. **Add your site content**  
   Extract your Tailwind (or other) template into `public/` so the site has real pages. Optionally put the token in `docs/temp/` for local `surfer put`; that path is gitignored. See [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md).

---

## Build (optional)

If you use Chatwoot or banner ads, run the build so the script can inject them into your HTML. Run **`./build.sh`**. Full details: [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md).

```bash
./build.sh
```

This copies **`source/banner_ads/`** to **`public/banner-ads/`**, copies **`source/favicon.png`** to **`public/favicon.png`** if present, then runs **`integrations/chatwoot/add_chatwoot.py`** (Chatwoot widget) and **`integrations/add_ad_banners.py`** (728×90 top/bottom banners). By default the scripts target `public/blog/*.html` and `public/science/*.html`; if your template uses other paths, edit the scripts. See [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) for details.

- **Chatwoot:** How to embed and configure: [integrations/chatwoot/README.md](integrations/chatwoot/README.md).
- **Banner ads:** 728×90 top header and bottom footer, placement and how to replace assets: [docs/BANNER_ADS.md](docs/BANNER_ADS.md).

---

## Deploy

Push to `main` or `master` to trigger the **Deploy to Surfer** workflow. The workflow runs **`./build.sh`** (so banners and injections are fresh), then uploads the contents of **`public/`** to the Cloudron Surfer app. You can also run it manually under **Actions → Deploy to Surfer → Run workflow**.

- **SURFER_TOKEN:** Repository **secret** (Surfer app → Settings → Access Token). See [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md).
- **SURFER_SERVER:** Repository **variable** (e.g. `https://yourdomain.com`). Set in **Settings → Secrets and variables → Actions → Variables**. If unset, the workflow uses the default in the workflow file.

No need to re-enter the token; the workflow uses the `SURFER_TOKEN` secret.

---

## Security

- Keep the Surfer token only in GitHub Actions secrets and in **`local/surfer-token`** (gitignored) for running **`./scripts/setup-deploy.sh`**; optionally in `docs/temp/` for local Surfer CLI use.
- See [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md) for details.

---

## Documentation

| Doc | Purpose |
|-----|---------|
| [AGENTS.md](AGENTS.md) | High-level plan for this template (purpose, flow, per-repo config, integrations). **Refer to this for LLM/agent context.** |
| [docs/QUICKSTART_CLI.md](docs/QUICKSTART_CLI.md) | New site from template using `local/` and `./scripts/setup-deploy.sh` (gh CLI). |
| [docs/NEW_SITE_FLOW.md](docs/NEW_SITE_FLOW.md) | Full stack: GoDaddy → Cloudflare → Cloudron → Surfer → GitHub; manual vs automated. |
| [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) | Build order and deploy (Actions, Surfer CLI, local deploy). |
| [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md) | Where the Surfer secret key lives; how to set it. |
| [docs/BANNER_ADS.md](docs/BANNER_ADS.md) | 728×90 top header and bottom footer; placement; how to replace. |
| [integrations/chatwoot/README.md](integrations/chatwoot/README.md) | How to embed Chatwoot; snippet; config; which pages. |
| [ORGANIZATION.md](ORGANIZATION.md) | Folder layout and doc index. |
