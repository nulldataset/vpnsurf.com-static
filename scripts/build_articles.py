#!/usr/bin/env python3
"""Convert 10 numbered source markdown articles to public/articles/<slug>.html.
Run from repo root. No dates on blog posts. Only generates the 10 new slugs; does not overwrite existing 5."""
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    markdown = None  # fallback to minimal conversion

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "source" / "articles"
OUT_DIR = ROOT / "public" / "articles"
PICTURES = ("vpnsurf.com-120.gif", "vpnsurf.com-121.png", "vpnsurf.com-122.png", "vpnsurf.com-123.png",
            "vpnsurf.com-124.gif", "vpnsurf.com-125.gif", "vpnsurf.com-126.gif", "vpnsurf.com-128.png",
            "vpnsurf.com-129.gif", "vpnsurf.com-130.gif")

# Filename prefix (e.g. 01-vpn-privacy-101-...) -> URL slug
SLUG_MAP = {
    "01-vpn-privacy-101": "vpn-privacy-101",
    "02-vpn-on-ios": "vpn-on-ios",
    "03-vpn-on-android": "vpn-on-android",
    "04-vpn-for-movie-streaming": "vpn-for-movie-streaming",
    "05-vpn-for-steam-and-pc-gaming": "vpn-for-steam-and-pc-gaming",
    "06-vpn-for-video-games-on-consoles": "vpn-for-video-games-consoles-mobile",
    "07-vpn-for-corporate-work": "vpn-for-corporate-work",
    "08-vpns-for-traders": "vpns-for-traders",
    "09-vpn-for-web3": "vpn-for-web3",
    "10-advanced-vpn-privacy-and-protocols": "advanced-vpn-privacy-and-protocols",
}


def slug_from_filename(name: str) -> str | None:
    """Map 01-xxx.md, 02-xxx.md, ... to slug. Returns None if not a numbered article."""
    if not name.endswith(".md") or name.startswith("."):
        return None
    base = name[:-3]  # strip .md
    for prefix, slug in SLUG_MAP.items():
        if base == prefix or base.startswith(prefix + "-"):
            return slug
    return None


def minimal_md_to_html(text: str) -> str:
    """Convert markdown to HTML without markdown lib: # title, ## h2, **bold**, paragraphs."""
    lines = text.split("\n")
    out = []
    in_para = False
    for line in lines:
        if line.startswith("# "):
            if in_para:
                out.append("</p>")
                in_para = False
            out.append(f"<h1>{_escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            if in_para:
                out.append("</p>")
                in_para = False
            out.append(f"<h2 class=\"text-xl font-medium text-white mt-8 mb-2\">{_escape(line[3:].strip())}</h2>")
        elif line.strip() == "":
            if in_para:
                out.append("</p>")
                in_para = False
        else:
            if not in_para:
                out.append("<p>")
                in_para = True
            else:
                out.append(" ")
            # Simple **bold** and escape
            out.append(_bold_and_escape(line.strip()))
    if in_para:
        out.append("</p>")
    html = "\n".join(out)
    # Add Tailwind classes to common tags
    html = re.sub(r"<strong>", r'<strong class="text-white">', html)
    html = re.sub(r"<a ", r'<a class="text-cyan-400 hover:underline transition-colors duration-200" ', html)
    return html


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _bold_and_escape(s: str) -> str:
    """Replace **x** with <strong class="text-white">x</strong> and escape."""
    s = _escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r'<strong class="text-white">\1</strong>', s)
    return s


def md_to_html(text: str) -> str:
    """Convert markdown body to HTML with Tailwind-friendly classes."""
    if markdown is not None:
        html = markdown.markdown(
            text,
            extensions=["extra", "nl2br"],
            output_format="html5",
        )
        html = re.sub(r"<strong>", r'<strong class="text-white">', html)
        html = re.sub(r"<a ", r'<a class="text-cyan-400 hover:underline transition-colors duration-200" ', html)
        html = re.sub(r"<h2>", r'<h2 class="text-xl font-medium text-white mt-8 mb-2">', html)
        return html
    return minimal_md_to_html(text)


