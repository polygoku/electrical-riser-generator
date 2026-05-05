# Lessons learned: 179 22nd Street sprint

This reference captures practical improvements learned while developing the load calculation, panel schedules, feeder schedule, and riser diagram for a dense 12-story mixed-use building.

## Load-calculation lessons

- Verify equipment schedules before overriding plumbing/gas assumptions. A gas riser can coexist with electric apartment water heaters if the mechanical/equipment schedule specifies electric HWH.
- Treat cooking as gas only when drawings or user direction support it. Keep the assumption visible in the load letter.
- Retail/community facility service should be calculated from area, actual fixture lighting, receptacles, equipment allowances, and HVAC rather than carried as a placeholder when enough plan data exists.
- For rooftop units with incomplete schedule data, use schedule BTUH/EER/COP to estimate kW and label the result as preliminary pending final MCA/MOCP/nameplate.
- Re-check elevator count visually. Stretcher-adaptable passenger elevator and service elevator may appear side by side and must both be carried in the load and panel schedules.
- Give large services margin when calculated current is close to the proposed service rating. Moving from 3000A to 4000A can be a practical planning decision, but it may affect EPR/utility review notes.

## Panel-schedule lessons

- Do not stretch schedules to page width when the user wants a presentable engineering schedule. Use compact, centered schedules.
- Show 2-pole and 3-pole loads occupying multiple consecutive circuit spaces with continuation rows.
- Use A/B/C phase columns for 3-phase panels.
- Split large lighting/receptacle loads into multiple labeled circuits: `Lighting #1`, `Lighting #2`, `Receptacles #1`, `Receptacles #2`, etc.
- Retail/community panels usually need more than one lighting and receptacle circuit even at preliminary stage.
- Keep two elevator disconnects/panels separate when plans show two elevators.

## Riser-diagram lessons

- Dense mixed-use projects should usually be split into multiple sheets rather than forced onto one sheet.
- A good split is:
  1. Upper repetitive residential floors.
  2. Lower residential/tenant floors.
  3. Cellar service distribution and large parallel branch loads.
  4. Feeder schedule.
- Every downstream panel/equipment group must be shown as parallel taps from a source bus/distribution panel, not chained in series.
- Use explicit source labels:
  - `RCDP RETAIL / COMMUNITY FACILITY PANELS - PARALLEL`.
  - `HMDP PARALLEL BRANCH LOADS`.
  - `P-M ROOF MECHANICAL LOADS - PARALLEL`.
  - `EDP ELEVATOR LOADS - PARALLEL`.
- Show the fire pump ahead of service disconnecting means when the design basis uses a line-side fire pump tap.
- Label every feeder on the conductor and maintain the same IDs in the feeder schedule.
- Avoid attaching several labels at the same point. Use a dedicated branch bus with vertical drops and repeated spacing.
- Panel boxes should show ratings only and be complete closed rectangles. Put panel names outside or below the box.
- Use matchlines when the riser spans multiple sheets.

## Editable-output lessons

- A `.drawio` output must be natively editable. Do not embed a single SVG or PNG as one background image.
- Native drawio cells should be created for lines, boxes, text, and symbols.
- SVG is still useful for CAD/vector fine-tuning, but drawio is better for non-CAD manual edits.
- Package PDF, editable drawio, SVG sheets, feeder schedule, and source config together in a ZIP.

## EPR / code coordination notes

- Large services can trigger DOB Electrical Plan Review. Include EPR notes when service size/kVA is near or above thresholds.
- Show required EPR information on one-line/riser drawings: service and distribution equipment, overcurrent devices, ampere ratings, interrupting ratings, wire sizes, and service-room cooling notes when applicable.
- Keep fire pump, fire alarm, service tap, utility metering, AIC/SCCR, selective coordination, conductor derating, and voltage-drop notes as preliminary until reviewed by the EOR/AHJ/utility.
