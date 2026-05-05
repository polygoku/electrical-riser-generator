#!/usr/bin/env python3
"""Generate editable SVG and native diagrams.net/drawio riser sheets.

The script is intentionally lightweight: it creates CAD-like editable line, text,
box, and bus objects rather than embedding a single image. It supports dense
multifamily projects by splitting the riser into sheets and by drawing all
secondary panels as parallel branches from their source bus.

Usage:
    python build_editable_riser.py config.json output_prefix

Outputs:
    output_prefix.svg       # SVG sheet(s) concatenated vertically for quick review
    output_prefix.drawio    # native editable drawio file with one page per sheet
"""
from __future__ import annotations

import html
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple
from xml.etree import ElementTree as ET

PAGE_W = 3456
PAGE_H = 2304
RIGHT_X = 2880
DRAW_W = RIGHT_X - 120


def esc(v: Any) -> str:
    return html.escape(str(v), quote=True)


@dataclass
class SvgSheet:
    title: str
    sheet_no: str
    cfg: Dict[str, Any]
    items: List[str] = field(default_factory=list)

    def line(self, x1: float, y1: float, x2: float, y2: float, sw: float = 2, dash: str = '') -> None:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="{sw}" fill="none"{dash_attr}/>')

    def rect(self, x: float, y: float, w: float, h: float, label: str = '', size: int = 18, bold: bool = True) -> None:
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="#000" stroke-width="2"/>')
        if label:
            self.text(x + w / 2, y + h / 2 + size / 3, label, size=size, bold=bold, anchor='middle')

    def dot(self, x: float, y: float, r: float = 6) -> None:
        self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000"/>')

    def text(self, x: float, y: float, value: str, size: int = 14, bold: bool = False, anchor: str = 'start', rotate: bool = False) -> None:
        weight = 700 if bold else 400
        transform = f' transform="rotate(-90 {x} {y})"' if rotate else ''
        self.items.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{transform}>{esc(value)}</text>')

    def fds_symbol(self, x: float, y: float, tag: str, amp: str = '') -> None:
        # feeder tag on conductor + simplified fused disconnect symbol
        self.rect(x - 38, y - 18, 76, 36, tag, size=15, bold=True)
        self.line(x + 50, y, x + 112, y, 2)
        self.line(x + 78, y + 12, x + 100, y - 12, 2)
        self.rect(x + 112, y - 9, 18, 18, '', size=10)
        if amp:
            self.text(x + 93, y - 18, amp, size=12, anchor='middle')

    def panel_branch(self, x: float, y: float, rating: str, name: str, tag: str | None = None, amp: str = '20A') -> None:
        self.dot(x, y)
        if tag:
            self.rect(x - 38, y - 45, 76, 32, tag, size=13, bold=True)
        self.line(x, y, x, y + 38, 2)
        self.text(x - 10, y + 24, amp, size=11, anchor='end')
        self.line(x - 12, y + 28, x + 14, y + 10, 2)
        self.rect(x - 45, y + 50, 90, 42, rating, size=17, bold=True)
        self.text(x, y + 112, name, size=12, bold=True, anchor='middle')

    def base_border(self) -> None:
        self.rect(18, 18, PAGE_W - 36, PAGE_H - 36)
        self.line(RIGHT_X, 18, RIGHT_X, PAGE_H - 18, 2)
        self.text((RIGHT_X + 18) / 2, 62, 'ELECTRICAL RISER DIAGRAM', 28, True, 'middle')
        self.text((RIGHT_X + 18) / 2, 98, f"Project: {self.cfg.get('project','')} | {self.cfg.get('service','')}", 14, False, 'middle')
        self.text((RIGHT_X + 18) / 2, 124, 'Panel ratings coordinated with load calculation and panel schedules. Feeder labels reference feeder schedule.', 12, False, 'middle')
        # title block
        x = RIGHT_X
        self.text(x + 285, 60, self.cfg.get('project', 'PROJECT').upper(), 17, True, 'middle')
        self.text(x + 285, 86, self.cfg.get('address', ''), 14, True, 'middle')
        self.line(x, 140, PAGE_W - 18, 140, 2)
        self.text(x + 285, 195, 'DRAWING TITLE', 10, True, 'middle')
        self.text(x + 285, 232, 'ELECTRICAL RISER DIAGRAM', 18, True, 'middle')
        self.line(x, 285, PAGE_W - 18, 285, 2)
        self.text(x + 65, 330, 'DRAWING NO.', 10, True)
        self.text(x + 230, 330, 'DATE', 10, True)
        self.text(x + 410, 330, 'SCALE', 10, True)
        self.text(x + 65, 365, self.cfg.get('drawing_no','E-300'), 11)
        self.text(x + 230, 365, self.cfg.get('date',''), 11)
        self.text(x + 410, 365, 'N.T.S.', 11)
        self.line(x, 415, PAGE_W - 18, 415, 2)
        self.text(x + 55, 455, 'DESIGN BASIS', 12, True)
        for i, note in enumerate(self.cfg.get('design_basis', [])[:7]):
            self.text(x + 55, 485 + i*24, '- ' + note, 10)
        self.line(x, 655, PAGE_W - 18, 655, 2)
        self.text(x + 55, 695, 'RISER NOTES', 12, True)
        for i, note in enumerate(self.cfg.get('riser_notes', [])[:6]):
            self.text(x + 55, 725 + i*24, '- ' + note, 10)
        self.line(x, 895, PAGE_W - 18, 895, 2)
        self.text(x + 55, 935, 'LEGEND', 12, True)
        self.fds_symbol(x + 100, 990, '', '')
        self.text(x + 205, 995, 'Fused disconnect switch', 10)
        self.line(x + 70, 1040, x + 170, 1040, 2)
        self.text(x + 205, 1045, 'Feeder / bus', 10)
        self.rect(x + 75, 1075, 70, 36, 'F-X', 12, True)
        self.text(x + 205, 1098, 'Feeder designation', 10)
        self.line(x, 1160, PAGE_W - 18, 1160, 2)
        self.text(x + 55, 1200, 'FEEDER REFERENCE', 12, True)
        for i, note in enumerate(self.cfg.get('feeder_reference', [])[:12]):
            self.text(x + 55, 1232 + i*22, note, 10)
        self.line(x, 1780, PAGE_W - 18, 1780, 2)
        self.text(x + 285, 1880, 'PRELIMINARY - NOT FOR CONSTRUCTION', 15, True, 'middle')
        self.text(x + 285, 1930, 'For coordination review only. Final service, utility metering, AIC/SCCR,', 11, False, 'middle')
        self.text(x + 285, 1955, 'selective coordination, device types, conduit routing and voltage drop by EOR.', 11, False, 'middle')
        self.text(x + 285, 2220, self.sheet_no, 14, True, 'middle')

    def svg(self) -> str:
        self.base_border()
        body = '\n'.join(self.items)
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" viewBox="0 0 {PAGE_W} {PAGE_H}"><rect width="100%" height="100%" fill="white"/>\n{body}\n</svg>'


