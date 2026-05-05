---
name: electrical-riser-generator
description: generate and revise preliminary electrical load-calculation narratives, panel schedules, single-line/riser diagrams, feeder schedules, and editable SVG/drawio outputs for multifamily or mixed-use building electrical design. use when asked to create dob-style electrical riser diagrams, service distribution diagrams, feeder tables, apartment panel schedules, or to review architectural/mechanical/plumbing/sprinkler/lighting plans for missing electrical loads and coordinated electrical deliverables.
---

# Electrical Riser Generator

## Core workflow

1. **Collect and classify inputs**
   - Separate file-supported facts from owner/user assumptions.
   - Search uploaded plan sets and internal/source files when the user references drawings, schedules, PDFs, or prior generated worksheets.
   - Keep separate load blocks for residential, commercial/tenant, house/common, mechanical, fire alarm/life safety, fire pump, elevators, and low-voltage/telecom/security.

2. **Review plans for missing electrical loads**
   - Architectural/sprinkler/plumbing plans: unit count, unit areas, cellar service spaces, pump/ejector symbols, fire pump schedule, roof/common areas, compactor room, meter rooms, and elevator count.
   - Mechanical plans: ACCU/VRF, FCU, ERV, RTU/DOAS, fans, boilers, domestic electric water heaters, pump schedules, elevator/EMR equipment, and noncoincident heating/cooling notes.
   - Lighting plans: use actual fixture wattage/counts where available; do not substitute area-based lighting when a fixture schedule exists.

3. **Build the riser/single-line diagram**
   - Use a true riser/single-line layout: floor lines, vertical risers, service entrance at cellar, main switchboard/distribution, meter bank, and floor-by-floor panel drops.
   - Panel boxes must show **ratings only** (for example `150A`, `200A`, `225A`). Put panel names outside the boxes.
   - Put feeder tags (`F-0`, `F-1`, etc.) on or near the feeder/wire, not inside the panel box.
   - Show fused disconnect switches for feeder outputs where used; do not clutter apartment risers with circuit breaker symbols.
   - Draw downstream panels/equipment as **parallel branches from their source bus or distribution panel**. Never daisy-chain retail, common, mechanical, elevator, pump, or apartment panels in series.
   - For dense buildings, split the riser into multiple sheets: upper repetitive residential floors, lower residential/tenant floors, and cellar/service distribution. Keep feeder IDs continuous across sheets.
   - Show fire pump supply as a line-side / ahead-of-service-disconnect tap when that is the selected preliminary arrangement, and flag final AHJ/utility/controller coordination.
   - Show fire alarm primary power diagrammatically and flag final local-code coordination.

4. **Create panel schedules**
   - Use compact centered schedules rather than page-width tables when the user wants a polished schedule style.
   - Show 2-pole and 3-pole loads occupying multiple consecutive circuit positions with continuation rows.
   - Split large retail/community lighting and receptacle loads into multiple circuits such as `Lighting #1`, `Lighting #2`, `Receptacles #1`, `Receptacles #2`, etc.
   - Cross-check panel ratings, elevator count, service size, and large loads against the latest load letter before issuing.

5. **Create feeder schedules**
   - Include feeder ID, source, destination, rating, OCP/disconnect, conductors, EGC, raceway, and notes.
   - Size preliminary feeders consistently using copper conductors, 75C terminals, EMT, and the applicable NEC/NYC Electrical Code edition unless the user directs otherwise.
   - Cross-check feeder ratings against the riser, panel schedules, and load letter before issuing.

6. **Deliver editable outputs**
   - Provide at least one review PDF plus one editable format. Preferred editable formats are SVG and diagrams.net `.drawio`.
   - The `.drawio` must use native editable cells, not a single embedded background image.
   - When the user wants manual fine tuning, package the editable SVG/drawio plus the PDF and feeder table into a ZIP.
   - State clearly what remains preliminary: utility service arrangement, fault current/AIC, selective coordination, voltage drop, final equipment MCA/MOCP, conductor derating, and EOR sign-off.

## Quality checks before final response

- No overlapping text, line labels, feeder tags, boxes, or symbols.
- Feeder lines are continuous and visibly connected.
- Parallel loads branch from a source bus or distribution panel, not from each other in series.
- All panel boxes are complete closed shapes.
- All panel ratings match the latest panel schedule and load calculation.
- Elevator count matches the plans; separate service/passenger elevators if both are shown.
- Fire pump is shown ahead of service tap when required by the current design basis.
- Commercial/tenant loads are calculated when area/HVAC/equipment data are available; use owner-directed placeholders only when explicitly directed.
- Feeder schedule is generated and IDs match the riser labels.
- EPR/utility/code notes are included when service size, kVA, voltage, fire pump, or service room cooling triggers are relevant.

## Bundled resources

- `references/riser-style-guide.md`: style and coordination checklist for DOB-style riser diagrams and feeder tables.
- `references/lessons-learned-179-22nd-street.md`: practical lessons from the 179 22nd Street sprint, including multi-sheet layout and parallel branch corrections.
- `scripts/build_editable_riser.py`: configurable SVG/drawio generator template for editable multi-sheet riser diagrams and feeder schedules.
- `assets/sample_project_config.json`: example project configuration that can be copied and modified for a new building.
