# HeroCharacterStage and ExampleEdit duration inputs

Both compositions retain their dimensions and 30 fps. Their Remotion
`calculateMetadata` callbacks use the merged input props selected for that render.

- `HeroCharacterStage` uses `durationFrames` when supplied. Omitting the field
  (or passing `undefined` from JavaScript) retains the 540-frame default.
  Explicit `null`, strings and other invalid values are rejected. Audio and
  voice events do not silently infer or override an explicitly selected duration.
- `ExampleEdit` sums the `frames` of the supplied `spec.segments` in cut-list
  order. Source `at` offsets, repeated clips and FX duration do not extend this
  consecutive output timeline. With no input override, the checked-in edit
  specification still produces 299 frames.
- Durations must be finite safe integers from **1 through 108,000 frames**
  inclusive (one hour at the fixed 30 fps). This cap applies to each duration
  and the total edit timeline. Requests above it fail; they are never truncated.
- An edit must contain at least one segment. Each segment must have kind
  `aroll` or `fx`, a positive duration within the cap, and a non-negative safe
  integer source `at` offset. Empty lists, malformed segments, zero, negative,
  fractional and non-finite values fail with an error identifying the field.

These checks validate duration/timeline inputs, not media availability, source
EOF, paths or effect IDs. No footage, voices, artwork or production defaults
were changed. A longer-duration policy can change the shared cap in
`src/compositionMetadata.ts` through a separately reviewed change.

## Regression checks

```sh
node --test tests/composition-duration.test.cjs
node scripts/check-composition-metadata.mjs
```

The first command compiles the actual pure TypeScript metadata module using
the existing TypeScript dependency and tests defaults, valid boundaries,
900/10-frame overrides, repeated/offset cuts, invalid inputs and cumulative caps.
The second bundles the actual application and calls Remotion `selectComposition`
against both registered compositions. It needs a supported browser but no
source footage, narration, API keys or GPU. On a host with a preinstalled
Chromium, set `REMOTION_BROWSER_EXECUTABLE=/path/to/chromium` for that command.
Both commands run in the existing unconditional PR safety workflow.

The reproduced registration outputs before and after the change are:

| Composition/input | Before | After |
| --- | ---: | ---: |
| Hero, defaults | 540 | 540 |
| Hero, `durationFrames: 900` | 540 | 900 |
| ExampleEdit, defaults | 299 | 299 |
| ExampleEdit, supplied ten-frame cut list | 299 | 10 |
