from __future__ import annotations

from pathlib import Path

from vosint.models import Hit
from vosint.providers.base import ProviderAdapter, ProviderContext
from vosint.utils.url import root_domain


class YandexAdapter(ProviderAdapter):
    name = "yandex"

    def search(self, frame_path: Path, frame_id: str, context: ProviderContext) -> list[Hit]:
        if context.no_browser:
            return []
        from playwright.sync_api import sync_playwright

        hits: list[Hit] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not context.headful)
            page = browser.new_page()
            page.goto("https://yandex.com/images/", wait_until="domcontentloaded", timeout=45000)
            page.locator("input[type=file]").first.set_input_files(str(frame_path))
            page.wait_for_timeout(7000)
            cards = page.locator("a[href^='http']").all()[:20]
            for card in cards:
                url = card.get_attribute("href") or ""
                title = card.inner_text().strip() if card.inner_text() else ""
                if url:
                    hits.append(Hit(engine=self.name, frame_id=frame_id, url=url, title=title, domain=root_domain(url)))
            browser.close()
        return hits
