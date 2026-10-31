const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const {test} = require('node:test');
const ts = require('typescript');

// Compile the actual pure TypeScript module with the existing compiler; no new runner dependency.
const filename = path.resolve(__dirname, '../src/compositionMetadata.ts');
const compiled = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022},
}).outputText;
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = Module._nodeModulePaths(path.dirname(filename));
loaded._compile(compiled, filename);
const {HERO_STAGE_DURATION, MAX_COMPOSITION_DURATION_FRAMES, calculateHeroMetadata,
  calculateEditMetadata, editDuration} = loaded.exports;
const edit = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../src/edit/edit.json'), 'utf8'));
const metadata = (fn, props) => fn({props, defaultProps: props, abortSignal: new AbortController().signal,
  compositionId: 'test', isRendering: true});
const spec = (segments) => ({...edit, source: {...edit.source, frames: 108000}, segments});

test('Hero retains the 540-frame default when no duration override is supplied', async () => {
  assert.equal(HERO_STAGE_DURATION, 540);
  assert.deepEqual(await metadata(calculateHeroMetadata, {}), {durationInFrames: 540});
  assert.deepEqual(await metadata(calculateHeroMetadata, {durationFrames: undefined}), {durationInFrames: 540});
});

test('Hero uses actual duration props, including the valid boundaries', async () => {
  for (const frames of [1, 900, MAX_COMPOSITION_DURATION_FRAMES]) {
    assert.deepEqual(await metadata(calculateHeroMetadata, {durationFrames: frames}), {durationInFrames: frames});
  }
});

const invalidFrames = [null, '', '900', false, [], {}, 0, -1, NaN, Infinity, -Infinity,
  1.5, Number.MAX_SAFE_INTEGER + 1, 108001];
test('Hero rejects invalid, non-finite, fractional and excessive overrides', async () => {
  for (const durationFrames of invalidFrames) {
    await assert.rejects(async () => metadata(calculateHeroMetadata, {durationFrames}),
      /HeroCharacterStage\.durationFrames.*integer.*108000/);
  }
});

test('ExampleEdit keeps the duration of the checked-in default cut list', async () => {
  assert.equal(editDuration(edit), 299);
  assert.deepEqual(await metadata(calculateEditMetadata, {spec: edit}), {durationInFrames: 299});
});

test('ExampleEdit uses supplied segments, not source offsets or the checked-in cut list', async () => {
  for (const segments of [
    [{kind: 'aroll', at: 0, frames: 10}],
    [{kind: 'aroll', at: 100, frames: 3}, {kind: 'aroll', at: 100, frames: 7}],
    [{kind: 'fx', id: 'orbit', at: 20, frames: 6}, {kind: 'aroll', at: 0, frames: 4}],
  ]) {
    assert.equal(editDuration(spec(segments)), 10);
    assert.deepEqual(await metadata(calculateEditMetadata, {spec: spec(segments)}), {durationInFrames: 10});
  }
});

test('ExampleEdit accepts exactly the cap and rejects an excessive cumulative timeline', () => {
  assert.equal(editDuration(spec([{kind: 'aroll', at: 0, frames: 108000}])), 108000);
  assert.throws(() => editDuration(spec([
    {kind: 'aroll', at: 0, frames: 108000}, {kind: 'aroll', at: 0, frames: 1},
  ])), /ExampleEdit.*108000/);
});

test('ExampleEdit rejects absent, malformed and empty cut lists', async () => {
  for (const value of [undefined, null, [], {}, {segments: null}, {segments: {}}, {segments: []}]) {
    await assert.rejects(async () => metadata(calculateEditMetadata, {spec: value}), /ExampleEdit\.spec/);
  }
});

test('ExampleEdit rejects malformed segments and invalid duration values', () => {
  for (const frames of [...invalidFrames, undefined]) {
    assert.throws(() => editDuration(spec([{kind: 'aroll', at: 0, frames}])),
      /ExampleEdit\.spec\.segments\[0\]\.frames/);
  }
  for (const segment of [null, [], 'aroll', {kind: 'unknown', at: 0, frames: 10}]) {
    assert.throws(() => editDuration(spec([segment])), /ExampleEdit\.spec\.segments\[0\]/);
  }
});

test('ExampleEdit requires non-negative safe integer source offsets', () => {
  for (const at of [undefined, null, '', '0', NaN, Infinity, -1, 0.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => editDuration(spec([{kind: 'aroll', at, frames: 10}])),
      /ExampleEdit\.spec\.segments\[0\]\.at/);
  }
});
