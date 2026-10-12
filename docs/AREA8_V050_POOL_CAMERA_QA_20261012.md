# Area 8 v050 — Pool-edge and hero-camera correction

Date: 2026-10-12

DM observations on the previous assembled room: visible gap between central cesspool and perimeter, and unwanted visible entrance in the hero shot. These are distinct issues: material/waterline interface versus camera composition.

Live Blender saved clean checkpoint: `G:\My Drive\D&D\Foundry Bridge\assets\Area8_Rebuild_v050_PoolRimHeroCorrection.blend`. Actual PNG rendered and visually inspected: https://drive.google.com/file/d/1g6GIbMW4odi4dzI1Ng1CTSRle9Asl_Q7/view .

Edits in a separate checkpoint: existing Meshy pool surface `POOL_SEWAGE_SURFACE_v001` moved from Z=-0.20 m to Z=-0.075 m; object XY scale increased by factor 1.012, giving approximately 15.413x15.411 m total extent, so water reaches slightly under inner walkway edge. Camera `AREA8_HERO_CAM` centered at (0,-9.5,1.72), 34 mm focal length, aimed toward (0,0,1.5). Camera entrance now out of frame. No new visible primitive meshes, GLB source changes, or paid asset tasks.

QA: visually inspected 1200x800 actual Blender PNG. Waterline visually closes previous dark transition, entrance not in hero frame, ceiling and tentacle visible. Numerical watertight topological pool edge and drainage continuity are NOT yet certified. Hanging ceiling pipe still needs a credible sewage stream physically entering pool. Ensure no camera composition hides other architectural defects; maintain independent structural cutaway and source-map checks.

Process lesson: treat source architecture, basin waterline contact and hero composition as separate coupled constraints. For fluid-to-walkway interfaces, test world-space water height, edge radius and surrounding wall top, rather than blaming the floor sector connector. Record changed camera lens and aim and inspect actual PNG before promotion.
