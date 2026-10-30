# Original Motion Toolkit

This opt-in Remotion toolkit provides reusable, frame-driven text entrances and
exits for future compositions. It does not change any existing composition,
character, voice, or production default.

## Existing motion audit

| Capability | Status | Existing implementation |
| --- | --- | --- |
| Footage FX movement | Usable, effect-specific | `src/fx/shared.tsx` provides `fxSpring`, `popSpring`, and clamped progress; effects such as `src/fx/HeadlineStorm.tsx` own their banner motion and typography. |
| Text entrances | Partial, not a shared API | `HeadlineStorm` animates fixed banners; `src/features/OfficialFeaturesDemo.tsx` fades a fixed headline with `interpolate`. Neither exposes reusable title presets. |
| Scene transitions | Usable for scene boundaries | `@remotion/transitions` is already used by `OfficialFeaturesDemo`; it does not animate text units. |
| Typed text presets and easing controls | Missing before this toolkit | No prior shared title preset catalog or timing contract was found. |
| Exits, stagger, and reduced-motion fallback | Missing before this toolkit | Added as opt-in behavior in `src/motion/MotionText.tsx`. |

The new motion module reuses Remotion's frame clock rather than CSS animation,
and adds no runtime dependency. No Qwix code, commercial presets, assets,
branding, or interface materials were copied or imported.

## Use in a composition

```tsx
import { MotionText } from '../motion/MotionText'

export const ChapterTitle = () => (
  <MotionText
    text="A title that moves with the story"
    preset="cleanSlide"
    fromFrame={12}
    durationInFrames={28}
    easing="ease-out"
    color="#F3F4EF"
    fontFamily="'Montserrat', sans-serif"
    fontSize={72}
    fontWeight={800}
    exitAtFrame={150}
    exitDurationInFrames={18}
    exitVariant="fade"
  />
)
```

Available presets are `signalFade`, `cleanSlide`, `softScale`, `impactBounce`,
`windowReveal`, and `wordCascade`. Pass a complete `MotionPreset` object to
define an original preset. `fromFrame`, duration, easing, direction, distance,
scale, stagger spacing, typography, and text color can be overridden on
`MotionText`. Set `reducedMotion` to disable transform animation while retaining
the scheduled visibility window. Text is frame-deterministic and can be timed
from an existing narration or caption event in the composition.

The landscape `MotionToolkitDemo` composition is 1920×1080 at 30 fps and runs
for eight seconds. Render it with:

```bash
npx remotion render MotionToolkitDemo out/motion-toolkit-demo.mp4 --scale=0.5 --codec=h264 --crf=21 --pixel-format=yuv420p
```

The PR safety workflow runs the focused motion tests, renders the demo, verifies
its 960×540 H.264 stream at 30 fps, and uploads the MP4 with the existing
model-free fixture artifact.