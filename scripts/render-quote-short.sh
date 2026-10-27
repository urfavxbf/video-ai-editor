#!/usr/bin/env bash
# Render a source-preserving, quote-first vertical interview clip.
# Licensed/authorized media stays local and is never committed to Git.
set -euo pipefail

if (($# < 3)); then
  echo 'Usage: bash scripts/render-quote-short.sh <source.mp4> <typography.ass> <output.mp4>' >&2
  echo 'Environment: SOURCE_START (seconds), DURATION (seconds), CROP_X (pixels), MUSIC (optional wav)' >&2
  exit 2
fi

SOURCE=$1
CAPTIONS=$2
OUTPUT=$3
SOURCE_START=${SOURCE_START:-0}
DURATION=${DURATION:-35}
CROP_X=${CROP_X:-800}
WIDTH=${WIDTH:-1080}
HEIGHT=${HEIGHT:-1920}

command -v ffmpeg >/dev/null || { echo 'ffmpeg is required' >&2; exit 1; }
command -v ffprobe >/dev/null || { echo 'ffprobe is required' >&2; exit 1; }
[[ -f "$SOURCE" && -f "$CAPTIONS" ]] || { echo 'Input video and caption file are required' >&2; exit 1; }
mkdir -p "$(dirname "$OUTPUT")"

# Caption file path for libass must escape any special ffmpeg filter characters.
# Use an absolute path with colon, comma and apostrophe escaping.
CAPTIONS_ABS=$(realpath "$CAPTIONS")
CAPTIONS_FILTER=$(printf '%s' "$CAPTIONS_ABS" | sed -e 's/\\/\\\\/g' -e 's/:/\\:/g' -e 's/,/\\,/g' -e "s/'/\\\\'/g")
video_filter="fps=30,crop=810:1440:${CROP_X}:0,scale=${WIDTH}:${HEIGHT}:flags=lanczos,ass='${CAPTIONS_FILTER}'"
audio_filter="highpass=f=85,acompressor=threshold=-21dB:ratio=2.2:attack=12:release=170:makeup=1.5dB,loudnorm=I=-16:TP=-1.5:LRA=10"

# A continuously flowing source audio track avoids misquoting or chopping the thought.
ffmpeg -hide_banner -y -nostdin \
  -ss "$SOURCE_START" -i "$SOURCE" -t "$DURATION" \
  -vf "$video_filter" -af "$audio_filter" \
  -r 30 -c:v libx264 -preset veryfast -crf 19 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"

ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$OUTPUT"
