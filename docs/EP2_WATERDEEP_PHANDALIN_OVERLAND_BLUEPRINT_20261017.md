# Episode 2 — Waterdeep to Phandalin: 3D Overland Blueprint v001
Date: 2026-10-17. Status: SOURCE-READ + G1 DESIGN, NOT constructed, NOT DM-accepted.
Private primary source: Acquistions_Incorporated_Full_Source_Book.pdf, Drive id 1amfybsizYOvD_2VSfDfw8wX1wtjDUArk, Chapter 4, Episode 2 pp.97–101. Do not redistribute primary text.

## Canonical authored itinerary (SOURCE)
Waterdeep → north High Road (about six walking days to Triboar turnoff) → east Triboar Trail (about one day) → south track into Phandalin (about four hours). Adventure offers 3 scripted overland encounters; random daytime/rest encounters optional.
1. Free-Market Lizardfolk, High Road beside Mere of Dead Men: Thetsis, Rasqel, bugbears Jutt and Meff; road parallel to dangerous marsh; commercial dispute and potential algae franchise opportunity.
2. The Wrongness, Triboar Trail: after eastbound turn, road less maintained than High Road, encounter Carkuss seated in center of road, holding Beshaba copper antler-symbol medallion; riddle and fortune/misfortune scene.
3. A Horse Is a Corpse, of Course, south track: rough road, pair of dead horses and overturned cart blocking path, spilled sacks and barrels, close trees and thick undergrowth, dead goblins posed/tied in vegetation/trees, undead horses spring ambush. Preserve GM secrets and scripted distances in encounter manifest.
Source fact != scene production design below. No pretense that official book maps exact encounter dimensions.

## Reusable route strategy (DESIGN)
Produce 3 separate performant Foundry 3D encounter scenes, not a physically continuous multi-day road. Transitions delivered with travel narration and a route progression map. One art-compatible kit: approved Meshy-derived repeatable terrain surfaces, road-edge shoulders, rocks, vegetation, banks, canopy clusters, wagon debris, and character-scale landmarks; each derived GLB optimized for Foundry. High Road: wider, maintained caravan way at swamp boundary; Triboar Trail: narrowed, rutted low-traffic road; final track: rough, close vegetation and concealed sightlines. Asset-only rendered geometry; never procedurally generate visible earth, foliage or road mesh.

## Prototype G1 — High Road / Mere of Dead Men (DESIGN dimensions pending asset interface measurements)
Canonical pitch 1.524m (5ft), axes X across road, Y along approach, Z vertical. First controlled fixture: 2x2 road tiles; two adjoining road-edge modules, 1 approved background marsh-bank/vegetation model only if real asset exists; two player-height QA views and structural overhead. Preliminary encounter canvas: 12 × 16 grid cells (60 × 80ft); provisional road corridor 3 cells (15ft) wide; shoulder + staged marsh off one side; positions TBD after authentic Meshy GLB bounds and collision. These dimensions are production choices, not source distances. Fix camera at approx 1.6m eye level, view along road toward Rasqel/Thetsis grouping; preserve flanking vegetation silhouette with no spoiler text in player exports.

## Asset procurement and QA
First search approved GLBs and Meshy library; existing module library only for construction technique unless stylistically certified. Missing road, marsh, trees, vegetation, wagon, NPC statues require purpose-built genuine Meshy GLBs. For each: isolated three-quarter isometric input image; verify single object; Meshy 7.1 PBR textured GLB; isolated 4-angle Blender review and provenance. Meshy charges require provider-specific advance confirmation. Build separate production derivatives with copy-versioned decimation and 1K textures for Foundry, retain original immutable. Instancing by linked mesh data; verify glTF and in-engine performance rather than assuming linked duplicates become GPU instances.
G3 actual connector planes/matrix-world tested on two adjacent road units, 2x2 traversal no cracks or unintended dips; screenshot with real active scene, roof not applicable; terrain edges blend with genuine vegetation GLBs. G4 no bulk replication without fixture pass. Camera/character support, walls/obstructions, line of sight, lighting, movement cost and token collision separately tested. No auto-follow camera changes. User approval only after genuine rendered review.

## Next reversible action
Inventory current approved road/ground/vegetation model availability, then create isolated road-tile reference and get provider credit confirmation if charged. Do not edit preserved Area8 v082 or Foundry Area8 test scene. Report exact new blend checkpoint and PNG only when verified.
