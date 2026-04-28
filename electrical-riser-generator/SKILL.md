---
name: electrical-riser-generator
description: generate and revise preliminary electrical load-calculation narratives, panel schedules, single-line/riser diagrams, and feeder schedules for multifamily or mixed-use building electrical design. use when asked to create dob-style electrical riser diagrams, service distribution diagrams, feeder tables, apartment panel schedules, or to review mechanical/plumbing/sprinkler plans for missing electrical loads and coordinate them into editable pdf/svg/drawio outputs.
---

# Electrical Riser Generator

## Core workflow

1. **Collect and classify inputs**
   - Separate file-supported facts from owner/user assumptions.
   - Search uploaded plan sets and internal/source files when the user references drawings, schedules, PDFs, or prior generated worksheets.
   - Keep separate load blocks for residential, commercial/tenant, house/common, mechanical, fire alarm/life safety, fire pump, and low-voltage/telecom/security.

2. **Review plans for missing electrical loads**
   - Architectural/sprinkler/plumbing plans: unit count, unit areas, cellar service spaces, pump/ejector symbols, fire pump schedule, roof/common areas, compactor room, meter rooms, and no/yes elevator.
   - Mechanical plans: ACCU/VRF, FCU, ERV, RTU/DOAS, fans, boilers, domestic electric water heaters, pump schedules, and noncoincident heating/cooling notes.
   - Lighting plans: use actual fixture wattage/counts where available; do not substitute area-based lighting when a fixture schedule exists.

3. **Build the riser/single-line diagram**
   - Use a true riser/single-line layout: floor lines, vertical risers, service entrance at cellar, main switchboard/distribution, meter bank, and floor-by-floor panel drops.
   - Panel boxes must show **ratings only** (for example `150A`, `200A`, `225A`). Put panel names outside the boxes.
   - Put feeder tags (`F-0`, `F-1`, etc.) on or near the feeder/wire, not inside the panel box.
   - Show fused disconnect switches for feeder outputs where used; do not clutter apartment risers with circuit breaker symbols.
   - Draw mechanical and house equipment as **parallel branch loads**, not daisy-chained serial loads.
   - Show fire alarm primary power and fire pump service/tap diagrammatically and flag final EOR/utility/code coordination.

4. **Create feeder schedules**
   - Include feeder ID, source, destination, rating, OCP/disconnect, conductors, EGC, raceway, and notes.
   - Size preliminary feeders consistently using copper conductors, 75C terminals, EMT, and the applicable NEC/NYC Electrical Code edition unless the user directs otherwise.
   - Cross-check feeder ratings against the panel schedules and load letter before issuing.

5. **Deliver editable outputs**
   - Provide at least one review PDF plus one editable format. Preferred editable formats are SVG and diagrams.net `.drawio`.
   - When the user wants manual fine tuning, package the editable SVG/drawio plus the PDF and feeder table into a ZIP.
   - State clearly what remains preliminary: utility service arrangement, fault current/AIC, selective coordination, voltage drop, final equipment MCA/MOCP, conductor derating, and EOR sign-off.

## Quality checks before final response

- No overlapping text, line labels, or feeder tags.
- Feeder lines are continuous and visibly connected.
- Parallel loads branch from a bus or panel, not from each other in series.
- All panel ratings match the latest panel schedule and load calculation.
- No elevator is shown unless the plans or user confirm an elevator.
- Commercial laundromat load remains owner-directed if actual equipment is not provided.
- Fire alarm and fire pump notes are present but not over-detailed beyond preliminary design basis.

## Bundled resources

- `references/riser-style-guide.md`: style and coordination checklist for producing DOB-style riser diagrams and feeder tables.
- `scripts/build_editable_riser.py`: configurable SVG/drawio generator template for creating editable riser-diagram files.
- `assets/sample_project_config.json`: example project configuration that can be copied and modified for a new building.
