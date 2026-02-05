# Workspace organization (surfer-static)

This document describes the folder layout for **surfer-static**. The site is ready for new content; deploy is via Cloudron Surfer and GitHub Actions. Rename the local folder to `surfer-static` when publishing as the GitHub template repo.

---

## Folder structure

```
├── .github/workflows/           # CI/CD (deploy to Surfer)
├── integrations/               # Third-party: Chatwoot + ad banners
│   ├── chatwoot/               # snippet.html + add_chatwoot.py (injects widget)
│   ├── add_ad_banners.py       # Injects 728×90 top/bottom ad banners
│   └── README.md
├── template/                   # Example site template (Tailwind 4 + HTML); LLM uses this + source content to build site in public/
│   └── README.md               # Purpose and LLM instructions
├── scripts/
│   └── setup-deploy.sh         # Sets GitHub SURFER_TOKEN + SURFER_SERVER from local/
├── local/                      # Per-site inputs (gitignored: surfer-token, site-url.txt)
│   ├── README.txt              # Instructions; copy .sample files and run setup-deploy.sh
│   ├── surfer-token.sample
│   └── site-url.txt.sample
├── source/
│   ├── banner_ads/             # Banner ad creative (all sizes); build copies to public/banner-ads/
│   │   └── README.md
│   ├── articles/               # Article content; build copies to public/articles/ (injectors run there)
│   ├── pictures/               # Images; build copies to public/pictures/
│   ├── videos/                 # Video assets; build copies to public/videos/
│   ├── favicon.png             # Optional; build copies to public/favicon.png if present
│   └── README.md
├── docs/                       # Project documentation
│   ├── temp/                   # Gitignored (e.g. Surfer token for local CLI)
│   ├── QUICKSTART_CLI.md       # New site from template using local/ + setup-deploy.sh
│   ├── NEW_SITE_FLOW.md        # Full stack: GoDaddy → Cloudflare → Cloudron → GitHub
│   ├── BUILD_AND_DEPLOY.md
│   ├── BANNER_ADS.md           # 728×90 top header and bottom footer; placement
│   └── SURFER_TOKEN_SECURITY.md
├── public/                     # Built static site (deploy target)
│   ├── index.html              # Placeholder until you add your template
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── favicon.png
│   ├── banner-ads/             # Populated by build from source/banner_ads
│   ├── articles/               # Populated by build from source/articles (injectors target here)
│   ├── pictures/               # Populated by build from source/pictures
│   └── videos/                 # Populated by build from source/videos
├── build.sh                    # Build: copy source content + banner ads, then Chatwoot + ad banner injection
├── AGENTS.md                   # High-level plan (surfer-static)
├── ORGANIZATION.md             # This file
└── README.md                   # Entry point: use template, setup, build, deploy, docs
```

---

## Documentation index

| Doc | Purpose |
|-----|---------|
| [README.md](README.md) | Entry point: use template, setup, build, deploy; links to all docs. Refer to [AGENTS.md](AGENTS.md) for LLM/agent context. |
| [AGENTS.md](AGENTS.md) | High-level plan: template for Surfer static sites; deploy flow; per-repo config; integrations. |
| [docs/QUICKSTART_CLI.md](docs/QUICKSTART_CLI.md) | New site from template using `local/` and `./scripts/setup-deploy.sh` (gh CLI). |
| [docs/NEW_SITE_FLOW.md](docs/NEW_SITE_FLOW.md) | Full stack (GoDaddy → Cloudflare → Cloudron → GitHub); manual vs automated. |
| [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) | Build order and deploy (Actions, Surfer CLI, local deploy). |
| [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md) | Where the Surfer secret key lives (repo secret, local/surfer-token); how to set it; do not commit. |
| [docs/BANNER_ADS.md](docs/BANNER_ADS.md) | 728×90 top header and bottom footer; where they’re placed; how to replace. |
| [integrations/chatwoot/README.md](integrations/chatwoot/README.md) | How to embed Chatwoot; snippet location; config; which pages; how to extend. |
| [integrations/README.md](integrations/README.md) | Overview of Chatwoot and ad-banner integrations. |

---

## Where to find things

| I want to… | Look here |
|------------|-----------|
| Add or change banner ad creative | `source/banner_ads/` (build copies to `public/banner-ads/`) |
| Set favicon | `source/favicon.png` (build copies to `public/favicon.png`) or put `public/favicon.png` directly |
| Add or change chat (Chatwoot) | `integrations/chatwoot/` |
| Add articles, images, or videos | `source/articles/`, `source/pictures/`, `source/videos/` — run `./build.sh` to copy to `public/` |
| Add main site code template (e.g. Tailwind 4) | `template/` — put your theme here; LLM uses it + source content to build the site in `public/` |
| Add new site content / template | Extract your Tailwind template into `public/` or `template/`, or add content in `source/` and run `./build.sh` |
| Configure deploy (token + URL) | Put token in `local/surfer-token`, URL in `local/site-url.txt` (copy from `local/*.sample`), then run `./scripts/setup-deploy.sh` |
| Run the build | `./build.sh` or copy banner_ads + `python3 integrations/chatwoot/add_chatwoot.py` + `python3 integrations/add_ad_banners.py` |
| Inspect built site | `public/` (deploy target) |

---

## Build and deploy

- **Live site:** The contents of `public/` are deployed via GitHub Actions and the Cloudron Surfer app. Set the repository variable `SURFER_SERVER` (e.g. via `./scripts/setup-deploy.sh` from `local/site-url.txt`) or in Settings → Actions → Variables.
- **Surfer token:** Stored as a GitHub Actions repository secret (`SURFER_TOKEN`). Put it in `local/surfer-token` (gitignored) and run `./scripts/setup-deploy.sh` to set the secret; or add it manually in Settings → Actions. Optionally in `docs/temp/` for local Surfer CLI. See [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) and [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md).
