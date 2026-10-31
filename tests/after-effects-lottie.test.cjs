const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {test} = require('node:test');
const root = path.resolve(__dirname, '..');
const animation = JSON.parse(fs.readFileSync(path.join(root, 'src/after-effects/original-growth.json'), 'utf8'));
const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
const registered = fs.readFileSync(path.join(root, 'src/Root.tsx'), 'utf8');

test('bundled original Bodymovin/Lottie sample is local and valid', () => {
  assert.equal(animation.w, 900);
  assert.equal(animation.h, 900);
  assert.equal(animation.fr, 30);
  assert.ok(animation.op > animation.ip);
  assert.ok(Array.isArray(animation.layers) && animation.layers.length === 3);
  assert.deepEqual(animation.assets, []);
  assert.equal(JSON.stringify(animation).includes('http://'), false);
  assert.equal(JSON.stringify(animation).includes('https://'), false);
  assert.ok(animation.layers.every(l => l.ty === 4 && l.shapes.some(s => s.ty === 'el')));
  assert.ok(animation.layers.some(l => l.ks.s.a === 1));
});

test('bridge pins Remotion package versions and registers explicit proof only', () => {
  assert.equal(pkg.dependencies['@remotion/lottie'], '4.0.522');
  assert.equal(pkg.dependencies['lottie-web'], '5.13.0');
  assert.equal(pkg.dependencies['@remotion/lottie'], pkg.dependencies.remotion);
  assert.match(registered, /id="AfterEffectsLottieProof"/);
  assert.ok(registered.includes('width={1080} height={1920} fps={30}'));
});
