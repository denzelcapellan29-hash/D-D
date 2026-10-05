const MODULE_ID = "acq-foundry-bridge";
const PROTOCOL_VERSION = 1;

const ALLOWED_EMBEDDED = new Set([
  "Tile", "AmbientLight", "Wall", "Region", "Drawing",
  "MeasuredTemplate", "Note", "Token", "AmbientSound"
]);

const ALLOWED_ENV_KEYS = new Set([
  "skybox", "exr", "renderTable", "tableTex", "tableColor",
  "renderBackground", "enableFog", "fogColor", "fogDistance",
  "sceneTint", "timeSync", "sunPosition", "sunIntensity",
  "exposure", "sunDistance", "sunTilt",
  "ambientLightIntensity", "ambientLightColor", "shadowBias",
  "bloom", "bloomThreshold", "bloomStrength", "bloomRadius",
  "filter", "filterStrength", "filterCustom",
  "renderSceneLights", "mirrorLevels", "showSceneWalls",
  "showSceneDoors", "showSceneFloors"
]);

let pollTimer = null;
let snapshotTimer = null;
let inFlight = false;
let lastConnected = false;

function agentUrl() {
  return String(game.settings.get(MODULE_ID, "agentUrl") || "http://127.0.0.1:18747").replace(/\/+$/, "");
}

function canonicalize(value) {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) out[key] = canonicalize(value[key]);
    return out;
  }
  return value;
}

async function sha256Object(value) {
  const text = JSON.stringify(canonicalize(value));
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, "0")).join("");
}

function activeScene() {
  return canvas?.scene ?? game.scenes?.active ?? null;
}

async function sceneSnapshot(scene = activeScene()) {
  if (!scene) return null;
  const data = scene.toObject();
  const revision = await sha256Object(data);
  return {
    protocol_version: PROTOCOL_VERSION,
    kind: "scene_state",
    generated_at: new Date().toISOString(),
    foundry: {
      version: game.version,
      world_id: game.world?.id ?? null,
      world_title: game.world?.title ?? null,
      system_id: game.system?.id ?? null,
      system_version: game.system?.version ?? null,
      user_id: game.user?.id ?? null,
      user_name: game.user?.name ?? null
    },
    scene_id: scene.id,
    scene_name: scene.name,
    revision,
    scene: data
  };
}

async function request(path, options = {}) {
  return fetch(`${agentUrl()}${path}`, {
    ...options,
    headers: {"Content-Type": "application/json", ...(options.headers ?? {})},
    cache: "no-store"
  });
}

async function postState(reason = "update") {
  if (!game.user?.isGM) return;
  const snapshot = await sceneSnapshot();
  if (!snapshot) return;
  snapshot.reason = reason;
  try {
    const response = await request("/bridge/state", {method: "POST", body: JSON.stringify(snapshot)});
    if (!response.ok) throw new Error(`Agent returned HTTP ${response.status}`);
    if (!lastConnected) {
      ui.notifications?.info("Acq Foundry Bridge connected.");
      lastConnected = true;
    }
  } catch (err) {
    if (lastConnected) ui.notifications?.warn("Acq Foundry Bridge disconnected.");
    lastConnected = false;
    console.debug(`${MODULE_ID} state post failed`, err);
  }
}

function scheduleSnapshot(reason = "update") {
  clearTimeout(snapshotTimer);
  snapshotTimer = setTimeout(() => postState(reason), 350);
}

function ensureGM() {
  if (!game.user?.isGM) throw new Error("Acq Foundry Bridge commands require an active GM client.");
}

function getFilePicker() {
  return foundry?.applications?.apps?.FilePicker ?? globalThis.FilePicker;
}

function b64ToFile(b64, filename, mimeType = "application/octet-stream") {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new File([bytes], filename, {type: mimeType});
}


function levels3d() {
  return game?.Levels3DPreview ?? null;
}

function vectorToObject(v) {
  if (!v) return null;
  return {
    x: Number(v.x ?? 0),
    y: Number(v.y ?? 0),
    z: Number(v.z ?? 0)
  };
}

