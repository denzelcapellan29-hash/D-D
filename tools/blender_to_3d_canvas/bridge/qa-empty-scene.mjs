/** Native Foundry V14-only, isolated empty QA Scene lifecycle.
 * Operates on one exact reserved name/tag. Never copies scene contents,
 * activates for players, or edits the accepted source or unowned Scenes.
 * Source revision is enforced by calling wrapper's sceneSnapshot().
 */
export const SOURCE_SCENE_ID = "NUEDEFAULTSCENE0";
export const SOURCE_SHA = "e1c023a1ef9688fb4a0f4112adbc41b39089d04190bbaa696a6b36946c8c974f";
export const QA_NAME = "QA ONLY - Empty 3D Canvas Integration - 20261024";
export const QA_TAG = "qaEmpty3dFixture";
export const MODULE_ID = "acq-foundry-bridge";
export const EMBEDDED = ["tiles","walls","lights","regions","tokens","drawings","sounds","notes","templates"];

const docList = collection => Array.from(collection?.contents ?? collection ?? []);

export function isOwnedEmptyQaScene(doc) {
  const tag = doc?.flags?.[MODULE_ID]?.[QA_TAG];
  return Boolean(doc?.name === QA_NAME && doc?.active === false &&
    doc?.navigation === false &&
    tag?.sourceSceneId === SOURCE_SCENE_ID &&
    tag?.expectedSourceRevision === SOURCE_SHA &&
    tag?.purpose === "isolated-3dcanvas-native-import-qa" &&
    tag?.schema === "acq-empty-scene-v1");
}
export function counts(scene) {
  const result = {};
  for (const key of EMBEDDED) result[key] = Number(scene?.[key]?.size ?? docList(scene?.[key]).length);
  return result;
}
export function exactEmpty(scene) {
  return Object.values(counts(scene)).every(n => n === 0);
}
export function reservedMatches(scenes) {
  const items = docList(scenes);
  return items.filter(s => s.name === QA_NAME || s.flags?.[MODULE_ID]?.[QA_TAG] !== undefined);
}
export function freshScenePayload() {
  return {
    name: QA_NAME,
    active: false,
    navigation: false,
    ownership: {default:0},
    width: 4000,
    height: 3000,
    padding: 0,
    grid: {type:1,size:100,distance:1,units:"ft"},
    tokenVision:false,
    background:{color:"#20252b"},
    flags: {
      [MODULE_ID]: {
        [QA_TAG]: {
          sourceSceneId:SOURCE_SCENE_ID,
          expectedSourceRevision:SOURCE_SHA,
          purpose:"isolated-3dcanvas-native-import-qa",
          schema:"acq-empty-scene-v1",
          createdAt:new Date().toISOString()
        }
      },
      "levels-3d-preview": {
        renderTable:false,renderBackground:false,
        showSceneWalls:false,
        ambientLightIntensity:0.9,exposure:1
      }
    }
  };
}
export async function manageEmptyQaScene(op, dryRun, context) {
  const {game,canvas,sourceRevision,revisionOf} = context;
  if (!game?.user?.isGM) throw new Error("Empty QA Scene lifecycle requires GM.");
  const action = String(op?.action ?? "");
  if (!["inspect","preflight","create","view","restore_view","delete"].includes(action)) {
    throw new Error("Unsupported empty QA lifecycle action.");
  }
  const source=game.scenes?.get(SOURCE_SCENE_ID);
  if (!source || sourceRevision !== SOURCE_SHA) {
    throw new Error("Protected source Scene absent or checksum changed.");
  }
  const matches=reservedMatches(game.scenes);
  if (matches.length > 1 || (matches.length === 1 && !isOwnedEmptyQaScene(matches[0]))) {
    throw new Error("Ambiguous/unowned reserved QA Scene. No operations allowed.");
  }
  const qa=matches[0] ?? null;
  if (qa && qa.id === SOURCE_SCENE_ID) throw new Error("QA Scene resolved to source Scene.");
  const active=game.scenes.active?.id ?? null;
  const viewed=canvas?.scene?.id ?? null;
  if (active !== SOURCE_SCENE_ID) throw new Error("Protected original must remain active for players.");
  const details={
    source_scene_id:SOURCE_SCENE_ID,source_revision:SOURCE_SHA,
    qa_scene_id:qa?.id ?? null,qa_exists:Boolean(qa),
    qa_owned: Boolean(qa && isOwnedEmptyQaScene(qa)),
    qa_counts:qa?counts(qa):null,
    qa_empty:qa?exactEmpty(qa):null,
    qa_revision:qa && typeof revisionOf==="function"?await revisionOf(qa):null,
    foundry_active_scene_id:active,gm_viewed_scene_id:viewed,
    players_pulled:false
  };
  if (action==="inspect" || action==="preflight") return {...details,read_only:true,dry_run:true};
  if (action==="create") {
    if (qa) return {...details,already_exists:true,dry_run:dryRun};
    if (viewed!==SOURCE_SCENE_ID) throw new Error("GM must view accepted original before creating QA Scene.");
    if (dryRun) return {...details,would_create:true,dry_run:true};
    const candidate=freshScenePayload();
    const created=await source.constructor.create(candidate);
    if (!created || !isOwnedEmptyQaScene(created) || !exactEmpty(created) ||
        game.scenes.active?.id !== SOURCE_SCENE_ID) {
      // Failed creation should not delete an uncertain Scene. A separate,
      // guarded inspector must establish ownership before cleanup.
      throw new Error("Native Scene creation not fully verified. STOP; inspect reserved QA Scene.");
    }
    return {...details,created:true,dry_run:false,qa_scene_id:created.id,
      qa_exists:true,qa_empty:true,qa_counts:counts(created),
      qa_revision:typeof revisionOf==="function"?await revisionOf(created):null};
  }
  if (!qa) throw new Error("Provisioned QA Scene does not exist.");
  if (action==="view") {
    if (op.qa_scene_id !== qa.id) throw new Error("Exact QA Scene id required for local viewing.");
    if (viewed!==SOURCE_SCENE_ID && viewed!==qa.id) throw new Error("GM is viewing an unrelated Scene.");
    if (dryRun) return {...details,would_view:qa.id,dry_run:true};
    if (viewed!==qa.id) await qa.view();
    if (canvas?.scene?.id!==qa.id || game.scenes.active?.id!==SOURCE_SCENE_ID) {
      throw new Error("GM QA view verification failed; restore source view.");
    }
    return {...details,now_viewed:qa.id,dry_run:false};
  }
  if (action==="restore_view") {
    if (viewed!==qa.id && viewed!==source.id) throw new Error("Cannot restore from an unrelated GM view.");
    if (dryRun) return {...details,would_view:source.id,dry_run:true};
    if (viewed!==source.id) await source.view();
    if (canvas?.scene?.id!==source.id || game.scenes.active?.id!==source.id) {
      throw new Error("GM original view restoration unverified.");
    }
    return {...details,now_viewed:source.id,dry_run:false};
  }
  // Deletion requires exact reserved ownership + empty Scene. Imported
  // Tiles or foreign added content prevent cleanup until separately removed.
  if (viewed!==SOURCE_SCENE_ID || !exactEmpty(qa)) {
    throw new Error("Cannot delete: GM not viewing original or QA Scene not empty.");
  }
  if (dryRun) return {...details,would_delete:qa.id,dry_run:true};
  const deletedId=qa.id;
  await qa.delete();
  if (game.scenes.get(deletedId) || game.scenes.active?.id!==source.id) {
    throw new Error("QA Scene deletion not independently verified.");
  }
  return {...details,deleted:true,deleted_scene_id:deletedId,dry_run:false,
    qa_exists:false,qa_scene_id:null};
}
