# Spritesheets.ai Open Source Integration — Existing Asset Import

## Verified upstream source

- Public repository: https://github.com/spritesheets-ai/spritesheets-companion
- Code inspected: `downloader.go`, `batch.go`, `server.go`, `README.md`, and `docs/03-architecture-and-tools.md`.
- Main behavior: `save_image` downloads one existing Spritesheets.ai asset by image URL/storage key; `save_batch` downloads a list, limited to four concurrent workers. It is a **local stdio MCP tool**, not a cloud generation service.
- Upstream README declares MIT licensing. Do not assume the cloud model or generation service is open-source. Verify license metadata before distributing any verbatim copied code.
- Documentation mentions `save_batch(items)`, but actual published `server.go` accepts `keys` and not a separate `items` argument, so use the live server schema, not just documentation.
- An existing Spritesheets.ai cloud generation request is still subject to authentication, subscription and credits. This adapter makes **zero cloud generation calls**.

## Adaptation in this repo

`scripts/import_sprite_animation.py` is an independent Python adaptation of
the companion's existing-asset import idea, designed for the Remotion runtime.
It accepts **already available** GIFs, PNG grid spritesheets or numbered PNG
frame directories, and yields:

```text
public/characters/imported/
  urfavxbf/
    idle_normal/
      000.png
      001.png
      ...
      manifest.json
  pix/
    walk/
      000.png
      ...
      manifest.json
```

- Originals stay untouched, overwritten outputs are refused.
- Every output is transparent RGBA, and opaque/colored backgrounds are rejected
  by default. Use `--allow-opaque` only for review of sources that are not
  genuinely transparent; it does NOT perform background removal.
- Animated GIF frame durations are preserved; PNG inputs accept `--fps`.
- 1–600 real source frames, sorted numerically when files have zero-padded
  names. Does not hallucinate missing animation poses.
- Output has SHA-256 per frame, native pixel dimensions, loop flag and
  honest `draft-requires-owner-visual-review` label.
- Tiny art receives explicit resolution warnings. A 1080p Remotion canvas
  does not make 64×78 source pixels into detailed 1080p sprites.
- Nothing is committed from `public/characters/imported/` by default.

## Usage

Stage an existing GIF from Spritesheets.ai or another generator:

```bash
python scripts/import_sprite_animation.py \
  --source /path/to/urfavxbf-idle.gif \
  --character urfavxbf --action idle_normal --loop
```

For a PNG sheet laid out as 8 equally sized columns × 1 row:

```bash
python scripts/import_sprite_animation.py \
  --source /path/to/urfavxbf-walk.png --columns 8 --rows 1 \
  --character urfavxbf --action walk --fps 8 --loop
```

Or a folder of frame PNGs:

```bash
python scripts/import_sprite_animation.py \
  --source /path/to/pix-frames/ --character pix --action talking --fps 10
```

The source directory must contain already separated, aligned PNG frames.
JSON-atlas rectangles from third-party providers need their own atlas adapter
and are not automatically interpreted as an equal-sized grid.

After importing, read the action's `manifest.json`. Render a private
1080p asset review via the `ImportedSpriteAnimationReview` Remotion
composition. Use its `character`, `action`, `durationsMs`, `loop` and
`assetsReady:true` props, for example:

```bash
npx remotion still ImportedSpriteAnimationReview out/review.png --frame=30 \
  --props='{"character":"urfavxbf","action":"idle_normal","durationsMs":[125,125,125,125],"loop":true,"assetsReady":true}'
```

If private PNGs have not been staged, keep `assetsReady:false`; the
composition will show a staging placeholder instead of an invented image.

## Current limitations

- This importer does not create new character art, rig a model, upscale
  source pixels, remove watermarks, create phoneme visemes, or download
  OAuth-protected content.
- The official Go local companion can be run on a machine in Cursor,
  Claude Desktop, Windsurf or a runner; **it is not a remote ChatGPT HTTP
  connector**, nor can it directly write to the user's Android phone from
  ChatGPT's cloud runtime.
- No new Spritesheets.ai generation credits are spent by this import tool.
- Source/license rights and any provider export restrictions still apply.

## Other relevant open-source reference

`aldegad/sprite-gen` (Apache-2.0) has a richer post-processing pipeline:
frame extraction, alpha cleanup, manual curation, and manifest writing.
It still depends on input art or a configured image-generation model and
is not the official Spritesheets.ai generator.

https://github.com/aldegad/sprite-gen