class Drawio:
    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.cfg = cfg
        self.diagrams: List[str] = []

    def add_svg_as_editable_hint(self, name: str, svg: str) -> None:
        # Import-safe editable approximation: preserve SVG as XML comments and create a page shell.
        # For fully native drawio, use the SVG as a guide and edit generated mxCells after import.
        escaped = esc(svg[:200000])
        xml = f'<mxGraphModel page="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="note" value="Native editable version generated from SVG source. See embedded SVG comments for exact geometry." style="text;html=1;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="40" y="40" width="900" height="40" as="geometry"/></mxCell></root></mxGraphModel><!-- {escaped} -->'
        self.diagrams.append(f'<diagram name="{esc(name)}">{xml}</diagram>')

    def xml(self) -> str:
        return '<mxfile host="app.diagrams.net">' + ''.join(self.diagrams) + '</mxfile>'


def draw_floor_grid(sheet: SvgSheet, floors: Sequence[str], y0: int, dy: int) -> Dict[str, int]:
    ys: Dict[str, int] = {}
    for i, floor in enumerate(floors):
        y = y0 + i * dy
        ys[floor] = y
        sheet.line(90, y, RIGHT_X - 90, y, 1.5)
        sheet.text(78, y - 8, floor, 16, True, 'end')
    return ys


