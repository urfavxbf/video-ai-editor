import React, {useMemo} from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import type {CalculateMetadataFunction} from 'remotion';
import {HeroCharacterStage} from '../characters/HeroCharacterStage';
import {compileEpisodeTimeline, type EpisodeManifestV1} from './episodeManifest';
import {validateProductionCaptions, type ProductionCaptions, type ProductionCaption} from './productionCaptions';

export type EpisodeProductionProps = {manifest: EpisodeManifestV1; captions: ProductionCaptions};
export const calculateEpisodeProductionMetadata: CalculateMetadataFunction<EpisodeProductionProps> = ({props}) => {
  const compiled = compileEpisodeTimeline(props.manifest);
  validateProductionCaptions(props.captions, compiled.chapters);
  return {durationInFrames: compiled.durationFrames};
};
const Captions: React.FC<{cues: ProductionCaption[]}> = ({cues}) => {
  const frame = useCurrentFrame();
  const cue = cues.find(c => c.startFrame <= frame && frame < c.endFrame);
  return cue ? <div style={{position:'absolute',bottom:195,left:620,width:680,textAlign:'center',
    fontFamily:'Inter',fontSize:36,fontWeight:750,lineHeight:1.35,color:'#fff',
    background:'#060d19ed',borderRadius:12,padding:'18px 24px',boxSizing:'border-box',overflowWrap:'anywhere'}}>{cue.text}</div> : null;
};
const ChapterTransition: React.FC = () => {
  const frame = useCurrentFrame();
  if (frame >= 7) return null;
  const opacity = (7-frame)/7*0.55;
  return <AbsoluteFill style={{opacity,pointerEvents:'none'}}>
    {Array.from({length:7},(_,i) => <div key={i} style={{position:'absolute',
      top:(i*139+frame*23)%1080,left:0,width:'100%',height:2+i%3,
      background:i%2?'#23f3e5':'#d43cfa',transform:`translateX(${Math.sin(frame*11)*12}px)`}}/>)}
  </AbsoluteFill>;
};

/** Uses measured/imported props. No providers, fake phonemes or study/demo overlay. */
export const EpisodeProduction: React.FC<EpisodeProductionProps> = ({manifest,captions}) => {
  const compiled = useMemo(() => compileEpisodeTimeline(manifest), [manifest]);
  const verified = useMemo(() => validateProductionCaptions(captions, compiled.chapters), [captions,compiled]);
  return <AbsoluteFill>{compiled.chapters.map(chapter =>
    <Sequence key={chapter.id} from={chapter.startFrame} durationInFrames={chapter.durationFrames}>
      <HeroCharacterStage assetsReady artApproved chapter={chapter.chapterNumber}
        voiceEvents={chapter.voiceEvents ?? []} audio={chapter.audio ?? []} showStudyOverlay={false}/>
      <div style={{position:'absolute',top:150,left:620,width:680,color:'#f1f6ff',textAlign:'center',
        fontFamily:'Inter',fontSize:48,fontWeight:850,lineHeight:1.2}}>{chapter.title}</div>
      <Captions cues={verified[chapter.id] ?? []}/>
      <ChapterTransition/>
    </Sequence>)}</AbsoluteFill>;
};
