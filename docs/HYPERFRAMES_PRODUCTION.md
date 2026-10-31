# HyperFrames by HeyGen — FIRST-CLASS local motion graphics for Video AI Editor

## Production status

HyperFrames is a **first-class supported animation tool** in this repo, alongside
the Remotion character/episode renderer, not an uninstalled suggestion or a
replacement for Remotion. We pin `hyperframes@0.8.222` in `package.json` and
the lockfile; the project includes a real original HTML/GSAP animation, its CLI
lint/render/staging command, strict motion-graphics clip validation in
`EpisodeProduction`, and a reproducible CI end-to-end render test.

| Stage | Owner |
| --- | --- |
| Original HTML motion graphics, seekable timeline | HyperFrames local CLI |
| Validate and encode original 1920×1080 at 30 fps | `npm run hyperframes:render` + FFprobe/FFmpeg |
| Publish to local Remotion asset directory | `public/hyperframes/kinetic-intro.mp4`, generated/ignored |
| Chapter-specific timed inset or full-screen visual | `EpisodeProduction.motionGraphics` |
| UrFavXBF / PIX / Chatterbox narration / accurate captions | Existing approved Remotion production stack |
| Media and audio delivery QA | Existing production gate + new render smoke |

This workflow **does not require HeyGen cloud or an API key**. Never use
`hyperframes cloud render`, `hyperframes publish`, `hyperframes media-use`,
or upload user media without express owner approval. The first-class package
also has optional paid capabilities; they are outside this approved workflow.
We disable CLI telemetry with `HYPERFRAMES_NO_TELEMETRY=1` and
`DO_NOT_TRACK=1`, and pass blank provider credentials to the render subprocess.

## Quick start (Node 22+, FFmpeg, FFprobe)

```bash
npm ci
npm run hyperframes:lint
npm run hyperframes:render
npm run hyperframes:studio
```

The local original composition lives in
`hyperframes/projects/kinetic-intro/index.html`.
`npm run hyperframes:render` creates an original **2-second, 1920×1080, 30fps
H.264** kinetic title animation, then checks dimensions, frames, decode,
and stages it under `public/hyperframes/`. That folder is ignored and
must not be committed as new unreviewed binary assets.

## Embed in an episode (real rendering)

Use the existing validated `EpisodeProduction` composition and its
approved manifest, character stage, actual approved voice audio and reviewed
captions. Pass the optional `motionGraphics` input property keyed by chapter
ID. The example uses only a **silent, locally staged visual**, no new speech:

```json
{
  "motionGraphics": {
    "opening": [
      {
        "file": "hyperframes/kinetic-intro.mp4",
        "startFrame": 8,
        "durationFrames": 50,
        "layout": "inset"
      }
    ]
  }
}
```

`opening` must match a real ID in your `manifest.chapters`.
`startFrame` and `durationFrames` are **chapter-local** at 30fps and must
fit inside that chapter. Layout options: `inset` (positioned motion graphic
on the right) or `fullscreen` (explicit graphic transition).
File paths must be local `public/hyperframes/*.mp4` paths; untrusted URLs,
traversal, unknown chapters and out-of-range clips are rejected.
Audio is always muted so no demo sounds replace approved Chatterbox narration.

A production owner should create appropriate graphics for each scene and
should not reuse the 2-second proof clip throughout an actual episode.
No default production manifest is altered: clips are included when authored,
validated and requested for narrative impact.

## Verification and limits

CI first performs npm lockfile syncing, tests and a **real HyperFrames render**.
It then stages the actual MP4, renders a Remotion EpisodeProduction fixture with
the staged clip, and verifies H.264 dimensions, frames and decode. Preview stills
and MP4 artifacts are uploaded for review. Validation is explicit: this is
a local-only graphics-to-episode integration, **not** a one-click AI script-to-
finished-video service, a true phoneme lip-sync engine, or a cloud integration.

The approved registry and default English 16:9 Chatterbox/UrFavXBF/PIX
production settings are unchanged. Do not generate or upload new narration
without permission.

References:
- https://github.com/heygen-com/hyperframes
- https://hyperframes.heygen.com/packages/cli
- https://github.com/heygen-com/hyperframes/blob/main/docs/guides/skills.mdx
