const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const {test} = require('node:test');
const ts = require('typescript');

const filename = path.resolve(__dirname, '../src/episodes/episodeManifest.ts');
const compiled = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022},
}).outputText;
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = Module._nodeModulePaths(path.dirname(filename));
loaded._compile(compiled, filename);
const {compileEpisodeTimeline, validateEpisodeManifest, EPISODE_V1_MAX_FRAMES} = loaded.exports;
const original = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../src/episodes/episode-proof-v1.json')));
const copy = () => structuredClone(original);
const failure = (manifest, pattern) => assert.throws(() => validateEpisodeManifest(manifest), pattern);

test('model-free v1 fixture is valid and compiled deterministically', () => {
  assert.deepEqual(compileEpisodeTimeline(original), compileEpisodeTimeline(copy()));
  const result = compileEpisodeTimeline(original);
  assert.equal(result.chapters[0].startFrame, 0);
  assert.equal(result.chapters[0].endFrame, result.chapters[1].startFrame);
  assert.equal(result.durationFrames, result.chapters.at(-1).endFrame);
  assert.equal(result.durationFrames, 120);
});
test('rejects invalid manifest header, unknown fields and unsupported output format', () => {
  for (const [key, value, match] of [
    ['schemaVersion', 2, /schemaVersion/], ['language', 'tl', /language/],
    ['episodeId', '../unsafe', /episodeId/], ['unexpected', 'x', /unknown field/],
  ]) {
    const m = copy(); m[key] = value; failure(m, match);
  }
  for (const video of [{...original.video, fps: 24}, {...original.video, width: 1080}]) {
    const m = copy(); m.video = video; failure(m, /manifest.video/);
  }
});
test('rejects missing or empty chapters and duplicate ids', () => {
  for (const chapters of [[], null, {}, undefined]) {
    const m = copy(); m.chapters = chapters; failure(m, /manifest.chapters/);
  }
  const m = copy(); m.chapters[1].id = m.chapters[0].id; failure(m, /chapters\[1\].id/);
});
test('rejects chapter timeline gaps, overlaps, negative frames and overflow', () => {
  for (const startFrame of [1, -1, NaN, Infinity, 1.5]) {
    const m = copy(); m.chapters[0].startFrame = startFrame; failure(m, /chapters\[0\].startFrame/);
  }
  const m = copy(); m.chapters[1].startFrame = 0; failure(m, /chapters\[1\].startFrame/);
  const n = copy(); n.chapters[0].durationFrames = EPISODE_V1_MAX_FRAMES;
  n.chapters[1].startFrame = EPISODE_V1_MAX_FRAMES;
  failure(n, /chapters\[1\].startFrame/);
  const valid = copy(); valid.chapters = [{...valid.chapters[0], durationFrames: EPISODE_V1_MAX_FRAMES}];
  assert.equal(compileEpisodeTimeline(valid).durationFrames, EPISODE_V1_MAX_FRAMES);
});
test('validates voice events: speakers, sorting, bounds, overlaps and real RMS', () => {
  const base = {speaker: 'urfavxbf', startFrame: 0, endFrame: 20, rms: [0.2, 0.8, 0.4, 0.1, 0.3, 0.2, 0.1], samplesPerSecond: 10};
  const m = copy(); m.chapters[0].voiceEvents = [base];
  assert.doesNotThrow(() => validateEpisodeManifest(m));
  for (const [key, value] of [
    ['speaker', 'unknown'], ['startFrame', -1], ['endFrame', 100], ['rms', [1.5]],
    ['samplesPerSecond', 0],
  ]) {
    const bad = copy(); bad.chapters[0].voiceEvents = [{...base, [key]: value}];
    failure(bad, /voiceEvents\[0\]/);
  }
  const same = copy(); same.chapters[0].voiceEvents = [base, {...base, startFrame: 15, endFrame: 30}];
  failure(same, /voiceEvents\[1\].startFrame/);
  const unsorted = copy(); unsorted.chapters[0].voiceEvents = [
    {...base, startFrame: 20, endFrame: 30},
    {...base, speaker: 'pix', startFrame: 0, endFrame: 10},
  ];
  failure(unsorted, /voiceEvents\[1\].startFrame/);
});
test('supplied RMS must cover the event instead of extending the last sample', () => {
  const m = copy();
  m.chapters[0].voiceEvents = [{speaker: 'pix', startFrame: 0, endFrame: 60,
    rms: [0.9], samplesPerSecond: 10}];
  failure(m, /rms.*cover/);
});
test('rejects traversal, URLs, malicious or out-of-bounds audio paths', () => {
  for (const value of ['../secret.wav', '/tmp/source.wav', 'https://x.com/a.wav',
    'sound\\track.wav', 'audio//clip.wav', 'audio/./clip.wav', 'audio/sound.exe']) {
    const m = copy();
    m.chapters[0].audio = [{file: value, startFrame: 0, endFrame: 10}];
    failure(m, /audio\[0\].file/);
  }
  const a = copy(); a.chapters[0].audio = [{file: 'audio/valid.wav', startFrame: 0, endFrame: 100}];
  failure(a, /audio\[0\].endFrame/);
  const okay = copy();
  okay.chapters[0].audio = [{file: 'audio/chapter1.wav', startFrame: 0, endFrame: 10}];
  assert.doesNotThrow(() => validateEpisodeManifest(okay));
});
test('caption metadata is validated but deliberately not synthesized', () => {
  const m = copy();
  m.chapters[0].captions = {file: 'captions/first.srt', source: 'human-reviewed'};
  assert.doesNotThrow(() => validateEpisodeManifest(m));
  m.chapters[0].captions.file = 'https://example.com/captions.srt';
  failure(m, /captions.file/);
});
