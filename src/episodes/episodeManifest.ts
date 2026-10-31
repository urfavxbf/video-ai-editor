import type {VoiceEvent} from '../characters/CharacterPuppet';

/**
 * Strict v1 contract for deterministic, model-free episode planning.
 * Frames are chapter-local for audio/voice events; chapter startFrame is global.
 * Nothing in this module generates speech, captions or licensed artwork.
 */
export const EPISODE_V1_MAX_FRAMES = 30 * 60 * 60;
const MAX_CHAPTERS = 120;
const MAX_EVENTS_PER_CHAPTER = 3000;

export type EpisodeAudioV1 = {file: string; startFrame: number; endFrame: number};
export type EpisodeCaptionsV1 = {file: string; source: 'human-reviewed' | 'forced-alignment'};
export type EpisodeChapterV1 = {
  id: string;
  title: string;
  chapterNumber: number;
  startFrame: number;
  durationFrames: number;
  voiceEvents?: VoiceEvent[];
  audio?: EpisodeAudioV1[];
  captions?: EpisodeCaptionsV1;
};
export type EpisodeManifestV1 = {
  schemaVersion: 1;
  episodeId: string;
  language: 'en';
  video: {width: 1920; height: 1080; fps: 30};
  chapters: EpisodeChapterV1[];
};
export type CompiledChapterV1 = EpisodeChapterV1 & {endFrame: number};
export type CompiledEpisodeV1 = {
  manifest: EpisodeManifestV1;
  chapters: CompiledChapterV1[];
  durationFrames: number;
};

const fail = (field: string, message: string): never => {
  throw new Error(`${field}: ${message}`);
};
const object = (value: unknown, path: string): Record<string, unknown> => {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    return fail(path, 'must be an object');
  }
  return value as Record<string, unknown>;
};
const keys = (value: Record<string, unknown>, allowed: readonly string[], path: string): void => {
  for (const key of Object.keys(value)) {
    if (!allowed.includes(key)) fail(`${path}.${key}`, 'unknown field');
  }
};
const integer = (value: unknown, path: string, min: number, max: number): number => {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < min || value > max) {
    return fail(path, `must be a safe integer from ${min} to ${max}`);
  }
  return value;
};
const slug = (value: unknown, path: string): void => {
  if (typeof value !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(value)) {
    fail(path, 'must be a lower-case slug, 1–64 characters');
  }
};
const title = (value: unknown, path: string): void => {
  if (typeof value !== 'string' || value.length < 1 || value.length > 120 || value.trim() !== value) {
    fail(path, 'must be a non-empty, trimmed title of at most 120 characters');
  }
};
const mediaPath = (value: unknown, path: string, extensions: RegExp): void => {
  if (typeof value !== 'string' || value.length > 240 ||
      !/^[a-zA-Z0-9][a-zA-Z0-9_.\/-]*$/.test(value) ||
      value.split('/').some((segment) => segment === '' || segment === '.' || segment === '..' || segment.startsWith('.')) ||
      !extensions.test(value)) {
    fail(path, 'must be a safe public/-relative asset path with supported extension');
  }
};
const range = (item: Record<string, unknown>, path: string, maxFrame: number): void => {
  const start = integer(item.startFrame, `${path}.startFrame`, 0, maxFrame - 1);
  const end = integer(item.endFrame, `${path}.endFrame`, 1, maxFrame);
  if (end <= start) fail(`${path}.endFrame`, 'must be greater than startFrame');
};

