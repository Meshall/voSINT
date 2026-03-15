from __future__ import annotations

import re
from pathlib import Path

from vosint.models import FramePivot


def run_ocr(frame_path: Path) -> list[str]:
    try:
        import pytesseract
        from PIL import Image
    except Exception:  # noqa: BLE001
        return []

    text = pytesseract.image_to_string(Image.open(frame_path))
    terms = [t for t in re.split(r"\W+", text) if len(t) > 3]
    return terms[:25]


def transcribe_video(video_path: Path) -> list[str]:
    try:
        import whisper
    except Exception:  # noqa: BLE001
        return []

    model = whisper.load_model("tiny")
    result = model.transcribe(str(video_path))
    raw = result.get("text", "")
    terms = [t for t in re.split(r"\W+", raw) if len(t) > 4]
    return terms[:40]


def build_pivot(frame_id: str, ocr_terms: list[str], transcript_terms: list[str]) -> FramePivot:
    phrases = [" ".join(ocr_terms[:4]).strip(), " ".join(transcript_terms[:5]).strip()]
    queries = [f'"{p}"' for p in phrases if p]
    queries += [f"site:youtube.com {t}" for t in ocr_terms[:3]]
    return FramePivot(frame_id=frame_id, ocr_terms=ocr_terms, transcript_terms=transcript_terms, queries=queries)
