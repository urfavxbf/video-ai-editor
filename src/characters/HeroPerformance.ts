import {type BodyGesture, type CharacterId, type CharacterReaction, type ReactionCue, type VoiceEvent} from './CharacterPuppet';

/**
 * Character-first continuity system for every UrFavXBF + PIX episode.
 * Artwork is approved Super Pixel/Glitch V2; do not replace its identities.
 * Dialogue envelopes originate from actual WAVs, never a script-length guess.
 */
export const HERO_IDENTITY = {
  urfavxbf: {
    name: 'UrFavXBF',
    role: 'host',
    accent: '#ffda00',
    glow: 'rgba(255,218,0,0.18)',
    assetPath: 'characters/pixel-glitch/urfavxbf/base.png',
    sha256: 'b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4',
    voiceProfile: 'natural-storyteller-v1',
    notes: 'Controlled, clear, warm, subtly witty. Stable posture and deliberate explanation gestures.',
  },
  pix: {
    name: 'PIX',
    role: 'AI companion',
    accent: '#27e8fd',
    glow: 'rgba(39,232,253,0.2)',
    assetPath: 'characters/pixel-glitch/pix/base.png',
    sha256: 'cc5ecccdbb74b8c90ea3af09a0c75ff2c72db05fcdf0006fdc19255641304c6f',
    voiceProfile: 'pix-cute-female-emily-v1',
    notes: 'Curious, bright, expressive and playful; punctuated bounces and quick reactions.',
  },
} as const;

export type HeroAction = BodyGesture;
export type HeroDirection = {
  gesture: HeroAction;
  listenerReaction?: CharacterReaction;
  isSpeaking: boolean;
  isActiveVoice: boolean;
  speakingEnergy: number;
};

export const clamp01 = (n: number) => Math.min(1, Math.max(0, n));
export const smooth01 = (n: number) => {
  const x = clamp01(n);
  return x * x * (3 - 2 * x);
};

/** A speaker's speech envelope is sampled and smoothed without inferring words. */
export const smoothVoiceEnergy = (frame: number, fps: number, event?: VoiceEvent): number => {
  if (!event || !event.rms?.length || fps <= 0) return 0;
  const rate = event.samplesPerSecond ?? 10;
  if (!Number.isFinite(rate) || rate <= 0) return 0;
  const position = (frame - event.startFrame) * rate / fps;
  const i = Math.floor(Math.max(0, position));
  const a = event.rms[Math.min(event.rms.length - 1, i)] ?? 0;
  const b = event.rms[Math.min(event.rms.length - 1, i + 1)] ?? a;
  return clamp01(a + (b - a) * (position - Math.floor(position)));
};

/** Cues are computed from speech turns; a listener never mouths partner audio. */
export const listeningReactionCues = (
  id: CharacterId, voiceEvents: VoiceEvent[], chapter: number,
): ReactionCue[] => voiceEvents.filter(x => x.speaker !== id).map((x, i) => {
  const candidate: CharacterReaction = chapter === 6 ? 'surprised'
    : id === 'pix' && i % 5 === 2 ? 'excited'
    : i % 3 === 0 ? 'curious' : 'agree';
  return {
    atFrame: x.startFrame,
    durationFrames: Math.min(38, Math.max(11, x.endFrame - x.startFrame)),
    kind: candidate,
  };
});

/** A tiny list of gestures in short arcs; no eight-minute perpetual dancing. */
export const heroGestureFor = (
  id: CharacterId,
  chapter: number,
  activeSpeaker: CharacterId | undefined,
  frame: number,
  voiceEvents: VoiceEvent[],
): BodyGesture => {
  if (activeSpeaker !== id) return 'idle';
  const event = voiceEvents.find(x => x.speaker === id &&
    frame >= x.startFrame && frame < x.endFrame);
  if (!event) return 'idle';

  const age = frame - event.startFrame;
  const duration = Math.max(1, event.endFrame - event.startFrame);
  const phase = age / duration;
  // Entrances and hand-offs have a purposeful beat, rather than repeating action.
  if (id === 'pix') {
    if ((chapter === 1 || chapter >= 9) && phase < 0.38) return 'celebrate';
    if (chapter === 2 && phase < 0.45) return 'walk';
    if (chapter === 5 || chapter === 6) return phase > 0.25 && phase < 0.7 ? 'point' : 'explain';
    if (chapter === 3 || chapter === 4 || chapter === 8) return phase < 0.65 ? 'point' : 'explain';
    return phase < 0.25 ? 'point' : 'explain';
  }
  if ([3, 4, 5, 6, 8].includes(chapter) && phase > 0.25 && phase < 0.58) return 'point';
  return 'explain';
};

export const heroStateAt = (
  id: CharacterId, chapter: number, frame: number, fps: number,
  voiceEvents: VoiceEvent[],
): HeroDirection => {
  const event = voiceEvents.find(e=>e.speaker===id && frame >= e.startFrame && frame < e.endFrame);
  const speakingEnergy = smoothVoiceEnergy(frame, fps, event);
  const partner = voiceEvents.find(e=>e.speaker!==id && frame >= e.startFrame && frame < e.endFrame);
  const age = partner ? frame-partner.startFrame : 9999;
  const reaction = partner && age < 36 ? (
    chapter===6 ? 'surprised' : id==='pix' ? 'curious' : 'agree'
  ) as CharacterReaction : undefined;
  return {
    gesture: heroGestureFor(id,chapter,event?.speaker,frame,voiceEvents),
    listenerReaction: reaction,
    isSpeaking: Boolean(event),
    isActiveVoice: speakingEnergy > 0.11,
    speakingEnergy,
  };
};