function setVector(target, value) {
  if (!target || !value) return;
  const x = Number(value.x);
  const y = Number(value.y);
  const z = Number(value.z);
  if (![x, y, z].every(Number.isFinite)) throw new Error("3D vector requires finite x, y, z.");
  if (typeof target.set === "function") target.set(x, y, z);
  else {
    target.x = x;
    target.y = y;
    target.z = z;
  }
}

function relevant3dFlags(flags = {}) {
  const allowed = [
    "model3d", "material", "color", "scale",
    "collision", "sight", "cameraCollision",
    "doorType", "doorState", "doorStyle",
    "doorAnimationDuration", "doorAnimateAngle", "doorSlidePercent",
    "imageTexture", "fillType", "castShadow"
  ];
  const out = {};
  for (const key of allowed) {
    if (Object.prototype.hasOwnProperty.call(flags, key)) out[key] = flags[key];
  }
  return out;
}

function environment3dFlags(scene) {
  const src = scene?.flags?.["levels-3d-preview"] ?? {};
  const out = {};
  for (const key of ALLOWED_ENV_KEYS) {
    if (Object.prototype.hasOwnProperty.call(src, key)) out[key] = src[key];
  }
  if (src.initialPosition) out.initialPosition = src.initialPosition;
  return out;
}

function inspect3dScene(scene) {
  const l3d = levels3d();
  const tiles = Array.from(scene?.tiles ?? []).map(tile => {
    const flags = tile?.flags?.["levels-3d-preview"] ?? {};
    return {
      id: tile.id,
      x: tile.x,
      y: tile.y,
      width: tile.width,
      height: tile.height,
      elevation: tile.elevation ?? 0,
      rotation: tile.rotation ?? 0,
      hidden: Boolean(tile.hidden),
      flags: relevant3dFlags(flags),
      acq: tile?.flags?.acq ?? null
    };
  }).filter(t => Object.keys(t.flags).length > 0 || t.acq);

  return {
    levels3d_active: Boolean(l3d?._active),
    levels3d_available: Boolean(l3d),
    camera: l3d ? {
      position: vectorToObject(l3d.camera?.position),
      target: vectorToObject(l3d.controls?.target),
      first_person_mode: Boolean(l3d.firstPersonMode)
    } : null,
    environment: environment3dFlags(scene),
    tiles,
    tile_count: tiles.length,
    light_count: Number(scene?.lights?.size ?? scene?.lights?.contents?.length ?? 0),
    region_count: Number(scene?.regions?.size ?? scene?.regions?.contents?.length ?? 0)
  };
}

async function set3dCamera(scene, op, dryRun = false) {
  const l3d = levels3d();
  if (!l3d?._active || !l3d.camera || !l3d.controls) {
    throw new Error("3D Canvas is not active or its camera controls are unavailable.");
  }

  const before = {
    position: vectorToObject(l3d.camera.position),
    target: vectorToObject(l3d.controls.target),
    first_person_mode: Boolean(l3d.firstPersonMode)
  };

  if (!dryRun) {
    if (op.position) setVector(l3d.camera.position, op.position);
    if (op.target) setVector(l3d.controls.target, op.target);
    if (typeof l3d.controls.update === "function") l3d.controls.update();

    if (op.save_as_initial) {
      await scene.update({
        "flags.levels-3d-preview.initialPosition": {
          target: vectorToObject(l3d.controls.target),
          position: vectorToObject(l3d.camera.position),
          firstPersonMode: Boolean(l3d.firstPersonMode)
        }
      }, {render: false});
    }
  }

  return {
    before,
    after: dryRun ? before : {
      position: vectorToObject(l3d.camera.position),
      target: vectorToObject(l3d.controls.target),
      first_person_mode: Boolean(l3d.firstPersonMode)
    },
    saved_as_initial: Boolean(op.save_as_initial && !dryRun)
  };
}


function canvasToBase64(canvas, format = "webp", quality = 0.85) {
  const normalized = String(format || "webp").toLowerCase();
  const mime = normalized === "png" ? "image/png" : "image/webp";
  const q = Math.max(0.1, Math.min(1, Number(quality) || 0.85));
  const dataUrl = canvas.toDataURL(mime, q);
  return {
    image_base64: dataUrl.replace(/^data:[^;]+;base64,/, ""),
    mime_type: mime,
    width: canvas.width,
    height: canvas.height
  };
}

