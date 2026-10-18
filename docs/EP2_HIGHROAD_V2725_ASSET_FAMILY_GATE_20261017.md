# Episode 2 High Road — v2.7.25 asset-family sufficiency QA

Date: 2026-10-17 US Eastern. **Read-only G0/G1.5 audit** of saved v006 after installed autonomous-world skill v2.7.25. This is NOT an edited scene or G3 pass.

## Source-fact envelope (private book, not reproduced)
The official adventure's Episode 2 travel segment sends the party north out of Waterdeep along the High Road, east along Triboar Trail, then south to Phandalin. On the High Road they skirt the Mere of Dead Men, dangerous swamp terrain, and encounter Thetsis the lizardfolk, Rasqel (Zhentarim-backed merchant), and his bugbear muscle Jutt and Meff. The scene must communicate a passable overland thoroughfare immediately beside dangerous, wet lowland, with space for that threatening roadside confrontation. The exact scenery positions and precise 3D road widths are not specified by this retrieved prose; label those as DESIGN. Later Triboar Trail and south track are separate encounters, not required in this immediate scene.

## Baseline — actually observed in connected Blender
Saved clean `G:\\My Drive\\D&D\\Foundry Bridge\\assets\\Episode2_HighRoad_BankPilot_v006.blend`, **167,326,574 bytes**. Renderer active camera `HighRoad_ThreeQuarter_QA`, World color gray `(0.15,0.15,0.15)`. Actual object inventory: 16 road objects sharing ONE genuine Meshy road mesh datablock; 11 marsh objects sharing ONE optimized genuine Meshy marsh mesh datablock; 4 bank wedge objects using TWO independent derivatives of the road source, neither a separate source silhouette. **31 mesh objects, only TWO unique provider source assets.** `Episode2_HighRoad_Environment_v007.blend` does NOT exist as of read-only check. Previous actual v006 hero image visually inspected: floating sandy raised slab with a huge tapered side wedge, handful of repeated low wetland clumps, empty gray background. Fails intended outdoor world feel. Current structural seam G3 still FAIL/UNVERIFIED from earlier paired surface crossing (local ~8.56mm, wider ~32.94mm).

## Mandatory G1.5 role matrix

| Environment asset role | Existing asset coverage | Gate / next |
|---|---|---|
| Continuous walkable road bed | Genuine single road tile instanced 16× | PARTIAL: path coverage sampled, physical connector and art repeat FAIL |
| Natural road-to-earth transition (dry shoulder) | Copied road mesh tapered four bank pieces | FAIL: obvious straight wedge/slab underside; needs bespoke terrain family |
| Marsh shoreline / muddy ground surface | Low vegetation clump only; no marsh ground | MISSING: design connected wetland earth/waterline and contact with road |
| Vertical wetland trees/deadwood/rock silhouette | None | MISSING: avoid empty gray skyline and repetitive low shrubs |
| Wetland edge reeds/brush | Genuine marsh clump one silhouette 11× | PARTIAL: variation/provenance inadequate for landscape |
| Convincing distant environment/horizon | World gray alone | FAIL: may use atmosphere/fog/lighting only; visible geometry needs genuine GLB |
| Thetsis/Rasqel/Jutt/Meff confrontation assets | None in road Blender scene | MISSING for later encounter staging; don't invent unverified action or conceal GM-only facts |
| Integrated true road + surrounding land, first-person hero | v006 high three-quarter camera | FAIL: no actual eye-height QA, no world-feel preview |

**Immediate decision:** G1.5 FAIL. Do not mass-replicate existing wedge/road tiles. Prioritize new purpose-built natural bank/ground connector + wetland vegetation/tree silhouettes. Choose source-faithful style consistent with approved sandy road and muted damp brown/moss green; disallow procedural Blender visible geometry. Before spending, make an isolated one-object reference that includes the intended road-facing connector and wet marsh silhouette, validate it, generate Meshy standard textured 2K PBR GLB, inspect four installed directions, then 2-module connector prototype at the canonical 1.524m pitch. Material-only tint of v006 did not solve shape; don't repeat.

## First asset contracts (DESIGN — not stated official dimensions)
1. **ROAD-SHOULDER-MARSH-EDGE modular strip**: authentic irregular 1.524m approximate repeatable front interface; natural slope and earth/grass/reeds toward swamp, opaque believable underside, no straight bevel wedge; both top/side profile reference and measured local road lip. Need controlled left/right variants or separate dry shoulder family.
2. **MERE-OF-DEAD-MEN MARSH EARTH/PUDDLE PANEL**: connected swamp ground visibly below road shoulder with reeds, saturated silt, roots, subtle greenish waterline detail as genuine textured 3D mesh; required truthful contact zones.
3. **DEAD-WILLOW/BROKEN-WETLAND-TREE silhouette**: gnarled stump/trunk/branches with a credible ground-contact root base and height sufficient to anchor horizon; isolated one asset, no backdrop painted into the model.
4. **DRY ROADSIDE EARTH/STONE BANK** distinct material and texture from peat side; use original Meshy ground source rather than copied road as substitute.
5. **ENCOUNTER PROPS** later: road merchant trade gear and source character staging; must be produced/placed after actual source/map reference and core world feel.

## Autonomy and hard gates
User has given standing overall Meshy budget authorization; however provider's tool requires per-operation cost confirmation. Reference GPT-image-2 via Meshy nominal 9 credits, standard Meshy 7.1 PBR textured model nominal 30 credits, 39 credits/one asset chain before any paid extras; this audit DOES NOT authorize circumventing provider hard confirmation. No new paid tasks started here. If paid actions gated, advance camera/blueprint/UV/connector and isolated free prep, clearly report needed step. Target 15–20 real hypothesis+QA+KEEP/REJECT operations per active hour when tools permit, not invented progress; preserve v002-v006 and accepted Area8 v082; actual art PREVIEW and G3/Foundry playability independently gated. Any new local .blend/PNG needs readback and Google Drive file-ID confirmation before cloud claim.

## Authority
Installed plugin v2.7.25 release pluginrel_6ad43e6ea5ac8191a0f00801d59b40b3, binding AUTONOMOUS_WORLD_BUILD_V2725.md. GitHub docs/AI_3D_SKILL_V2725_AUTONOMOUS_WORLD_BUILD_20261017.md commit ffcff221c766f086dde7c5a0f40130bf8f7425f3. The current scene remains v006 and was not changed by this audit.
