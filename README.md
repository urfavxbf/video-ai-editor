# Video AI Editor

**Video AI Editor** is an independent video-editing workspace maintained in [urfavxbf/video-ai-editor](https://github.com/urfavxbf/video-ai-editor), built around Remotion motion graphics and FFmpeg processing, with **16:9 cinematic long-form YouTube episodes** as the default for new UrFavXBF + PIX productions. Existing vertical clips and Shorts are retained as legacy examples.

## Production direction (new content)

**English-only for new original videos**: scripts, narration, motion-design text, captions and publishing metadata. The approved English narrator is **Natural Storyteller** via Chatterbox Multilingual V3 (`natural-storyteller-v1`). Existing Tagalog/Taglish compositions remain unchanged as archived examples; this does not imply translating third-party footage or automatic publishing. See [English production policy](docs/ENGLISH_PRODUCTION_POLICY.md).

## Default new-video format

**Long-form YouTube videos • 16:9 widescreen • 1920 × 1080 • 30 fps.** No fixed Short runtime; write a chaptered, dialogue-led episode appropriate to the subject. Use character interaction, the 21 Remotion effects selectively, scene-specific advanced motion graphics and reliable Chatterbox speaker/caption synchronization. Preserve the old 9:16 demos without treating them as production templates.

## Official characters — UrFavXBF and PIX

This repository is the AI-operated video production workspace for the recurring duo **UrFavXBF** (main host) and **PIX** (his talking AI cat companion). UrFavXBF covers wisdom, science, mathematics, internet culture, AI and video editing; this is **not a science-only project**. PIX is an inquisitive, playful, cute female-voiced AI sidekick. Both characters speak **English**.

- **UrFavXBF**: transparent high-contrast pixel-art human overlay, black/yellow outfit; Chatterbox Multilingual V3 `natural-storyteller-v1` built-in English narrator.
- **PIX**: transparent white/black/yellow/cyan robotic-cat overlay; Chatterbox Multilingual V3 `pix-cute-female-emily-v1` female reference voice.
- **Voice samples**: real verified GitHub Actions WAVs ([UrFavXBF](https://github.com/urfavxbf/video-ai-editor/actions/runs/40607467395), [PIX](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831)).
- **Assets**: the two original transparent PNGs plus audio samples and a ZIP pack are saved to the owner's persistent **ChatGPT Library** under `/UrFavXBF Video Characters/`. These binary images are **not yet committed to GitHub**; [character registry](characters/registry.json) specifies required names and SHA-256 checksums for staging assets into `public/characters/` in a render workspace.

**Production quality standard:** [advanced motion graphics + the 21 Remotion FX + character animation + Chatterbox voice accuracy](docs/PRODUCTION_STANDARD.md) must guide new video creation. The agreed first long-form episode is **“Is the Internet Becoming a Ghost Town?”** with English dialogue between UrFavXBF and PIX, an expanded evidence-based narrative, interactive internet/AI graphics, and checked facts. The **21 effects are distinct from the 13 CineForge agent skills**; choose effects for storytelling rather than cramming all 21 into each Short.

See [official character setup](docs/OFFICIAL_CHARACTERS.md) and [PIX voice guide](docs/PIX_VOICE.md). The existing test/demo compositions remain for regression purposes; they do not define the project's subject or host.

## Included
- **18-second original Remotion product reel** with kinetic typography, podcast mockups, Tagalog caption animation and stack overview. Run `npm run render:repo-showcase`; see [showcase guide](docs/SHOWCASE.md).
- **21 Remotion motion effects**: Snap Zoom, Headline Storm, Liquid Glass, Frame Escape, Paper Cutout, Magazine Cover, Split and more.
- **Video editing compositions** in `src/edit/` with a JSON cut list.
- **Effects source code** in `src/fx/` with fonts, textures and sound effects in `public/`.
- **Groq transcription helper** in `scripts/groq_transcribe.py` for Tagalog/Taglish captions.
- **Default narrator: Natural Storyteller (approved Chatterbox Multilingual V3 built-in speaker)** for all English voice-overs, with long-form WAV export, optional consent-based reference voices, and a Remotion narration track. See [Chatterbox setup](docs/CHATTERBOX_TTS.md). Tagalog is not officially supported.
- **AI editing workflows and Claude skill** in `.claude/skills/ai-video-editor/`.
- **12 official Remotion Agent Skills** in `.claude/skills/remotion-*/` (full source/reference files, pinned official import). See [the Remotion skills guide](docs/REMOTION_SKILLS.md).
- **CineForge Pro all-in-one Skill** in [`.claude/skills/cineforge-pro/SKILL.md`](.claude/skills/cineforge-pro/SKILL.md): one portable skill merging the 12 official Remotion skill bodies and our professional `ai-video-editor` skill. The original 13 directories remain for auditing and maintenance; run `python3 scripts/build-cineforge-master-skill.py` to rebuild the master file.
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
