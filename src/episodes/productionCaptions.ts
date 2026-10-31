export type ProductionCaption = {startFrame: number; endFrame: number; text: string};
export type ProductionCaptions = Record<string, ProductionCaption[]>;

/** Captions are supplied timing data. This contract never synthesizes alignment. */
export function validateProductionCaptions(input: unknown, chapters: {id: string; durationFrames: number}[]): ProductionCaptions {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('Invalid production captions');
  for (const [id, value] of Object.entries(input)) {
    const chapter = chapters.find(c => c.id === id);
    if (!chapter || !Array.isArray(value) || value.length > 3000) throw new Error('Unknown or oversized caption chapter');
    let end = 0;
    for (const cue of value) {
      if (!cue || typeof cue !== 'object' || Array.isArray(cue) ||
        Object.keys(cue).some(key => !['startFrame','endFrame','text'].includes(key)) ||
        !Number.isSafeInteger(cue.startFrame) || !Number.isSafeInteger(cue.endFrame) ||
        cue.startFrame < end || cue.endFrame <= cue.startFrame || cue.endFrame > chapter.durationFrames ||
        typeof cue.text !== 'string' || !cue.text.trim() || cue.text.length > 60 || /[\x00-\x1f]/.test(cue.text)) {
        throw new Error('Invalid, overlapping or unreadable production caption');
      }
      end = cue.endFrame;
    }
  }
  return input as ProductionCaptions;
}
