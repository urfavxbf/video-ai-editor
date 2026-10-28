import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {CharacterPuppet, type VoiceEvent, type ReactionCue} from './CharacterPuppet';

/**
 * Rendering workbench for the officially approved transparent characters.
 * Pass assetsReady=true only after staging both PNGs in public/characters/.
 * The default workbench safely describes the missing binary inputs rather
 * than silently displaying substituted character art.
 */
export type CharacterAnimationLabProps = {
  assetsReady: boolean;
  voiceEvents?: VoiceEvent[];
};

export const CharacterAnimationLab: React.FC<CharacterAnimationLabProps> = ({
  assetsReady,
  voiceEvents = [],
}) => {
  const frame = useCurrentFrame();
  const glow = interpolate(frame, [0, 120, 240], [0.12, 0.35, 0.12], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const hostReactions: ReactionCue[] = [
    {atFrame: 26, durationFrames: 40, kind: 'curious'},
    {atFrame: 140, durationFrames: 40, kind: 'agree'},
  ];
  const pixReactions: ReactionCue[] = [
    {atFrame: 70, durationFrames: 36, kind: 'surprised'},
    {atFrame: 165, durationFrames: 54, kind: 'excited'},
  ];
  return (
    <AbsoluteFill style={{
      background: '#080f20', color: '#fff', fontFamily: 'Arial, sans-serif', overflow: 'hidden',
    }}>
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at 50% 34%, rgba(36,127,183,${glow.toFixed(3)}), transparent 63%)`,
      }}/>
      <div style={{
        position: 'absolute', left: 84, top: 74, fontSize: 21, letterSpacing: 5,
        fontWeight: 700, color: '#45D9F0',
      }}>CHARACTER ANIMATION LAB / 16:9</div>
      <div style={{
        position: 'absolute', left: 80, top: 128, maxWidth: 1700, fontWeight: 900,
        fontSize: 64, lineHeight: 1.07,
      }}>UrFavXBF <span style={{color:'#FFC600'}}>+</span> PIX</div>
      {assetsReady ? (
        <>
          <CharacterPuppet
            id="urfavxbf"
            assetPath="characters/UrFavXBF_Transparent.png"
            width={800} height={850} left={110} bottom={-18}
            voiceEvents={voiceEvents} reactions={hostReactions}
          />
          <CharacterPuppet
            id="pix"
            assetPath="characters/PIX_Transparent.png"
            width={610} height={700} right={80} bottom={45}
            voiceEvents={voiceEvents} reactions={pixReactions}
          />
        </>
      ) : (
        <div style={{
          position: 'absolute', left: 90, top: 400, width: 1710, minHeight: 230,
          border: '2px dashed #7D99AF', borderRadius: 24, padding: 38,
          fontSize: 29, lineHeight: 1.6, background: 'rgba(14,23,42,0.78)',
        }}>
          Stage the approved transparent character PNGs in <b>public/characters/</b>,
          then render this workbench with <b>assetsReady: true</b>.
          <div style={{fontSize: 23, color: '#93BCD0'}}>
            This placeholder does not imply 3D rigging or phoneme lip-sync.
          </div>
        </div>
      )}
      <div style={{
        position: 'absolute', left: 70, right: 70, bottom: 25,
        fontSize: 22, color: '#91ABB9', textAlign: 'center',
      }}>
        Speaker-aware reactions • measured WAV energy supported • optional independent sprite layers
      </div>
    </AbsoluteFill>
  );
};
