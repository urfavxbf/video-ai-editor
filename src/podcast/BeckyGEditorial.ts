import type {EditorialBeat, EditorialKineticProps} from './EditorialKinetic';

/**
 * Quote-first editing brief based on the guest's actual spoken words.
 *
 * These are SELECTED WORDS / kinetic display cues, not a complete transcript.
 * The spacing is a DRAFT for a silent typography preview only.
 * Attach cleared source material, align to speech, and review the full context
 * before publishing. See docs/BECKY_G_EDITORIAL.md.
 */

const timed = (words: string, duration: number, strong: string[] = []) => {
  const tokens = words.split(' ');
  const step = (duration - 0.5) / Math.max(1, tokens.length);
  return tokens.map((text, index) => ({
    text,
    at: Math.round((0.12 + index * step) * 1000) / 1000,
    strong: strong.includes(text.toLowerCase().replace(/[^a-z]/g, '')),
  }));
};

const moment = (
  start: number,
  end: number,
  mode: EditorialBeat['mode'],
  words: string,
  kicker?: string,
  mark?: EditorialBeat['mark'],
  strong: string[] = [],
): EditorialBeat => ({
  start,
  end,
  mode,
  tokens: timed(words, end - start, strong),
  kicker,
  mark,
});

export const BECKY_G_SECONDS = 27;

// These phrases appear in the April 1, 2026 Call Her Daddy episode around
// transcript chapter 42:19–43:33; the source video sync is UNVERIFIED.
export const BECKY_G_BEATS: EditorialBeat[] = [
  moment(0, 5, 'speaker', 'I called off my engagement.',
    'WHAT SHE SAID', undefined, ['engagement']),
  moment(5, 10, 'type', 'I took off my ring.',
    'HER DECISION', 'circle', ['ring']),
  moment(10, 15, 'speaker', 'The thing about betrayal',
    'THE HARD TRUTH', undefined, ['betrayal']),
  moment(15, 22, 'type', "You don't trust yourself anymore.",
    'THE LINE THAT HITS', 'underline', ['trust', 'yourself']),
  moment(22, 27, 'speaker', 'No, I come first.',
    'CHOOSING HERSELF', undefined, ['first']),
];

export const beckyGEditorialProps = {
  beats: BECKY_G_BEATS,
  totalSeconds: BECKY_G_SECONDS,
  sourceLabel: 'CALL HER DADDY · APR 2026',
  seriesLabel: 'RELATIONSHIPS / REAL TALK',
  approximateTiming: true,
} satisfies EditorialKineticProps;
