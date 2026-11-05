---
name: hyperframes-motion-graphics
description: Use when creating original offline HyperFrames and GSAP motion graphics, validating local H.264 output, or embedding chapter-timed animations in Video AI Editor Remotion episodes.
---

# HyperFrames Motion Graphics

**Scope:** local, first-class HyperFrames-to-Remotion integration. This skill
does not install HyperFrames, use HeyGen Cloud, or promise an end-to-end episode.
Read `AGENTS.md`, `docs/PRODUCTION_POLICY.md`,
`docs/HYPERFRAMES_PRODUCTION.md`, and the character registry first.
For general Remotion implementation also load `remotion-markup` or
`remotion-render`; this skill owns only the local integration workflow.

## Existing source of truth

- Pinned `hyperframes` and `gsap` versions: `package.json` and lockfile.
- Editable original HTML/GSAP fixture: `hyperframes/projects/kinetic-intro/index.html`.
- Asset preparation and deterministic local renderer:
  `scripts/prepare-hyperframes.mjs`, `scripts/render-hyperframes.mjs`.
- Chapter bridge: `src/episodes/EpisodeProduction.tsx`.
- Integration contract: `docs/HYPERFRAMES_PRODUCTION.md`.

## Workflow

1. Inspect the current chapter, narrative cue, existing visual design, and
   approved media before writing scene-specific **original** HTML/GSAP motion.
2. Keep motion on a seekable timeline; use local GSAP assets, not a remote CDN.
3. On Node.js 22+ with FFmpeg and FFprobe available, run:
   ```bash
   npm ci
   npm run hyperframes:lint
   npm run hyperframes:render
   node --test tests/hyperframes-bridge.test.cjs
   ```
4. Inspect the actual staged file under `public/hyperframes/` and verify H.264,
   1920x1080, 30 fps, frame count and decodability before reuse. The supplied
   2-second fixture is a proof, **not** a completed production episode.
5. Embed only approved **local** `public/hyperframes/*.mp4` clips using the
   `EpisodeProduction.motionGraphics` input keyed by a real chapter ID.
   `startFrame` and `durationFrames` are **chapter-local** and must fit
   inside its duration; valid layouts are `inset` and `fullscreen`.
   Graphics are muted so they never replace the approved narration.
6. Check the embedded Remotion still and actual encoded episode fixture
   (see `.github/workflows/hyperframes-remotion-production.yml`).
   Inspect composition, chapter timing, cropping and audio after integration.

## Boundaries

Local rendering only. Never run `hyperframes cloud render`,
`hyperframes publish`, or `hyperframes media-use`; never upload source media
or use paid provider APIs/GPU without explicit authorization. No automatic
character redesign, replacement voices, watermarks, published video, or merge
to main. If official HyperFrames skills are already installed by the setup
script, treat them as optional tool-specific guidance; **do not vendor copies**
or replace these project-specific guardrails.
