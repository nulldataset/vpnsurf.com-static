# Chatwoot embed

How to embed the Chatwoot chat widget on your static site.

---

## What it is

The Chatwoot chat widget is loaded via a snippet of JavaScript. The snippet lives in **`integrations/chatwoot/snippet.html`**. The build script **`integrations/chatwoot/add_chatwoot.py`** can inject this snippet into target HTML pages so you don’t have to paste it into every page by hand.

---

## How to get the embed code

1. **Use the snippet in this repo:** Open **`integrations/chatwoot/snippet.html`**.
2. **Get your website token:** In Chatwoot, go to **Inbox → Settings → Website channel** and copy the **Website token**.
3. **Configure the snippet:** In `snippet.html`, set:
   - **BASE_URL** — Your Chatwoot server (e.g. `https://messg.com` or your self-hosted URL).
   - **websiteToken** — The token you copied from the Website channel.

The snippet is a `<script>...</script>` block. The build script reads this file and injects it into target pages.

---

## Where it’s placed (automatic injection)

- **Location:** The script is injected **just before `</body>`** on each target page.
- **Exact pattern:** The injector looks for `</script>\n</body>` and inserts the Chatwoot snippet between them. Your HTML must contain that pattern (e.g. a closing `</script>` followed by a newline and `</body>`).
- **Default target pages:** By default the script runs only on:
  - `public/articles/*.html`

If your site uses different paths, edit **`integrations/chatwoot/add_chatwoot.py`** to target your pages (see below).

---

## How to add the widget to more pages

1. **Edit the injector:** Open **`integrations/chatwoot/add_chatwoot.py`**. In `main()`, the script loops over subdirs (by default `("articles",)`) and globs `*.html` in each. Add more subdirs (e.g. `"docs"`) or change the glob to match your structure.
2. **Ensure HTML pattern:** Each target page must contain `</script>\n</body>` so the injector can insert the snippet. Most templates that have a script block before `</body>` already do.
3. **Run the build:** Run `./build.sh` or `python3 integrations/chatwoot/add_chatwoot.py`. The script will inject the snippet into all matching pages that don’t already have `chatwootSDK` in them.

---

## Manual embed (no script)

To add the widget to a single page or a template without using the injector:

1. Copy the **entire contents** of **`integrations/chatwoot/snippet.html`** (the `<script>...</script>` block).
2. Paste it into your HTML where you want the chat launcher to appear—typically just before `</body>`.
3. Save. No need to run `add_chatwoot.py` for that page.

---

## Placement and behavior

- **Inside `<body>`:** The snippet is placed near the end of `<body>` so the chat launcher renders after main content.
- **Async load:** The script loads asynchronously; do not wrap it in `defer` in a way that breaks the Chatwoot loader.
- **Sitewide:** Once injected (or manually added), the widget appears on every page that includes the snippet.

---

## Build

- **Automatic:** Run **`./build.sh`** (which runs `integrations/chatwoot/add_chatwoot.py`).
- **Manual:** From the repo root, run **`python3 integrations/chatwoot/add_chatwoot.py`**. The script reads `snippet.html` from this folder and updates matching HTML files under `public/`.
