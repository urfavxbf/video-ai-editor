# Installed Remotion features (actual npm modules)

The official Remotion **agent skills** are documentation/workflow guidance; the packages below are **runtime libraries** that supply functionality to video compositions and future editor UI.

Installed via `scripts/install-remotion-features.sh` and version-locked alongside `remotion` in `package.json` and `package-lock.json`. All Remotion packages are pinned to **4.0.522**, matching the existing working project. Do not install a different version of one package in isolation.

| Package | Available functionality | Current implementation |
| --- | --- | --- |
| `@remotion/captions` | Caption data, grouping, highlighting, SRT parsing | `src/features/OfficialFeaturesDemo.tsx` |
| `@remotion/transitions` | Scene TransitionSeries, fade, slide and more | Working showcase composition |
| `@remotion/shapes` | SVG vector shapes and animatable paths | Working showcase composition |
| `@remotion/effects` | Blur, color, distortion and stylize effects on compatible canvas media | Installed; apply selectively in future edits |
| `@remotion/motion-blur` | Motion trail/blur | Installed, not globally enabled |
| `@remotion/sfx` | Official audio cues | Installed; existing imported SFX library remains |
| `@remotion/player` | React video player UI for future editor app | Installed; **not yet an editor website** |

## Preview the real feature integration

Open Remotion Studio and select the **OfficialFeaturesDemo** composition.

The demo has 180 frames at 1080×1920 / 30 FPS, two official transition presentations, animated SVG circles, and token-based timed caption highlighting using `createTikTokStyleCaptions()`.

To test a frame in CI:

```bash
npm ci
npm run typecheck
npx remotion still OfficialFeaturesDemo out/official-feature-demo.png --frame=75
```

## Scope and limitations

- Original Dudut and Doorway compositions remain intact.
- The new libraries do not, by themselves, generate editing decisions, select highlights, transcribe Tagalog audio, or create custom motion graphics autonomously.
- `@remotion/player` is a package for implementing future UI—not a completed mobile editing application.
- Effects that need GPU or browser-specific support need separate output verification.
- Some new upstream features are introduced after 4.0.522; this repository has **not** been upgraded to latest Remotion.
- The Remotion framework has its own license, separate from the repository's third-party notices.
