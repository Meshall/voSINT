from __future__ import annotations

from pathlib import Path

from vosint.models import Hit
from vosint.providers._playwright_utils import retry
from vosint.providers.base import ProviderAdapter, ProviderContext
from vosint.utils.url import root_domain


class PinterestAdapter(ProviderAdapter):
    name = "pinterest"

    def search(self, frame_path: Path, frame_id: str, context: ProviderContext) -> list[Hit]:
        if context.no_browser:
            return []

        def _run() -> list[Hit]:
            from playwright.sync_api import sync_playwright

            hits: list[Hit] = []
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=not context.headful)
                page = browser.new_page()
                page.goto("https://www.pinterest.com/", wait_until="domcontentloaded", timeout=45000)
                page.goto("https://www.pinterest.com/search/pins/?q=image%20search", timeout=45000)
                for selector in ["input[type=file]", "input[data-test-id='ImageSearchInput']"]:
                    element = page.locator(selector).first
                    if element.count() > 0:
                        element.set_input_files(str(frame_path))
                        break
                page.wait_for_timeout(5000)
                cards = page.locator("a[href*='/pin/']").all()[:20]
                for card in cards:
                    url = card.get_attribute("href") or ""
                    title = (card.get_attribute("title") or "").strip()
                    if url and url.startswith("/"):
                        url = f"https://www.pinterest.com{url}"
                    hits.append(
                        Hit(
                            engine=self.name,
                            frame_id=frame_id,
                            url=url,
                            title=title,
                            snippet="Pinterest pin match",
                            domain=root_domain(url),
                            source_type="pin",
                        )
                    )
                browser.close()
            return hits

        return retry(_run, retries=context.retries)
