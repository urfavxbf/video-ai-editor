# Motion Graphics, Video and Audio — senior workflow

## Project policy has precedence
For video-ai-editor, read root `AGENTS.md`, `docs/PRODUCTION_POLICY.md`, `characters/registry.json` and `.claude/skills/ai-video-editor/SKILL.md` before deciding video language, character visuals, voices, poses, aspect ratio or frame rate. Preserve approved defaults. Do not silently replace voice identity, copyrighted assets or existing compositions.

## Creative direction
Translate the brief into audience, visual hierarchy, narrative arc, timing, typography, compositing strategy, color and motion language. Define scenes, source assets, transitions, audio beats, and safe areas. Keep text legible on phones and maintain intentional easing, motion continuity, rhythm, negative space and contrast. Avoid movement with no narrative purpose.

## Engineering pipeline
Check repository lockfiles and existing Remotion composition definitions. Prefer deterministic, frame-based animations driven by `useCurrentFrame()` and `interpolate()` rather than wall-clock timers. Avoid nondeterministic random values, remote unpinned assets and browser-dependent effects. For FFmpeg, probe streams with `ffprobe` before transcoding, specify frame rate, sample rate, pixel format, audio codec and output container, and verify mapping and timestamps.

## Rendering and quality assurance
Inspect representative still frames, transitions, captions and audio sync; ensure frame 0, boundaries, last frame and long-tail sections render. Inspect resolution, duration, frame rate, codec, audio peak/clipping, silence and black frames. Compare target platform specs. Use bounded render resolution/concurrency in Codespaces and note when GPU or paid services are unavailable. Do not claim a video is rendered unless the artifact exists and was inspected.

## Asset governance
Maintain exact references, license records, consent where required, source and generated asset provenance, and repeatable render parameters. Respect portrait or character identity constraints. Preserve source materials and never publish or upload media without authorization.

## Delivery checklist
Provide actual output path, duration, dimensions, fps, codecs, source dependencies, reproducibility command and verified playback or frame tests. Note any incomplete render or quality limitations explicitly.
