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
├── source/
│   ├── banner_ads/             # Banner ad creative (all sizes); build copies to public/banner-ads/
│   │   └── README.md
│   ├── favicon.png             # Optional; build copies to public/favicon.png if present
│   └── README.md
├── docs/                       # Project documentation
│   ├── temp/                   # Gitignored (e.g. Surfer token)
│   ├── BUILD_AND_DEPLOY.md
│   ├── BANNER_ADS.md           # 728×90 top header and bottom footer; placement
│   └── SURFER_TOKEN_SECURITY.md
├── public/                     # Built static site (deploy target)
│   ├── index.html              # Placeholder until you add your template
│   ├── robots.txt
│   ├── sitemap.xml
│   ├── favicon.png
│   └── banner-ads/             # Populated by build from source/banner_ads
├── build.sh                    # Build: banner ads copy, Chatwoot injection, ad banner injection
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
| [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) | Build order and deploy (Actions, Surfer CLI, local deploy). |
| [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md) | Where the Surfer secret key lives (repo secret); how to set it; do not commit. |
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
| Add new site content / template | Extract your Tailwind template into `public/` (or add a sync script and source folder) |
| Run the build | `./build.sh` or copy banner_ads + `python3 integrations/chatwoot/add_chatwoot.py` + `python3 integrations/add_ad_banners.py` |
| Inspect built site | `public/` (deploy target) |

---

## Build and deploy

- **Live site:** The contents of `public/` are deployed via GitHub Actions and the Cloudron Surfer app. Set the repository variable `SURFER_SERVER` to your domain (e.g. `https://yourdomain.com`).
- **Surfer token:** Stored as a GitHub Actions repository secret (`SURFER_TOKEN`). For local CLI use, you may store it in `docs/temp/` (gitignored). See [docs/BUILD_AND_DEPLOY.md](docs/BUILD_AND_DEPLOY.md) and [docs/SURFER_TOKEN_SECURITY.md](docs/SURFER_TOKEN_SECURITY.md).
