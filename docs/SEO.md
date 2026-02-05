# SEO and URL structure

## Live site SEO review (best practices)

Audit of the current site (vpnsurf.com) against SEO best practices:

### What’s already in good shape

- **Unique titles per page** — Home, FAQ, Glossary, Blog index, and each article have distinct `<title>` tags with brand (VPNsurf.com). Lengths are within the ~60-character guideline for SERP display.
- **Meta descriptions** — Every page has a unique `<meta name="description">` that summarizes the page. Keep them under ~155 characters for full display in search results.
- **Single H1 per page** — Each page has one main `<h1>` (e.g. “Browse privately…”, “Frequently asked questions”, “VPN & security glossary”, “Blog”, and article titles). Article bodies use `<h2>` for sections.
- **Semantic structure** — Homepage uses sections and headings; FAQ uses accordions; glossary uses `<dl>`/`<dt>`/`<dd>`; articles use `<article>`, `<header>`, `<figure>`.
- **Image alt text** — Content images have descriptive `alt` (e.g. “VPN encrypts your connection”, “Secure browsing with VPNsurf.com”). Ad banners use `alt="Advertisement"` and `aria-label` where appropriate.
- **Mobile viewport** — `<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">` is set on all pages.
- **Language** — `<html lang="en">` is set.
- **robots.txt** — `User-agent: *` and `Allow: /` with `Sitemap: https://vpnsurf.com/sitemap.xml` is correct.

### Gaps and recommendations

| Area | Current state | Best practice |
|------|----------------|---------------|
| **Sitemap** | Only `<loc>/</loc>` in `sitemap.xml`. | Add all indexable URLs: `/`, `/faq.html`, `/glossary.html`, `/articles/index.html`, and each article (e.g. `/articles/why-use-vpn.html`). Use absolute URLs: `https://vpnsurf.com/...`. Optionally add `<lastmod>` for freshness. |
| **Canonical URLs** | No `<link rel="canonical">` on any page. | Add one per page with the final URL (e.g. `https://vpnsurf.com/`, `https://vpnsurf.com/faq.html`, `https://vpnsurf.com/articles/why-use-vpn.html`) to avoid duplicate-content issues and consolidate signals. |
| **Open Graph** | No `og:title`, `og:description`, `og:url`, `og:type` (or `og:image`). | Add these in `<head>` so shares on social networks show the right title, description, and URL. Use the same absolute URLs as canonicals. |
| **Structured data** | None. | Consider `WebSite` + `Organization` (and per-article `Article`) JSON-LD for rich results. Optional but helpful for search and assistants. |
| **Internal links** | Nav and in-content links are present; some CTA links are `href="#"`. | Replace placeholder `#` links (e.g. “Get Started”) with real signup or contact URLs when available. |
| **URLs with .html** | All pages use `.html` in the path. | Not required for SEO; clean URLs (e.g. `/faq/`, `/articles/why-use-vpn/`) are a UX/preference improvement. See “URLs without .html” below. |

### Quick wins

1. **Expand sitemap.xml** — List every public HTML page with `https://vpnsurf.com/...` so crawlers can discover all content.
2. **Add canonicals** — In each page’s `<head>`, add `<link rel="canonical" href="https://vpnsurf.com/...">` for that page’s canonical URL.
3. **Add Open Graph tags** — At minimum: `og:title`, `og:description`, `og:url`, `og:type` (and `og:image` for key pages) using the same canonical base URL.

Use the live site URL (e.g. from `local/site-url.txt` at build time) so canonicals and OG tags stay correct across environments. No imageoptim or exiftool is required for the build.

---

## URLs without `.html`

You don’t have to use `.html` in URLs. Two common approaches:

### 1. Directory-style URLs (recommended for static)

Serve each “page” as a **directory** containing `index.html`. The URL is then the path with a trailing slash and no `.html`.

| Current (with .html)     | Clean URL (directory)           |
|--------------------------|----------------------------------|
| `/faq.html`              | `/faq/`                          |
| `/glossary.html`         | `/glossary/`                     |
| `/articles/index.html`   | `/articles/` (already clean)     |
| `/articles/why-use-vpn.html` | `/articles/why-use-vpn/`     |

**How it works:** Put the content in `faq/index.html`, `glossary/index.html`, `articles/why-use-vpn/index.html`, etc. When a user or search engine requests `https://yoursite.com/faq/`, the server returns `faq/index.html`. Most static hosts (including Surfer) do this by default.

**What to change:**
- **File layout:** For each `.html` file that should have a clean URL, create a directory with the same base name and move the file into it as `index.html`.  
  Example: `faq.html` → `faq/index.html`; `articles/secure-browsing-tips.html` → `articles/secure-browsing-tips/index.html`.
- **Links:** Update all internal links to use the path without `.html`, with a trailing slash (e.g. `href="/faq/"`, `href="articles/why-use-vpn/"`). Use root-relative or absolute paths so they work from any page.
- **Sitemap and canonicals:** Use the clean URLs in `sitemap.xml` and in `<link rel="canonical">`.

You can do this once by hand, or add a build step that (1) creates `path/index.html` from `path.html` (or from your source) and (2) rewrites internal links in the generated HTML to the clean form.

### 2. Server rewrites

Some hosts let you rewrite `/faq` → `/faq.html` so that the browser shows `/faq`. That depends on Surfer/Cloudron supporting rewrite rules. If it does, you keep your current files and add a rule; if not, directory-style URLs above are the reliable static approach.

---

## Summary

- **Exiftool / imageoptim:** Removed from the default build; no dependency on them for deploy.
- **SEO:** Titles and meta are in place; improve sitemap and add canonicals + OG when you have the live domain in the build.
- **No `.html` in URLs:** Use directory-style URLs (`path/index.html` → URL `path/`) and update links and sitemap to the clean paths.