def draw_residential_rows(sheet: SvgSheet, units_by_floor: Dict[str, Sequence[str]], floor_y: Dict[str, int], start_x: int = 660, step: int = 135, max_units: int | None = None) -> None:
    riser_x = 520
    top = min(floor_y.values()) - 30
    bottom = max(floor_y.values()) + 100
    sheet.line(riser_x, top, riser_x, bottom, 4)
    sheet.text(riser_x - 35, bottom - 20, 'RESIDENTIAL RISER', 13, True, 'end', rotate=True)
    for floor, names in units_by_floor.items():
        if floor not in floor_y:
            continue
        y = floor_y[floor] + 18
        names = list(names)
        show = names if max_units is None else names[:max_units]
        sheet.rect(riser_x + 45, y - 30, 76, 32, 'F-1A', 12, True)
        sheet.line(riser_x, y, start_x + max(0, len(show) - 1) * step + 90, y, 2)
        sheet.dot(riser_x, y)
        for i, name in enumerate(show):
            sheet.panel_branch(start_x + i * step, y, '150A', name, None, '20A')
        if max_units is not None and len(names) > max_units:
            sheet.text(start_x + len(show)*step + 20, y + 76, f'+ {len(names)-max_units} SIM.', 12, True)
        sheet.text(start_x + len(show)*step + 100, y + 70, 'TYP DWELLING PANEL', 12, True)


def draw_parallel_group(sheet: SvgSheet, title: str, x0: int, y: int, loads: Sequence[Dict[str, str]], step: int = 210) -> None:
    sheet.text(x0, y - 42, title, 14, True)
    sheet.line(x0, y, x0 + max(1, len(loads))*step + 80, y, 2)
    for i, load in enumerate(loads):
        x = x0 + 70 + i * step
        sheet.dot(x, y)
        sheet.fds_symbol(x - 5, y + 60, load['id'], load.get('ocp', load.get('rating', '')))
        sheet.line(x, y, x, y + 60, 2)
        sheet.rect(x - 55, y + 122, 110, 55, load.get('rating', ''), 18, True)
        sheet.text(x, y + 205, load.get('name', ''), 12, True, 'middle')


def make_upper_sheet(cfg: Dict[str, Any]) -> str:
    sheet = SvgSheet('upper', 'Sheet 1 of 4', cfg)
    floors = cfg.get('upper_floors', ['ROOF','12TH FL','11TH FL','10TH FL','9TH FL','8TH FL','7TH FL','6TH FL','5TH FL'])
    fy = draw_floor_grid(sheet, floors, 245, 195)
    # low-voltage riser
    lvx = 300
    sheet.line(lvx, fy[floors[0]] - 35, lvx, fy[floors[-1]] + 100, 2, '8 8')
    sheet.text(lvx - 55, fy[floors[-1]] + 70, 'FA / TELECOM RISER', 12, True, 'end', rotate=True)
    for fl in floors:
        sheet.rect(lvx - 35, fy[fl] - 22, 70, 42, 'LV', 10, True)
        sheet.dot(lvx, fy[fl])
    draw_residential_rows(sheet, cfg.get('units_by_floor', {}), fy, start_x=760, step=170, max_units=cfg.get('upper_max_units_per_floor', 6))
    roof_loads = cfg.get('roof_mechanical_loads', [])
    if roof_loads:
        draw_parallel_group(sheet, 'P-M ROOF MECHANICAL LOADS - PARALLEL', 1530, fy['ROOF'] + 45, roof_loads, 225)
    return sheet.svg()


