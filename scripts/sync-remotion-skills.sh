#!/usr/bin/env bash
# Vendor official Remotion Agent Skills without touching project-specific skills.
# Upstream: https://github.com/remotion-dev/skills
# Source commit pinned so the snapshot is reproducible.
set -euo pipefail
cd "$(dirname "$0")/.."

UPSTREAM_URL="https://github.com/remotion-dev/skills.git"
UPSTREAM_COMMIT="30d4553ecd46fbc5212fd0ff006ae43af522158b"
DEST=".claude/skills"
EXPECTED=(
  remotion-best-practices remotion-captions remotion-create
  remotion-docs remotion-interactivity remotion-maps
  remotion-markup remotion-multimedia remotion-render
  remotion-saas remotion-studio remotion-upgrade
)

command -v git >/dev/null || { echo "git is required" >&2; exit 1; }
temp="$(mktemp -d)"
trap 'rm -rf "$temp"' EXIT

echo "Fetching official Remotion skills at pinned upstream commit"
git clone --depth 1 --no-checkout "$UPSTREAM_URL" "$temp/official" >/dev/null 2>&1
git -C "$temp/official" fetch --depth 1 origin "$UPSTREAM_COMMIT" >/dev/null 2>&1
git -C "$temp/official" checkout --detach "$UPSTREAM_COMMIT" >/dev/null 2>&1
resolved="$(git -C "$temp/official" rev-parse HEAD)"
[[ "$resolved" == "$UPSTREAM_COMMIT" ]] || { echo "Upstream commit mismatch"; exit 1; }

mkdir -p "$DEST"
for name in "${EXPECTED[@]}"; do
  src="$temp/official/skills/$name"
  test -s "$src/SKILL.md" || { echo "Missing upstream skill: $name" >&2; exit 1; }
  # Only official remotion-* folders are updated. Never touch ai-video-editor.
  rm -rf "$DEST/$name"
  cp -a "$src" "$DEST/$name"
  test -s "$DEST/$name/SKILL.md"
done

test -s "$DEST/ai-video-editor/SKILL.md" || {
  echo "Custom project editor skill was unexpectedly missing" >&2
  exit 1
}
count="$(find "$DEST" -mindepth 2 -maxdepth 2 -path '*/remotion-*/SKILL.md' | wc -l)"
test "$count" -eq "${#EXPECTED[@]}" || {
  echo "Expected ${#EXPECTED[@]} Remotion skills, found $count" >&2
  exit 1
}

# Prevent generic embedded skill instructions from being taken as our repo policy.
# Remotion remains an external framework with its own license.
mkdir -p docs
printf '%s\n' "$UPSTREAM_COMMIT" > docs/REMOTION_SKILLS_SOURCE_COMMIT.txt
echo "Synchronized $count official Remotion skills; existing custom skill preserved."
