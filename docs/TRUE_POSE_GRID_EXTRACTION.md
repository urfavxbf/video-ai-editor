## Offline generated pose-grid extraction (no provider calls)

A reference-guided image model or an artist may supply a **4×2 image of genuinely distinct whole-character poses**, each in its own equally sized cell on pure bright-magenta background. This step is local Python/Pillow, no paid credits:

```sh
python scripts/extract_drawn_pose_grid.py --source poses.png \
  --columns 4 --rows 2 --character urfavxbf --out out/host-pose-studies
```

It exports separate RGBA PNG files, detects boundary-clipped hands/feet, and writes SHA-256 records. This does **not** stitch cells into a fake walking cycle: its manifest explicitly sets `isAnimationLoop=false`. A plausible motion cycle requires purposeful sequential drawings (e.g. contact / recoil / passing / high point) and human playback review. This extractor is separate from the completed-action importer.
