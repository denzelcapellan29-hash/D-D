# TaleSpire native pilot v002, hero-asset audit and cross-runtime boundary (2026-10-18 ET)

## Updated DM priorities
DM confirms a 3D experience, high automation, stability and efficient prep. Native TaleSpire tile family is allowed for routine architecture; custom genuine Meshy set-pieces remain important (trapped dragon under boulder, otherworldly tentacle). First-person view is nice-to-have, **not hard**. Continue TaleSpire P1. DM suspects TaleSpire→Foundry 3D interchange; evaluate but do not compromise provenance/licensing. Existing approved Area8 artwork, source GLBs and Blender checkpoints no-touch; both autonomous Foundry build tasks disabled.

## Installed skill / authority
Use installed AI 3D Asset Workflow v2.7.27, preserve G0/source → G1 metric 1.524m blueprint and socket interfaces → Meshy authentic approved assets → versioned Blender derivative + UV/PBR/LOD QA → platform adapter → actual renderer G3/G5/G6 QA. TaleSpire is the current runtime pilot, not yet DM-accepted as final. No duplicate Blender and VTT scene construction. User-approved ordinary tiles can use native game registry for gameplay; genuine custom Meshy signature mini uses TaleWeaver Lite official *creature* route, not a custom structural tile.

## P1 slab compiler v002 test evidence
Read and executed prior local conversation artifact under /mnt/data/talespire_native_pilot; 12/12 regression PASS; regenerated FOUR registered asset placements (2x2 + 1x1 floor, two half-walls), 95-byte compressed slab, 3 UUID kinds. Introduced a new check in independent v002 ZIP `/mnt/data/talespire_native_slab_pilot_v002.zip`:
- Native **tiles** may rotate only by 90 degrees (yaw steps 0,6,12,18); native **props** may use 15-degree increments. Published slab v2 encoding has generic 24-step angle, but runtime asset type imposes distinct user-facing constraints. TaleSpire FAQ: https://talespire.com/faq
- Added two negative/positive tests; now **14/14 PASS**, regenerated original 4-piece slab, binary packing unchanged, no in-game QA yet.
- v002 ZIP SHA-256 `d767ef69ed7f4796aa11caa074bf9e7b161bde54b5c68803fa662a5557959ab5`.
- Original format basis: https://github.com/Bouncyrock/DumbSlabStats/blob/master/format.md and independent published Python sample: https://github.com/Baldrax/TaleSpire-Encoding-Python
- v002 artifact contains script, registry of verified installed TaleSpire asset UUIDs, sample room JSON, sample slab text, structural AABB-only check and test suite. Any apparent connector alignment is NOT certified by format test.

Local Windows staged handoff (SHA-verified text files; NOT cloud sync): `C:\Users\denze\Documents\AcqTaleSpireQA\P1_NativeSlab_20261018\four_piece_native_pilot.slab.txt`; README in same folder. Slab ASCII text SHA-256 `1f0992595d52eb4821c3ce77d502d18b9fae418729c926714cc4ae26fa72fc48`.

## Game runtime attempt (single attempted launch, no board changes)
- TaleSpire installed, Steam app 720620 buildid 25937418; launched through Steam -applaunch, game pid 41532 obtained, backend connection reaches ConnectionNormal (log contained session cookie; DO NOT copy secrets).
- Live screen verified actual TaleSpire early-access animated **opening/menu screen**, not a campaign board; game responded; keyboard ESC/menu click and Alt+Enter layout test did not advance to a real board. STOP further unsolicited UI interaction. No campaign created, no board/sandbox modified and no 3D piece placed. **TaleSpire P1 in-game render, coordinate and save/reopen tests UNVERIFIED**.
- Required DM step when at computer: in TaleSpire create/open a disposable empty QA campaign/board named `Acq QA Native Slab P1`, then notify ChatGPT it is open. We can use saved slab file or copy one-line code, paste into GM's hand, click once to place, and take actual screenshots. Do not use live campaign boards.
- The single local test folder is ready for that step; game may already be open at menu.

## Genuine signature asset P2 (no paid work or geometry edits)
Read-only independently inspected existing approved Area8 optimized tentacle GLB at local Foundry Data `assets/acq-inc/Area8_v082_Tentacle_Foundry_90pctFaces_1K_OriginZero.glb`:
- source derivative GLB valid v2, SHA-256 `f7e795d547fd907d5a95f5c51f3a65167bd7ddb4d9897b7b93ae617d84b6a6e3`, 9,323,008 bytes, 1 mesh/material, 3 embedded images, 190,669 vertices, 237,335 triangles.
- TaleWeaver Lite creature limit **60,000 vertices** per official guide https://talespire.com/taleweaverlite-guide; a further independently numbered derivative/decimation+normal+PBR re-pack test will be required, not an in-place original edit. The bespoke tentacle can be studied as a large creature miniature with default scale, but not automatically treated as watertight collision floor/prop. Unity Hub 2021.3.45f2 + TaleWeaver Lite install/activation has NOT yet been verified, so no .tsMod acceptance.
- Ordinary architecture native tiles, genuine Meshy distinctive creatures/set-pieces under P2; special interactions and structural composites independently require QA.

## TaleSpire → Foundry GLB EXPORT evaluation and legal boundary
Found active third-party MIT **code** project https://github.com/Canonheim/TaleSpire-Slab-Exporter-to-GLB-and-OBJ, which claims read-only TaleSpire cached board sectors and local copyrighted native Tile/Prop meshes/textures, exports GLB/OBJ via UnityPy; Light/Exact/Merged modes and Blender simplification. Explicitly excludes creatures/minis, fog/hide volumes, water, effects and GM markers, and loses normal/metallic maps. This is NOT a complete reauthorable game scene or route for our custom monster minis. Official Bouncyrock does not support full 3D board export or top-down map export. Bouncyrock EULA https://store.steampowered.com/eula/720620_eula_0 §5 restricts copying, reverse engineering, derivatives and reuse of TaleSpire asset content except authorized cases. Third-party exporter README itself acknowledges TaleSpire content rights separate from its MIT code. A previous community 3D export author reports developers declined tutorial publication on EULA grounds. Thus do NOT install/run native asset extractor or stage/share extracted assets in Foundry absent explicit rights clarification. Keep canonical semantic layout + personally owned Meshy GLBs as cross-runtime authoritative exporter data. This is a product/legal risk assessment, not definitive legal advice.

## Acceptance gate next
P1: User opens NEW disposable empty TaleSpire board, paste v002 sample, check 4 native parts/visual texture/horizontal seams/y=.5 wall bearings/camera/model errors, record real in-game screenshot, save/reopen. Until then only binary/schema 14/14 PASS.
P2: Once P1 works, independently optimize real approved tentacle under 60k vertices on versioned derivative, compare multiangle QA and converted three PBR textures, install official Unity+TWL after explicit install/action and compile .tsMod creature; in-game actual test before art acceptance.
P3: build a source-grounded room that uses native architecture plus Meshy signature hero asset, not 100% custom structure. Programmatic source→semantic→native slab for architecture, then manual creature placement until native creature position interface proven. Validate collision, navigation, fog/GM secrets and 3–4h play.

No Meshy credits, Foundry/Blender project edits, installed TaleSpire modifications, or scene/gameplay changes in this checkpoint.
