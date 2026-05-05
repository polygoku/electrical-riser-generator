# Electrical Riser Generator

Reusable ChatGPT Skill for generating and revising preliminary DOB-style electrical load calculation narratives, panel schedules, feeder schedules, and electrical riser/single-line diagrams for multifamily or mixed-use buildings.

## Contents

- `electrical-riser-generator/SKILL.md` - skill entrypoint and workflow instructions.
- `electrical-riser-generator/agents/openai.yaml` - ChatGPT UI metadata.
- `electrical-riser-generator/references/riser-style-guide.md` - riser diagram and feeder table style guide.
- `electrical-riser-generator/references/lessons-learned-179-22nd-street.md` - lessons from the 179 22nd Street sprint.
- `electrical-riser-generator/scripts/build_editable_riser.py` - SVG/drawio generator template for multi-sheet riser diagrams.
- `electrical-riser-generator/assets/sample_project_config.json` - sample 12-story mixed-use project configuration.

## Typical use

Use this skill when asked to:

- Review building plans for electrical load calculation inputs.
- Generate electrical load calculation narratives.
- Create panel schedules and feeder tables.
- Produce editable riser/single-line diagrams in SVG or drawio format.
- Keep feeder labels on conductors, panel boxes showing ratings only, and mechanical/house/retail/elevator loads shown in parallel.
- Split dense riser diagrams into multiple sheets to avoid overlap.

## Lessons learned now captured

The latest update incorporates lessons from a large 12-story mixed-use project:

- Restore equipment-schedule values when they conflict with assumptions from riser/plumbing context.
- Account for multiple elevators where plans show separate passenger/service elevators.
- Use compact panel schedules with multi-pole continuation rows.
- Avoid serial downstream riser connections; show panels and loads as parallel taps from their source distribution panel.
- Show fire pump taps ahead of service disconnecting means when used as the design basis.
- Provide a feeder schedule and editable drawio/SVG outputs with every issued riser package.

## Status

Preliminary engineering-assistance workflow. Final service arrangement, conductor sizing, utility requirements, fault current/AIC, selective coordination, voltage drop, equipment nameplates, AHJ/DOB/EPR review, and EOR sign-off remain project-specific.
