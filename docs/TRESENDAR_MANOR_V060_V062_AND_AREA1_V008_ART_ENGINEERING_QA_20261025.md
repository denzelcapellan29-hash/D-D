# Tresendar Manor art-and-engineering continuation — 2026-10-25
**Workstream:** DM-authorized Manor rebuild performed from this chat. **Runtime:** Foundry VTT V14 native 3D Canvas; Godot experimental only. **Credits:** 0 Meshy task credits this pass. **Not DM art accepted / not native-certified.**

## Key outcomes
The Blender connector is online again, but the visible GUI is still the clean, older v107 build. All work was done in independent Blender 5.2 background processes against the latest saved source derivatives, never overwriting GUI v107, v055, v058, v006, original source GLBs, or previously accepted Areas 8/10.

### Exterior v060–v061 rejected visual direction
From v058 (SHA256 `7fe845704759250e4cbddf8f1e6ec0db089eab4a703d099b9c0a7875e85bfcea`), generated and saved reversible four-segment connected L masonry over exact hidden CAD supports; nine stone fragments from separately copied/decimated original Meshy wall source; two reused timber pieces from existing library. All four CAD supports had 0 contact gap to Z0.315m ground, +25mm displaced-negative control detected. v060 initial timber world offset found and corrected in v061 (`0a81d7ab4a70cecb3e64fdd63c4350ebca2d11be7b1b49ca76dc3540d7c77e16`). Five actual Cycles view captures revealed strong upright Meshy masonry but unacceptable artistic assembly: uniform stepped panel top, unnaturally spiky/splinter-like fallen blocks when source mesh decimated/rotated, and incomplete larger manor silhouette. **Do NOT PROMOTE v060/v061.** Real visual evidence:
- https://drive.google.com/file/d/1roeqHFXBwL1PbCdt_qQXwp37BS6nxEq3/view (approach)
- https://drive.google.com/file/d/1Em3AeHjavjpAy5Ft1ThJCljahA9btbbv/view (close-up)
- https://drive.google.com/file/d/1Xd0FT3_E7M6eRRNE1dWf0YuWk4In4NlH/view (reverse)
- https://drive.google.com/file/d/1jWe__d9onbtKj__8OIT78MXIHtT91-cZ/view (overhead).
MCP scene test of applying an irregular Boolean INTERSECT cutter to the source Meshy panel also produced 25,059 non-manifold edges and 23,991 boundary edges due highly fragmented source geometry; rejected unsaved. The Meshy wall must NOT be treated as a watertight rubble master. Two failed collapse strategies trigger asset-method pivot, not further tint, scaling or mass replication.

### Free installed 3D Canvas source inspection and UV/material negative control
Read-only actual Foundry module catalog identified `canvas3dcompendium/assets/Tiles/Modular%20Ruins/Wall_Broken.glb`, `Wall_Double_Broken.glb`, `Wall_ArchRound_Broken.glb`, Kenney `debris.glb`, and CreativeTrio damaged boards. Files exist in local Foundry `C:\Users\denze\AppData\Local\FoundryVTT\Data\modules\canvas3dcompendium\assets\...`. Tested in isolated temporary Blender factory startup with five actual Cycles renders, NOT imported into a production Manor scene. Wall_Broken 976 triangles and Wall_Double_Broken 856 triangles, both stylized flat block geometry, insufficient match against volumetric Meshy rough-coursed stone. Tried world-space BOX stone PBR projection using CC0 ambientCG-style `Materials/Rock002` bundled textures: visuals developed obvious directional streaks and still lacked high-relief carving. That shading would also require texture baking for portable glTF. **REJECT ART; no binary redistributed or baked into project.** Official pack wiki confirms 3D tile models CC0, while certain other asset folders are not; source attribution https://wiki.theripper93.com/levels-3d-preview/canvas3dcompendium . Pilot images:
- https://drive.google.com/file/d/1rqxERpRUhBv6c91V-CXpu7hMFT_RAEVT/view (original broken wall)
- https://drive.google.com/file/d/1vCFDp_IdYtbX33swC_R3Dd6XeQq0HHYr/view (box-reskin test)
- https://drive.google.com/file/d/1ca-3D7-m5qKkBefFMaoYvlZviHX5mklY/view (double broken reskin).
No suitable prior existing paid Meshy rubble task was found through recent task list; previously rejected Area9 QuakeRubble not reinstated. A genuine dedicated rubble/ruin sculpture will require new source role plus priced Meshy task authorization, or an independently inspected high-quality verified library mesh.

