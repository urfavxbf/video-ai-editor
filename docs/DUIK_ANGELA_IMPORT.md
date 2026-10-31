# Duik Ángela → Remotion: baked character animation bridge

## What is integrated

**Duik Ángela** is a free, GPLv3 After Effects character-rigging/animation **script**, not a Node.js or Remotion plugin. It requires **Adobe After Effects on Windows or macOS for authoring**. The runtime in this repo does not install Duik or distribute its GPL code. <https://duik.org/guide/Angela/>

This integration makes **exports produced by compatible Duik/After Effects workflows** usable in the existing Remotion video editor with the already merged `@remotion/lottie` bridge. It does not recreate Duik IK solvers inside Remotion.

Included:
- `scripts/import_duik_baked_lottie.py`: validates and atomically imports local, 2D **vector-only** Bodymovin JSON. Rejects unbaked expressions, unsupported 3D, raster/image assets, URLs, text layers, masks, effects, excessive files, malformed media, and unexpected FPS.
- `src/after-effects/duik-imported.json`: **original hand-authored, Duik-style vector puppet** showing articulated poses with baked keyframes. **Not** a Duik-generated file; serves as an offline demo and regression fixture.
- `DuikBakedCharacterProof`: actual 1920×1080, 30fps Remotion composition playing the local animated vectors.
- Python security/contract tests, GitHub Actions headless still/MP4 render proof, and integration with the existing PR safety gate.

## How to use real Duik animations

1. On a properly licensed **After Effects** workstation, install **Duik Ángela** from the [official RxLaboratory site](https://rxlaboratorio.org/rx-tool/duik/) and **Bodymovin** from the [official Remotion guide](https://www.remotion.dev/docs/after-effects). Do not copy Duik source code or bundled third-party art into this repo.
2. Rig a licensed/original **2D vector character** using Duik's bones, IK and controllers.
3. Animate, then **bake all evaluated animation expressions and relevant parent-controlled transforms to ordinary keyframes**, including dependencies of visible layers. Remove helper/controller layers that retain unsupported expressions. Duik provides layer baking utilities: <https://duik.org/api/Angela/DuAELayer.html>.
4. Prepare an AE composition for export: 30fps, vector shape layers, no raster image assets, no 3D, no expressions, no effects or track mattes. Review actual final frames in AE.
5. Export Bodymovin/Lottie `.json` from After Effects.
6. In this repo run:

```bash
python3 scripts/import_duik_baked_lottie.py /path/to/approved-animation.json --check
python3 scripts/import_duik_baked_lottie.py /path/to/approved-animation.json --output src/after-effects/duik-imported.json
npm ci
npm run typecheck
npx remotion still DuikBakedCharacterProof out/duik-frame.png --frame=45
npx remotion render DuikBakedCharacterProof out/duik-video.mp4 --codec=h264 --pixel-format=yuv420p
```

7. Verify real source dimensions and timing: `DuikBakedCharacterProof` is a **fixed 150-frame landscape test composition**. For a real export with a different frame count, retime or create a separately registered composition to match the exported duration, rather than silently truncating. Review multiple render frames and audio sync.
8. If your Duik character is raster-based or uses nonportable AE features, render a **licensed, transparent RGBA image sequence** or an approved video+alpha asset in After Effects and use the project's existing asset-based animation/import path. This vector-only bridge intentionally rejects those features instead of producing a broken render.

## Why no GPL dependency in the render runtime?

Duik is licensed GPLv3 and contains copyrighted art/brand elements. We **do not redistribute or bundle Duik**, or use it as a server-side Node dependency. The original export assets' rights remain subject to their authors' permission; do not claim a Duik-produced animation merely because an output has rig-style keyframes.

## Production constraints

- No new paid API, ads or remote services.
- Keeps existing **English UrFavXBF Natural Storyteller** and **PIX Emily** Chatterbox voices, 13 approved pixel character poses, and default 1920×1080 long-form timeline.
- Duik exports must use owner-approved assets. Do **not** substitute rig demonstration characters for the approved UrFavXBF/PIX character identities.
- No native/live Duik expression playback, IK solving, puppet editing, or automatic conversion of proprietary `.aep` files in GitHub Actions.
- The tests prove our importer and Remotion playback of an **original** baked-vector fixture; they do not prove any specific third-party Duik export is semantically/render-wise compatible.

## References

- [Official Duik manual](https://duik.org/guide/Angela/)
- [Duik open-source repository and GPLv3](https://github.com/RxLaboratory/Duik)
- [Duik bake API](https://duik.org/api/Angela/DuAELayer.html)
- [Remotion After Effects / Bodymovin guide](https://www.remotion.dev/docs/after-effects)
- [Remotion Lottie limitations](https://www.remotion.dev/docs/lottie/lottie)
