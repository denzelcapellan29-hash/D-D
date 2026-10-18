# Episode 2 High Road — v008 player-eye visual baseline / full-episode skill v2.7.26
Date: 2026-10-17 Eastern. **Real scene write, real render inspected; artistic WORLD-FEEL FAIL. NOT DM accepted, G3 FAIL.**

## Verified Blender scene/checkpoints (all originals preserved)
- Input v006 `G:\\My Drive\\D&D\\Foundry Bridge\\assets\\Episode2_HighRoad_BankPilot_v006.blend` saved clean 167,326,574 bytes at restoration.
- New `Episode2_HighRoad_EpisodeFactory_v007.blend` saved separately/clean, size **167,326,728 bytes**; no new visible geometry; 31 mesh objects.
- New `G:\\My Drive\\D&D\\Foundry Bridge\\assets\\Episode2_HighRoad_VisualBaseline_v008.blend` saved separately/clean, **167,327,289 bytes**, exactly **31 original-derived meshes** (16 genuine road instances, 11 genuine marsh instances, 4 independent road-source wedge-bank derivatives), active camera `EP2_R1_PlayerEye_35mm_QA`. No original GLBs or Area8 accepted v082 modified.
- v008 includes three authored geometry-free QA cameras; coordinates/mode for primary: location approx (X1.524m,Y-0.45m,Z1.70m), 35mm focal length, looking toward positive Y up the road and slight downward. This is a QA design choice, not official source camera.

## Actual locally rendered images (no cloud links claimed)
All rendered from connected Blender 5.2.2 Eevee at 960x540, actual nonblank PNG and visually inspected pixels through Blender preview:
1. `Episode2_HighRoad_v007_PlayerEye_DRAFT.png` **482,257 bytes**. Actual player eye reveals raised tan road with squared-off far edge, repeated dark marsh clumps on one flank, pervasive empty gray background. **WORLD-FEEL FAIL**.
2. `Episode2_HighRoad_v007_Lookback_DRAFT.png` **476,242 bytes**. Actual reverse view reveals exposed rectangular road ends, exposed bank triangles and isolated side clumps over gray void. **WORLD-FEEL FAIL**.
3. `Episode2_HighRoad_v007_Structural_DRAFT.png` **500,424 bytes**. Actual overhead reveals repeated separated clump islands, no ground underneath or connected marsh-land surface. **G1.5 ASSET INSUFFICIENCY FAIL**.
These are local G:\\My Drive Windows paths only, not independently verified cloud files; no user-download links.

## Root cause, gating, and immediately next needed genuine assets
Only **two** unique original Meshy silhouettes (road tile, marsh clump), four wedges are independent derivatives of the same road source, not new terrain family. The missing ground/shore and middle-ground arboreal forms make meaningful world-feel impossible regardless of more seam scans. The road Y overlapping upper surfaces still have recorded max discrepancies up to 32.94mm; keep **G3 FAIL** for Foundry deployment. Do not enlarge fake banks or generate Blender procedural visible terrain. Next provider task is an isolated reference image of a genuine physically grounded ROAD-TO-PEAT LAND module, with measured connector envelope and authentic brown/green wetland texture, followed by source-approved Meshy 7.1 textured PBR 2K GLB; then complement with independent wetland ground/shore and tall dead willow silhouette. Meshy paid generator provider requires explicit action-specific cost confirmation if demanded; user has standing overall permission but not a bypass. Do not claim credits spent here. No playable/DM-accepted export.

## Skill and scope
Private AI 3D Asset Workflow **v2.7.26**, release `pluginrel_6ad442f15abc8191af8c19381d3a63c2`, binding `skills/meshy-asset-pipeline/references/AUTONOMOUS_EPISODE_PRODUCTION_V2726.md`; canonical episode-wide registry `docs/EP2_FULL_EPISODE_SCENE_PRODUCTION_REGISTER_20261017.md` (GitHub commit `3c3280db51222e7ac2ba1d44effd66906ebb9a88`). Different future scenes include later road encounters, Phandalin hub, Tresendar manor, all 12 Map 2.2 keyed underground rooms, and cleanup crew; scene reuse must keep official location/story logic, geometry, secrets and asset lineage.

## Actual meaningful operations in this pass
1. Reversible/versioned save baseline v007; 2. new player-eye camera draft and render/visual QA (FAIL); 3. lookback render and QA (FAIL); 4. structural render and QA (FAIL); 5. v008 saved verified with locked camera state. Not 15–20 iterations. No new third-party GLB generated, no Meshy credits charged. The policy+documentation milestones are separate from construction iteration counts.
