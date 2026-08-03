#!/usr/bin/env python3
"""Generate matching SVG and native editable diagrams.net riser files.

Input JSON requires:
- project, address, revision, service
- riser.nodes: [{id, kind, label, rating, x, y, w, h}]
- riser.edges: [{id, source, target, label, points?, disconnect?}]

Disconnect values may be `true`, `"fused"`, `"non_fused"`, or an object such
as {"kind": "fused", "label": "60A/3P FDS", "at": [900, 420]}.

Every SVG object has a corresponding native mxCell object. No image or SVG is
embedded in the drawio file.

Usage:
    python build_native_riser.py project.json output_prefix
"""
from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

PAGE_W = 1600
PAGE_H = 1000
EATON_SYMBOL_REFERENCE = "https://www.newark.com/pdfs/techarticles/eatonCH/ElectricalSymbols.pdf"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def node_style(kind: str) -> tuple[str, str]:
    if kind == "bus":
        return "#1f4e79", "#1f4e79"
    if kind == "transformer":
        return "#fff2cc", "#bf9000"
    if kind == "service":
        return "#ddebf7", "#1f4e79"
    if kind == "note":
        return "#fce4d6", "#c65911"
    return "#ffffff", "#000000"


def svg_text(x: float, y: float, text: str, size: int = 14, bold: bool = False, anchor: str = "middle") -> str:
    weight = "700" if bold else "400"
    return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{esc(text)}</text>'


def disconnect_spec(value: Any) -> dict[str, Any] | None:
    """Normalize legacy flags and explicit disconnect definitions."""
    if not value:
        return None
    if value is True:
        return {"kind": "fused", "label": "FDS"}
    if isinstance(value, str):
        value = {"kind": value}
    if not isinstance(value, dict):
        raise ValueError("disconnect must be a boolean, string, or object")

    kind = str(value.get("kind", "fused")).strip().lower().replace("-", "_")
    aliases = {
        "fds": "fused",
        "sfds": "fused",
        "fused_disconnect": "fused",
        "nfd": "non_fused",
        "nonfused": "non_fused",
        "non_fused_disconnect": "non_fused",
        "lds": "non_fused",
        "switch": "non_fused",
    }
    kind = aliases.get(kind, kind)
    if kind not in {"fused", "non_fused"}:
        raise ValueError(f"Unsupported disconnect kind: {kind}")

    spec = dict(value)
    spec["kind"] = kind
    spec.setdefault("label", "FDS" if kind == "fused" else "NFD")
    return spec


def edge_points(edge: dict[str, Any], source: dict[str, Any], target: dict[str, Any]) -> list[list[float]]:
    sx = source["x"] + source.get("w", 120)
    sy = source["y"] + source.get("h", 60) / 2
    tx = target["x"]
    ty = target["y"] + target.get("h", 60) / 2
    return edge.get("points") or [[sx, sy], [tx, sy], [tx, ty]]


def disconnect_placement(points: list[list[float]], spec: dict[str, Any]) -> tuple[float, float, str]:
    """Place and orient a symbol on an orthogonal feeder segment."""
    segments: list[tuple[float, int, list[float], list[float]]] = []
    for index, (start, end) in enumerate(zip(points, points[1:])):
        length = math.hypot(end[0] - start[0], end[1] - start[1])
        if length:
            segments.append((length, index, start, end))
    if not segments:
        raise ValueError("disconnect feeder requires at least one non-zero segment")

    preferred = next((item for item in reversed(segments) if item[0] >= 80), max(segments))
    _, _, start, end = preferred
    at = spec.get("at")
    x, y = (float(at[0]), float(at[1])) if at else ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
    direction = spec.get("orientation")
    if not direction:
        dx, dy = end[0] - start[0], end[1] - start[1]
        direction = ("right" if dx >= 0 else "left") if abs(dx) >= abs(dy) else ("down" if dy >= 0 else "up")
    if direction not in {"right", "down", "left", "up"}:
        raise ValueError(f"Unsupported disconnect orientation: {direction}")
    return x, y, direction


def rotate_point(x: float, y: float, direction: str) -> tuple[float, float]:
    if direction == "right":
        return x, y
    if direction == "down":
        return -y, x
    if direction == "left":
        return -x, -y
    return y, -x


def symbol_parts(kind: str) -> tuple[tuple[float, float, float, float], list[tuple[float, float, float, float]], tuple[float, float, float, float] | None]:
    """Return mask, line segments, and optional fuse body in left-to-right power-flow order."""
    if kind == "fused":
        lines = [
            (-48, 0, -37, 0),
            (-37, -8, -37, 8),
            (-3, -8, -3, 8),
            (-3, 0, 10, 0),
            (10, 0, 29, -13),
            (34, 0, 48, 0),
        ]
        return (-50, -18, 100, 36), lines, (-34, -6, 28, 12)
    lines = [(-34, 0, -10, 0), (-10, 0, 10, -13), (15, 0, 34, 0)]
    return (-36, -18, 72, 36), lines, None


