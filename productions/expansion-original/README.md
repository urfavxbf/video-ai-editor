# Expansion — Original Reference-Inspired Video

## Scope

Production of an original 60-second portrait motivational video using the **techniques** from the owner's "Expansion feels like chaos before alignment" reference. The reference media is for study only; no original video frames, narration or copyrighted graphics are reused in the new edit.

**Status (2026-10-31):** local original animated MP4 rendered and video/audio streams decoded successfully, but using a **local editorial guide voice** rather than an approved Chatterbox V3 recording. This is not a final voice-approved master. The MP4 and full original Python/FFmpeg rendering source package are delivered as downloadable conversation artifacts; they are not committed as binary files in this repo.

## Files

- [scene-plan.json](scene-plan.json) — the original 25-scene script and visual-metaphor/typography directions, ready for the current editor's scene data pipeline.
- Existing [production policy](../../docs/PRODUCTION_POLICY.md) and [character registry](../../characters/registry.json) — authoritative defaults, unchanged.
- Existing [Chatterbox V3 narrator](../../scripts/chatterbox_voiceover.py), [long-form chunking](../../scripts/chatterbox_longform.py), and [CPU synthesis workflow](../../.github/workflows/chatterbox-generate.yml).

## Verified local preview

- Duration: **60.593 seconds**
- Video: H.264 **1080×1920, 30 fps, 1817 frames**
- Audio: AAC **with English editorial guide narration and original synthesized ambient underscore**
- Original graphics: 25 illustrated vector-like scenes rasterized and animated using local Python/OpenCV/FFmpeg; bold kinetic headlines, approximate voice-paced scene changes, independent artwork drift.
- Media verification: `ffprobe` validated both streams; whole-file `ffmpeg -f null -` decode passed.
- The render is a reference-specific 9:16 edit. It does **not** change the project-wide default (English 16:9 long-form 1920×1080/30fps with approved UrFavXBF/PIX assets).

## Outstanding production acceptance requirements

1. Re-record the **original** narration from `scene-plan.json` through the existing approved **UrFavXBF Chatterbox V3 Natural Storyteller** profile. No arbitrary substitute speakers.
2. Time-align each line to the produced WAV. Do not reuse the temporary guide timing when the spoken recording changes.
3. Replace the guide track, verify speech content, mix and synchronized typography; complete human listening QA.
4. Only then mark a video **approved master** or publish. Reproduction of the reference's copyrighted audio/art is out of scope.

## Repository hygiene

All changes for this study and original edit must remain in a dedicated branch / PR. **Do not push to or merge into `main`** as part of this request. The earlier reference analysis in PR #76 is separate and does not change production settings.
