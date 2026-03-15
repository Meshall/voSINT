from __future__ import annotations

import hashlib
from pathlib import Path

from vosint.models import VideoDNA


def build_video_dna(video_path: Path, frame_rows: list[dict], ocr_terms: list[str], transcript_terms: list[str]) -> VideoDNA:
    with open(video_path, "rb") as fh:
        video_hash = hashlib.sha1(fh.read()).hexdigest()
    frame_hashes = {row["frame_id"]: row["hash"] for row in frame_rows}
    scene_hashes = list(frame_hashes.values())[:8]
    best_pivots = list(dict.fromkeys((ocr_terms + transcript_terms)))[:20]
    return VideoDNA(
        video_hash=video_hash,
        frame_hashes=frame_hashes,
        scene_hashes=scene_hashes,
        ocr_terms=ocr_terms,
        transcript_terms=transcript_terms,
        best_pivots=best_pivots,
    )