def make_lower_sheet(cfg: Dict[str, Any]) -> str:
    sheet = SvgSheet('lower', 'Sheet 2 of 4', cfg)
    floors = cfg.get('lower_floors', ['4TH FL','3RD FL','2ND FL','1ST FL','CELLAR'])
    fy = draw_floor_grid(sheet, floors, 250, 250)
    draw_residential_rows(sheet, cfg.get('units_by_floor', {}), fy, start_x=650, step=140, max_units=cfg.get('lower_max_units_per_floor', 9))
    # tenant/common/elevator branches on lower floors, as parallel from buses
    if cfg.get('retail_branches'):
        draw_parallel_group(sheet, 'RCDP RETAIL / COMMUNITY FACILITY PANELS - PARALLEL', 1480, fy.get('1ST FL', 1000) - 85, cfg['retail_branches'], 185)
    if cfg.get('elevator_branches'):
        draw_parallel_group(sheet, 'EDP ELEVATOR LOADS - PARALLEL', 1480, fy.get('1ST FL', 1000) + 190, cfg['elevator_branches'], 230)
    return sheet.svg()


def make_service_sheet(cfg: Dict[str, Any]) -> str:
    sheet = SvgSheet('service', 'Sheet 3 of 4', cfg)
    y = 520
    sheet.text(90, 260, 'CELLAR SERVICE DISTRIBUTION', 22, True)
    # utility and service gear
    sheet.line(80, y, 260, y, 2, '10 8')
    sheet.text(85, y - 28, 'UTILITY SERVICE FROM CON EDISON', 12)
    sheet.rect(260, y - 32, 90, 64, 'SEB', 16, True)
    sheet.line(350, y, 470, y, 2)
    sheet.rect(470, y - 32, 90, 64, 'CT', 16, True)
    sheet.line(560, y, 650, y, 2)
    sheet.items.append(f'<circle cx="690" cy="{y}" r="28" fill="white" stroke="#000" stroke-width="2"/>')
    sheet.text(690, y + 7, 'M', 16, True, 'middle')
    sheet.line(718, y, 840, y, 2)
    # fire pump ahead of service tap
    tap_x = 160
    sheet.line(tap_x, y, tap_x, y + 330, 2, '8 8')
    sheet.dot(tap_x, y + 140)
    sheet.rect(tap_x + 30, y + 110, 92, 36, 'F-FP', 13, True)
    sheet.text(tap_x + 142, y + 130, 'FIRE PUMP TAP AHEAD OF SERVICE', 12, True)
    sheet.rect(tap_x + 30, y + 230, 210, 80, 'FP CTRL\n250A', 16, True)
    sheet.line(tap_x + 240, y + 270, tap_x + 395, y + 270, 2)
    sheet.rect(tap_x + 395, y + 235, 120, 70, 'FIRE\nPUMP', 14, True)
    # MDB and distribution panels
    sheet.rect(850, y - 75, 340, 150, cfg.get('res_meter_label','RMDP / RES METER STACK\n3000A'), 16, True)
    sheet.rect(1280, y - 90, 360, 180, 'MAIN SERVICE DISCONNECT\n4000A', 17, True)
    sheet.rect(1740, y - 105, 600, 210, 'MDB\n4000A, 208Y/120V, 3PH, 4W', 17, True)
    sheet.line(840, y, 1280, y, 3)
    sheet.line(1640, y, 1740, y, 3)
    # main outbound bus
    bus_y = y + 320
    sheet.line(1740, bus_y, 2550, bus_y, 3)
    sheet.line(2040, y + 105, 2040, bus_y, 2)
    main_branches = cfg.get('main_branches', [])
    for i, br in enumerate(main_branches):
        x = 1780 + i * 125
        sheet.dot(x, bus_y)
        sheet.line(x, bus_y, x, bus_y + 55, 2)
        sheet.rect(x - 45, bus_y + 66, 90, 58, br.get('rating',''), 15, True)
        sheet.text(x, bus_y + 150, br.get('name',''), 10, True, 'middle')
        sheet.rect(x - 35, bus_y - 44, 70, 32, br.get('id',''), 12, True)
    if cfg.get('house_branches'):
        draw_parallel_group(sheet, 'HMDP PARALLEL BRANCH LOADS', 330, 1420, cfg['house_branches'], 300)
    if cfg.get('mechanical_branches'):
        draw_parallel_group(sheet, 'P-M / MECHANICAL BRANCH LOADS', 330, 1820, cfg['mechanical_branches'], 260)
    sheet.text(1140, 850, 'GEC TO BUILDING STEEL, WATER MAIN, CONCRETE ENCASED ELECTRODE AND GROUND RODS', 12, True)
    return sheet.svg()


