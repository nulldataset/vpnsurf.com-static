# Source

This folder holds source material used by the build. The live site content lives in `public/` (e.g. from your Tailwind template zip).

| Item | Purpose | Used by |
|------|---------|---------|
| **banner_ads/** | Banner ad creative | Build copies to `public/banner-ads/` |
| **favicon.png** | Site favicon (optional) | Build copies to `public/favicon.png` if present |

To add or change banner ads, edit `banner_ads/` and run `./build.sh` (or copy manually to `public/banner-ads/`). To set the site favicon, put `favicon.png` here; the build copies it to `public/favicon.png`. New HTML, CSS, and JS come from your template (e.g. extract into `public/` or into a source folder and add a sync script).
