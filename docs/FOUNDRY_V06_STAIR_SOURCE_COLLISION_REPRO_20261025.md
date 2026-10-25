# Foundry V14 / native 3D Canvas 9.0.36 — stair collision source reproduction
**2026-10-25, read-only independent GLB geometry QA. Status: SOURCE_RISER_REPRO_PASS; native ascent remains FAIL; Manor release NOT CERTIFIED.**

## Scope and immutable evidence
- Existing *disposable library* v06 stair fixture only, **not the current Tresendar Manor staircase**. Exact installed file: `modules/acq-foundry-bridge/assets/blender_bundles/qa-native-door-v05-20261024/qa-native-door-v05-003-stair_connector.glb`.
- Recomputed SHA256 **`734f0c1bff44ce81fcad156c45477d36cdbd09f78e4117b07ec83f46071df81e`** (matches prior source). Parsed GLB v2 JSON/BIN **without importing or editing a Blender scene**. Mesh: 756 indexed vertices, 358 triangles; glTF node `stairs`, scale (0.8,1,1), translation (0,0,-2). Transformed mesh bounds X[-2,2], vertical Y[0,5.1], run Z[-2,2]. Triangle intersection computed using two-sided Möller–Trumbore ray/triangle tests against original POSITION and index accessors. All geometry, UVs and material buffers untouched.
- Historical native blocked fourth move: token document (2720,1410,elev1.24) -> attempted (2720,1310), no motion. Native 3D Canvas BVH independently hit `stairs` mesh at **world (2.77,0.16,1.45375)** face183 and **(2.77,0.20,1.385)** face319, each direct parent-chain Tile `qfbRiIKCFSix8yzP`, semantic `qa:multichunk:qa-native-door-v05:stair_connector`. See [live QA](FOUNDRY_V06_NATIVE_AXIS_ALIGNED_STAIR_QA_20261025.md). The *native* face IDs differ from the GLB's source triangle indexing.

## Independent quantitative reproduction (new in this run)
For the blocked **100px native step**, GLB local forward run is 100px / (1000px/m * 0.075) = **1.333333 source units**. At centerline, tested local GLB Z **0 -> -1.333333**. Native world heights map to source `local_y=(native_y+0.02625)/0.075`; source hit Z maps to `world_z=1.46+0.075*local_z`. These mappings are specific to this v06 Tile placement, not a universal importer rule.

| Native movement-ray height (m) | Source-only first hit (GLB Z) | Reprojected native world Z (m) | Prior actual native BVH hit Z (m) | Result |
|---:|---:|---:|---:|---|
| 0.12 | none | — | none | CLEAR control |
| **0.16** | **-0.083333** | **1.453750** | **1.453750** | **BLOCKED, exact position match** |
| 0.18 | -0.500000 | 1.422500 | not previously sampled | BLOCKED |
| **0.20** | **-1.000000** | **1.385000** | **1.385000** | **BLOCKED, exact position match** |
| 0.22 | -1.000000 | 1.385000 | not previously sampled | BLOCKED |
| 0.24 | none | — | none | CLEAR control |

**Lateral negative controls:** repeat at source X=-0.35, 0, +0.35 produced the same first-hit world Z **1.453750** at ray height0.16 and **1.385000** at ray height0.20; at0.12 and0.24 all three lanes were clear (12/12 expected hit/clear outcomes). This excludes a centerline-only crack. GLB triangle IDs for the two centerline hits are 1 and 350; native Three.js reports 183 and 319. They are not required to agree.

**Actual source tread support envelope:** centerline downward ray at GLB Z=0 first hits source vertical Y=2.0 (world Y=0.12375m). At Z=-0.0952 it rises to Y≈2.4952 (world0.16089m), then Y2.5 across the tread; near Z=-0.5714 it rises to Y≈2.9714 (world0.19661m); near Z=-1.0476 it rises to Y≈3.4476 (world0.23232m), then Y3.5 (world0.23625m). Across the single 100px input the source support climbs **1.5 GLB units = 0.1125m**, crossing **three ~0.0375m native rises**. The installed native `wrappers.js` `TokenLayer.moveMany` performs a **horizontal `computeSightCollision(...,"move")` at the old token3d.losHeight** and separately finds downward destination support. The existing risers intersect that horizontal movement segment at the sampled heights. This establishes a physically specific source/native collision mechanism, not merely a guessed bad Tile flag.

## Interpretation and release gate
**New result:** source-only triangle geometry reproduces **both previously measured native BVH collision coordinates exactly to the reported precision** using the unchanged source GLB and as-placed Tile scale. Strong independent evidence that the *existing v06 fixture's vertical risers* block the installed native 100px horizontal movement ray. This does **not** prove the selected new modular Manor stairs have the same defect, nor does it capture the fourth TokenLayer callback, establish exact native eye height, or certify any corrected fixture.

**Next permitted corrective experiment (SCENE owner):** author a **separately versioned disposable** source-faithful stair profile using existing approved materials, unchanged portal sockets/entry/exit heights and a supported tread/rise envelope; preserve original visible art/master and exact source hashes. Preflight the candidate with the **same source ray sweep** at actual token LOS-height and 100px increments, including lateral lanes, foot support and 25mm displaced negative control. If geometry is accepted, RUNTIME owner imports only the versioned QA asset and repeats genuine camera-axis-aligned native `TokenLayer.moveMany` ascent **and descent**, blocked-wall control, open-door token passage, roof/Levels hide, cold reload, renderer parity, FPS and rollback. Do **not** disable collision on the stair, teleport tokens, patch vendor code or overwrite current Manor art.

## Live-state and ownership check (this run)
- Foundry MCP world: V14.368, D&D5e6.0.5; active player Scene remains `NUEDEFAULTSCENE0`. `scene_get` on inactive QA `3WNB3GURss8vPtua`: **14 Tiles and 1 QA-only token**. Native source Scene capability read-only checksum **`e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f`** before source analysis. Native 3D renderer in GM's source view **inactive**, not claimed tested now; read-only native inspection of inactive QA returned an error, so its document SHA was **not freshly recomputed** in this run.
- Blender MCP live read-only: open historical v107 `.blend` saved/clean; no Blender source edit/import/save. Godot project exists but editor disconnected; no Godot edit. Plugin Creator read installed private AI 3D Asset Workflow **v2.7.70** and native interoperability skill; `skills__list` returned empty, so plugin source was read directly.
- No Foundry Scene/Tile/Token/setting, Manor geometry, Meshy, vendor module, or GM camera/view writes. This report is a **source-only engineering QA artifact** on the isolated Foundry feature branch. Current modular Manor review family and desktop coordinator retain ownership. **NATIVE_PLAYABILITY remains FAIL/UNVERIFIED; DM acceptance pending.**
