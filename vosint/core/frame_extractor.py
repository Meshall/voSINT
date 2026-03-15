from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from vosint.utils.scoring import frame_quality_score


def _read_frames_cv2(video_path: Path) -> tuple[list[np.ndarray], float]:
    import cv2

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)
    cap.release()
    return frames, fps


def _read_frames_imageio(video_path: Path) -> tuple[list[np.ndarray], float]:
    import imageio.v3 as iio

    frames = [f for f in iio.imiter(video_path)]
    meta = iio.immeta(video_path)
    fps = meta.get("fps", 25) if isinstance(meta, dict) else 25
    return frames, fps


def _read_frames(video_path: Path) -> tuple[list[np.ndarray], float]:
    try:
        return _read_frames_cv2(video_path)
    except Exception:
        return _read_frames_imageio(video_path)


def _scene_cut_indices(frames: list[np.ndarray], limit: int = 10) -> list[int]:
    if len(frames) < 2:
        return []
    idx = []
    prev = frames[0].astype(float)
    for i, frame in enumerate(frames[1:], start=1):
        diff = float(np.mean(np.abs(prev - frame.astype(float))))
        if diff > 25:
            idx.append(i)
        prev = frame.astype(float)
    return idx[:limit]


def _save_frame(frame_path: Path, frame: np.ndarray) -> None:
    try:
        import cv2

        cv2.imwrite(str(frame_path), frame)
        return
    except Exception:
        pass
    import imageio.v3 as iio

    iio.imwrite(frame_path, frame)


def extract_ranked_frames(video_path: Path, output_dir: Path, max_frames: int = 8) -> list[dict]:
    frames, fps = _read_frames(video_path)
    if not frames:
        return []

    N = len(frames)
    candidates = {0, N // 2, max(0, N - 1)}
    interval = max(1, N // max(max_frames, 1))
    for i in range(0, N, interval):
        candidates.add(i)
    for i in _scene_cut_indices(frames, limit=max_frames * 2):
        candidates.add(i)

    ranked = []
    for i in sorted(candidates):
        frame = frames[i]
        score = frame_quality_score(frame)
        frame_id = f"f{i:05d}"
        frame_path = output_dir / f"{frame_id}.jpg"
        _save_frame(frame_path, frame)
        ranked.append(
            {
                "frame_id": frame_id,
                "path": frame_path,
                "index": i,
                "timestamp": round(i / fps, 3),
                "quality": score,
                "hash": hashlib.sha1(frame.tobytes()).hexdigest(),
            }
        )

    ranked.sort(key=lambda x: x["quality"], reverse=True)
    return ranked[:max_frames]
