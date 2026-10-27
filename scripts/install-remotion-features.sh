#!/usr/bin/env bash
# Install actual official Remotion feature packages, distinct from Remotion Agent Skills.
# All Remotion packages MUST share the same exact version.
set -euo pipefail
cd "$(dirname "$0")/.."
runtime="$(node -p 'require("./package.json").dependencies.remotion')"
[[ "$runtime" =~ ^[0-9]+[.][0-9]+[.][0-9]+$ ]] || { echo "Expected pinned Remotion version, got: $runtime"; exit 1; }
echo "Installing official Remotion feature modules at $runtime (same as the core runtime)"
npm install --save-exact --no-audit --no-fund \
  "@remotion/captions@$runtime" \
  "@remotion/transitions@$runtime" \
  "@remotion/shapes@$runtime" \
  "@remotion/effects@$runtime" \
  "@remotion/sfx@$runtime" \
  "@remotion/player@$runtime" \
  "@remotion/motion-blur@$runtime"
npm ci --no-audit --no-fund
npm run typecheck
node - <<'NODE'
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json','utf8'));
const lock = JSON.parse(fs.readFileSync('package-lock.json','utf8'));
const version = pkg.dependencies.remotion;
const names=['captions','transitions','shapes','effects','sfx','player','motion-blur'];
for(const name of names){
  const id='@remotion/'+name;
  if(pkg.dependencies[id]!==version) throw Error('Mismatched '+id+' version');
  if(lock.packages['node_modules/'+id]?.version!==version) throw Error('Lock file missing '+id);
  console.log('OK:',id,version);
}
console.log('All seven feature modules are installed at the existing Remotion runtime version.');
NODE