export const validateEpisodeManifest = (value: unknown): EpisodeManifestV1 => {
  const root = object(value, 'manifest');
  keys(root, ['schemaVersion', 'episodeId', 'language', 'video', 'chapters'], 'manifest');
  if (root.schemaVersion !== 1) fail('manifest.schemaVersion', 'only version 1 is supported');
  slug(root.episodeId, 'manifest.episodeId');
  if (root.language !== 'en') fail('manifest.language', 'approved v1 production language is en');
  const video = object(root.video, 'manifest.video');
  keys(video, ['width', 'height', 'fps'], 'manifest.video');
  if (video.width !== 1920 || video.height !== 1080 || video.fps !== 30) {
    fail('manifest.video', 'must be 1920x1080 at 30fps');
  }
  if (!Array.isArray(root.chapters) || root.chapters.length < 1 || root.chapters.length > MAX_CHAPTERS) {
    fail('manifest.chapters', `must contain 1–${MAX_CHAPTERS} chapters`);
  }
  const seenIds = new Set<string>();
  let nextStartFrame = 0;
  for (const [index, raw] of root.chapters.entries()) {
    const p = `manifest.chapters[${index}]`;
    const chapter = object(raw, p);
    keys(chapter, ['id', 'title', 'chapterNumber', 'startFrame', 'durationFrames',
      'voiceEvents', 'audio', 'captions'], p);
    slug(chapter.id, `${p}.id`);
    title(chapter.title, `${p}.title`);
    if (seenIds.has(chapter.id as string)) fail(`${p}.id`, 'duplicate chapter identifier');
    seenIds.add(chapter.id as string);
    integer(chapter.chapterNumber, `${p}.chapterNumber`, 1, 999);
    const start = integer(chapter.startFrame, `${p}.startFrame`, 0, EPISODE_V1_MAX_FRAMES - 1);
    if (start !== nextStartFrame) fail(`${p}.startFrame`, `must equal contiguous timeline offset ${nextStartFrame}`);
    const frames = integer(chapter.durationFrames, `${p}.durationFrames`, 1, EPISODE_V1_MAX_FRAMES);
    if (frames > EPISODE_V1_MAX_FRAMES - nextStartFrame) {
      fail(`${p}.durationFrames`, 'total episode exceeds the maximum duration');
    }
    nextStartFrame += frames;

    if (chapter.voiceEvents !== undefined) {
      if (!Array.isArray(chapter.voiceEvents) || chapter.voiceEvents.length > MAX_EVENTS_PER_CHAPTER) {
        fail(`${p}.voiceEvents`, 'must be an array of at most 3000 events');
      }
      const speakerEnd: Record<string, number> = {};
      let previousStart = -1;
      for (const [j, rawEvent] of chapter.voiceEvents.entries()) {
        const path = `${p}.voiceEvents[${j}]`;
        const event = object(rawEvent, path);
        keys(event, ['speaker', 'startFrame', 'endFrame', 'rms', 'samplesPerSecond'], path);
        if (event.speaker !== 'urfavxbf' && event.speaker !== 'pix') {
          fail(`${path}.speaker`, 'must be urfavxbf or pix');
        }
        range(event, path, frames);
        const s = event.startFrame as number;
        if (s < previousStart) fail(`${path}.startFrame`, 'voice events must be sorted by startFrame');
        if (s < (speakerEnd[event.speaker as string] ?? 0)) {
          fail(`${path}.startFrame`, 'same-speaker events must not overlap');
        }
        speakerEnd[event.speaker as string] = event.endFrame as number;
        previousStart = s;
        if (event.samplesPerSecond !== undefined) {
          integer(event.samplesPerSecond, `${path}.samplesPerSecond`, 1, 1000);
        }
        if (event.rms !== undefined) {
          if (!Array.isArray(event.rms) || event.rms.length > 100000) {
            fail(`${path}.rms`, 'must be an array of up to 100000 real audio samples');
          }
          for (const [k, sample] of event.rms.entries()) {
            if (typeof sample !== 'number' || !Number.isFinite(sample) || sample < 0 || sample > 1) {
              fail(`${path}.rms[${k}]`, 'must be finite and between 0 and 1');
            }
          }
        }
      }
    }
    if (chapter.audio !== undefined) {
      if (!Array.isArray(chapter.audio) || chapter.audio.length > MAX_EVENTS_PER_CHAPTER) {
        fail(`${p}.audio`, 'must be an array of at most 3000 clips');
      }
      for (const [j, rawClip] of chapter.audio.entries()) {
        const path = `${p}.audio[${j}]`;
        const clip = object(rawClip, path);
        keys(clip, ['file', 'startFrame', 'endFrame'], path);
        mediaPath(clip.file, `${path}.file`, /\.(wav|mp3)$/i);
        range(clip, path, frames);
      }
    }
    if (chapter.captions !== undefined) {
      const cpath = `${p}.captions`;
      const captions = object(chapter.captions, cpath);
      keys(captions, ['file', 'source'], cpath);
      mediaPath(captions.file, `${cpath}.file`, /\.(srt|json)$/i);
      if (captions.source !== 'human-reviewed' && captions.source !== 'forced-alignment') {
        fail(`${cpath}.source`, 'must be human-reviewed or forced-alignment');
      }
    }
  }
  return value as EpisodeManifestV1;
};

export const compileEpisodeTimeline = (input: unknown): CompiledEpisodeV1 => {
  const manifest = validateEpisodeManifest(input);
  return {
    manifest,
    chapters: manifest.chapters.map((chapter) => ({
      ...chapter,
      endFrame: chapter.startFrame + chapter.durationFrames,
    })),
    durationFrames: manifest.chapters.reduce((total, chapter) => total + chapter.durationFrames, 0),
  };
};
