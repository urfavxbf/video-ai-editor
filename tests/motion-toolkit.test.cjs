const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const {test} = require('node:test');
const ts = require('typescript');

const filename = path.resolve(__dirname, '../src/motion/motionMath.ts');
const compiled = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022},
}).outputText;
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = Module._nodeModulePaths(path.dirname(filename));
loaded._compile(compiled, filename);
const {MOTION_PRESETS, resolveMotionState} = loaded.exports;

const state = (preset, frame, overrides = {}) => resolveMotionState(frame, {...preset, ...overrides});

test('all six original presets define usable timing, typography and color', () => {
  assert.equal(Object.keys(MOTION_PRESETS).length, 6);
  for (const preset of Object.values(MOTION_PRESETS)) {
    assert.ok(Number.isSafeInteger(preset.durationInFrames) && preset.durationInFrames > 0);
    assert.ok(preset.fontFamily.length > 0);
    assert.ok(preset.color.startsWith('#'));
    assert.ok(preset.accentColor.startsWith('#'));
  }
});

test('fade, slide and scale have deterministic clamped start and end frames', () => {
  const fade = MOTION_PRESETS.signalFade;
  assert.equal(state(fade, 0).opacity, 0);
  assert.equal(state(fade, fade.durationInFrames).opacity, 1);
  assert.equal(state(fade, fade.durationInFrames + 100).opacity, 1);

  const slide = MOTION_PRESETS.cleanSlide;
  assert.equal(state(slide, 0).translateX, -slide.distance);
  assert.equal(state(slide, slide.durationInFrames).translateX, 0);

  const scale = MOTION_PRESETS.softScale;
  assert.equal(state(scale, 0).scale, scale.fromScale);
  assert.equal(state(scale, scale.durationInFrames).scale, 1);
});

test('bounce overshoots, masked reveal clips, and stagger timing is offset by its caller', () => {
  const bounce = MOTION_PRESETS.impactBounce;
  assert.ok(state(bounce, 8).scale > 1);
  assert.equal(state(bounce, bounce.durationInFrames).scale, 1);

  const mask = MOTION_PRESETS.windowReveal;
  assert.equal(state(mask, 0).clipInsetRight, 100);
  assert.equal(state(mask, mask.durationInFrames).clipInsetRight, 0);

  const stagger = MOTION_PRESETS.wordCascade;
  const firstCharacter = state(stagger, 24, {variant: stagger.staggerVariant, fromFrame: 4});
  const secondCharacter = state(stagger, 24, {variant: stagger.staggerVariant, fromFrame: 8});
  assert.equal(firstCharacter.opacity, 1);
  assert.ok(secondCharacter.opacity > 0 && secondCharacter.opacity < firstCharacter.opacity);
});

test('exit motions and reduced-motion behavior are frame deterministic', () => {
  const preset = MOTION_PRESETS.cleanSlide;
  const options = {...preset, exitAtFrame: 40, exitDurationInFrames: 10, exitVariant: 'fade'};
  assert.equal(resolveMotionState(40, options).opacity, 1);
  assert.equal(resolveMotionState(50, options).opacity, 0);
  assert.deepEqual(resolveMotionState(8, options), resolveMotionState(8, options));
  assert.deepEqual(resolveMotionState(0, {...preset, reducedMotion: true}), {
    opacity: 1, translateX: 0, translateY: 0, scale: 1, clipInsetRight: 0,
  });
  assert.equal(resolveMotionState(0, {...preset, fromFrame: 10, reducedMotion: true}).opacity, 0);
  assert.equal(resolveMotionState(10, {...preset, fromFrame: 10, reducedMotion: true}).opacity, 1);
});

test('invalid durations, offsets and non-finite frames are rejected', () => {
  const preset = MOTION_PRESETS.signalFade;
  for (const durationInFrames of [0, -1, 1.5, Infinity, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => state(preset, 0, {durationInFrames}), /durationInFrames must be a positive safe integer/);
  }
  assert.throws(() => state(preset, 0, {exitAtFrame: 10, exitDurationInFrames: 0}), /exitDurationInFrames/);
  assert.throws(() => state(preset, 0, {fromFrame: -1}), /fromFrame/);
  assert.throws(() => resolveMotionState(NaN, preset), /frame/);
});