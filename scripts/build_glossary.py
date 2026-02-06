#!/usr/bin/env python3
"""Build public/glossary.html (index with A–Z) and public/glossary/<slug>.html (per-term pages).
Run from repo root. No dates. Updates sitemap with term URLs."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source" / "articles" / "vpnsurf_vpn_glossary_100_terms.md"
PUBLIC = ROOT / "public"
OUT_INDEX = PUBLIC / "glossary.html"
OUT_GLOSSARY_DIR = PUBLIC / "glossary"
SITEMAP = PUBLIC / "sitemap.xml"
BASE = "https://vpnsurf.com"
RELATED_CAP = 10

# Strip this line from definitions (and variants)
VPNSURF_LINE_RE = re.compile(
    r'\s*\[https://vpnsurf\.com/\]\(https://vpnsurf\.com/\)\s*—\s*VPNsurf\.com™\s*$',
    re.IGNORECASE
)


def parse_terms(md_path: Path) -> list[tuple[str, str]]:
    """Parse ## N. Term Name sections; return list of (term, definition_raw)."""
    text = md_path.read_text(encoding="utf-8")
    terms = []
    section_re = re.compile(r'^##\s+\d+\.\s+(.+)$', re.MULTILINE)
    for m in section_re.finditer(text):
        term_name = m.group(1).strip()
        start = m.end()
        next_m = section_re.search(text, start)
        end = next_m.start() if next_m else len(text)
        definition = text[start:end]
        definition = VPNSURF_LINE_RE.sub("", definition)
        definition = re.sub(r'\n\s*', ' ', definition).strip()
        terms.append((term_name, definition))
    return terms


def term_to_slug(term: str) -> str:
    """Lowercase, replace non-alphanumeric with hyphen, collapse, strip."""
    slug = re.sub(r'[^a-z0-9]+', '-', term.lower()).strip('-')
    slug = re.sub(r'-+', '-', slug)
    return slug or "term"


