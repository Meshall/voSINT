from __future__ import annotations


def diff_video_dna(a: dict, b: dict) -> dict:
    a_frames = set(a.get("frame_hashes", {}).values())
    b_frames = set(b.get("frame_hashes", {}).values())
    overlap = len(a_frames & b_frames)
    total = max(len(a_frames | b_frames), 1)
    ratio = overlap / total
    return {
        "same_source_probability": round(ratio, 4),
        "shared_frames": overlap,
        "first_divergence_point": "early" if ratio < 0.5 else "late",
        "likely_edits": ["crop/mirror/subtitle"] if 0 < ratio < 1 else [],
    }
