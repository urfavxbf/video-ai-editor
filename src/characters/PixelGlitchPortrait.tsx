import React from 'react';
import {PORTRAIT_LAYOUT} from './portraitLayout';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {type CharacterId, type VoiceEvent, findVoiceEvent, voiceEnergyAtFrame} from './CharacterPuppet';

/**
 * Canonical pixel/glitch V2 character layout: animated HEAD PORTRAITS ONLY.
 * Never renders full-body sprites. The expressions are independent transparent
 * PNGs from the approved pack, not face-rigged 3D models or viseme-accurate lips.
 */
export type PortraitReaction = 'neutral' | 'curious' | 'happy' | 'excited' | 'thinking' | 'surprised' | 'glitch';

export type PortraitReactionCue = {
  speaker: CharacterId;
  startFrame: number;
  endFrame: number; // exclusive
  reaction: PortraitReaction;
};

export type PixelGlitchPortraitProps = {
  id: CharacterId;
  left?: number;
  right?: number;
  top?: number;
  bottom?: number;
  /** Approved enlarged head portraits for 16:9, with central infographics unobstructed. */
  width?: number;
  height?: number;
  voiceEvents?: VoiceEvent[];
  reactions?: PortraitReactionCue[];
  showGlitch?: boolean;
  /** Pass paths only after the approved ZIP has been staged into public/. */
  assetPrefix?: string;
};

export type PortraitState = {
  expression: 'neutral' | 'talk' | 'excited' | 'thinking' | 'surprised' | 'glitch' | 'happy' | 'curious';
  isSpeaking: boolean;
  energy: number;
};

const clamp = (n: number) => Math.max(0, Math.min(1, n));

export const portraitStateAtFrame = (
  id: CharacterId,
  frame: number,
  fps: number,
  events: VoiceEvent[],
  reactions: PortraitReactionCue[],
  glitchEnabled = true,
): PortraitState => {
  const event = findVoiceEvent(id, frame, events);
  const energy = voiceEnergyAtFrame(frame, fps, event);
  const reaction = reactions.find(c => c.speaker === id && frame >= c.startFrame && frame < c.endFrame);
  const react = reaction?.reaction ?? 'neutral';
  const glitch = glitchEnabled && frame > 0 && frame % 131 < 4;
  const allowed = id === 'pix'
    ? ['neutral', 'talk', 'happy', 'curious', 'surprised', 'glitch']
    : ['neutral', 'talk', 'excited', 'thinking', 'surprised', 'glitch'];
  const expression = glitch ? 'glitch'
    : event && energy > 0.16 ? 'talk'
      : allowed.includes(react) ? react : 'neutral';
  return {expression: expression as PortraitState['expression'], isSpeaking: Boolean(event), energy: clamp(energy)};
};

export const PixelGlitchPortrait: React.FC<PixelGlitchPortraitProps> = ({
  id, left, right, top, bottom,
  width = PORTRAIT_LAYOUT.width, height = PORTRAIT_LAYOUT.height, voiceEvents = [], reactions = [],
  showGlitch = true, assetPrefix = 'characters/pixel-glitch',
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const state = portraitStateAtFrame(id, frame, fps, voiceEvents, reactions, showGlitch);
  const yellow = id === 'urfavxbf';
  const accent = yellow ? '#FFDA00' : '#27E8FD';
  const title = yellow ? 'URFAVXBF' : 'PIX';
  const bob = Math.sin((frame / fps) * 2.3 + (yellow ? 1.1 : 0)) * 4;
  const activeGlow = state.isSpeaking ? 0.3 + state.energy * 0.65 : 0.13;
  const background = '#071322';
  return (
    <div data-character={id} data-layout="portrait-only" data-speaking={state.isSpeaking ? 'true' : 'false'}
      style={{
        position: 'absolute', width, height, left, right, top, bottom,
        transform: `translateY(${bob.toFixed(2)}px)`,
        pointerEvents: 'none',
        background, border: `3px solid ${accent}`, borderRadius: 24,
        boxShadow: `0 0 ${Math.round(24 * activeGlow)}px ${accent}`,
        overflow: 'hidden',
      }}
    >
      <Img
        src={staticFile(`${assetPrefix}/${id}/${state.expression}.png`)}
        style={{
          position: 'absolute', top: 9, left: 7, width: width - 20, height: height - 67,
          objectFit: 'contain', imageRendering: 'pixelated',
        }}
      />
      <div style={{
        position: 'absolute', bottom: 0, left: 0, right: 0, height: 58,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 17px', fontFamily: 'monospace', fontSize: 24, fontWeight: 800,
        letterSpacing: 1, color: accent, background: 'rgba(3,8,20,0.97)',
      }}>
        <span>{title}</span>
        <div style={{display: 'flex', alignItems: 'flex-end', gap: 6, height: 26}}>
          {[0,1,2,3,4].map(k => (
            <div key={k} style={{
              width: 8,
              height: 5 + (state.isSpeaking ? Math.round(20 * state.energy * Math.abs(Math.sin(frame * 0.32 + k * 0.7))) : 0),
              background: accent,
            }}/>
          ))}
        </div>
      </div>
    </div>
  );
};
