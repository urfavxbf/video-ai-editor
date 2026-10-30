#!/usr/bin/env bash
# Read-only, no-secret health check for the isolated OpenMontage installation.
set -euo pipefail
integration_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime_dir="$integration_dir/.runtime/openmontage"
pin="$(tr -d '[:space:]' < "$integration_dir/UPSTREAM_COMMIT")"

if [[ ! -d "$runtime_dir/.git" ]]; then
  echo "Not installed. Run: bash integrations/openmontage/scripts/setup.sh" >&2
  exit 1
fi

actual="$(git -C "$runtime_dir" rev-parse HEAD)"
if [[ "$actual" != "$pin" ]]; then
  echo "ERROR: Checkout SHA does not match UPSTREAM_COMMIT" >&2
  exit 1
fi

for binary in git node npm ffmpeg ffprobe; do
  command -v "$binary" >/dev/null 2>&1 || {
    echo "MISSING: $binary" >&2
    exit 1
  }
done

if [[ ! -x "$runtime_dir/.venv/bin/python" ]]; then
  echo "MISSING: isolated Python virtual environment" >&2
  exit 1
fi

"$runtime_dir/.venv/bin/python" -c 'import yaml, pydantic, PIL, fastapi'
test -d "$runtime_dir/remotion-composer/node_modules" || {
  echo "MISSING: isolated Remotion dependencies" >&2
  exit 1
}
test -f "$runtime_dir/.env" || {
  echo "MISSING: local .env configuration" >&2
  exit 1
}

echo "OK: OpenMontage pinned at $actual"
echo "OK: Python deps, Remotion deps, FFmpeg and local .env"
echo "No credential values were inspected or printed."
