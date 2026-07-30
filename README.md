# Electrical Riser Generator

Reusable ChatGPT Skill for producing coordinated preliminary electrical load calculations, compact panel schedules, feeder schedules, and riser/single-line diagrams for multifamily, mixed-use, retail, restaurant, warehouse, and transformer-fed projects.

## Contents

- `electrical-riser-generator/SKILL.md` - required workflow and QA gates.
- `electrical-riser-generator/references/repeatable-deliverables-standard.md` - controlling production standard.
- `electrical-riser-generator/references/riser-style-guide.md` - drawing and schedule conventions.
- `electrical-riser-generator/references/lessons-learned-179-22nd-street.md` - dense mixed-use lessons.
- `electrical-riser-generator/scripts/validate_project.py` - consistency validator for loads, panels, feeders, transformers, and riser IDs.
- `electrical-riser-generator/scripts/build_native_riser.py` - matching SVG and native editable drawio generator.
- `electrical-riser-generator/scripts/build_editable_riser.py` - legacy multi-sheet generator.
- `electrical-riser-generator/assets/optimized_retail_project_config.json` - coordinated retail example.
- `electrical-riser-generator/assets/sample_project_config.json` - legacy 12-story mixed-use example.

## Optimized workflow

1. Review architectural, mechanical, plumbing/fire-protection, electrical, and lighting plans first.
2. Build a source/assumptions register with one canonical ID per load.
3. Separate service rating, panel rating, feeder/OCP rating, connected load, demand load, and calculated current.
4. Use actual fixture/equipment data before generic branch allowances.
5. Deduplicate owner equipment lists against scheduled mechanical equipment.
6. Generate compact blue-header panel schedules with X-only phase columns and consecutive continuation rows for 2P/3P breakers.
7. Generate a feeder schedule whose IDs match the riser one-to-one.
8. Draw parallel branches from source buses, inline connected fused-disconnect symbols, actual panel locations, and no invented intermediate panels.
9. Label assumed transformers and equipment `ASSUMED - FIELD VERIFY`.
10. Validate the project before issue and visually inspect DOCX/PDF/SVG/drawio outputs.

## Native editable drawio requirement

A valid `.drawio` deliverable contains native editable `mxCell` vertices and edges for every box, line, label, bus, and symbol. A single embedded SVG/image, background image, or XML comment is not an acceptable editable drawing.

Use:

```bash
python electrical-riser-generator/scripts/validate_project.py project.json
python electrical-riser-generator/scripts/build_native_riser.py project.json output/riser
```

## Deliverable package

Unless scope is narrowed, issue:

- Load calculation DOCX/PDF.
- Panel schedules DOCX/PDF.
- Riser plus feeder schedule PDF.
- Native editable `.drawio`.
- Editable SVG.
- Feeder schedule XLSX/CSV.
- Source/assumptions register.
- Full coordinated ZIP.

## Engineering status

This repository supports preliminary engineering assistance. Final utility/service arrangement, conductor sizing, fault current/AIC, SCCR, selective coordination, voltage drop, equipment MCA/MOCP, derating, grounding/bonding, fire-pump requirements, AHJ/DOB/EPR review, and EOR sign-off remain project-specific.
