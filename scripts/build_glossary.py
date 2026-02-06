#!/usr/bin/env python3
"""Build public/glossary.html from source/articles/vpnsurf_vpn_glossary_100_terms.md.
Run from repo root. No dates on the glossary page."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source" / "articles" / "vpnsurf_vpn_glossary_100_terms.md"
OUT = ROOT / "public" / "glossary.html"

# Strip this line from definitions (and variants)
VPNSURF_LINE_RE = re.compile(
    r'\s*\[https://vpnsurf\.com/\]\(https://vpnsurf\.com/\)\s*—\s*VPNsurf\.com™\s*$',
    re.IGNORECASE
)


def parse_terms(md_path: Path) -> list[tuple[str, str]]:
    """Parse ## N. Term Name sections; return list of (term, definition)."""
    text = md_path.read_text(encoding="utf-8")
    terms = []
    # Skip title/intro until first ## N.
    section_re = re.compile(r'^##\s+\d+\.\s+(.+)$', re.MULTILINE)
    for m in section_re.finditer(text):
        term_name = m.group(1).strip()
        start = m.end()
        next_m = section_re.search(text, start)
        end = next_m.start() if next_m else len(text)
        definition = text[start:end]
        # Normalize: strip vpnsurf line, collapse newlines to spaces, trim
        definition = VPNSURF_LINE_RE.sub("", definition)
        definition = re.sub(r'\n\s*', ' ', definition).strip()
        definition = html.escape(definition)
        terms.append((term_name, definition))
    return terms


def build_html(terms: list[tuple[str, str]]) -> str:
    """Full glossary page HTML (same layout as current glossary.html). No dates."""
    dl_parts = []
    for i, (term, definition) in enumerate(terms):
        term_esc = html.escape(term)
        border_class = "border-b border-neutral-800 pb-8" if i < len(terms) - 1 else "pb-8"
        dl_parts.append(f'''                <div class="{border_class}">
                  <dt class="text-lg font-semibold text-white mb-2">{term_esc}</dt>
                  <dd class="text-neutral-300">{definition}</dd>
                </div>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>VPN &amp; Security Glossary — VPNsurf.com</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Definitions for VPN and security terms: encryption, IP address, kill switch, no-logs policy, and more.">
    <link rel="canonical" href="https://vpnsurf.com/glossary/">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.cdnfonts.com/css/inter?styles=135009,135005,135007,135002,135000" rel="stylesheet" />
    <link rel="stylesheet" href="../css/tailwind/tailwind.min.css">
    <link rel="icon" type="image/png" sizes="32x32" href="../favicon.png">
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js" defer></script>
</head>
<body class="antialiased bg-body text-body font-body">
    <div class="">
      <section class="bg-gradient-to-r from-neutral-950 via-neutral-900 to-neutral-950" x-data="{{ mobileNavOpen: false }}">
        <div class="container px-4 mx-auto">
          <nav class="flex justify-between items-center py-8">
            <a href="../" class="text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-300">VPNsurf.com</a>
            <div class="lg:hidden">
              <button x-on:click="mobileNavOpen = !mobileNavOpen" class="block hover:text-white text-neutral-300 focus:outline-none transition-colors duration-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="currentColor" viewbox="0 0 20 20"><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path></svg>
              </button>
            </div>
            <ul class="hidden lg:flex ml-auto mr-8 items-center w-auto space-x-8">
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Home</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../articles/">Blog</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../faq/">FAQ</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="./">Glossary</a></li>
            </ul>
            <a class="hidden lg:block px-4 py-2 text-sm font-semibold text-neutral-950 bg-white hover:bg-neutral-100 rounded-full transition-all duration-200 hover:shadow-lg" href="#">Get Started</a>
          </nav>
          <div class="ad-banner ad-banner-top w-full bg-neutral-900/80 border-y border-neutral-800 py-3">
            <div class="container px-4 mx-auto max-w-4xl">
              <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block rounded-lg overflow-hidden border border-neutral-700 shadow-lg hover:border-neutral-600 transition-colors" aria-label="Advertisement">
                <img src="../banner-ads/gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="w-full h-auto block"/>
              </a>
            </div>
          </div>
          <section class="pt-8 pb-20">
            <div class="max-w-3xl mx-auto">
              <h1 class="text-3xl md:text-4xl font-medium text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-300 mb-2">VPN &amp; security glossary</h1>
              <p class="text-neutral-400 mb-12">Short definitions for terms we use on VPNsurf.com and across the site.</p>
              <dl class="space-y-10">
{chr(10).join(dl_parts)}
              </dl>
              <p class="mt-12 text-neutral-400 text-sm"><a href="../" class="text-cyan-400 hover:underline">← Back to home</a></p>
            </div>
          </section>
        </div>
        <div :class="{{'block': mobileNavOpen, 'hidden': !mobileNavOpen}}" class="hidden fixed top-0 left-0 bottom-0 w-5/6 max-w-sm z-50">
          <div x-on:click="mobileNavOpen = !mobileNavOpen" class="fixed inset-0 bg-neutral-950 opacity-75 filter blur-3xl"></div>
          <nav class="relative flex flex-col py-6 px-6 w-full h-full bg-neutral-900 border-r border-neutral-800 overflow-y-auto">
            <div class="flex items-center mb-12">
              <a href="../" class="mr-auto text-lg font-semibold text-white">VPNsurf.com</a>
              <button x-on:click="mobileNavOpen = !mobileNavOpen"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-neutral-400" fill="none" viewbox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
            </div>
            <ul>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../">Home</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../articles/">Blog</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../faq/">FAQ</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="./">Glossary</a></li>
            </ul>
          </nav>
        </div>
      </section>

      <div class="ad-banner ad-banner-bottom w-full bg-neutral-900/80 border-y border-neutral-800 py-3">
        <div class="container px-4 mx-auto max-w-4xl">
          <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block rounded-lg overflow-hidden border border-neutral-700 shadow-lg hover:border-neutral-600 transition-colors" aria-label="Advertisement">
            <img src="../banner-ads/gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="w-full h-auto block"/>
          </a>
        </div>
      </div>
      <footer class="py-20 bg-gradient-to-r from-neutral-950 via-neutral-900 to-neutral-950">
        <div class="container px-4 mx-auto">
          <div class="flex flex-wrap -mx-4 mb-8 lg:mb-16">
            <div class="w-full lg:w-1/3 px-4 mb-12 lg:mb-0">
              <a class="flex items-center text-white text-xl leading-none font-semibold" href="../"><span class="text-transparent bg-clip-text bg-gradient-to-r from-gray-100 via-gray-300 to-gray-100">VPNsurf.com</span></a>
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
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Home</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../articles/">Blog</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../faq/">FAQ</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="./">Glossary</a></li>
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
    </div>
</body>
</html>
'''


def main() -> None:
    if not SOURCE.exists():
        print(f"Glossary source not found: {SOURCE}")
        return
    terms = parse_terms(SOURCE)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_html(terms), encoding="utf-8")
    print(f"Wrote {len(terms)} terms to {OUT}")


if __name__ == "__main__":
    main()
