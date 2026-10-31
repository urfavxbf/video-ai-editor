#!/usr/bin/env bash
# Reproducible Linux Codespaces/Actions setup. Does not contact Groq or disclose credentials.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  command -v apt-get >/dev/null || { echo "Install FFmpeg and FFprobe first." >&2; exit 1; }
  sudo apt-get update
  sudo apt-get install -y ffmpeg
fi

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo "Install Node.js 22+ (Codespaces: nvm install 22 && nvm use 22)." >&2
  exit 1
fi
node_major="$(node -p "Number(process.versions.node.split('.')[0])")"
if (( node_major < 22 )); then
  echo "Node.js 22+ required, found $(node -v). Run nvm install 22 && nvm use 22." >&2
  exit 1
fi

echo "== Installing pinned Remotion / React =="
npm ci --no-audit --no-fund
echo "== Installing Python dependencies and Groq client =="
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt 'groq>=0.30,<2'
echo "== Installing official HyperFrames core skills =="
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 ./node_modules/.bin/hyperframes skills update
echo "== Ensuring browser renderer =="
npx remotion browser ensure
echo "== Validating installation (never reveal secrets) =="
node -p "'Node: ' + process.version + ' / Remotion: ' + require('./node_modules/remotion/package.json').version"
.venv/bin/python -c 'import groq, numpy, PIL; print("Groq SDK, NumPy, Pillow: OK")'
ffmpeg -version | sed -n '1p'
ffprobe -version | sed -n '1p'
npm run typecheck
if test -n "${GROQ_API_KEY:-}"; then
  echo "Groq key detected in this environment (not validated with API)."
else
  echo "Groq key not detected; save GROQ_API_KEY as a Codespaces secret to use transcription."
fi
echo "Video editor tools are installed."
