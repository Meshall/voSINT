from __future__ import annotations

import json
from pathlib import Path

from vosint.core.dna import build_video_dna
from vosint.core.frame_extractor import extract_ranked_frames
from vosint.core.normalize import normalize_hits
from vosint.core.pivots import build_pivot, run_ocr, transcribe_video
from vosint.core.timeline import rank_timeline
from vosint.models import Case
from vosint.output.renderers import write_csv_timeline, write_html, write_json
from vosint.output.terminal import print_summary
from vosint.providers import DEFAULT_PROVIDER_ORDER, PROVIDER_REGISTRY
from vosint.providers.base import ProviderContext
from vosint.utils.fs import make_case_dir, stage_input
from vosint.utils.logging import log_progress


MODE_DEFAULTS = {
    "fast": {"max_frames": 3, "providers": ["pinterest", "google_lens", "bing_visual"], "ocr": False, "transcribe": False},
    "deep": {"max_frames": 8, "providers": DEFAULT_PROVIDER_ORDER, "ocr": True, "transcribe": True},
    "stealth": {"max_frames": 6, "providers": [], "ocr": True, "transcribe": True},
}


def run_scan(
    video_path: Path,
    cases_root: Path,
    mode: str = "deep",
    providers: list[str] | None = None,
    max_frames: int | None = None,
    do_ocr: bool | None = None,
    do_transcribe: bool | None = None,
    no_browser: bool = False,
    headful: bool = False,
    keep_frames: bool = False,
    want_json: bool = True,
    want_csv: bool = True,
    want_html: bool = True,
) -> Case:
    defaults = MODE_DEFAULTS[mode]
    selected_providers = providers or defaults["providers"]
    frame_limit = max_frames or defaults["max_frames"]
    do_ocr = defaults["ocr"] if do_ocr is None else do_ocr
    do_transcribe = defaults["transcribe"] if do_transcribe is None else do_transcribe

    case_id, case_dir = make_case_dir(cases_root)
    staged_video = stage_input(video_path, case_dir)
    case = Case(case_id=case_id, mode=mode, input_path=str(video_path), case_dir=case_dir)

    log_progress("loading video", str(video_path))
    log_progress("extracting frames", f"max={frame_limit}")
    frames = extract_ranked_frames(staged_video, case_dir / "frames", max_frames=frame_limit)
    if not frames:
        raise RuntimeError("No frames extracted")

    all_ocr_terms: list[str] = []
    transcript_terms: list[str] = []
    if do_ocr:
        log_progress("running OCR")
        for frame in frames:
            terms = run_ocr(frame["path"])
            all_ocr_terms.extend(terms)
            case.pivots.append(build_pivot(frame["frame_id"], terms, []))

    if do_transcribe:
        log_progress("running transcript extraction")
        transcript_terms = transcribe_video(staged_video)

    context = ProviderContext(headful=headful, no_browser=no_browser)
    raw_hits = []
    for provider_name in selected_providers:
        adapter_cls = PROVIDER_REGISTRY.get(provider_name)
        if not adapter_cls:
            continue
        adapter = adapter_cls()
        for frame in frames:
            log_progress(f"searching {provider_name}", frame["frame_id"])
            try:
                hits = adapter.search(frame["path"], frame["frame_id"], context)
                raw_hits.extend(hits)
            except Exception as exc:  # noqa: BLE001
                case.failures.append({"provider": provider_name, "frame_id": frame["frame_id"], "error": str(exc)})

    log_progress("normalizing results")
    merged = normalize_hits(raw_hits)
    case.hits = rank_timeline(merged)

    case.video_dna = build_video_dna(staged_video, frames, all_ocr_terms[:120], transcript_terms[:120])
    (case_dir / "normalized" / "video_dna.json").write_text(json.dumps(case.video_dna.to_dict(), indent=2), encoding="utf-8")

    if mode == "stealth" or no_browser:
        manual_pack = {
            "frames": [str(f["path"]) for f in frames],
            "ocr_terms": all_ocr_terms[:100],
            "transcript_terms": transcript_terms[:100],
            "queries": [p for pivot in case.pivots for p in pivot.queries][:50],
        }
        (case_dir / "raw" / "manual_query_pack.json").write_text(json.dumps(manual_pack, indent=2), encoding="utf-8")

    if not keep_frames:
        for frame in (case_dir / "frames").glob("*.jpg"):
            frame.unlink(missing_ok=True)

    if want_json:
        write_json(case, case_dir / "report.json")
    if want_csv:
        write_csv_timeline(case, case_dir / "timeline.csv")
    if want_html:
        write_html(case, case_dir / "report.html")

    print_summary(case)
    print(f"Output path: {case_dir}")
    return case
