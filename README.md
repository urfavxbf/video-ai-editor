# Video AI Editor

A Remotion/TypeScript + FFmpeg/Python AI video-production workspace.
It is not an Android app.

## Current approved production settings

Read [the current production policy](docs/PRODUCTION_POLICY.md) and
[characters/registry.json](characters/registry.json) before planning. The latest
explicit user instruction governs the request; otherwise current registry values
win over historical examples and superseded policy bodies.

- **English (en)** for script, narration, captions, graphics and metadata.
- **Long-form, 16:9, 1920×1080, 30 fps**; runtime follows script and chapters.
- **13 committed approved pixel poses**: UrFavXBF (6) and PIX (7), with original
  transparent PNGs and SHA-256 fingerprints in the [asset manifest](characters/pixel-default-manifest.json).
- **HeroCharacterStage** is the default full-body pixel-pose/2.5D composition.
  **PixelProductionProof** is the existing model-free artwork proof.
- English Chatterbox V3 voices stay **Natural Storyteller** for UrFavXBF
  (`natural-storyteller-v1`) and **Emily** for PIX (`pix-cute-female-emily-v1`).
- Tagalog/VoxCPM2 is **on hold, opt-in only**. No paid API/GPU usage or
  replacement/rejected art is authorized by the default workflow.

Verify the actual checkout with:

```bash
python3 scripts/stage_pixel_default_pack.py --verify-workspace
```

The approved images are already in the repository; no manual Library upload is
needed for the default art. Voice synchronization, word alignment and episode
content still require actual audio and audiovisual QA. Artwork readiness does
not mean that a voiced episode or real lip-sync has been delivered.

If new English narration is authorized, use the existing character CLI with
`--language en --device cpu` and the optional Chatterbox runtime. Reuse approved
WAVs where available; do not silently switch speakers or generate Tagalog audio.
See [English policy](docs/ENGLISH_PRODUCTION_POLICY.md),
[character identities](docs/OFFICIAL_CHARACTERS.md), and
[production quality](docs/PRODUCTION_STANDARD.md).

## AI agent operating policy and copy-ready prompts

**Start with [AGENTS.md](AGENTS.md)** — the primary operating instructions for
every AI coding/production agent. The authoritative default format, approved
voices and approved assets remain in
[docs/PRODUCTION_POLICY.md](docs/PRODUCTION_POLICY.md),
[characters/registry.json](characters/registry.json) and
[characters/pixel-default-manifest.json](characters/pixel-default-manifest.json).

Use the [AI agent prompt playbook](docs/AI_AGENT_PROMPTS.md) to request a new
episode, reference-inspired video, supplied-footage edit, one of 21 effects,
approved English voiceover, transcript/captions, Lottie or Duik import, or
production QA. All templates require real evidence before claiming delivery;
copying a prompt never authorizes external uploads, paid services, GPU usage,
publishing, or a merge to main.

## Agent entrypoints and historical work

Codex reads [AGENTS.md](AGENTS.md). The active production skill is
[ai-video-editor](.claude/skills/ai-video-editor/SKILL.md); the generated
[CineForge Pro](.claude/skills/cineforge-pro/SKILL.md) includes that same guidance
plus the 12 imported Remotion skills. Rebuild it with
`python3 scripts/build-cineforge-master-skill.py` after changing its source.
The root [video-effects skill](SKILL.md) covers explicitly requested supplied
9:16 footage; it does not set defaults for new original episodes.

The 21 existing FX remain available, selected for storytelling rather than
forced into every video. Historical portrait/V2 layouts and Tagalog voice
designs remain in [the archive-scoped policies](docs/MULTILINGUAL_PRODUCTION_POLICY.md)
and [portrait-only reference](docs/PIXEL_GLITCH_PORTRAITS_ONLY.md) for explicit
reproduction. They do not supersede current defaults. Generic imported skills
supply framework techniques, not a different project identity.

## One-click Codespaces setup (Android / browser)

Create a Codespace from the `main` branch using **Code → Codespaces → Create codespace on main**. The committed `.devcontainer/devcontainer.json` installs the full editing toolchain automatically. After initialization, run:

```bash
bash scripts/check-codespace.sh
```

See [Codespaces setup and Groq secrets](docs/CODESPACES_SETUP.md) for Android-friendly steps. Codespaces and Groq usage can consume plan quotas.

## Quick start

```bash
npm ci
npm run typecheck
npm run studio
# Preview the 21 motion effects
npm run render:showcase
# Render an edit configured in src/edit/edit.json
npm run render:edit
```

Install FFmpeg separately. See [AI editing setup](docs/AI_VIDEO_TOOLS.md) for Groq and HyperFrames configuration. Some subject-masking steps currently require macOS / Apple Vision; Android/Codespaces and Linux need a different segmentation provider for those specific effects. This repository is an editing toolkit, not yet an end-to-end one-tap automated video service.

## Provenance and licenses

**Video AI Editor is not published under a repository-wide MIT license.** Its custom application and newer video compositions are distinct from the Remotion framework and from the effects source that was imported earlier.

The initial 21-effect library was imported from [urfavxbf/video-effects-mobile](https://github.com/urfavxbf/video-effects-mobile), originally derived from [JesseEisenbart/video-effects-skill](https://github.com/JesseEisenbart/video-effects-skill). The required MIT notice for the applicable imported source code is preserved **only as a third-party notice** in [licenses/video-effects-skill-MIT.txt](licenses/video-effects-skill-MIT.txt). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the license scope, separate font and audio asset notes, and the archived [upstream README](docs/UPSTREAM_README.md).

[Remotion](https://github.com/remotion-dev/remotion) is the independent video framework used as an npm dependency. It has its **own license** ([official Remotion license](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)); it is **not** relicensed by this project.

This repository is not a GitHub fork of either upstream repository. Refer to Git history and the links above for provenance.
