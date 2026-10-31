# Episode Manifest v1 — deterministic timeline foundation

Issue: [#66](https://github.com/urfavxbf/video-ai-editor/issues/66)

This is a **model-free chapter timeline proof**, not a voiced/published episode or a one-click AI editor. It does not create new art, generate narration, synthesize subtitles, or claim phoneme-accurate lip-sync.

## Source and contract
- `src/episodes/episodeManifest.ts`: versioned TypeScript schema, strict runtime validator and pure compiler.
- `src/episodes/episode-proof-v1.json`: two-chapter, 120-frame/4-second silent proof fixture.
- `src/episodes/EpisodeTimelineProof.tsx`: Remotion scene assembly driven by compiled chapters.
- The current production policy stays authoritative: English, 1920×1080 at 30 fps, approved UrFavXBF and PIX pixel poses and Chatterbox profiles.

```json
{
  "schemaVersion": 1,
  "episodeId": "episode-timeline-proof",
  "language": "en",
  "video": {"width": 1920, "height": 1080, "fps": 30},
  "chapters": [
    {
      "id": "opening",
      "title": "Chapter One: Timeline Proof",
      "chapterNumber": 1,
      "startFrame": 0,
      "durationFrames": 60,
      "voiceEvents": [],
      "audio": []
    }
  ]
}
```

A production manifest has one or more chapters, a lower-case stable episode ID, a unique chapter ID and title, a positive chapter number and **contiguous, zero-based absolute startFrame values**. Each chapter's `durationFrames` must be positive. The total is capped at 108000 frames (one hour). Out-of-order, overlapping or gapped chapters are rejected rather than silently fixed.

Optional `voiceEvents` are chapter-relative events with speaker (`urfavxbf`/`pix`), start/end frames and optional **real audio RMS** samples/rate. Same-speaker events must not overlap. Optional `audio` clips have a `public/`-relative WAV/MP3 path plus chapter-local start/end frames. Paths cannot contain absolute roots, protocols, backslashes, dot segments, empty segments or unsupported extensions. The validator validates **format**, not file existence: a later preparation stage must verify media presence, durations, hashes and licenses before final rendering.

Optional `captions` holds `{file, source}`, with a `public/`-relative SRT/JSON and provenance `human-reviewed` or `forced-alignment`. **Captions are metadata only in v1**; there is no caption renderer or timing guarantee here. Do not claim subtitle delivery until actual alignment and audiovisual QA exist.

## Repeatable, no-paid-service verification

```bash
npm ci
npm run typecheck
node --test tests/composition-duration.test.cjs tests/episode-manifest.test.cjs
node scripts/check-composition-metadata.mjs
python3 scripts/stage_pixel_default_pack.py --verify-workspace
npx remotion render EpisodeTimelineProof out/episode-timeline-proof.mp4 \
  --scale=0.25 --concurrency=2 --codec=h264 --pixel-format=yuv420p
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of json out/episode-timeline-proof.mp4
```

The short, silent fixture is the only render recommended for this PR. A successful fixture is **not** proof of full-resolution performance, real voice sync or finished episode quality.

## Future production stages (not implemented yet)
1. Research and fact-checking with recorded sources, approvals and dated evidence.
2. Script, storyboard and chapter generation with owner review.
3. Chatterbox voice generation with pinned profiles, verified files and sample hashes.
4. Actual WAV-derived speaker timing, word alignment and subtitle quality review.
5. Scene design, motion/FX decisions, asset governance and timeline assembly.
6. Media preparation, bounded rendering, FFprobe/visual/audio QA and human approval.

All these stages should be explicit, independently resumable jobs. No paid API, external provider access, publishing or production media upload is enabled by the manifest itself.

## Verified integration gate

The PR gate now evaluates the registered episode metadata with default and custom
props, rejects a gapped/overlapping manifest in Chromium, and renders all 120
frames with `--muted`. `scripts/check-episode-proof.py` checks the actual codec,
frame count, duration, and static title region at frames 58–61. It requires a
title change at frame 60 and stable titles within each chapter, allowing codec
noise. Supplied RMS arrays must cover every event frame at their declared rate;
short envelopes cannot stretch a last sample into invented speaking energy.

Local verification on 2026-10-31: TypeScript; 17 Node tests; 78 Python tests;
all 13 PNG hashes; actual Chromium metadata checks;
and a 120-frame silent H.264 proof (480×270 at 30 fps). The chapter-two frame was
visually inspected. This validates the small proof, not voiced production or
full-resolution delivery. GitHub Actions must pass on the updated commit too.
