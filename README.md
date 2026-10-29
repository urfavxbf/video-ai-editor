# Video AI Editor

> **Current character models (October 29, 2026):** Two original, zero-budget procedural 3D models now exist as [UrFavXBF glTF](public/characters/3d/urfavxbf.gltf) and [PIX glTF](public/characters/3d/pix.gltf), with independent hierarchical joints and 10 baked animation clips each. Their [source generator](scripts/build-3d-models.mjs) is reproducible and uses no paid services. The former 2D PNG production-model paths were placeholders, have been retired from the active character registry, and are **not** the default. This is an initial geometric 3D pass, not yet owner-approved identity-perfect artwork or an integrated 3D Remotion video composition. See [3D implementation and limitations](docs/RIGGED_3D_CHARACTERS.md).

> **Current production setting (October 28, 2026): English voices are the default.** The user paused Tagalog voice synthesis because there is no budget for a GPU runner. Use the previously approved Chatterbox English speakers: UrFavXBF Natural Storyteller and PIX Emily. Keep VoxCPM2 Tagalog voice designs and source code for future explicit opt-in only. The Tagalog GitHub Actions workflow is manual-only; no automatic TTS generation or paid GPU runner is authorized. Earlier references below to Tagalog being the default describe the prior experimental configuration and are superseded by this setting.

