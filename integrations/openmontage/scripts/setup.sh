#!/usr/bin/env bash
# Install a pinned OpenMontage checkout strictly inside integrations/openmontage/.runtime.
set -euo pipefail

integration_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime_dir="$integration_dir/.runtime/openmontage"
upstream_url="https://github.com/calesthio/OpenMontage.git"
pinned_commit="$(tr -d '[:space:]' < "$integration_dir/UPSTREAM_COMMIT")"
skip_tts=false

if [[ "${1:-}" == "--skip-tts" ]]; then
  skip_tts=true
elif [[ "$#" -ne 0 ]]; then
  echo "Usage: bash integrations/openmontage/scripts/setup.sh [--skip-tts]" >&2
  exit 2
fi

if [[ ! "$pinned_commit" =~ ^[0-9a-f]{40}$ ]]; then
  echo "Invalid upstream commit pin" >&2
  exit 1
fi

for binary in git python3 node npm ffmpeg ffprobe; do
  if ! command -v "$binary" >/dev/null 2>&1; then
    echo "Missing required command: $binary" >&2
    exit 1
  fi
done

python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || {
  echo "OpenMontage requires Python >= 3.10" >&2
  exit 1
}
node -e 'process.exit(Number(process.versions.node.split(".")[0]) >= 18 ? 0 : 1)' || {
  echo "OpenMontage requires Node.js >= 18" >&2
  exit 1
}

mkdir -p "$runtime_dir"
if [[ ! -d "$runtime_dir/.git" ]]; then
  git -C "$runtime_dir" init -q
  git -C "$runtime_dir" remote add origin "$upstream_url"
fi

if [[ "$(git -C "$runtime_dir" remote get-url origin)" != "$upstream_url" ]]; then
  echo "Unexpected OpenMontage remote URL; refusing to modify checkout" >&2
  exit 1
fi

current_commit="$(git -C "$runtime_dir" rev-parse HEAD 2>/dev/null || true)"
if [[ "$current_commit" != "$pinned_commit" ]]; then
  if [[ -n "$(git -C "$runtime_dir" status --porcelain --untracked-files=no)" ]]; then
    echo "OpenMontage checkout contains modified tracked files; refusing to overwrite" >&2
    exit 1
  fi
  git -C "$runtime_dir" fetch --depth 1 origin "$pinned_commit"
  git -C "$runtime_dir" -c advice.detachedHead=false checkout --detach --force "$pinned_commit"
fi

actual_commit="$(git -C "$runtime_dir" rev-parse HEAD)"
if [[ "$actual_commit" != "$pinned_commit" ]]; then
  echo "Upstream checkout does not match the reviewed SHA" >&2
  exit 1
fi

cd "$runtime_dir"
if [[ ! -x ".venv/bin/python" ]]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt

if [[ -f remotion-composer/package-lock.json ]]; then
  (cd remotion-composer && npm ci --no-audit --no-fund)
else
  (cd remotion-composer && npm install --no-audit --no-fund)
fi

if [[ "$skip_tts" != true ]]; then
  if ! .venv/bin/python -m pip install piper-tts; then
    echo "WARNING: Optional Piper TTS install failed; narration requires a working provider."
  fi
fi

if [[ ! -f .env ]]; then
  cp .env.example .env
  chmod 600 .env
fi

echo "OpenMontage pinned checkout installed at: $runtime_dir"
echo "No changes were made to the host project's dependencies or Remotion sources."
echo "Next: bash integrations/openmontage/scripts/doctor.sh"
