# Tresendar Manor Area 1 — G0/G1 stair-source correction and bounded construction trials (2026-10-23)

Status: **ENGINEERING SAVED; ART, NATIVE PLAYABILITY, AND DM ACCEPTANCE BLOCKED**. Platform: Foundry V14 + native 3D Canvas, not Godot. Private GM details remain in the private Google Drive build ledger, not here.

## Binding source reconciliation

Read both the complete official *Acquisitions Incorporated* Episode 2 Area 1 description and **Map 2.2** (5-ft grid) together. The text describes double stairs descending **north and south** from the entrance. The map shows stair graphics in **two lanes on both the north and south banks** of the east stair wing. Prior v077 end-to-end geometry and v081–v083 parallel **one-bank-only** geometry are not sufficient source-faithful room layouts despite correct individual risers.

G0 mapping MUST inspect all stair symbols and narrative flow at the **same time**. G1 should represent four routed flights (NW, NE, SW, SE), a central east-facing entry landing, and their lower foot transitions. Published source gives **approximately 10 ft of descent**, not a literal number of treads. 16 risers of 0.1905 m and 0.3048-m treads were an **engineering proposal**, not an authorial fact.

The published drawing is schematic. Do not silently treat a ~50-pixel printed stair symbol as an exact architectural stair flight. Compare model envelope/route to the grid and report any deliberate dimensional adaptation. A source-map pixel estimate on the current archived crop implies an east stair wing nominal N–S length roughly 8.8 m, **manually estimated and not exact**. The original 16-tread 4-flight assembly spans 15.85 m; it is too long to claim matching map proportions.

## Numbered reversible results

| Checkpoint | Result | Classification |
|---|---|---|
| v086/v087 | Valid isolated 16-step Blender reference and enforced release gate (self-test exit 0, actual release exit 3). No credits charged | SAVED, blocked |
| v088 | Three matched PBR transfers from source-approved existing Area8 floor, Area10 limestone wall, and roof. All retained accurate stairs but failed source art quality | REJECTED art |
| v089 | Four independent *source-linked* 16-riser flights, NW/NE/SW/SE. Exact upper/lower mating, 3.048-m lateral center pitch, 1.524-m aisle. Deliberate +30mm landing gap detected | P1 test PASS, art/room not ready |
| v090 | Connected entrance-head landing with 4 new **linked copies** of existing 1.524-m square CAD landing meshes; 8/8 support sample hits, no vertical variance, negative 30mm control | P1 test PASS, not a room |
| v091 | Lower exit floor patches: 4 source-linked floor panels at north/south stair feet; 8/8 supports, six adjoining seam pairs (max axial gap <0.000001 m, elevation <0.000001 m), negative 25mm seam control | G3 floor fixture PASS, not a room |
| v092 | Tested actual 2K PBR stone material from the approved cistern on original stair geometry using original-UV vs axis-projected UV. Both look too much like uniform rectangular stone blocks; art not approved | REJECTED art |
| v093 | Bounded world-Y transform factor 0.65 (original master immutable). Stair lateral geometry and landing contacts remain coherent. N–S overall length 10.302 m, tread run 0.19812 m, riser 0.1905 m, ~43.88° stair angle. This is **~1.51m longer** than the hand-estimated source envelope; native movement unknown. | Experimental P1 PASS, NOT G1/art/runtime accepted |

Do not promote any of these numeric successes as true environmental art or as Foundry collision/navigation QA. G0/G1 still requires authoritative scale reconciliation, upper exterior connection and doorway route. The approved cistern remains a separate good visual source. Main cellar west door and accessible branches still require full route assembly. Existing accepted Area8, Area10, and High Road sources are unchanged; original player GM Foundry Scene untouched. Meshy credits spent this milestone: **0**.

## Next gated work

1. Calibrate the existing source map by labelled squares and plan elevation; choose the shortest actually walkable stair family consistent with source intention (no silent impossible treads).
2. Fit just **one north/south pair + a real west cellar interface** before room-wide expansion; test exact landing/door/no-wall-crossing.
3. Commission approved realistic chipped limestone stair artwork or use a proven source-derived projection/bake with actual art QA; generic 3D Canvas stylized stair GLBs failed earlier tests.
4. Only after player-eye, overhead, reverse, dark/illuminated visual QA and structural contacts pass: native Foundry + 3D Canvas GM-only QA import; preserve and restore source Scene and camera, test collision and Falling separately. DM alone accepts art.

Private construction ledger: https://docs.google.com/document/d/1bRmOPONvqp95-cYztfk058xXY47BgYAnQOjX9s7-i28/edit
