# Area 8 Foundry 3D Canvas — visual review candidate (2026-10-16)

**State:** Real renderer visual review candidate, NOT DM accepted and NOT certified playable. This supersedes failed Tile-loader pilot states for choosing the latest working checkpoint. Existing active default Foundry scene is reused; no new scene has been created.

## Independently verified runtime
- World `acquisitions-incorporated`, Foundry v14.368, dnd5e v6.0.5, 3D Canvas; active Scene `NUEDEFAULTSCENE0` (Foundry Virtual Tabletop).
- Scene revision `dc5788296198a1c5c065e1eacef1052ba126d7bc2f85944a8900953281891bb0`.
- Strict live `validate_scene_manifest` PASS with **161 authored source-derived 3D Tiles, 1 authored AmbientLight** (162 semantic IDs total), `allow_unexpected:false`, no missing/unexpected IDs, no count mismatches. Five older non-semantic default ambient lights remain. Eight temporary Kenney/library and solitary control Tiles deleted by exact semantic ID and readback verified.
- Real Three.js renderer images at 1920×992, camera restoration enabled, visually inspected as coherent enclosed circular sewer pool chamber, green pool/tentacle, two flanking waste discharges ending in pool, perimeter walking stone, masonry wall/roof, green interior light; no branded red tabletop.
- **Hero capture (239,850 bytes, SHA256 7ef29f6a8d79b4ffe78d47cddcd3c03e4c65c746f4c32affa5bc30453933f4e8):** https://drive.google.com/file/d/1zcxK4UO6WwmuE4rTPVF_bDl45-IQlD11/view
- **Structural/close capture (227,388 bytes, SHA256 879fea130ce71e45a779eca3248acdb4856be517fb492c3e325bb280bb5699fa):** https://drive.google.com/file/d/1EhFbVNQcNMv1DnXSNnf0IdYTRSSqM962/view
- Both captures were saved from first-party bridge result image bytes and **independently located by exact name/size in Google Drive**, folder D&D/Foundry Bridge/captures.
- DM-ACCEPTED ORIGINAL BLENDER SOURCE `G:\My Drive\D&D\Foundry Bridge\assets\Area8_Rebuild_v082_SicklySewerFinal.blend` saved clean, unchanged. Area 9 frozen.

## Actual construction
- 144 optimized traceable Area 8 Meshy-derived wall Tiles: 36 sectors × 4 courses, azimuth step 10°, `x=round(1920-800sin(theta))`, `y=round(960-800cos(theta))`, `rotation=(360-10n)%360`, width141 height20 depth58; course `elevation=[0,0.58,1.16,1.74]`, runtime vertical course 0.058 world units, last wall-top y0.232. Original asset GLB isolated, Decimate 0.25/1K textures on temporary copies, origin zero.
- 12 traceable Area 8 `RADIAL_CONNECTOR` annular-floor sectors at 30° steps, centers `(1920-685.8sin(theta),960-685.8cos(theta))`, width413 height248 depth13. Final renderer captures show the stone perimeter walkway surrounding the green pool, with all earlier Kenney floor fixtures removed.
- One separately optimized derived cesspool surface, one approved curling planar tentacle, two genuine dedicated sewage discharge pipe assets placed to flank the hero composition, one optimized roof with elevation2.32 whose Tile world y0.232 matches final masonry course upper bound. Physical join/collision beyond controlled Tile bounds remains unverified.
- Green AmbientLight semantic `area8:lighting:sewer-green-key` with color `#97c870`, final alpha0.47 luminosity0.52, x1810 y975 elevation1.75. Environment EXR moonless_golf_1k, renderTable:false, renderBackground:false, ambientLightIntensity0.24, sunIntensity0.12, exposure0.9.
- Hero camera `(2.44,0.135,1.15)` targeting `(1.92,0.09,0.96)`; alternate close structural camera `(1.92,0.215,0.44)` targeting `(1.92,0.015,0.96)`.
- The pipe left/right position is a disclosed artistic framing correction compared with original Blender positions; no source text rewritten.

## Binding reproducible workflow
The user's PRIVATE installed plugin `ai-3d-asset-workflow` was successfully updated and independently read back as **v2.7.17**, release `pluginrel_6ad23d6c029c8191a89e1c93fdf3c0f6`. Read `skills/meshy-asset-pipeline/references/FOUNDRY_TILE_PRODUCTION_V2716.md` and `references/FOUNDRY_AREA8_SCENE_BUILD_V2717.md` for exact source GLBs, hashes, asset-only derivative recipe, model/tile transforms, and runtime QA gates. The root source .blend remains immutable. Blender export must use use_selection:true AND use_active_scene:true. Tile texture.src must be valid conventional 2D `modules/levels-3d-preview/assets/blank.webp`, model3d in 3D Canvas flags. Check non-null ID, changed revision, manifest, actual renderer rather than solely controlled AABB.

## Remaining before PLAYABLE or DM ACCEPTED
- Actual player-token navigation across annular sectors and at entrances; collision/sight and fall-through checks; source/perimeter accessibility and doorway/exit correctness; measured genuine mesh-mesh seam and roof bearing; player vs GM visibility.
- Foundry actor/encounter/journal, secrets, triggers, ambience, performance/VRAM/FPS and real session smoke test, plus final DM visual review and acceptance.
- Keep released test scene as a numbered reversible baseline. No claim new dedicated scene exists, no claim GLB instancing in runtime is preserved, and no claim final DM acceptance.
