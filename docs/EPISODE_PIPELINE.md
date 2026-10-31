# Resumable local episode stages

`scripts/episode_pipeline.py` provides a standard-library, Linux CPU stage runner.
It records actual local artifacts and rehashes them before resuming. This core
does not synthesize audio, align words, render video, call providers, publish, or
change the approved English UrFavXBF/PIX production defaults.

## Public interface

```python
from pathlib import Path
from episode_pipeline import StageRunner, StageError, canonical_hash, file_sha256, read_json

runner = StageRunner(Path('work/episode-001'))

def verify(directory: Path):
    # Write only inside this provided, stage-owned temporary directory.
    (directory / 'evidence.json').write_text('{"verified": true}\n')
    return {'evidence': 'evidence.json', 'verified': True}

result = runner.run(
    'verify-manifest', '1',
    {'manifestHash': file_sha256('episode.json')},
    verify,
)
evidence = Path(result['directory']) / result['payload']['evidence']
```

Importers outside `scripts/` must add that directory to their Python import
path. There is no CLI in the runner core.

`StageRunner(root).run(stage_id, version, inputs, action)` accepts a lowercase
slug matching `[a-z0-9][a-z0-9-]{0,63}`, a nonempty version string of at most 128
characters, JSON-serializable inputs, and a callable accepting a `Path`. The
action returns a JSON-serializable payload. All regular files beneath its
temporary directory become outputs automatically; there is no caller-supplied
output path list. JSON must contain finite numbers.

The returned dictionary contains:

| Key | Meaning |
| --- | --- |
| `stage` | Stage ID |
| `status` | `completed` |
| `version` | Caller-provided stage implementation version |
| `inputHash` | SHA-256 of canonical input JSON |
| `outputs` | Sorted list of `{path, size, sha256}`; paths are relative POSIX paths |
| `payload` | A JSON copy of the action result |
| `resultHash` | SHA-256 of the complete result content above, excluding itself |
| `directory` | Absolute path containing the completed stage outputs |
| `cached` | Whether execution was skipped after verifying completed evidence |

`directory` and `cached` are excluded from the digest and persisted completion
record. No timestamp participates in hashing. Equivalent input key ordering and
identical files/payload/version produce the same digest across run roots. Use
relative artifact references in payloads; random temporary paths would make a
payload nonreproducible. Include source hashes, dependent result hashes, policy
hashes and any other relevant evidence in `inputs`; increment `version` when the
action's behavior changes. The runner cannot infer undeclared dependencies.

Public helpers are `canonical_hash(value) -> str`,
`file_sha256(path, max_bytes=2147483648) -> str`, and
`read_json(path, max_bytes=4194304) -> JSON value`. Helpers raise `ValueError` for
invalid, unsafe, or oversized content. JSON reading rejects duplicate keys,
nonfinite numbers and overflowed floats. File reads reject symlinks and special
files and stream file hashes in bounded chunks. Caller-supplied limits can only
reduce the defaults.

## Persistence and recovery

Each `run` holds an exclusive nonblocking `flock` on `root/.lock`, covering
cache verification, action execution and publication. A competing process gets
`StageError` with code `run_locked`; there is no automatic retry. Cooperating
callers using the same root therefore cannot execute stages concurrently.

The run directory contains `state.json`, `tmp/`, and
`stages/<stage-id>/<resultHash>/`. State is written to a temporary file, fsynced,
atomically replaced, and followed by a directory fsync. Verified output files
and all temporary-tree directories are fsynced before the tree is renamed into
its generation directory and that directory's parent is fsynced. Newly created
run/output directories also have their parent entries fsynced. A valid orphaned
generation is reused after re-execution; its existing files are preserved.

Resume requires the same version/input hash, a matching completion digest, safe
relative output paths, and an exact match against the rehashed output file set.
Missing, changed, extra or unsafe files invalidate the cache and cause explicit
local execution. Absolute paths, traversal, symlinks and special-file outputs
are rejected. Failed new attempts preserve previous valid completions and their
files. Interrupted temporary trees never prove completion and are ignored.

`state.json` keeps successful records under `stages`, separately from the latest
attempt under `attempts`. The latter has `running`, `completed`, `failed` or
`cancelled` status. `StageError.error` is the safe structure
`{stage, code, message, retryable}`. Action exception text, URLs, tracebacks and
input content are not copied into failure records. `SystemExit` from an action
becomes a safe `action_failed` error. `KeyboardInterrupt` is persisted with code
`cancelled` and then raised without its original arguments. Call `run` again to retry a
local failure; each invocation executes an action at most once. A cache hit can
reuse a previous completion after a later failed version attempt, while the
attempt record still describes that failure.

## Boundaries

Actions are trusted Python code, with no OS sandbox or timeout. They must write
only inside their provided directory and must not perform irreversible external
effects. The runner cannot undo such effects after a crash and does not retry
them automatically. JSON content is capped at 4 MiB, output trees at 10,000
entries and 2 GiB total file bytes. These are verification limits, not filesystem
quotas on running actions. Files must remain stable while being verified; this
is not protection against a hostile process racing filesystem changes.

The runner retains old generation directories and abandoned temporary trees;
garbage collection is a separate operator task performed while no stage runs.
It fails closed on invalid state. If storage cannot persist a failure record,
the caller still receives a safe error, but durable failure reporting is not
guaranteed. The guarantees assume a local filesystem honoring rename, fsync and
Linux advisory locks.

