# OpenMontage / Codex capability audit — issue #60

Audited 2026-10-31 (Asia/Manila), starting from main `1842257` (PR #61).
Upstream: official `calesthio/OpenMontage`, **`195eab24478dc9363326aec437aefc3701635ddf`**,
the unchanged `integrations/openmontage/UPSTREAM_COMMIT`. Findings describe this
snapshot, not an assertion about all future upstream versions. PR #52 is not on
main and is not used here. The pending Zod work is outside this change.

## Verified capability-gap matrix (before implementation)

“Available upstream” means inspected executable source and/or the stated test;
it does not mean an external service, real media, or a finished episode was verified.
Registry availability alone is particularly insufficient for network/GPU tools.

| Capability | Mainline / isolated integration | Pinned upstream evidence | Status / safest missing piece |
| --- | --- | --- | --- |
| Agent / orchestration | Existing Codex session can read files and execute commands; README incorrectly demands a separate assistant | `CODEX.md` → `AGENT_GUIDE.md` → `PROJECT_CONTEXT.md`; agent supplies reasoning, Python supplies tools/persistence | **Working agent; missing entrypoint/docs.** No Copilot, Claude or Cursor account is needed. Actions is deterministic compute, not another agent. |
| Install / isolation | `scripts/setup.sh --skip-tts`, `doctor.sh`, ignored `.runtime/`; both reproduced successfully | Correct SHA, separate venv and composer; installed composer Remotion **4.0.484**, host remains **4.0.522** | **Working.** Keep both dependency trees separate; do not upgrade either incidentally. Existing doctor does not establish production readiness. |
| Pipeline / approvals | Only demo wrapper; no project route | `pipeline_defs/documentary-montage.yaml`, `lib/pipeline_loader.py`, `lib/checkpoint.py` | **Available upstream / missing adapter.** Actual order is `idea → scene_plan → assets → edit → compose`, not a generic seven-stage pipeline. First four stages require approval. Reuse schema validation and checkpoint enforcement. |
| Brief / script / scene plan | Codex can author original English content; no canonical OpenMontage project in the wrapper | `schemas/artifacts/{brief,script,scene_plan}.schema.json`, stage director skills | **Available upstream.** Documentary has no separate script stage; narration/script and timing must be explicit artifacts, not fabricated by a Python topic-to-video engine. |
| Tool discovery | Doctor imports a few packages; does not discover capabilities | `tools/tool_registry.py`: discovery executed; **155 tools** found | **Available upstream / missing bounded preflight.** Inspect selected tools rather than dumping credentials or a huge support envelope. |
| Motion footage search/download | No host acquisition adapter | `tools/video/direct_clip_search.py`, `stock_sources/{nasa,archive_org,wikimedia,pexels,...}.py`; direct NASA search actually executed | **Blocked here by network policy.** NASA, Archive.org and Commons endpoints fail with proxy tunnel 403. The tool returned `success=True` with **zero clips and an errors array**: consumers must inspect results, never equate this with acquired footage. Approved local footage is a valid input; generated test patterns are fixtures only. |
| Semantic corpus retrieval | No corpus/CLIP installation | `corpus_builder`, `clip_search`, `lib/clip_embedder.py` | **Requires optional dependencies/models.** Corpus status `degraded`; CLIP search `unavailable`. Direct search avoids embeddings/GPU; no need to rebuild retrieval or install it for a small first route. |
| Rights / provenance | No license gate around the demo | Per-asset `provider`, `original_url`, `license`; asset-director requires provenance | **Missing local acceptance checks.** No registered `license_checker` was found. A source's public-domain label is not legal clearance; retain item-level evidence and human review, hashes, attribution and allowed use. NASA can include third-party work. No automatic downloading/publishing or license claim. |
| Approved narration | Host `scripts/character_voiceover.py`, `chatterbox_voice_profile.py`, `pix_voice_profile.py`, `check_chatterbox_v3.py` | Upstream registry has TTS selector/providers but no approved Chatterbox adapter | **Requires dependencies / missing bridge.** Actual preflight fails `No module named 'torch'`; no approved production WAV is committed. CPU synthesis is an existing option, not proven here. Reuse approved WAVs or existing CPU path; never substitute Piper/generic/Tagalog TTS. |
| Editing / transitions | Host Remotion/FFmpeg and validated durations exist | `edit_decisions` schema, `video_compose`, `CinematicRenderer`, trim/stitch/mix tools | **Available upstream / missing artifact-to-render bridge.** Canonical cuts adapt to cinematic video scenes. Runtime is locked; unsupported effects must fail, not disappear. First route can restrict itself to hard cuts. |
| Runtime / delivery format | Approved host output is 1920×1080, 30 fps | Documentary director requires **Remotion** (end-tag parity); registry also reports FFmpeg/HyperFrames | **Available upstream with constraints.** Generic “all runtimes available” is not documentary parity. Its 24 fps recommendation cannot override our approved 30 fps policy. Keep Remotion, no silent FFmpeg/HyperFrames downgrade. |
| Narration / caption transport | Host word-timed caption formatter and envelope tools exist | `subtitle_gen` works from supplied timestamps; `CinematicRenderer` consumes `soundtrack` and `captions.words` | **Missing thin translation.** Canonical `audio.narration`/`subtitles` are not automatically the cinematic props. Bind reviewed word timings to the actual WAV hash; estimates are not alignment. |
| Music / end-tag | No host documentary bridge | Documentary directors require music + Remotion end-tag unless explicitly opted out | **Available via staged upstream tools; missing turnkey bridge.** First slice must refuse unhandled music/end-tag plans, or require the real approved opt-out; tests can explicitly label fixture exclusions. Do not silently ship omissions. |
| Rendering | Existing `demo.sh` is a static technical example | `video_compose.execute(operation='render')` selects `CinematicRenderer`, stages local files, invokes isolated composer | **Available upstream / needs real execution evidence.** A new multi-shot motion fixture, audio and captions can verify the bridge; it is not licensed footage or synthesized speech. |
| QA | Host fixture probe + 13 approved PNG checks | `video_compose` final review probes output and samples frames; no registered `quality_gate` tool | **Partial upstream.** Technical probe/frame checks are executable, not perceptual or legal approval. Validate exact canvas/fps/duration/audio, sample images and preserve review artifacts. No finished-episode claim based on tests. |
| Android access | Existing PR-only isolated demo workflow uploads an MP4 | Backlot is optional observer, not execution or approval substitute | **Working compute; missing new-route proof artifact.** Extend existing integration smoke with a bounded fixture and reports; Android GitHub can download it. Do not duplicate unmerged #52 or auto-publish. |
| Paid / GPU providers | No credentials configured in this task | Many registry providers need cloud keys; CLIP/local generation can need models/hardware | **Optional / excluded.** No paid calls, GPU usage, credential onboarding, subscriptions or agent installation in this route. Actions/Codespaces still consume account quotas. |

## Reproduction and results

From the host repository:

```bash
bash integrations/openmontage/scripts/setup.sh --skip-tts
bash integrations/openmontage/scripts/doctor.sh
python3 scripts/check_chatterbox_v3.py
python3 scripts/stage_pixel_default_pack.py --verify-workspace
```

Setup + doctor passed; Chatterbox failed before weight download (`torch` absent).
The approved assets remain unchanged; 13 PNGs verified in the existing gate.
Do not install optional Piper as a remedy for the approved-voice blocker.

In `integrations/openmontage/.runtime/openmontage`, using `.venv/bin/python`:

```python
from lib.pipeline_loader import load_pipeline, get_stage_order
from tools.tool_registry import registry
registry.discover()
print(len(registry.list_all()))  # 155 on this snapshot
print(get_stage_order(load_pipeline('documentary-montage')))
print(registry.get('video_compose').get_info()['render_engines'])
r = registry.get('direct_clip_search').execute({
    'output_dir': 'projects/acquisition-audit/assets/video',
    'queries': [{'query': 'Earth orbit', 'kind': 'video'}],
    'sources': ['nasa'], 'clips_per_query': 1, 'timeout_seconds': 5,
})
print(r.success, r.data['total_clips'], r.data['errors'])
```

Search result: `True`, **0 clips**, explicit proxy-error details. Archive.org and
Commons read-only reachability probes also failed. No media was obtained and no
network-policy bypass was attempted. Provider menus do not prove connectivity.

Installed pytest only into the ignored upstream venv for this audit; no host
dependency changes. Selected upstream checks:

```bash
.venv/bin/python -m pytest -q \
  tests/tools/test_documentary_governance.py \
  tests/tools/test_subtitle_timestamps.py \
  tests/lib/test_checkpoint_prerequisites.py \
  tests/lib/test_checkpoint_noncanonical_stage.py \
  tests/contracts/test_pipeline_catalog.py
```

**64 passed**. These cover real schema/governance/helper behavior with fixtures;
they do not certify all 155 tools, stock services or an entire episode.

## License and trust boundary

Upstream `LICENSE` is **AGPL-3.0**. Preserve its license/source in the pinned,
ignored checkout; do not copy implementation into the host, relicense it, or
assume isolation by itself removes copyleft obligations. The proposed adapter
calls that local runtime and exchanges its documented artifacts. Distribution
of a combined work or offering a modified upstream over a network needs a
specific license review and any required corresponding-source/notices. This
change neither modifies upstream nor offers it as a hosted service. MP4 media
rights and any embedded fonts/music remain separate checks. Do not include
third-party source, local `.env`, provider menus, credentials or model weights
in downloadable proof artifacts.

## Prioritized implementation, deliberately small

1. **First PR:** correct Codex instructions; add a one-command bounded preflight
   and thin project/checkpoint/render adapter. Load the real manifest, validate
   upstream schemas, preserve its approval gates, verify local media/provenance,
   approved English voice identity and WAV-bound captions. Render an explicitly
   labeled new multi-shot motion/audio/caption fixture using the pinned composer;
   upload only the proof MP4, canonical artifacts and QA. Refuse unsupported
   production plans rather than quietly approximating them.
2. **Next independent PR:** item-level free-footage acquisition/review bridge
   around `direct_clip_search`, including zero-results errors, network/quota
   checks, provenance and human selection. Requires a permitted source endpoint
   or owner-approved local footage; do not replace motion with stills.
3. **Next independent PR:** approved Chatterbox CPU runtime/reusable WAV and
   actual alignment bridge. Resolve the concrete torch/model/runtime blocker
   without changing Natural Storyteller/Emily or using paid services.
4. **Then:** music/end-tag/LUT execution parity and longer-project QA, reusing
   upstream tools. Preserve creative approval and the reviewed runtime; no
   publishing automation. Until then, the narrow route rejects these plans
   unless the owner has explicitly approved the documented opt-out.

The first PR is a usable execution route for approved local inputs and a real
technical proof, **not** a claim that a narrated, licensed documentary has been
delivered. Codex still writes/reviews creative artifacts and obtains real owner
approvals; Actions only executes the bounded test route.

## First-slice verification ledger

The adapter was implemented after the matrix above. Initial regression tests
failed because no adapter existed. Independent review reproduced checkpoint
temporary/history symlink escapes, stale downstream approvals, omitted-transition
fades, ignored caption/background options, completed revision-required QA and
caption overruns within WAV/edit tolerance. All six were covered by failing
regressions and fixed: 12 new guard tests pass, alongside 5 existing integration
contracts and 78 host tests. Prerequisite hashes bind approvals; explicit hard
cuts are checked against the pinned scene conversion in the fixture harness.

Local `preflight` runs and reports the actual voice blocker. The four-second
fixture reaches pinned Remotion but the default Chromium download fails with
`getaddrinfo EAI_AGAIN remotion.media` in this restricted task environment. Its
failure report is preserved; no fallback or finished-video claim follows.
Installed `/usr/bin/chromium` is usable by the existing host gate, whose explicit
browser option remains available; the pinned OpenMontage tool does not expose
that option. No upstream source/config is changed to conceal the limitation.
The existing GitHub-hosted integration smoke executes the same new route and
uploads proof if it succeeds; its observed result is reported in the PR.
