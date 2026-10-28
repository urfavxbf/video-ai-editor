import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {type CharacterId, type VoiceEvent, findVoiceEvent, voiceEnergyAtFrame} from './CharacterPuppet';

/**
 * Separate transparent pixel-art sprite loops, rendered frame deterministically.
 * Requires the approved binary pack staged in public/characters/pixel-glitch/.
 * No live 3D skeleton, mouth-viseme mapping or waveform-based word alignment.
 */
export type PixelGlitchSpriteProps = {
  id: CharacterId;
  left?: number;
  right?: number;
  top?: number;
  bottom?: number;
  width?: number;
  height?: number;
  mode?: 'idle' | 'talk' | 'react';
  voiceEvents?: VoiceEvent[];
  startFrame?: number;
  glitchIntervalFrames?: number;
};

const modes = {
  idle: {frameCount: 8, speed: 5},
  talk: {frameCount: 8, speed: 8},
  react: {frameCount: 8, speed: 8},
} as const;
const BASE = 'characters/pixel-glitch';
const frameIndex = (f: number, fps: number, speed: number, count: number) =>
  Math.floor(Math.max(0, f) / Math.max(1, fps / speed)) % count;

/** No media fallbacks: require real staged character files, not fake stock assets. */
export const PixelGlitchSprite: React.FC<PixelGlitchSpriteProps> = ({
  id, left, right, top, bottom, width = 300, height = 300,
  mode = 'idle', voiceEvents = [], startFrame = 0,
  glitchIntervalFrames = 107,
}) => {
  const currentFrame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = currentFrame - startFrame;
  const activeEvent = findVoiceEvent(id, currentFrame, voiceEvents);
  const effectiveMode = activeEvent ? 'talk' : mode;
  const config = modes[effectiveMode];
  const index = frameIndex(t, fps, config.speed, config.frameCount);
  const src = staticFile(`${BASE}/${id}/loops/${effectiveMode}/${String(index).padStart(2, '0')}.png`);
  const energy = voiceEnergyAtFrame(currentFrame, fps, activeEvent);
  const bob = 2 * Math.sin(currentFrame * 0.055 + (id === 'pix' ? 0 : 1.1))
    - (activeEvent ? 3.3 * energy : 0);
  const roll = (id === 'pix' ? 1 : -1) *
    (activeEvent ? Math.sin(currentFrame * 0.2) * 1.2 * energy : Math.sin(currentFrame * 0.04) * 0.4);
  const glitch = glitchIntervalFrames > 0 && currentFrame > 0 && currentFrame % glitchIntervalFrames < 4;
  return (
    <div data-character={id} data-state={effectiveMode} style={{
      position: 'absolute', left, right, top, bottom, width, height,
      pointerEvents: 'none',
      transform: `translateY(${bob.toFixed(1)}px) rotate(${roll.toFixed(2)}deg)`,
      filter: glitch
        ? 'drop-shadow(6px 0 #f000fb) drop-shadow(-6px 0 #00f5ff)'
        : id === 'pix' ? 'drop-shadow(0 0 8px rgba(0,230,255,.26))'
          : 'drop-shadow(0 0 8px rgba(255,210,0,.22))',
    }}>
      <Img src={src} style={{width:'100%',height:'100%',objectFit:'contain',imageRendering:'pixelated'}} />
    </div>
  );
};
