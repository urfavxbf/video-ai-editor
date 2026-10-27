#!/usr/bin/env bash
# Render Dudut's uploaded podcast clip with premium Remotion motion design.
# Usage: bash scripts/render-dudut.sh input/50812.mp4
set -euo pipefail
cd "$(dirname "$0")/.."

source_path="${1:-input/50812.mp4}"
if [[ ! -f "$source_path" ]]; then
  echo "Source clip not found: $source_path" >&2
  echo "Place the original clip at input/50812.mp4 or pass its path as the first argument." >&2
  exit 2
fi

command -v ffmpeg >/dev/null || { echo "Missing ffmpeg"; exit 2; }
command -v ffprobe >/dev/null || { echo "Missing ffprobe"; exit 2; }
command -v npm >/dev/null || { echo "Missing npm"; exit 2; }

duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$source_path")
width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$source_path")
height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$source_path")

if ! awk -v d="$duration" 'BEGIN { exit !(d >= 84) }'; then
  echo "Dudut edit needs a source clip of at least 84 seconds; found ${duration}s." >&2
  exit 2
fi
echo "Source: ${width}x${height}, ${duration}s"
echo "Selecting source 00:42.00 - 01:24.00; preserving original sound and landscape speaker framing."

mkdir -p public/takes/dudut out
# Keep the original codec/resolution; no extra lossy preprocessing.
cp -f "$source_path" public/takes/dudut/clip.mp4
npm run typecheck
npx remotion render DudutPremium out/dudut-premium-1080x1920.mp4 \
  --codec=h264 --crf=16 --pixel-format=yuv420p \
  --audio-codec=aac --audio-bitrate=256k --concurrency=2

test -s out/dudut-premium-1080x1920.mp4
echo "Rendered: out/dudut-premium-1080x1920.mp4"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=noprint_wrappers=1 out/dudut-premium-1080x1920.mp4
