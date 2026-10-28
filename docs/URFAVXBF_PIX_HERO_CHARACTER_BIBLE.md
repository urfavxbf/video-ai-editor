> **Articulated V3.2 implementation (29 October 2026):** The first original-art 2.5D cutout rig has now been authored and CPU-validated. UrFavXBF has independent head, two arms and two legs; seated PIX has independent head, two visible forelegs and tail. Both have separate torso and hidden joint underlay. The source-preserving extractor is `scripts/rig_official_v2_characters.py`, the default runtime manifest is `src/characters/OfficialV2Rig.ts`, and the output neutral pose is **pixel-identical to the approved source art**. Joint angles are deliberately constrained to reduce seams. This is NOT a full 3D skeletal rig, articulated hind legs for PIX, or phoneme-correct facial lip sync. Review the rendered preview and owner's acceptance before labeling it production locked.

# THE OFFICIAL HERO CHARACTER BIBLE — URFAVXBF × PIX

**Status:** Character performance system V3 in development, artwork identity approved;
character-driven motion preview available for aesthetic review. This is the
default reference for **all future episodes**, not merely the YouTube Beginner
Journey episode. Previous portrait-only composition remains archived for old
videos. Do not change source character identity without owner approval.

## Non-negotiable continuity

| | UrFavXBF | PIX |
|---|---|---|
| Story job | Main host; translates complexity into clear explanations | Curious AI companion; asks the viewer's natural follow-up questions |
| Core style | Black and luminous yellow Super Pixel art; black hair; yellow headset/hoodie | Pale lavender/white cyber cat; cyan ears, tail and headphones |
| Speaker | Existing approved **English** Chatterbox Natural Storyteller | Existing approved **English** Chatterbox Emily-based profile |
| Character rhythm | Deliberate, calm and precise; expressive without frantic fidgeting | Bouncy and quick; reactive but not continuously dancing |
| Screen accent | #ffda00 | #27e8fd |
| Canonical file | `public/characters/pixel-glitch/urfavxbf/base.png` | `public/characters/pixel-glitch/pix/base.png` |

Original 560×768 RGBA source art remains untouched; SHA-256 pinning is the
identity gate. Do not upscale with blurry interpolation or change faces,
colors, wardrobes, silhouettes, voices, proportions or character names.
Pixel-native styling is deliberate, **not** a request for fake 3D.

## Acting principles

1. The **speaker** leads: limited squash/stretch, calm torso lean, controlled
   placement changes and small accent glitch at the start of a new speech
   turn. RMS is measured from real WAV audio, interpolated, and used only
   as *performance energy* (not fake viseme lip sync).
2. The **listener** never mouths the speaker's voice. Use a restrained brief
   agree/curious/surprised reaction at the start of partner's turn; then
   settle into an idle pose so the focus stays on the speaking character.
3. UrFavXBF's explanation cues are measured and sparse. A brief point toward
   a data panel should fade into a normal posture, not remain locked for a
   two-minute explanation.
4. PIX gets faster reaction timing and slightly stronger but short bounces;
   excitement belongs at meaningful moments, not constantly.
5. **Scene choreography has intentional starts/ends.** Fade, ease and damp
   directional changes; avoid abrupt frame-to-frame teleportation.
6. Glitch is an occasional two-frame handoff accent, not a perpetual flashing
   overlay. Respect sensitive viewers.

## Motion modes and current fidelity

**V3.1 — implemented / whole-body 2.5D:**
Both original characters move as complete full-body sprites with distinct
idle sway, voice-linked y movement, posture, micro-squash, stepping,
momentary chromatic glitch and expression *through movement*, not fake mouth
art. This is GPU-free and deterministic at 30 fps.

**V3.2 — implemented original cutout layers, asset-gated:**
`rig_official_v2_characters.py` hand-traces the official 560×768 RGBA art into
aligned transparent `head`, `body`, `leftArm`, `rightArm`, host `leftLeg`
and `rightLeg`, PIX `tail` and hidden `underlay` files. The original source
is copied **byte for byte**. At zero joint rotation, compositing the cutouts
reproduces the original source image exactly. The neutral reference PNG and a
SHA-pinned manifest are output for inspection.

The Remotion `CharacterPuppet` reads `OfficialV2Rig.ts` by default on the
character stage and YouTube episode. Separate head/arms/leg pivots are
calibrated to the actual canvas and rotation is constrained: head ±3°,
UrFavXBF arms ±6°, legs ±3°, PIX forelegs ±3.5°, tail ±8°.

**Not implemented:** independently visible PIX hind legs, open/closed mouth
viseme art, true 3D skeleton, inverse kinematics, or original facial emotion
sheet matching the exact full-body face. Head-only expression sprite loops
cannot be pasted onto bodies without duplicate outlines.

Do **not** auto-create arbitrary rig layers and claim true arm/leg movement.
Creating clean segmentation, missing torso fill, joint pivots, expression
variants and occlusion corrections from approved source artwork is a separate
artist-approved rigging step. Likewise, audio energy is NOT phoneme alignment.
Any lip-sync claim requires real aligned viseme assets and real alignment.

