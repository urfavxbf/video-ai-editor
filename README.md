# Video AI Editor

**Video AI Editor** is an independent video-editing workspace maintained in [urfavxbf/video-ai-editor](https://github.com/urfavxbf/video-ai-editor), built around Remotion motion graphics and FFmpeg processing for vertical videos, podcast clips and Shorts.

## Included
- **21 Remotion motion effects**: Snap Zoom, Headline Storm, Liquid Glass, Frame Escape, Paper Cutout, Magazine Cover, Split and more.
- **Video editing compositions** in `src/edit/` with a JSON cut list.
- **Effects source code** in `src/fx/` with fonts, textures and sound effects in `public/`.
- **Groq transcription helper** in `scripts/groq_transcribe.py` for Tagalog/Taglish captions.
- **AI editing workflows and Claude skill** in `.claude/skills/ai-video-editor/`.
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

This repository is a standalone copy of [urfavxbf/video-effects-mobile](https://github.com/urfavxbf/video-effects-mobile), based on the MIT-licensed original [JesseEisenbart/video-effects-skill](https://github.com/JesseEisenbart/video-effects-skill). Original authorship is credited in [LICENSE](LICENSE) and the [upstream README](docs/UPSTREAM_README.md). The original MIT terms and copyright notice must stay intact. Bundled fonts are governed separately by [SIL OFL](public/fonts/OFL.txt). Remotion itself has separate licensing conditions.

This repository is **not** a GitHub fork of the upstream repository. Original history remains available at the links above.
