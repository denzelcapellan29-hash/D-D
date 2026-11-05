# Native procedural kits and source-constrained furnishing

Use this opt-in lane when native procedural construction has been selected. It complements the editable Blender workflow; evaluating a generator does not migrate an accepted location. Keep Blender originals for our authored assets and unique structural/artwork sections. For native kit construction, the editable assembly is the source specification, versioned recipe, asset catalog and native documents, rather than an inseparable whole-building GLB.

## Choose the authority before generating

| Situation | Geometry authority | Appropriate generator role |
| --- | --- | --- |
| Source permits a regular room/building with no fixed plan | Approved dimensions, connections and feature constraints | Seeded kit layout and furnishing within those constraints |
| Published map specifies rooms, passages, stairs or irregular boundaries | Calibrated source polygons, elevations, portal graph and approved interpretation | Build compatible fixed components or furnish the authored shell |
| Distinctive ruins, caves, relief or signature art | Existing source-fitted Blender master | Native furnishing, compatible repeated components and runtime integration |

A room-type label, matching seed or plausible overhead image does not certify the source layout. Before construction record map identity, scale, north, coordinate transform, polygons, height changes, doors and blocked/secret routes. Assign one owner per shared wall and opening. Separate fixed source facts from decorative variation. Preserve source-required absences: a room containing only a bed and desk must not receive generic workshop clutter.

## Why the native kit approach is useful

The generator combines a small measured asset vocabulary, seeded layout decisions, semantic room recipes, targeted dependency downloads and native Tile/light emission. Compatible repeated static pieces share native instanced groups. Doors and animated props normally remain independent. This can substantially reduce manual placement and CPU submission. It does not remove texture, pixel shading, lighting, transparency or postprocessing cost.

Reuse these principles in our production tools:

1. Select a small compatible family before constructing the location. Use measured physical bounds, pivot/axes, connectors, materials, provenance and native role contracts.
2. Compile layout and furnishing from data. Keep coordinates and required features out of one-off UI actions. Author unique geometry only where the source or art needs it.
3. Reuse the same runtime resource for repeated eligible pieces. A category name or similar appearance does not create GPU resource sharing.
4. Batch compatible static content at a sensible spatial/level boundary. A whole-storey instance group may keep offscreen instances rendering; fewer draw calls can increase submitted triangles. Measure player views and overhead views separately.
5. Keep interactive, mixed-role, secret/reveal and level-transition pieces independently editable and testable. Never make a moving door part of an inseparable static group.
6. Preflight dependencies and required categories before a costly build. Missing entitled models can yield a partial generation; a returned API call is not completeness evidence.

## Our assets: consumer adapters, not changes to the master

Baileywiki Building Generator 0.2.14 exposes mutable asset/theme/floor/room catalogs and generation/furnishing functions. This was inspected and tested with 3D Canvas 9.0.36. It is a version-specific extension surface, not a guaranteed stable registration API. Keep the adapter in our code; leave publisher files unchanged. Recheck behavior after updates.

Architectural model measurements in this generator use one unit per five-foot square. Our metric architecture uses 1.524 meters per five feet. Make an immutable runtime derivative scaled by `1 / 1.524`, including node translations, and verify physical dimensions after native placement. Do not change the metric art master or rescale all props indiscriminately. Prop length/height limits use feet alongside measured model units; declare and test both.

The accompanying static-GLB normalizer deliberately rejects animation, skinning, morphs, compressed geometry, sparse attributes, multiple scenes and unsafe dependency paths. It preserves topology, UVs, normals, materials and image bytes while scaling positions and translations. Verification includes altered-vertex/material/channel negative controls. Animated assets need a separate appropriate exporter.

Library compatibility and procedural kit compatibility are different. Confirm:

- model dimensions, origin, orientation and native Tile anchors;
- floor thickness, continuous support, wall pitch and corner/end fittings;
- independent hinges, closed/open clearances and exact native door control;
- material/texture/channel support and repeat density;
- actual consumer collision, sight and camera roles;
- measured cost, dependency availability and permitted private/public distribution.

### Preserve roles through instancing

In the inspected native version, merged instances can retain an entity-level indication that source meshes had role tags while the newly created instance meshes lack those tags. This can leave a visible custom floor out of native collision groups. A consumer-specific derivative may transfer a declared *uniform* static role to native Tile flags, after explicit compatibility checks. Preserve the original tagged asset. Never flatten conflicting per-mesh roles or embedded doors this way.

An embedded-hinge model placed through a wall category can be batched even though its source contains a door. Normal generator exclusion of door-category Tiles does not automatically protect a custom wall-category model. Exclude/rebuild those interactive pieces independently from the authoritative plan and test the result. Native unmerge is not automatically lossless for every origin/hierarchy; compare actual geometry and placement before relying on it.

Loaded geometry is not the same as ready interaction. In the inspected native implementation, embedded-door setup runs after the `_loaded` flag. Wait for the required native hinge/control inventory and stable behavior, not merely the loader bit.

### Scope catalog changes

Register namespaced temporary entries only for the owned generation. Initialize or account for cached recipe templates before adding entries: an internal template may snapshot custom entries and restore them after apparent cleanup. Restore our entries in both the live catalog and the cached template in `finally`. Guard supported versions and reject concurrent mutation. Do not spoof BCM paths, authentication or entitlements. A local own-asset path is not a purchased-content identity.

## Source-constrained furnishing

