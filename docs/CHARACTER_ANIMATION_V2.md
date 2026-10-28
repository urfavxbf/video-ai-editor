# Animation v2 — UrFavXBF + PIX (owner feedback, 28 October 2026)

## Priorities (in this order)

1. **Character animation first.** The first finished 16:9 Ghost Town pilot looked good but UrFavXBF and PIX were too static. Animate speaking turns, idles, facial expressions, independent head/arms/tail/ears when layered sprites or rigs exist, eye movements, blinks, gestures, and reactions with coherent frame-to-frame continuity. Never swap the approved character design or Chatterbox speaker identity.
2. **Data + caption fusion.** Rather than separate subtitle cards floating below infographics, integrate *verified numerical claims* directly into animated speaker captions and contextual graphs. For example, while the speaker says "fifty-three percent," the emphasized token should connect to an animated 53% traffic bar/card, then restore normal captions. All facts must be verified and captions must come from actual speech timings.
3. **True 3D workflow**, after authoring approved 3D meshes and expressive rigs. The existing repository is **Remotion 4.0.522 with 21 FX**, but **does not currently install `@remotion/three`, `three`, `@react-three/fiber`, Blender, or any rigged 3D model**. The official avatars are transparent RGBA 2D images. Applying CSS perspective to PNGs is **2.5D**, not a genuine 3D character render.

## First implemented milestone: speaker-aware 2.5D puppetry

`src/characters/CharacterPuppet.tsx` introduces a frame-deterministic, reusable Remotion character animator:
- Approved character identity mapped to existing assets in `public/characters/` (copied from owner Library before rendering).
- Speaker-aware timing based on actual Chatterbox utterance frames; audio RMS envelope can drive breath/lean emphasis, and listening reactions are distinct from active speech.
- Whole-cutout fallback with subtle depth/perspective when no rig layers exist. This is a temporary improvement, **not** proper face animation.
- Optional, full-canvas transparent **layered puppet textures** `body`, `head`, `tail`, `mouthOpen` / `mouthClosed` with pivot points. Head/tail can animate independently; mouth state is a rough audio-energy open/close only, **not phoneme-accurate lip-sync**.
- Frame-pure motion functions; no unstable browser timers, useFrame hooks, random transforms, or engine-specific interpolation drift.

### Pipeline contract

```tsx
<CharacterPuppet
  id="pix"
  assetPath="characters/PIX_Transparent.png"
  voiceEvents={[{ speaker: "pix", startFrame: 360, endFrame: 500, rms: [0.1, 0.6, 0.9, 0.4], samplesPerSecond: 10 }]}
  left={1300}
  bottom={50}
  width={460}
  height={520}
/>
```

`rms` should be measured from the *final rendered WAV*, normalized to 0–1 and sampled at the declared rate; never invent it from transcript words. The code supports a fallback 0.55 activity level only for positioning/proxy movement, not "accurate lip sync". If the array is omitted, **no mouth asset should be switched open**.

`layeredRig` paths are optional and can be added only after actual transparent layers have been authored/checked for accurate overlap. The old single-PNG avatars do not contain independently animatable eyes/arms/tail.

## Next: real 3D rigs

For **real 3D characters** in this repo:
- Prepare an **approved 3D representation of both characters**, preferably Blender source plus rigged `.glb` / `.gltf` / `.fbx` exports with a consistent pixel/voxel shader matching the approved UrFavXBF art and the robotic cat PIX.
- Build a face/viseme rig or suitable mouth blend shapes, eyelid rig, body skeleton, and named animation clips (`idle`, `listen`, `talk`, `question`, `surprised`, `explain`). Keep true mouth-to-phoneme alignment as a separate tested feature.
- Install matching versions of `@remotion/three`, `three`, `@react-three/fiber` and types, then add a **separate** 16:9 3D composition; preserve the old 2D compositions for compatibility. On Remotion 4, render WebGL with `--gl=angle` on suitable GPU systems or `--gl=swangle` on CPU-only runners. Verify actual ThreeCanvas renders, do not assume guidance files equal installed engine.
- Frame-drive all animation from Remotion's `useCurrentFrame()`; no wall-clock or real-time animation loops. Test face tracking/visemes and character identity at multiple camera angles before replacing the canonical 2D overlays.
- Store model authorship/licensing, mesh scale, bone names and asset hashes in `characters/registry.json` only once files exist.

References: https://www.remotion.dev/docs/three-canvas and https://www.remotion.dev/docs/webgl

## Combined data + animated subtitles (after characters)

Specify `TimedWord = {text, startFrame, endFrame}` from audited final WAV alignment. The infographic and text should share the **same timeline and semantic fact ID**, avoiding unrelated motion. The active word animates (scale/underline/highlight), and a corresponding bar, counter, marker, or source line moves into focus. Distinguish web-request percentages from people/accounts; no fabricated timestamps. Keep captions clear on 16:9 screens and label sources. Draw graphics behind the caption layer and ensure text has contrast.

## Quality gates

- Do **not** call the existing PNG cutouts 3D, a skeletal animation, or fully lip-synced characters.
- Character voice IDs remain `natural-storyteller-v1` (UrFavXBF) and `pix-cute-female-emily-v1` (PIX).
- Keep **16:9 / 1920 × 1080 / 30fps**, English-only, full-length narrative default.
- Use the **21 existing FX** selectively. Do not claim they all appear in one scene.
- Verify character consistency, voice attribution, active/listening poses, visible motion, accurate captions, final render dimensions and actual MP4 output.
- Never upload to YouTube without user authorization.
