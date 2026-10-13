# Area 9 — Meshy asset production and G3 connector QA failure (2026-10-13)

## Authority
Official `Acq_Inc_Ep1.pdf` Map 1.3 inspected at high resolution: Area 9 is a long irregular north–south cavern with dragon Dabshabah and two darkmantles near north rubble, separate south-middle rubble and narrow southern approach. Earlier rectangular broad-room v001 blueprint was provisional and corrected in live `Area9_G1_MapCorrected_v007.blend`. Skill `ai-3d-asset-workflow` installed v2.7.1. Approved Area8 v082 remains untouched.

## Asset pipeline and actual credits
Meshy-native text-to-image -> actual reference visual inspection -> Meshy 7.1 textured PBR 2K GLB -> Blender source import/QA. Spent **201 credits** total: first cavern-floor reference 3 (rejected for visually constructed masonry); revised natural cavern-floor reference 3; floor GLB 30; brass dragon/darkmantle/rubble/wall refs 4x3=12; four corresponding GLBs 4x30=120; roof reference 3 and roof GLB 30. All GLBs locally saved under `G:\My Drive\D&D\Foundry Bridge\assets`:
- `Area9_NaturalCavernFloor_Meshy71_v001.glb`
- `Area9_NaturalWall_Meshy71_v001.glb`
- `Area9_CavernCeiling_Meshy71_v001.glb`
- `Area9_QuakeRubble_Meshy71_v001.glb`
- `Area9_BrassWyrmling_Meshy71_v001.glb`
- `Area9_Darkmantle_Meshy71_v001.glb`
Plus original texture folders and inspected reference PNG files. Provider accepted charged actions under DM budget approval. Local Drive-folder saves are NOT independent cloud sync proof.

## Floor fixture validated only within sampled test
Isolated floor GLB source 602623 verts, 1.839 x 1.904 x 0.531 m, original untouched. Independent derivative made via planar cuts and edge-height regulation to 1.524m square; preserved 516721 vertices. Two-module grid fixture `Area9_FloorDerivative_v006_TwoGridFixture.blend` physically visually inspected and 15/15 downward BVH ray surface samples near seam valid, max height delta 0.026m. This **is not full-floor certification** or watertight enclosure. Its render is saved locally in captures.

## G3 wall/roof failure and explicit STOP
Two natural wall + roof initial fixture v009 rendered with severe wall floor intrusion; v010 `Area9_EnclosureFixture_v010_PlacementTrial.blend` preserved with corrected wall placement, but roof appeared floating; actual wall top/roof underside samples show ~0.3–0.45m vertical gap. Attempted v011 `Area9_EnclosureFixture_v011_MirroredWallConnectors.blend`: original Meshy wall source copied to independent derivative, bisect side planes at x=±0.762, bmesh.holes_fill over **34,188 boundary edges**, generating **336 fill faces**, 243858 output verts. Actual rendered fixture inspected and showed **wild malformed triangles/shattered surfaces**; this is a catastrophic mesh-interface fabrication failure. v011 saved clean but REJECTED/QUARANTINED, never DM reviewed as usable and never replicate. Last safely preserved pre-failure enclosure file = v010 (itself unverified and not room-ready). No further Blender edits after detecting abnormal geometry, respecting single recovery/STOP policy.

## Next targeted work after incident review
Investigate why hole-filling over all boundary loops corrupted wall topology, distinguish pre-existing source nonmanifold islands from cut cross-sections, isolate actual cut edges only and avoid blanket holes_fill. Verify geometry in isolated single wall before mirroring/placing. For roof-bearing produce genuine measured contact patch and retest 2-wall/roof/floor fixture; **do not proceed to room replication until source-derived structural contact and actual visuals pass**. Then construct long mapped passage and place saved dragon/darkmantle/rubble GLBs with fixed hero and cutaway QA. No Area9 accepted scene, Foundry export or cloud link claim.