let threeModulePromise = null;

async function getThreeModule() {
  if (!threeModulePromise) {
    threeModulePromise = import("/modules/levels-3d-preview/scripts/lib/three.module.js");
  }
  return threeModulePromise;
}

async function capture3dView(scene, op) {
  const l3d = levels3d();
  if (!l3d?._active || !l3d.renderer || !l3d.scene || !l3d.camera || !l3d.controls) {
    throw new Error("3D Canvas is not active or its renderer/camera is unavailable.");
  }

  const THREE3D = await getThreeModule();
  const renderer = l3d.renderer;
  const sourceCanvas = renderer.domElement;
  const width = Math.max(1, Math.min(4096, Number(op.width) || sourceCanvas?.width || 1920));
  const height = Math.max(1, Math.min(4096, Number(op.height) || sourceCanvas?.height || 1080));

  const originalPosition = vectorToObject(l3d.camera.position);
  const originalTarget = vectorToObject(l3d.controls.target);
  const originalRenderTarget = renderer.getRenderTarget();
  const originalSize = renderer.getSize(new THREE3D.Vector2());

  const renderTarget = new THREE3D.WebGLRenderTarget(width, height, {
    format: THREE3D.RGBAFormat,
    type: THREE3D.UnsignedByteType
  });

  try {
    if (op.position) setVector(l3d.camera.position, op.position);
    if (op.target) setVector(l3d.controls.target, op.target);
    if (typeof l3d.controls.update === "function") l3d.controls.update();

    renderer.setSize(width, height, false);
    renderer.setRenderTarget(renderTarget);
    renderer.clear();
    renderer.render(l3d.scene, l3d.camera);

    const pixels = new Uint8Array(4 * width * height);
    renderer.readRenderTargetPixels(renderTarget, 0, 0, width, height, pixels);

    const captureCanvas = document.createElement("canvas");
    captureCanvas.width = width;
    captureCanvas.height = height;
    const ctx = captureCanvas.getContext("2d");
    if (!ctx) throw new Error("Unable to create 2D canvas context for 3D capture.");
    const imageData = ctx.createImageData(width, height);

    for (let y = 0; y < height; y++) {
      const srcRow = (height - 1 - y) * width * 4;
      const destRow = y * width * 4;
      imageData.data.set(pixels.subarray(srcRow, srcRow + width * 4), destRow);
    }
    ctx.putImageData(imageData, 0, 0);

    return {
      ...canvasToBase64(captureCanvas, op.format, op.quality),
      scene_id: scene.id,
      scene_name: scene.name,
      camera: {
        position: vectorToObject(l3d.camera.position),
        target: vectorToObject(l3d.controls.target),
        first_person_mode: Boolean(l3d.firstPersonMode)
      }
    };
  } finally {
    renderer.setRenderTarget(originalRenderTarget);
    renderer.setSize(originalSize.x ?? originalSize.width, originalSize.y ?? originalSize.height, false);
    renderTarget.dispose();

    if (op.restore_camera !== false) {
      setVector(l3d.camera.position, originalPosition);
      setVector(l3d.controls.target, originalTarget);
      if (typeof l3d.controls.update === "function") l3d.controls.update();
    }

    renderer.render(l3d.scene, l3d.camera);
  }
}

async function browseAssetDirectory(path) {
  const FP = getFilePicker();
  if (!FP?.browse) throw new Error("Foundry FilePicker.browse API unavailable.");
  try {
    return await FP.browse("public", path, {extensions: [".glb", ".gltf", ".fbx", ".webp", ".png", ".jpg", ".jpeg", ".exr"]});
  } catch {
    return await FP.browse("data", path, {extensions: [".glb", ".gltf", ".fbx", ".webp", ".png", ".jpg", ".jpeg", ".exr"]});
  }
}

