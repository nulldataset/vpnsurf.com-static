# Source

This folder holds source material used by the build. Add content here; run **`./build.sh`** to copy it to `public/` for the live site. You can also add a Tailwind (or other) template directly into `public/`.

| Item | Purpose | Build copies to |
|------|---------|-----------------|
| **banner_ads/** | Banner ad creative | `public/banner-ads/` |
| **favicon.png** | Site favicon (optional) | `public/favicon.png` if present |
| **articles/** | Article pages or content (Chatwoot and ad banners injected into HTML here) | `public/articles/` |
| **pictures/** | Images and photos | `public/pictures/` |
| **videos/** | Video files or assets | `public/videos/` |

To add or change banner ads, edit `banner_ads/` and run `./build.sh`. To set the site favicon, put `favicon.png` here. Add articles, images, and videos in the folders above and run `./build.sh` to copy them to `public/` for deploy.
