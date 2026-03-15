from __future__ import annotations

import argparse
import json
from pathlib import Path

from vosint.core.diffing import diff_video_dna
from vosint.core.orchestrator import MODE_DEFAULTS, run_scan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="vosint", description="voSINT v2 token-free reverse-video OSINT")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="scan a video or batch folder")
    scan.add_argument("target")
    scan.add_argument("--batch", action="store_true")
    scan.add_argument("--mode", choices=list(MODE_DEFAULTS), default="deep")
    scan.add_argument("--providers", default="")
    scan.add_argument("--max-frames", type=int, default=None)
    scan.add_argument("--ocr", action="store_true")
    scan.add_argument("--transcribe", action="store_true")
    scan.add_argument("--json", action="store_true")
    scan.add_argument("--csv", action="store_true")
    scan.add_argument("--html", action="store_true")
    scan.add_argument("--keep-frames", action="store_true")
    scan.add_argument("--no-browser", action="store_true")
    scan.add_argument("--headful", action="store_true")

    diff = sub.add_parser("diff", help="compare two videos")
    diff.add_argument("video_a")
    diff.add_argument("video_b")

    report = sub.add_parser("report", help="print report summary from case dir")
    report.add_argument("case_dir")
    return parser.parse_args()


def _scan_one(args: argparse.Namespace, path: Path) -> None:
    providers = [p.strip() for p in args.providers.split(",") if p.strip()] or None
    run_scan(
        video_path=path,
        cases_root=Path("cases"),
        mode=args.mode,
        providers=providers,
        max_frames=args.max_frames,
        do_ocr=args.ocr or None,
        do_transcribe=args.transcribe or None,
        no_browser=args.no_browser,
        headful=args.headful,
        keep_frames=args.keep_frames,
        want_json=args.json or True,
        want_csv=args.csv or True,
        want_html=args.html or True,
    )


def main() -> None:
    args = parse_args()
    if args.command == "scan":
        target = Path(args.target)
        if args.batch:
            videos = [p for p in target.iterdir() if p.suffix.lower() in {".mp4", ".mov", ".avi", ".mkv"}]
            for video in videos:
                _scan_one(args, video)
        else:
            _scan_one(args, target)
    elif args.command == "diff":
        case_a = run_scan(Path(args.video_a), Path("cases"), mode="stealth", no_browser=True)
        case_b = run_scan(Path(args.video_b), Path("cases"), mode="stealth", no_browser=True)
        comparison = diff_video_dna(case_a.video_dna.to_dict(), case_b.video_dna.to_dict())
        print(json.dumps(comparison, indent=2))
    elif args.command == "report":
        case_dir = Path(args.case_dir)
        report_json = case_dir / "report.json"
        print(report_json.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
