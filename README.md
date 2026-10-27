# Video AI Editor

**Video AI Editor** is an independent video-editing workspace maintained in [urfavxbf/video-ai-editor](https://github.com/urfavxbf/video-ai-editor), built around Remotion motion graphics and FFmpeg processing for vertical videos, podcast clips and Shorts.

## Included
- **21 Remotion motion effects**: Snap Zoom, Headline Storm, Liquid Glass, Frame Escape, Paper Cutout, Magazine Cover, Split and more.
- **Video editing compositions** in `src/edit/` with a JSON cut list.
- **Effects source code** in `src/fx/` with fonts, textures and sound effects in `public/`.
- **Groq transcription helper** in `scripts/groq_transcribe.py` for Tagalog/Taglish captions.
- **AI editing workflows and Claude skill** in `.claude/skills/ai-video-editor/`.
- **12 official Remotion Agent Skills** in `.claude/skills/remotion-*/` (full source/reference files, pinned official import). See [the Remotion skills guide](docs/REMOTION_SKILLS.md).
- **7 official Remotion feature packages**, including captions, transitions, shapes, effects, motion blur, SFX and Player, with a working `OfficialFeaturesDemo` composition. See [feature details](docs/REMOTION_FEATURES.md).
- **CI smoke tests** and dependency installation scripts.

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
