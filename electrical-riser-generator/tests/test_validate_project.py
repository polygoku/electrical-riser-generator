import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validate_project", ROOT / "scripts" / "validate_project.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def load_example():
    return json.loads((ROOT / "assets" / "optimized_retail_project_config.json").read_text())


def test_optimized_retail_example_passes():
    assert MODULE.validate(load_example()) == []


def test_duplicate_load_id_fails():
    cfg = load_example()
    cfg["source_register"].append(dict(cfg["source_register"][0]))
    errors = MODULE.validate(cfg)
    assert any("Duplicate canonical load_id" in item for item in errors)


def test_feeder_must_match_riser():
    cfg = load_example()
    cfg["riser"]["feeder_ids"].remove("F-3")
    errors = MODULE.validate(cfg)
    assert any("Feeders missing from riser" in item for item in errors)


def test_assumed_transformer_requires_field_verify_label():
    cfg = load_example()
    cfg["transformers"] = [{
        "name": "T-1",
        "status": "ASSUMED",
        "label": "112.5 kVA 480-208Y/120V",
        "secondary_panels": ["P-K"]
    }]
    errors = MODULE.validate(cfg)
    assert any("label lacks FIELD VERIFY" in item for item in errors)


def test_panel_overload_fails():
    cfg = load_example()
    cfg["panels"][0]["rating_a"] = 50
    errors = MODULE.validate(cfg)
    assert any("exceeds 50A rating" in item for item in errors)


def test_disconnect_kind_and_orientation_are_validated():
    cfg = load_example()
    cfg["riser"]["edges"] = [{
        "id": "F-1",
        "disconnect": {"kind": "mystery", "orientation": "sideways", "at": [100]},
    }]
    errors = MODULE.validate(cfg)
    assert any("unsupported disconnect kind" in item for item in errors)
    assert any("unsupported disconnect orientation" in item for item in errors)
    assert any("two-number list" in item for item in errors)