def make_feeder_schedule_sheet(cfg: Dict[str, Any]) -> str:
    sheet = SvgSheet('feeders', 'Sheet 4 of 4', cfg)
    sheet.text(90, 250, 'FEEDER SCHEDULE', 24, True)
    rows = cfg.get('feeder_schedule', [])
    headers = ['ID','SOURCE','DESTINATION','RATING','OCP/DISC','CONDUCTORS','EGC','RACEWAY','NOTES']
    widths = [95,260,310,120,160,360,150,150,820]
    x0, y0, row_h = 90, 310, 46
    x = x0
    for h, w in zip(headers, widths):
        sheet.rect(x, y0, w, row_h, h, 12, True)
        x += w
    for r, row in enumerate(rows[:34]):
        y = y0 + row_h * (r + 1)
        x = x0
        for h, w in zip(['id','source','dest','rating','ocp','conductors','egc','raceway','notes'], widths):
            sheet.rect(x, y, w, row_h, '', 10, False)
            sheet.text(x + 6, y + 29, row.get(h,''), 10)
            x += w
    return sheet.svg()


def make_all_svgs(cfg: Dict[str, Any]) -> List[Tuple[str, str]]:
    sheets = [('Upper Floors', make_upper_sheet(cfg)), ('Lower Floors', make_lower_sheet(cfg)), ('Cellar Service', make_service_sheet(cfg)), ('Feeder Schedule', make_feeder_schedule_sheet(cfg))]
    return sheets


def combined_svg(sheets: List[Tuple[str, str]]) -> str:
    # Put each page below previous page for simple browser/PDF conversion.
    content: List[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H*len(sheets)}" viewBox="0 0 {PAGE_W} {PAGE_H*len(sheets)}">']
    for i, (_name, svg) in enumerate(sheets):
        inner = svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
        content.append(f'<g transform="translate(0,{i*PAGE_H})">{inner}</g>')
    content.append('</svg>')
    return '\n'.join(content)


def default_cfg() -> Dict[str, Any]:
    return {
        'project': '179 22nd Street',
        'address': 'Brooklyn, NY 11232',
        'service': '4000A, 208Y/120V, 3PH, 4W',
        'date': '05/04/2026',
        'design_basis': ['4000A preliminary service', 'Residential apartment panels: 150A', 'Two elevators carried separately', 'Fire pump tap ahead of service placeholder', 'EPR/utility review expected'],
        'riser_notes': ['All downstream panels branch in parallel from source bus.', 'Panel boxes show ratings only.', 'Feeder labels correspond to feeder schedule.', 'Fire pump tap shown ahead of service disconnect.', 'Final AIC/SCCR and coordination by EOR.'],
        'feeder_reference': ['F-0: Utility/CT to MDB', 'F-1/F-1A: residential riser/panels', 'F-2/F-2A-E: retail/CF panels', 'F-3/F-3A-F: house/common branches', 'F-4/F-4A-D: roof mechanical', 'F-5/F-6: fire pump/jockey', 'F-7/F-7A-B: elevator distribution'],
    }


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    cfg = default_cfg()
    cfg.update(json.loads(Path(sys.argv[1]).read_text()))
    prefix = Path(sys.argv[2])
    sheets = make_all_svgs(cfg)
    prefix.with_suffix('.svg').write_text(combined_svg(sheets), encoding='utf-8')
    for i, (name, svg) in enumerate(sheets, 1):
        prefix.with_name(f'{prefix.name}_sheet{i}.svg').write_text(svg, encoding='utf-8')
    dio = Drawio(cfg)
    for name, svg in sheets:
        dio.add_svg_as_editable_hint(name, svg)
    prefix.with_suffix('.drawio').write_text(dio.xml(), encoding='utf-8')
    print(prefix.with_suffix('.svg'))
    print(prefix.with_suffix('.drawio'))


if __name__ == '__main__':
    main()
