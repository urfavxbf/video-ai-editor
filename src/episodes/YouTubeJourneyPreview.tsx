import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {JourneyVisualAid} from './YouTubeJourneyVisuals';
import {PixelGlitchPortrait} from '../characters/PixelGlitchPortrait';
import {type VoiceEvent} from '../characters/CharacterPuppet';

export type PreviewCaption = {text: string; startFrame: number; endFrame: number};
export type PreviewLine = {
  id: string;
  speaker: 'pix' | 'urfavxbf';
  text: string;
  startFrame: number;
  endFrame: number;
  file: string;
  scene: number;
  captions: PreviewCaption[];
};
export type PreviewSection = {scene: number; startFrame: number; endFrame: number};
export type YouTubeJourneyPreviewProps = {
  lines: PreviewLine[];
  sections: PreviewSection[];
  voiceEvents: VoiceEvent[];
  totalFrames: number;
  captionTiming: string;
};

const labelFor = (chapter: number) => chapter === 5
  ? 'HOW MONETIZATION WORKS'
  : 'WHAT A VIEW REALLY PAYS';

const PreviewCut: React.FC<{chapter: number; progress: number}> = ({chapter, progress}) => (
  <AbsoluteFill style={{
    background: '#060d19', display: 'flex', alignItems: 'center',
    justifyContent: 'center', fontFamily: 'Inter', color: '#f1f6ff',
    overflow: 'hidden',
  }}>
    <div style={{
      position: 'absolute', left: '16%', right: '16%', top: '50%',
      height: 2, background: '#27e8fd', opacity: 0.7,
      transform: `scaleX(${Math.min(1, progress * 2)})`,
    }}/>
    <div style={{position: 'absolute', top: 295, letterSpacing: 6, color: '#27e8fd', fontSize: 22}}>
      EDITED CHAPTER EXCERPT
    </div>
    <div style={{position: 'absolute', top: 375, fontWeight: 900, fontSize: 68,
      transform: `translateY(${Math.max(0, 1 - progress * 2) * 25}px)`}}>
      {labelFor(chapter)}
    </div>
    <div style={{position: 'absolute', top: 690, fontSize: 24, color: '#96a8c3'}}>
      Preview sequencing · not a continuous conversation
    </div>
  </AbsoluteFill>
);

/** Audio timings are measured from decoded WAV samples, never guessed from script length. */
export const YouTubeJourneyPreview: React.FC<YouTubeJourneyPreviewProps> = ({
  lines, sections, voiceEvents, captionTiming,
}) => {
  const frame = useCurrentFrame();
  const section = sections.find(s => frame >= s.startFrame && frame < s.endFrame);
  const next = sections.find(s => s.startFrame > frame);
  const activeLine = lines.find(l => frame >= l.startFrame && frame < l.endFrame);
  const activeCaption = activeLine?.captions.find(c => frame >= c.startFrame && frame < c.endFrame);
  const caption = activeCaption?.text ?? '';
  const previousEnd = sections.reduce((latest, s) => s.endFrame <= frame ? Math.max(latest, s.endFrame) : latest, 0);
  const scene = section?.scene ?? sections[sections.length - 1]?.scene ?? 1;
  const speaker = activeLine ? (activeLine.speaker === 'pix' ? 'PIX' : 'URFAVXBF') : '';

  return <AbsoluteFill style={{background: '#060d19'}}>
    {section ? <AbsoluteFill style={{color:'#f1f6ff',fontFamily:'Inter',
      background:'radial-gradient(ellipse at 50% 40%,#17364b 0%,#060d19 76%)'}}>
      <div style={{position:'absolute',left:64,top:50,right:64,display:'flex',
        justifyContent:'space-between',fontSize:18,letterSpacing:2,color:'#96a8c3'}}>
        <span>URFAVXBF × PIX / CREATOR FIELD GUIDE</span><span>ENGLISH · VISUAL PREVIEW</span>
      </div>
      <div style={{position:'absolute',left:64,top:110,fontSize:52,fontWeight:900}}>
        {scene===5?'TWO MONETIZATION GATES':scene===6?'HOW RPM CHANGES EARNINGS':'AFTER YOU HIT UPLOAD'}
      </div>
      <PixelGlitchPortrait id="urfavxbf" left={64} top={220} showGlitch={false}
        voiceEvents={voiceEvents} reactions={[{speaker:'urfavxbf',startFrame:0,endFrame:999999,reaction:'thinking'}]}/>
      <PixelGlitchPortrait id="pix" right={64} top={220} showGlitch={false}
        voiceEvents={voiceEvents} reactions={[{speaker:'pix',startFrame:0,endFrame:999999,reaction:scene===6?'surprised':'curious'}]}/>
      <div style={{position:'absolute',left:515,top:230,width:890}}>
        <JourneyVisualAid beat={scene===5?5:scene===6?6:1}
          chapter={scene} localFrame={frame-section.startFrame}/>
      </div>
      <div style={{position:'absolute',bottom:85,left:64,right:64,minHeight:105,
        borderTop:'1px solid #35485e',paddingTop:17,background:'rgba(6,13,25,.88)'}}>
        <div style={{fontSize:17,letterSpacing:2.5,color:speaker==='PIX'?'#27e8fd':'#ffda00',
          fontWeight:900}}>{speaker}</div>
        <div style={{fontSize:30,fontWeight:700,marginTop:6}}>{caption}</div>
      </div>
      <div style={{position:'absolute',left:64,bottom:30,fontSize:16,color:'#96a8c3'}}>
        PRODUCTION PREVIEW · SELECTED EXCERPTS
      </div>
    </AbsoluteFill> : next ? <PreviewCut
      chapter={next.scene}
      progress={(frame - previousEnd) / Math.max(1, next.startFrame - previousEnd)}
    /> : <AbsoluteFill style={{
      background: '#060d19', color: '#f1f6ff', justifyContent: 'center',
      alignItems: 'center', fontFamily: 'Inter', fontSize: 60, fontWeight: 900,
    }}>ONE USEFUL VIDEO AT A TIME.</AbsoluteFill>}
    {lines.map(l => <Sequence key={l.id} from={l.startFrame}
      durationInFrames={l.endFrame - l.startFrame}>
      <Audio src={staticFile(l.file)} volume={0.85}/>
    </Sequence>)}
    {section && captionTiming !== 'reviewed-word-aligned' ? <div style={{
      position: 'absolute', right: 65, top: 209, color: '#96a8c3',
      fontFamily: 'Inter', fontSize: 14, letterSpacing: 1,
    }}>DRAFT CAPTION TIMING · HUMAN QC REQUIRED</div> : null}
  </AbsoluteFill>;
};
