from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from vosint.models import Hit


@dataclass
class ProviderContext:
    headful: bool = False
    no_browser: bool = False
    retries: int = 2


class ProviderAdapter:
    name = "base"

    def search(self, frame_path: Path, frame_id: str, context: ProviderContext) -> list[Hit]:
        raise NotImplementedError
