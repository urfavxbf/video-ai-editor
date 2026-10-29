# UrFavXBF × PIX: pixel-art pose system — locked visual direction

**Date:** 2026-10-29  
**User-approved creative direction:** Pose-based expressive pixel-art chibi characters set into cinematic 2.5D/3D scenes, with custom motion graphics, character speaking/reacting cues, and short **glitch effects at every scene transition**. **Full frame-by-frame animation is not required.** No paid APIs, generation credits, or GPU rentals.

**Critical distinction:** "style locked" means the character specifications and production technique are locked. The individual illustrations are **drafts awaiting visual approval**; do not mark them official final artwork without user confirmation.

## Identities

**UrFavXBF:** messy black hair / neon-green streaks, green eyes, X-branded black/green headphones, black/forest-green cyber hoodie, dark pants and trainers; pixelated chibi male host/storyteller.

**PIX:** cute fluffy ice-cyan/white pixel-art **cat**, pink inner ears, blue/purple eyes, cyan/purple headphones, glowing collar, fluffy tail and four paws. *Never substitute a human or a copied reference-video mascot.*

Style sheets are **design references only**, not to be cropped into production sprites. Original individual poses were rendered on their own native pixel grid. Each independent PNG is delivered in the separate attached owner review ZIP. The generated pixel-art linework is a simplified first-pass candidate for review; character identity fidelity must be confirmed visually.

## One file per pose, no cropping or blur

- UrFavXBF: \`idle\`, \`talk\`, \`point_camera\`, \`point_side\`, \`laugh\`.
- PIX: \`idle\`, \`curious\`, \`talk\`, \`paw_point\`, \`happy\`.
- Native 256 × 256 RGBA source and its exact **4× nearest-neighbor** 1024 × 1024 RGBA export supplied for **each of the ten** poses.
- Source: \`UrFavXBF_PIX_Individual_Pixel_Poses_v1.zip\`, generated as standalone pixel illustrations by \`build_pixel_poses.py\`, no cropping from a sheet.
- All ten independent exported PNG file hashes are pinned in \`characters/pixel-pose-style-lock.json\`.
- **Runtime target** after staging: \`public/characters/pixel-poses-v1/{id}/{pose}.png\` and \`{pose}_native_256.png\`.
- For React/Remotion use \`imageRendering:'pixelated'\` or \`imageRendering:'crisp-edges'\`, never filter with blur. Prefer integer scaling of 256 native pixels.
- Keep transitions in Remotion, not baked into sprite texture files: RGB split, pixel slice, scanline break, block reveal. Transitions should be brief and informative, rather than long noisy overlays.

## Import to repository workspace

The image binaries were produced in the connected conversation render workspace, **not yet checked into GitHub by this design commit**. Download the separate ZIP from that conversation and run:

\`\`\`bash
python -m pip install Pillow
python scripts/stage_pixel_pose_pack.py /path/to/UrFavXBF_PIX_Individual_Pixel_Poses_v1.zip
\`\`\`

The staging script verifies the locked SHA-256 for **every independent image**, dimensions, transparent canvas and **exact nearest-neighbor upscale equivalence** before writing usable files under \`public/characters/pixel-poses-v1\`. It rejects missing or duplicate poses and refuses overwrites. After staging, commit binary assets to the working branch; do not merge or use the art in final episodes before the owner has reviewed the images.

## Storyboard & animation usage

Each character uses its own pose state (idle, speaking, explaining, laughing etc.). Brief head/position movement may be applied by Remotion without masquerading as a true multi-frame walk-cycle. Voice-derived speaking/listening cues should select a real pose, while timed kinetic captions interact with on-screen diagrams in a cinematic environment.

- Keep 16:9, 1920 × 1080 and 30fps for long-form.
- Retain existing English Chatterbox voices.
- No unapproved old models, generic primitive-3D faces, or screenshots from the reference video as background assets.
- Owner visual review of both characters and the cinematic sample is required.

**Status:** Direction and 10-pose asset manifest locked; produced PNGs are ready to preview, **NOT approved**, and must be staged using the verified ZIP before Remotion can use them.
