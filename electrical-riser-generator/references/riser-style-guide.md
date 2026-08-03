# Riser diagram style guide

## Preferred drawing conventions

- Use floor datum lines from cellar to roof.
- Show one main residential vertical riser and separate common/mechanical/low-voltage risers when needed.
- Use one-line representation for power conductors.
- Label each feeder with `F-#` near the conductor.
- Keep panel boxes simple; ratings inside, names outside.
- Use the Eaton/Cutler-Hammer combination symbol when a fused disconnect is required: fuse first, then the open disconnect blade in the direction of power flow. Reference: https://www.newark.com/pdfs/techarticles/eatonCH/ElectricalSymbols.pdf
- Rotate the complete symbol with the feeder direction. Do not mirror or reorder its fuse and switch components.
- Use only the open disconnect-switch portion for a non-fused disconnect. Label the device `FDS`, `SFDS`, `NFD`, or `LDS` so the symbol and feeder schedule agree.
- Place every disconnect inline on its feeder, with visible conductor continuity to both device terminals.
- Keep mechanical downstream loads parallel from P-M or the applicable panel.
- Keep house/common downstream loads parallel from P-H or the applicable panel.
- Keep retail/community facility panels parallel from RCDP or the applicable retail distribution panel.
- Keep elevator loads parallel from EDP or the elevator distribution panel.
- Keep apartment panels parallel from the residential meter stack/riser/floor bus.
- Draw fire pump ahead of service disconnecting means when the selected design basis is a line-side fire pump tap.

## Multi-sheet layout for dense projects

When more than 5-6 floors or more than 30-40 panels create overlap, do not force the riser onto one sheet.

Preferred split:

1. **Sheet 1 - upper floors / repetitive residential**
   - Roof and upper residential levels.
   - Repetitive apartment panels compressed by floor.
   - Roof mechanical loads in parallel if space permits.
2. **Sheet 2 - lower floors / tenant and amenity panels**
   - 1st through 4th floors, retail/community facility, garage, elevators, common panels, and crowded lower floor loads.
3. **Sheet 3 - cellar service distribution**
   - Utility service, service end box, CT/metering, MDB, RMDP, RCDP, HMDP, P-M, EDP, fire pump tap, jockey pump, grounding, and parallel branch loads.
4. **Sheet 4 - feeder schedule**
   - Use if the feeder table is too large for the riser sheets.

Keep feeder numbering continuous across sheets. Add matchline notes such as `CONTINUED ON SHEET 2` for risers that span pages.

## Common panel naming pattern

- `MDB`: main distribution board / main switchboard.
- `RMDP`: residential meter/distribution panel or meter bank.
- `RCDP`: retail/community facility distribution panel.
- `HMDP`: house/main distribution panel.
- `EDP`: elevator distribution panel.
- `AP-1A`, `AP-2A`, etc.: apartment panels.
- `P-L`: laundromat/tenant panel.
- `P-H`: house/common panel.
- `P-M`: mechanical/roof common loads panel.
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
- Drop vertically to the fused disconnect or panel/load box.
- Do not draw feeder lines from one downstream panel to the next.
- For house, mechanical, retail, and elevator groups, label the bus such as `HMDP PARALLEL BRANCH LOADS`, `P-M ROOF MECHANICAL LOADS - PARALLEL`, or `EDP ELEVATOR LOADS - PARALLEL`.
- Place feeder tags at each branch conductor before the disconnect/panel box.
- For vertical branches, orient the fuse and switch vertically in top-to-bottom power-flow order. Do not place a horizontal switch symbol beside a vertical feeder.

## Panel schedule conventions

- Use 3-phase A/B/C columns for 208Y/120V 3-phase panels.
- Use 2-pole and 3-pole continuation rows so multi-pole loads occupy multiple circuit spaces.
- Split larger retail/community loads into multiple circuits: `Lighting #1`, `Lighting #2`, `Receptacles #1`, `Receptacles #2`, etc.
- Keep panel schedules compact and centered when presenting as Word/PDF deliverables.

## Engineering caveats to preserve

- Utility service, CT cabinet, meter stack, service end box, and service-tap arrangement are subject to utility review.
- Feeder sizing is preliminary until conductor material, insulation, terminal rating, ambient correction, conductor count, raceway type, voltage drop, SCCR/AIC, and selective coordination are finalized.
- Fire pump overcurrent protection and feeder routing must be finalized per controller nameplate and applicable NEC/NYC Electrical Code requirements.
- Required fire alarm primary power may need line-side arrangement per local code/AHJ.
- DOB/EPR review may be required for large installations; include a note when service kVA or other triggers are present.
- Show service-room cooling method when the applicable rules require it for large service equipment.
