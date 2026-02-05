# Banner ads — 728×90 top header and bottom footer

How to use and place 728×90 (leaderboard) ad banners on your static site.

---

## Size and placement

- **Size:** **728×90** (leaderboard).
- **Where they go:**
  - **Top header:** One 728×90 banner at the **top** of the main content area, immediately after the main navigation (`</nav>`) and before the main content (e.g. before the first `<section>`).
  - **Bottom footer:** One 728×90 banner at the **bottom** of the page, immediately before the closing wrapper and script block (e.g. after `</footer>` and before the main `</div>` and `<script>` that loads your JS).

The build script **`integrations/add_ad_banners.py`** injects these two banners into target HTML pages. By default it targets `public/articles/*.html`. If your template uses different paths or a different HTML structure, you must edit the script (see below).

---

## Where assets live

- **Source:** Banner ad assets (GIFs or images) live in **`source/banner_ads/`**.
- **Build:** When you run **`./build.sh`**, the contents of `source/banner_ads/` are copied to **`public/banner-ads/`**. The live site serves from `public/`, so pages reference banners as `banner-ads/...` (or `../banner-ads/...` from subdirs like `articles/`).
- **Default image:** The injector script uses **`gdfn.com-728x90-xyz.gif`** for both top and bottom banners. That file (or a 728×90 replacement) must exist in `source/banner_ads/` so it is copied to `public/banner-ads/` by the build.

---

## Where they’re injected (exact patterns)

The script **`integrations/add_ad_banners.py`** looks for specific HTML patterns and inserts the banner markup. These patterns match a Shuffle-style theme; other templates may not match.

- **Top banner:** Inserted **after** `</nav>` and **before** the next `<section>`. The script looks for the string:
  - `      </nav>\n      <section`
  and inserts the top banner between `</nav>` and `<section>`.

- **Bottom banner:** Inserted **after** `</footer>` and **before** the closing `</div>` and script. The script looks for:
  - `      </footer>\n    </div>\n    <script type="text/javascript" src=`
  and inserts the bottom banner between `</footer>` and `</div>`.

If your HTML does not contain these exact patterns (e.g. different indentation, no `<section>`, or a different script tag), the script will not inject the banners. You have two options:

1. **Edit the script:** Change the strings in **`integrations/add_ad_banners.py`** to match your template’s structure (e.g. different tags or whitespace).
2. **Manual placement:** Add the banner HTML by hand in your template where you want the top and bottom ads, and do not run the injector for those pages (or skip injection and keep your manual markup).

---

## How to use your own 728×90 assets

1. **Add or replace the image:** Put your 728×90 image (e.g. GIF or PNG) in **`source/banner_ads/`**. For example `my-ad-728x90.gif`.
2. **Update the script (if needed):** If you use a different filename than `gdfn.com-728x90-xyz.gif`, open **`integrations/add_ad_banners.py`** and change the filename in `TOP_BANNER` and `BOTTOM_BANNER` (the `src=...` attribute) to your file name. You can also change the link URL (`href="..."`) to point to your campaign or site.
3. **Run the build:** Run **`./build.sh`**. This copies `source/banner_ads/` to `public/banner-ads/` and then runs the ad-banner injector. Your new image will be in `public/banner-ads/` and the script will use it if you updated the script in step 2.

You can keep multiple 728×90 files in `source/banner_ads/` and switch which one is used by editing only the filename (and optionally the link) in `add_ad_banners.py`.
