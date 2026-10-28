import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {YouTubeJourneyStyleframes} from './YouTubeJourneyStyleframes';
import {type VoiceEvent} from '../characters/CharacterPuppet';

export type PreviewLine = {id:string;speaker:'pix'|'urfavxbf';text:string;startFrame:number;endFrame:number;file:string;scene:number};
export type YouTubeJourneyPreviewProps = {lines:PreviewLine[];voiceEvents:VoiceEvent[];totalFrames:number;chapterBreakStart:number;chapterBreakEnd:number};
export const YouTubeJourneyPreview: React.FC<YouTubeJourneyPreviewProps> = ({lines,voiceEvents,chapterBreakStart,chapterBreakEnd}) => {
  const f=useCurrentFrame();
  const line=lines.find(l=>f>=l.startFrame&&f<l.endFrame);
  const inBreak=f>=chapterBreakStart&&f<chapterBreakEnd;
  const scene=f>=chapterBreakEnd?1:0;
  return <AbsoluteFill>
    <YouTubeJourneyStyleframes sceneOverride={scene} captionOverride={line?.text??''} speakerOverride={line?(line.speaker==='pix'?'PIX':'URFAVXBF'):''} voiceEvents={voiceEvents} preview sceneStart={scene===1?chapterBreakEnd:0}/>
    {lines.map(l=><Sequence key={l.id} from={l.startFrame} durationInFrames={l.endFrame-l.startFrame}><Audio src={staticFile(l.file)}/></Sequence>)}
    {inBreak?<AbsoluteFill style={{background:'#060d19',justifyContent:'center',alignItems:'center',color:'white',fontFamily:'Inter',gap:24}}><div style={{fontSize:22,letterSpacing:5,color:'#27e8fd'}}>LATER IN THE EPISODE</div><div style={{fontSize:72,fontWeight:900}}>THE MONETIZATION GATES</div><div style={{fontSize:25,color:'#96a8c3'}}>Preview excerpt · requirements and speaker handoff</div></AbsoluteFill>:null}
  </AbsoluteFill>;
};
