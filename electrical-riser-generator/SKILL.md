---
name: electrical-riser-generator
description: generate and revise preliminary electrical load calculations, compact panel schedules, feeder schedules, and coordinated single-line/riser diagrams with native editable SVG/drawio outputs. use for multifamily, mixed-use, retail, restaurant, warehouse, and transformer-fed projects where drawing sets must be reviewed and all deliverables must reconcile.
---

# Electrical Riser Generator

The controlling standard is `references/repeatable-deliverables-standard.md`. Read it before generating a package.

## Required workflow

### 1. Review plans before drafting

Review every provided discipline and record findings before calculating:

- Architectural: floors, rooms, tenant/unit layout, service/electrical rooms, actual panel locations, roof/cellar/mezzanine areas.
- Mechanical: ACCU/VRF, FCU, ERV, RTU/DOAS, refrigeration, fans, pumps, boilers, water heaters, kitchen hoods and exhaust.
- Plumbing/fire protection: fire pump, jockey pump, sump/ejector, domestic water equipment and special loads.
- Electrical/lighting: service, metering, one-line/riser, panel schedules, feeder notes, fixture quantities and wattages.
- Owner equipment lists: treat as owner data, not nameplate data.

Do not begin the final load calculation until a source register exists.

### 2. Build a source and assumptions register

For every load, record:

- Canonical load ID.
- Description and quantity.
- Source file/sheet/location.
- Voltage, phase, poles, watts/VA/kVA, FLA/MCA/MOCP when available.
- Serving panel and physical location.
- Status: `PLAN`, `SCHEDULE`, `OWNER`, `ASSUMED`, or `FIELD VERIFY`.
- Conflict/coordination notes.

No load enters the calculation unless it is in this register. Run `scripts/validate_project.py` before issuing.

### 3. Calculate loads without conflating ratings

Keep these values separate:

- Existing service rating.
- Panel bus/main rating.
- Feeder/OCP rating.
- Connected load.
- Demand load.
- Calculated current.

The sum of downstream panel ratings is not the service load. A reported 400A service stays 400A unless the service itself is being changed.

Use this evidence order:

1. Equipment schedule/nameplate.
2. Electrical plan/riser/panel data.
3. Mechanical/plumbing/lighting/architectural plans.
4. Owner list.
5. Explicit preliminary assumption.

Use actual fixture wattage/counts and equipment MCA where available. Use MOCP only for OCP selection. Generic circuit-capacity allowances must be labeled and must not duplicate scheduled equipment.

Before totaling, deduplicate owner entries against mechanical schedules. Apply largest-motor, continuous-load, and noncoincident-load rules explicitly and only where applicable.

Report connected kVA, demand kVA, calculated current, service capacity, utilization, and remaining capacity. If existing building load is unknown, do not declare the service adequate without field demand information or an approved existing-load method.

### 4. Generate optimized panel schedules

Use the compact blue-header style.

Required header data:

- Panel name/description.
- Location.
- Mains/bus rating.
- Voltage, phase, wires.
- Mounting.
- AIC/SCCR status.
- Source feeder ID.

Required circuit-table order:

`CKT | DESCRIPTION | BREAKER | A | B | C | BREAKER | DESCRIPTION | CKT`

Rules:

- A/B/C columns use `X` marks only.
- 2P and 3P breakers occupy consecutive circuit positions.
- Continuation rows show `(description cont.)` and no repeated breaker rating.
- Preserve exact plan equipment names.
- Split lighting/receptacle groups into multiple circuits where needed.
- Balance 1P loads across A/B/C and rotate 2P loads across AB/BC/CA.
- Report phase totals and flag imbalance over 10% unless another threshold is specified.

### 5. Generate the feeder schedule

Minimum columns:

`ID | Source | Destination | Rating | OCP/Disconnect | Conductors | EGC | Raceway | Load basis | Notes`

Every riser feeder label must have exactly one table row, and every table row must appear on the riser. Cross-check service, panel, feeder, and OCP ratings independently.

Use copper conductors, 75C terminals, and EMT only as an explicitly stated preliminary basis unless directed otherwise. Transformer, motor, tap, and fire-pump feeders require their applicable special rules.

### 6. Build the riser/single-line

Use a true single-line layout with actual floors and actual panel locations.

Drawing rules:

- Panel boxes contain ratings only; names are outside.
- Feeder IDs and ratings are directly beside conductor runs.
- Fused disconnect symbols follow the Eaton combination convention: fuse first, then the open switch in the direction of power flow. Rotate the complete symbol with the feeder and keep it inline and connected on both ends.
- Non-fused disconnects use the open-switch portion only. Device labels and the feeder schedule must distinguish `FDS`/`SFDS` from `NFD`/`LDS`.
- No floating disconnects or open-ended feeders.
- Remote panels appear only at their actual serving location.
- Service/electrical rooms show feeder disconnects/callouts, not duplicate remote panels.
- All branch panels/equipment connect in parallel from their source bus.
- Never daisy-chain unrelated panels or equipment.
- Transformer workflow: source -> primary OCP/disconnect -> transformer -> secondary protection/tap arrangement -> destination panels.
- Any transformer not shown in the plans must be labeled `ASSUMED - FIELD VERIFY`.
- Do not invent an intermediate panel for drafting convenience.

For dense projects, split into multiple sheets and keep feeder IDs continuous.

### 7. Deliver truly editable files

Issue at least one PDF and one editable format. Preferred package:

- Load calculation DOCX/PDF.
- Panel schedules DOCX/PDF.
- Riser plus feeder schedule PDF.
- Native editable `.drawio`.
- Editable SVG.
- Feeder schedule XLSX/CSV.
- Source/assumptions register.
- Full ZIP.

The `.drawio` must contain native editable `mxCell` objects for all lines, labels, boxes, buses, and symbols. Embedded images, SVG backgrounds, or XML comments are not acceptable substitutes. The drawio, SVG, and PDF must match visually and logically.

## Mandatory QA before issue

- Source register complete; no duplicate canonical load IDs.
- Connected/demand totals reconcile.
- Service rating is not confused with downstream panel ratings.
- Panel ratings match riser and feeder schedule.
- Feeder IDs are one-to-one across all outputs.
- Multi-pole rows are consecutive and phase-correct.
- Phase balance is reported.
- Assumed transformers and equipment are visibly labeled.
- No invented panels remain.
- All lines and disconnect symbols are visibly connected.
- Native drawio opens with editable objects and matches SVG/PDF.
- DOCX and PDF files are rendered and visually inspected.
- XLSX formulas recalculate without errors.
- Final caveats identify utility/service arrangement, AIC/SCCR, selective coordination, voltage drop, derating, final MCA/MOCP, code edition, and EOR/AHJ sign-off.

## Bundled resources

- `references/repeatable-deliverables-standard.md`: controlling production and QA standard.
- `references/riser-style-guide.md`: drawing and schedule conventions.
- `references/lessons-learned-179-22nd-street.md`: dense mixed-use project lessons.
- `scripts/validate_project.py`: coordination validator.
- `scripts/build_editable_riser.py`: legacy multi-sheet generator; native drawio output must be verified before use.
- `assets/optimized_retail_project_config.json`: example showing service/panel/load separation and coordinated feeder IDs.
- `assets/sample_project_config.json`: legacy multifamily example.
