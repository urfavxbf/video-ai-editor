/** A first-class, local-only HyperFrames export contract for EpisodeProduction. */
export type HyperFramesGraphic = {
  file: string;
  startFrame: number;
  durationFrames: number;
  layout?: 'inset' | 'fullscreen';
};
export type HyperFramesGraphics = Record<string, HyperFramesGraphic[]>;

const integer = (value: unknown): value is number =>
  typeof value === 'number' && Number.isSafeInteger(value);
const validFile = (file: unknown): file is string =>
  typeof file === 'string' && file.length <= 160 &&
  /^hyperframes\/[a-z0-9][a-z0-9/_-]*\.mp4$/.test(file) &&
  !file.split('/').some(segment => segment === '..' || segment === '.');

export const validateHyperFramesGraphics = (
  value: unknown,
  chapters: {id: string; durationFrames: number}[],
): HyperFramesGraphics => {
  if (value === undefined) return {};
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('motionGraphics must map chapter IDs to local HyperFrames clips');
  }
  const graphics = value as Record<string, unknown>;
  const durations = new Map(chapters.map(chapter => [chapter.id, chapter.durationFrames]));
  const validated: HyperFramesGraphics = {};
  for (const [chapterId, clips] of Object.entries(graphics)) {
    const duration = durations.get(chapterId);
    if (duration === undefined || !Array.isArray(clips) || clips.length > 24) {
      throw new Error('motionGraphics contains unknown chapter or too many clips');
    }
    const checked: HyperFramesGraphic[] = [];
    for (const raw of clips) {
      if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
        throw new Error('motionGraphics clip must be an object');
      }
      const clip = raw as Record<string, unknown>;
      if (Object.keys(clip).some(k => !['file','startFrame','durationFrames','layout'].includes(k))) {
        throw new Error('motionGraphics contains unknown clip property');
      }
      if (!validFile(clip.file)) throw new Error('motionGraphics requires safe public/hyperframes/*.mp4');
      if (!integer(clip.startFrame) || clip.startFrame < 0 ||
          !integer(clip.durationFrames) || clip.durationFrames <= 0 ||
          clip.startFrame + clip.durationFrames > duration) {
        throw new Error('motionGraphics frame range exceeds its chapter');
      }
      if (clip.layout !== undefined && clip.layout !== 'inset' && clip.layout !== 'fullscreen') {
        throw new Error('motionGraphics layout must be inset or fullscreen');
      }
      checked.push({
        file: clip.file,
        startFrame: clip.startFrame,
        durationFrames: clip.durationFrames,
        layout: clip.layout === 'fullscreen' ? 'fullscreen' : 'inset',
      });
    }
    validated[chapterId] = checked;
  }
  return validated;
};
