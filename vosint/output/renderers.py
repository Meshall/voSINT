from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from vosint.models import Case


def write_json(case: Case, path: Path) -> None:
    path.write_text(json.dumps(case.to_dict(), indent=2), encoding="utf-8")


def write_csv_timeline(case: Case, path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["date", "url", "domain", "confidence", "engines", "frames", "title"],
        )
        writer.writeheader()
        for hit in case.hits:
            writer.writerow(
                {
                    "date": hit.date_parsed.isoformat() if hit.date_parsed else "",
                    "url": hit.url,
                    "domain": hit.domain,
                    "confidence": hit.confidence,
                    "engines": ";".join(sorted(hit.support_engines)),
                    "frames": ";".join(sorted(hit.support_frames)),
                    "title": hit.title,
                }
            )


def write_html(case: Case, path: Path) -> None:
    rows = []
    for hit in case.hits[:200]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(hit.date_parsed.isoformat() if hit.date_parsed else 'undated')}</td>"
            f"<td><a href='{html.escape(hit.url)}'>{html.escape(hit.url)}</a></td>"
            f"<td>{html.escape(hit.domain)}</td>"
            f"<td>{html.escape(hit.title)}</td>"
            f"<td>{hit.confidence:.2f}</td>"
            f"<td>{html.escape(', '.join(sorted(hit.support_engines)))}</td>"
            "</tr>"
        )

    content = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>voSINT {case.case_id}</title>
<style>body{{font-family:Arial;margin:20px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px}}</style>
</head><body>
<h1>voSINT v2 report</h1>
<p><strong>Case:</strong> {html.escape(case.case_id)} | <strong>Mode:</strong> {html.escape(case.mode)}</p>
<h2>Likely earliest source</h2>
<p>{html.escape(case.hits[0].url if case.hits else 'No results')}</p>
<h2>Provider breakdown</h2>
<p>{html.escape(', '.join(sorted({e for h in case.hits for e in h.support_engines})) or 'No providers')}</p>
<h2>Timeline</h2>
<table><thead><tr><th>Date</th><th>URL</th><th>Domain</th><th>Title</th><th>Confidence</th><th>Support</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
</body></html>"""
    path.write_text(content, encoding="utf-8")