def ensure_unique_slugs(terms: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    """Return list of (term, definition_raw, slug) with unique slugs (suffix -2, -3 if needed)."""
    seen: dict[str, int] = {}
    out = []
    for term, definition in terms:
        base = term_to_slug(term)
        if base not in seen:
            seen[base] = 0
        seen[base] += 1
        slug = f"{base}-{seen[base]}" if seen[base] > 1 else base
        out.append((term, definition, slug))
    return out


def first_letter(term: str) -> str:
    """First alphanumeric character of term, uppercase; else #."""
    for c in term:
        if c.isalnum():
            return c.upper()
    return "#"


def linkify_definition(
    raw_definition: str,
    current_term: str,
    term_names_by_len: list[str],
    term_to_slug: dict[str, str],
) -> str:
    """Replace other term names in raw_definition with links (longest-first, no overlap)."""
    other_terms = [t for t in term_names_by_len if t != current_term]
    if not other_terms:
        return html.escape(raw_definition)
    # Collect all matches (start, end, term_name), longest first per position
    intervals: list[tuple[int, int, str]] = []
    for term in other_terms:
        slug = term_to_slug.get(term)
        if not slug:
            continue
        # Word-boundary match so "Port" does not match inside "important" or "airports"
        pattern = r"\b" + re.escape(term) + r"\b"
        for m in re.finditer(pattern, raw_definition, re.IGNORECASE):
            intervals.append((m.start(), m.end(), term))
    # Sort by start, then by length descending so longer wins
    intervals.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    # Drop overlaps: keep only if no kept interval contains this one
    kept: list[tuple[int, int, str]] = []
    for s, e, t in intervals:
        if any(k[0] <= s and k[1] >= e for k in kept):
            continue
        kept.append((s, e, t))
    kept.sort(key=lambda x: x[0])
    # Build output
    parts: list[str] = []
    pos = 0
    for s, end, t in kept:
        parts.append(html.escape(raw_definition[pos:s]))
        slug = term_to_slug[t]
        parts.append(f'<a href="../{slug}/" class="text-cyan-400 hover:underline">{html.escape(t)}</a>')
        pos = end
    parts.append(html.escape(raw_definition[pos:]))
    return "".join(parts)


def related_terms(
    current_term: str,
    current_slug: str,
    letter: str,
    terms_with_slugs: list[tuple[str, str, str]],
    by_letter: dict[str, list[tuple[str, str, str]]],
    raw_definition: str,
) -> list[tuple[str, str]]:
    """Same-letter + in-definition, dedupe by slug, cap at RELATED_CAP. Return [(term, slug)]."""
    related: list[tuple[str, str]] = []
    seen_slugs: set[str] = {current_slug}
    # Same letter first
    for t, _, slug in by_letter.get(letter, []):
        if slug != current_slug and slug not in seen_slugs:
            related.append((t, slug))
            seen_slugs.add(slug)
    # Then in-definition (term names that appear as whole words in raw_definition)
    for t, _, slug in terms_with_slugs:
        if slug in seen_slugs:
            continue
        if re.search(r"\b" + re.escape(t) + r"\b", raw_definition, re.IGNORECASE):
            related.append((t, slug))
            seen_slugs.add(slug)
    return related[:RELATED_CAP]


def build_index_html(
    terms_with_slugs: list[tuple[str, str, str]],
    by_letter: dict[str, list[tuple[str, str, str]]],
) -> str:
    """Main glossary index with A–Z strip and term links."""
    letters = sorted(c for c in by_letter.keys() if c != "#")
    if "#" in by_letter:
        letters = ["#"] + letters
    letter_links = " ".join(
        f'<a href="#letter-{c}" class="inline-block w-8 h-8 text-center leading-8 rounded hover:bg-neutral-700 text-neutral-300 font-medium">{c}</a>'
        for c in letters
    )
    sections = []
    for letter in letters:
        group = by_letter[letter]
        terms_html = []
        for term, _, slug in group:
            term_esc = html.escape(term)
            terms_html.append(f'<li><a href="./{slug}/" class="text-cyan-400 hover:underline">{term_esc}</a></li>')
        section = f'''              <section id="letter-{letter}" class="mb-12">
                <h2 class="text-xl font-semibold text-white mb-4 border-b border-neutral-700 pb-2">{letter}</h2>
                <ul class="space-y-2 text-neutral-300">
{chr(10).join(terms_html)}
                </ul>
              </section>'''
        sections.append(section)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>VPN &amp; Security Glossary — VPNsurf.com</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="100+ VPN and security terms defined: encryption, kill switch, no-logs, WireGuard, DNS leak, and more. Browse by letter or term.">
    <link rel="canonical" href="{BASE}/glossary/">
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
              <p class="text-neutral-400 mb-6">Short definitions for terms we use on VPNsurf.com. Browse by letter or open any term for the full definition and related terms.</p>
              <nav class="flex flex-wrap gap-1 mb-10" aria-label="Jump to letter">
                {letter_links}
              </nav>
              <div class="space-y-0">
{chr(10).join(sections)}
              </div>
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


def term_page_html(
    term: str,
    slug: str,
    raw_definition: str,
    definition_linked: str,
    related: list[tuple[str, str]],
    term_to_slug: dict[str, str],
) -> str:
    """Single term page with breadcrumb, H1, definition, related terms, schema."""
    meta_desc = raw_definition[:155].strip()
    if len(raw_definition) > 155:
        meta_desc = meta_desc.rsplit(" ", 1)[0] + "…"
    meta_desc = html.escape(meta_desc)
    term_esc = html.escape(term)
    title_esc = html.escape(f"What is {term}? | VPN Glossary — VPNsurf.com" if len(term) < 50 else f"{term} — VPN Glossary — VPNsurf.com")
    related_block = ""
    if related:
        related_items = " ".join(
            f'<li><a href="../{s}/" class="text-cyan-400 hover:underline">{html.escape(t)}</a></li>'
            for t, s in related
        )
        related_block = f'''              <section class="mt-10 pt-8 border-t border-neutral-800">
                <h2 class="text-lg font-semibold text-white mb-3">Related terms</h2>
                <ul class="flex flex-wrap gap-x-4 gap-y-2 text-neutral-300">
                  {related_items}
                </ul>
              </section>'''
    schema_ld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": term,
        "description": raw_definition,
        "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "VPN & Security Glossary", "url": f"{BASE}/glossary/"},
    }
    schema_json = json.dumps(schema_ld, ensure_ascii=False)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title_esc}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="{meta_desc}">
    <link rel="canonical" href="{BASE}/glossary/{slug}/">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.cdnfonts.com/css/inter?styles=135009,135005,135007,135002,135000" rel="stylesheet" />
    <link rel="stylesheet" href="../../css/tailwind/tailwind.min.css">
    <link rel="icon" type="image/png" sizes="32x32" href="../../favicon.png">
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js" defer></script>
    <script type="application/ld+json">
{schema_json}
    </script>
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
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../articles/">Blog</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../faq/">FAQ</a></li>
              <li><a class="text-sm hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Glossary</a></li>
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
          <section class="pt-8 pb-20">
            <div class="max-w-3xl mx-auto">
              <p class="text-neutral-400 text-sm mb-4"><a href="../../" class="text-cyan-400 hover:underline">Home</a> → <a href="../" class="text-cyan-400 hover:underline">Glossary</a> → <span class="text-white">{term_esc}</span></p>
              <h1 class="text-3xl md:text-4xl font-medium text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-300 mb-6">{term_esc}</h1>
              <div class="text-neutral-300 leading-relaxed">
                <p>{definition_linked}</p>
              </div>
{related_block}
              <p class="mt-10 text-neutral-400 text-sm"><a href="../" class="text-cyan-400 hover:underline">← Back to glossary</a></p>
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
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../../articles/">Blog</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../../faq/">FAQ</a></li>
              <li class="mb-1"><a class="block p-4 text-sm font-semibold hover:bg-neutral-800 hover:text-white rounded-lg text-neutral-300" href="../">Glossary</a></li>
            </ul>
          </nav>
        </div>
      </section>

      <div class="ad-banner ad-banner-bottom w-full bg-neutral-900/80 border-y border-neutral-800 py-3">
        <div class="container px-4 mx-auto max-w-4xl">
          <a href="https://gdfn.com" target="_blank" rel="noopener noreferrer" class="block rounded-lg overflow-hidden border border-neutral-700 shadow-lg hover:border-neutral-600 transition-colors" aria-label="Advertisement">
            <img src="../../banner-ads/gdfn.com-728x90-xyz.gif" width="728" height="90" alt="Advertisement" class="w-full h-auto block"/>
          </a>
        </div>
      </div>
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
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../articles/">Blog</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../../faq/">FAQ</a></li>
                    <li class="mb-4"><a class="hover:text-white font-medium text-neutral-300 transition-colors duration-200" href="../">Glossary</a></li>
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


