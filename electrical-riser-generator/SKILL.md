---
name: electrical-riser-generator
description: generate and revise preliminary electrical load-calculation narratives, panel schedules, single-line/riser diagrams, feeder schedules, and editable SVG/drawio outputs for multifamily, retail, commercial, and mixed-use electrical design. use when asked to create dob-style electrical riser diagrams, service distribution diagrams, feeder tables, panel schedules, transformer-fed tenant risers, or to review architectural/mechanical/plumbing/sprinkler/lighting plans for missing electrical loads and coordinated electrical deliverables.
---

# Electrical Riser Generator

## Core workflow

1. **Collect and classify inputs**
   - Separate file-supported facts from owner/user assumptions.
   - Search uploaded plan sets and source files when the user references drawings, schedules, PDFs, field photos, or prior generated worksheets.
   - Keep separate load blocks for residential, commercial/tenant, house/common, mechanical, fire alarm/life safety, fire pump, elevators, low-voltage/telecom/security, signs, and transformer-fed loads.

2. **Review plans for missing electrical loads**
   - Architectural/sprinkler/plumbing plans: unit count, tenant areas, service spaces, pump/ejector symbols, fire pump schedule, meter rooms, utility/service entrance, and elevator count.
   - Mechanical plans: ACCU/VRF, FCU, ERV, RTU/DOAS, WSHP, fans, boilers, domestic electric water heaters, pump schedules, elevator/EMR equipment, and noncoincident heating/cooling notes.
   - Lighting/electrical plans: use actual fixture wattage/counts where available; do not substitute area-based lighting when a fixture schedule exists.
   - Field photos: verify existing panel voltage, phase, wire count, panel ampere rating, breaker spaces, and manufacturer labels. If a field photo shows an existing 480Y/277V panel, consider a transformer-fed 208Y/120V tenant-panel workflow.

3. **Build the riser/single-line diagram**
   - Use a true riser/single-line layout: floor lines, vertical risers, service entrance, main switchboard/distribution, meter bank, transformer, and floor-by-floor panel drops.
   - Place physical panels only once at their serving floor/location. In the cellar/service room, show feeder disconnects/callouts to remote panels, not duplicate panel boxes.
   - Panel boxes show **ratings only**; put names outside/below boxes.
   - Feeder tags such as `F-1` must be plain text beside the feeder/conduit run and must correspond to the feeder schedule. Do not put feeder IDs in panel boxes. Avoid boxed feeder labels unless the user explicitly asks.
   - Draw downstream panels/equipment as **parallel branches from their source bus or distribution panel**. Never daisy-chain retail, common, mechanical, elevator, pump, apartment, or tenant panels in series.
   - Use switch-fuse/disconnect symbols only where appropriate: service/distribution feeders, transformer primary/secondary as needed, mechanical equipment, major tenant equipment, fire pump/elevator coordination, and manufacturer/SCCR-driven disconnects. Do not add a fused disconnect to every apartment or ordinary panel tap.
   - A switch-fuse/disconnect symbol must be connected on both ends and lie in-line with the circuit. Never leave floating disconnect symbols beside wires.
   - For transformer-fed tenant projects, show: existing source panel voltage/rating -> primary feeder/OCP -> transformer kVA and voltage -> secondary MDP/disconnect -> tenant/mechanical panels. Include grounding/bonding and final EOR verification notes.
   - For dense projects, split the riser into multiple sheets: upper repetitive floors, lower tenant/common floors, cellar/service distribution, and feeder schedule.

4. **Create panel schedules**
   - Use compact centered schedules rather than page-width tables when the user wants a polished schedule style.
   - Use A/B/C phase columns with simple `X` marks only. Do not put phase labels inside individual load cells.
   - Show 2-pole and 3-pole loads occupying multiple consecutive circuit positions with continuation rows.
   - Split large retail/community lighting and receptacle loads into multiple circuits such as `Lighting #1`, `Lighting #2`, `Receptacles #1`, `Receptacles #2`, etc.
   - Cross-check panel ratings, transformer secondary capacity, elevator count, service size, and large loads against the latest load letter before issuing.

5. **Create feeder schedules**
   - Include feeder ID, source, destination, rating, OCP/disconnect, conductors, EGC, raceway, and notes.
   - Size preliminary feeders consistently using copper conductors, 75C terminals, EMT, and the applicable NEC/local electrical code edition unless the user directs otherwise.
   - Same-size feeders can share the same feeder symbol/detail, but each destination must remain clearly labeled and scheduled.
   - Cross-check feeder ratings against the riser, panel schedules, and load letter before issuing.

6. **Run riser QA/QC before delivery**
   - Render the riser PDF/SVG/drawio to a visual preview and inspect for overlap, disconnected lines, and floating symbols.
   - Verify every feeder can be traced from source to destination.
   - Verify every disconnect/switch symbol is connected on both ends.
   - Verify physical panels are not duplicated across floors and service room.
   - Verify drawio XML opens in diagrams.net. Escape `<`, `>`, `&`, quotes, and line breaks in XML attributes.
   - If a package includes a drawio file, it must use native editable cells, not a single embedded image background.

7. **Deliver editable outputs**
   - Provide at least one review PDF plus one editable format. Preferred editable formats are SVG and diagrams.net `.drawio`.
   - When the user wants manual fine tuning, package the editable SVG/drawio plus the PDF and feeder table into a ZIP.
   - State clearly what remains preliminary: utility service arrangement, fault current/AIC, selective coordination, voltage drop, final equipment MCA/MOCP, conductor derating, and EOR sign-off.

## Quality checks before final response

- No overlapping text, line labels, feeder tags, boxes, or symbols.
- Feeder lines are continuous and visibly connected.
- Disconnect symbols are connected on both ends and are part of the circuit.
- Parallel loads branch from a source bus or distribution panel, not from each other in series.
- All panel boxes are complete closed shapes.
- All panel ratings match the latest panel schedule and load calculation.
- Remote panels appear only at their physical location; service room/cellar shows feeder disconnects and callouts only.
- Transformer-fed systems show source panel, transformer, secondary MDP/panel, and grounding/bonding notes.
- Feeder schedule is generated and IDs match the riser labels.
- EPR/utility/code notes are included when service size, kVA, voltage, fire pump, transformer, or service room cooling triggers are relevant.

## Bundled resources

- `references/riser-style-guide.md`: style and coordination checklist for riser diagrams, feeder schedules, switch/disconnect symbols, transformers, and panel schedules.
- `references/riser-qc-checklist.md`: pre-issue checklist for overlap, floating connections, drawio XML, and feeder cross-checks.
- `references/lessons-learned-179-22nd-street.md`: practical lessons from the 179 22nd Street sprint, including multi-sheet layout and parallel branch corrections.
- `scripts/build_editable_riser.py`: configurable SVG/drawio generator template for editable multi-sheet riser diagrams and feeder schedules.
- `scripts/riser_qc.py`: lightweight validation helper for drawio/SVG packages.
- `assets/sample_project_config.json`: example project configuration that can be copied and modified for a new building.
