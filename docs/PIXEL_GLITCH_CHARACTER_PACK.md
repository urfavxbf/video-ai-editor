> **Current hero update (29 October 2026):** The two approved Super Pixel V2 **full-body** PNGs are now the default character identity for new videos. This supersedes the archived portrait-only directive below. The pack's 8-frame talk/idle/react loops contain **head-only** expressions, not articulated whole-body motion. See [the official hero bible](URFAVXBF_PIX_HERO_CHARACTER_BIBLE.md).

> **Update (28 October 2026):** The preferred production layout is now **animated head portraits only**. Do not show the full-body V2 sprites in new videos. See [the portrait-only policy](PIXEL_GLITCH_PORTRAITS_ONLY.md). The pack retains full-body originals as archived raw source material.

# Super Pixel / Glitch V2 — character asset pack

**Status:** Approved visual direction for future UrFavXBF + PIX videos. Previous v1 PNGs remain in the registry for reproducing older edits. **The two original Chatterbox V3 English voice profiles remain available for legacy work; the new Tagalog default uses separate VoxCPM2 Neon Storyteller / Pixel Spark text-based voice designs.**

## Saved binary assets

The full **V2 asset pack** is saved persistently in the owner's ChatGPT Library:

`/UrFavXBF Video Characters/Pixel Glitch V2/PixelGlitch_Complete_Pack.zip`

It contains:
- **Two transparent full-body RGBA base sprites**, one for each character, isolated from the pixel-art concept sheet.
- **12 individual expression portraits**, six per character: UrFavXBF (neutral, talk, excited, thinking, surprised, glitch); PIX (neutral, talk, happy, curious, surprised, glitch).
- **6 non-destructive full-body glitch variants** (RGB split, scanline and pixel burst, one of each per character).
- **48 isolated transparent loop frames**: each character gets talk (8), idle (8), react (8) at recommended 8/5/8 FPS, plus matching transparent sprite-sheet atlases.
- Four reusable, separate transparent glitch VFX layers; sprite manifest, contact sheet, source reference images, two real Chatterbox dialogue WAVs, a 23.5-second 1080p animated MP4 sample with AAC audio, and usage README.

All art is pixelated, high contrast: UrFavXBF in black/gold and PIX as a cyan/white digital cat. The images are genuine cutouts with alpha; they are **not** yet physically added to this GitHub repository.

The animation sample was generated in the ChatGPT workspace and independently checked with `ffprobe` at **1920×1080, 30 fps, H.264 video + AAC audio**. Its lips switch approximate mouth-expression portraits based on actual WAV RMS amplitude; **this is not phoneme-accurate lip-sync**. Captions are demonstration-level phrase timing, not professionally forced-aligned words. Motion is 2D sprite animation, not volumetric 3D.

## Using the pack with Remotion

1. Download/extract the official ZIP pack from ChatGPT Library.
2. Copy its `PixelGlitch_SpritePack/urfavxbf` and `PixelGlitch_SpritePack/pix` folders into `public/characters/pixel-glitch/`. Keep subfolder names and 00.png–07.png frame numbering.
3. The [`PixelGlitchSprite`](../src/characters/PixelGlitchSprite.tsx) component automatically plays the eight-frame loop, switches from idle to talk when a speaker event is active, and supports controlled glitch bursts. Example:

```tsx
<PixelGlitchSprite
  id="pix"
  right={120} bottom={50}
  width={380} height={380}
  voiceEvents={[
    {speaker: 'pix', startFrame: 80, endFrame: 170, rms: measuredRms, samplesPerSecond: 10}
  ]}
/>
```

`measuredRms` must come from a real WAV, e.g. `python scripts/extract_voice_envelope.py`. Never fabricate audio timing or speaker attribution. If no audio events are available, the sprite plays the `idle` animation.

For data+caption fusion, read approved transcripts with actual timestamps; animate the infographic and text highlight using the same cue. The provided demo is an aesthetic test, not a verified word-aligned caption production.

## Voice profile identity

UrFavXBF remains `natural-storyteller-v1` (Chatterbox Multilingual V3), and PIX remains `pix-cute-female-emily-v1`. Do not confuse the archived English voices with the approved new Tagalog VoxCPM2 default designs. No Tagalog voice WAVs have been auditioned yet.

## Versioning and continuity

- `characters/registry.json` now identifies `super-pixel-glitch-v2` as the preferred new visual version and records SHA-256 digests for the two new full-body base assets. The v1 avatar entries are preserved for prior renders.
- Current new original videos default to Tagalog/Taglish (English optional) and stay 16:9 / 1920×1080 / 30fps.
- The source sprite images are 2D pixel art. To obtain true skeleton animation and facial rigging, additional source layers or Blender/GLB models are required; see `docs/CHARACTER_ANIMATION_V2.md`.
- Avoid copying the visual style/source code from third-party creators. The pixel illustrations here were generated for this project's characters.
