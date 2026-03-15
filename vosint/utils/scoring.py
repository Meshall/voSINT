from __future__ import annotations

import numpy as np


def _gray(frame: np.ndarray) -> np.ndarray:
    if frame.ndim == 2:
        return frame.astype(float)
    return (0.299 * frame[..., 0] + 0.587 * frame[..., 1] + 0.114 * frame[..., 2]).astype(float)


def blur_score(frame: np.ndarray) -> float:
    gray = _gray(frame)
    gy, gx = np.gradient(gray)
    return float(np.var(gx) + np.var(gy))


def darkness_score(frame: np.ndarray) -> float:
    gray = _gray(frame)
    return float(np.mean(gray) / 255.0)


def text_density_score(frame: np.ndarray) -> float:
    gray = _gray(frame)
    gy, gx = np.gradient(gray)
    mag = np.hypot(gx, gy)
    return float(np.count_nonzero(mag > np.percentile(mag, 80)) / mag.size)


def frame_quality_score(frame: np.ndarray) -> float:
    blur = min(1.0, blur_score(frame) / 800.0)
    dark = darkness_score(frame)
    text = min(1.0, text_density_score(frame) * 3)
    return round((0.45 * blur) + (0.25 * dark) + (0.30 * text), 4)
