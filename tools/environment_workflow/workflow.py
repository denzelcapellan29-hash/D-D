"""Rebuild a NEW technical bundle, or audit its evidence without app mutations.

External reviews attest to one exact bundle digest. They are never synthesized
from file existence, test counts, a Tile report, or this example's geometry.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
import architecture as engine

GATES = ('SOURCE', 'ART', 'NATIVE', 'PERFORMANCE', 'DM_ACCEPTED')
CODE = ('architecture.py', 'export_blender.py', 'workflow.py')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in sorted(root.rglob('*'))
            if p.is_file() and p.relative_to(root).parts[0] != 'evidence'
            and p.name != 'release.json'}

def local_file(root, relative):
    p = (root / relative).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError('Evidence/assets must stay inside the bundle')
    return p

def audit(root):
    root = Path(root).resolve(); failures = []; gates = {}
    def fail(message): failures.append(message)
    try:
        s = json.loads((root/'source.json').read_text()); a = json.loads((root/'export/assembly.json').read_text())
        manifest = json.loads((root/'export/manifest.json').read_text())
        qa = json.loads((root/'export/export_qa.json').read_text())
        contract = engine.check_assembly(s, a)
        gates['STRUCTURE'] = 'PASS' if contract['ok'] else 'FAIL'
        if not contract['ok']: fail('Assembly contract fails')
        # Reproducibility is scoped to semantic geometry, not Blender file bytes.
        recipe = json.loads((root/'recipe.json').read_text())
        for name in CODE:
            if sha(Path(__file__).parent/name) != recipe['code'][name]: fail('Recipe changed: '+name)
        if a['spec_sha256'] != engine.digest(s) or manifest['spec_sha256'] != engine.digest(s): fail('Stale source fingerprint')
        if a['generator_sha256'] != recipe['code']['architecture.py'] or manifest['generator_sha256'] != recipe['code']['architecture.py']: fail('Stale generator fingerprint')
        if manifest['adapter_sha256'] != recipe['code']['export_blender.py']: fail('Stale exporter fingerprint')
        if not qa['ok'] or not qa['families'] or not all(f['ok'] for f in qa['families']): fail('Export checks fail')
        expected = {p['id']:p for p in a['parts']}; actual = {p['id']:p for p in manifest['parts']}
        if len(actual) != len(manifest['parts']) or set(actual) != set(expected): fail('Placement inventory differs')
        for id, p in actual.items():
            if id in expected and (p['bounds'] != expected[id]['bounds'] or p['role'] != expected[id]['role']): fail('Placement differs: '+id)
        for asset in manifest['families']:
            if sha(local_file(root/'export',asset['file'])) != asset['sha256']: fail('Asset changed: '+asset['file'])
        for p in manifest['parts']:
            if sha(local_file(root/'export',p['asset'])) != p['asset_sha256']: fail('Placement asset changed: '+p['id'])
        gates['GLB'] = 'PASS' if not failures else 'FAIL'
    except (OSError, ValueError, KeyError, TypeError) as exc:
        fail('Incomplete or invalid bundle: '+str(exc)); s = {'features':[]}
        gates.setdefault('STRUCTURE','UNVERIFIED'); gates['GLB']='UNVERIFIED'
    fingerprint = engine.digest(inventory(root))
    try: evidence = json.loads((root/'evidence/reviews.json').read_text())
    except (OSError,ValueError): evidence = {}
    for gate in GATES:
        record = evidence.get(gate, {}); ok = record.get('status')=='PASS' and record.get('bundle_sha256')==fingerprint
        ok = ok and bool(record.get('reviewer')) and bool(record.get('basis')) and bool(record.get('artifacts'))
        try:
            for artifact in record.get('artifacts',[]):
                ok = ok and artifact['sha256']==sha(local_file(root,artifact['path']))
        except (ValueError,OSError,KeyError,TypeError): ok=False
        if gate=='NATIVE':
            required = {'rendered_controls','forward_return','stairs_support','closed_blocking','pit_explore_recovery','secret_reveal_restore','reload','native_features'}
            ok = ok and bool(record.get('scene_revision')) and required <= set(record.get('checks',[]))
            ok = ok and {f['id'] for f in s.get('features',[])} <= set(record.get('features_verified',[]))
        if gate=='PERFORMANCE':
            fields = {'viewport_px','render_scale','quality','visibility','lighting','hardware','route','warmup','baseline_revision','candidate_revision','moving_frame_ms','stationary_frame_ms','quality_parity','accepted_target'}
            ok = ok and fields <= set(record.get('measurement',{}))
            ok = ok and record.get('measurement',{}).get('quality_parity') is True
        if gate=='DM_ACCEPTED': ok = ok and record.get('reviewer_role')=='DM'
        gates[gate] = 'PASS' if ok else 'UNVERIFIED'
    ready = not failures and all(v=='PASS'for v in gates.values())
    result = {'ready_for_play':ready,'bundle_sha256':fingerprint,'gates':gates,'failures':failures,
              'scope':'Reference rectilinear contract. External source/art/native/performance/DM reviews require current, inspected evidence; declarations are attestations, not automated runtime proof.'}
    (root/'release.json').write_text(json.dumps(result,indent=2)); return result

def build(spec, output, blender):
    out=Path(output).resolve()
    if out.exists(): raise ValueError('Choose a new revision directory; existing bundles are never overwritten')
    s=json.loads(Path(spec).read_text()); a=engine.compile_plan(s); qa=engine.check_assembly(s,a)
    if not qa['ok']: raise ValueError('Structural contract failed before export')
    out.mkdir(parents=True); (out/'source.json').write_text(json.dumps(s,indent=2))
    recipe={'schema_version':1,'code':{name:sha(Path(__file__).parent/name) for name in CODE},'spec_sha256':engine.digest(s),'blender':str(Path(blender).resolve()),'scope':'technical reference; no native writes'}
    (out/'recipe.json').write_text(json.dumps(recipe,indent=2)); (out/'evidence').mkdir()
    (out/'evidence/reviews.json').write_text('{}\n')
    with (out/'blender.log').open('w',encoding='utf-8') as log:
        subprocess.run([str(blender),'--background','--python',str(Path(__file__).parent/'export_blender.py'),'--','--spec',str(out/'source.json'),'--out',str(out/'export')],check=True,stdout=log,stderr=subprocess.STDOUT)
    return audit(out)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='command',required=True)
    b=sub.add_parser('build');b.add_argument('--spec',required=True);b.add_argument('--out',required=True);b.add_argument('--blender',required=True)
    r=sub.add_parser('audit');r.add_argument('bundle');args=parser.parse_args()
    result=build(args.spec,args.out,args.blender)if args.command=='build'else audit(args.bundle)
    print(json.dumps(result,indent=2))
    # Build success is distinct from play-ready acceptance; audit returns 2 for holds.
    if args.command=='audit' and not result['ready_for_play']: raise SystemExit(2)
