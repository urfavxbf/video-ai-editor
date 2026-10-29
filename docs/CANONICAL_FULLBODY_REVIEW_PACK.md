# Canonical full-body motion review pack (2026-10-29)

The owner-approved three-image reference set remains the **only authoritative
visual direction**. The separately delivered ZIP contains provisional transparent
full-body art and **112 real transform frames**: seven actions × eight poses ×
two characters. These are independently articulated **2.5D geometric keyframes**,
not 112 new hand-drawn animations or completed 3D models.

The new PIX full-body artwork is a derived AI concept (the uploaded official PIX
reference only covers facial expressions). It needs identity and leg/tail QA
before production release. Actual Chatterbox WAVs and timed phoneme cues
are not in this pack, so finished lip sync is not claimed.

## Staging the conversation-delivered ZIP

Place `UrFavXBF_PIX_FullBody_Draft_Animation_Pack.zip` in a local checkout:

```sh
python -m pip install Pillow==11.3.0
python scripts/stage_canonical_fullbody_pack.py --pack UrFavXBF_PIX_FullBody_Draft_Animation_Pack.zip
npm ci
npx remotion still CanonicalFullBodyReviewStage out/draft-fullbody.png --frame=250 \
  --props='{"assetsReady":true,"artApproved":false}'
```

The importer verifies every SHA-256, refuses ZIP path traversal, rejects duplicate
entries and opaque production sprites, and will never overwrite existing staged
assets. A stage status record explicitly says ownerApprovedArt=false.
`assetsReady` is **not** permission to publish: production mode still requires
`artApproved` after a verified human QA pass. The `reviewDraft` switch is
allowed only for preview compositions.

## Rendering system

`src/characters/CanonicalActionSprite.tsx` is a reusable native Remotion player.
Use `CanonicalFullBodyReviewStage` to inspect seven actions; it never substitutes
legacy V2 art. Native character data lives under `characters/canonical/`; old
episodes remain archival. Preserve current approved English Chatterbox voices.

### Unresolved production art

- PIX full-body needs owner identity review against the official face sheet.
- Pivots/seams need closeup review after full motion; sprite source is not multilayer artwork.
- The 2.5D action set provides restrained presentational gestures and simple steps,
  not hand-drawn walk/run/jump cycles with individually painted inbetweens.
- The full face/viseme rig still needs authentic aligned expression layers and
  real timed phoneme cues. RMS amplitude may provide *approximate* mouth openness
  but never counts as accurate lip sync.

Do not claim the video is production-ready based on CI or a resized art canvas.
