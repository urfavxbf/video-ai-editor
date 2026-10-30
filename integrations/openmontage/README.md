# OpenMontage — Codex-native, isolated production tools

**The Codex environment already connected to this repository is the agent.**
No Copilot, Claude, Cursor account or second AI-agent installation is required.
Codex reads the pinned instructions, makes creative decisions, authors/reviews
artifacts, requests real approvals and runs tools. Actions executes deterministic
commands; it is not an AI reasoning agent.

Read the [verified capability-gap audit](../../docs/OPENMONTAGE_CODEX_GAP_AUDIT.md)
and [current production policy](../../docs/PRODUCTION_POLICY.md). This opt-in route
preserves UrFavXBF/PIX, approved art/voices, English and 1920×1080/30 fps.

## One-command preflight

From the host root in the existing Codex task environment:

```bash
# Only if not already installed:
bash integrations/openmontage/scripts/setup.sh --skip-tts
python3 integrations/openmontage/scripts/production.py preflight
```

This selects the isolated venv, verifies the unchanged source pin, loads the real
manifest and discovers selected tools. Its JSON diagnoses capabilities; `degraded`
is not production readiness or approval. It does not print credentials, synthesize
speech, download footage or make paid calls. Registration does not prove network
connectivity. Modified tracked upstream source or a wrong SHA is a hard blocker.

Verified task-machine blockers: Chatterbox lacks `torch`; NASA, Archive.org and
Commons are denied by network policy; the default Chromium download from
`remotion.media` also fails. Do not downgrade voice/runtime to conceal these.
Existing approved WAVs do not require synthesis dependencies.

## Approved local inputs → reviewed MP4

Codex reads nested `CODEX.md`, `AGENT_GUIDE.md`, `PROJECT_CONTEXT.md`,
`pipeline_defs/documentary-montage.yaml` and each stage's director skill. Actual
stages: **idea → scene_plan → assets → edit → compose**. The first four require
owner approval. Python does not generate topics, invent scripts or approve stages.
Backlot is an optional observer, not an execution/approval substitute.

A task you can send to the configured Codex environment from Android:

> Use the pinned OpenMontage documentary route and current production policy.
> Run preflight; propose an original English brief/script, scenes and footage/license
> sources. Keep 1920×1080/30 fps, approved Natural Storyteller/Emily and zero paid
> API/GPU. Present each real approval gate before advancing. Use approved local
> footage/WAV where available; report exact missing media/runtime/rights blockers.
> Do not substitute voices, deliver test media as an episode or publish.

Commands run by Codex:

```bash
python3 integrations/openmontage/scripts/production.py init my-documentary --title 'My original topic'
# Codex writes schema-valid artifacts after reading the stage director skill.
python3 integrations/openmontage/scripts/production.py checkpoint my-documentary idea
# Present brief and stop for the actual owner decision. Only after that decision:
python3 integrations/openmontage/scripts/production.py checkpoint my-documentary idea --approve 'owner decision reference'
# Repeat separately for scene_plan, assets and edit with real owner approvals.
python3 integrations/openmontage/scripts/production.py render my-documentary
```

Projects are under ignored `.runtime/openmontage/projects/my-documentary/`.
Use canonical `artifacts/{brief,scene_plan,asset_manifest,edit_decisions}.json`,
following upstream `schemas/artifacts/`. The adapter uses upstream checkpoints;
changed approved artifacts/media fail acceptance. Never use `--approve` to skip
an actual conversation gate. Use a new project ID for a new render.
Each gate is bound to prerequisite artifact hashes; reapproving a changed brief
invalidates downstream approvals. A changed prerequisite also invalidates a
pending approval. No checkpoint/history/temp symlinks are accepted.

First-route limits: **2–180 seconds, at most 60 hard cuts**, matching `broll`
scenes and distinct local motion assets. Transforms, overlays, speed changes,
multi-speaker mixing, music/end-tag execution are explicit blockers. Caption
styling overrides and cut background colors are also rejected explicitly.
Documentary normally requires music and an end-tag; this route needs **real approved opt-out
reasons**, or stops for the next adapter. It never invents those decisions.

