"""Read-only declared-dependency plan; does not execute builds or grant quality PASS."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def plan(manifest, previous, root):
    if not isinstance(manifest, dict) or not isinstance(previous, dict): raise ValueError('Manifest and previous cache must be objects')
    if manifest.get('schema_version') != 1 or not isinstance(manifest.get('project_id'), str) or not manifest['project_id']:
        raise ValueError('schema_version1 and nonempty project_id required')
    stages = manifest.get('stages'); context = manifest.get('context', {})
    if not isinstance(stages, list) or not stages or not isinstance(context, dict):
        raise ValueError('Nonempty stages list and object context required')
    by_id = {}; ordered = []; visiting = set(); visited = set()
    for stage in stages:
        if not isinstance(stage, dict): raise ValueError('Each stage must be an object')
        key = stage.get('id')
        if not isinstance(key, str) or not key or key in by_id: raise ValueError('Stage IDs must be nonempty and unique')
        if not isinstance(stage.get('recipe'), dict): raise ValueError('Every stage needs an explicit recipe object')
        if not isinstance(stage.get('inputs', []), list) or not isinstance(stage.get('depends_on', []), list):
            raise ValueError('inputs and depends_on must be lists')
        outputs = stage.get('outputs')
        if not isinstance(outputs, list) or not outputs or not all(isinstance(p, str) and p for p in outputs) or len(outputs) != len(set(outputs)):
            raise ValueError('Every stage needs unique nonempty output paths')
        by_id[key] = stage

    def visit(key):
        if key not in by_id: raise ValueError('Unknown stage dependency: ' + str(key))
        if key in visiting: raise ValueError('Cycle in stage dependencies')
        if key in visited: return
        visiting.add(key)
        for dependency in by_id[key].get('depends_on', []): visit(dependency)
        visiting.remove(key); visited.add(key); ordered.append(key)

    for key in by_id: visit(key)
    root = Path(root).resolve(); scanned = {}; producers = {}
    for stage in stages:
        for path in stage['outputs']:
            p = Path(path); p = (p if p.is_absolute() else root / p).resolve()
            if p in producers: raise ValueError('Output has multiple producers: ' + path)
            producers[p] = stage['id']

    def digest(path):
        p = Path(path); p = p if p.is_absolute() else root / p; p = p.resolve()
        before = p.stat(); stamp = (before.st_size, before.st_mtime_ns)
        if p in scanned:
            if scanned[p][0] != stamp: raise ValueError('File changed during planning: ' + str(path))
            return scanned[p][1]
        h = hashlib.sha256()
        with p.open('rb') as f:
            for block in iter(lambda: f.read(1024 * 1024), b''): h.update(block)
        after = p.stat()
        if stamp != (after.st_size, after.st_mtime_ns): raise ValueError('File changed while hashing: ' + str(path))
        scanned[p] = (stamp, h.hexdigest()); return h.hexdigest()

    cache_compatible = previous.get('schema_version') == 1 and previous.get('project_id') == manifest['project_id']
    records = previous.get('stages', {}) if cache_compatible else {}
    if not isinstance(records, dict): raise ValueError('Previous stages must be keyed records')
    results = {}
    for key in ordered:
        stage = by_id[key]; reasons = []; blocked = False; observed = []
        deps = {dep: {'fingerprint': results[dep]['fingerprint'], 'outputs': results[dep]['outputs_observed']} for dep in stage.get('depends_on', [])}
        if any(results[d]['action'] == 'BLOCKED' for d in deps): blocked = True; reasons.append('upstream_blocked')
        for item in stage.get('inputs', []):
            if not isinstance(item, dict) or not isinstance(item.get('path'), str) or not item['path'] or not re.fullmatch('[0-9a-f]{64}', str(item.get('sha256', ''))):
                raise ValueError('Every input requires path and pinned lowercase SHA256')
            try:
                actual = digest(item['path']); observed.append({'path': item['path'].replace('\\', '/'), 'sha256': actual})
                if actual != item['sha256']: blocked = True; reasons.append('input_hash_mismatch:' + item['path'])
            except (OSError, ValueError) as error:
                blocked = True; reasons.append('input_unavailable:' + item['path'] + ':' + str(error))
        fingerprint = hashlib.sha256(canonical({'context': context, 'stage': key, 'recipe': stage['recipe'], 'inputs': observed, 'dependencies': deps, 'outputs': stage['outputs']})).hexdigest()
        old = records.get(key, {}); action = 'RUN'
        if not isinstance(old, dict): raise ValueError('Previous stage record must be an object')
        if blocked: action = 'BLOCKED'
        elif any(results[d]['action'] != 'REUSE' for d in deps): reasons.append('upstream_requires_run')
        elif old.get('completed') is not True: reasons.append('no_completed_record')
        elif old.get('fingerprint') != fingerprint: reasons.append('declared_inputs_recipe_or_dependencies_changed')
        else:
            outputs = old.get('outputs', [])
            if not isinstance(outputs, list) or not all(isinstance(o, dict) for o in outputs):
                raise ValueError('Previous outputs must be path/hash records')
            output_map = {o.get('path'): o.get('sha256') for o in outputs}
            if len(output_map) != len(outputs) or set(output_map) != set(stage['outputs']): reasons.append('output_set_changed')
            else:
                for path, expected in output_map.items():
                    try:
                        if digest(path) != expected: reasons.append('output_hash_changed:' + path)
                    except (OSError, ValueError): reasons.append('output_missing_or_changed:' + path)
                if not reasons: action = 'REUSE'; reasons.append('same_declared_inputs_recipe_dependencies_and_output_hashes')
        output_observed = []
        for path in stage['outputs']:
            try: output_observed.append({'path': path, 'sha256': digest(path)})
            except (OSError, ValueError): output_observed.append({'path': path, 'sha256': None})
        results[key] = {'id': key, 'action': action, 'fingerprint': fingerprint, 'reasons': reasons, 'inputs_observed': observed, 'outputs': stage['outputs'], 'outputs_observed': output_observed}
    counts = {action: sum(r['action'] == action for r in results.values()) for action in ['REUSE', 'RUN', 'BLOCKED']}
    return {'schema_version': 1, 'project_id': manifest['project_id'], 'scope': 'Declared dependency plan only; no build execution or quality certification',
            'quality_gates': 'UNVERIFIED; interpret actual source/art/structure/native/DM evidence separately',
            'cache_project_matches': cache_compatible, 'counts': counts, 'stages': [results[k] for k in ordered]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--previous', type=Path)
    parser.add_argument('--root', type=Path, help='Explicit input/output root; defaults to manifest parent')
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
        previous = json.loads(args.previous.read_text(encoding='utf-8-sig')) if args.previous else {}
        report = plan(manifest, previous, args.root or args.manifest.parent)
        print(json.dumps(report, indent=2, allow_nan=False)); return 2 if report['counts']['BLOCKED'] else 0
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(json.dumps({'error': str(error), 'scope': 'No build execution or quality certification'})); return 2


if __name__ == '__main__':
    raise SystemExit(main())
