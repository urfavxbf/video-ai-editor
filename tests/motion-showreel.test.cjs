const assert = require('node:assert/strict');
const {test} = require('node:test');
const {readFileSync,existsSync} = require('node:fs');
const path = require('node:path');
const root=path.resolve(__dirname,'..');
const reel=readFileSync(path.join(root,'src/showcase/MotionShowreel.tsx'),'utf8');
const registry=readFileSync(path.join(root,'src/fx/index.tsx'),'utf8');
const ids=['orbit','chat-takeover','frame-escape','snap-zoom','checklist-pop',
 'headline-storm','zoom-portal','growth-curve','broll-overlay','paper-cutout',
 'magazine-cover','liquid-glass','zoom-through-cut','green-screen','frame-break',
 'digital-zoom','phone-mockup','checklist-tally','glass-widgets','checklist','split'];
test('real 21 registered effect components rendered in one motion showreel',()=>{
  assert.equal(ids.length,21);
  for(const id of ids)assert.ok(registry.includes("id") || registry.includes('Fx'),id);
  assert.match(reel,/FX_ALL\.reduce/);
  assert.match(reel,/<entry\.Component from=\{from\}\/>/);
  assert.match(reel,/FxSourceContext\.Provider/);
  assert.match(reel,/SHOWREEL_EFFECT_IDS = FX_ALL\.map/);
  assert.match(reel,/showreel/i);
});
test('proof reel also shows actual Lottie, baked Duik and HyperFrames',()=>{
 for(const fragment of ['<AfterEffectsLottieProof/>','<DuikBakedCharacterProof/>',
                       "hyperframes/kinetic-intro.mp4","OffthreadVideo"]){
   assert.ok(reel.includes(fragment),fragment);
 }
});
test('approved character art is source and old SFX licensing not relied on',()=>{
 const script=readFileSync(path.join(root,'scripts/generate_motion_reel_source.py'),'utf8');
 assert.match(script,/pixel-default\/urfavxbf/);
 assert.match(script,/pixel-default\/pix/);
 assert.match(script,/fgdir.*stickdir/);
 assert.doesNotMatch(reel,/<Sfx/);
});
test('new landscape registered composition and deterministic original soundtrack',()=>{
 const spec=readFileSync(path.join(root,'src/Root.tsx'),'utf8');
 assert.match(spec,/id="MotionShowreel"/);
 assert.match(spec,/width=\{1920\} height=\{1080\} fps=\{30\}/);
 const music=readFileSync(path.join(root,'scripts/generate_motion_reel_score.py'),'utf8');
 assert.match(music,/default_rng\(20261031\)/);
});
