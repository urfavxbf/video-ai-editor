import type {CalculateMetadataFunction} from 'remotion';
import type {HeroStageProps} from './characters/HeroCharacterStage';
import type {EditSpec} from './edit/Edit';

export const HERO_STAGE_DURATION = 540;
// Both compositions run at 30 fps: reject timelines over one hour, never truncate.
export const MAX_COMPOSITION_DURATION_FRAMES = 30 * 60 * 60;

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
  if (!spec || typeof spec !== 'object' || Array.isArray(spec)) {
    throw new Error('ExampleEdit.spec must be an edit specification');
  }
  if (!Array.isArray(spec.segments) || spec.segments.length === 0) {
    throw new Error('ExampleEdit.spec.segments must be a non-empty cut list');
  }
  let total = 0;
  for (const [index, segment] of spec.segments.entries()) {
    const field = `ExampleEdit.spec.segments[${index}]`;
    if (!segment || typeof segment !== 'object' || Array.isArray(segment) ||
        (segment.kind !== 'aroll' && segment.kind !== 'fx')) {
      throw new Error(`${field} must be an aroll or fx segment`);
    }
    if (!Number.isSafeInteger(segment.at) || segment.at < 0) {
      throw new Error(`${field}.at must be a non-negative safe integer source frame`);
    }
    total += duration(segment.frames, `${field}.frames`);
    duration(total, 'ExampleEdit duration');
  }
  return total;
};

export const calculateEditMetadata: CalculateMetadataFunction<{spec: EditSpec}> = ({props}) => ({
  durationInFrames: editDuration(props.spec),
});
