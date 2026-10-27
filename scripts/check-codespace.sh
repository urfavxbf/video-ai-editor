#!/usr/bin/env bash
# Check the Video AI Editor Codespaces setup without printing any secret values.
set -euo pipefail
cd "$(dirname "$0")/.."

check_command() {
  local label="$1" command_name="$2"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "MISSING: $label ($command_name)"
    return 1
  fi
  echo "OK: $label"
}

echo "Video AI Editor — Codespaces verification"
check_command "Node.js" node
node -e 'if (parseInt(process.versions.node.split(".")[0], 10) < 22) { console.error("Node.js 22+ is required"); process.exit(1); }'
check_command "npm" npm
check_command "FFmpeg" ffmpeg
check_command "FFprobe" ffprobe

if test ! -x .venv/bin/python; then
  echo "MISSING: Python virtual environment (.venv). Run: bash scripts/setup-ai-video-tools.sh"
  exit 1
fi
.venv/bin/python -c 'import groq, numpy, PIL; print("OK: Groq SDK, NumPy, Pillow")'
test -x node_modules/.bin/remotion || {
  echo "MISSING: Remotion CLI. Run: npm ci"
  exit 1
}
echo "OK: Remotion CLI"
npm run typecheck

if [[ -n "${GROQ_API_KEY:-}" ]]; then
  echo "OK: GROQ_API_KEY environment variable is available (not tested against API)"
else
  echo "OPTIONAL: GROQ_API_KEY missing. Add it in GitHub Settings > Codespaces > Secrets."
fi

echo "Codespaces editor setup verified."
