# Electrical Riser Generator

Reusable ChatGPT Skill for generating and revising preliminary DOB-style electrical load calculation narratives, panel schedules, feeder schedules, and electrical riser/single-line diagrams for multifamily or mixed-use buildings.

## Contents

- `electrical-riser-generator/SKILL.md` - skill entrypoint and workflow instructions.
- `electrical-riser-generator/agents/openai.yaml` - ChatGPT UI metadata.
- `electrical-riser-generator/references/riser-style-guide.md` - riser diagram and feeder table style guide.
- `electrical-riser-generator/scripts/build_editable_riser.py` - starter SVG/drawio generator template.
- `electrical-riser-generator/assets/sample_project_config.json` - sample project configuration.

## Typical use

Use this skill when asked to:

- Review building plans for electrical load calculation inputs.
- Generate electrical load calculation narratives.
- Create panel schedules and feeder tables.
- Produce editable riser/single-line diagrams in SVG or drawio format.
- Keep feeder labels on conductors, panel boxes showing ratings only, and mechanical/house loads shown in parallel.

## Status

Preliminary engineering-assistance workflow. Final service arrangement, conductor sizing, utility requirements, fault current/AIC, selective coordination, voltage drop, equipment nameplates, and EOR sign-off remain project-specific.
