# Real 21-FX Motion Showreel — not a slideshow

This composition is a **real filmed-style motion-graphics showreel** using
the repository's **actual 21 effect components** rendered in sequence, followed
by playback of its three motion engine bridges:
local Lottie vectors, a baked Duik-style puppet (not a real Duik-export sample),
and HyperFrames locally rendered HTML/GSAP animation.

Every effect runs over **changing actual video frames** and local person
cutout/sticker mattes, not a background image with title cards. All shots
share a single bold 1920×1080 broadcast-style graphical layout with
continuously animated footage, kinetic titles, wipes, effects, compositing,
live index/timing and an **original procedurally composed soundtrack**.
Existing legacy SFX files are intentionally *not used* since their commercial
distribution rights are not independently verified.

## Source and rights

- `scripts/generate_motion_reel_source.py` builds an original 10-second
  animated 540×960 source video and synchronized WebP mattes/stickers using
  **only the repo's approved UrFavXBF and PIX art**. Sources remain ignored
  under `public/sample/`. The original sprites retain their exact hashes;
  the software creates a new derived work for this specific showreel.
- This is **animated pose swaps**, not phoneme lip-sync, human recording
  or a 3D model. FX titles and demo UI copy are illustrative **fictional**
  example data, not verified news or revenue metrics.
- `scripts/generate_motion_reel_score.py` synthesizes the master soundtrack
  using local NumPy sine waves and seeded noise; no third-party music,
  provider account or API.
- Approved English Chatterbox voice profiles remain unchanged; this reel
  is **music-only**, not a narrated episode.
- `npm run hyperframes:render` runs the existing local HyperFrames bridge and
  stages the animation for the final scene. No cloud rendering.

## Render and validate

```bash
npm ci
python3 -m pip install -r requirements.txt
python3 scripts/stage_pixel_default_pack.py --verify-workspace
python3 scripts/generate_motion_reel_source.py --output public/sample
npm run hyperframes:render
npm run typecheck
npx remotion render MotionShowreel out/motion-showreel/video-only.mp4 \
  --codec=h264 --crf=21 --pixel-format=yuv420p --concurrency=2
# generate an exact-length procedural original soundtrack:
python3 scripts/generate_motion_reel_score.py \
  --seconds "$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 out/motion-showreel/video-only.mp4)" \
  --output out/motion-showreel/original-score.wav
ffmpeg -y -i out/motion-showreel/video-only.mp4 \
  -i out/motion-showreel/original-score.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart \
  out/motion-showreel/Real_21_FX_Motion_Showreel.mp4
```

Production-quality gate: video 1920×1080 / 30fps, 21 segments present,
3 engine demonstrations, verified duration and H.264/AAC streams, full
decode, representative frames from each effect, audible score and no
missing matte requests. The CI workflow renders a test preview and
attaches the full playable MP4 as an Actions artifact, **not** only a still.
No claim of a finished narrated episode or that every numerical UI label
describes real data.

The raw test artifacts are intermediate, *not* public stock assets.
