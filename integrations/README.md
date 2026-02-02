# Integrations

This folder holds **third-party integrations** and the scripts that inject them into HTML.

| Item | Purpose |
|------|---------|
| [chatwoot/](chatwoot/) | Chat widget (Chatwoot SDK). Snippet in `snippet.html`; [add_chatwoot.py](chatwoot/add_chatwoot.py) injects it into target pages. |
| [add_ad_banners.py](add_ad_banners.py) | Injects 728×90 top/bottom ad banners into target pages. |

**Webmaster:** To change the Chatwoot token or base URL, edit `integrations/chatwoot/snippet.html`. The build runs `integrations/chatwoot/add_chatwoot.py` and `integrations/add_ad_banners.py`. See [chatwoot/README.md](chatwoot/README.md) for placement notes.
