const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const ts = require('typescript');
const {test} = require('node:test');
function load(file) {
 const filename=path.resolve(__dirname,'../',file), m=new Module(filename,module);
 m.filename=filename;m.paths=Module._nodeModulePaths(path.dirname(filename));
 m._compile(ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
 return m.exports;
}
const target=path.resolve(__dirname,'../src/showcase/showreelTimeline.ts');
test('showreel timeline is implemented',()=>assert.ok(fs.existsSync(target),'missing cinematic showreel timeline'));
if (fs.existsSync(target)) {
 const t=load('src/showcase/showreelTimeline.ts');
 const registry=load('src/compositionMetadata.ts');
 test('every registered FX appears exactly once',()=>{
  const expected=[...registry.EDIT_EFFECT_IDS,...registry.ADVANCED_EFFECT_IDS].sort();
  assert.deepEqual(t.SHOWREEL_SHOTS.map(s=>s.id).sort(),expected);
  assert.equal(new Set(t.SHOWREEL_SHOTS.map(s=>s.id)).size,33);
 });
 test('intro, effects and outro cover the timeline contiguously within 60–90 seconds',()=>{
  let end=t.INTRO_FRAMES;
  for(const shot of t.SHOWREEL_SHOTS){assert.equal(shot.at,end);assert.ok(shot.frames>=60);end+=shot.frames;}
  assert.equal(end+t.OUTRO_FRAMES,t.SHOWREEL_FRAMES);
  assert.ok(t.SHOWREEL_FRAMES>=1800&&t.SHOWREEL_FRAMES<=2700);
 });
 test('all 16 approved poses are selected and no unknown poses occur',()=>{
  const manifest=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../characters/pixel-default-manifest.json')));
  for(const id of ['urfavxbf','pix']) {
   const poses=t.SHOWREEL_SHOTS.map((_,i)=>t.shotPose(id,i));
   assert.deepEqual([...new Set(poses)].sort(),Object.keys(manifest.characters[id].poses).sort());
  }
 });
 test('effect lookup rejects unknown IDs rather than producing a silent blank',()=>{
  assert.throws(()=>t.assertShowreelEffect('not-real'),/Unknown showreel effect/);
  assert.throws(()=>t.assertShowreelEffect('__proto__'),/Unknown showreel effect/);
  assert.equal(t.assertShowreelEffect('orbit'),'orbit');
 });
}
if (fs.existsSync(target)) {
 const t=load('src/showcase/showreelTimeline.ts');
 test('all poses remain visible in character shots, excluding typography-only passages',()=>{
  assert.ok(t.MATERIAL_EFFECT_IDS,'material passages need an explicit coverage contract');
  const audio=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../src/showcase/showreel-audio.json')));
  const manifest=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../characters/pixel-default-manifest.json')));
  for(const id of ['urfavxbf','pix']) {
   const seen=new Set();
   for(const shot of t.SHOWREEL_SHOTS.filter(s=>!t.MATERIAL_EFFECT_IDS.includes(s.id))) {
    for(let frame=shot.at+20;frame<shot.at+shot.frames;frame++) {
     const speaking=audio.ready&&audio.voices.some(v=>v.character===id&&frame>=v.at&&frame<v.at+v.frames);
     seen.add(t.performancePose(id,shot.index,frame-shot.at,speaking));
    }
   }
   assert.deepEqual([...seen].sort(),Object.keys(manifest.characters[id].poses).sort());
  }
 });
}
if (fs.existsSync(target)) {
 const t=load('src/showcase/showreelTimeline.ts');
 test('a speaking character still demonstrates each authored expression before returning to talk',()=>{
  assert.equal(typeof t.performancePose,'function','missing authored-expression hold');
  for(const id of ['urfavxbf','pix']) {
   for(const shot of t.SHOWREEL_SHOTS) {
    for(let f=0;f<36;f++)assert.equal(t.performancePose(id,shot.index,f,true),t.shotPose(id,shot.index));
    assert.equal(t.performancePose(id,shot.index,40,true),id==='pix'?'talk':'explaining');
    assert.equal(t.performancePose(id,shot.index,40,false),t.shotPose(id,shot.index));
   }
  }
 });
}
