#!/usr/bin/env bash
# Produce one zero-paid-API OpenMontage example and validate its MP4.
set -euo pipefail
integration_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
runtime_dir="$integration_dir/.runtime/openmontage"
demo_name="${1:-world-in-numbers}"

bash "$integration_dir/scripts/doctor.sh"
cd "$runtime_dir"
.venv/bin/python render_demo.py "$demo_name"
output="projects/demos/renders/$demo_name.mp4"

if [[ ! -s "$output" ]]; then
  echo "Render failed: expected non-empty file $output" >&2
  exit 1
fi
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "$output" >/dev/null
echo "Verified rendered video: $runtime_dir/$output"
