#!/usr/bin/env python3
"""Generate matching SVG and native editable diagrams.net riser files.

Input JSON requires:
- project, address, revision, service
- riser.nodes: [{id, kind, label, rating, x, y, w, h}]
- riser.edges: [{id, source, target, label, points?}]

Every SVG object has a corresponding native mxCell object. No image or SVG is
embedded in the drawio file.

Usage:
    python build_native_riser.py project.json output_prefix
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

PAGE_W = 1600
PAGE_H = 1000


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


def build_svg(cfg: dict[str, Any]) -> str:
    items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" viewBox="0 0 {PAGE_W} {PAGE_H}">', '<rect width="100%" height="100%" fill="white"/>']
    items.append(svg_text(PAGE_W / 2, 36, cfg.get("project", "ELECTRICAL RISER"), 22, True))
    items.append(svg_text(PAGE_W / 2, 60, f"{cfg.get('address','')} | {cfg.get('revision','')}", 12))

    nodes = {n["id"]: n for n in cfg.get("riser", {}).get("nodes", [])}
    for edge in cfg.get("riser", {}).get("edges", []):
        source = nodes[edge["source"]]
        target = nodes[edge["target"]]
        sx = source["x"] + source.get("w", 120)
        sy = source["y"] + source.get("h", 60) / 2
        tx = target["x"]
        ty = target["y"] + target.get("h", 60) / 2
        points = edge.get("points") or [[sx, sy], [tx, sy], [tx, ty]]
        d = " ".join(("M" if i == 0 else "L") + f" {p[0]} {p[1]}" for i, p in enumerate(points))
        items.append(f'<path d="{d}" fill="none" stroke="#000" stroke-width="2"/>')
        label = edge.get("label", "")
        if label:
            mx = sum(p[0] for p in points) / len(points)
            my = sum(p[1] for p in points) / len(points) - 8
            items.append(svg_text(mx, my, label, 12, True))
        if edge.get("disconnect"):
            p = points[-2] if len(points) > 2 else points[0]
            x, y = p[0] + 28, p[1]
            items.append(f'<rect x="{x-10}" y="{y-7}" width="20" height="14" fill="white" stroke="#000" stroke-width="2"/>')
            items.append(f'<line x1="{x+14}" y1="{y+8}" x2="{x+34}" y2="{y-8}" stroke="#000" stroke-width="2"/>')
            items.append(f'<circle cx="{x+38}" cy="{y}" r="4" fill="white" stroke="#000" stroke-width="2"/>')

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


def build_drawio(cfg: dict[str, Any]) -> str:
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "version": "24.7.17"})
    diagram = ET.SubElement(mxfile, "diagram", {"name": "Electrical Riser"})
    model = ET.SubElement(diagram, "mxGraphModel", {"dx": "1200", "dy": "800", "grid": "1", "gridSize": "10", "page": "1", "pageScale": "1", "pageWidth": str(PAGE_W), "pageHeight": str(PAGE_H)})
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})

    add_vertex(root, "title", f"<b>{esc(cfg.get('project','ELECTRICAL RISER'))}</b><br>{esc(cfg.get('address',''))} | {esc(cfg.get('revision',''))}", 350, 10, 900, 55, "text;html=1;align=center;verticalAlign=middle;fontSize=18;strokeColor=none;fillColor=none;")

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
        points = edge.get("points", [])
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;strokeWidth=2;"
        add_edge(root, f"e{i}", esc(edge.get("label", "")), node_map[edge["source"]], node_map[edge["target"]], points, style)
        if edge.get("disconnect") and points:
            p = points[-2] if len(points) > 2 else points[0]
            add_vertex(root, f"d{i}", "", p[0] + 15, p[1] - 10, 55, 20, "shape=mxgraph.electrical.abstract.switch;html=1;strokeWidth=2;fillColor=white;")

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
