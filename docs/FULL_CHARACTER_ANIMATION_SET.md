# UrFavXBF × PIX — Full Animation Production System (V4)

**Owner brief:** Both characters are the protagonists of every long-form 16:9
YouTube video. This is the authoritative production checklist for all motions,
expressions, hair and mouth shapes. No stock stand-ins, no head-on-body
overlay, and no faux "walk" made by rotating a single cutout.

**Scope:** 72 individually versioned action/expression slots, 36 for UrFavXBF
and 36 for PIX. Machine-readable catalog: `characters/full-animation-set.json`.
Schema/asset gate: `scripts/validate_full_animation_set.py`. Actual preview
composition: `HeroAnimationReviewReel`.

## What the existing official pack ACTUALLY contains

The approved `PixelGlitch_Complete_Pack.zip` already contains:

- **48 true 384×384 head-only frames**: 8 idle, 8 talk, 8 react,
  per character, plus atlases.
- **12 separately drawn 384×384 facial expressions**, 6 for each character.
- Two **560×768 RGBA full-body originals** and separate non-destructive VFX.
- Existing approved English Chatterbox voice samples.

The canonical source PNG SHA-256 hashes remain pinned in the catalog.
Head sprites are excellent for dedicated facial close-up shots, BUT they
have a different composition from the full-body V2 originals. Never paste
the head sprites directly over the full-body PNG: doing so produces two
sets of hair/headphones/ears and broken edges.

The currently available `HeroAnimationPlayer` supports ONLY explicitly
verified source-driven close-ups and simple full-character VFX (e.g.,
glitch, float). Missing poses/visemes explicitly throw an error. It does
**not** claim the full 72 original animations are completed.

## Design and animation contract

Each final frame MUST be explicitly authored or drawn from approved
protagonist artwork. A sequence's pixels cannot merely be rotations,
cuts or scaling of a single neutral PNG.

`characters/full-animation-set.json` specifies ID, category, frame count,
fps, loop policy, status and source type for each slot. Required production
assets should use this structure:

```text
public/characters/animation-v4/urfavxbf/<action-id>/00.png
public/characters/animation-v4/urfavxbf/<action-id>/01.png
...
public/characters/animation-v4/pix/<action-id>/00.png
...
```

All final frames: native **560×768 RGBA**, transparent background,
pixel-art aligned to a common character origin/ground baseline. Rendering
output: **1920×1080 at 30fps**. Each artwork cycle has carefully reviewed
anticipation, action, settle/recovery and identical start/end silhouette
where looped. Transitions must keep poses consistent and maintain clear
silhouette readability in a small YouTube frame.

### Priority A — Facial identity, speech and hair

UrFavXBF: neutral/rest, A, E, I, O, U, M/B/P closed, F/V,
blink, eyebrow raise/furrow, speaking smiles and natural listening
expressions. The distinctive tousled black hair and gold-edged strands
require **new overlapping source drawings** for idle, running, jumping
and impact; maintain the signature hairstyle silhouette in every keyframe.

PIX: same seven phoneme-mouth families plus rest, clean eye blinks,
ear twitches, expressive brows and whisker follow-through. The
headphone/ears must be coherent frame-to-frame. Make PIX's mouth
cute/expressive without changing her face identity.

**Timing:** audio RMS is useful only as an overall speech-activity/energy
signal. It is NOT enough to know the vowel or consonant; real A/E/I/O/U/M/F
lip-sync needs actual phoneme/viseme timestamps from text+speech alignment
or carefully authored cue sheets. Without that, retain the existing
head-talk loop, accurately labeled approximate mouth animation.

**Hair:** shape-honoring original animation drawings, not a chopped-off
hair layer simply rotated at an arbitrary pivot. A hair loop must
preserve original head silhouette where the head is still.

### Priority B — UrFavXBF full-body action

Idle, talk, walk, run, jump start-air-land, fall/landing, crouch/sit,
turn left/right, forward/side pointing, wave, arms crossed, hand on hip,
hand on chin, talk gestures, idle glitch, surprise, laugh, focused,
alert and glitch reaction. Build body motion around distinct
action poses and clean shoulder, neck, elbow, hip and knee construction.
No visible cut-matte halo, missing torso or joint holes.

### Priority C — PIX full-body action

Sitting idle, standing idle, walk, trot, pounce, sit-stand transitions,
curious head tilt, paw raise/point, wag/fluff tail, lick paw, stretch,
meow/talk, glitch idle, happy, curious, annoyed, surprised, sleepy,
glitch reaction, float and appear/disappear. Her legs and front paws
need deliberately drawn new side/front views when she walks/runs;
the default seated 2D artwork does not contain real hidden limb geometry.

### Priority D — Paired animation

PIX on UrFavXBF's shoulder: draw purpose-built matching interaction poses
at a shared origin; maintain real occlusion, shoulder contact, believable
weight and both characters' consistent proportions. This cannot be
achieved professionally by shrinking the sitting-cat PNG and sticking it
onto a human shoulder.

## Current playability vs new art

**Approved ready for close-up use:** source 8-frame idle/talk/react loops,
specific expression portraits, and simple glitch/float compositing.
The 72-slot catalog explicitly marks these as `available-closeup` or
`available-composite`.

**Not yet drawn:** genuine new locomotion frames, full-body gesture cycles,
hair follow-through, blink/brow sequences, seven independent mouth
shapes plus rest, all PIX paired/pose transitions and true phoneme sync.
These are marked `needs-new-animation-art` and MUST remain gated.

## Regression and staging

```bash
python scripts/validate_full_animation_set.py

# Optional verify original binary pack including exactly 48 loop PNGs:
python scripts/validate_full_animation_set.py \
    --sprite-pack /private/PixelGlitch_Complete_Pack.zip

python -m unittest discover -s tests -p 'test_full_animation_catalog.py' -v

npm ci
npm run typecheck
npx remotion still HeroAnimationReviewReel out/available-facial-sprites.png \
    --frame=190 --scale=0.5

# For an ACTUAL image review, stage genuine source frames from the owner
# ZIP under public/characters/pixel-glitch and use assetsReady=true.
```

The composition never substitutes a flat full-body PNG for an unfinished
animation. It is a review board for authentic already-created sprites.

## Quality release gates

1. Source identities and color palette match official originals.
2. All 72 catalog statuses reflect real approved drawings, not just code paths.
3. Neutral source, facial hair/ears, eyebrows and expression variations are
   coherent shot-to-shot; no face swapping or misalignment.
4. Mouth visemes are aligned, timestamped and reviewed against actual English
   or Tagalog voice recordings before claiming lip-sync.
5. 2D loops do not pop at seam, feet do not slide, shoulder joints and
   hair do not clip.
6. Every scene is audited in 16:9 alongside subtitles and infographic
   blocking; speaker and listener do not share the same talking animation.
7. Render actual Remotion MP4, inspect playback, and request owner approval
   before setting an action's status to `production-approved`.

**Bottom line:** The catalog and playback/validation infrastructure are
implemented, while the absent original frame art is explicitly scoped.
A polished complete animation set is an artwork task, not a claim we can
make by adding TypeScript action names.
