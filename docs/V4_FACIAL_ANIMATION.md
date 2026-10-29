# Chibi V4 Facial Expressions — UrFavXBF + PIX

**Status: implementation underway; artwork not yet drawn/aligned/approved.**
This is an independent V4 art-production track, not an automatic visual switch
in existing videos. The uploaded old PixelGlitch pack is the reference for
**state names and timing only** — its yellow/black legacy faces and cyan/yellow
legacy cat portraits must NOT be imported as the new characters.

## Work completed

1. Inspected the user's actual `UrFavXBF_PIX_PixelGlitch_Complete_Pack.zip`:
   - UrFavXBF: neutral, talk, excited, thinking, surprised, glitch PNG portraits.
   - PIX: neutral, talk, happy, curious, surprised, glitch PNG portraits.
   - Both: idle/talk/react 8-frame portrait loops at 5/8/8 FPS respectively.
   - NOT separate body movements, independent face rig or phoneme-aligned visemes.
2. `characters/facial-v4-rig.json` defines new chibi palette, layer geometry,
   10 expression states and 7 mouth states for each character.
3. `V4FacialController.ts` maps voice/reaction/manual expression cues to state,
   plus deterministic blink and generic mouth intensity from real RMS only.
4. `V4FacialPortrait.tsx` layers same-canvas V4 RGBA base, expression, mouth.
5. `V4FacialReviewStage.tsx` shows the two characters at 1920x1080/30fps,
   with honest placeholder cards until artwork is staged and owner-approved.
6. `validate_v4_facial_assets.py` blocks missing layers, wrong dimensions,
   opaque/empty PNGs, excessive overlay coverage, duplicate files and
   EXACT SHA copies of the old PixelGlitch model's 14 source portraits.

**Important:** The controller cannot make accurate phoneme lip sync from
audio energy. It can display generic speaking intensity, or consume correctly
timed, explicitly authored `V4MouthCue` mouth positions. No real aligned
new mouth/face art has been supplied as of this update.

## Required actual new artwork

All files for both V4 characters must be **genuine new drawings**, 512×512
RGBA with transparency. Keep exactly the same canvas, view, face anchor,
head dimensions, pixel scale, palette and alignment.

```text
public/characters/facial-v4/
  urfavxbf/
    base.png                     # V4 head/portrait; blank eye+brow+mouth region
    expressions/
      neutral.png happy.png curious.png excited.png surprised.png
      thinking.png focused.png sleepy.png glitch.png blink.png
    mouth/
      rest.png small.png medium.png wide.png round.png closed.png fv.png
  pix/
    base.png                     # matching cyan/purple chibi PIX, blank face region
    expressions/                 # same ten filenames
    mouth/                       # same seven filenames
```

A **blank facial region** on base.png is necessary: if eyes or mouth are
already baked into base, overlays would duplicate eyes or lips. Expression
PNGs draw only eyes and eyebrows; mouth PNGs draw only the mouth. Use the same
512×512 coordinate system across all layers. Eyelid blink is a separate
`expressions/blink.png` design, not a primitive blink effect imposed on
an existing portrait. An image with face expressions baked into whole-head
snapshots does not meet this layer contract.

- UrFavXBF: new **warm medium tan / green hoodie / black-green spiky hair /
  emerald eyes / green X headphones**, friendly not angry.
- PIX: new **cyan/light-blue AI cat, purple/pink cyber accents**, expressive
  ears/eyes/collar; not original yellow/white V2 styling.
- Mouth poses: `rest`, `small`, `medium`, `wide`, `round`, `closed`,
  `fv`. The latter two need actual shape art to work as visemes.
- Merging old expressions onto the new face without artist re-drawing is
  **forbidden**, because the art/pixel scale and anchor are different.

## Quality check / stage in Remotion

Verify metadata contract (no art required):

```bash
python scripts/validate_v4_facial_assets.py
python -m unittest discover -s tests -p 'test_v4_facial_system.py' -v
npm run typecheck
npx remotion still V4FacialReviewStage out/v4-facial-staging.png --frame=120
```

When all 36 genuinely new PNG files are staged:

```bash
python scripts/validate_v4_facial_assets.py \
  --assets public/characters/facial-v4 \
  --output out/v4-facial-art-qa.json
```

If validation passes, manually inspect the face/ear/hair continuity and
actual mouth/eye alignment across every expression. Only after the owner
**explicitly approves** the new drawings should `assetsReady:true` AND
`artApproved:true` be supplied to the Remotion composition. The technical
validator alone cannot assess style likeness or art identity.

## Implementation notes

- Keep original V2 hero episodes pinned to their original V2 visuals.
- For speaking character, only that character's own VoiceEvent may trigger
  a mouth cue; partner mouth remains resting.
- Missing/unknown RMS samples result in resting mouth. The
  `audio-energy-proxy` label is NOT phoneme lip sync.
- An explicitly aligned manual/phoneme cue may use `round`, `closed`, or
  `fv` mouth shapes at exact time points.
- Independent full-body movements will be a separate true V4 sprite/rig job.
- The face layer system uses no paid Spritesheets.ai generation APIs and
  consumes no generation credits.


## Actual art draft V1 produced (29 October 2026)

A new **original vector-authored artwork prototype** has been built: 36 transparent
512x512 RGBA assets (two base portraits, 20 eyes/brows expressions and 14
mouth layers), **not crops** from a concept poster and not V2 art reuse.

- Personal asset Library:
  `/UrFavXBF Video Characters/Chibi Pixel V4/Facial Artwork Draft V1/`
- ZIP: `UrFavXBF_PIX_V4_Actual_Facial_Artwork_Draft.zip`
- Review panel: `V4_Facial_Review_Contact_Sheet.png`
- Video: `V4_Facial_Animation_Draft_1080p.mp4` (silent, 7 seconds, 1920x1080 at 30 fps).
- ZIP includes `build_v4_face_art.py`, the 36 source PNGs and SHA manifest.
- The video demonstrates deterministic **facial state switching**, not
  waveform-triggered speech or phoneme-accurate lip-sync. Previous English
  voice sample bytes were unavailable during drafting, so there is no
  audio-synchronized preview yet.

All 36 new files passed deterministic local canvas/alpha/uniqueness checks
against the contract. **These are visual-review drafts**, not owner-approved
production art. The vector drawing fidelity is simpler than the illustrated
high-detail reference. Do not call the visuals final without owner approval.

The artwork is **not committed to public GitHub**. It must be downloaded
from the personal Library and staged into the repo using:

```bash
python scripts/stage_v4_facial_art.py \
  --pack UrFavXBF_PIX_V4_Actual_Facial_Artwork_Draft.zip
python scripts/validate_v4_facial_assets.py \
  --assets public/characters/facial-v4 \
  --output out/v4-facial-art-qa.json
```

**No auto-approval:** The staging script does not switch production episodes to
V4 and does not set `artApproved:true`. Run with both flags explicitly only
in a private visual review after file QA. Existing episodes remain pinned to
prior art.

