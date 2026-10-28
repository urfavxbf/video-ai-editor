import React from 'react';
import {CharacterPuppet, type BodyGesture, type CharacterId,
  type LayeredPuppetRig, type ReactionCue, type VoiceEvent} from '../characters/CharacterPuppet';

/**
 * Verified Super Pixel/Glitch V2 transparent full-body sprites, not head-only loop PNGs.
 * Rig layers are optional and must represent the SAME original character;
 * never auto-generate replacement art or pretend a flat PNG has separate arms.
 */
export type JourneyFullBodyAsset = {
  assetPath: string;
  layeredRig?: LayeredPuppetRig;
};
export type JourneyFullBodyAssetMap = Record<CharacterId, JourneyFullBodyAsset>;

export const DEFAULT_JOURNEY_FULL_BODY_ASSETS: JourneyFullBodyAssetMap = {
  urfavxbf: {assetPath: 'characters/pixel-glitch/urfavxbf/base.png'},
  pix: {assetPath: 'characters/pixel-glitch/pix/base.png'},
};

const actionFor = (chapter: number, speaker: CharacterId, active: boolean): BodyGesture => {
  if (!active) return 'idle';
  if (chapter === 1) return speaker === 'pix' ? 'celebrate' : 'explain';
  if (chapter === 2) return speaker === 'pix' ? 'walk' : 'explain';
  if (chapter === 3 || chapter === 4) return 'point';
  if (chapter === 5 || chapter === 6) return speaker === 'pix' ? 'point' : 'explain';
  if (chapter === 7) return 'explain';
  if (chapter === 8) return 'point';
  return speaker === 'pix' ? 'celebrate' : 'explain';
};

const listeningReactions = (
  id: CharacterId,
  events: VoiceEvent[],
  chapter: number,
): ReactionCue[] => events.filter(e=>e.speaker!==id).map((e,i)=>({
  atFrame: e.startFrame,
  durationFrames: Math.min(42, Math.max(10, e.endFrame-e.startFrame)),
  kind: chapter===6 ? 'surprised' : i%3===0 ? 'curious' : 'agree',
}));

export type JourneyFullBodyCharactersProps = {
  voiceEvents: VoiceEvent[];
  chapter: number;
  activeSpeaker?: CharacterId;
  assets?: JourneyFullBodyAssetMap;
};

/** Character-only staging, leaving the 890px diagram area and caption zone legible. */
export const YouTubeJourneyFullBodyCharacters: React.FC<JourneyFullBodyCharactersProps> = ({
  voiceEvents, chapter, activeSpeaker, assets=DEFAULT_JOURNEY_FULL_BODY_ASSETS,
}) => <React.Fragment>
  <CharacterPuppet
    id="urfavxbf"
    assetPath={assets.urfavxbf.assetPath}
    layeredRig={assets.urfavxbf.layeredRig}
    width={438} height={670} left={30} bottom={204}
    voiceEvents={voiceEvents}
    bodyGesture={actionFor(chapter,'urfavxbf',activeSpeaker==='urfavxbf')}
    reactions={listeningReactions('urfavxbf',voiceEvents,chapter)}
    fadeInFrames={13}
  />
  <CharacterPuppet
    id="pix"
    assetPath={assets.pix.assetPath}
    layeredRig={assets.pix.layeredRig}
    width={412} height={645} right={30} bottom={206}
    voiceEvents={voiceEvents}
    bodyGesture={actionFor(chapter,'pix',activeSpeaker==='pix')}
    reactions={listeningReactions('pix',voiceEvents,chapter)}
    fadeInFrames={16}
  />
  <div style={{position:'absolute',left:37,bottom:180,
    width:425,textAlign:'center',fontSize:18,fontWeight:900,letterSpacing:2,
    fontFamily:'Inter',color:'#ffda00',textShadow:'0 2px 8px #060d19'}}>
    URFAVXBF
  </div>
  <div style={{position:'absolute',right:37,bottom:180,
    width:398,textAlign:'center',fontSize:18,fontWeight:900,letterSpacing:2,
    fontFamily:'Inter',color:'#27e8fd',textShadow:'0 2px 8px #060d19'}}>
    PIX
  </div>
</React.Fragment>;
