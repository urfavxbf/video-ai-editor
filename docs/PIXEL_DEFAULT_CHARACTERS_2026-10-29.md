# Default UrFavXBF × PIX pixel pose art — 2026-10-29

**The user selected the thirteen individual high-resolution pixel-art poses** based on the two owner-selected reference sheets. Treat these as the *only* default art for new episodes. Do not use the rejected geometric 3D prototypes or rejected old pose packs. Do not crop sprites from the presentation sheets.

- UrFavXBF: idle, talk, point_camera, point_side, happy, surprised (!).
- PIX: idle, curious, talk, point, happy, question (?), surprised (!).
- Original **1254 × 1254 RGBA PNG**, alpha-verified, one independent image per pose. Scaling: CSS `image-rendering: pixelated`, nearest-neighbor for integer enlargements, never bilinear-resample into soft sprites.
- Style: pixel-art chibi UrFavXBF in black/neon-green hoodie/X headphones; PIX is a fluffy cyan/lavender cat with blue/purple eyes, headphone X and luminous collar.
- Direction: cinematic 2.5D stage, pose swaps triggered by active speaker/listener actions; short RGB/slice/scanline glitches at scene transitions, not continuous fake jitter. No compulsory full frame-by-frame animation.
- Default audio: existing English Chatterbox profiles unchanged. Zero paid art or GPU credits.

## Assets and status

All 13 source PNG binaries are committed and verified against
`characters/pixel-default-manifest.json`. Run
`python3 scripts/stage_pixel_default_pack.py --verify-workspace` on the actual
checkout. The default registrations enable approved assets without extra props;
no manual ZIP upload is needed. Historical code-only import notes are superseded
by the installed-pack status below; [import tooling](../assets/import/README.md)
remains available for explicit staging/reproduction.

`PixelProductionProof` provides a model-free visual check of the existing PNGs
and short transition glitches. It is not narration, word alignment or lip-sync.
See [the current policy](PRODUCTION_POLICY.md) for production defaults.

## Production default (active on main)
All 13 original PNGs were installed by [the verified GitHub Actions import workflow](https://github.com/urfavxbf/video-ai-editor/actions/runs/40845188627) and merged to `main` in PR #45. No manual ZIP upload is needed. The production `HeroCharacterStage` and proof `PixelProductionProof` are now registered in `src/Root.tsx` with `assetsReady:true` (and `artApproved:true` for the host stage), so standard renders display the official sprites **without extra props**. The registry's `default_video.default_character_composition` points to `HeroCharacterStage` for future UrFavXBF × PIX episodes. Old experimental compositions are retained for archive/review only; never auto-select legacy character art. This enables character artwork, **not automatic voice synchronization or an entire finished episode**.