Additional adapter metadata (alongside the upstream canonical fields):

- `brief.metadata`: `language: "en"`, `render_runtime: "remotion"`,
  `music_plan: {"source":"none","opt_out_reason":"<actual owner decision>"}`,
  `end_tag_plan: null`, `end_tag_opt_out_reason: "<actual owner decision>"`.
- Each asset: unique `id`, project-relative real `path`, `scene_id`, `source_tool`,
  `provider`, `original_url`, item-level `license`, `cost_usd: 0`.
- `asset_manifest.metadata.provenance[asset_id]`: `sha256`, `rights_review`
  (item evidence, attribution and allowed use), `reviewed_by`. A site's generic
  license label is not legal clearance.
- `asset_manifest.metadata.narration`: narration WAV `asset_id`,
  `character: "urfavxbf"` or `"pix"`, matching `voice_id` (`natural-storyteller-v1`
  or `pix-cute-female-emily-v1`), `language: "en"`, `audio_sha256`,
  `alignment_review`, `segments: [{"words":[{"word":"Hello","start":0.2,"end":0.7}]}]`.
  Reviewed WAV/edit durations must match within 50 ms. Word timings must be
  ordered, finite and within the actual WAV; estimates are not alignment.
- `edit_decisions`: `renderer_family: "documentary-montage"`,
  `render_runtime: "remotion"`, cuts referencing asset IDs with matching scene
  IDs, real source in/out times and explicit hard cuts.

The registry's `subtitle_gen` writes SRT. `video_compose` renders the cinematic
word-caption transport props and muxes the approved audio without extra speech
fades. Exact probe, full decode and sample frames verify technical output;
`final_review`, `render_report` and FFprobe JSON are preserved.
Upstream `revise` QA results remain `awaiting_human`, never completed; evidence
is kept and the report identifies that state. A failed/unknown QA result blocks.
Labels/checksums cannot prove audible voice identity, alignment or rights: owner audiovisual/legal
review remains necessary. No automatic publishing occurs.

When new narration is separately authorized and available, reuse the existing
host Chatterbox environment and CPU path, not upstream Piper or paid TTS:

```bash
python scripts/check_chatterbox_v3.py
python scripts/character_voiceover.py --character urfavxbf --language en --device cpu \
  --text-file SCRIPT.txt --output APPROVED.wav
```

This neither installs/downloads models automatically nor guarantees inference.
PIX retains the existing Emily-reference path; no voice identities change.

## Real technical proof and Android download

```bash
python3 integrations/openmontage/tests/production_fixture.py local-check
```

This creates `projects/fixture-local-check/` with editable canonical JSON, two
moving FFmpeg test patterns, a four-second tone **not speech**, timed labels and
simulated **fixture-only** approvals. Production mode rejects it. Explicit fixture
mode produces a new 1080p/30 fps MP4/SRT/probe/reviews/frames; it is not a licensed
or voiced episode. Use a new ID for another run; existing projects are preserved.

The existing PR-only **OpenMontage isolated integration** workflow retains its
demo and also runs the new proof. On Android GitHub: PR → Checks → OpenMontage run
→ Artifacts → **openmontage-codex-motion-proof** → download ZIP. Open `fixture.mp4`,
`qa-*.jpg`, `captions.srt` and JSON reports. Evidence expires after three days.
No duplicate manual-demo workflow, extra AI agent or publishing is introduced.
Actions/Codespaces still consume account quotas; do not launch large jobs blindly.

## Preservation and license

Official pin: `195eab24478dc9363326aec437aefc3701635ddf`, **AGPL-3.0**. Its source,
dependencies and media stay in the ignored runtime. No implementation is copied
into the host. Isolation alone does not remove AGPL obligations; see the audit
before distributing/hosting modified combined systems. Media rights are separate.

No root dependency changes, framework migration, paid API/GPU, secrets, publishing,
main push or merge. Keep pending Zod work separate. Existing doctor/demo and the
optional Codespaces profile remain usable. On Android Codespaces select the
reviewed branch (or merged main after approval) and the OpenMontage configuration;
no obsolete branch or additional AI-assistant connection is required.
