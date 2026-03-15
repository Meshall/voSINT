from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path


CASE_SUBDIRS = ["input", "frames", "raw", "normalized"]


def make_case_dir(base: Path, prefix: str = "case") -> tuple[str, Path]:
    case_id = f"{prefix}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    case_dir = base / case_id
    for sub in CASE_SUBDIRS:
        (case_dir / sub).mkdir(parents=True, exist_ok=True)
    return case_id, case_dir


def stage_input(input_path: Path, case_dir: Path) -> Path:
    destination = case_dir / "input" / input_path.name
    shutil.copy2(input_path, destination)
    return destination
