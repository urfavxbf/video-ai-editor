# Character assets: installed and verified

**Status as of 2026-10-29:** The original 13 independently generated transparent PNG poses for UrFavXBF and PIX are **already committed** to this branch, with 1254 × 1254 resolution and original SHA-256 hashes matching `characters/pixel-default-manifest.json`.

- **UrFavXBF:** 6 poses including surprised (`!`).
- **PIX:** 7 poses including question (`?`) and surprised (`!`).
- **Location:** `public/characters/pixel-default/{character}/{pose}.png`.
- **Default selection:** `src/characters/CanonicalCharacterAssets.ts` and `src/characters/PixelPoseCharacter.tsx`.
- **Source:** Independently drawn owner-selected pixel chibi poses, no crops from the source sheets.
- **No rejected visual fallback, no paid services, original English voices preserved.**

The one-time import was performed successfully by GitHub Actions workflow [40845188627](https://github.com/urfavxbf/video-ai-editor/actions/runs/40845188627). It also generated the **UrFavXBF-PIX-real-pose-production-proof** screenshot artifact. This installer workflow remains only for a future deliberate asset replacement and is **not** required to start rendering with the now-committed poses.

For future checks:

```bash
python scripts/stage_pixel_default_pack.py --verify-workspace
npm ci
npm run typecheck
npx remotion still PixelProductionProof out/pixel-production-proof.png --frame=170 --scale=0.5 --props='{"assetsReady":true}'
```

The character default is ready **on this PR branch**; it becomes the default on `main` only after a successful merge. Voice synchronization and full-length episode assembly are separate steps, not guaranteed by a pose smoke test.
