# Reusable modular Blender to native 3D Canvas construction

Use physically measured reusable components for constructed rooms. Keep registered organic cave/chasm meshes and terrain in their natural shapes. Grid scale is a mapping between metres and scene pixels; it does not authorize rescaling door clearance or making a natural boundary rectangular.

## Construction contract

Author metres, global coordinates, one shared connector lattice, named portal ownership, supported floors/treads, exact clear openings and continuous world texture phase. Preserve independent moving leaves, reveal walls, fixed frames, hazards and dressing. Keep an editable collection-instance assembly and independently editable area scenes. Export repeated static components to shared, content-hashed model paths, with verified shared image dependencies.

A component catalog does not by itself establish a connected building. Verify assembled corners, ceiling-height returns, complete doorway roof bands, floor bridges and walls above pit shafts. A floor hole must not suppress the adjacent room's wall above floor level. Shared-wall artwork must select the actual shared surface, regardless of which room owns it.

## Native placement and merging

Foundry V14 rounds Tile position and dimensions. At a 100-pixel, five-foot grid, quarter-grid components have odd pixel extents. Use integer static construction bounds, baked orthogonal variants and exact anchors. Preserve half-grid fixed frames/headers independently when their placement cannot survive the merge/unmerge rounding rule.

Use native Auto Merge on compatible static placements sharing the same model path and effective collision, sight, camera, shadow and material settings. Keep moving leaves, reveal objects, independent portal frames, bars and support-only meshes outside that batch. Measure actual native Merge/Unmerge transform preservation. Retain a complete original placement manifest: native unmerge may copy the representative member's custom flags rather than restoring each member's semantic metadata.

Native model caches use paths. Replacing bytes under an unchanged URL can leave the old model visible; put the content hash in the filename. Match a merged representative to its native orientation variant as well as its original component family when updating models. Replacing an owned repair batch must remove its previous merged derivatives before creating the canonical placements again.

Rotating doors and frames require native anchors compatible with both the rendered rotation and Foundry's spatial index. Test closed blocking, opening, crossing, ordinary Close, reverse blocking, reopening and return. Test actual rendered menu buttons; the reserved Dialog action `close` dismisses a menu, so use a distinct action such as `shutDoor` for changing the door state. Pair double leaves in the user-facing control.

## Surface art and support

Export exactly one populated glTF Scene. Inspect the exported scene list rather than assuming selection-only export excludes other Blender scenes. Thin conforming surface art needs exact placement bounds; an invisible, noncolliding registered export envelope can prevent integer Tile dimensions from shifting the visible skin behind masonry. Keep these helpers separate from visible art and physics.

Sample actual evaluated floor/tread faces and native support independently. Test slightly inside mating faces; retain exact-edge numerical misses separately. A conservative millimetre tolerance in a source-derived invisible support mesh can address native seam precision without moving visible floors or changing source hazard depths. Do not use AABB proximity as proof of actual structural contact.

## Evidence and speed

Freeze the physical grid and portal contract after a tested fixture. Expand in connected area batches. Use dependency-aware repair checks: a texture edit needs matched renders; a wall/aperture edit needs collision and route tests; a render-visibility policy needs matched actual images, collider invariance and moving/standing performance samples.

Keep grid review positions, setup relocations, ordinary movement and valid standing footprints distinct. Record source-boundary, solid structure, occupied miniature, prop and low-headroom exclusions. Unexplained missing floor support fails the review. Use actual native token eye positions and actual composer frames; do not infer camera correctness from a capture label.

For performance, identify the true native renderer, loaded models, focus, buffer size, full-composer calls/triangles, light/shadow state and pass inventory. Keep original resolution/materials and measure both standing and ordinary movement. Instance counts and fewer Tile documents are not FPS proof. A conservative exterior/underground render policy must recognize mixed-area merged instance groups and preserve the entry transition; never classify every instance by its first room's metadata.

Preserve accepted source masters, separate review Scenes, release manifests, failed diagnostics and rollback. Saved, structural, visual, runtime and DM acceptance remain separate states.

## Final acceptance correction

The final modular candidate disables automatic exterior/interior visibility culling. Conflicting cached helper instances had hidden exterior models, invalidating earlier culling-based timings and image-parity results. Stop every owned legacy helper instance before checking that all native Tile meshes are visible. Use only full-visibility timings for this candidate: fewer Tile documents and native merging did not deliver a consistent 60 FPS. Keep the prior production version selected until the DM accepts the alternative.

Desktop key simulation can produce a trusted ArrowUp event with an empty `code`. Foundry binds `ArrowUp` by code, so that event does not test physical keyboard walking. Record event fields before changing bindings. In this case the unchanged native registered movement callback, supplied a complete key context, moved the selected walker one supported grid step; physical keyboard input remains a separate user check.

## Source-feature preservation across construction methods

A modular migration must preserve native image effects, clue images, particle settings and their offset/elevation contracts as well as GLB props. Geometry-only or solid/decorative-prop retention filters can silently omit a visible portal or clue without failing floor, wall or door tests. Reconcile every source feature to an actual current visual/runtime artifact, including effects that have no Blender mesh. Carry that explicit native-effects inventory through the layout, import manifest, dependency package and close-up review. A successful traversal test cannot substitute for this check.

