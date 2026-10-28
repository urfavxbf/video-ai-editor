# Official UrFavXBF and PIX — production character bible

**Approved 2026-10-28.** The project's main topic is the character **UrFavXBF**, a creator and knowledgeable explorer of wisdom, science, math, the internet, AI, and editing. This is not a science-only content project. New original video dialogue, narration, screen text, captions and metadata are **Tagalog/Taglish by default**; English is optional per production.

The second recurring character is **PIX**, UrFavXBF's cute, talking female-voiced AI pet. PIX is a bright, curious robotic cat who can question UrFavXBF, joke with him, and explain concepts alongside him. PIX does not replace the main host.

## Visual version update — super-pixel glitch V2

The owner approved the **super-pixelated, high-contrast glitch** appearances. Use the separately extracted V2 sprite pack as the preferred appearance for **new** episodes. Keep prior v1 images for replaying earlier footage and do not silently claim a 3D rig.

The V2 full-body characters, expressions and talk/idle/react loops are in the owner's ChatGPT Library: `/UrFavXBF Video Characters/Pixel Glitch V2/`. See [the asset pack guide](PIXEL_GLITCH_CHARACTER_PACK.md) and the registry's `preferred_visual_variant` field. The previously verified Chatterbox **English** voices remain unchanged. The new **default Tagalog** voice-design profiles use VoxCPM2; neither has a verified recorded Tagalog sample yet.

## Canonical visual identity

| Character | Appearance | Reusable overlay file |
|---|---|---|
| UrFavXBF | Pixelated young man, black and bright yellow high-contrast streetwear, messy black hair, backpack, black/yellow shoes. | `UrFavXBF_Transparent.png` |
| PIX | Friendly white/black robotic cat, yellow tech hoodie, blue/cyan glowing details, headset. | `PIX_Transparent.png` |

These PNGs have **real transparent alpha channels**, and their exact dimensions and SHA-256 fingerprints are frozen in [the machine-readable registry](../characters/registry.json). Do not change the characters' costumes, color identities, or face shapes casually between videos.

### Where the original binary assets are saved

The owner's persistent **ChatGPT Library** holds the official downloadable pack and individual assets at `/UrFavXBF Video Characters/`:
- `UrFavXBF_Transparent.png`
- `PIX_Transparent.png`
- `UrFavXBF_Chatterbox_Natural_Storyteller_Sample.wav`
- `PIX_Chatterbox_V3_Emily_Sample.wav`
- `CHARACTERS.json`
- `UrFavXBF_PIX_Official_Character_Pack.zip`

**Important:** These images and audio samples are **saved to ChatGPT Library but not committed as binary files to this GitHub repository**. Download the pack into your editor/Codespace environment, then copy the PNGs to `public/characters/` under exactly the filenames above to use them as Remotion `staticFile` overlay sources. GitHub Actions runners cannot access your private ChatGPT Library automatically.

These are **still assets**, not a rigged/animated talking character or working lip-sync system. Chatterbox dialogue WAVs and motions still need to be sequenced by the video editor.

## Canonical voice mapping

| Character | New default (Tagalog/Taglish) | Legacy English |
|---|---|---|
| UrFavXBF | VoxCPM2 `urfavxbf-neon-storyteller-tl-v1` — **Neon Storyteller**, warm medium-low Filipino male voice-design description | Chatterbox V3 `natural-storyteller-v1` built-in |
| PIX | VoxCPM2 `pix-pixel-spark-tl-v1` — **Pixel Spark**, bright playful adult-sounding Filipino female voice-design description | Chatterbox V3 `pix-cute-female-emily-v1` consent-cleared synthetic reference |

See [`characters/registry.json`](../characters/registry.json) for the precise approved
VoxCPM2 voice-design prompts. The text descriptions are approved, but **no Tagalog
WAV or stable speaker embedding has been rendered/auditioned yet**. The previous
[UrFavXBF](https://github.com/urfavxbf/video-ai-editor/actions/runs/40607467395) and
[PIX](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831)
samples validate only the historical **English** voices.

Tagalog synthesis (default; needs optional VoxCPM2 runtime and model weights):

```bash
python scripts/character_voiceover.py --character urfavxbf --text "Alam mo ba, PIX?" --output out/urfavxbf-tl.wav
python scripts/character_voiceover.py --character pix --text "Hala, seryoso?!" --output out/pix-tl.wav
```

English remains available via `--language en` and Chatterbox dependencies.
See [multilingual production policy](MULTILINGUAL_PRODUCTION_POLICY.md) for setup and
commercial-use/consent requirements. No model weights or generated WAVs are committed.

## Animation improvement priority

The owner requested stronger animation following the completed Ghost Town pilot: show more head/ear/tail motion, expressive gestures, speaker reactions and voice-driven timing. Keep the official visual identities unchanged and preserve both historical English Chatterbox speaker presets; default to the new Tagalog voice designs. The current Remotion [CharacterPuppet](../src/characters/CharacterPuppet.tsx) is a 2.5D stepping stone; true 3D models require approved volumetric meshes, skeletons and facial rigs. See [CHARACTER_ANIMATION_V2.md](CHARACTER_ANIMATION_V2.md). Fusion of data and captions is the next step after character animation.

## Production quality standard and pilot

For all new videos, follow [the advanced motion/animation/voice QA standard](PRODUCTION_STANDARD.md). The first **widescreen long-form** episode concept is **“Is the Internet Becoming a Ghost Town?”** (English, 16:9 / 1920 × 1080 / 30 fps, two speakers, an expanded chaptered narrative, cinematic pixel-art character overlays on realistic backgrounds, interactive animated internet/AI graphics). Episode runtime is story-driven, not ~40–50 seconds. The studio has **21 effects** and **13 agent skills**; only use those effects that add visual meaning. Real mouth/viseme lip sync requires actual sprites or a rig and is not supplied by the two static transparent PNGs alone.

## Video editing policy

An AI agent is the editor: choose story beats, cue effects and camera moves, apply each character's **own** overlay and **own** voice. Keep both roles consistent, avoid repeatedly stacking effects, and do not switch who is speaking without matching the narration. Preserve third-party source dialogue and ask for permission before translating/revoicing it. Never upload to YouTube without explicit authorization.
