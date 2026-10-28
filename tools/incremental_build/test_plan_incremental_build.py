import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from plan_incremental_build import plan


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        for name in ['wall.src', 'prop.src', 'wall.glb', 'prop.glb', 'assembly.json', 'qa.json']:
            (self.root / name).write_text(name)
        self.manifest = {'schema_version': 1, 'project_id': 'fixture', 'stages': [
            {'id': 'wall', 'recipe': {'generator': 'v1'}, 'inputs': [self.input('wall.src')], 'outputs': ['wall.glb']},
            {'id': 'prop', 'recipe': {'generator': 'v1'}, 'inputs': [self.input('prop.src')], 'outputs': ['prop.glb']},
            {'id': 'assembly', 'recipe': {'adapter': 'v1'}, 'depends_on': ['wall', 'prop'], 'outputs': ['assembly.json']},
            {'id': 'qa', 'recipe': {'test': 'v1', 'light': 'source'}, 'depends_on': ['assembly'], 'outputs': ['qa.json']}]}
        first = plan(self.manifest, {}, self.root)
        self.cache = {'schema_version': 1, 'project_id': 'fixture', 'stages': {s['id']: {'completed': True, 'fingerprint': s['fingerprint'], 'outputs': [self.input(p) for p in s['outputs']]} for s in first['stages']}}

    def input(self, name):
        return {'path': name, 'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest()}

    def actions(self):
        return {s['id']: s['action'] for s in plan(self.manifest, self.cache, self.root)['stages']}

    def test_unchanged_outputs_reused_without_quality_pass(self):
        result = plan(self.manifest, self.cache, self.root)
        self.assertEqual(result['counts']['REUSE'], 4); self.assertIn('UNVERIFIED', result['quality_gates'])

    def test_changed_source_rebuilds_only_dependents(self):
        (self.root / 'wall.src').write_text('new wall'); self.manifest['stages'][0]['inputs'] = [self.input('wall.src')]
        self.assertEqual(self.actions(), {'wall': 'RUN', 'prop': 'REUSE', 'assembly': 'RUN', 'qa': 'RUN'})

    def test_unapproved_source_hash_change_blocks(self):
        (self.root / 'wall.src').write_text('unexpected change')
        self.assertEqual(self.actions(), {'wall': 'BLOCKED', 'prop': 'REUSE', 'assembly': 'BLOCKED', 'qa': 'BLOCKED'})

    def test_changed_output_rebuilds_downstream(self):
        (self.root / 'wall.glb').write_text('tampered output')
        self.assertEqual(self.actions(), {'wall': 'RUN', 'prop': 'REUSE', 'assembly': 'RUN', 'qa': 'RUN'})

    def test_missing_output_rebuilds_downstream(self):
        (self.root / 'wall.glb').unlink()
        self.assertEqual(self.actions()['qa'], 'RUN')

    def test_only_qa_recipe_change_does_not_reexport(self):
        self.manifest['stages'][3]['recipe']['light'] = 'changed light'
        self.assertEqual(self.actions(), {'wall': 'REUSE', 'prop': 'REUSE', 'assembly': 'REUSE', 'qa': 'RUN'})

    def test_previous_other_location_is_not_reused(self):
        self.cache['project_id'] = 'other-location'; self.assertEqual(set(self.actions().values()), {'RUN'})

    def test_dependency_cycle_rejected(self):
        self.manifest['stages'][0]['depends_on'] = ['qa']
        with self.assertRaises(ValueError): self.actions()

    def test_unpinned_input_rejected(self):
        del self.manifest['stages'][0]['inputs'][0]['sha256']
        with self.assertRaises(ValueError): self.actions()

    def test_tool_version_invalidates_dependent_outputs(self):
        self.manifest['stages'][0]['recipe']['generator'] = 'v2'
        self.assertEqual(self.actions()['prop'], 'REUSE'); self.assertEqual(self.actions()['qa'], 'RUN')

    def test_new_upstream_output_invalidates_old_downstream_cache(self):
        (self.root / 'wall.glb').write_text('accepted regenerated output')
        self.cache['stages']['wall']['outputs'] = [self.input('wall.glb')]
        self.assertEqual(self.actions(), {'wall': 'REUSE', 'prop': 'REUSE', 'assembly': 'RUN', 'qa': 'RUN'})

    def test_two_stages_cannot_own_same_output(self):
        self.manifest['stages'][1]['outputs'] = ['wall.glb']
        with self.assertRaises(ValueError): self.actions()

    def test_completion_string_is_not_success(self):
        self.cache['stages']['wall']['completed'] = 'false'
        self.assertEqual(self.actions()['wall'], 'RUN')

    def test_malformed_previous_stage_rejected(self):
        self.cache['stages']['wall'] = 'completed'
        with self.assertRaises(ValueError): self.actions()


if __name__ == '__main__':
    unittest.main()