def update_sitemap(slugs: list[str]) -> None:
    """Insert glossary term URLs after the glossary/ line in sitemap.xml."""
    if not SITEMAP.exists():
        return
    text = SITEMAP.read_text(encoding="utf-8")
    marker = "<url><loc>https://vpnsurf.com/glossary/</loc></url>"
    if marker not in text:
        return
    lines = text.split("\n")
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        if marker in line and not inserted:
            for s in slugs:
                new_lines.append(f"  <url><loc>{BASE}/glossary/{s}/</loc></url>")
            inserted = True
    SITEMAP.write_text("\n".join(new_lines), encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        print(f"Glossary source not found: {SOURCE}")
        return
    terms_raw = parse_terms(SOURCE)
    terms_with_slugs = ensure_unique_slugs(terms_raw)
    term_names_by_len = sorted([t for t, _, _ in terms_with_slugs], key=lambda x: -len(x))
    term_to_slug = {t: s for t, _, s in terms_with_slugs}
    by_letter: dict[str, list[tuple[str, str, str]]] = {}
    for term, raw_def, slug in terms_with_slugs:
        letter = first_letter(term)
        by_letter.setdefault(letter, []).append((term, raw_def, slug))
    for letter in by_letter:
        by_letter[letter].sort(key=lambda x: x[0].lower())

    OUT_INDEX.parent.mkdir(parents=True, exist_ok=True)
    OUT_GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)

    index_html = build_index_html(terms_with_slugs, by_letter)
    OUT_INDEX.write_text(index_html, encoding="utf-8")
    print(f"Wrote index to {OUT_INDEX}")

    for term, raw_def, slug in terms_with_slugs:
        definition_linked = linkify_definition(
            raw_def, term, term_names_by_len, term_to_slug
        )
        letter = first_letter(term)
        related = related_terms(term, slug, letter, terms_with_slugs, by_letter, raw_def)
        html_out = term_page_html(term, slug, raw_def, definition_linked, related, term_to_slug)
        out_path = OUT_GLOSSARY_DIR / f"{slug}.html"
        out_path.write_text(html_out, encoding="utf-8")

    print(f"Wrote {len(terms_with_slugs)} term pages to {OUT_GLOSSARY_DIR}/")
    update_sitemap([s for _, _, s in terms_with_slugs])
    print(f"Updated {SITEMAP}")


if __name__ == "__main__":
    main()
