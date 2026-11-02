# Original UrFavXBF 8-bit host — active sprite pack (2026-11-02)

The latest explicit owner request replaces the **production UrFavXBF visual** with an original 8-bit character in a navy jacket, gray hood and Philippine-flag patch. This is derived from the concept-board style in the conversation, **not a physical likeness or extracted transparent sheet crop**.

## Stored assets

- `public/characters/8bit-host/urfavxbf/{action}/frame-00.svg` through the last indexed frame
- `characters/8bit-host-sprite-manifest.json` — 15 actions, **116 frame-specific transparent SVGs**, 72×82 pixel viewBox, 8fps playback
- `scripts/generate_8bit_host_sprites.mjs` — deterministically regenerates these original assets; committed SVG frames are the runtime assets
- `src/characters/PixelPoseCharacter.tsx` — production action/frame selector, also used in `HeroCharacterStage` and `EpisodeProduction`
- `characters/8bit-host-motions.json` — **33 demo motion presets and complete explainer script**; `Host33MotionShowcase` composition stages an animated silent storyboard

Original blue-coat host replaces the old neon-green UrFavXBF **in current production compositions**. PIX retains the 7 original committed PNGs. Earlier PNG poses and their SHA-256 manifest are kept for archival reproduction and rollback.

## Play and verify

```bash
npm ci
node scripts/generate_8bit_host_sprites.mjs
python3 -m unittest tests.test_8bit_host_sprite_pack -v
npm run typecheck
npx remotion still Host33MotionShowcase out/8bit-host-still.png --frame=25
npx remotion render Host33MotionShowcase out/8bit-host-33-motions.mp4 --codec=h264 --pixel-format=yuv420p
```

This **silent** preview is a separate 33-motion educational performance, *not* the existing 33 source-video effects in `FxPreview`/`ExampleEdit`. For actual episodes use selective real media effects, not 33 transitions pasted indiscriminately. The demo's narration is stored as `narration` strings and on-screen text, but **no voiceover WAV has been generated**. English Chatterbox V3 default voice profiles remain unchanged and require real sampled audio before lips/captions are aligned. These are distinct drawn sprite frames, **not phoneme-accurate mouth shapes**.

The 116 frame assets and their source generator are committed; full audiovisual/CI render acceptance requires executing the commands above and inspecting frames. No paid APIs, GPUs, uploaded footage, automatic publication or merge to `main`.