### New v062 EXTERIOR ground-source derivative — SAVED, STRUCTURE PASS, ART WORLD STILL PARTIAL
**File**: https://drive.google.com/file/d/1j607dsPP45kTGCtKlSfSQCD5adUqeRWJ/view
SHA256 `3acd074595fc63e68bf37208c3dc802b79977f9042ba33f39fec97b4aa111036`, 127,840,691 bytes.
Opened v058 saved-clean source and copied only the existing courtyard mesh `EXT054_RETAINED_COBBLE_SOURCE_DERIVED_REAL_PORTAL_CUT`, not a new invented surface. Subdivided its 26 original polygons to 23,104 polygons / 11,552 vertices; varied off-plateau elevation from -1.3866m to +0.0123m according to a low-frequency hillside ring, `DESIGN_CHOICE` because no detailed outdoor contour map in official book. Protected original courtyard and surviving building foundation region and approach/stair opening. 0 non-manifold edges / 0 boundary edges after evaluated mesh regeneration; 11 BVH world-space downward tests verify **no ground over center entrance or either stair**, **unchanged Z 0.315m beneath and near both wooden buildings, at route and next to entrance**. Original 198 protected CAD/Area1 objects unchanged. Independent readback of ALL 392 original v058 scene objects showed only terrain mesh datablock/face/vertex counts changed. v058 SHA preserved.
Proof https://drive.google.com/file/d/1lBx8j5fKzZewtvtDNmC5Ok4ZDOOHz4m4/view and https://drive.google.com/file/d/11SpI6ylv8LDjuktPz26bgRM8T_FTi36p/view .
Actual Cycles captures:
- https://drive.google.com/file/d/1NixVxD15CB6naQGq9RAN-Pu9mD12Q0fW/view (approach)
- https://drive.google.com/file/d/1rumRtcAuB7wKI_L1Z996Kadx2q3GEzHK/view (south hillside)
- https://drive.google.com/file/d/1YS36wspy19gdfGpaNpfom50O55g2Uh1t/view (north hillside)
- https://drive.google.com/file/d/1eklxkxAOlIxp9UmFUpjwXWYhxUdEeAF3/view (overhead).
Actual player-eye ART review: gentle sculpted relief exists and source ground/manifold is sound, but resulting hilltop still reads too flat/barren, with open gray horizons and skeletal timber shells. **Do not mark exterior ART PASS or scale.** Keep v062 as terrain candidate and v058 as coherent general fallback.

### New Area1 v008 — successful *limited* lintel art repair
**File**: https://drive.google.com/file/d/1tzxM5nPFMvlOi6OZhEK3air9DJSlYILA/view
SHA256 `f22154f17d77201e9d8c8cd1df0d36fe8aa22ce43bc57e840294187456247b32`, 121,865,010 bytes.
Opened independently saved A1/A2 v006 (SHA256 `c2c8b620645af7c9c8822f0f5fdbf27b6f6db76f5b3abc886726770393edc8fa`). Created one new named visual-only Meshy floor-source geometry instance (79,688 actual polygons and original UV/PBR), turned to face downward to fill v006 original cropped-scene stone lintel's visibly hollow underside. Actual visual bounding cage x[-6.326,-6.096] y[2.438,3.658] z[-0.848,-0.778], full source stone relief not gray CAD reskin. Exact visual fit max drift 0.0000003m; no penetration into doorway. Original **2.200m doorway clearance** preserved; deliberate art move down 25mm would reduce to **2.175m**, correctly caught by negative gate. Independent saved-file readback: **all 271 original objects retained, all their mesh names, faces, materials and transforms unchanged; v008 adds one visual object**. Original v006 .blend untouched, no source Meshy GLB edited.
Three matched real Blender renders:
- https://drive.google.com/file/d/1LAqTPc8AG0viS0sEfpvhqopeVPXCMkz2/view (underside)
- https://drive.google.com/file/d/1tyDzzMjaTAC9KVa9E1KmXeNm6Rxdzh-A/view (eye/approach)
- https://drive.google.com/file/d/1eOTsz322HH6bwrC0jNomkclXLzJeT2hA/view (reverse).
Visible underside is now credible sculpted stone rather than open cut, with UV/PBR intact. HOWEVER unfinished gray walls/ceiling beyond the door remain visible and the full Area1 world gate has NOT passed; no DM art acceptance yet. Do not promote full Area1 acceptance from a single improved lintel.

## Next concrete production work
1. Protect v055 entrance and v058/v062 outdoor source and v008 Area1 lintel derivative. **No more Meshy-decimated wall-as-rubble** or flat CC0 wall tiles as hero art.
2. Obtain an appropriately source-faithful *actual collapsed masonry / debris / broken roof* art family via verified high-quality library or isolated four-view reference and new priced Meshy task (DM per-task approval required). Must possess jagged horizontal and vertical contact, built rather than cave form, grounded debris, material match to accepted wall and burnt timber. Test one actual assembled CAD/decorated fixture, not mass replication.
3. Separate high priority Area1 continuation: make visible wall/ceiling/threshold beyond the doorway match v008 coherent stone family; inspect low-angle/header/reverse and native 3D Canvas with preserved CAD.
4. Native Foundry V14 3D Canvas materials, import and actual walkability remain UNVERIFIED; defer promotion. DM alone accepts art.
