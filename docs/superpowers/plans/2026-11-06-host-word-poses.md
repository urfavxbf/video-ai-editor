# Host Word Poses Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement sequentially.

**Goal:** Produce an example of the newly supplied UrFavXBF using all nine poses and word-triggered glitches.
**Architecture:** Original JPEG viewports preserve the supplied art; a deterministic word schedule drives a reusable host component. Local Jasper generation and local Whisper estimates bind the schedule to actual audio.
**Tech Stack:** Remotion 4.0.522, React, Python, Kitten ONNX, faster-whisper, FFmpeg.
**Spec:** docs/superpowers/specs/2026-11-06-host-word-poses-design.md

## Global Constraints
1920×1080, 30 fps, English, CPU only; no remote speech processing or GitHub publication. Glitches confined to character, three frames. Preserve completed showreel.

## Review Focus
Missing audio must fail delivery; ASR omissions must fail word alignment; successive words need distinct poses; all nine poses must survive actual rendering; clipped source viewports must exclude sheet labels and adjacent artwork.

### Task 1: Stage exact art and real narration
- [x] Record source JPEG hash and nine bounded viewports.
- [x] Generate short Jasper phrases, transcribe actual PCM locally, reject word mismatches, concatenate and record word estimates with hashes.

### Task 2: Implement word performance
- [x] Add schedule validation tests for nine-pose coverage, ordering, minimum holds and distinct adjacent poses.
- [x] Implement reusable sprite viewport and deterministic three-frame glitch; register WordPoseHostDemo.
- [x] Typecheck and run relevant tests; render representative and boundary frames.

### Task 3: Deliver example
- [x] Render actual MP4, loudness-master, fully decode, verify streams and caption/pose coverage; review independent code feedback.
- [x] Package source/JPEG/timing/audio with provenance; upload MP4 and archive to authorized Drive, verify metadata, report links and limitations accurately.
