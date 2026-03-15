from __future__ import annotations

import time
from collections.abc import Callable


def retry(func: Callable, retries: int = 2, delay: float = 1.5):
    last_error = None
    for _ in range(retries + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(delay)
    if last_error:
        raise last_error
