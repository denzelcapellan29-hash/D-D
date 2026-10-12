# Modular library study — October 12, 2026

**DM direction:** Four-floor-tile and two-row wall v012 visually look good (DM feedback); preserve them as visual prototype, not yet certified structural connectors. Kenney and Quaternius assets are available as **construction references only**. Do not place their meshes or materials into the bespoke Area 8 scene.

## Kenney
Official source: https://kenney.nl/assets/modular-dungeon-kit (40 files, CC0, revisions 2.0 higher walls and 2.1 ground detail). Verified ZIP downloaded on connected Blender workstation to `G:\My Drive\D&D\Foundry Bridge\references\modular_library_study\kenney_modular_dungeon_1.0_REFERENCE_ONLY.zip`, size 6,886,434 bytes, archive 218 entries, with `License.txt` and FBX models such as corridor-corner, corridor-end, corridor-intersection, corridor-junction, corridor-transition, corridor-wide. Versioned filename may differ from site update text: verify actual archive metadata before relying on version.

## Quaternius
Official https://quaternius.com/packs/modulardungeon.html; official public Drive folder https://drive.google.com/drive/folders/1CvofJVYHf00StUTsIWtOuyVxeV0CN3UI; 48 models in Blend, OBJ, FBX (CC0), distributed as separate folders. Two actual OBJ references downloaded through connected Drive and examined in temporary analysis container; full pack not copied into project storage. `Wall_Modular.obj`: 872 source vertices, XYZ bounds approximately [-0.9998,1.0009],[-1.0021,1.0033],[-0.2190,0.2190]; `WallCover_Modular.obj`: 146 vertices, XYZ [-1.0043,1.0058],[-1.0098,-0.5781],[-0.2546,0.2546]. A near-2-unit repeating span suggests modular pitch but this remains a **hypothesis**, not certified join compatibility. Representative public Drive file IDs 1YwJR8fY-QQEmDyq0Al9DJlR8zEHz8MoU and 1tLsNbIWttYJvDRYXOi3HqKm0JtI0hLcR.

## Construction lessons
Study naming by role and connector (straight / corner / junction / end / wide), shared base pitches, object pivots, world-coordinate normal/face joins, wall/floor/roof connection strategy, and verifiable physical surfaces. Keep source module shape/artist-driven texture separate from world grid transform. Do not infer joint quality from AABB or matching names alone. Do not add third-party geometry to active approved Area 8 scene. V012 remains DM visually satisfactory but structural QA pending.
