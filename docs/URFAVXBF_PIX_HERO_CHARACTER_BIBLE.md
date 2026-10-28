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

**V3.2 — rig-ready, asset-gated:**
`CharacterPuppet` supports separately rotatable shared-canvas transparent
`head`, `body`, `leftArm`, `rightArm`, `leftLeg`, `rightLeg`,
`tail`, and paired closed/open mouth layers. These are NOT present in the
approved pack. The existing eight-frame idle/talk/react sprite loops are
**HEAD ONLY**, unsuitable for whole-body articulation.

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
- [ ] Review actual Remotion render with both sprite binaries staged.
- [ ] Visually confirm **each** reaction, clipping, subtitle safety and camera
      framing for at least one speaking/listening handoff.
- [ ] Obtain clean cut-out **head/arms/legs** layers if separate-joint acting
      is required, then quality-review anatomical pivots and seams.
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