def svg_disconnect_symbol(x: float, y: float, direction: str, spec: dict[str, Any]) -> str:
    angle = {"right": 0, "down": 90, "left": 180, "up": -90}[direction]
    mask, lines, fuse = symbol_parts(spec["kind"])
    items = [
        f'<g data-symbol="{spec["kind"]}-disconnect" data-orientation="{direction}" transform="translate({x} {y}) rotate({angle})">',
        f'<rect x="{mask[0]}" y="{mask[1]}" width="{mask[2]}" height="{mask[3]}" fill="white" stroke="none"/>',
    ]
    if fuse:
        items.append(f'<rect x="{fuse[0]}" y="{fuse[1]}" width="{fuse[2]}" height="{fuse[3]}" fill="white" stroke="#000" stroke-width="2"/>')
    items.extend(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}" stroke="#000" stroke-width="2"/>' for a, b, c, d in lines)
    items.append("</g>")
    label_x, label_y, anchor = (x + 20, y + 4, "start") if direction in {"down", "up"} else (x, y + 30, "middle")
    items.append(svg_text(label_x, label_y, spec.get("label", ""), 10, True, anchor))
    return "\n".join(items)


def build_svg(cfg: dict[str, Any]) -> str:
    items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" viewBox="0 0 {PAGE_W} {PAGE_H}">', '<rect width="100%" height="100%" fill="white"/>']
    items.append(svg_text(PAGE_W / 2, 36, cfg.get("project", "ELECTRICAL RISER"), 22, True))
    items.append(svg_text(PAGE_W / 2, 60, f"{cfg.get('address','')} | {cfg.get('revision','')}", 12))

    nodes = {n["id"]: n for n in cfg.get("riser", {}).get("nodes", [])}
    for edge in cfg.get("riser", {}).get("edges", []):
        source = nodes[edge["source"]]
        target = nodes[edge["target"]]
        points = edge_points(edge, source, target)
        d = " ".join(("M" if i == 0 else "L") + f" {p[0]} {p[1]}" for i, p in enumerate(points))
        items.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="2"/>')
        label = edge.get("label", "")
        if label:
            mx = sum(p[0] for p in points) / len(points)
            my = sum(p[1] for p in points) / len(points) - 8
            items.append(svg_text(mx, my, label, 12, True))
        spec = disconnect_spec(edge.get("disconnect"))
        if spec:
            x, y, direction = disconnect_placement(points, spec)
            items.append(svg_disconnect_symbol(x, y, direction, spec))

    for node in cfg.get("riser", {}).get("nodes", []):
        x, y = node["x"], node["y"]
        w, h = node.get("w", 120), node.get("h", 60)
        fill, stroke = node_style(node.get("kind", "panel"))
        if node.get("kind") == "bus":
            items.append(f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{stroke}" stroke-width="6"/>')
            items.append(svg_text(x + w / 2, y - 12, node.get("label", "BUS"), 13, True))
            continue
        items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        if node.get("rating"):
            items.append(svg_text(x + w / 2, y + h / 2 + 5, node["rating"], 16, True))
        if node.get("label"):
            items.append(svg_text(x + w / 2, y + h + 20, node["label"], 12, True))
        if node.get("status"):
            items.append(svg_text(x + w / 2, y + h + 36, node["status"], 10, False))

    items.append('</svg>')
    return "\n".join(items)


def add_vertex(root: ET.Element, cell_id: str, value: str, x: float, y: float, w: float, h: float, style: str) -> None:
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"})
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})


def add_edge(root: ET.Element, cell_id: str, value: str, source: str, target: str, points: list[list[float]], style: str) -> None:
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": value, "style": style, "edge": "1", "parent": "1", "source": source, "target": target})
    geo = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    if points:
        array = ET.SubElement(geo, "Array", {"as": "points"})
        for x, y in points[1:-1]:
            ET.SubElement(array, "mxPoint", {"x": str(x), "y": str(y)})


def add_free_edge(root: ET.Element, cell_id: str, start: tuple[float, float], end: tuple[float, float], width: int = 2) -> None:
    cell = ET.SubElement(root, "mxCell", {"id": cell_id, "value": "", "style": f"endArrow=none;html=1;strokeWidth={width};", "edge": "1", "parent": "1"})
    geo = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    ET.SubElement(geo, "mxPoint", {"x": str(start[0]), "y": str(start[1]), "as": "sourcePoint"})
    ET.SubElement(geo, "mxPoint", {"x": str(end[0]), "y": str(end[1]), "as": "targetPoint"})


