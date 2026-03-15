# voSINT v2

Token-free reverse-video OSINT workflow focused on **origin hunting** and **repost spread** analysis.

## Highlights
- No SerpApi key, no `config.ini` setup, no upload-to-host requirement.
- Playwright provider adapters (default order): **Pinterest**, Google Lens, Bing Visual, Yandex, TinEye.
- Multi-frame extraction with quality scoring and timeline-first ranking.
- OCR pivots, transcript pivots (optional local dependencies), and Video DNA artifact.
- Case-folder outputs: HTML/JSON/CSV + raw/normalized artifacts.
- Commands: `scan`, `diff`, `report`.

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m playwright install chromium
```

## CLI
### Single scan
```bash
vosint scan video.mp4
```

### Batch scan
```bash
vosint scan ./videos --batch --mode deep
```

### Compare videos
```bash
vosint diff a.mp4 b.mp4
```

### Re-open a case report
```bash
vosint report cases/case_YYYYMMDD_HHMMSS
```

## Modes
- `fast`: few top frames, Pinterest + Google Lens + Bing.
- `deep` (default): more frames, OCR+transcript, all default providers.
- `stealth`: local-only extraction/pivots, no provider submission; emits manual query pack.

## Common flags
```bash
--mode fast|deep|stealth
--providers pinterest,google_lens,bing_visual,yandex,tineye
--max-frames 8
--ocr
--transcribe
--json --csv --html
--keep-frames
--no-browser
--headful
```

## Output layout
Each run writes:
```
cases/<case_id>/
  input/
  frames/
  raw/
  normalized/
  report.html
  report.json
  timeline.csv
```

## Privacy note
Reverse-image providers receive submitted frames unless `--mode stealth` or `--no-browser` is used.
