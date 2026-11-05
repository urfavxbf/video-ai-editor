---
name: animation-import
description: Use when importing authorized After Effects Bodymovin Lottie vector animation or baked Duik Angela character motion into the existing Remotion editor with validated local JSON and render proofs.
---

# Animation Import — Bodymovin, Lottie and Duik

**Scope:** opt-in animation interoperability, not Adobe After Effects or Duik
execution in the render environment. Read `AGENTS.md`,
`docs/PRODUCTION_POLICY.md`, `docs/AFTER_EFFECTS_LOTTIE.md`,
and `docs/DUIK_ANGELA_IMPORT.md`. For Remotion composition code also
load `remotion-markup` or `remotion-render`.

## Identify the actual source

- **Bodymovin / Lottie:** compatible local JSON from licensed/original
  After Effects vector animation. `@remotion/lottie` renders supported
  animation data; it does not support arbitrary AE expressions, plugins,
  native AE projects or all 3D effects.
- **Duik Ángela:** authoring happens on a properly licensed After Effects
  workstation. This repo does not install or redistribute Duik or execute
  its IK rig. Only compatible **baked, 2D vector** Bodymovin exports are
  accepted by the local import bridge.
- The committed `src/after-effects/duik-imported.json` is a **hand-authored
  demonstration fixture**, not proof of a real Duik-produced export.

## Import workflow

1. Confirm the user's license/permissions and verify the actual local JSON
   and source frame rate. Reject untrusted URLs, unexpected assets, unbaked
   expressions, unsupported raster/3D/effects and unsafe file paths.
2. For an eligible baked-vector Duik export, use the existing secure
   validator first:
   ```bash
   python3 scripts/import_duik_baked_lottie.py /path/to/approved-animation.json --check
   ```
3. After verification and authorization to replace the destination:
   ```bash
   python3 scripts/import_duik_baked_lottie.py /path/to/approved-animation.json \
     --output src/after-effects/duik-imported.json
   ```
   Never silently overwrite approved character art, registry files or a
   different user's previous export.
4. For general Bodymovin exports, follow `docs/AFTER_EFFECTS_LOTTIE.md`:
   place reviewed, compatible JSON under `src/after-effects/`, import with
   `@remotion/lottie`, and register the appropriate composition only after
   checking multiple representative frames.
5. Run the existing model-free and rendering checks:
   ```bash
   python3 -m unittest discover -s tests -p 'test_duik_baked_lottie.py' -v
   node --test tests/after-effects-lottie.test.cjs
   npm run typecheck
   ```
   Render actual stills/MP4 via the relevant Remotion proof composition and
   validate real frame count, duration, visual motion, format and decoding.

## Boundaries

The demo `DuikBakedCharacterProof` is a fixed 150-frame test composition;
real imports may need a differently timed composition. A successful Lottie
proof does **not** prove native AE compatibility or real Duik export fidelity.
Keep the project's approved UrFavXBF/PIX identities and English production
defaults unless explicitly authorized to replace them. If the source needs
unsupported AE features, request an authorized, licensed transparent image
sequence/video render rather than pretending the JSON bridge can play it.
