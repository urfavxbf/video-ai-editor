> **Quality correction (29 October 2026):** The first V4 motion frames are ONLY **64×78 actual source pixels**, padded to 128×128 in the normalized QA pack. The local MP4 previews were **1280×720**, not 1920×1080. Nearest-neighbor scaling preserved pixel edges but cannot recreate missing face, mouth, or hair detail. The illustrated poster is also NOT a source for true high-detail full-body frames. Do NOT call the cropped pack “1080p-ready”. `scripts/validate_chibi_v4_production.py` now blocks such false claims: require separately authored original transparent master artwork at >=512×768 per full-body character and >=384×384 per facial/viseme layer, authentic per-file fingerprints, actual 1920×1080 video export, plus owner approval. **No current V4 draft image passes that production-ready gate**. Concept approval is not art-production approval.

# Chibi Pixel Art V4 — dark-green UrFavXBF and PIX

The owner approved the newly illustrated **dark-green chibi pixel-art** aesthetic
in place of the previous black/yellow concept. PIX retains the cyan, purple and
pink cyber-cat colors. The current reference is the independently generated
`new_chibi_concept_v4.png`.

## Current delivery (draft sprite assets)

A **downloadable ZIP** called
`UrFavXBF_PIX_Chibi_V4_Draft_Sprite_Pack.zip` was generated from the new
illustrated concept board. It is a conversation artifact, not checked into the
public GitHub repo. It contains:

| Character | Motion action groups | Extracted motion source frames | Facial references | Mouth references |
|---|---:|---:|---:|---:|
| UrFavXBF | 23 | 85 | 10 | 15 |
| PIX | 24 | 86 | 10 | 15 |
| **Total** | **47** | **171** | **20** | **30** |

The downloadable ZIP additionally includes the concept art, build script,
SHA-256 manifest, README and 17-second H.264/AAC review video with the
existing approved English voice samples.

**Not yet final**: The source sheet is a composite illustration, not a
studio-quality source scene with editable layers. Its drawn movement strips
generally show 3–5 different poses despite saying “8F”; **no missing
in-betweens have been invented**. Motion sprites are native small-format
**64×78 transparent RGBA** and need per-frame cleanup to remove the few
neighbor outlines, inconsistent body proportions and poster artifacts.
Facial refs are 78×83 and mouth tiles are 56×25, not aligned viseme layers.
Hair-follow-through, accurate A/E/I/O/U/M/F lip sync, full turnarounds,
two-character interaction shots and smooth long-form animation remain
dedicated art/QA work.

## How to stage and review

Extract the pack under the repo's local workspace, preserving
`public/characters/animation-v4` paths, then run:

```bash
python scripts/validate_chibi_v4_assets.py \
  --pack /private/UrFavXBF_PIX_Chibi_V4_Draft_Sprite_Pack.zip

npm ci
npm run typecheck

npx remotion still ChibiV4ReviewStage out/chibi-v4-review.png \
  --frame=40 --props='{"assetsReady":true}'
```

The composition is in
`src/characters/ChibiV4ReviewStage.tsx`, using
`src/characters/ChibiV4Sprite.tsx`. It deliberately does not fall back to
legacy V2 artwork for missing V4 images. If the asset pack is not staged,
keep `assetsReady:false` (the stage shows labeled missing-image placeholders).

The code is safe to ship in a draft PR because the source art remains private.
Asset PNGs are not present in the repo; do not claim public GitHub Actions has
rendered them without a staging step.

## Production acceptance checklist

- [x] New dark-green chibi concept artwork and companion's cyan/purple palette.
- [x] Isolated 171 distinct source pose images into individually named RGBA PNG files.
- [x] Isolated 20 facial reference images and 30 mouth-reference tiles.
- [x] SHA-256 manifest, scripted extractor and downloadable ZIP.
- [x] 17-second 30fps H.264/AAC local review with approved original English sample voices.
- [x] New opt-in Remotion review composition, catalog and strict asset-path checks.
- [ ] Redraw/clean frames at consistent native art scale, remove any neighbor
      artifacts and enforce per-action pose consistency.
- [ ] Supply the actual missing inbetweens and loop endpoints for every requested
      full-body movement in the 72-item creative catalog.
- [ ] Create editable standalone hair components and action-specific hair
      overlapping frames, NOT flat cutouts.
- [ ] Make aligned facial expressions and viseme overlays on the same exact
      full-body face drawing; validate against actual spoken phonemes.
- [ ] Stage final pixel-clean images and render an actual Remotion review with
      animations, captions and voice, then obtain owner visual approval.
- [ ] Migrate existing episode away from yellow/black V2 only after this review.

## Integrity rules

`characters/registry.json` records the **new preferred next visual style**
while keeping existing episode artwork pinned until the new sprite pack is
production-approved. Never substitute the old V2 full-body PNGs for missing
green chibi frames. Do not equate posters, per-pose cutouts, timing code,
or static mouth-reference tiles with completed 72-action character animation.
