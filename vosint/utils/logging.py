def log_progress(stage: str, detail: str = "") -> None:
    suffix = f" - {detail}" if detail else ""
    print(f"[voSINT] {stage}{suffix}")