## Composition and camera rules

- Landscape: 1920×1080 at 30 fps; safe captions remain below characters and
  central charts. Never cover percentages, units, subtitles or threshold data.
- Character-led interlude: `HeroCharacterStage` (standalone Remotion
  composition) gives them the whole scene, with gold/cyan brand identity,
  visible speaking state and voice-responsive waveform.
- Explainer: `YouTubeJourneyFullBodyCharacters` uses the same global
  `HeroPerformance` direction and leaves the central 890px infographic field
  available. Subsequent episodes should reuse these primitives with a
  scene-specific cue timeline, never copy/paste new puppetry engines.
- Keep stage lighting dark navy; crisp high-contrast character silhouettes;
  no unapproved style conversion or random generated substitutes.
- No full-body art or model weights committed to public GitHub: load from
  the private render workspace and verify checksum first.

## Approved language policy

The **current repository/episode** defaults to English Chatterbox V3:
UrFavXBF `natural-storyteller-v1`, PIX `pix-cute-female-emily-v1`.
The repository retains the separately designed Tagalog VoxCPM2 voice path
as an explicit option; this is not a claim that live Tagalog voice samples
have been audited or that a GPU service is available.

## QA before character direction is locked

- [x] Verify canonical full-body PNGs against recorded SHA-256.
- [x] Preserve identities, pixel aesthetic, English voice profiles.
- [x] Shared, reusable voice-informed motion profiles and episode integration.
- [x] Character-only workbench and 15-second local audio-visual motion test.
- [ ] Review actual Remotion render with both rigged sprite binaries staged
      (the standalone local cutout rig demo is not the Remotion CI render).
- [ ] Visually confirm **each** reaction, clipping, subtitle safety and camera
      framing for at least one speaking/listening handoff.
- [x] Generate original-art cut-out **head/arms/legs/tail** layers and exact
      neutral composite; bounded pivots and hidden joint patches in runtime.
- [ ] Complete final aesthetic review of **moving** arm/neck/foreleg seams,
      and commission artist correction if any seam is distracting.
- [ ] Confirm any new expressions/mouth assets are original and aligned,
      with explicit approval of facial continuity.
- [ ] Final owner approval of character aesthetic and acting style.

## Asset staging and local review

Source: ChatGPT Library, `/UrFavXBF Video Characters/Pixel Glitch V2/`.
Put these approved PNGs in private `public/characters/pixel-glitch/`
subfolders as `urfavxbf/base.png` and `pix/base.png`.

```bash
python scripts/prepare_hero_stage.py \
  --host-png /your/private/path/UrFavXBF_SuperPixel_Transparent.png \
  --pix-png /your/private/path/PIX_SuperPixel_Transparent.png \
  --host-wav /your/private/path/UrFavXBF_Chatterbox_Natural_Storyteller_Sample.wav \
  --pix-wav /your/private/path/PIX_Chatterbox_V3_Emily_Sample.wav \
  --out out/hero-stage.props.json

npm ci
npm run typecheck
npx remotion render HeroCharacterStage out/hero-character-review.mp4 \
  --props=out/hero-stage.props.json --codec=h264 --crf=18 \
  --pixel-format=yuv420p --audio-codec=aac
```

The props come from real WAV sample counts. Replacing audio requires
regenerating the envelope; merely extending durations in JSON is invalid.

**Media policy:** no commercial music, model-based copies or third-party
character replacement. The official V2 art may be composited in a private
review video but not silently published to YouTube.

## Generate the layered production rig

Install CPU image requirements and stage the two approved full-body PNGs (the
source files live in ChatGPT Library and are not checked into GitHub):

```bash
python -m pip install -r requirements-character-rig.txt
python scripts/rig_official_v2_characters.py \
  --urfavxbf /private/UrFavXBF_SuperPixel_Transparent.png \
  --pix /private/PIX_SuperPixel_Transparent.png \
  --out public/characters/pixel-glitch

# The output contains:
#   urfavxbf/base.png, rig/{underlay,body,head,leftArm,rightArm,leftLeg,rightLeg}.png
#   pix/base.png, rig/{underlay,body,head,leftArm,rightArm,tail}.png
#   rig-assets.json, rig-provenance.json
python scripts/prepare_hero_stage.py \
  --host-png /private/UrFavXBF_SuperPixel_Transparent.png \
  --pix-png /private/PIX_SuperPixel_Transparent.png \
  --host-wav /private/UrFavXBF_Chatterbox_Natural_Storyteller_Sample.wav \
  --pix-wav /private/PIX_Chatterbox_V3_Emily_Sample.wav
npx remotion render HeroCharacterStage out/heroes-rigged.mp4 \
  --props=out/hero-stage.props.json --codec=h264 --crf=18
```

`prepare_hero_stage.py` now **refuses** to create an authorized voiced
review unless the layered rigs exist, except when an explicit `--flat-review`
flag is used. The episode validator also requires the rig by default. This
guarantees new production work cannot accidentally claim a flat PNG has
independently moving arms and legs.