Retain the calibrated structural shell and native role semantics. Supply the furnishing API with the actual room footprint or verified decomposition, elevation, doorway keepouts and existing obstacles. Restrict eligible assets by source role and palette. Treat automatic placement as a candidate that must satisfy postconditions.

For each room record:

| Field | Purpose |
| --- | --- |
| Fixed shell members and hashes | Prevent an attractive new random plan from replacing the source |
| Required/forbidden features | Prove source semantics, including intentionally sparse rooms |
| Allowed asset IDs and versions | Prevent unrelated furniture or modern/default scenery |
| Placement region and keepouts | Preserve entrances, stairs, combat space and accessible clues |
| Mechanic/reveal ownership | Keep secret clues, traps and GM-only features off shared views |
| Seed, options and dependency snapshot | Repeat the same candidate deterministically |

Do not claim full polygon support from a rectangular furnishing call. Validate every placement against the actual polygon, obstacle and clearance contract. Where the API lacks a required constraint, own that validation and repair in our adapter. Published trap mechanics remain manual unless separately implemented and tested.

When isolating a room for furnishing, follow its shared-boundary ownership into neighboring assemblies. Copying only matching area prefixes can omit a wall, ceiling return or concealed portal. Retain required boundary owners and closed/locked/secret states, inspect eye/reverse/overhead images, and probe the actual enclosure before accepting the shell.

## Reproduce the result, not just the seed

Freeze module/runtime versions, generator package hash, catalog entries, measured size/triangle metadata, exact asset and image hashes, authentication/dependency availability, scene grid/anchors/elevations, all options and seed. Existing-scene obstacles and load/quality budgets can affect a build. Preserve the returned plan and expected document/category inventory.

Rebuild into a new empty private scene. Compare the plan and complete normalized native Tile/light payloads, stripping only declared identity/generation/timestamp fields. Explain every stripped field. Compare required membership, transforms, materials, role flags, door states and dependencies; matching counts alone is insufficient. Keep the source scene's independent strict hash guard. Exercise native undo after a partial failure and confirm that lights and history are cleaned as well as Tiles.

Archive compact private recipes, allowed own assets, dependency manifests, scene exports, captures, tests and receipts. Do not copy complete module libraries, caches, private browser profiles or whole sourcebooks into each checkpoint. Download vendor dependencies through their authorized manager when restoring. Readable distributed code is not automatically licensed for public redistribution.

## Native acceptance and performance

Follow [native rendering and route evidence](NATIVE_RENDER_AND_ROUTE_EVIDENCE.md) and [performance preflight](NATIVE_PERFORMANCE_PREFLIGHT.md). Keep these separate:

- source/structural fit and visual review;
- native model/material/role readiness;
- finite floor/wall rays;
- ordinary supported walking, both portal directions, closed/open/reclosed blocking and stairs;
- Core Region Surface/Falling behavior where applicable;
- actual on-screen control usability;
- performance at stated views and buffer sizes;
- clean rebuild and exact authored-state restoration;
- DM artistic acceptance.

An unbroken visible floor may need a continuous collision representation; it must follow the declared source floor and preserve pits, stairs, holes and transitions. Never fill an unsupported source void to make a movement test pass. Verify seam contacts and actual traversal separately. Teleportation, retained elevation or disabled collision/Falling is not physical-support proof.

Measure a fresh verified native compositor, the actual shared drawing buffer, focus and GPU timer validity. Compare identical geometry, lights, materials, camera and display conditions. Record unique and placed triangles, complete-frame calls, median/p95/p99 intervals and actual images. Keep other heavy viewers/render jobs inactive. A scene report's letter grade estimates load; it is not measured FPS.

Report half/three-quarter/full rendering by actual buffer dimensions and visual tradeoff. Upscaled rendering may be a useful play option but does not establish full-resolution performance. Do not blame shadows without inspecting actual shadow-casting lights. Native cached/global lights and transmission materials can add costs absent from simple document counts.

### Camera-specific presentation

A top-down automatic cutaway can hide upper floors and roofs during first-person viewing. In the inspected native version the Scene `levels-3d-preview.mirrorLevels` flag controls mirroring of 2D Tile occlusion. Test a private camera-specific presentation profile with authored ceilings retained; preserve the original top-down profile and global settings. Roof geometry may expose its exterior shingles underneath and still need a source-compatible ceiling finish. Visibility settings do not provide GM secrecy: omit unrevealed GM-only geometry from shared views and test actual player-eye images.

## Adoption decision

Use a proven native kit for regular architecture and ambient dressing when it fits the source and art. Use our constrained adapter for fixed source shells. Keep distinctive geometry and source-specific interfaces in the existing Blender lane. Advance only the validated family/scale/runtime combination; one passing room does not certify all doors, stairs, roofs or the complete Manor. Preserve accepted originals and failed evidence while repairing the affected interface.

## Portable normalizer checks

Run `python -m unittest discover -s tools/native_kit -p "test_*.py" -v`. Fixtures are original synthetic geometry with interleaved channels and a hinge hierarchy; they need no campaign files or vendor downloads. Use `python tools/native_kit/normalize_glb.py <metric-static.glb> <new-runtime.glb>` only after validating the model family and intended scale. Native collision/door/movement tests remain separate.

Compare two exported empty-environment Scene objects with `python tools/native_kit/compare_native_scenes.py first.json second.json`. It compares declared configuration/native settings and complete embedded environment document payloads, removing only document identity/audit fields and the named generation ID. It rejects live tokens and detects changed door states, lost collision, moved pieces, missing lights and scale changes. Its report lists the exact scope; it does not compare an entire world or certify source/gameplay/art.
