# New site flow: full stack (manual vs automated)

This document describes the end-to-end flow for creating and deploying a new static site with **GoDaddy → Cloudflare → Cloudron Surfer → GitHub (this template)**. It marks what stays **manual** and what is **automated** so you can run the best possible new-website flow.

---

## Stack overview

```text
GoDaddy (registrar) → Cloudflare (DNS) → Cloudron (host) → Surfer app → GitHub repo → GitHub Actions → deploy to Surfer
```

All domains use **GoDaddy** as registrar and **Cloudflare** for DNS (nameservers at GoDaddy point to Cloudflare). Cloudron is used to add the domain and install the Surfer app. This repo (one per site) holds the static content and deploys via GitHub Actions.

---

## 1. Registrar and DNS — manual

| Step | Action | Time |
|------|--------|------|
| Domain at GoDaddy | You register or already own the domain at GoDaddy. | — |
| Add domain to Cloudflare | In your Cloudflare account, add the domain. | — |
| Point GoDaddy to Cloudflare | In GoDaddy, set the domain’s nameservers to Cloudflare’s (e.g. NS1 and NS2 from Cloudflare). | — |

This is manual and stays that way; no automation in this repo.

---

## 2. Cloudron — manual

| Step | Action | Time |
|------|--------|------|
| Add domain in Cloudron | In Cloudron, add the new domain. When asked which DNS provider, choose **Cloudflare** (used for 100% of domains in this setup). | ~1 min |
| Install Surfer app | Install the **Surfer** app and assign it to this domain (e.g. `https://yourdomain.com`). | ~1 min |
| Generate Surfer token | While logged into Cloudron, open the Surfer app’s admin page (e.g. `https://yourdomain.com/_admin/`) → **Settings** → **Access Token** → create a new token. Copy the token. | — |

All of this is manual. Cloudron and Surfer do not provide a supported way in this setup to add domains or create tokens from the command line, so these steps stay human-driven.

---

## 3. GitHub repo and deploy config — mixed (manual + automated)

| Step | Action | Manual or automated |
|------|--------|----------------------|
| Create new repo | Create a new repository from **this template** (e.g. “Use this template” on GitHub, or `gh repo create my-site --template OWNER/surfer-static --clone`). | Manual (or one `gh` command) |
| Clone and add content | Clone the new repo, add your static site into **`public/`**. Optionally run **`./build.sh`** if you use Chatwoot or banner ads. | Manual |
| Save token and site URL | Create **`local/surfer-token`** (paste the Surfer token, one line) and **`local/site-url.txt`** (one line: e.g. `https://yourdomain.com`). Use the `.sample` files in `local/` as a guide. | Manual |
| Set GitHub secret and variable | Run **`./scripts/setup-deploy.sh`**. It reads `local/surfer-token` and `local/site-url.txt` and runs `gh secret set SURFER_TOKEN` and `gh variable set SURFER_SERVER`. | **Automated** (script) |
| Deploy | From Ubuntu (or any machine with git/gh): `git add .`, `git commit -m "..."`, `git push` to `main` or `master`. GitHub Actions runs and uploads **`public/`** to the Surfer app. | Push is manual; **deploy (upload) is automated** by Actions |

So: you no longer open GitHub → Settings → Secrets and variables → Actions to create **SURFER_TOKEN** and **SURFER_SERVER** by hand; the script does it from the `local/` files. On Linux (e.g. Ubuntu) you use **GitHub CLI** and **git** instead of GitHub Desktop.

---

## 4. Summary: what is manual vs automated

| Layer | Manual | Automated |
|-------|--------|-----------|
| **GoDaddy** | Register/own domain; set nameservers to Cloudflare | — |
| **Cloudflare** | Add domain; configure DNS | — |
| **Cloudron** | Add domain (Cloudflare DNS); install Surfer; generate token | — |
| **Repo setup** | Create repo from template; add content to `public/`; create and fill `local/surfer-token` and `local/site-url.txt` | **`./scripts/setup-deploy.sh`** sets GitHub secret and variable |
| **Deploy** | Run `git add` / `commit` / `push` (e.g. via `gh` or git on Ubuntu) | **GitHub Actions** runs workflow and uploads `public/` to Surfer via `cloudron-surfer` CLI |

---

## 5. Recommended order for each new site

1. **Registrar & DNS:** GoDaddy + Cloudflare (manual).
2. **Cloudron:** Add domain (Cloudflare), install Surfer on that domain, open Surfer admin and create token; copy token (manual).
3. **GitHub:** Create new repo from this template (manual or `gh repo create ... --template ...`); clone; add site to `public/` (manual).
4. **Local config:** Copy `local/surfer-token.sample` → `local/surfer-token`, `local/site-url.txt.sample` → `local/site-url.txt`; paste token and site URL (manual).
5. **Automated config:** Run **`./scripts/setup-deploy.sh`** (automated).
6. **Deploy:** **`git add . && git commit -m "Add site" && git push`** (manual trigger); Actions performs the deploy (automated).

For the repo-only steps (create repo, content, `local/` files, script, push), see [QUICKSTART_CLI.md](QUICKSTART_CLI.md).
