# AI 3D Asset Workflow v2.7.61 — art-first production responsibilities (2026-10-24)

**Status:** PRIVATE PLUGIN SKILL UPDATED and source readback VERIFIED. This note is coordination guidance, not visual QA or a Manor/Foundry release. Latest explicit DM decision controls.

## Workstream separation
- **Art/Skill chat** owns artistic acceptance method, style-coherence examples, comparative visual audit rules, and updates to the private AI 3D Asset Workflow plugin. Does not edit active Manor .blend/GLBs or Foundry import/runtime code.
- **Manor build chat** owns all Tresendar Blender scene construction, approved asset intake, art fixtures, renders, source-map relationships and persistent scene checkpoints. Read and apply art skill at the next safe edit boundary; retain previously working structural connectors.
- **Foundry integration chat** owns GLB/manifest reconstruction, native 3D Canvas and Foundry playability, FPS, lighting parity, performance, and safe QA Scene rollback. Does not overwrite Manor source or the art skill.

Shared rule: one mutable artifact has one owner; only the DM accepts final art. Do not pre-empt ongoing jobs in either chat, and do not confuse saved architecture with accepted art/playable runtime.

## Published skill
- Private plugin: https://chatgpt.com/plugins/plugins_6ac99807af3c81918a869eb5e2710a6b
- Version **2.7.61**; release `pluginrel_6add0112c46c8191ae224e7952d34c31`; source readback confirmed changed manifests, new `skills/art-direction-and-scene-qa/SKILL.md`, and updated `skills/player-route-first/SKILL.md`. All 91 files remain accessible in inventory; preexisting engine and Meshy skills retained.
- Artistic gate sequence: source-locked one-page art brief (AR0) -> small style-coherent material/relief fixture **before** mass duplication (AR1) -> authentic same-revision player-eye/exit/reverse/overhead and structural capture (AR2) -> top-three player-visible defect queue with causal A/B treatment, keep/reject and no tint thrashing (AR3).
- Required art predicates: place recognition, stylistic material coherence, believable world completion/no void, antirepetition/UV, motivated lighting/physical relief, causal aging/dressing, player-view continuity, Foundry material parity. Log PASS/FAIL/UNVERIFIED with real screenshot references. Engineering G3/P1, asset provenance, paid Meshy approval, runtime and source constraints continue as separate hard gates.
- Current explicit target: **Blender scene master -> Foundry VTT + native 3D Canvas primary 3D play**. Godot remains exploratory.

## Verified evidence prompting the update
Latest private Tresendar engineering v111/v112 improved real wall, floor, ceiling and Area1–Area2 connectivity. Independent scene-art trials v114 (pale repeated stone), v115 (shader tint), v116 (pastel low-poly props), v117 (cave-looking stone for a constructed cellar) were visually rejected, while structural v112 remained saved. Preserve source-v107 and v112 checkpoints; do not interpret an art-failed test as structural regression.

Visual evidence and GM-only build record:
https://docs.google.com/document/d/1EyA1b45f_JgIyzV-fBZHfR9b55znV8Et5cuFmNbzBqk/edit
Area8 v082 artistic benchmark:
https://drive.google.com/file/d/1OBJJchJMTV4BtGjtc1SWeI6uH4IRUbFA/view

## Next steps and stop conditions
Manor chat: at next safe fixture, test source-compatible dressed-cellar masonry/floor/roof together at eye height before any repeated installation. Continue architecture independently. Foundry chat: complete its importer/runtime release gates and report Blender-vs-native art discrepancies back to Manor. Art/Skill chat: review actual benchmark and fixture evidence, only generalize lessons after demonstrated results, then issue a new conflict-guarded plugin release if warranted.

No Blender, Meshy, Foundry or Godot writes, provider credit spends, nor original source modifications were performed by this art/skill update. This is not DM visual acceptance.
