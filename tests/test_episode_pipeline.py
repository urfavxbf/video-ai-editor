"""Filesystem contract tests for the CPU-only durable stage runner."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).parents[1] / 'scripts/episode_pipeline.py'
spec = importlib.util.spec_from_file_location('episode_pipeline', SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class StageRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'run'
        self.runner = m.StageRunner(self.root)
        self.calls = 0

    def action(self, directory):
        self.calls += 1
        (directory / 'nested').mkdir()
        (directory / 'nested/proof.txt').write_bytes(b'actual evidence\n')
        return {'verified': True, 'frames': 30}

    def run_stage(self, version='1', inputs=None, action=None):
        return self.runner.run('verify-audio', version, inputs or {'sourceHash': 'abc'}, action or self.action)

    def test_resume_rehashes_outputs_and_skips_action(self):
        first = self.run_stage()
        second = m.StageRunner(self.root).run('verify-audio', '1', {'sourceHash': 'abc'}, self.action)
        self.assertEqual(self.calls, 1)
        self.assertFalse(first['cached'])
        self.assertTrue(second['cached'])
        self.assertEqual(first['resultHash'], second['resultHash'])
        self.assertEqual(first['payload'], {'verified': True, 'frames': 30})
        self.assertEqual(second['status'], 'completed')
        self.assertTrue(Path(second['directory']).is_absolute())
        self.assertEqual(second['outputs'], [{
            'path': 'nested/proof.txt', 'size': 16,
            'sha256': hashlib.sha256(b'actual evidence\n').hexdigest(),
        }])

    def test_mutation_missing_and_extra_output_each_invalidate_cache(self):
        result = self.run_stage()
        directory = Path(result['directory'])
        (directory / 'nested/proof.txt').write_text('tampered')
        self.assertFalse(self.run_stage()['cached'])
        (directory / 'nested/proof.txt').unlink()
        self.assertFalse(self.run_stage()['cached'])
        (directory / 'unrecorded.txt').write_text('unrecorded')
        self.assertFalse(self.run_stage()['cached'])
        self.assertEqual(self.calls, 4)
        self.assertFalse((directory / 'unrecorded.txt').exists())

    def test_version_and_input_changes_invalidate_cache(self):
        first = self.run_stage()
        version = self.run_stage(version='2')
        inputs = self.run_stage(version='2', inputs={'sourceHash': 'def'})
        self.assertEqual(self.calls, 3)
        self.assertEqual(len({r['resultHash'] for r in [first, version, inputs]}), 3)
        self.assertEqual(inputs['version'], '2')
        self.assertNotEqual(first['inputHash'], inputs['inputHash'])

    def test_failed_attempt_is_explicitly_retryable_and_redacted(self):
        secret = 'token=secret https://private.example/voice?q=private-dialogue'
        def fail(directory):
            (directory / 'partial.txt').write_text('partial')
            raise RuntimeError(secret)
        with self.assertRaises(m.StageError) as caught:
            self.run_stage(action=fail)
        self.assertEqual(caught.exception.error['stage'], 'verify-audio')
        self.assertEqual(caught.exception.error['code'], 'action_failed')
        self.assertTrue(caught.exception.error['retryable'])
        self.assertNotIn(secret, str(caught.exception))
        state = m.read_json(self.root / 'state.json')
        self.assertEqual(state['attempts']['verify-audio']['status'], 'failed')
        self.assertNotIn('private', json.dumps(state))
        self.assertNotIn('verify-audio', state['stages'])
        self.assertFalse(self.run_stage()['cached'])

    def test_failed_new_version_preserves_valid_previous_completion(self):
        first = self.run_stage()
        def fail(_directory):
            raise RuntimeError('failure')
        with self.assertRaises(m.StageError):
            self.run_stage(version='2', action=fail)
        self.assertTrue((Path(first['directory']) / 'nested/proof.txt').is_file())
        resumed = self.run_stage()
        self.assertTrue(resumed['cached'])
        self.assertEqual(resumed['resultHash'], first['resultHash'])

    def test_keyboard_interrupt_is_persisted_and_reraises(self):
        def cancel(directory):
            (directory / 'partial.txt').write_text('unfinished')
            raise KeyboardInterrupt()
        with self.assertRaises(KeyboardInterrupt):
            self.run_stage(action=cancel)
        state = m.read_json(self.root / 'state.json')
        attempt = state['attempts']['verify-audio']
        self.assertEqual(attempt['status'], 'cancelled')
        self.assertEqual(attempt['error']['code'], 'cancelled')
        self.assertTrue(attempt['error']['retryable'])
        self.assertFalse(self.run_stage()['cached'])

    def test_exit_and_interrupt_arguments_cannot_leak_action_secrets(self):
        secret = 'token=secret https://private.example/dialogue'
        for exception_type in [SystemExit, KeyboardInterrupt]:
            def stop(_directory):
                raise exception_type(secret)
            expected = KeyboardInterrupt if exception_type is KeyboardInterrupt else m.StageError
            with self.subTest(exception_type=exception_type):
                with self.assertRaises(BaseException) as caught:
                    self.run_stage(action=stop)
                self.assertIsInstance(caught.exception, expected)
                self.assertNotIn(secret, str(caught.exception))
                self.assertNotIn('private', (self.root / 'state.json').read_text())

    def test_abandoned_temporary_files_are_never_completed_outputs(self):
        abandoned = self.root / 'tmp/verify-audio-abandoned'
        abandoned.mkdir(parents=True)
        (abandoned / 'proof.txt').write_text('not completed')
        result = self.run_stage()
        self.assertFalse(result['cached'])
        self.assertNotEqual(Path(result['directory']), abandoned)
        self.assertEqual(self.calls, 1)

    def test_unsafe_stage_identifiers_are_rejected_before_action(self):
        for stage in ['', '../escape', '/absolute', 'two/stages', '.hidden', 'UPPER', 'a\\b', 'a' * 65]:
            with self.subTest(stage=stage), self.assertRaises(m.StageError):
                self.runner.run(stage, '1', {}, self.action)
        self.assertEqual(self.calls, 0)

    def test_symlink_outputs_and_symlink_directories_are_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        (outside / 'secret.txt').write_text('private')
        for target in [outside, outside / 'secret.txt']:
            def link(directory):
                (directory / 'link').symlink_to(target)
                return {}
            with self.subTest(target=target), self.assertRaises(m.StageError) as caught:
                self.run_stage(action=link)
            self.assertEqual(caught.exception.error['code'], 'unsafe_output')
        self.assertEqual((outside / 'secret.txt').read_text(), 'private')

    def test_fifo_output_is_rejected_without_blocking(self):
        import os
        def fifo(directory):
            os.mkfifo(directory / 'blocked')
            return {}
        with self.assertRaises(m.StageError) as caught:
            self.run_stage(action=fifo)
        self.assertEqual(caught.exception.error['code'], 'unsafe_output')

    def test_untrusted_cached_artifact_paths_cannot_escape_stage_directory(self):
        self.run_stage()
        outside = Path(self.tmp.name) / 'secret.txt'
        outside.write_text('private')
        for path in ['../secret.txt', str(outside), 'nested/../../secret.txt', 'nested\\proof.txt']:
            state = m.read_json(self.root / 'state.json')
            state['stages']['verify-audio']['outputs'][0]['path'] = path
            (self.root / 'state.json').write_text(json.dumps(state))
            with self.subTest(path=path):
                self.assertFalse(self.run_stage()['cached'])
        self.assertEqual(outside.read_text(), 'private')

    def test_cached_symlink_is_not_followed(self):
        result = self.run_stage()
        proof = Path(result['directory']) / 'nested/proof.txt'
        outside = Path(self.tmp.name) / 'secret.txt'
        outside.write_text('private')
        proof.unlink()
        proof.symlink_to(outside)
        self.assertFalse(self.run_stage()['cached'])
        self.assertEqual(outside.read_text(), 'private')

    def test_root_and_state_symlinks_are_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        link = Path(self.tmp.name) / 'link'
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaises((ValueError, m.StageError)):
            m.StageRunner(link).run('verify', '1', {}, self.action)
        self.root.mkdir(parents=True, exist_ok=True)
        outside_state = outside / 'state.json'
        outside_state.write_text('{}')
        (self.root / 'state.json').symlink_to(outside_state)
        with self.assertRaises(m.StageError):
            self.run_stage()
        self.assertEqual(outside_state.read_text(), '{}')

    def test_exclusive_lock_rejects_a_second_process(self):
        program = '''
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from episode_pipeline import StageRunner
def action(directory):
    print('READY', flush=True)
    sys.stdin.readline()
    (directory / 'proof.txt').write_text('finished')
    return {}
StageRunner(Path(sys.argv[2])).run('held', '1', {}, action)
'''
        child = subprocess.Popen([sys.executable, '-c', program, str(SCRIPT.parent), str(self.root)],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), 'READY')
            with self.assertRaises(m.StageError) as caught:
                self.run_stage()
            self.assertEqual(caught.exception.error['code'], 'run_locked')
            self.assertEqual(self.calls, 0)
            child.communicate('\n', timeout=10)
            self.assertEqual(child.returncode, 0)
        finally:
            if child.poll() is None:
                child.kill()
                child.communicate()
        self.assertFalse(self.run_stage()['cached'])

    def test_result_hash_is_reproducible_across_roots_and_key_order(self):
        first = self.run_stage(inputs={'b': 2, 'a': 1})
        second = m.StageRunner(Path(self.tmp.name) / 'another').run(
            'verify-audio', '1', {'a': 1, 'b': 2}, self.action)
        self.assertEqual(first['resultHash'], second['resultHash'])
        self.assertNotEqual(first['directory'], second['directory'])
        self.assertNotIn('directory', m.read_json(self.root / 'state.json')['stages']['verify-audio'])

    def test_bounded_json_rejects_nonfinite_oversized_and_duplicate_data(self):
        path = Path(self.tmp.name) / 'data.json'
        for text in ['{"value": NaN}', '{"value": 1e999}', '{"a": 1, "a": 2}', '{broken']:
            path.write_text(text)
            with self.subTest(text=text), self.assertRaises(ValueError):
                m.read_json(path)
        path.write_text('{"valid": true}')
        with self.assertRaises(ValueError):
            m.read_json(path, max_bytes=4)
        self.assertEqual(m.read_json(path), {'valid': True})
        for value in [float('nan'), float('inf'), {'bad': object()}]:
            with self.subTest(value=type(value)), self.assertRaises(ValueError):
                m.canonical_hash(value)

    def test_file_hash_is_streamed_bounded_and_rejects_symlinks(self):
        path = Path(self.tmp.name) / 'data'
        path.write_bytes(b'abc')
        self.assertEqual(m.file_sha256(path), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        with self.assertRaises(ValueError):
            m.file_sha256(path, max_bytes=2)
        link = Path(self.tmp.name) / 'link'
        link.symlink_to(path)
        with self.assertRaises(ValueError):
            m.file_sha256(link)

    def test_invalid_payload_never_completes(self):
        with self.assertRaises(m.StageError):
            self.run_stage(action=lambda _directory: {'bad': float('nan')})
        self.assertNotIn('verify-audio', m.read_json(self.root / 'state.json')['stages'])

    def test_existing_valid_generation_is_reused_without_replacing_files(self):
        first = self.run_stage()
        proof = Path(first['directory']) / 'nested/proof.txt'
        inode = proof.stat().st_ino
        # An orphaned valid generation can remain after a crash before state commit.
        state = m.read_json(self.root / 'state.json')
        del state['stages']['verify-audio']
        (self.root / 'state.json').write_text(json.dumps(state))
        result = self.run_stage()
        self.assertFalse(result['cached'])
        self.assertEqual(proof.stat().st_ino, inode)
        self.assertEqual(result['resultHash'], first['resultHash'])


if __name__ == '__main__':
    unittest.main()
