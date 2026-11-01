const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs');
const path=require('node:path');
const Module=require('node:module');
const ts=require('typescript');
const root=path.resolve(__dirname,'..');
const src=(p)=>fs.readFileSync(path.join(root,p),'utf8');
const typescriptModule=(p)=>{
 const file=path.join(root,p);
 const js=ts.transpileModule(src(p),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
 const mod=new Module(file,module);
 mod.filename=file;mod.paths=Module._nodeModulePaths(path.dirname(file));mod._compile(js,file);
 return mod.exports;
};
const metadata=typescriptModule('src/compositionMetadata.ts');
const names=[
 'rgb-split','speed-trails','film-light-leak','glass-shatter',
 'liquid-displacement','pixel-dissolve','whip-pan-blur','svg-path-morph',
 'comic-halftone','shader-portal','film-burn-reveal','audio-reactive-particles',
];
const advanced=src('src/fx/advanced/AdvancedEffects.tsx');

test('all twelve new effects are unique, alongside the 21 original validated IDs',()=>{
 assert.equal(names.length,12);
 assert.equal(new Set(names).size,12);
 assert.equal(metadata.EDIT_EFFECT_IDS.length,21);
 assert.equal(metadata.ADVANCED_EFFECT_IDS.length,12);
 assert.deepEqual([...metadata.ADVANCED_EFFECT_IDS],names);
 assert.equal(new Set([...metadata.EDIT_EFFECT_IDS,...metadata.ADVANCED_EFFECT_IDS]).size,33);
 for(const id of names) assert.ok(advanced.includes("id:'"+id+"'"),id);
});
test('existing cut-list validator accepts new IDs without changing existing schema',()=>{
 const raw=JSON.parse(src('src/edit/edit.json'));
 const original=JSON.parse(JSON.stringify(raw));
 for(const id of names){
   const spec=JSON.parse(JSON.stringify(raw));
   const effect=spec.segments.find(x=>x.kind==='fx');
   assert.ok(effect,'fixture requires FX segment');
   effect.id=id;
   assert.doesNotThrow(()=>metadata.validateEditSpec(spec),id);
 }
 assert.deepEqual(JSON.parse(src('src/edit/edit.json')),original);
 const bad=JSON.parse(JSON.stringify(raw));
 bad.segments.find(s=>s.kind==='fx').id='invalid-unknown-effect';
 assert.throws(()=>metadata.validateEditSpec(bad),/must identify a registered effect/);
});
test('one FxPreview and one unbranded AdvancedFxShowcase select real effects',()=>{
 const index=src('src/fx/index.tsx');
 const comp=src('src/Root.tsx');
 const showcase=src('src/fx/advanced/AdvancedFxShowcase.tsx');
 assert.match(index,/\?\? FX_ADVANCED\.find/);
 assert.match(comp,/id="AdvancedFxShowcase"/);
 assert.match(showcase,/<effect\.Component from=/);
 assert.doesNotMatch(showcase,/(VIDEO AI EDITOR|title card|<Label|grid|watermark)/i);
 for(const avoid of ['URFAVXBF VIDEO AI EDITOR','bottom-footer','effect-counter','presentation-sidebar'])
    assert.ok(!advanced.includes(avoid));
});
test('procedural effects use frame animation, real matte and typed paths',()=>{
 assert.match(advanced,/useCurrentFrame/);
 assert.match(advanced,/<ARoll from=/);
 assert.match(advanced,/<Cutout from=/);
 assert.match(advanced,/interpolatePath\(t,MORPH_A,MORPH_B\)/);
 assert.match(advanced,/evolvePath\(/);
 assert.match(advanced,/<feDisplacementMap/);
 assert.match(advanced,/transform:.*translate/);
 assert.match(advanced,/from\+24/);
 assert.match(advanced,/FX_ADVANCED:FxEntry\[\]/);
 assert.match(advanced,/useSrcFrame\(from\)/);
 assert.match(advanced,/backgroundPosition:/);
 assert.match(advanced,/points=Array\.from\(\{length:56/);
});
test('original measured audio envelope is finite and actually varies',()=>{
 const levels=JSON.parse(src('src/fx/advanced/reactive-envelope.json'));
 assert.equal(levels.length,120);
 assert.ok(levels.every(v=>Number.isFinite(v)&&v>=0&&v<=1));
 assert.ok(Math.max(...levels)-Math.min(...levels)>.07);
 const py=src('scripts/generate_advanced_fx_audio.py');
 assert.match(py,/math\.sqrt\(acc/);
 assert.match(py,/wave\.open/);
});
test('no premature import of newer official shaders or cloud assets',()=>{
 for(const forbidden of ['@remotion/effects/shatter','@remotion/effects/film-burn',
                           'gl-transitions/','https://','fetch('])
   assert.ok(!advanced.includes(forbidden),forbidden);
 const pkg=JSON.parse(src('package.json'));
 assert.equal(pkg.dependencies['@remotion/paths'],'4.0.522');
 assert.equal(pkg.dependencies.remotion,'4.0.522');
});