async function search3dAssets(op) {
  const query = String(op.query ?? "").trim().toLowerCase();
  if (!query) throw new Error("search_3d_assets requires a non-empty query.");
  const limit = Math.max(1, Math.min(200, Number(op.limit) || 50));
  const requestedRoots = Array.isArray(op.roots) ? op.roots : [];
  const roots = requestedRoots.length ? requestedRoots : [
    "modules/canvas3dcompendium/assets",
    "modules/levels-3d-preview/assets",
    "modules/canvas3d-premium/assets"
  ];
  const safeRoots = roots.filter(p => /^modules\/[a-z0-9._-]+\/assets(?:\/|$)/i.test(String(p)));
  if (!safeRoots.length) throw new Error("No safe module asset roots supplied.");

  const results = [];
  const queue = safeRoots.map(root => ({path: String(root), depth: 0}));
  const maxDepth = Math.max(0, Math.min(8, Number(op.max_depth) || 5));
  const seen = new Set();

  while (queue.length && results.length < limit) {
    const current = queue.shift();
    if (!current || seen.has(current.path)) continue;
    seen.add(current.path);
    let listing;
    try {
      listing = await browseAssetDirectory(current.path);
    } catch {
      continue;
    }

    for (const file of listing?.files ?? []) {
      const lower = String(file).toLowerCase();
      if (!lower.includes(query)) continue;
      results.push({
        foundry_path: String(file),
        filename: String(file).split("/").pop(),
        module_id: String(file).split("/")[1] ?? null,
        kind: /\.(glb|gltf|fbx)$/i.test(String(file)) ? "model" :
              /\.exr$/i.test(String(file)) ? "environment" : "texture"
      });
      if (results.length >= limit) break;
    }

    if (current.depth < maxDepth) {
      for (const dir of listing?.dirs ?? []) {
        if (String(dir).startsWith(current.path) && !seen.has(String(dir))) {
          queue.push({path: String(dir), depth: current.depth + 1});
        }
      }
    }
  }

  return {query, roots: safeRoots, count: results.length, results};
}


const SCENE_COLLECTION_BY_DOCUMENT = {
  Tile: "tiles",
  AmbientLight: "lights",
  Wall: "walls",
  Region: "regions",
  Drawing: "drawings",
  MeasuredTemplate: "templates",
  Note: "notes",
  Token: "tokens",
  AmbientSound: "sounds"
};

function cloneData(value) {
  if (foundry?.utils?.deepClone) return foundry.utils.deepClone(value);
  return JSON.parse(JSON.stringify(value));
}

function collectionForDocument(scene, document) {
  const key = SCENE_COLLECTION_BY_DOCUMENT[document];
  if (!key) return [];
  const collection = scene?.[key];
  if (!collection) return [];
  return Array.from(collection?.contents ?? collection);
}

function withAcqIdentity(data, identity) {
  const out = cloneData(data ?? {});
  out.flags ??= {};
  out.flags.acq = {
    ...(out.flags.acq ?? {}),
    semantic_id: identity.semantic_id,
    build_id: identity.build_id ?? null,
    provenance: identity.provenance ?? null,
    classification: identity.classification ?? null
  };
  return out;
}

async function applySemanticObjects(scene, op, dryRun = false) {
  const objects = Array.isArray(op.objects) ? op.objects : [];
  if (!objects.length) throw new Error("apply_semantic_objects requires a non-empty objects array.");

  const created = [];
  const updated = [];
  const unchanged = [];

  for (const item of objects) {
    const document = String(item?.document ?? "");
    if (!ALLOWED_EMBEDDED.has(document)) throw new Error(`Semantic object document not allowed: ${document}`);
    const semanticId = String(item?.semantic_id ?? "").trim();
    if (!semanticId) throw new Error("Every semantic object requires semantic_id.");

    const matches = collectionForDocument(scene, document)
      .filter(doc => String(doc?.flags?.acq?.semantic_id ?? "") === semanticId);
    if (matches.length > 1) {
      throw new Error(`Duplicate semantic_id ${semanticId} in ${document}; repair required before idempotent apply.`);
    }

    if (item.delete === true) {
      if (matches.length === 0) {
        unchanged.push({document, semantic_id: semanticId, id: null, deleted: false});
      } else {
        const existing = matches[0];
        if (!dryRun) await scene.deleteEmbeddedDocuments(document, [existing.id]);
        updated.push({document, semantic_id: semanticId, id: existing.id, deleted: true});
      }
      continue;
    }

    const payload = withAcqIdentity(item.data ?? {}, {
      semantic_id: semanticId,
      build_id: item.build_id ?? op.build_id ?? null,
      provenance: item.provenance ?? null,
      classification: item.classification ?? null
    });

    if (matches.length === 0) {
      if (!dryRun) {
        const docs = await scene.createEmbeddedDocuments(document, [payload]);
        created.push({document, semantic_id: semanticId, id: docs?.[0]?.id ?? null});
      } else {
        created.push({document, semantic_id: semanticId, id: null});
      }
      continue;
    }

    const existing = matches[0];
    const update = {_id: existing.id, ...payload};
    if (!dryRun) await scene.updateEmbeddedDocuments(document, [update]);
    updated.push({document, semantic_id: semanticId, id: existing.id});
  }

  return {created, updated, unchanged, count: objects.length};
}


