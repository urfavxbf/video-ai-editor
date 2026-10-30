#!/usr/bin/env bash
# Render the approved blue-app tutorial via pinned upstream OpenMontage's
# EXISTING Remotion Explainer, not a replacement compositor.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
UPSTREAM="$ROOT/integrations/openmontage/.runtime/openmontage"
COMPOSER="$UPSTREAM/remotion-composer"
PRODUCTION="$ROOT/productions/blue-app-html-history"
MODE="${1:-preview}"
mkdir -p "$ROOT/out/blue-app-tutorial"
test -f "$COMPOSER/package.json" || { echo "OpenMontage not installed" >&2; exit 2; }
python3 "$ROOT/integrations/openmontage/scripts/stage_blue_app_visual.py" \
  --integration "$ROOT/integrations/openmontage" --composer "$COMPOSER"
cd "$COMPOSER"
if [[ "$MODE" == preview ]]; then
  test -s "$PRODUCTION/scene-props.json"
  npx --no-install remotion render src/index.tsx BlueAppVisual \
    "$ROOT/out/blue-app-tutorial/blue-app-preview.mp4" \
    --props "$PRODUCTION/scene-props.json" --scale=0.5 \
    --frames=0-449 --codec=h264 --crf=23 --concurrency=2 \
    --pixel-format=yuv420p
  OUTPUT="$ROOT/out/blue-app-tutorial/blue-app-preview.mp4"
elif [[ "$MODE" == final ]]; then
  test -s "$PRODUCTION/render-props.json" || { echo "Narration props missing" >&2; exit 2; }
  test -s "public/audio/blue-app-narration.wav" || { echo "Approved narrator WAV missing" >&2; exit 2; }
  npx --no-install remotion render src/index.tsx BlueAppVisual \
    "$ROOT/out/blue-app-tutorial/blue-app-final.mp4" \
    --props "$PRODUCTION/render-props.json" \
    --codec=h264 --crf=22 --audio-codec=aac --audio-bitrate=192k \
    --concurrency=2 --pixel-format=yuv420p
  OUTPUT="$ROOT/out/blue-app-tutorial/blue-app-final.mp4"
else
  echo "Expected preview or final" >&2; exit 2
fi
test -s "$OUTPUT"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height \
  -of json "$OUTPUT" > "$ROOT/out/blue-app-tutorial/$MODE-probe.json"
python3 - "$ROOT/out/blue-app-tutorial/$MODE-probe.json" "$MODE" <<'PY'
import json,sys
data=json.load(open(sys.argv[1]))
streams=data.get("streams",[])
video=[s for s in streams if s.get("codec_type")=="video"]
audio=[s for s in streams if s.get("codec_type")=="audio"]
expected=(960,540) if sys.argv[2]=="preview" else (1920,1080)
assert video and (video[0].get("width"),video[0].get("height"))==expected, "Not a 16:9 widescreen MP4"
assert video[0].get("codec_name")=="h264", "Expected H.264"
if sys.argv[2]=="final":
    assert audio and audio[0].get("codec_name")=="aac", "Approved voice not present as AAC"
print("Verified",sys.argv[2],"MP4 streams and 16:9 landscape size.")
PY
echo "Render verified: $OUTPUT"
