#!/usr/bin/env python3
"""Generate a simple editable SVG and drawio riser skeleton from a project config.

Usage:
    python build_editable_riser.py config.json output_prefix
"""
import base64
import json
import sys
from html import escape
from pathlib import Path

W, H = 3456, 2304
RIGHT_X = 3020

def line(x1, y1, x2, y2, sw=2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#000" stroke-width="{sw}" fill="none"/>'

def rect(x, y, w, h, text='', size=18):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="white" stroke="#000" stroke-width="2"/>']
    if text:
        out.append(f'<text x="{x+w/2}" y="{y+h/2+size/3}" font-family="Arial" font-size="{size}" font-weight="700" text-anchor="middle">{escape(text)}</text>')
    return '\n'.join(out)

def text(x, y, value, size=14, bold=False, anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(str(value))}</text>'

def make_svg(cfg):
    floors = cfg.get('floors', ['ROOF','4TH FL','3RD FL','2ND FL','1ST FL','CELLAR'])
    floor_y = dict(zip(floors, [260, 535, 805, 1075, 1345, 1745]))
    p = cfg.get('panels', {})
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', '<rect width="100%" height="100%" fill="white"/>']
    out += [rect(24,24,W-48,H-48), line(RIGHT_X,24,RIGHT_X,H-24), text((RIGHT_X-24)/2+24,70,'ELECTRICAL RISER DIAGRAM',26,True,'middle')]
    out.append(text((RIGHT_X-24)/2+24,102, f"Project: {cfg.get('project','')} | {cfg.get('service','')}", 15, False, 'middle'))
    for floor, y in floor_y.items():
        out += [line(88,y,RIGHT_X-70,y,1.4), text(70,y-10,floor,17,True,'end')]
    # service and core gear
    out += [line(92,1930,715,1930,2.5), rect(245,1898,74,64,'SEB',18), rect(410,1898,92,64,'CT',18), rect(715,1825,660,260,'MDB',22)]
    # residential riser and apartment panel placeholders
    res_x = 465
    out.append(line(res_x,330,res_x,1745,3))
    units = cfg.get('units_by_floor', {'1ST FL':['AP-1A'], '2ND FL':['AP-2A','AP-2B','AP-2C','AP-2D','AP-2E','AP-2F','AP-2G'], '3RD FL':['AP-3A','AP-3B','AP-3C','AP-3D','AP-3E','AP-3F'], '4TH FL':['AP-4A','AP-4B','AP-4C','AP-4D','AP-4E','AP-4F']})
    for floor, names in units.items():
        y = floor_y[floor] - 76
        out.append(line(res_x,y,1850 if len(names)>1 else 760,y,2))
        for i, name in enumerate(names):
            x = (625 if len(names)==1 else 620) + i*164
            out += [rect(x,y+44,80,42,p.get('apartment','150A'),18), text(x+40,y+30,name,13,True,'middle')]
    out += [rect(575,1614,190,76,p.get('residential_meter_bank','800A'),20), rect(1510,1285,86,50,p.get('laundromat','200A'),18), rect(1510,1890,88,50,p.get('house','225A'),18), rect(2230,1001,86,50,p.get('mechanical','100A'),18)]
    # title block
    out += [text(RIGHT_X+196,58,cfg.get('project','PROJECT'),15,True,'middle'), text(RIGHT_X+196,82,cfg.get('address',''),13,True,'middle')]
    out.append('</svg>')
    return '\n'.join(out)

def make_drawio(svg):
    b64 = base64.b64encode(svg.encode()).decode()
    return f'<mxfile host="app.diagrams.net"><diagram name="E-300"><mxGraphModel page="1" pageWidth="3456" pageHeight="2304"><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="svg" value="" style="shape=image;imageAspect=0;aspect=fixed;image=data:image/svg+xml,{b64};" vertex="1" parent="1"><mxGeometry x="0" y="0" width="3456" height="2304" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>'

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    cfg = json.loads(Path(sys.argv[1]).read_text())
    prefix = Path(sys.argv[2])
    svg = make_svg(cfg)
    prefix.with_suffix('.svg').write_text(svg)
    prefix.with_suffix('.drawio').write_text(make_drawio(svg))
    print(prefix.with_suffix('.svg'))
    print(prefix.with_suffix('.drawio'))

if __name__ == '__main__':
    main()