async function deleteSemanticObjects(scene, op, dryRun = false) {
  const semanticIds = Array.isArray(op.semantic_ids) ? op.semantic_ids.map(String) : [];
  if (!semanticIds.length) throw new Error("delete_semantic_objects requires semantic_ids.");

  const wanted = new Set(semanticIds);
  const deleted = [];
  for (const document of ALLOWED_EMBEDDED) {
    const matches = collectionForDocument(scene, document)
      .filter(doc => wanted.has(String(doc?.flags?.acq?.semantic_id ?? "")));
    if (!matches.length) continue;
    const ids = matches.map(doc => doc.id);
    if (!dryRun) await scene.deleteEmbeddedDocuments(document, ids);
    for (const doc of matches) {
      deleted.push({
        document,
        id: doc.id,
        semantic_id: String(doc.flags.acq.semantic_id)
      });
    }
  }

  const found = new Set(deleted.map(x => x.semantic_id));
  const missing = semanticIds.filter(id => !found.has(id));
  return {deleted, missing, count: deleted.length};
}

function semanticInventory(scene) {
  const inventory = [];
  for (const document of ALLOWED_EMBEDDED) {
    for (const doc of collectionForDocument(scene, document)) {
      const semanticId = doc?.flags?.acq?.semantic_id;
      if (!semanticId) continue;
      inventory.push({
        document,
        id: doc.id,
        semantic_id: String(semanticId),
        build_id: doc?.flags?.acq?.build_id ?? null,
        provenance: doc?.flags?.acq?.provenance ?? null,
        classification: doc?.flags?.acq?.classification ?? null
      });
    }
  }
  return inventory;
}

function validateSceneManifest(scene, op) {
  const manifest = op.expected_manifest ?? {};
  const expectedIds = new Set((manifest.semantic_ids ?? []).map(String));
  const inventory = semanticInventory(scene);
  const actualIds = new Set(inventory.map(x => x.semantic_id));
  const missing = [...expectedIds].filter(id => !actualIds.has(id));
  const unexpected = manifest.allow_unexpected === false
    ? [...actualIds].filter(id => !expectedIds.has(id))
    : [];

  const counts = {};
  for (const item of inventory) counts[item.document] = (counts[item.document] ?? 0) + 1;
  const countMismatches = [];
  for (const [document, expected] of Object.entries(manifest.counts ?? {})) {
    const actual = counts[document] ?? 0;
    if (actual !== Number(expected)) countMismatches.push({document, expected: Number(expected), actual});
  }

  return {
    ok: missing.length === 0 && unexpected.length === 0 && countMismatches.length === 0,
    missing,
    unexpected,
    count_mismatches: countMismatches,
    inventory
  };
}

