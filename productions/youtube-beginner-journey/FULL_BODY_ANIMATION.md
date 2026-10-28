# Full-body character motion — UrFavXBF × PIX

This episode has changed from portrait-only staging to **approved full-body 2.5D
performance**. The original 1920×1080 graphics stay centered, with the host
and PIX visible to either side and the captions in a protected footer.

## Two supported types of character animation

**A. One original transparent full-body PNG per character:** use the existing
full-body sprites at these exact paths:

```text
public/characters/pixel-glitch/urfavxbf/base.png
public/characters/pixel-glitch/pix/base.png
```

The character can breathe, bob, lean, sway, take small stylized steps,
celebrate, react and change its posture/position based on who is speaking.
This moves the whole complete character; it does **not** independently
articulate arms, legs or mouth. This remains a frame-deterministic,
CPU-renderable 2.5D motion treatment, not a 3D mesh.

**B. Official transparent cutout rig:** for actual independent moving head,
left/right arms, and left/right legs, supply a shared-canvas sprite layer for
each moving part. The torso file must **not** already contain the separated
limbs, or motion will double up the artwork. All six PNGs must be the same
canvas dimensions (transparent padding included), have correct alignment in
their neutral resting pose, and have sensible pivot percentages. Optional
tail and paired mouth layers can be added. The rig must retain each character's
approved appearance.

Example `out/youtube-journey-fullbody-assets.json`:

```json
{
  "urfavxbf": {
    "assetPath": "characters/pixel-glitch/urfavxbf/base.png",
    "layeredRig": {
      "body": "characters/rigs/urfavxbf/body.png",
      "head": "characters/rigs/urfavxbf/head.png",
      "leftArm": "characters/rigs/urfavxbf/left-arm.png",
      "rightArm": "characters/rigs/urfavxbf/right-arm.png",
      "leftLeg": "characters/rigs/urfavxbf/left-leg.png",
      "rightLeg": "characters/rigs/urfavxbf/right-leg.png",
      "leftArmPivotPercent": [33, 38],
      "rightArmPivotPercent": [68, 38],
      "leftLegPivotPercent": [43, 69],
      "rightLegPivotPercent": [57, 69],
      "headPivotPercent": [51, 22]
    }
  },
  "pix": {
    "assetPath": "characters/pixel-glitch/pix/base.png",
    "layeredRig": {
      "body": "characters/rigs/pix/body.png",
      "head": "characters/rigs/pix/head.png",
      "leftArm": "characters/rigs/pix/left-arm.png",
      "rightArm": "characters/rigs/pix/right-arm.png",
      "leftLeg": "characters/rigs/pix/left-leg.png",
      "rightLeg": "characters/rigs/pix/right-leg.png",
      "tail": "characters/rigs/pix/tail.png",
      "headPivotPercent": [51, 48],
      "tailPivotPercent": [39, 77]
    }
  }
}
```

The percentages shown are **illustrative pivot defaults**. Adjust after
viewing the source cutouts; they are not claims about the user's original
art's exact joint coordinates. For **flat sprite** motion, omit both
`layeredRig` objects entirely.

## Performance by chapter

- Opening: PIX gets an anticipatory celebratory movement when narrating the
  first upload, then reacts to zero income. The host explains with measured,
  restrained hand/body emphasis.
- Audience and discovery: PIX gets short steps when talking about exploring
  topics; both point toward the organizer and three discovery contexts.
- Packaging: the active speaker points to the changed title and graphic.
- Eligibility and RPM: deliberate explaining/pointing gestures, with PIX
  reacting to the calculations. Neither person dances while numeric data is
  onscreen.
- Revenue branches: explanatory gestures.
- Originality and action plan: clear pointing and restrained celebration at
  PIX's next original video.

RMS from the real English WAVs drives speaking energy and some gestures.
The listening character reacts but does not copy the other speaker's motion.
These are gestures and energy-linked open/closed mouth flaps **only if actual
mouth layers exist**—not phoneme-accurate lip-sync or a 3D skeleton.

## Validation / authorized rendering

Both original Super Pixel V2 full-body PNGs were located in ChatGPT Library and their SHA-256 digests matched `characters/registry.json` exactly. The pack's separate 8-frame idle/talk/react loops are cropped HEAD animations, not independent whole-body motions.

The approved images are currently **not stored in this GitHub branch**.
Do not claim they were staged; the GitHub `public/` directory contains no
`characters/` directory. Once official PNGs are provided:

```bash
# Download the completed CPU voice artifact into the workspace. It contains:
# out/youtube-journey-full.props.json and the 68 WAVs under public/voiceovers/.
# Place both full-body transparent PNGs at the paths above.
python scripts/validate_youtube_journey_fullbody.py \
  --props out/youtube-journey-full.props.json \
  --out out/youtube-journey-full-ready.props.json

# To enable articulated limbs, append:
# --assets-json out/youtube-journey-fullbody-assets.json

npm ci
npm run typecheck
npx remotion render YouTubeJourneyFullEpisode out/youtube-journey-full.mp4 \
  --props=out/youtube-journey-full-ready.props.json \
  --codec=h264 --crf=18 --pixel-format=yuv420p --audio-codec=aac
```

The validator checks SHA-256 fingerprints for the two official V2 base sprites, that both expected RGBA PNG sprites exist, all rigged
limbs are present and aligned to the same canvas dimensions, and no path
escapes `characters/`. It changes `assetsReady` only in a separate local
**review** props file; it never sets `readyForPublishing`.

To render the existing 47.9-second preview, validate its downloaded
`out/youtube-journey-preview.props.json` the same way and render
`YouTubeJourneyPreview` using the resulting ready props.

The unchanged 68-turn script is **8:05.867** based on measured Chatterbox V3
WAVs; the storyboard's 11:30 remains an editorial target only. The user has
not approved final playback. Captions are still editorially estimated and
must be aligned and audited before a final publishable MP4. No GPU needed;
no automatic YouTube upload.
