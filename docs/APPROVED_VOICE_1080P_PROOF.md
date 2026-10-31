# Approved English voice samples — 1080p production proof

**Scope:** integration test using two *previously generated*, owner-approved GitHub Actions sample WAVs. This is **not** a completed scripted episode, human-reviewed voice release, aligned-caption demo or YouTube publication.

Workflow: `.github/workflows/approved-voice-1080p-proof.yml`. Use **Actions → Approved English voices — 1080p integration proof** to rerun manually while the artifacts remain available.

## Verified source provenance
- UrFavXBF: successful [CPU English Chatterbox V3 smoke run](https://github.com/urfavxbf/video-ai-editor/actions/runs/40607467395), artifact `chatterbox-v3-english-voice-sample`.
- PIX: successful [English approved Emily-reference sample run](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831), artifact `pix-cute-female-chatterbox-voice-sample`.
- **Before** preparing a manifest, the workflow checks their SHA-256 digests against the current `characters/registry.json` `english_voice.sample_sha256` fields and verifies both are PCM16 mono at 24 kHz. These exact artifacts have also been inspected independently.
- The artifact downloads require GitHub `actions:read` permission. Neither voice model is downloaded or invoked; no paid provider, GPU, or biometric voice cloning is performed. Artifacts expire, so a later rerun may need new, explicitly approved inputs.

## What the proof actually verifies
- An exact two-chapter manifest derived from the real WAV sample counts.
- The hash-verified WAVs are ingested using the existing receipt contract as `owner-supplied-chatterbox` (a provenance declaration), deriving real duration/RMS and speaker turns.
- The CPU `EpisodeProduction` path renders full **1920×1080, 30fps H.264/AAC** with approved 13-pose art, within the renderer's 600-second timeout and workflow 22-minute limit.
- FFprobe/FFmpeg machine QA checks exact streams, frame count and duration, black frames, audio coverage and silence. An independent video hash-bound `approved-voice-review.json` marks manual checks pending.
- Outputs are uploaded as a time-limited GitHub Actions artifact. They must not be posted as a finished video or published to YouTube.

## Not established by machine QA
Actual listening approval, Chatterbox speaker similarity, semantic alignment, word-level captions, sound mastering, full-length episode performance, and narrative quality. Sample speech lines do not form an original episode script. The manual-review checklist documents what remains.

This workflow can consume GitHub Actions runner minutes and requires the source artifacts to remain available. Keep work on a reviewable PR until the pipeline is validated.
