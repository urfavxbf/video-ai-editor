"""Durable local CPU stage execution. Actions are trusted Python, not sandboxed."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile


MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024**3
MAX_OUTPUT_ENTRIES = 10000
SLUG = re.compile(r'[a-z0-9][a-z0-9-]{0,63}\Z')
DIGEST = re.compile(r'[0-9a-f]{64}\Z')


class StageError(RuntimeError):
    """Safe caller-facing failure; original action exceptions are never logged."""
    def __init__(self, stage, code, message, retryable=True):
        self.error = {'stage': stage, 'code': code, 'message': message, 'retryable': retryable}
        super().__init__(message)


def _checked_path(path):
    path = Path(path).absolute()
    if '..' in path.parts:
        raise ValueError('Traversal paths are not allowed.')
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ValueError('Symlink paths are not allowed.')
    return path


def _open_regular(path):
    path = _checked_path(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise ValueError('A regular file is required.')
    return os.fdopen(fd, 'rb')


def _json_bytes(value):
    try:
        data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':'), allow_nan=False).encode('utf-8')
        if len(data) > MAX_JSON_BYTES:
            raise ValueError('oversized')
        return data
    except (TypeError, ValueError, OverflowError, RecursionError, UnicodeError):
        raise ValueError('Invalid or oversized JSON content.') from None


def canonical_hash(value):
    """SHA-256 of sorted compact UTF-8 JSON, bounded to 4 MiB; no NaN/Infinity."""
    return hashlib.sha256(_json_bytes(value)).hexdigest()


def read_json(path, max_bytes=MAX_JSON_BYTES):
    """Read bounded strict JSON from a regular file without following symlinks."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON keys.')
            result[key] = value
        return result
    try:
        if not isinstance(max_bytes, int) or not 0 < max_bytes <= MAX_JSON_BYTES:
            raise ValueError('Invalid JSON limit.')
        with _open_regular(path) as stream:
            data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError('Oversized JSON file.')
        value = json.loads(data, object_pairs_hook=pairs,
                           parse_constant=lambda _value: (_ for _ in ()).throw(ValueError()))
        _json_bytes(value)  # Also reject finite JSON literals that overflow to infinity.
        return value
    except (OSError, ValueError, RecursionError, UnicodeError):
        raise ValueError('Invalid, unsafe, or oversized JSON file.') from None


def file_sha256(path, max_bytes=MAX_FILE_BYTES):
    """Stream at most 2 GiB from a regular, non-symlink file into SHA-256."""
    if not isinstance(max_bytes, int) or not 0 <= max_bytes <= MAX_FILE_BYTES:
        raise ValueError('Invalid file limit.')
    digest, count = hashlib.sha256(), 0
    try:
        with _open_regular(path) as stream:
            if os.fstat(stream.fileno()).st_size > max_bytes:
                raise ValueError('Oversized file.')
            while chunk := stream.read(min(1024 * 1024, max_bytes - count + 1)):
                count += len(chunk)
                if count > max_bytes:
                    raise ValueError('Oversized file.')
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        raise ValueError('Cannot hash unsafe or missing file.') from None


def _relative(value):
    if (not isinstance(value, str) or len(value) > 1024 or '\\' in value
            or '\0' in value or any(p in ('', '.', '..') for p in value.split('/'))
            or Path(value).is_absolute()):
        raise ValueError('Unsafe artifact path.')
    return value


def _outputs(directory):
    directory = _checked_path(directory)
    if not directory.is_dir():
        raise ValueError('Output directory is missing.')
    files, pending, entries, total = [], [directory], 0, 0
    while pending:
        with os.scandir(pending.pop()) as children:
            for child in children:
                entries += 1
                if entries > MAX_OUTPUT_ENTRIES:
                    raise ValueError('Too many output entries.')
                info = child.stat(follow_symlinks=False)
                if stat.S_ISDIR(info.st_mode):
                    pending.append(Path(child.path))
                elif stat.S_ISREG(info.st_mode):
                    total += info.st_size
                    if total > MAX_FILE_BYTES:
                        raise ValueError('Stage output exceeds 2 GiB.')
                    relative = _relative(Path(child.path).relative_to(directory).as_posix())
                    files.append({'path': relative, 'size': info.st_size,
                                  'sha256': file_sha256(child.path)})
                else:
                    raise ValueError('Only regular files and directories are allowed.')
    return sorted(files, key=lambda item: item['path'])


def _sync_directory(directory):
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _mkdir(directory):
    missing, current = [], directory
    while not current.exists():
        missing.append(current)
        current = current.parent
    directory.mkdir(parents=True, exist_ok=True)
    for created in reversed(missing):
        _sync_directory(created.parent)


