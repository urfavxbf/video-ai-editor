# Zero-budget true-frame character sprite production

## Non-negotiable budget contract
**Maximum outside spend: USD $0.** No subscription upgrade, GPU rental, automatic API-key generation, metered model calls, or paid Spritesheets.ai/OpenArt consumption. GitHub Actions are for bounded CPU *validation*, not running generative models. Abort instead of falling back to a billed provider.

## Artwork contract
The new October 29 2026 approved faces/body reference images remain the identity anchors. A true action means independent full-body drawings in different poses (including leg shape/occlusion, hands, proportions and facial expression), NOT layered cuts of a still photo with rotations, translations or mesh warping. Do not claim that a pose collage is a timed motion cycle. The archived 2.5D Remotion character animation remains a **draft review tool only**.

The mandatory frame counts and animation names for **both characters** are in `characters/true-action-contract.json`. PIX uses custom feline/cat paw gestures, not human Mixamo joint positions.

## What existing free tools really provide
- [sprite-gen](https://github.com/aldegad/sprite-gen) (Apache-2.0): local `cutout`, `slice-sheet`, `extract`, atlas and frame hygiene. Its *generation commands require a signed-in Codex/Grok provider or metered API*, so **do not invoke** `gen`, `gen-set`, `video*` on CI. You may use only its offline conversion/post-processing with manually supplied artwork.
- [ComfyUI CharacterPose](https://github.com/Spit8/_ComfyUI_CharacterPose) (MIT): useful for offline human pose guides; its Flux Klein pose transfer **needs GPU/model resources**. Keep optional and disabled for zero-budget CI. Pose guides are not artwork.
- [LibreSprite](https://github.com/LibreSprite/LibreSprite): editor to manually repaint and audit original frames; optional GUI. Respect its GPL license.
- `scripts/import_sprite_animation.py`: existing local GIF/grid extraction helper from the Spritesheets.ai workflow. No generation credits spent.
- `scripts/true_frame_action_pipeline.py`: bundled production-safe validator/stager for fully drawn RGBA frames. It never generates or fabricates action art.

## Input format
```
source-frames/urfavxbf/point_camera/000.png
source-frames/urfavxbf/point_camera/001.png
...
source-frames/pix/walk/000.png
```
Each input must be a **native full-body, aligned, transparent RGBA PNG** with a real independently authored pose. Avoid reference-poster crops, fake padding, low-res upsamples and single-image cutout transforms. Validate a complete action (its expected frame count must match the JSON contract):

```sh
python -m pip install Pillow==11.3.0
python scripts/true_frame_action_pipeline.py --plan
python scripts/true_frame_action_pipeline.py \
  --character urfavxbf --action point_camera \
  --frames-dir source-frames/urfavxbf/point_camera \
  --out-dir public/characters/true-action --fps 12
```

The generated `manifest.json` has SHA-256 digests, aligned canvas and frame order. It is deliberately marked **artApproved=false** and **motionReviewed=false** until the animation is examined as moving footage, including hands, feet, occlusions, drift, and return to first frame. Matching dimensions / unique pixel hashes DO NOT prove the frames were independently drawn. Keep the art unapproved if motion loops jitter or faces mutate.

## Delivery safeguards
- Don't consume Spritesheets.ai (100 available vs 500 for one sheet) or OpenArt (40 available) credits.
- Don't claim frame interpolation or partial body transforms count as authored sprite animation.
- Don't set `assetsReady=true` for an episode without complete, reviewed sprites for that action; use an explicit pending-art message, never legacy fallback.
- Distinct standalone still poses are **reference keyframes**, not a walk cycle, unless ordered and motion-reviewed.
- Future videos default to the new genuine frame-by-frame workflow **only after** completed sprites pass review. English Chatterbox voice direction unchanged.

## Remaining expensive part
Open-source code and CPU tools do not magically supply hundreds of detailed anime frames. We can stage original frames created through included interactive image generation and manual cleanup at no extra external API charge; identity/motion still need visual review. If free generation capacity is exhausted, stop with the accurately reported coverage instead of spending.