Run the contract tests with:

```bash
python3 -m unittest discover -s tests -p 'test_episode_pipeline.py' -v
```

## Local production increment (issue #69)

`python3 scripts/produce-episode.py --manifest episode.json --clips clips.json
--media-root public --work-dir work/my-episode` runs validated manifest and media
preparation stages. Add `--render` to run the CPU Remotion encoder and machine QA.
The production render is English 1920×1080 at 30fps, H.264/AAC, concurrency 2, with
a hard 600-second render deadline. Chromium uses software GL and hardware
encoding is explicitly disabled. Logs are monitored while processes run.
Input hashing and WAV analysis use cooperative deadlines (120 seconds per
preflight/preparation pass, at most 30 seconds per WAV analysis); regular-file
I/O can exceed a cooperative deadline during a single read. Total unique WAV
inputs are capped at 2 GiB. Each CPU job runs in a dedicated Linux subreaper supervisor, so detached
Chromium children remain owned after their original parent exits. Timeout and
cancellation terminate that tree; pidfds pin process identities while signaling,
and adopted children are reaped. Cleanup has a short additional bounded grace
period. This is trusted local execution, not an OS sandbox.
An explicit `--diagnostic` opt-in permits nonspeech fixtures and uses 480×270;
that output is never a production delivery. No TTS, ASR, research provider,
external API, GPU, upload or publishing is invoked.

The job contract is:

```json
{
  "schemaVersion": 1,
  "clips": [{
    "chapterId": "opening",
    "speaker": "urfavxbf",
    "file": "voiceovers/my-approved-clip.wav",
    "startFrame": 0,
    "voiceProfile": "natural-storyteller-v1",
    "sha256": "REPLACE_WITH_ACTUAL_WAV_SHA256",
    "provenance": "owner-supplied-chatterbox"
  }]
}
```

PIX must use `pix-cute-female-emily-v1`. Profile declarations are compared with
the character registry; SHA-256 verifies the actual supplied bytes. Neither
establishes speaker identity acoustically. A person must confirm the actual
Chatterbox speaker/provenance by listening. No real character WAVs were supplied
or generated for this implementation. Inputs must be local, stable PCM16 WAVs,
8–96 kHz, mono/stereo, nonempty and nonsilent. Measurements derive actual sample
durations, clip end frames and normalized RMS. Existing unverified manifest
voice/audio/caption data is rejected at production preparation; clip receipts
supply those values. Chapters must be long enough; overruns fail explicitly.

An optional clip `alignment` object contains `schemaVersion:1`,
`audioSha256` matching the exact WAV, `source:"human-reviewed"` or
`"forced-alignment"`, `reviewed:true`, and `words:[{start:0.1,end:0.4,text:"Hello"}]`.
Times are supplied seconds within that WAV. The importer checks provenance,
ordering, overlap, duration bounds and text, then groups adjacent supplied words
into readable cues. It does not infer words/times from the script or perform
forced alignment. A `reviewed` flag is a declaration; semantic timing accuracy
still needs listening. Missing alignment produces no captions. The Remotion
`EpisodeProduction` scene uses chapter-local measured speaker/listener events,
approved pixel poses, chapter titles and optional validated captions. There is
no phoneme lip-sync claim.

Preparation snapshots only the 13 hash-verified PNGs, local fonts and content-
addressed WAVs into a private stage public directory. The render uses those
snapshots, not an arbitrary served public tree. Stages include implementation,
registry, asset, input and media hashes in cache keys; the render also records
Node/FFmpeg versions and selected browser version. Outputs are reproducible for a pinned toolchain;
we do not promise byte-identical encoding across browser/OS versions.

Machine QA probes the actual encoded MP4 for H.264, dimensions, 30fps, exact
video frame count, duration, AAC presence when narration exists, mean/peak dBFS,
black intervals, audio EOF coverage, and excessive silence within source-derived
active RMS windows (preserving genuine source pauses).
Mean/peak dBFS is not integrated LUFS. Manual review remains required for identity,
word timing, pronunciation, narrative/fact quality, caption readability and
visual/audio playback. QA never grants publishing approval.

Run the actual diagnostic render and cache-resume assertion:

```bash
REMOTION_BROWSER_EXECUTABLE=/usr/bin/chromium \
python3 scripts/check-production-fixture.py --work-dir work/production-fixture
```

Omit the browser variable when using Remotion's installed managed Chrome.
The fixture makes two explicitly labeled sine tones (not character voices),
renders four seconds, checks the actual H.264/AAC artifact and asserts that a
second invocation caches all four stages. GitHub's safety gate runs this proof
and uploads MP4, state and QA artifacts. Local verification produced 120 video
frames at 480×270/30fps, AAC, no black intervals; the first chapter was visually
inspected. It is not a narrated, captioned or fully reviewed episode.

Remaining milestones: sourced research/script/storyboard authoring stages,
controlled opt-in Chatterbox/ASR generation receipts and quotas, real approved
voice/alignment fixtures, integrated-LUFS targets, full-resolution long-form
performance and manual delivery review. Existing standalone voice/transcription
scripts remain available under their existing authorization rules; they are not
automatically invoked here. Issue #69 remains open.
