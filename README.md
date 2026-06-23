# Electrical Riser Generator

Reusable ChatGPT Skill for generating and revising preliminary DOB-style electrical load calculation narratives, panel schedules, feeder schedules, transformer-fed tenant workflows, and electrical riser/single-line diagrams for multifamily, retail, commercial, and mixed-use buildings.

## Contents

- `electrical-riser-generator/SKILL.md` - skill entrypoint and workflow instructions.
- `electrical-riser-generator/agents/openai.yaml` - ChatGPT UI metadata.
- `electrical-riser-generator/references/riser-style-guide.md` - riser diagram and feeder table style guide.
- `electrical-riser-generator/references/riser-qc-checklist.md` - pre-issue QC checklist for riser geometry, feeder coordination, and editable output checks.
- `electrical-riser-generator/references/lessons-learned-179-22nd-street.md` - lessons from the 179 22nd Street sprint.
- `electrical-riser-generator/scripts/build_editable_riser.py` - SVG/drawio generator template for multi-sheet riser diagrams.
- `electrical-riser-generator/scripts/riser_qc.py` - lightweight SVG/drawio package validation helper.
- `electrical-riser-generator/assets/sample_project_config.json` - sample 12-story mixed-use project configuration.

## Typical use

Use this skill when asked to:

- Review building plans for electrical load calculation inputs.
- Generate electrical load calculation narratives.
- Create panel schedules and feeder tables.
- Produce editable riser/single-line diagrams in SVG or drawio format.
- Keep feeder labels as plain text beside conductors, panel boxes showing ratings only, and mechanical/house/retail/elevator/tenant loads shown in parallel.
- Split dense riser diagrams into multiple sheets to avoid overlap.
- Model transformer-fed tenant work, including existing 480Y/277V source panels feeding step-down transformers and 208Y/120V tenant distribution panels.
- Run pre-issue riser QC for overlaps, floating symbols, duplicated remote panels, feeder schedule cross-checks, and editable drawio XML.

## Lessons learned now captured

The skill captures lessons from the 179 22nd Street, 21-23 W Jamaica Ave / Valley Stream, and 99 Newbridge Road / Starbucks iterations:

- Restore equipment-schedule values when they conflict with assumptions from riser/plumbing context.
- Account for multiple elevators where plans show separate passenger/service elevators.
- Use compact panel schedules with simple `X` marks in A/B/C phase columns and multi-pole continuation rows.
- Avoid serial downstream riser connections; show panels and loads as parallel taps from their source distribution panel.
- Place remote panels only on their serving floor/location; use service-room disconnects and `TO PANEL @ FLOOR` callouts instead of duplicate physical panels.
- Keep disconnect/fused-switch symbols inline and connected on both ends, never floating beside a conductor.
- Keep feeder labels as plain text near feeder/conduit runs; put feeder details in the feeder schedule.
- Support transformer workflows such as existing 480Y/277V panel -> step-down transformer -> 208Y/120V tenant distribution -> P-SB/P-M.
- Show fire pump taps ahead of service disconnecting means when used as the design basis.
- Provide a feeder schedule and editable drawio/SVG outputs with every issued riser package. Drawio output must be valid XML with escaped attribute values and native editable cells, not a single embedded image.

## QC workflow

Before issuing a riser package:

- Render and visually inspect the riser for overlapping labels, boxes, feeder tags, switch symbols, and floor datum conflicts.
- Trace every feeder from source to destination and confirm the feeder schedule IDs match the riser.
- Confirm downstream loads branch in parallel from the correct bus or distribution panel.
- Validate `.drawio` and `.svg` deliverables with `python electrical-riser-generator/scripts/riser_qc.py path/to/file.drawio path/to/file.svg`, then complete a manual visual review using `references/riser-qc-checklist.md`.

## Status

Preliminary engineering-assistance workflow. Final service arrangement, conductor sizing, utility requirements, fault current/AIC, selective coordination, voltage drop, equipment nameplates, AHJ/DOB/EPR review, and EOR sign-off remain project-specific.
