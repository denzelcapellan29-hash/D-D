# Three-way pipeline comparison — Foundry 3D Canvas / Dungeon Alchemist / TaleSpire (2026-10-18)

## Authority and user intent
DM requests an evaluation of three competing scene-building environments while continuing the TaleSpire prototype. This is an exploratory recommendation, NOT user acceptance of final runtime. Follow installed AI 3D Asset Workflow v2.7.27 and existing G0-G7 gates, 1.524m grid, original Meshy GLB preservation, independently versioned Blender derivatives, measured connectors, no generated procedural visible geometry, immutable accepted Area8, and frozen Foundry automations.

## Architecture-level conclusion
All three compete in 3D **authoring and visualization**; only TaleSpire and Foundry+3D Canvas are established multiplayer **3D game runtimes**. Dungeon Alchemist is primarily a fast, procedural 3D map creator/visualizer (with internal first-person camera and configurable imported custom models) whose supported VTT export is rendered 2D media and scene metadata, NOT fully editable or playable 3D geometry.

| Requirement | Foundry + 3D Canvas | Dungeon Alchemist | TaleSpire |
|---|---|---|---|
| Room authoring | Custom 3D Tiles/GLBs via live scene API | Excellent fast auto-rooms, lighting, terrain, asset importer | Native 3D kit and slabs |
| Custom Meshy structural assets | Independent optimized GLB Tile supported | GLB, FBX, glTF/STL input supports custom visual props | TaleWeaver Lite officially supports custom creatures; tile/prop structural mods remain planned |
| Programmatic room builder | Rich external Foundry API and existing bridge; presently WebGL failing | No established official scriptable room authoring/export API | Slab format v2 supports Tile/Prop UUID/coordinate packing; GM paste; Symbiote sendSlabToHand puts slab in hand, not persisted edits |
| Full 3D scene export | Scene supported internally; custom mesh files | No official full 3D export; Foundry gets 2D image/movie and walls/lights/doors | Native game board; slab import/export of registered assets |
| RPG operation | Full D&D5e actors/sheets/rolls/combat/vision etc. | Screen-share 3D viewer or export 2D to another VTT; not native multiplayer campaign runtime | Playable multiplayer 3D with less automated D&D5e mechanics |
| Actual current state | Foundry world intact, 3D Canvas spinner/WebGL FAIL | Not found in normal C: Steam app manifest; no local test | Steam build 25937418 installed; two native packs contain 1,760 tiles / 1,529 props, 12/12 local slab codec tests PASS; no in-game paste/visibility QA |

## Independent sources
Dungeon Alchemist official FAQ: https://www.dungeonalchemist.com/faqs
Official custom asset announcement: https://www.dungeonalchemist.com/post/the-treasury-update-is-live
Custom 3D import roadmap marked live: https://roadmap.dungeonalchemist.com/p/import-3d-models
Actual export to Foundry: https://www.dungeonalchemist.com/import-to-foundry
Developer/moderator details on 3D export infeasibility and first-person streaming: https://steamcommunity.com/app/1588530/discussions/0/560260115063827979/ and https://steamcommunity.com/app/1588530/discussions/0/4131557115917858663/
TaleSpire FAQ: https://talespire.com/faq
TaleWeaverLite scope: https://talespire.com/taleweaverlite-guide
Official Slab Format v2: https://github.com/Bouncyrock/DumbSlabStats/blob/master/format.md
Independent Python slab v1/v2 codec: https://github.com/Baldrax/TaleSpire-Encoding-Python
Symbiote sendSlabToHand: https://symbiote-docs.talespire.com/api_doc_v0_1.md.html
Foundry rules engine: https://foundryvtt.com/article/faq/

## TaleSpire P1 prototype independent review
The previously generated conversation artifact exists locally: /mnt/data/talespire_native_slab_pilot_v001.zip, with source code, 3 native Tile UUIDs and 4-piece layout. In this session the test suite was independently rerun: 12/12 tests PASS. Public example slab from the independent library decodes version 2 with 1 layout and 9 placements. Packed 18-bit X/Y/Z, 5-bit 15-degree rotation and little-endian payload matched Bouncyrock format and the independent Python reference code.
Limitations: no external library executable cross-implementation test, no TaleSpire renderer/collision/board paste QA, custom Meshy architecture still unsupported via official TaleWeaver Lite. The validator relies on conservative rotated AABBs rather than measured connector contact; in-game tile pivot and rotational alignment require calibration. Do NOT call this fixture playable or visually accepted.

## Recommended next stage
1. Continue TaleSpire P1 with disposable board: paste four Tile/Prop fixture, check actual 3D image, pose, floor-wall contacts, move/navigate, saving/reopening; require both numerical and real screenshot QA.
2. Test approved Meshy-derived miniature with Blender FBX into official TaleWeaver Lite (P2) only once Unity/TWL setup exists and original files backed up.
3. Do not promise full custom Meshy-built structural rooms in TaleSpire until imported structural tile/prop asset UUID is confirmed (P3), or DM explicitly approves native-kit visual compromises.
4. Maintain Dungeon Alchemist as optional 2D map speed/reference art solution, not a lossless interchange path between Blender and TaleSpire. Its imported assets cannot be assumed extractable/redistributable after composition.
5. Retain Foundry, existing Bridge and backups for 2D D&D tooling/conditional 3D future after a separate actual renderer fix; no continuing scene mutations while broken.
6. Benchmark 3-4 hour two-PC play stability and D&D5e GM operational burden before final platform selection.

Decision status: PROVISIONAL TaleSpire runtime trial; no new DM acceptance, no Meshy charges, app install or scene writes. This comparison extends the SAME semantic model and existing skill, not another duplicate authoring pipeline.
