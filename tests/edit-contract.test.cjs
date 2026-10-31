const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const {test} = require('node:test');
const ts = require('typescript');
const filename = path.resolve(__dirname, '../src/compositionMetadata.ts');
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = Module._nodeModulePaths(path.dirname(filename));
loaded._compile(ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022},
}).outputText, filename);
const {editDuration} = loaded.exports;
const original = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../src/edit/edit.json')));
const copy = () => structuredClone(original);
test('committed edit remains compatible', () => assert.equal(editDuration(copy()), 299));
test('all 21 registered effects are accepted and unknown or missing effects fail closed', () => {
  const ids = fs.readdirSync(path.resolve(__dirname, '../src/fx')).flatMap(file =>
    file.endsWith('.tsx') ? [...fs.readFileSync(path.resolve(__dirname, '../src/fx', file), 'utf8')
      .matchAll(/FxEntry\s*=\s*\{\s*id:\s*'([^']+)'/g)].map(m => m[1]) : []);
  assert.equal(ids.length, 21);
  for (const id of ids) {
    const m = copy(); m.segments = [{kind:'fx',id,at:0,frames:10}];
    assert.equal(editDuration(m), 10);
  }
  for (const id of ['no-effect', '', undefined, '__proto__']) {
    const m=copy(); m.segments[1].id=id;
    assert.throws(() => editDuration(m), /segments\[1\].id/);
  }
});
test('rejects unsafe video and derivative media paths before rendering', () => {
  for (const field of ['video', 'matte', 'sticker']) {
    for (const value of ['', '../secret', '/tmp/media', 'https://evil.test/clip.mp4',
      '//evil.test/a', 'sample/../x', 'sample/%2e%2e/x', 'sample\\x', 'sample//x', 'sample/./x', 'sample/a?token=x']) {
      const m=copy(); m.source[field]=value;
      assert.throws(() => editDuration(m), new RegExp(`source.${field}`));
    }
  }
  const m=copy(); m.source.video='sample/script.html';
  assert.throws(() => editDuration(m), /source.video/);
});
test('rejects invalid source, geometry and source overruns', () => {
  for (const frames of [0, -1, NaN, Infinity, '300', 108001]) {
    const m=copy(); m.source.frames=frames;
    assert.throws(() => editDuration(m), /source.frames/);
  }
  const m=copy(); m.segments=[{kind:'aroll',at:299,frames:2}];
  assert.throws(() => editDuration(m), /source bounds/);
  const g=copy(); g.source.face.x=NaN;
  assert.throws(() => editDuration(g), /source.face.x/);
});
test('rejects audio paths, gains, trims, unknown fields and excessive cut counts', () => {
  for (const value of [NaN, Infinity, -0.1, 2.1, '1', null]) {
    for (const kind of ['music','narration']) {
      const m=copy(); m[kind]={file:'audio/clip.wav',volume:value};
      assert.throws(() => editDuration(m), new RegExp(`${kind}.volume`));
    }
    const m=copy(); m.sourceVolume=value;
    assert.throws(() => editDuration(m), /sourceVolume/);
  }
  for (const trimBefore of [-1, 0.5, NaN, Infinity, 108001]) {
    const m=copy(); m.music={file:'audio/clip.wav',volume:0.4,trimBefore};
    assert.throws(() => editDuration(m), /music.trimBefore/);
  }
  const m=copy(); m.narration={file:'file:///etc/passwd'};
  assert.throws(() => editDuration(m), /narration.file/);
  const u=copy(); u.source.url='https://evil.test';
  assert.throws(() => editDuration(u), /source.*unsupported/);
  const big=copy(); big.segments=Array.from({length:3001},()=>({kind:'aroll',at:0,frames:1}));
  assert.throws(() => editDuration(big), /segments/);
});
test('unknown property names cannot leak URL credentials through validation errors', () => {
  const m=copy(); m.source['https://invalid.test/?token=private-value']='x';
  assert.throws(() => editDuration(m), error => !error.message.includes('private-value') && /unsupported/.test(error.message));
});