class StageRunner:
    """Serialize stages per root, preserve successful generations, and verify resume."""
    def __init__(self, root):
        self.root = _checked_path(root)
        _mkdir(self.root)

    def _save(self, state):
        _checked_path(self.root / 'state.json')
        data = _json_bytes(state)
        fd, name = tempfile.mkstemp(prefix='.state-', dir=self.root)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, self.root / 'state.json')
            _sync_directory(self.root)
        finally:
            Path(name).unlink(missing_ok=True)

    def _cached(self, record, stage_id, version, input_hash):
        try:
            if (not isinstance(record, dict) or record['stage'] != stage_id
                    or record['status'] != 'completed' or record['version'] != version
                    or record['inputHash'] != input_hash or not DIGEST.fullmatch(record['resultHash'])):
                return None
            for output in record['outputs']:
                _relative(output['path'])
            content = {key: value for key, value in record.items() if key != 'resultHash'}
            if canonical_hash(content) != record['resultHash']:
                return None
            directory = self.root / 'stages' / stage_id / record['resultHash']
            if _outputs(directory) != record['outputs']:
                return None
            return dict(record, directory=str(directory), cached=True)
        except (KeyError, TypeError, OSError, ValueError):
            return None

    def run(self, stage_id, version, inputs, action):
        """Run action(temp_directory)->JSON payload or return rehashed cached evidence.

        Raises StageError for safe structured failures; KeyboardInterrupt is saved
        as cancelled then reraised. Explicit reruns are the only action retries.
        """
        if not isinstance(stage_id, str) or not SLUG.fullmatch(stage_id):
            raise StageError(None, 'invalid_stage', 'Stage ID must be a safe lowercase slug.', False)
        if not isinstance(version, str) or not 0 < len(version) <= 128:
            raise StageError(stage_id, 'invalid_version', 'Stage version must be a short nonempty string.', False)
        try:
            input_hash = canonical_hash(inputs)
        except ValueError:
            raise StageError(stage_id, 'invalid_inputs', 'Stage inputs must be bounded JSON.', False) from None
        try:
            _checked_path(self.root / '.lock')
            lock = os.open(self.root / '.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        except (OSError, ValueError):
            raise StageError(stage_id, 'unsafe_root', 'Run directory is unsafe or unavailable.', False) from None
        try:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise StageError(stage_id, 'run_locked', 'Another stage owns this run directory.') from None
            return self._run_locked(stage_id, version, input_hash, action)
        finally:
            os.close(lock)

    def _run_locked(self, stage_id, version, input_hash, action):
        try:
            state_path = _checked_path(self.root / 'state.json')
            state = read_json(state_path) if state_path.exists() else {'schemaVersion': 1, 'stages': {}, 'attempts': {}}
            if (state['schemaVersion'] != 1 or not isinstance(state['stages'], dict)
                    or not isinstance(state['attempts'], dict)):
                raise ValueError('Invalid state.')
            for relative in ['tmp', 'stages', f'stages/{stage_id}']:
                directory = _checked_path(self.root / relative)
                _mkdir(directory)
        except (KeyError, TypeError, OSError, ValueError):
            raise StageError(stage_id, 'invalid_state', 'Run state or output directories are unsafe or invalid.', False) from None
        cached = self._cached(state['stages'].get(stage_id), stage_id, version, input_hash)
        if cached is not None:
            return cached
        attempt = {'stage': stage_id, 'status': 'running', 'version': version, 'inputHash': input_hash}
        state['attempts'][stage_id] = attempt
        previous = state['stages'].get(stage_id)
        temporary = None
        try:
            self._save(state)
            temporary = Path(tempfile.mkdtemp(prefix=f'{stage_id}-', dir=self.root / 'tmp'))
            try:
                payload = json.loads(_json_bytes(action(temporary)))
            except KeyboardInterrupt:
                raise
            except (Exception, SystemExit):
                raise StageError(stage_id, 'action_failed', 'Stage action failed; rerun explicitly to retry.') from None
            try:
                outputs = _outputs(temporary)
            except (OSError, ValueError):
                raise StageError(stage_id, 'unsafe_output', 'Stage outputs are unsafe, missing, or over the resource limit.') from None
            record = {'stage': stage_id, 'status': 'completed', 'version': version,
                      'inputHash': input_hash, 'outputs': outputs, 'payload': payload}
            record['resultHash'] = canonical_hash(record)
            destination = self.root / 'stages' / stage_id / record['resultHash']
            _checked_path(destination)
            # Publish only verified complete trees. Earlier generations survive failures.
            for output in outputs:
                with _open_regular(temporary / output['path']) as stream:
                    os.fsync(stream.fileno())
            for directory, _children, _files in os.walk(temporary, topdown=False):
                _sync_directory(directory)
            try:
                valid_generation = _outputs(destination) == outputs
            except (OSError, ValueError):
                valid_generation = False
            if not valid_generation:
                if destination.exists():
                    shutil.rmtree(destination)
                os.replace(temporary, destination)
            _sync_directory(destination.parent)
            state['stages'][stage_id] = record
            state['attempts'][stage_id] = dict(attempt, status='completed')
            self._save(state)
            return dict(record, directory=str(destination), cached=False)
        except BaseException as exc:
            if previous is None:
                state['stages'].pop(stage_id, None)
            else:
                state['stages'][stage_id] = previous
            if isinstance(exc, KeyboardInterrupt):
                error = StageError(stage_id, 'cancelled', 'Stage cancelled; rerun explicitly to retry.')
                status = 'cancelled'
            else:
                error = exc if isinstance(exc, StageError) else StageError(stage_id, 'storage_failed', 'Stage storage failed; rerun explicitly to retry.')
                status = 'failed'
            state['attempts'][stage_id] = dict(attempt, status=status, error=error.error)
            try:
                self._save(state)
            except (OSError, ValueError):
                pass  # Do not replace a safe failure with storage metadata/errors.
            if isinstance(exc, KeyboardInterrupt):
                raise KeyboardInterrupt() from None
            raise error from None
        finally:
            if temporary is not None:
                try:
                    if temporary.is_symlink() or temporary.is_file():
                        temporary.unlink(missing_ok=True)
                    elif temporary.exists():
                        shutil.rmtree(temporary)
                except OSError:
                    pass  # Abandoned temporary trees never constitute completion.
