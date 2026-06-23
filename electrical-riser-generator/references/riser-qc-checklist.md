# Riser QC checklist

Use this checklist before issuing any electrical riser package.

## Geometry and readability

- No text overlaps another text object, panel box, switch symbol, feeder label, or floor datum line.
- No feeder line terminates in empty space unless intentionally marked `CONTINUED` or `TO/FROM` another sheet.
- Every disconnect/switch symbol is connected on both ends and is part of the feeder circuit, never floating beside the wire.
- Feeder labels are plain text beside the conductor/run; do not place feeder IDs inside panel boxes.
- Panel boxes show ratings only. Names are outside/below boxes.
- Remote panels are drawn only on their serving floors/locations. In the service room/cellar, show feeder disconnects and callouts to remote panels, not duplicate panel boxes.
- Similar feeders use consistent symbol style and label placement.

## Electrical relationship checks

- Downstream loads branch in parallel from the correct source bus/distribution panel; do not connect panels in series.
- Each remote panel can be traced back to its source without ambiguity.
- Transformer-fed systems clearly show primary source, transformer kVA/voltage, secondary distribution, grounding/bonding note, and downstream panels.
- Fire pump is shown ahead of service disconnecting means only when that is the selected design basis.
- Typical panels do not get unnecessary fused disconnect symbols unless the design basis requires them.

## Feeder schedule checks

- Every feeder tag on the riser appears in the feeder schedule.
- Every feeder schedule row appears on the riser or is explicitly marked spare/future/existing.
- Feeder schedule includes source, destination, rating, OCP/disconnect, conductors, EGC, raceway, and notes.
- Same-size typical feeders may share one schedule symbol/detail, but individual destinations remain clearly labeled.

## Editable output checks

- Drawio output opens in diagrams.net without XML errors.
- Drawio output uses native editable cells, not a single embedded image.
- XML attribute values escape `<`, `>`, `&`, quotes, and line breaks correctly.
- SVG/PDF review output visually matches the drawio source.
