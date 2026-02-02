#!/usr/bin/env python3
"""Inject 728x90 top/bottom ad banners into target HTML pages. Run from repo root."""
# Edit TOP_BANNER and BOTTOM_BANNER (href, src) to use your own ad URL and image filename.
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
# For pages in public/blog/ and public/science/, banner path is ../banner-ads/
BANNER_PREFIX = "../banner-ads/"
TOP_BANNER = f'''      <div class="ad-banner ad-banner-top w-full flex justify-center bg-slate-900/80 py-2 border-b border-slate-800">
        <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block" aria-label="Advertisement"><img src="{BANNER_PREFIX}gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="max-w-full h-auto"/></a>
      </div>
'''
BOTTOM_BANNER = f'''      <div class="ad-banner ad-banner-bottom w-full flex justify-center bg-slate-900/80 py-2 border-t border-slate-800">
        <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block" aria-label="Advertisement"><img src="{BANNER_PREFIX}gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="max-w-full h-auto"/></a>
      </div>
'''


def add_to_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    changed = False
    if "ad-banner-top" not in text:
        text = text.replace("      </nav>\n      <section", TOP_BANNER.rstrip() + "\n      <section")
        changed = True
    if "ad-banner-bottom" not in text:
        text = text.replace(
            "      </footer>\n    </div>\n    <script type=\"text/javascript\" src=",
            "      </footer>\n" + BOTTOM_BANNER + "    </div>\n    <script type=\"text/javascript\" src=",
        )
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path}")
    return changed


def main():
    count = 0
    for subdir in ("blog", "science"):
        for f in (PUBLIC / subdir).glob("*.html"):
            if add_to_file(f):
                count += 1
    print(f"Ad banners: {count} file(s) updated.")


if __name__ == "__main__":
    main()
