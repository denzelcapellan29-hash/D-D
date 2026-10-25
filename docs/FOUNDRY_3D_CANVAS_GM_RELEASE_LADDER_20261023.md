# GM-controlled Foundry V14 + 3D Canvas — condensed release ladder

Status as at 2026-10-23 late: ENGINEERING DEVELOPMENT, NOT production acceptance. This ladder targets completion in no more than approximately ten DM follow-up exchanges, but no QA results may be fabricated to meet a prompt count. DM holds visual acceptance.

## Already verified; do not repeat as setup
- 3D Canvas and Premium installed; 14 Acq tools, 121 Foundry actions exposed. Native renderer, first-person following/free-look and native wall-blocked movement passed; closed/open/reclosed sliding door passed; Foundry V14 Surface hit independently passed.
- v0.1 true Blender GLB source-derived native import passed; v0.2 two-chunk rotated/parented/elevated asset import and 3-mesh native door Tile structure passed; v0.2r two-Tile idempotency and targeted GLB model URL updates passed.
- Native transaction interrupted-write and *lost acknowledgement* completed create/update recovery passed against the pinned GM-only QA clone; 27/27 offline test suite passed. Last verified source/QA checksums exact and fully restored. Draft PR8 unmerged.

## Six remaining independent completion gates (efficient order)
1. **Source-faithful full-room fixture:** choose only a confirmed available source-authored room (not another instance's live Manor build) or an assembled small test from existing genuine library floor/wall/roof/door assets. Validate source provenance, measured floor grades, entrances, material maps and lighting. Stage per-chunk GLBs and compare real player-eye, overhead and angled native Foundry captures against real Blender views. No fake procedural visible geometry.
2. **Native imported-world physics:** on the newly imported fixture, verify actual step/floor transitions and support, collision/LOS/roof separation and door through/open/closed. Reuse prior movement and separate native Surface/wall/door evidence; test only newly introduced interoperability. Keep D&D5e Falling disabled unless a separate DM-approved controlled rules test is needed. If manual falling suffices, document that as intended GM operation.
3. **Production-worthy pipeline:** validate multi-chunk imports at realistic memory budgets, save/reload and update/rollback after renderer reload. Remove pinned QA-only assumptions only with a new approved destination-scene allowlist and exact protected-source ownership checks, not arbitrary production mutations.
4. **GM presentation:** native free/first-person camera, no clipping/black-frame regression, token occupancy, hiding GM-only spoilers on the shared display, optional cutscene/free camera; native GameCamera visual failure may remain an optional feature if native free/FPS meets DM requirement.
5. **Native Premium operational coverage:** inventory actual UI capabilities; create scoped typed bridge methods only for essential materials, environments, props and effects not already operable. Never duplicate 3D Canvas mechanics or patch third-party vendor source; preserve existing 14 tools and expand cautiously with versioned tests.
6. **Release soak and handoff:** cold Foundry reload, repeated GM scene-switch/camera interaction, performance/memory capture and exact accepted-source scene revision. One consolidated release report distinguishes passed controls, deliberate optional disabled features, remaining bugs and direct DM acceptance. Only merge PR after successful full fixture and approvals.

## Authority and no-touch
Accepted source Scene NUEDEFAULTSCENE0 SHA e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f, QA clone sW4aXZgKXj1cH0US baseline SHA 05134d2c6debeb2ffb49d17b3f1c06e96dfa409c35a348d801157dd815a03e94. Other instance owns Manor work. Do not modify it, its GLBs, Blender masters or scene documents. No unapproved generated Blender-visible geometry, no Meshy paid actions without task-specific provider confirmation, no vendor patch or blanket D&D5e setting change.

Current implementation and proof: https://github.com/denzelcapellan29-hash/D-D/pull/8 ; docs/FOUNDRY_BLENDER_MULTICHUNK_IMPORT_V02_QA_20261023.md (feature branch).
