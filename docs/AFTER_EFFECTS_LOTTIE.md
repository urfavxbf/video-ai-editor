# After Effects graphics → Remotion (Bodymovin + Lottie)

## Goal
Import supported After Effects motion-graphics animations without running Adobe After Effects on the render server. **Bodymovin is a free After Effects desktop extension**, while `@remotion/lottie` plays exported Lottie JSON in our existing Remotion / FFmpeg video editor.

This is a small **opt-in vector-animation bridge**, not an Adobe renderer, a replacement video editor, an external SaaS, or an auto-generating AI agent. It does not change the approved English Chatterbox V3 voices, UrFavXBF/PIX characters, or default 1920×1080 long-form episode format.

## Local demo
Open Remotion Studio and select `AfterEffectsLottieProof`. This portrait, 30 fps original test composition imports a **hand-authored Lottie JSON** (`src/after-effects/original-growth.json`) and uses typed `<Lottie>` playback with kinetic text.

```bash
npm ci
npm run typecheck
node --test tests/after-effects-lottie.test.cjs
npx remotion still AfterEffectsLottieProof out/ae-lottie-proof.png --frame=40
npx remotion render AfterEffectsLottieProof out/ae-lottie-proof.mp4 --codec=h264 --pixel-format=yuv420p
```

All sample artwork is original. No Adobe app or subscription is needed to **run** the Remotion demo.

## Use your own After Effects artwork
1. Install **Bodymovin** on a workstation that already has a properly licensed Adobe After Effects installation, following [Remotion's official guide](https://www.remotion.dev/docs/after-effects).
2. Animate supported vector shapes and transforms. In Bodymovin choose the composition and export as **JSON**.
3. Review file license, fonts, external images and linked paths. Keep files local. Avoid placing private or unlicensed artwork in a public repository.
4. Place the approved JSON under `src/after-effects/` and import it from a composition the same way as `original-growth.json`. Replace `<Lottie animationData={originalGrowth} />` with your own imported JSON.
5. Register a separate composition in `src/Root.tsx` only after rendering and checking real frames (dimensions, frame rate, visual fidelity, duration, audio).
6. If your JSON references images, stage them as approved local assets and validate rendering; the demo intentionally avoids external images.

## Limitations and quality gates
- **Not full After Effects compatibility:** 3D, third-party AE effects, expressions, certain fonts, raster assets, mattes and filters may require a different path or manual recreation.
- Lottie files must be verified for deterministic seeking: render multiple different frames and inspect motion. Rendering a still does not prove all effects and frames are correct.
- Never auto-download untrusted URLs from a Lottie file, install AE plugins in Actions, or assume third-party Lottie libraries are commercially licensed.
- Use current repository production policy; the portrait demo is opt-in and does **not** supersede it.
- Remotion packages are pinned to `4.0.522` to match the existing lockstep versions.
- The branch-only setup workflow generates and commits the npm lockfile only if smoke tests pass. PR safety checks should be green before merging. This does not merge automatically.
- This feature does not provide kinetic text generation from narration, phoneme-level sync, sound design, or licensed illustration assets. Those remain separate production responsibilities.

## Sources
- https://www.remotion.dev/docs/after-effects
- https://www.remotion.dev/docs/lottie/lottie
- https://github.com/airbnb/lottie-web