async function applyOperation(scene, op, dryRun = false) {
  if (!op || typeof op !== "object") throw new Error("Operation must be an object.");
  const type = op.op;

  if (type === "snapshot" || type === "ping") return {op: type, ok: true};

  if (type === "inspect_3d_scene") {
    return {op: type, ok: true, ...inspect3dScene(scene)};
  }

  if (type === "set_3d_camera") {
    const camera = await set3dCamera(scene, op, dryRun);
    return {op: type, ok: true, dry_run: dryRun, ...camera};
  }

  if (type === "capture_3d_view") {
    if (dryRun) return {op: type, ok: true, dry_run: true};
    const capture = await capture3dView(scene, op);
    return {op: type, ok: true, ...capture};
  }

  if (type === "search_3d_assets") {
    const search = await search3dAssets(op);
    return {op: type, ok: true, ...search};
  }

  if (type === "apply_semantic_objects") {
    const result = await applySemanticObjects(scene, op, dryRun);
    return {op: type, ok: true, dry_run: dryRun, ...result};
  }

  if (type === "validate_scene_manifest") {
    const result = validateSceneManifest(scene, op);
    return {op: type, ok: true, ...result};
  }

  if (type === "delete_semantic_objects") {
    const result = await deleteSemanticObjects(scene, op, dryRun);
    return {op: type, ok: true, dry_run: dryRun, ...result};
  }

  if (type === "set_3d_environment") {
    const values = op.values ?? {};
    const changes = {};
    for (const [key, value] of Object.entries(values)) {
      if (!ALLOWED_ENV_KEYS.has(key)) throw new Error(`3D environment key not allowed: ${key}`);
      changes[`flags.levels-3d-preview.${key}`] = value;
    }
    if (!dryRun) await scene.update(changes);
    return {op: type, ok: true, changes};
  }

  if (type === "scene_update") {
    const changes = op.changes ?? {};
    const allowedPrefixes = ["flags.", "name", "environment", "darkness", "grid", "background", "foreground", "tokenVision", "fog"];
    for (const key of Object.keys(changes)) {
      if (!allowedPrefixes.some(p => key === p || key.startsWith(p))) {
        throw new Error(`Scene update path not allowed: ${key}`);
      }
    }
    if (!dryRun) await scene.update(changes);
    return {op: type, ok: true, changes};
  }

  if (["embedded_create", "embedded_update", "embedded_delete"].includes(type)) {
    const document = String(op.document ?? "");
    if (!ALLOWED_EMBEDDED.has(document)) throw new Error(`Embedded document type not allowed: ${document}`);

    if (type === "embedded_create") {
      const data = Array.isArray(op.data) ? op.data : [op.data].filter(Boolean);
      if (!dryRun) await scene.createEmbeddedDocuments(document, data);
      return {op: type, document, count: data.length, ok: true};
    }
    if (type === "embedded_update") {
      const updates = Array.isArray(op.updates) ? op.updates : [op.updates].filter(Boolean);
      if (updates.some(u => !u?._id)) throw new Error("Every embedded update requires _id.");
      if (!dryRun) await scene.updateEmbeddedDocuments(document, updates);
      return {op: type, document, count: updates.length, ok: true};
    }
    const ids = Array.isArray(op.ids) ? op.ids : [];
    if (!dryRun) await scene.deleteEmbeddedDocuments(document, ids);
    return {op: type, document, count: ids.length, ok: true};
  }

  if (type === "tile_set_model3d") {
    if (!op.tile_id || !op.foundry_path) throw new Error("tile_set_model3d requires tile_id and foundry_path.");
    const update = {
      _id: op.tile_id,
      "flags.levels-3d-preview.model3d": op.foundry_path,
      "flags.levels-3d-preview.color": op.color ?? "#ffffff"
    };
    if (!dryRun) await scene.updateEmbeddedDocuments("Tile", [update]);
    return {op: type, ok: true, tile_id: op.tile_id, foundry_path: op.foundry_path};
  }

  if (type === "asset_upload") {
    if (!op.file_b64 || !op.filename) throw new Error("asset_upload requires file_b64 and filename.");
    const relativeDir = String(op.relative_dir ?? "assets").replace(/^\/+|\/+$/g, "");
    if (dryRun) return {op: type, ok: true, dry_run: true, filename: op.filename, relative_dir: relativeDir};
    const FP = getFilePicker();
    if (!FP?.uploadPersistent) throw new Error("Foundry FilePicker.uploadPersistent API unavailable.");
    const file = b64ToFile(op.file_b64, op.filename, op.mime_type ?? "application/octet-stream");
    const response = await FP.uploadPersistent(MODULE_ID, relativeDir, file, {}, {notify: false});
    return {op: type, ok: true, upload_response: response};
  }

  throw new Error(`Unsupported operation: ${type}`);
}

