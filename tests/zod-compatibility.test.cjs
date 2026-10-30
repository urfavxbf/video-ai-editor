// Bounded, model-free checks for the Zod exception documented in docs/ZOD_SECURITY_REVIEW.md.
// These exercise the installed package and Remotion APIs; they do not certify embedded Zod.
const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {test} = require('node:test');
const z = require('zod');

// Private helpers are deliberately tested against the pinned Studio release.
const studioFile = (file) => path.join(path.dirname(require.resolve('@remotion/studio/package.json')), 'dist', file);
const schemaHelpers = require(studioFile('components/RenderModal/SchemaEditor/zod-schema-type.js'));
const {resolveCompositionSchema} = require(studioFile('components/RenderModal/SchemaEditor/infer-zod-schema-from-value.js'));
const {extractEnumJsonPaths} = require(studioFile('components/RenderModal/SchemaEditor/extract-enum-json-paths.js'));
const compositionDrag = require(studioFile('components/composition-drag-data.js'));

for (const kind of ['array', 'set', 'map']) {
  test(`installed Zod rejects oversized ${kind} before traversing elements`, () => {
    let visits = 0;
    const element = z.custom(() => { visits++; return true; });
    const schema = kind === 'array' ? z.array(element).max(2)
      : kind === 'set' ? z.set(element).max(2) : z.map(z.string(), element).max(2);
    const input = kind === 'array' ? [1, 2, 3]
      : kind === 'set' ? new Set([1, 2, 3]) : new Map([['a', 1], ['b', 2], ['c', 3]]);
    assert.equal(schema.safeParse(input).success, false);
    assert.equal(visits, 0);
    const valid = kind === 'array' ? [1] : kind === 'set' ? new Set([1]) : new Map([['a', 1]]);
    assert.equal(schema.safeParse(valid).success, true);
    assert.equal(visits, 1);
  });
}

test('Studio infers and validates the current hero-stage props', () => {
  const defaultProps = {assetsReady: true, artApproved: true, voiceEvents: [], chapter: 1};
  const schema = resolveCompositionSchema({explicitSchema: undefined, defaultProps, z, zodTypes: null});
  assert.equal(schemaHelpers.getZodSchemaType(schema), 'object');
  assert.equal(schemaHelpers.zodSafeParse(schema, {...defaultProps, chapter: 2}).success, true);
  assert.equal(schemaHelpers.zodSafeParse(schema, {...defaultProps, chapter: 'invalid'}).success, false);
});

test('Studio reads nested enum and array schemas for prop serialization', () => {
  const schema = z.object({
    mode: z.enum(['preview', 'final']),
    speakers: z.array(z.enum(['urfavxbf', 'pix'])).max(2),
    chapter: z.number().int().positive().default(1),
  });
  assert.deepEqual(extractEnumJsonPaths({schema, zodRuntime: z, currentPath: [], zodTypes: null}),
    [['mode'], ['speakers', '[]']]);
  assert.equal(schema.safeParse({mode: 'preview', speakers: ['pix']}).success, true);
  assert.equal(schema.safeParse({mode: 'invalid', speakers: ['pix']}).success, false);
});

test('Studio composition drag data round-trips through installed zod/mini', () => {
  const data = compositionDrag.makeCompositionDragData({
    compositionId: 'HeroCharacterStage', compositionFile: 'src/Root.tsx',
    width: 1920, height: 1080, durationInFrames: 540,
  });
  assert.deepEqual(compositionDrag.parseCompositionDragData(data), data.data);
  assert.equal(compositionDrag.parseCompositionDragData({...data, payload: '{invalid'}), null);
  assert.equal(compositionDrag.parseCompositionDragData({...data,
    payload: JSON.stringify({...data.data, compositionFile: '../outside.tsx'})}), null);
});

for (const format of ['CJS', 'ESM']) {
  test(`Studio protocol ${format} accepts valid payloads and rejects malformed or over-limit inputs`, async () => {
    const protocol = format === 'CJS' ? require('@remotion/studio-protocol') : await import(pathToFileURL(
      path.join(path.dirname(require.resolve('@remotion/studio-protocol/package.json')), 'dist/esm/index.mjs')));
    const internals = protocol.StudioProtocolInternals;
    const input = {
      displayName: 'Review card', slug: 'review-card', sourceCode: 'export const ReviewCard = () => null;',
      dependencies: [], dimensions: {width: 1920, height: 1080}, durationInFrames: 30,
    };
    const payload = protocol.createElementPayload(input);
    assert.deepEqual(internals.parseStudioElementPayload(payload), payload);
    const envelope = {operation: 'install-element', protocol: 'remotion-studio-protocol',
      protocolVersion: 1, targetId: 'review-only', payload};
    assert.equal(internals.parseStudioProtocolInstallRequest(envelope).status, 'valid');
    assert.deepEqual(internals.parseStudioProtocolIframeInstallRequest(envelope), payload);
    assert.equal(internals.parseStudioProtocolInstallRequest({...envelope, protocolVersion: 999}).status, 'invalid-request');
    const oversized = {...payload, element: {...payload.element,
      dependencies: Array.from({length: 101}, () => ({name: '@remotion/shapes', version: null}))}};
    assert.equal(internals.parseStudioElementPayload(oversized), null);
    assert.throws(() => protocol.createElementPayload({...input, dependencies: oversized.element.dependencies}));
    // Rejection alone does not prove preflight rejection in the embedded parsers.
  });
}
