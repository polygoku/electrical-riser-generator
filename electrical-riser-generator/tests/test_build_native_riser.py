import importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_native_riser", ROOT / "scripts" / "build_native_riser.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def example_config():
    return {
        "project": "Disconnect symbol test",
        "address": "Test address",
        "revision": "Rev0",
        "riser": {
            "nodes": [
                {"id": "source-h", "kind": "panel", "x": 100, "y": 100, "w": 100, "h": 60},
                {"id": "target-h", "kind": "panel", "x": 500, "y": 100, "w": 100, "h": 60},
                {"id": "source-v", "kind": "panel", "x": 750, "y": 100, "w": 100, "h": 60},
                {"id": "target-v", "kind": "panel", "x": 750, "y": 500, "w": 100, "h": 60},
            ],
            "edges": [
                {
                    "id": "F-1",
                    "source": "source-h",
                    "target": "target-h",
                    "points": [[200, 130], [500, 130]],
                    "disconnect": {"kind": "fused", "label": "60A/3P FDS"},
                },
                {
                    "id": "F-2",
                    "source": "source-v",
                    "target": "target-v",
                    "points": [[800, 160], [800, 500]],
                    "disconnect": {"kind": "non_fused", "label": "NFD"},
                },
            ],
        },
    }


def test_disconnect_aliases_and_orientation():
    assert MODULE.disconnect_spec(True)["kind"] == "fused"
    assert MODULE.disconnect_spec("SFDS")["kind"] == "fused"
    assert MODULE.disconnect_spec("NFD")["kind"] == "non_fused"
    assert MODULE.disconnect_placement([[0, 0], [0, 200]], {"kind": "fused"}) == (0.0, 100.0, "down")
    assert MODULE.disconnect_placement([[200, 0], [0, 0]], {"kind": "fused"}) == (100.0, 0.0, "left")


def test_svg_symbols_rotate_with_feeder_and_preserve_device_type():
    svg = MODULE.build_svg(example_config())
    assert 'data-symbol="fused-disconnect" data-orientation="right"' in svg
    assert 'data-symbol="non_fused-disconnect" data-orientation="down"' in svg
    assert "60A/3P FDS" in svg
    assert "data:image" not in svg
    assert "<image" not in svg


def test_drawio_uses_native_fuse_and_switch_geometry():
    drawio = MODULE.build_drawio(example_config())
    root = ET.fromstring(drawio)
    cells = {cell.get("id"): cell for cell in root.findall(".//mxCell")}
    assert "d1-fuse" in cells
    assert "d1-line-4" in cells
    assert "d2-fuse" not in cells
    assert "d2-line-1" in cells
    assert all("image;" not in (cell.get("style") or "") for cell in cells.values())