**Video AI Editor** is an independent video-editing workspace maintained in [urfavxbf/video-ai-editor](https://github.com/urfavxbf/video-ai-editor), built around Remotion motion graphics and FFmpeg processing, with **16:9 cinematic long-form YouTube episodes** as the default for new UrFavXBF + PIX productions. Existing vertical clips and Shorts are retained as legacy examples.

## Production direction (new content)

**Tagalog/Taglish is the default for new original videos**: scripts, narrator dialogue, motion-graphic labels, captions and YouTube titles/descriptions. Approved character voice designs are **Neon Storyteller** (UrFavXBF) and **Pixel Spark** (PIX) using VoxCPM2 text-based voice design. **English remains an explicit option** via the existing Chatterbox V3 speaker presets (`--language en`). The two new Tagalog presets are approved *descriptions*, not yet auditioned voice WAVs. See [multilingual production policy](docs/MULTILINGUAL_PRODUCTION_POLICY.md).

## Default new-video format

**Long-form YouTube videos • 16:9 widescreen • 1920 × 1080 • 30 fps.** No fixed Short runtime; write a chaptered, dialogue-led episode appropriate to the subject. Use character interaction, the 21 Remotion effects selectively, scene-specific advanced motion graphics and reliable Chatterbox speaker/caption synchronization. Preserve the old 9:16 demos without treating them as production templates.

## Larger portraits + next episode candidate

Owner requested enlarging **both** already-approved animated pixel-glitch face portraits: now **414 × 468 px** (from 306 × 346), on a 1920 × 1080 video with balanced side placements, unobstructed center HUD/captions, and no full bodies. Shared settings: [portraitLayout.ts](src/characters/portraitLayout.ts). Proposed next topic: [The 2038 Problem — The Day Computers Travel Back to 1901](docs/episodes/y2038.md), an evidence-checked 7–9-minute chaptered technology mystery. The [Y2038Teaser](src/episodes/Y2038Teaser.tsx) composition uses a visual countdown plus numeric overflow tied to subtitle cues.

## New default layout — animated portraits only

The owner reviewed the Pixel Glitch sample and requested that **full-body overlays be removed from new videos**. Only the **two animated head portraits** may appear at the left/right of the 16:9 data-and-caption HUD. Keep the separate approved UrFavXBF and PIX expression sprites, voice-driven talk states, neon outlines, and high-contrast glitch details. **Do not insert full-body sprite layers or their bottom nameplates** into the new video timeline.

Use `src/characters/PixelGlitchPortrait.tsx` and the registered `PixelPortraitHUD` composition. See [portrait-only layout policy](docs/PIXEL_GLITCH_PORTRAITS_ONLY.md). The earlier full-body sample is a historical artifact; it is not the current default.

## Official V2 visual style — super-pixel / glitch

The owner has approved new **highly pixelated, neon glitch** designs for UrFavXBF and PIX. The separated transparent avatar PNGs, 12 expression portraits, 48 talk/idle/reaction frames, six character glitch variants and reusable VFX overlays are saved in the owner's ChatGPT Library at `/UrFavXBF Video Characters/Pixel Glitch V2/`. **The ZIP media binaries are not yet committed to GitHub**. `characters/registry.json` now records this V2 as the preferred visual version while retaining V1 for older episodes.

Use `src/characters/PixelGlitchSprite.tsx` for frame-driven Remotion talking/idle/reaction loops, after staging `public/characters/pixel-glitch/` from the ZIP. Previously verified English Chatterbox voice identities remain available as legacy options; new Tagalog voice designs are saved separately. [Read the pack guide](docs/PIXEL_GLITCH_CHARACTER_PACK.md).

## Official characters — UrFavXBF and PIX

This repository is the AI-operated video production workspace for the recurring duo **UrFavXBF** (main host) and **PIX** (his talking AI cat companion). UrFavXBF covers wisdom, science, mathematics, internet culture, AI and video editing; this is **not a science-only project**. PIX is an inquisitive, playful, cute female-voiced AI sidekick. Both characters speak **Tagalog/Taglish by default**, with an opt-in English option.

- **UrFavXBF**: neon pixel-glitch human portrait in black/yellow; default **Neon Storyteller** Filipino voice-design preset `urfavxbf-neon-storyteller-tl-v1` on VoxCPM2; original Chatterbox English narrator preserved.
- **PIX**: cyan/lavender pixel-glitch AI cat portrait; default **Pixel Spark** female Filipino voice-design preset `pix-pixel-spark-tl-v1` on VoxCPM2; original Chatterbox Emily reference preserved for English.
- **Voice samples**: existing verified [UrFavXBF English](https://github.com/urfavxbf/video-ai-editor/actions/runs/40607467395) and [PIX English](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831) WAVs. No Tagalog character WAVs have been verified yet.
- **Assets**: the two original transparent PNGs plus audio samples and a ZIP pack are saved to the owner's persistent **ChatGPT Library** under `/UrFavXBF Video Characters/`. These binary images are **not yet committed to GitHub**; [character registry](characters/registry.json) specifies required names and SHA-256 checksums for staging assets into `public/characters/` in a render workspace.

**Production quality standard:** [advanced motion graphics + the 21 Remotion FX + character animation + Chatterbox voice accuracy](docs/PRODUCTION_STANDARD.md) must guide new video creation. A prior first long-form episode was **“Is the Internet Becoming a Ghost Town?”** with English dialogue between UrFavXBF and PIX, an expanded evidence-based narrative, interactive internet/AI graphics, and checked facts. The **21 effects are distinct from the 13 CineForge agent skills**; choose effects for storytelling rather than cramming all 21 into each Short.

See [official character setup](docs/OFFICIAL_CHARACTERS.md) and [PIX voice guide](docs/PIX_VOICE.md). The existing test/demo compositions remain for regression purposes; they do not define the project's subject or host.

## Character animation v2 — active priority

Based on the owner's Ghost Town pilot feedback, character animation is now the **first improvement**, before caption-and-data fusion. The current implementation adds a [speaker-aware 2.5D Remotion character puppet](src/characters/CharacterPuppet.tsx), a [1920×1080 animation workbench](src/characters/CharacterAnimationLab.tsx), and a [real-WAV motion envelope extractor](scripts/extract_voice_envelope.py). These are **not 3D skeletal rigs or verified lip-sync**; the canonical PNGs must be staged from the owner's asset Library.

The next visual pass will integrate **verified data directly into animated captions**, tied to actual word timestamps, rather than stacking independent infographic and subtitle panels. See [Animation V2 roadmap](docs/CHARACTER_ANIMATION_V2.md) for capabilities, delivery gates, and the proper `@remotion/three` + GLB / Blender rig path to real 3D characters.

## Included
- **18-second original Remotion product reel** with kinetic typography, podcast mockups, Tagalog caption animation and stack overview. Run `npm run render:repo-showcase`; see [showcase guide](docs/SHOWCASE.md).
- **21 Remotion motion effects**: Snap Zoom, Headline Storm, Liquid Glass, Frame Escape, Paper Cutout, Magazine Cover, Split and more.
- **Video editing compositions** in `src/edit/` with a JSON cut list.
- **Effects source code** in `src/fx/` with fonts, textures and sound effects in `public/`.
- **Groq transcription helper** in `scripts/groq_transcribe.py` for Tagalog/Taglish captions.
- **Default character narration: VoxCPM2 Tagalog/Taglish voice design** for UrFavXBF and PIX using `scripts/character_voiceover.py`; the approved English Chatterbox Natural Storyteller and Emily speakers remain usable with `--language en`. See [language/voice setup](docs/MULTILINGUAL_PRODUCTION_POLICY.md) and [legacy Chatterbox guide](docs/CHATTERBOX_TTS.md). Chatterbox itself does not officially support Tagalog.
- **AI editing workflows and Claude skill** in `.claude/skills/ai-video-editor/`.
- **12 official Remotion Agent Skills** in `.claude/skills/remotion-*/` (full source/reference files, pinned official import). See [the Remotion skills guide](docs/REMOTION_SKILLS.md).
- **CineForge Pro all-in-one Skill** in [`.claude/skills/cineforge-pro/SKILL.md`](.claude/skills/cineforge-pro/SKILL.md): one portable skill merging the 12 official Remotion skill bodies and our professional `ai-video-editor` skill. The original 13 directories remain for auditing and maintenance; run `python3 scripts/build-cineforge-master-skill.py` to rebuild the master file.
- **7 official Remotion feature packages**, including captions, transitions, shapes, effects, motion blur, SFX and Player, with a working `OfficialFeaturesDemo` composition. See [feature details](docs/REMOTION_FEATURES.md).
- **CI smoke tests** and dependency installation scripts.

## Default Tagalog character voiceover

```bash
# Optional runtime: pip install -r requirements-voxcpm.txt
python scripts/character_voiceover.py --character urfavxbf \
  --text "Alam mo ba, PIX? May sikreto sa likod ng internet." \
  --output out/urfavxbf-tl.wav
python scripts/character_voiceover.py --character pix \
  --text "Hala, seryoso?! Tara, alamin natin!" \
  --output out/pix-tl.wav
# Model-free verification of prompt/chunk routing:
python scripts/character_voiceover.py --character pix \
  --text "Kamusta!" --output out/preview.wav --dry-run
# Original verified English voices remain opt-in:
python scripts/character_voiceover.py --character pix --language en \
  --text "Let's find out!" --output out/pix-en.wav
```

The default Tagalog TTS model requires model downloads and GPU-class compute for practical rendering.
These are voice design prompts, not pre-rendered or auditioned Tagalog speaker samples.
The workflow does not automatically publish videos.

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
