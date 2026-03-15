from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from vosint.models import Hit
from vosint.utils.url import canonicalize_url, root_domain


DATE_PATTERNS = ["%Y-%m-%d", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y"]


def parse_date(raw: str) -> datetime | None:
    value = (raw or "").strip()
    for pattern in DATE_PATTERNS:
        try:
            return datetime.strptime(value, pattern)
        except ValueError:
            continue
    return None


def normalize_hits(hits: list[Hit]) -> list[Hit]:
    grouped: dict[str, list[Hit]] = defaultdict(list)
    for hit in hits:
        if not hit.url:
            continue
        hit.url = canonicalize_url(hit.url)
        hit.domain = hit.domain or root_domain(hit.url)
        hit.date_parsed = parse_date(hit.date_raw)
        grouped[hit.url].append(hit)

    merged: list[Hit] = []
    for url, items in grouped.items():
        base = items[0]
        for item in items[1:]:
            base.support_frames |= item.support_frames
            base.support_engines |= item.support_engines
            if not base.title and item.title:
                base.title = item.title
            if not base.snippet and item.snippet:
                base.snippet = item.snippet
            if not base.date_parsed and item.date_parsed:
                base.date_parsed = item.date_parsed
        base.confidence = min(1.0, 0.2 + (0.15 * len(base.support_engines)) + (0.1 * len(base.support_frames)))
        merged.append(base)
    return merged