def parse_article(md_path: Path) -> tuple[str, str, str]:
    """Return (title, excerpt, body_html). First # line = title; rest = body. No dates."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    title = ""
    body_lines = []
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        body_lines.append(line)
    body_md = "\n".join(body_lines).strip()
    # Excerpt: first paragraph of body (no markdown headers)
    excerpt = ""
    for line in body_md.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            continue
        if line:
            excerpt = line[:160] + ("…" if len(line) > 160 else "")
            break
    body_html = md_to_html(body_md)
    return title, excerpt, body_html


def build_article_html(slug: str, title: str, excerpt: str, body_html: str, hero_img: str) -> str:
    """Full article page HTML (same structure as why-use-vpn). No date."""
    title_esc = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    excerpt_esc = excerpt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title_esc} — VPNsurf.com Blog</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="{excerpt_esc}">
    <link rel="canonical" href="https://vpnsurf.com/articles/{slug}/">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.cdnfonts.com/css/inter?styles=135009,135005,135007,135002,135000" rel="stylesheet" />
    <link rel="stylesheet" href="../../css/tailwind/tailwind.min.css">
    <link rel="icon" type="image/png" sizes="32x32" href="../../favicon.png">
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js" defer></script>
</head>
<body class="antialiased bg-body text-body font-body">
    <div class="">
      <section class="bg-gradient-to-r from-neutral-950 via-neutral-900 to-neutral-950" x-data="{{ mobileNavOpen: false }}">
        <div class="container px-4 mx-auto">
          <nav class="flex justify-between items-center py-8">
            <a href="../../" class="text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-300">VPNsurf.com</a>
            <div class="lg:hidden">
              <button x-on:click="mobileNavOpen = !mobileNavOpen" class="block hover:text-white text-neutral-300 focus:outline-none transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewbox="0 0 20 20"><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path></svg>
              </button>
            </div>
            <ul class="hidden lg:flex ml-auto mr-8 items-center w-auto space-x-8">
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../">Home</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Blog</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../faq/">FAQ</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../glossary/">Glossary</a></li>
            </ul>
            <a class="hidden lg:block px-4 py-2 text-sm font-semibold text-neutral-950 bg-white hover:bg-neutral-100 rounded-full transition-all duration-200 hover:shadow-lg" href="#">Get Started</a>
          </nav>
          <div class="ad-banner ad-banner-top w-full bg-neutral-900/80 border-y border-neutral-800 py-3">
            <div class="container px-4 mx-auto max-w-4xl">
          <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block rounded-lg overflow-hidden border border-neutral-700 shadow-lg hover:border-neutral-600 transition-colors" aria-label="Advertisement">
            <img src="../../banner-ads/gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="w-full h-auto block"/>
          </a>
            </div>
          </div>
          <section class="pt-12 pb-20">
            <div class="max-w-3xl mx-auto">
              <a href="../" class="inline-flex items-center text-sm text-neutral-400 hover:text-white transition-colors duration-200 mb-6">← Back to Blog</a>
              <article class="relative">
                <div class="absolute inset-0 opacity-20 bg-gradient-to-r from-cyan-950 via-cyan-800 to-cyan-950 rounded-2xl filter blur-3xl"></div>
                <div class="relative p-1 border border-white border-opacity-20 rounded-2xl">
                  <div class="p-8 md:p-10 lg:p-12 bg-gradient-to-bl from-neutral-950 via-neutral-900 to-neutral-950 border border-white border-opacity-20 rounded-xl">
                    <header class="mb-8">
                      <h1 class="text-3xl md:text-4xl lg:text-5xl font-medium leading-tight text-transparent bg-clip-text bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300 mb-4">{title_esc}</h1>
                      <p class="text-lg text-neutral-400">{excerpt_esc}</p>
                    </header>
                    <figure class="mb-10 rounded-xl overflow-hidden border border-neutral-800 p-1 bg-neutral-900">
                      <img src="../../pictures/{hero_img}" alt="{title_esc}" class="w-full h-64 md:h-80 object-cover rounded-lg"/>
                    </figure>
                    <div class="text-neutral-300 space-y-6 text-lg leading-relaxed">
{body_html}
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>
        <div :class="{{'block': mobileNavOpen, 'hidden': !mobileNavOpen}}" class="hidden fixed top-0 left-0 bottom-0 w-5/6 max-w-sm z-50">
          <div x-on:click="mobileNavOpen = !mobileNavOpen" class="fixed inset-0 bg-neutral-950 opacity-75 filter blur-3xl"></div>
          <nav class="relative flex flex-col py-6 px-6 w-full h-full bg-neutral-900 border-r border-neutral-800 overflow-y-auto">
            <div class="flex items-center mb-12">
              <a href="../../" class="mr-auto text-lg font-semibold text-white">VPNsurf.com</a>
              <button x-on:click="mobileNavOpen = !mobileNavOpen"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-neutral-400" fill="none" viewbox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
            </div>
            <ul>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../../">Home</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../">Blog</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../../faq/">FAQ</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../../glossary/">Glossary</a></li>
            </ul>
          </nav>
        </div>
      </section>

      <footer class="py-20 bg-gradient-to-r from-neutral-950 via-neutral-900 to-neutral-950">
        <div class="container px-4 mx-auto">
          <div class="flex flex-wrap -mx-4 mb-8 lg:mb-16">
            <div class="w-full lg:w-1/3 px-4 mb-12 lg:mb-0">
              <a class="flex items-center text-white text-xl leading-none font-semibold" href="../../"><span class="text-transparent bg-clip-text bg-gradient-to-r from-gray-100 via-gray-300 to-gray-100">VPNsurf.com</span></a>
              <p class="mt-5 mb-6 max-w-xs text-neutral-300 leading-relaxed">Private, fast VPN for everyday browsing. No logs, no hassle.</p>
              <div class="text-sm text-neutral-300 space-y-2">
                <p><a href="mailto:info@vpnsurf.com" class="hover:text-white transition-colors duration-200">info@vpnsurf.com</a></p>
                <p><a href="tel:+18552892773" class="hover:text-white transition-colors duration-200">1-855-289-2773</a></p>
                <p><a href="tel:+18552892773" class="hover:text-white transition-colors duration-200">1-855-BUY-ASSET</a></p>
              </div>
            </div>
            <div class="w-full lg:w-2/3 px-4">
              <div class="flex flex-wrap justify-between">
                <div class="w-1/2 lg:w-1/4 mb-8 lg:mb-0">
                  <h3 class="mb-6 text-lg font-medium text-transparent bg-clip-text bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300">Site</h3>
                  <ul class="text-sm">
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../">Home</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Blog</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../faq/">FAQ</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../glossary/">Glossary</a></li>
                  </ul>
                </div>
                <div class="w-1/2 lg:w-1/4 mb-8 lg:mb-0">
                  <h3 class="mb-6 text-lg font-medium text-transparent bg-clip-text bg-gradient-to-r from-gray-100 via-gray-200 to-gray-300">Legal</h3>
                  <ul class="text-sm">
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="#">Privacy</a></li>
                    <li><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="#">Terms</a></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <div class="border-t border-neutral-700 pt-8">
            <p class="lg:text-center text-sm text-neutral-400">© VPNsurf.com. All rights reserved.</p>
          </div>
        </div>
      </footer>
      <div class="ad-banner ad-banner-bottom w-full bg-neutral-900/80 border-y border-neutral-800 py-3">
        <div class="container px-4 mx-auto max-w-4xl">
          <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block rounded-lg overflow-hidden border border-neutral-700 shadow-lg hover:border-neutral-600 transition-colors" aria-label="Advertisement">
            <img src="../../banner-ads/gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="w-full h-auto block"/>
          </a>
        </div>
      </div>
    </div>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js" defer></script>
</body>
</html>
'''


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Only process 01- through 10- *.md (exclude glossary and README)
    md_files = sorted(SOURCE_DIR.glob("*.md"))
    generated = []
    for i, md_path in enumerate(md_files):
        slug = slug_from_filename(md_path.name)
        if slug is None:
            continue
        title, excerpt, body_html = parse_article(md_path)
        hero_img = PICTURES[i % len(PICTURES)]
        html = build_article_html(slug, title, excerpt, body_html, hero_img)
        out_path = OUT_DIR / f"{slug}.html"
        out_path.write_text(html, encoding="utf-8")
        generated.append((slug, title, excerpt, hero_img))
        print(f"Wrote {out_path}")
    print(f"Generated {len(generated)} article(s).")


if __name__ == "__main__":
    main()
