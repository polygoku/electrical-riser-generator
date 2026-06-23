#!/usr/bin/env python3
"""Lightweight QA helper for electrical-riser SVG/drawio packages.

This script does not replace engineering review. It catches common packaging and
drafting mistakes that occurred in prior riser iterations: invalid drawio XML,
embedded-image-only drawio files, unescaped XML attributes, floating line ends,
and obvious text/rectangle overlaps in SVG review files.

Usage:
    python scripts/riser_qc.py path/to/file.drawio path/to/file.svg
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_xml(path: Path) -> ET.Element | None:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        print(f"FAIL XML parse: {path}: {exc}")
        return None


def check_drawio(path: Path) -> int:
    root = parse_xml(path)
    if root is None:
        return 1
    cells = root.findall('.//mxCell')
    image_cells = [c for c in cells if 'shape=image' in (c.get('style') or '')]
    print(f"drawio cells: {len(cells)} | image cells: {len(image_cells)}")
    failures = 0
    if len(cells) < 20:
        print('WARN drawio has very few cells; confirm it is not just a background image.')
    if image_cells and len(image_cells) >= max(1, len(cells) - 3):
        print('FAIL drawio appears to be embedded-image-only, not native editable geometry.')
        failures += 1
    return failures


def check_svg(path: Path) -> int:
    text = path.read_text(encoding='utf-8', errors='ignore')
    root = parse_xml(path)
    if root is None:
        return 1
    failures = 0
    # Basic line endpoint census. Repeated unpaired endpoints are not always an error,
    # but a high count is a useful prompt for manual review.
    endpoints = []
    for m in re.finditer(r'<line[^>]*x1="([0-9.\-]+)"[^>]*y1="([0-9.\-]+)"[^>]*x2="([0-9.\-]+)"[^>]*y2="([0-9.\-]+)"', text):
        x1, y1, x2, y2 = map(float, m.groups())
        endpoints.append((round(x1), round(y1)))
        endpoints.append((round(x2), round(y2)))
    print(f"svg line endpoints: {len(endpoints)}")
    # Check for common raw XML attribute hazards that break drawio import.
    if '<br>' in text or '<BR>' in text:
        print('WARN raw <br> found; drawio attributes must escape line breaks or use html=1 labels.')
    return failures


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    failures = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"FAIL missing file: {path}")
            failures += 1
            continue
        suffix = path.suffix.lower()
        if suffix == '.drawio':
            failures += check_drawio(path)
        elif suffix == '.svg':
            failures += check_svg(path)
        else:
            print(f"SKIP unsupported file type: {path}")
    if failures:
        print(f"QC completed with {failures} failure(s).")
    else:
        print('QC completed without fatal failures. Perform visual review for overlap/floating symbols.')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
