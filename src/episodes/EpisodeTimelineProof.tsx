import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import type {CalculateMetadataFunction} from 'remotion';
import {HeroCharacterStage} from '../characters/HeroCharacterStage';
import {compileEpisodeTimeline, type EpisodeManifestV1} from './episodeManifest';

/**
 * Deterministic proof composition. The fixtures deliberately contain NO generated
 * audio or captions; future production stages must provide verified source media.
 */
export type EpisodeTimelineProofProps = {manifest: EpisodeManifestV1};
export const calculateEpisodeTimelineMetadata: CalculateMetadataFunction<EpisodeTimelineProofProps> =
  ({props}) => ({durationInFrames: compileEpisodeTimeline(props.manifest).durationFrames});

export const EpisodeTimelineProof: React.FC<EpisodeTimelineProofProps> = ({manifest}) => {
  const {chapters} = compileEpisodeTimeline(manifest);
  return <AbsoluteFill style={{background: '#060d19'}}>
    {chapters.map((chapter) =>
      <Sequence key={chapter.id} from={chapter.startFrame} durationInFrames={chapter.durationFrames}>
        <AbsoluteFill>
          <HeroCharacterStage
            assetsReady={true}
            artApproved={true}
            chapter={chapter.chapterNumber}
            voiceEvents={chapter.voiceEvents ?? []}
            audio={chapter.audio ?? []}
            showStudyOverlay={false}
          />
          <div style={{
            position: 'absolute', top: 140, left: 610, width: 700,
            color: '#f1f6ff', textAlign: 'center', fontFamily: 'Inter',
            textShadow: '0 4px 16px #050e1c', pointerEvents: 'none',
          }}>
            <div style={{fontSize: 18, letterSpacing: 5, color: '#70e8ff'}}>
              MODEL-FREE TIMELINE PROOF
            </div>
            <div style={{fontSize: 49, fontWeight: 900, lineHeight: 1.15, marginTop: 24}}>
              {chapter.title}
            </div>
          </div>
        </AbsoluteFill>
      </Sequence>)}
  </AbsoluteFill>;
};