async function executeCommand(command) {
  ensureGM();
  const scene = activeScene();
  if (!scene) throw new Error("No active Scene.");
  if (command.protocol_version !== PROTOCOL_VERSION) throw new Error(`Unsupported protocol version ${command.protocol_version}.`);
  if (command.scene_id && command.scene_id !== scene.id) {
    throw new Error(`Command scene_id ${command.scene_id} does not match active Scene ${scene.id}.`);
  }

  const before = await sceneSnapshot(scene);
  if (command.expected_revision && command.expected_revision !== before.revision) {
    throw new Error(`Revision mismatch. Expected ${command.expected_revision}; current ${before.revision}.`);
  }

  const results = [];
  for (const op of command.operations ?? []) results.push(await applyOperation(scene, op, Boolean(command.dry_run)));
  const after = await sceneSnapshot(scene);

  return {
    protocol_version: PROTOCOL_VERSION,
    kind: "command_result",
    command_id: command.command_id,
    completed_at: new Date().toISOString(),
    dry_run: Boolean(command.dry_run),
    ok: true,
    before_revision: before.revision,
    after_revision: after.revision,
    scene_id: scene.id,
    operations: results
  };
}

async function pollCommand() {
  if (inFlight || !game.user?.isGM) return;
  const scene = activeScene();
  if (!scene) return;
  inFlight = true;
  try {
    const qs = new URLSearchParams({world_id: game.world?.id ?? "", scene_id: scene.id});
    const response = await request(`/bridge/next?${qs.toString()}`, {method: "GET"});
    if (response.status === 204) return;
    if (!response.ok) throw new Error(`Agent returned HTTP ${response.status}`);
    const command = await response.json();

    let result;
    try {
      result = await executeCommand(command);
    } catch (err) {
      const snap = await sceneSnapshot(scene);
      result = {
        protocol_version: PROTOCOL_VERSION,
        kind: "command_result",
        command_id: command.command_id,
        completed_at: new Date().toISOString(),
        ok: false,
        error: String(err?.stack ?? err),
        current_revision: snap?.revision ?? null,
        scene_id: scene.id
      };
      console.error(`${MODULE_ID} command failed`, err);
      ui.notifications?.error(`Acq Bridge command failed: ${err.message ?? err}`);
    }

    await request("/bridge/result", {method: "POST", body: JSON.stringify(result)});
    await postState("command-complete");
  } catch (err) {
    console.debug(`${MODULE_ID} poll failed`, err);
  } finally {
    inFlight = false;
  }
}

function startPolling() {
  clearInterval(pollTimer);
  const interval = Math.max(500, Number(game.settings.get(MODULE_ID, "pollMs") || 1000));
  pollTimer = setInterval(pollCommand, interval);
  postState("bridge-start");
}

Hooks.once("init", () => {
  game.settings.register(MODULE_ID, "enabled", {
    name: "Enable local bridge",
    hint: "Connect this GM client to the local Acq Bridge Agent.",
    scope: "client", config: true, type: Boolean, default: true
  });
  game.settings.register(MODULE_ID, "agentUrl", {
    name: "Bridge Agent URL",
    hint: "Loopback URL for the local bridge agent.",
    scope: "client", config: true, type: String, default: "http://127.0.0.1:18747"
  });
  game.settings.register(MODULE_ID, "pollMs", {
    name: "Command polling interval (ms)",
    hint: "How often the active GM checks for bridge commands.",
    scope: "client", config: true, type: Number, default: 1000
  });
});

Hooks.once("ready", () => {
  globalThis.AcqFoundryBridge = {snapshot: sceneSnapshot, postState, executeCommand};
  if (!game.user?.isGM || !game.settings.get(MODULE_ID, "enabled")) return;
  startPolling();

  Hooks.on("canvasReady", () => scheduleSnapshot("canvas-ready"));
  Hooks.on("updateScene", () => scheduleSnapshot("scene-update"));
  for (const hook of [
    "createTile", "updateTile", "deleteTile",
    "createAmbientLight", "updateAmbientLight", "deleteAmbientLight",
    "createWall", "updateWall", "deleteWall",
    "createRegion", "updateRegion", "deleteRegion"
  ]) Hooks.on(hook, () => scheduleSnapshot(hook));
});
