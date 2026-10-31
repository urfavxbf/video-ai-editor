const assert = require('node:assert/strict');
const {test} = require('node:test');
const {readFileSync,existsSync} = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const ts = require('typescript');
const root = path.resolve(__dirname,'..');
const html = readFileSync(path.join(root,'hyperframes/projects/kinetic-intro/index.html'),'utf8');
const pkg = JSON.parse(readFileSync(path.join(root,'package.json'),'utf8'));
const source = path.join(root,'src/hyperframes/validateHyperFramesGraphics.ts');
const translated = ts.transpileModule(readFileSync(source,'utf8'),{
  compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022},
}).outputText;
const loaded=new Module(source,module);
loaded.filename=source;
loaded.paths=Module._nodeModulePaths(path.dirname(source));
loaded._compile(translated,source);
const {validateHyperFramesGraphics:validate}=loaded.exports;
const chapters=[{id:'opening',durationFrames:70},{id:'next',durationFrames:80}];
const validClip={file:'hyperframes/kinetic-intro.mp4',startFrame:8,durationFrames:50};

test('first-class HyperFrames package is pinned and has real render/staging commands',()=>{
  assert.equal(pkg.devDependencies.hyperframes,'0.8.222');
  assert.match(pkg.scripts['hyperframes:render'],/render-hyperframes/);
  assert.match(pkg.scripts['hyperframes:lint'],/hyperframes lint/);
  assert.ok(existsSync(path.join(root,'scripts/render-hyperframes.mjs')));
});
test('original 1920x1080 composition has seekable timeline and no remote media',()=>{
  for(const v of ['data-composition-id="main"','data-width="1920"',
                  'data-height="1080"','data-fps="30"','data-duration="2"',
                  'gsap.timeline({paused:true})','window.__timelines["main"]']) {
    assert.ok(html.includes(v),v);
  }
  assert.equal(/https?:\/\//i.test(html),false);
});
test('valid clips can be scheduled inside approved episode chapters',()=>{
  const out=validate({opening:[validClip]},chapters);
  assert.deepEqual(out.opening,[{...validClip,layout:'inset'}]);
  assert.deepEqual(validate(undefined,chapters),{});
});
test('invalid or unsafe media, clip intervals and chapter IDs fail closed',()=>{
  const invalid=[
    {opening:[{...validClip,file:'https://example.com/a.mp4'}]},
    {opening:[{...validClip,file:'hyperframes/../secrets.mp4'}]},
    {opening:[{...validClip,file:'hyperframes/a.webm'}]},
    {opening:[{...validClip,startFrame:-1}]},
    {opening:[{...validClip,durationFrames:100}]},
    {opening:[{...validClip,layout:'surprise'}]},
    {missing:[validClip]},
    {opening:[{...validClip,unexpected:true}]},
  ];
  for(const value of invalid) assert.throws(()=>validate(value,chapters));
});
test('EpisodeProduction explicitly accepts verified HyperFrames graphics',()=>{
  const text=readFileSync(path.join(root,'src/episodes/EpisodeProduction.tsx'),'utf8');
  assert.match(text,/motionGraphics\?: HyperFramesGraphics/);
  assert.match(text,/validateHyperFramesGraphics\(props\.motionGraphics/);
  assert.match(text,/HyperFramesGraphicLayer key/);
});
