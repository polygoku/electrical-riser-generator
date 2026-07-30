#!/usr/bin/env python3
"""Validate coordinated electrical project inputs before deliverable generation.

Usage:
    python validate_project.py project.json

The validator intentionally fails fast on the coordination errors that most often
produce inconsistent load calculations, panel schedules, feeder tables, and risers.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REQUIRED_FEEDER_FIELDS = {
    "id", "source", "destination", "rating_a", "ocp", "conductors", "egc", "raceway"
}
VALID_STATUS = {"PLAN", "SCHEDULE", "OWNER", "ASSUMED", "FIELD VERIFY"}


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def phase_current(kva: float, voltage: float, phases: int) -> float:
    if phases == 3:
        return kva * 1000.0 / (math.sqrt(3.0) * voltage)
    return kva * 1000.0 / voltage


def validate(cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in ("project", "revision", "service", "source_register", "panels", "feeders"):
        if key not in cfg:
            error(errors, f"Missing top-level key: {key}")

    source_rows = cfg.get("source_register", [])
    ids = [str(r.get("load_id", "")).strip() for r in source_rows]
    missing_ids = [i for i, value in enumerate(ids, 1) if not value]
    if missing_ids:
        error(errors, f"Source-register rows missing load_id: {missing_ids}")
    duplicates = [item for item, count in Counter(ids).items() if item and count > 1]
    if duplicates:
        error(errors, f"Duplicate canonical load_id values: {duplicates}")

    for row in source_rows:
        status = row.get("status")
        if status not in VALID_STATUS:
            error(errors, f"Load {row.get('load_id')} has invalid status {status!r}")
        if status in {"ASSUMED", "FIELD VERIFY"} and not row.get("notes"):
            error(errors, f"Load {row.get('load_id')} is {status} but has no explanatory note")

    panel_names = {p.get("name") for p in cfg.get("panels", [])}
    if None in panel_names or "" in panel_names:
        error(errors, "Each panel requires a nonblank name")

    feeder_ids = [f.get("id") for f in cfg.get("feeders", [])]
    feeder_duplicates = [item for item, count in Counter(feeder_ids).items() if item and count > 1]
    if feeder_duplicates:
        error(errors, f"Duplicate feeder IDs: {feeder_duplicates}")

    for feeder in cfg.get("feeders", []):
        missing = REQUIRED_FEEDER_FIELDS - set(feeder)
        if missing:
            error(errors, f"Feeder {feeder.get('id')} missing fields: {sorted(missing)}")
        destination = feeder.get("destination")
        if feeder.get("destination_type") == "panel" and destination not in panel_names:
            error(errors, f"Feeder {feeder.get('id')} references unknown panel {destination}")

    riser_ids = cfg.get("riser", {}).get("feeder_ids", [])
    missing_on_riser = sorted(set(feeder_ids) - set(riser_ids))
    extra_on_riser = sorted(set(riser_ids) - set(feeder_ids))
    if missing_on_riser:
        error(errors, f"Feeders missing from riser: {missing_on_riser}")
    if extra_on_riser:
        error(errors, f"Riser feeder labels missing from feeder schedule: {extra_on_riser}")

    loads_by_panel: dict[str, float] = defaultdict(float)
    for row in source_rows:
        panel = row.get("panel")
        kva = float(row.get("connected_kva", 0.0) or 0.0)
        if panel:
            loads_by_panel[panel] += kva

    for panel in cfg.get("panels", []):
        name = panel.get("name")
        voltage = float(panel.get("voltage", 208))
        phases = int(panel.get("phases", 3))
        rating = float(panel.get("rating_a", 0))
        calculated = phase_current(loads_by_panel.get(name, 0.0), voltage, phases)
        panel["calculated_connected_a"] = round(calculated, 1)
        if calculated > rating + 0.05:
            error(errors, f"Panel {name}: connected current {calculated:.1f}A exceeds {rating:.0f}A rating")

    service = cfg.get("service", {})
    service_rating = float(service.get("rating_a", 0))
    service_voltage = float(service.get("voltage", 208))
    service_phases = int(service.get("phases", 3))
    demand_kva = float(cfg.get("load_summary", {}).get("demand_kva", 0.0))
    demand_a = phase_current(demand_kva, service_voltage, service_phases) if demand_kva else 0.0
    if demand_a > service_rating + 0.05:
        error(errors, f"Demand current {demand_a:.1f}A exceeds service rating {service_rating:.0f}A")

    transformers = cfg.get("transformers", [])
    for transformer in transformers:
        if transformer.get("status") in {"ASSUMED", "FIELD VERIFY"} and "FIELD VERIFY" not in transformer.get("label", ""):
            error(errors, f"Transformer {transformer.get('name')} is assumed but label lacks FIELD VERIFY")
        secondary_panels = transformer.get("secondary_panels", [])
        unknown = sorted(set(secondary_panels) - panel_names)
        if unknown:
            error(errors, f"Transformer {transformer.get('name')} references unknown panels: {unknown}")

    invented = [p.get("name") for p in cfg.get("panels", []) if p.get("status") == "INVENTED"]
    if invented:
        error(errors, f"Invented panels are prohibited: {invented}")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    cfg = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(cfg)
    if errors:
        print("VALIDATION FAILED")
        for item in errors:
            print(f"- {item}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