def add_drawio_disconnect(root: ET.Element, prefix: str, x: float, y: float, direction: str, spec: dict[str, Any]) -> None:
    mask, lines, fuse = symbol_parts(spec["kind"])
    corners = [rotate_point(mask[0], mask[1], direction), rotate_point(mask[0] + mask[2], mask[1] + mask[3], direction)]
    mask_x, mask_y = x + min(p[0] for p in corners), y + min(p[1] for p in corners)
    mask_w, mask_h = abs(corners[1][0] - corners[0][0]), abs(corners[1][1] - corners[0][1])
    add_vertex(root, f"{prefix}-mask", "", mask_x, mask_y, mask_w, mask_h, "rounded=0;html=1;strokeColor=none;fillColor=#ffffff;")

    if fuse:
        fx, fy, fw, fh = fuse
        corners = [rotate_point(fx, fy, direction), rotate_point(fx + fw, fy + fh, direction)]
        rx, ry = x + min(p[0] for p in corners), y + min(p[1] for p in corners)
        rw, rh = abs(corners[1][0] - corners[0][0]), abs(corners[1][1] - corners[0][1])
        add_vertex(root, f"{prefix}-fuse", "", rx, ry, rw, rh, "rounded=0;html=1;strokeWidth=2;fillColor=#ffffff;")

    for index, (a, b, c, d) in enumerate(lines):
        p1, p2 = rotate_point(a, b, direction), rotate_point(c, d, direction)
        add_free_edge(root, f"{prefix}-line-{index}", (x + p1[0], y + p1[1]), (x + p2[0], y + p2[1]))

    label_x, label_y, label_w = (x + 20, y - 10, 90) if direction in {"down", "up"} else (x - 45, y + 18, 90)
    add_vertex(root, f"{prefix}-label", esc(spec.get("label", "")), label_x, label_y, label_w, 22, "text;html=1;align=center;verticalAlign=middle;fontSize=10;fontStyle=1;strokeColor=none;fillColor=none;")


def build_drawio(cfg: dict[str, Any]) -> str:
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "24.7.17"})
    diagram = ET.SubElement(mxfile, "diagram", {"name": "Electrical Riser"})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx": "1200", "dy": "800", "grid": "1", "gridSize": "10", "page": "1", "pageScale": "1", "pageWidth": str(PAGE_W), "pageHeight": str(PAGE_H)})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    add_vertex(root, "title", f"<b>{esc(cfg.get('project','ELECTRICAL RISER'))}</b><br>{esc(cfg.get('address',''))} | {esc(cfg.get('revision',''))}", 350, 10, 900, 55, "text;html=1;align=center;verticalAlign=middle;fontSize=18;strokeColor=none;fillColor=none;")

    nodes = {n["id"]: n for n in cfg.get("riser", {}).get("nodes", [])}
    node_map: dict[str, str] = {}
    for i, node in enumerate(cfg.get("riser", {}).get("nodes", []), 1):
        cid = f"n{i}"
        node_map[node["id"]] = cid
        x, y = node["x"], node["y"]
        w, h = node.get("w", 120), node.get("h", 60)
        fill, stroke = node_style(node.get("kind", "panel"))
        if node.get("kind") == "bus":
            value = esc(node.get("label", "BUS"))
            style = f"shape=line;html=1;strokeWidth=6;strokeColor={stroke};fontStyle=1;labelPosition=center;verticalLabelPosition=top;verticalAlign=bottom;"
            add_vertex(root, cid, value, x, y, w, 1, style)
        else:
            rating = esc(node.get("rating", ""))
            label = esc(node.get("label", ""))
            status = esc(node.get("status", ""))
            value = f"<b>{rating}</b>" if rating else ""
            if label:
                value += f"<br>{label}"
            if status:
                value += f"<br><font style='font-size:10px'>{status}</font>"
            style = f"rounded=0;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=13;"
            add_vertex(root, cid, value, x, y, w, h, style)

    for i, edge in enumerate(cfg.get("riser", {}).get("edges", []), 1):
        source = nodes[edge["source"]]
        target = nodes[edge["target"]]
        points = edge_points(edge, source, target)
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;strokeWidth=2;"
        add_edge(root, f"e{i}", esc(edge.get("label", "")), node_map[edge["source"]], node_map[edge["target"]], points, style)
        spec = disconnect_spec(edge.get("disconnect"))
        if spec:
            x, y, direction = disconnect_placement(points, spec)
            add_drawio_disconnect(root, f"d{i}", x, y, direction, spec)

    return ET.tostring(mxfile, encoding="unicode")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    prefix = Path(sys.argv[2])
    prefix.with_suffix(".svg").write_text(build_svg(cfg), encoding="utf-8")
    prefix.with_suffix(".drawio").write_text(build_drawio(cfg), encoding="utf-8")
    print(prefix.with_suffix(".svg"))
    print(prefix.with_suffix(".drawio"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
