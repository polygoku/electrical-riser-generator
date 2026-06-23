# Riser diagram style guide

## Preferred drawing conventions

- Use floor datum lines from cellar/service entrance to roof.
- Use one-line representation for multi-conductor feeder paths.
- Place each physical panel only once at its actual location/floor.
- In the service room/cellar, show feeder disconnects and `TO PANEL @ FLOOR` callouts for remote panels. Do not duplicate remote panel boxes there.
- Keep panel boxes simple: rating inside, name outside/below.
- Label each feeder with plain text such as `F-4` beside the conductor/run. Do not put feeder IDs inside panel boxes.
- Keep downstream panels and equipment parallel from their source bus/distribution panel.
- Draw fire pump ahead of service disconnecting means only when the selected design basis is a line-side fire pump tap.

## Switch-fuse / disconnect symbol rules

- Use the project-selected disconnect symbol consistently across the sheet.
- A disconnect symbol must be inline with the circuit and connected on both ends.
- Do not allow a switch/disconnect symbol to float near a feeder without conductor connection.
- Use disconnects selectively. Typical use cases include:
  - Service/distribution feeders.
  - Transformer primary or secondary disconnects where required.
  - Mechanical equipment and major HVAC equipment.
  - Elevator/fire-pump coordination.
  - Panels/equipment with SCCR or manufacturer disconnect requirements.
- Do not show a fused disconnect at every apartment panel, ordinary lighting/receptacle panel, or minor branch unless the design basis requires it.

## Transformer-fed tenant workflow

When a field condition shows an existing 480Y/277V tenant panel feeding 120/208V tenant loads:

1. Show the existing source panel with rating, voltage, phase, and wire count, e.g. `EX-PNL-480 100A, 480Y/277V, 3PH, 4W`.
2. Show primary feeder/OCP/disconnect to transformer.
3. Show transformer tag, kVA, and voltage, e.g. `T-1 75 kVA, 480V primary to 208Y/120V secondary`.
4. Show secondary disconnect/MDP at 208Y/120V.
5. Branch P-SB, P-M, P-H, or other tenant panels in parallel from the secondary distribution.
6. Include grounding/bonding note, transformer ventilation/clearance note, and final EOR/utility/AIC verification note.

## Multi-sheet layout for dense projects

When more than 5-6 floors or more than 30-40 panels create overlap, do not force the riser onto one sheet.

Preferred split:

1. **Sheet 1 - upper floors / repetitive residential**
   - Roof and upper residential levels.
   - Repetitive apartment panels compressed by floor.
   - Roof mechanical loads in parallel if space permits.
2. **Sheet 2 - lower floors / tenant and amenity panels**
   - Lower residential floors, retail/community facility, garage, elevators, common panels, and crowded lower floor loads.
3. **Sheet 3 - cellar/service distribution**
   - Utility service, service end box, CT/metering, MDB, transformers, RMDP, RCDP, HMDP, P-M, EDP, fire pump tap, grounding, and parallel branch loads.
4. **Sheet 4 - feeder schedule**
   - Use if the feeder table is too large for the riser sheets.

Keep feeder numbering continuous across sheets. Add matchline notes such as `CONTINUED ON SHEET 2` for risers that span pages.

## Common panel naming pattern

- `MDB`: main distribution board / main switchboard.
- `MDP`: main distribution panel.
- `RMDP`: residential meter/distribution panel or meter bank.
- `RCDP`: retail/community facility distribution panel.
- `HMDP`: house/main distribution panel.
- `EDP`: elevator distribution panel.
- `P-SB`: Starbucks / retail tenant panel.
- `P-M`: mechanical panel.
- `P-H`: house/common panel.
- `FACP`: fire alarm control panel.
- `FP CTRL`: fire pump controller.

## Feeder table minimum columns

1. ID
2. Source
3. Destination
4. Rating
5. OCP / disconnect
6. Conductors
7. EGC
8. Raceway
9. Notes

## Parallel-branch drawing rules

- Draw a horizontal bus from the source distribution panel.
- Place a filled dot at each branch tap.
- Drop vertically to the disconnect, panel, or load box.
- Do not draw feeder lines from one downstream panel to the next.
- Label the bus, such as `MDP FEEDER BUS`, `P-M MECHANICAL LOADS - PARALLEL`, or `P-SB TENANT LOADS - PARALLEL`.
- Place feeder tags directly next to each branch conductor.

## Panel schedule conventions

- Use 3-phase A/B/C columns for 208Y/120V or 480Y/277V 3-phase panels.
- Use simple `X` marks in the A/B/C phase columns only.
- Use 2-pole and 3-pole continuation rows so multi-pole loads occupy multiple circuit spaces.
- Split larger retail/community loads into multiple circuits: `Lighting #1`, `Lighting #2`, `Receptacles #1`, `Receptacles #2`, etc.
- Keep panel schedules compact and centered when presenting as Word/PDF deliverables.

## Engineering caveats to preserve

- Utility service, CT cabinet, meter stack, service end box, service-tap arrangement, and existing panel capacity are subject to field/utility review.
- Feeder sizing is preliminary until conductor material, insulation, terminal rating, ambient correction, conductor count, raceway type, voltage drop, SCCR/AIC, and selective coordination are finalized.
- Transformer feeder and secondary sizing must be finalized by the EOR using nameplate and code requirements.
- Fire pump overcurrent protection and feeder routing must be finalized per controller nameplate and applicable NEC/local electrical code requirements.
- Required fire alarm primary power may need line-side arrangement per local code/AHJ.
- DOB/EPR or local plan review may be required for large installations; include notes when service kVA or other triggers are present.
