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
  // Quote-first hook: a universal lesson, not celebrity gossip.
  // Source wording/order is based on the cited episode transcript, while
  // durations remain visual storyboard estimates until real source alignment.
  moment(0, 5, 'speaker', 'The thing about betrayal',
    'THE MOMENT THAT CHANGES YOU', undefined, ['betrayal']),
  moment(5, 12, 'type', "You don't trust yourself anymore.",
    'THE LINE THAT STAYS WITH YOU', 'underline', ['trust', 'yourself']),
  moment(12, 17, 'speaker', 'This is about me.',
    'TURNING INWARD', undefined, ['me']),
  moment(17, 22, 'type', 'No, I come first.',
    'SELF RESPECT', 'circle', ['first']),
  moment(22, 27, 'speaker', "The love isn't enough.",
    'THE HARD REALIZATION', undefined, ['enough']),
];

export const beckyGEditorialProps = {
  beats: BECKY_G_BEATS,
  totalSeconds: BECKY_G_SECONDS,
  sourceLabel: 'CALL HER DADDY · APR 2026',
  seriesLabel: 'RELATIONSHIPS / REAL TALK',
  approximateTiming: true,
} satisfies EditorialKineticProps;
