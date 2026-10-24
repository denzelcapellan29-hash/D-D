# Tresendar Manor — Area 1 source-aligned Blender checkpoint v107

**Date:** 2026-10-24  
**Scope:** Blender build and visual QA only. Native Foundry VTT + 3D Canvas is the target runtime, with its importer/knowledge-base work maintained separately.  
**State:** SAVED ENGINEERING FIXTURE — **NOT** DM-accepted artwork; source trace and room enclosure incomplete; runtime untested.

## Official source reconciliation

The official Episode 2 Map 2.2 and Area 1 prose place the cellar cistern in the western room and a raised entry on the eastern side, with two stair descents heading **north and south**. Earlier iterations arranged two flights side-by-side on a northern portal. Their technical contact tests are retained, but their source topology is superseded.

The prior roughly 6×4-cell room shell was undersized against a rough map bounding box of approximately 8.33×6.81 five-foot cells (43px nominal grid, itself approximate). v107 therefore uses an **8×7-cell working footprint**. This is a staging choice, **not** a finalized wall/portal trace.

## Saved assets and proof

Under the GM-only local workspace `G:\My Drive\D&D\Foundry Bridge\assets\TresendarManor\Parametric_Resumption_v015`:

- `Tresendar_A1_8x7_Cistern_EastEntry_v107_G1_QA_PENDING.blend` — latest independent scene, approximately 48.8 MB.
- `Tresendar_A1_v107_overhead.png`, `...entry_hero.png`, `...cistern_eye.png` — genuine Blender captures, visually inspected; no cloud links asserted until separate verification.
- `Tresendar_A1_v107_G1_G3_QA.json` — measured contacts, origins, and limits.
- `TRESENDAR_AREA1_G1_SOURCE_CORRECTION_v106_PRIVATE.json` — GM-only source/topology ledger.

## Native structural QA, v107

| Check | Result |
|---|---|
| Parametric visible floor modules copied from archived source | 56 |
| Sampled floor supports | 280 / 280 |
| Adjacent floor XY edge pairs | 97 checked |
| Largest edge residual | 2.384e-7 m |
| North/south stair sample supports | 24 / 24 |
| Optimized original cistern contact to floor | 0.000765 m discrepancy |
| Reversible negative 25 mm support offset | Rejected |

CAD masters and source assets remain immutable on disk; scene copies reuse their existing mesh data. This pass does **not** establish walls, roof, door clearance, character collision, falling mechanics, artistic acceptance, or playability.

## Meshy artwork study and cost

Three paid provider jobs consumed **69 credits total** this continuation: first textured staircase v101 (30), second isolated reference image v102 (9), better-coursed textured source v103 (30).

- v101: imported, actual isolated PBR/UV checks pass, visual appearance too pale and uniform — ART REJECTED.
- v103: genuine 79,256-face dark-masonry-source model, real multiangle render improves block coursing, but scaled whole-wedge tread surfaces fail alignment with exact CAD flight geometry (up to ~0.745 m deviation on one tested bank). Do not put its entire modeled stair body into walkable production.
- v105: exact CAD stair parts reuse v103 source PBR and pass 120/120 contact samples, but actual close-up artwork still needs genuine stone relief and better joint finish — ART NOT ACCEPTED.
- A free image generator again returned an unrelated full-manor progress board instead of isolated prop; rejected and never passed into paid model generation.

## Next build gate

1. Lock source-traced east raised entrance, perimeter wall runs, authentic portal interfaces, and both north/south lower landings on an 8×7-or-corrected room plan.
2. Produce properly measured source-derived individual stone-step/cladding art; compare real player-eye and joint captures against the previously accepted cistern style.
3. Complete the enclosing cellar, west exit, and blocked wall interfaces while preserving source-dependent hidden topology privately.
4. Then construct ruined manor exterior and fit its upper entrance to this stair core.
5. Send optimized GLBs for separate Foundry VTT/3D Canvas work **after** visual and structural gate, not as a substitute.

**Do not confuse SAVED/P1 STRUCTURAL PASS with ART ACCEPTED or FOUNDRY PLAYABLE.** Existing approved Areas 8/10, active Foundry scene, and Godot High Road were not modified.
