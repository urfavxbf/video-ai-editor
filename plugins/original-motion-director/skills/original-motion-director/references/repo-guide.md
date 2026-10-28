# Video AI Editor: inspected starting map

Repository: https://github.com/urfavxbf/video-ai-editor
Inspected 2026-10-28; tree revision f6b80619c64ef1bd7cc2e5410dc897a6d1ab8e08. This is a navigation aid, not a promise that the next checkout is identical. Refresh source and instructions before production.

## Current policy conflicts to resolve correctly

The dated override at the top of README specifies **English voices by default**: Chatterbox UrFavXBF Natural Storyteller and PIX Emily. Older sections and PRODUCTION_STANDARD still describe Tagalog defaults. The dated override supersedes them. Tagalog VoxCPM2 remains an explicit future opt-in; there is no authorization for paid GPU compute or automatic Tagalog generation. Verify this remains current; never infer language from the language of the user's chat.

Current visual direction: animated pixel-glitch **head portraits only**, at the sides of a widescreen graphic field. No full-body overlays. Default new episodes are story-driven long-form 1920×1080, 30 fps; do not assume a Shorts runtime. The user may explicitly choose another format.

Asset binaries are not guaranteed to be in GitHub. Read characters/registry.json and stage approved assets from the user's connected files, checking supplied hashes. Do not substitute placeholders in a final render.

## Capability navigation

| Need | Inspect | Application / constraint |
| --- | --- | --- |
| Entry point and compositions | src/Root.tsx, src/index.ts | Register a new original composition; do not reskin existing demos. |
| Effects toolbox | src/fx/, docs/PRODUCTION_STANDARD.md | 21 documented effects; adapt primitives selectively, not all at once. |
| Native feature packages | package.json, docs/REMOTION_FEATURES.md | Captions, transitions, shapes, effects, motion blur, SFX, Player. Inspect installed APIs. |
| Workflow knowledge | .claude/skills/ai-video-editor/, .claude/skills/remotion-*/ | Read only relevant guides. |
| Aggregated reference | .claude/skills/cineforge-pro/SKILL.md | Combines 13 workflow skills; these are distinct from 21 effects. Load relevant portions. |
| Portrait animation | src/characters/PixelGlitchPortrait.tsx, portraitLayout.ts | Speaker-aware expressions, RMS energy, reactions; not viseme lip sync. |
| Audio event behavior | src/characters/CharacterPuppet.tsx | Inspect VoiceEvent, frame-offset and envelope sampling semantics before integration. |
| Measured motion envelope | scripts/extract_voice_envelope.py | Requires uncompressed 16-bit PCM WAV; exports speaker, startFrame, endFrame, rms, samplesPerSecond. |
| Voice generation | scripts/character_voiceover.py, docs/CHATTERBOX_TTS.md | Check actual defaults; explicitly select English when following current policy. |
| Transcription | scripts/groq_transcribe.py | Verify credentials, language, timestamp granularity, and cost before use. |
| Layout/asset policy | docs/PIXEL_GLITCH_PORTRAITS_ONLY.md, docs/PIXEL_GLITCH_CHARACTER_PACK.md, characters/registry.json | Preserve approved identities; verify staged binaries. |
| Animation roadmap | docs/CHARACTER_ANIMATION_V2.md | Distinguish working 2.5D motion from proposed rigged 3D. |
| Existing QA | tests/, .github/workflows/, package.json | Use actual scripts; do not invent npm test or render tasks. |
| Editing existing footage | src/edit/Edit.tsx, src/edit/edit.json | Inspect cut-list schema and create a new task-specific edit. |
| Licenses | THIRD_PARTY_NOTICES.md, licenses/ | No repository-wide MIT assumption; assets/framework may have separate terms. |

## Verified command starting points

Read the current scripts first. At inspection, npm scripts included `typecheck`, `studio`, `render:showcase`, `render:edit`, `render:repo-showcase`, `stills`, and `bench`. Existing showcase/edit commands render examples, not a newly commissioned production. Remotion packages were pinned to 4.0.522; use the lockfile rather than installing latest dependencies by default.

The inspected envelope CLI accepts:

```bash
python3 scripts/extract_voice_envelope.py \
  --input out/pix-line-001.wav --speaker pix \
  --start-frame 300 --fps 30 \
  --output out/pix-line-001-envelope.json
```

This example start frame is illustrative; replace it with the measured production timeline. The default envelope sampling is 10 Hz, insufficient by itself to establish phoneme timing. Silence gates and visible talk states require checking against the actual audio.

Some subject-masking helpers depend on macOS/Apple Vision. Check host support before choosing a masking technique on Linux/Codespaces. The repo is a toolkit, not proof of a complete one-click production pipeline.
