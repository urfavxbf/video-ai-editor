# Default UrFavXBF × PIX pixel pose art — 2026-10-29

**The user selected the ten new individual high-resolution pixel-art poses** based on the two owner-selected reference sheets. Treat these as the *only* default art for new episodes. Do not use the rejected geometric 3D prototypes or rejected old pose packs. Do not crop sprites from the presentation sheets.

- UrFavXBF: idle, talk, point_camera, point_side, happy.
- PIX: idle, curious, talk, point, happy.
- Original **1254 × 1254 RGBA PNG**, alpha-verified, one independent image per pose. Scaling: CSS `image-rendering: pixelated`, nearest-neighbor for integer enlargements, never bilinear-resample into soft sprites.
- Style: pixel-art chibi UrFavXBF in black/neon-green hoodie/X headphones; PIX is a fluffy cyan/lavender cat with blue/purple eyes, headphone X and luminous collar.
- Direction: cinematic 2.5D stage, pose swaps triggered by active speaker/listener actions; short RGB/slice/scanline glitches at scene transitions, not continuous fake jitter. No compulsory full frame-by-frame animation.
- Default audio: existing English Chatterbox profiles unchanged. Zero paid art or GPU credits.

## Assets and status

`characters/pixel-default-manifest.json` records paths and SHA-256 fingerprints for the ten exact PNGs. They are packaged in the downloadable `UrFavXBF_PIX_Official_10_Poses.zip` attached to the user conversation. **The GitHub connector cannot directly read local binary output paths, so this PR only commits registry/runtime/validator code, not the PNG bytes.** The selected style and path defaults are configured, but production must remain blocked until all ten binaries have been staged and validated in the repository. No silent legacy fallback.

To stage, download the ZIP and run `python scripts/stage_pixel_default_pack.py /path/to/UrFavXBF_PIX_Official_10_Poses.zip`, then commit `public/characters/pixel-default/` on the branch. Only after all SHA checks and an actual rendered smoke test can `assetsReady` / `artApproved` be enabled for 16:9 productions. No publishing automatically.
