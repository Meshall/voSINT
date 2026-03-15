from __future__ import annotations

from vosint.models import Hit


def rank_timeline(hits: list[Hit]) -> list[Hit]:
    known = [h for h in hits if h.date_parsed is not None]
    unknown = [h for h in hits if h.date_parsed is None]
    known.sort(key=lambda h: (h.date_parsed, -h.confidence))
    unknown.sort(key=lambda h: h.confidence, reverse=True)
    return known + unknown
