# Codex-native OpenMontage first production route

User-authorized scope: issue #60 and `docs/OPENMONTAGE_CODEX_GAP_AUDIT.md`.
The audit was delivered before implementation. Codex supplies orchestration;
the adapter supplies bounded deterministic commands, not a replacement agent.

## Approach and boundaries

Use a thin local adapter calling the existing pinned upstream manifest, schemas,
checkpoints, registry and CinematicRenderer. Vendoring upstream would create
unnecessary AGPL/dependency maintenance; rebuilding orchestration would duplicate
the agent-first system. Neither is selected. No framework/dependency/pin changes.

First route: approved local motion clips + one approved English Chatterbox WAV
and reviewed word timings → canonical documentary artifacts → human checkpoints
→ Remotion cinematic render with audio/captions → exact probe and frame evidence.
Natural Storyteller or Emily is required; no automatic synthesis or provider swap.
Music/end-tag generation, multi-speaker mixing and advanced transitions remain
explicit blockers, unless the owner approved music/end-tag opt-outs in the brief.
First-route render budget is 2–180 seconds, at most 60 hard cuts, 1920×1080/30 fps.
This narrow limit is an implementation choice for a bounded first proof; longer
production is a follow-up, not a reason to change project defaults.

## Interfaces

`python3 integrations/openmontage/scripts/production.py` uses/re-execs the
isolated Python. It verifies SHA and clean tracked upstream source before import.
Commands: `preflight`; `init SLUG --title TITLE`; `checkpoint SLUG STAGE`
(awaiting approval); `checkpoint SLUG STAGE --approve 'owner decision reference'`;
`render SLUG [--fixture]`. Approval requires an existing identical pending artifact.
Project slugs and all media paths stay inside the ignored upstream projects tree.
No command executes arbitrary tool names, downloads media, installs models,
advances all stages, publishes, or asks for another AI subscription.

Creative JSON lives in `projects/SLUG/artifacts/`. Canonical names come from the
real pipeline. Additional asset-manifest metadata holds per-asset SHA256,
rights-review evidence and narration voice/language/word timestamps with WAV hash
and alignment-review note. Require finite ordered timestamps within the actual
audio and edit. Validate scene/cut identity, bounds and the render-runtime lock.
On render re-check every approved artifact snapshot, not only checkpoint status.
Old approvals cannot authorize changed inputs. Missing media/rights/audio stop
before render; generated fixture media cannot pass production mode.

The adapter translates canonical metadata to upstream cinematic `soundtrack` and
`captions.words` transport props, preserving original canonical artifacts. Use
registry `video_compose` for render and `subtitle_gen` for SRT. Keep upstream
final_review and independently probe exact codecs, dimensions, fps, duration and
audio; extract representative frames. Write the compose checkpoint only after QA.
Technical checks do not assert perceptual, caption alignment or rights approval.

## Proof and delivery

Separate test utility builds an editable, schema-valid fixture project with two
distinct FFmpeg-generated moving clips, synthetic tone (NOT speech), reviewed
fixture captions and explicit fixture-only gate simulations. Production mode
must reject it; `--fixture` requires fixture labels throughout. Output/report
remain clearly marked fixture, never a completed episode. Extend the existing
PR-only isolated integration smoke to run it and upload only MP4/SRT/JSON/JPG
evidence. Preserve the existing demo smoke and unconditional host safety gate.

Tests run without runtime installation in the host contract job for pure input
guards; runtime tests/fixture run after existing isolated setup. No runtime test
is represented as passed when skipped. Run all host checks and selected upstream
tests. Android owners can initiate a Codex task and download the PR artifact.
