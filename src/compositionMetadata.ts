import type {CalculateMetadataFunction} from 'remotion';
import type {HeroStageProps} from './characters/HeroCharacterStage';
import type {EditSpec} from './edit/Edit';

export const HERO_STAGE_DURATION = 540;
// Both compositions run at 30 fps: reject timelines over one hour, never truncate.
export const MAX_COMPOSITION_DURATION_FRAMES = 30 * 60 * 60;
// Pure catalog shared with the runtime registry; no React/media imports in validation.
export const EDIT_EFFECT_IDS = [
  'orbit', 'chat-takeover', 'frame-escape', 'snap-zoom', 'checklist-pop',
  'headline-storm', 'zoom-portal', 'growth-curve', 'broll-overlay', 'paper-cutout',
  'magazine-cover', 'liquid-glass', 'zoom-through-cut', 'green-screen', 'frame-break',
  'digital-zoom', 'phone-mockup', 'checklist-tally', 'glass-widgets', 'checklist', 'split',
] as const;

function record(value: unknown, field: string): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error(`${field} must be an object`);
  }
  return value as Record<string, unknown>;
}
function fields(value: Record<string, unknown>, allowed: string[], field: string) {
  for (const key of Object.keys(value)) {
    if (!allowed.includes(key)) throw new Error(`${field} contains an unsupported field`);
  }
}
function number(value: unknown, field: string, min: number, max: number, whole = false): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < min || value > max ||
      (whole && !Number.isSafeInteger(value))) {
    throw new Error(`${field} must be ${whole ? 'an integer' : 'finite'} between ${min} and ${max}`);
  }
  return value;
}
function assetPath(value: unknown, field: string, extension?: RegExp) {
  if (typeof value !== 'string' || value.length > 240 ||
      !/^[a-zA-Z0-9][a-zA-Z0-9_./-]*$/.test(value) ||
      value.split('/').some(part => !part || part.startsWith('.')) ||
      (extension && !extension.test(value))) {
    throw new Error(`${field} must be a safe public-relative local media path`);
  }
}

/** Runtime boundary for both metadata and frames, independent of TypeScript casts. */
export function validateEditSpec(input: unknown): EditSpec {
  const field = 'ExampleEdit.spec';
  const spec = record(input, field);
  fields(spec, ['source','segments','music','narration','sourceVolume'], field);
  // Validate the cut-list first to preserve useful historical duration errors.
  if (!Array.isArray(spec.segments) || !spec.segments.length || spec.segments.length > 3000) {
    throw new Error(`${field}.segments must contain 1 to 3000 segments`);
  }
  let total = 0;
  for (const [i, value] of spec.segments.entries()) {
    const p = `${field}.segments[${i}]`;
    const s = record(value, p);
    fields(s, ['kind','at','frames','id'], p);
    if (s.kind !== 'aroll' && s.kind !== 'fx') throw new Error(`${p}.kind must be aroll or fx`);
    number(s.at, `${p}.at`, 0, MAX_COMPOSITION_DURATION_FRAMES, true);
    total += duration(s.frames, `${p}.frames`);
    duration(total, 'ExampleEdit duration');
    if (s.kind === 'fx' && !EDIT_EFFECT_IDS.includes(s.id as typeof EDIT_EFFECT_IDS[number])) {
      throw new Error(`${p}.id must identify a registered effect`);
    }
    if (s.kind === 'aroll' && s.id !== undefined) throw new Error(`${p}.id is only valid for fx`);
  }
  const source = record(spec.source, `${field}.source`);
  fields(source, ['video','matte','sticker','frames','face','continuous'], `${field}.source`);
  for (const key of ['video','matte','sticker']) {
    assetPath(source[key], `${field}.source.${key}`, key === 'video' ? /\.(mp4|webm|mov)$/i : undefined);
  }
  const frames = duration(source.frames, `${field}.source.frames`);
  for (const [i, s] of spec.segments.entries()) {
    if (s.at + s.frames > frames) throw new Error(`${field}.segments[${i}] exceeds source bounds`);
  }
  if (source.continuous !== undefined && typeof source.continuous !== 'boolean') {
    throw new Error(`${field}.source.continuous must be boolean`);
  }
  if (source.face !== undefined) {
    const face = record(source.face, `${field}.source.face`);
    fields(face, ['x','y','mouthY'], `${field}.source.face`);
    number(face.x, `${field}.source.face.x`, 0, 1080);
    number(face.y, `${field}.source.face.y`, 0, 1920);
    number(face.mouthY, `${field}.source.face.mouthY`, 0, 1920);
  }
  if (spec.sourceVolume !== undefined) number(spec.sourceVolume, `${field}.sourceVolume`, 0, 2);
  for (const kind of ['music','narration']) {
    if (spec[kind] === undefined) continue;
    const p = `${field}.${kind}`;
    const audio = record(spec[kind], p);
    fields(audio, kind === 'music' ? ['file','volume','trimBefore'] : ['file','volume'], p);
    assetPath(audio.file, `${p}.file`, /\.(wav|mp3|m4a|aac|ogg)$/i);
    if (kind === 'music' || audio.volume !== undefined) number(audio.volume, `${p}.volume`, 0, 2);
    if (audio.trimBefore !== undefined) number(audio.trimBefore, `${p}.trimBefore`, 0, MAX_COMPOSITION_DURATION_FRAMES, true);
  }
  return input as EditSpec;
}

const duration = (value: unknown, field: string): number => {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) ||
      value < 1 || value > MAX_COMPOSITION_DURATION_FRAMES) {
    throw new Error(`${field} must be an integer between 1 and ${MAX_COMPOSITION_DURATION_FRAMES} frames`);
  }
  return value;
};

export const calculateHeroMetadata: CalculateMetadataFunction<HeroStageProps> = ({props}) => ({
  durationInFrames: props.durationFrames === undefined ? HERO_STAGE_DURATION
    : duration(props.durationFrames, 'HeroCharacterStage.durationFrames'),
});

/** Cut-list segments play consecutively. Source offsets do not extend the output timeline. */
export const editDuration = (spec: EditSpec): number => {
  return validateEditSpec(spec).segments.reduce((sum, segment) => sum + segment.frames, 0);
};

export const calculateEditMetadata: CalculateMetadataFunction<{spec: EditSpec}> = ({props}) => ({
  durationInFrames: editDuration(props.spec),
});
