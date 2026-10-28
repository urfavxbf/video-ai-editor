import React from 'react';
import {useCurrentFrame} from 'remotion';
import {CharacterPuppet, type CharacterId,
  type LayeredPuppetRig, type VoiceEvent} from '../characters/CharacterPuppet';
import {HERO_IDENTITY, heroGestureFor, listeningReactionCues} from '../characters/HeroPerformance';

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
  urfavxbf: {assetPath: HERO_IDENTITY.urfavxbf.assetPath},
  pix: {assetPath: HERO_IDENTITY.pix.assetPath},
};

export type JourneyFullBodyCharactersProps = {
  voiceEvents: VoiceEvent[];
  chapter: number;
  activeSpeaker?: CharacterId;
  assets?: JourneyFullBodyAssetMap;
};

/** Character-only staging, leaving the 890px diagram area and caption zone legible. */
export const YouTubeJourneyFullBodyCharacters: React.FC<JourneyFullBodyCharactersProps> = ({
  voiceEvents, chapter, activeSpeaker, assets=DEFAULT_JOURNEY_FULL_BODY_ASSETS,
}) => {
  const frame = useCurrentFrame();
  return <React.Fragment>
  <CharacterPuppet
    id="urfavxbf"
    assetPath={assets.urfavxbf.assetPath}
    layeredRig={assets.urfavxbf.layeredRig}
    width={438} height={670} left={30} bottom={204}
    voiceEvents={voiceEvents}
    bodyGesture={heroGestureFor('urfavxbf',chapter,activeSpeaker,frame,voiceEvents)}
    reactions={listeningReactionCues('urfavxbf',voiceEvents,chapter)}
    fadeInFrames={13}
  />
  <CharacterPuppet
    id="pix"
    assetPath={assets.pix.assetPath}
    layeredRig={assets.pix.layeredRig}
    width={412} height={645} right={30} bottom={206}
    voiceEvents={voiceEvents}
    bodyGesture={heroGestureFor('pix',chapter,activeSpeaker,frame,voiceEvents)}
    reactions={listeningReactionCues('pix',voiceEvents,chapter)}
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
};
