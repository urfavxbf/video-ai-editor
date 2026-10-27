#!/usr/bin/env bash
# Render revised Dudut V2: motion-design-first podcast edit.
set -euo pipefail
cd "$(dirname "$0")/.."
source_path="${1:-input/50812.mp4}"
test -f "$source_path" || { echo "Missing source: $source_path" >&2; exit 2; }
for tool in ffmpeg ffprobe npm; do
  command -v "$tool" >/dev/null || { echo "Missing dependency: $tool" >&2; exit 2; }
done
duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$source_path")"
awk -v d="$duration" 'BEGIN { exit !(d >= 84) }' || { echo "Input must be at least 84 seconds"; exit 2; }
mkdir -p public/takes/dudut out
cp -f "$source_path" public/takes/dudut/clip.mp4
npm run typecheck
npx remotion render DudutV2 out/dudut-v2-cinematic-1080x1920.mp4 \
  --codec=h264 --crf=16 --pixel-format=yuv420p \
  --audio-codec=aac --audio-bitrate=256k --concurrency=2
test -s out/dudut-v2-cinematic-1080x1920.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate -show_entries format=duration -of default=noprint_wrappers=1 out/dudut-v2-cinematic-1080x1920.mp4
