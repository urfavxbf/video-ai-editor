# Codex-native OpenMontage Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement task by task. Steps use checkbox syntax.

**Goal:** Deliver issue #60's verified audit and the smallest tested execution route.
**Architecture:** Thin adapter over pinned upstream tools/persistence; Codex remains the agent.
**Tech Stack:** Existing Python, Remotion, FFmpeg, GitHub Actions; no new host dependencies.
**Spec:** `docs/superpowers/specs/2026-10-31-openmontage-codex-design.md`

## Global Constraints

- Pin `195eab24478dc9363326aec437aefc3701635ddf`; no vendored upstream code.
- English approved Chatterbox voices; approved assets unchanged; 1920×1080/30 fps.
- No paid API/GPU, extra AI-agent requirement, secrets, publishing, main push or merge.
- Preserve upstream approval gates and runtime lock; fixture is not an episode.

## Review Focus

- Edited artifacts or media after approval must invalidate execution.
- Path traversal/symlinks and malformed/non-finite timings must fail before tools.
- Unsupported creative instructions must not be silently dropped.
- Installed tools and service reachability must not be conflated.
- Fixture tone/test patterns must never be presented as approved narration/footage.

### Task 1: Audit and bounded adapter

Files: audit/design/plan, `integrations/openmontage/scripts/production.py`,
`integrations/openmontage/tests/test_production.py`.
Consumes pinned manifest/schema/checkpoint/tool APIs; produces preflight/init/
checkpoint/render commands and validated cinematic transport inputs.

- [x] Reproduce install/doctor, discovery, network/voice blockers, 64 upstream tests.
- [x] Write failing guard/schema/gate/media/timing tests; confirm failures.
- [x] Implement minimal adapter; test valid inputs and each rejected input class.
- [x] Run all host tests; record results and commit focused change.

### Task 2: New motion proof, access documentation and CI

Files: `integrations/openmontage/tests/production_fixture.py`, integration README,
new integration AGENTS.md, existing `.github/workflows/openmontage-integration.yml`.
Consumes Task 1 commands; produces real fixture MP4/SRT/QA/frames in ignored runtime.

- [x] Add real fixture execution with gate simulation labeled fixture-only.
- [ ] Run actual 1080p motion/audio/caption render and inspect output frames/probe.
- [x] Extend existing isolated smoke artifact; document native Codex task and blockers.
- [ ] Run existing safety gate, independent branch review and GitHub Actions.
- [ ] Open dedicated PR against main with audit, test evidence and actual limitations.
