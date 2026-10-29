# Global canonical character development

**Effective:** 2026-10-29 · **Scope:** all new UrFavXBF × PIX videos.

The three owner-uploaded character images are the authoritative source of visual identity, pinned by SHA-256 in `characters/canonical-references.json`. Source boards are RGB references, **not transparent production sprites**. UrFavXBF is a dark-green chibi host with black/green hair and green X headphones. PIX is a cyan/purple/pink AI cat. Preserve English Chatterbox voice profiles. Default video: 1920 × 1080 landscape, 30fps.

## Reusable runtime
- `CanonicalCharacterAssets.ts` defines new approved-image target paths and a gated asset contract.
- `CharacterPuppet.tsx` supports full-body 2.5D puppetry: separately verified limbs/head/tail, voice-driven movements and whole-sprite motion when no rig exists.
- `HeroPerformance.ts` manages speaker and listener actions with real WAV envelope data.
- `HeroCharacterStage.tsx` stages the canonical two-character hero composition.
- `V4FacialController.ts` manages ten expressions and seven mouth states. RMS amplitude is **not** phoneme alignment; timed cues must be supplied for phonemes.
- `ChibiV4Sprite.tsx` supports review of draft motion frames, which are low-res and not final character art.
- `scripts/import_sprite_animation.py` is the already-existing helper for importing GIFs/PNG sheets/frames inspired by the MIT spritesheets-companion. No paid credits or automatic source image generation.

## Required production asset delivery
- `public/characters/canonical/urfavxbf/full-body.png`
- `public/characters/canonical/pix/full-body.png`
- Separate matching transparent `LayeredPuppetRig` pieces for any real arm/leg/head articulation.
- Verified layered facial expressions and mouth drawings under `public/characters/facial-v4/{character}/`.

**Pending:** PIX has only an official facial reference, not an official full-body model. A genuine matching full-body drawing must be authored and reviewed. UrFavXBF's official full-body image is an opaque reference with white background, not a renderable RGBA layer.

Never mark `assetsReady` or `artApproved` as true merely because a reference exists. Workbenches show a pending-art state; they never quietly fall back to old V2 art. Historical videos and legacy compositions are archival only.

## Validation commands
```bash
npm ci && npm run typecheck
python -m pip install Pillow==11.3.0
python -m unittest discover -s tests -p 'test_import_sprite_animation.py' -v
python -m unittest discover -s tests -p 'test_v4_facial_system.py' -v
npx remotion still HeroCharacterStage out/canonical-review.png --frame=80
```
