#!/usr/bin/env python3
"""Inject Chatwoot widget script into target HTML pages. Run from repo root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root
PUBLIC = ROOT / "public"
SNIPPET_PATH = Path(__file__).resolve().parent / "snippet.html"


def _load_snippet() -> str:
    if SNIPPET_PATH.exists():
        return "\n    " + SNIPPET_PATH.read_text(encoding="utf-8").strip().replace("\n", "\n    ")
    return ""


def add_to_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "chatwootSDK" in text:
        return False
    snippet = _load_snippet()
    if not snippet:
        return False
    text = text.replace("</script>\n</body>", "</script>" + snippet + "\n</body>")
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path}")
    return True


def main():
    count = 0
    for subdir in ("articles",):
        for f in (PUBLIC / subdir).glob("*.html"):
            if add_to_file(f):
                count += 1
    print(f"Chatwoot: {count} file(s) updated.")


if __name__ == "__main__":
    main()
