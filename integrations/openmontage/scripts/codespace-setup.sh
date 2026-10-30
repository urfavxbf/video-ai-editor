#!/usr/bin/env bash
# Used only by the optional OpenMontage Codespaces configuration.
set -euo pipefail
integration_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v ffmpeg >/dev/null 2>&1 || ! command -v ffprobe >/dev/null 2>&1; then
  if ! command -v sudo >/dev/null 2>&1; then
    echo "FFmpeg is missing and sudo is not available; install FFmpeg manually." >&2
    exit 1
  fi
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg
fi

bash "$integration_dir/scripts/setup.sh"
bash "$integration_dir/scripts/doctor.sh"
