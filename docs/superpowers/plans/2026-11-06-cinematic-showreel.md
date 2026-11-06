# Cinematic Showreel Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; the owner requested immediate execution.

**Goal:** Deliver the approved original widescreen reel with all effects, approved characters and English voices.
**Architecture:** A pure timeline manifest schedules typed widescreen effect variants around an intro/outro. Original character scenes are the source for effects; an offline asset preparation script measures WAVs and generates an original score/envelope. Delivery rendering requires real audio assets.
**Tech Stack:** Existing Remotion 4.0.522, React, TypeScript, Python, FFmpeg, approved CPU Chatterbox V3.
**Spec:** docs/superpowers/specs/2026-11-06-cinematic-showreel-design.md

## Global Constraints
1920×1080, 30 fps; 60–90 seconds; exact approved PNGs; independent approved English voices; all 33 effects; no paid services, external processing or publication; preserve existing compositions.

## Review Focus
- Effect coverage must remain synchronized with both existing registries.
- Voice intervals must use measured WAV durations and fit their slots.
- Both character pose sets must remain valid and fully exercised.
- Render cannot silently succeed with missing narration or use fake speech waveforms.
- Every effect must visibly change the original scene at landscape dimensions.

### Task 1: Timeline and acceptance contract
Files: src/showcase/showreelTimeline.ts, tests/showreel.test.cjs.
- [x] Write and run failing coverage, contiguity, duration and unknown-ID tests.
- [x] Implement typed timeline, pose selection, clip schedule and validator.
- [x] Run timeline tests and typecheck.

### Task 2: Widescreen visual composition
Files: src/showcase/CinematicShowreel.tsx, src/showcase/ShowreelScene.tsx, src/showcase/ShowreelEffects.tsx, src/Root.tsx.
Consumes the timeline and produces the CinematicShowreel composition.
- [x] Implement original scenes and 33 explicitly mapped landscape FX variants.
- [x] Register without changing legacy composition behavior.
- [x] Render representative stills; inspect layout, pose coverage and transitions.

### Task 3: Actual audio and reproducible delivery
Files: scripts/prepare_showreel.py, src/showcase/showreel-audio.json, package.json, docs/CINEMATIC_SHOWREEL.md.
Consumes approved local generated WAVs and emits a measured audio manifest plus original score/envelope in ignored public/voiceovers/showreel.
- [x] Generate approved host/PIX voice lines on CPU and inspect actual WAVs.
- [x] Validate durations, generate original score and measured envelope, and refuse missing voice assets.
- [x] Render full MP4; probe, decode, inspect frames and audio playback where available.
- [x] Run relevant regression suites and record actual results and any playback limitations.

Execution complete as a review render. Manual listening/name-pronunciation and full-speed aesthetic review remain explicitly pending; see docs/CINEMATIC_SHOWREEL_VERIFICATION.md. Remote GitHub publication is blocked pending explicit owner push permission.
