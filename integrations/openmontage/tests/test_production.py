"""Model-free input guards; no upstream install, network or model needed."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/production.py'


def example():
    return {
        'brief': {'target_duration_seconds': 4, 'target_platform': 'youtube', 'metadata': {
            'language': 'en', 'render_runtime': 'remotion', 'fixture': True,
            'music_plan': {'source': 'none', 'opt_out_reason': 'fixture excludes music'},
            'end_tag_plan': None, 'end_tag_opt_out_reason': 'fixture excludes end-tag'}},
        'scene_plan': {'scenes': [
            {'id': 'one', 'type': 'broll', 'start_seconds': 0, 'end_seconds': 2},
            {'id': 'two', 'type': 'broll', 'start_seconds': 2, 'end_seconds': 4}]},
        'asset_manifest': {'assets': [
            {'id': 'a', 'type': 'video', 'path': 'assets/a.mp4', 'scene_id': 'one', 'provider': 'lavfi-fixture', 'license': 'generated fixture', 'original_url': 'fixture:lavfi/testsrc2', 'cost_usd': 0},
            {'id': 'b', 'type': 'video', 'path': 'assets/b.mp4', 'scene_id': 'two', 'provider': 'lavfi-fixture', 'license': 'generated fixture', 'original_url': 'fixture:lavfi/testsrc2', 'cost_usd': 0},
            {'id': 'voice', 'type': 'narration', 'path': 'assets/tone.wav', 'scene_id': 'all', 'provider': 'lavfi-fixture', 'license': 'generated fixture', 'original_url': 'fixture:lavfi/sine', 'cost_usd': 0}],
            'metadata': {'fixture': True, 'provenance': {}, 'narration': {
                'asset_id': 'voice', 'character': 'urfavxbf', 'voice_id': 'fixture-tone-not-speech',
                'language': 'en', 'audio_sha256': 'pending', 'alignment_review': 'fixture labels, not speech',
                'segments': [{'words': [{'word': 'FIXTURE', 'start': 0.1, 'end': 1.5}, {'word': 'NOT SPEECH', 'start': 2.1, 'end': 3.5}]}]}}},
        'edit_decisions': {'render_runtime': 'remotion', 'renderer_family': 'documentary-montage',
            'cuts': [{'id': 'one', 'source': 'a', 'in_seconds': 0, 'out_seconds': 2, 'transition_in': 'cut', 'transition_out': 'cut'},
                     {'id': 'two', 'source': 'b', 'in_seconds': 0, 'out_seconds': 2, 'transition_in': 'cut', 'transition_out': 'cut'}]}}


class ProductionGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('openmontage_production', SCRIPT)
        cls.p = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.p)

    def setUp(self):
        self.data = example()

    def test_fixture_plan_is_explicit_and_production_rejects_it(self):
        self.assertEqual(self.p.validate_plan(self.data, fixture=True), 4)
        with self.assertRaisesRegex(ValueError, 'fixture'):
            self.p.validate_plan(self.data)

    def test_voice_identity_and_language_cannot_be_substituted(self):
        data = self.data
        data['brief']['metadata']['fixture'] = False
        data['asset_manifest']['metadata']['fixture'] = False
        narration = data['asset_manifest']['metadata']['narration']
        narration['voice_id'] = 'natural-storyteller-v1'
        self.assertEqual(self.p.validate_plan(data), 4)
        for field, value in (('voice_id', 'piper'), ('language', 'tl'), ('character', 'pix')):
            bad = copy.deepcopy(data)
            bad['asset_manifest']['metadata']['narration'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.p.validate_plan(bad)

    def test_runtime_music_end_tag_and_unsupported_edits_fail_closed(self):
        edits = [
            ('render_runtime', 'ffmpeg'), ('composition_mode', 'atelier'),
            ('overlays', [{'asset_id': 'a'}]), ('audio', {'music': {'asset_id': 'a'}}),
            ('music', {'asset_id': 'a'}), ('transitions', [{'type': 'wipe'}]),
            ('subtitles', {'enabled': False}), ('subtitles', {'font_size': 120}),
        ]
        for key, value in edits:
            bad = copy.deepcopy(self.data)
            bad['edit_decisions'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.p.validate_plan(bad, fixture=True)
        for key, value in [('music_plan', {'source': 'generated'}), ('end_tag_plan', {'text': 'THE END'})]:
            bad = copy.deepcopy(self.data)
            bad['brief']['metadata'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.p.validate_plan(bad, fixture=True)

    def test_cut_speed_transforms_transitions_and_bounds_are_not_ignored(self):
        for key, value in [('speed', 2), ('transform', {'scale': 2}), ('transition_in', 'wipe'),
                           ('out_seconds', -1), ('in_seconds', float('nan')), ('backgroundColor', '#ff0000')]:
            bad = copy.deepcopy(self.data)
            bad['edit_decisions']['cuts'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.p.validate_plan(bad, fixture=True)

    def test_timing_must_be_finite_ordered_and_match_scenes(self):
        for value in (True, float('inf'), float('nan'), -1, 181, '4'):
            bad = copy.deepcopy(self.data)
            bad['brief']['target_duration_seconds'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.p.validate_plan(bad, fixture=True)
        self.data['scene_plan']['scenes'][1]['start_seconds'] = 3
        with self.assertRaises(ValueError):
            self.p.validate_plan(self.data, fixture=True)

    def test_caption_words_cannot_overlap_or_outlast_audio(self):
        for word in ({'word': '', 'start': 0, 'end': 1}, {'word': 'bad', 'start': 0, 'end': 5},
                     {'word': 'bad', 'start': 3, 'end': 2}, {'word': 'bad', 'start': 0.2, 'end': 0.3}):
            bad = copy.deepcopy(self.data)
            bad['asset_manifest']['metadata']['narration']['segments'][0]['words'][1] = word
            with self.subTest(word=word), self.assertRaises(ValueError):
                self.p.validate_plan(bad, fixture=True)

    def test_paths_reject_escape_absolute_and_symlink_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / 'project'
            base.mkdir()
            self.assertEqual(self.p.safe_path(base, 'assets/a.mp4'), base / 'assets/a.mp4')
            (base / 'renders').symlink_to(Path(tmp), target_is_directory=True)
            for path in ('../outside', '/etc/passwd', 'renders/final.mp4', 'assets/../../outside', 'https://example.com/a'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    self.p.safe_path(base, path)

    def test_changed_or_unapproved_snapshots_cannot_render(self):
        stages = [{'name': stage, 'produces': [name], 'human_approval_default': True}
                  for stage, name in [('idea', 'brief'), ('scene_plan', 'scene_plan'), ('assets', 'asset_manifest'), ('edit', 'edit_decisions')]]
        checkpoints = {s['name']: {'status': 'completed', 'human_approved': True,
            'pipeline_type': 'documentary-montage', 'artifacts': {s['produces'][0]: copy.deepcopy(self.data[s['produces'][0]])}}
            for s in stages}
        for stage in stages:
            checkpoints[stage['name']]['metadata'] = {'prerequisites': self.p.gate_context(stages, stage['name'], checkpoints)}
        self.p.require_approvals(stages, checkpoints, self.data)
        for key, value in [('human_approved', False), ('status', 'awaiting_human'), ('pipeline_type', 'hybrid')]:
            bad = copy.deepcopy(checkpoints)
            bad['assets'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.p.require_approvals(stages, bad, self.data)
        self.data['brief']['title'] = 'changed after approval'
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.p.require_approvals(stages, checkpoints, self.data)
        checkpoints['idea']['artifacts']['brief'] = copy.deepcopy(self.data['brief'])
        with self.assertRaisesRegex(ValueError, 'prerequisite'):
            self.p.require_approvals(stages, checkpoints, self.data)

    def test_checkpoint_temp_history_and_dangling_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / 'runtime'
            project = runtime / 'projects/test'
            project.mkdir(parents=True)
            for name in ('checkpoint_idea.json.tmp', 'history/checkpoint_idea_previous.json', 'project.json'):
                path = project / name
                path.parent.mkdir(exist_ok=True)
                path.symlink_to(Path(tmp) / 'outside-even-if-missing')
                with self.subTest(path=name), self.assertRaisesRegex(ValueError, 'symlink'):
                    self.p.project_path(runtime, 'test')
                path.unlink()

    def test_transport_keeps_explicit_hard_cuts_captions_and_no_audio_fade(self):
        edit = self.data['edit_decisions']
        del edit['cuts'][0]['transition_in']
        del edit['cuts'][0]['transition_out']
        narration = self.data['asset_manifest']['metadata']['narration']
        paths = {'a': Path('/local/a.mp4'), 'b': Path('/local/b.mp4')}
        props = self.p.transport_edit(edit, paths, narration, Path('/local/captions.srt'), 4)
        self.assertEqual(props['cuts'][0]['transition_in'], 'cut')
        self.assertEqual(props['cuts'][0]['transition_out'], 'cut')
        self.assertEqual(props['captions']['words'][0]['startMs'], 100)
        self.assertNotIn('soundtrack', props)  # Audio goes through the unfaded upstream mux.
        self.assertNotIn('transition_in', edit['cuts'][0])

    def test_revision_or_unknown_qa_never_completes_a_run(self):
        self.assertEqual(self.p.review_checkpoint_status({'operation': 'remotion_render', 'final_review': {'status': 'pass'}}), 'completed')
        self.assertEqual(self.p.review_checkpoint_status({'operation': 'remotion_render', 'final_review': {'status': 'revise'}}), 'awaiting_human')
        for data in ({'operation': 'compose', 'final_review': {'status': 'pass'}},
                     {'operation': 'remotion_render', 'final_review': {'status': 'fail'}}, {}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.p.review_checkpoint_status(data)

    def test_media_hashes_rights_source_bounds_and_actual_wav_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.data['asset_manifest']
            for asset in manifest['assets']:
                path = root / asset['path']
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(asset['id'].encode())
                manifest['metadata']['provenance'][asset['id']] = {
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'rights_review': 'fixture generation recipe', 'reviewed_by': 'test'}
            manifest['metadata']['narration']['audio_sha256'] = manifest['metadata']['provenance']['voice']['sha256']
            def probe(path):
                return {'format': {'duration': '4'}, 'streams': [
                    {'codec_type': 'audio'} if path.suffix == '.wav' else {'codec_type': 'video', 'width': 640, 'height': 360}]}
            self.p.validate_media(root, self.data, fixture=True, probe=probe)
            bad = copy.deepcopy(self.data)
            bad['asset_manifest']['metadata']['narration']['segments'][0]['words'][-1]['end'] = 4
            def short_audio(path):
                info = probe(path)
                if path.suffix == '.wav':
                    info['format']['duration'] = '3.96'
                return info
            with self.assertRaisesRegex(ValueError, 'audio duration'):
                self.p.validate_media(root, bad, fixture=True, probe=short_audio)
            manifest['metadata']['provenance']['a']['rights_review'] = ''
            with self.assertRaisesRegex(ValueError, 'rights'):
                self.p.validate_media(root, self.data, fixture=True, probe=probe)
            manifest['metadata']['provenance']['a']['rights_review'] = 'reviewed'
            (root / 'assets/a.mp4').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash'):
                self.p.validate_media(root, self.data, fixture=True, probe=probe)


if __name__ == '__main__':
    unittest.main()
