import type {EditorialBeat, EditorialKineticProps} from './EditorialKinetic';

/**
 * An ORIGINAL narration storyboard, not a transcript of the podcast.
 *
 * Draft word positions are proportional estimates. Retiming to a recorded
 * narration track with a forced aligner is required before final delivery.
 */
const paced = (sentence: string, duration: number, strong: string[] = []) => {
  const words = sentence.split(' ');
  const interval = (duration - 0.45) / Math.max(1, words.length);
  return words.map((text, index) => ({
    text,
    at: Number((index * interval + 0.08).toFixed(3)),
    strong: strong.includes(text.replace(/[,.?!]/g, '').toLowerCase()),
  }));
};

const beat = (
  start: number,
  end: number,
  mode: EditorialBeat['mode'],
  words: string,
  kicker?: string,
  mark?: EditorialBeat['mark'],
  emphasis: string[] = [],
): EditorialBeat => ({
  start,
  end,
  mode,
  tokens: paced(words, end - start, emphasis),
  kicker,
  mark,
});

export const BECKY_G_SECONDS = 43;
export const BECKY_G_BEATS: EditorialBeat[] = [
  beat(0, 5, 'speaker',
    'Becky G finally explained what happened after those public cheating allegations.',
    'WHAT REALLY HAPPENED', undefined, ['cheating']),
  beat(5, 10, 'type',
    'Most people only saw the headlines. They missed her decision.',
    'THE PUBLIC STORY', 'strike', ['missed']),
  beat(10, 16, 'speaker',
    'She revealed that she actually called off the engagement entirely.',
    'THE REVELATION', undefined, ['off']),
  beat(16, 21, 'type',
    'And yes, she even took off her ring.',
    'WHAT SHE DID', 'circle', ['ring']),
  beat(21, 28, 'speaker',
    "But the deepest pain wasn't just losing trust in someone else.",
    'THE EMOTIONAL COST', undefined, ['trust']),
  beat(28, 34, 'type',
    'She said betrayal also made her question her own judgment.',
    'AFTER THE BETRAYAL', 'underline', ['betrayal', 'judgment']),
  beat(34, 39, 'speaker',
    'The couple later chose to keep working on their relationship.',
    'THE NUANCE', undefined, ['working']),
  beat(39, 43, 'type',
    'So would you ever stay?',
    'YOUR OPINION', 'circle', ['stay']),
];

export const beckyGEditorialProps = {
  beats: BECKY_G_BEATS,
  totalSeconds: BECKY_G_SECONDS,
  sourceLabel: 'CALL HER DADDY · APR 2026',
  seriesLabel: 'HOLLYWOOD / EXPLAINED',
  approximateTiming: true,
} satisfies EditorialKineticProps;
