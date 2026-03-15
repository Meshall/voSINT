from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Hit:
    engine: str
    frame_id: str
    url: str
    title: str = ""
    snippet: str = ""
    thumbnail: str = ""
    domain: str = ""
    date_raw: str = ""
    date_parsed: datetime | None = None
    confidence: float = 0.0
    source_type: str = "result"
    support_frames: set[str] = field(default_factory=set)
    support_engines: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.frame_id:
            self.support_frames.add(self.frame_id)
        if self.engine:
            self.support_engines.add(self.engine)

    def to_dict(self) -> dict:
        return {
            "engine": self.engine,
            "frame_id": self.frame_id,
            "url": self.url,
            "title": self.title,
            "snippet": self.snippet,
            "thumbnail": self.thumbnail,
            "domain": self.domain,
            "date_raw": self.date_raw,
            "date_parsed": self.date_parsed.isoformat() if self.date_parsed else None,
            "confidence": round(self.confidence, 4),
            "source_type": self.source_type,
            "support_frames": sorted(self.support_frames),
            "support_engines": sorted(self.support_engines),
        }
