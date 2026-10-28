# Official UrFavXBF and PIX — production character bible

**Approved 2026-10-28.** The project's main topic is the character **UrFavXBF**, a creator and knowledgeable explorer of wisdom, science, math, the internet, AI, and editing. This is not a science-only content project. All new original video dialogue, narration, screen text, captions and metadata are **English only**.

The second recurring character is **PIX**, UrFavXBF's cute, talking female-voiced AI pet. PIX is a bright, curious robotic cat who can question UrFavXBF, joke with him, and explain concepts alongside him. PIX does not replace the main host.

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

| Character | Chatterbox Multilingual V3 voice | How selected |
|---|---|---|
| UrFavXBF | `natural-storyteller-v1` | Built-in V3 speaker, `0.5` exaggeration, `0.5` CFG |
| PIX | `pix-cute-female-emily-v1` | Pinned synthetic female Emily reference, `0.65` exaggeration, `0.35` CFG |

Both language IDs are `en`. Both voice identities have **successfully rendered real audio samples**: [UrFavXBF](https://github.com/urfavxbf/video-ai-editor/actions/runs/40607467395), [PIX](https://github.com/urfavxbf/video-ai-editor/actions/runs/40614959831). A validated WAV is not a guarantee of natural expressive delivery or complete end-to-end video production; QC listening and video export checks remain necessary.

Generate a fresh character-specific line with Chatterbox installed:

```bash
python scripts/character_voiceover.py --character urfavxbf \
  --text "Hey PIX, ready to explore something new?" --output out/urfavxbf.wav
python scripts/character_voiceover.py --character pix \
  --text "Always! I've already got three questions!" --output out/pix.wav
```

PIX's source recording is an openly available synthetic voice reference with MIT [attribution and provenance](PIX_VOICE.md). Do not use unrelated private recordings or claim that the same waveform is guaranteed across synthesis attempts.

## Production quality standard and pilot

For all new videos, follow [the advanced motion/animation/voice QA standard](PRODUCTION_STANDARD.md). The first **widescreen long-form** episode concept is **“Is the Internet Becoming a Ghost Town?”** (English, 16:9 / 1920 × 1080 / 30 fps, two speakers, an expanded chaptered narrative, cinematic pixel-art character overlays on realistic backgrounds, interactive animated internet/AI graphics). Episode runtime is story-driven, not ~40–50 seconds. The studio has **21 effects** and **13 agent skills**; only use those effects that add visual meaning. Real mouth/viseme lip sync requires actual sprites or a rig and is not supplied by the two static transparent PNGs alone.

## Video editing policy

An AI agent is the editor: choose story beats, cue effects and camera moves, apply each character's **own** overlay and **own** voice. Keep both roles consistent, avoid repeatedly stacking effects, and do not switch who is speaking without matching the narration. Preserve third-party source dialogue and ask for permission before translating/revoicing it. Never upload to YouTube without explicit authorization.
