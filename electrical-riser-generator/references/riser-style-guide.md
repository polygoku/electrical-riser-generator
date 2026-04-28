# Riser diagram style guide

## Preferred drawing conventions

- Use floor datum lines from cellar to roof.
- Show one main residential vertical riser and separate common/mechanical/low-voltage risers when needed.
- Use one-line representation for power conductors.
- Label each feeder with `F-#` near the conductor.
- Keep panel boxes simple; ratings inside, names outside.
- Use fused disconnect switch symbols at feed-outs from MDB/RMDP/house/mechanical panels when the diagram requires disconnect/fuse callouts.
- Keep mechanical downstream loads parallel from P-M or the applicable panel.
- Keep house/common downstream loads parallel from P-H or the applicable panel.

## Common panel naming pattern

- `MDB`: main distribution board / main switchboard.
- `RMDP`: residential meter/distribution panel or meter bank.
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

## Engineering caveats to preserve

- Utility service, CT cabinet, meter stack, and service end box are subject to utility review.
- Feeder sizing is preliminary until conductor material, insulation, terminal rating, ambient correction, conductor count, raceway type, voltage drop, SCCR/AIC, and selective coordination are finalized.
- Fire pump overcurrent protection and feeder routing must be finalized per controller nameplate and applicable NEC/NYC Electrical Code requirements.
- Required fire alarm primary power may need line-side arrangement per local code/AHJ.
