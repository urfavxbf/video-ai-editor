import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {PixelGlitchPortrait} from '../characters/PixelGlitchPortrait';
import {type VoiceEvent} from '../characters/CharacterPuppet';
import {type PreviewLine} from './YouTubeJourneyPreview';
import {JourneyVisualAid} from './YouTubeJourneyVisuals';

export type YouTubeJourneyFullEpisodeProps = {
  lines: PreviewLine[];
  voiceEvents: VoiceEvent[];
  totalFrames: number;
  captionTiming: 'estimated-unreviewed' | 'reviewed-word-aligned';
  assetsReady: boolean;
};

const visualBeatFor = (chapter:number) => Math.min(chapter,8);

export const YouTubeJourneyFullEpisode:React.FC<YouTubeJourneyFullEpisodeProps> = ({
  lines, voiceEvents, captionTiming, assetsReady,
}) => {
  const frame=useCurrentFrame();
  // Never produce an audio-backed final video with missing approved portraits.
  if (lines.length && !assetsReady) {
    throw new Error('Approved PIX + UrFavXBF pixel glitch portrait PNGs must be staged before full-episode render');
  }
  const currentLine=lines.find(l=>frame>=l.startFrame&&frame<l.endFrame);
  const preceding=[...lines].reverse().find(l=>l.startFrame<=frame);
  const chapter=currentLine?.scene ?? preceding?.scene ?? 1;
  const chapterStart=lines.find(l=>l.scene===chapter)?.startFrame ?? 0;
  const caption=currentLine?.captions.find(c=>frame>=c.startFrame&&frame<c.endFrame)?.text ?? '';
  const speaker=currentLine?.speaker==='pix'?'PIX':currentLine?.speaker==='urfavxbf'?'URFAVXBF':'';
  const titles=[
    'YOU HIT UPLOAD. NOW WHAT?', 'FIND YOUR VIEWER', 'HOW VIEWERS DISCOVER YOU',
    'MAKE THE PROMISE CLEAR', 'TWO MONETIZATION GATES', 'WHY RPM CHANGES THE MATH',
    'MORE THAN AD REVENUE', 'ORIGINAL WORK MATTERS', 'PIX HAS A PLAN',
  ];
  const title=titles[chapter-1] ?? 'THE CREATOR FIELD GUIDE';
  const accent=speaker==='PIX'?'#27e8fd':'#ffda00';

  return <AbsoluteFill style={{background:'#060d19',color:'#f1f6ff',fontFamily:'Inter'}}>
    <div style={{position:'absolute',inset:0,
      backgroundImage:'radial-gradient(ellipse at 50% 40%, #17364b 0%, transparent 68%)'}}/>
    <div style={{position:'absolute',left:64,top:43,right:64,display:'flex',
      justifyContent:'space-between',color:'#96a8c3',fontSize:18,letterSpacing:2.8}}>
      <span>URFAVXBF × PIX / CREATOR FIELD GUIDE</span>
      <span>ENGLISH · ORIGINAL LONG FORM</span>
    </div>
    <div style={{position:'absolute',left:64,top:108,right:64,fontSize:53,
      fontWeight:900,letterSpacing:-1}}>{title}</div>
    {assetsReady?<>
      <PixelGlitchPortrait id="urfavxbf" left={64} top={218}
        voiceEvents={voiceEvents} showGlitch={false}
        reactions={[{speaker:'urfavxbf',startFrame:0,endFrame:999999,reaction:chapter===6?'excited':'thinking'}]}/>
      <PixelGlitchPortrait id="pix" right={64} top={218}
        voiceEvents={voiceEvents} showGlitch={false}
        reactions={[{speaker:'pix',startFrame:0,endFrame:999999,reaction:chapter===6?'surprised':'curious'}]}/>
    </>:null}
    <div style={{position:'absolute',left:515,width:890,top:230}}>
      <JourneyVisualAid beat={visualBeatFor(chapter)}
        chapter={chapter} localFrame={frame-chapterStart}/>
    </div>
    <div style={{position:'absolute',left:64,right:64,bottom:91,minHeight:114,
      borderTop:'2px solid #35485e',paddingTop:16,background:'rgba(6,13,25,.92)'}}>
      <div style={{fontSize:17,fontWeight:900,letterSpacing:2.5,color:accent}}>
        {speaker}
      </div>
      <div style={{fontSize:30,fontWeight:750,marginTop:8,lineHeight:1.16,
        maxWidth:1720}}>{caption}</div>
    </div>
    <div style={{position:'absolute',left:64,bottom:29,right:64,display:'flex',
      justifyContent:'space-between',color:'#96a8c3',fontSize:16}}>
      <span>{captionTiming!=='reviewed-word-aligned'?
        'DRAFT CAPTIONS · TIMING ESTIMATED · HUMAN QC REQUIRED':
        'REVIEWED CAPTION ALIGNMENT'}</span>
      <span>CHAPTER {String(chapter).padStart(2,'0')} / 09 · NOT FOR AUTO-UPLOAD</span>
    </div>
    {lines.map(l=><Sequence key={l.id} from={l.startFrame}
      durationInFrames={l.endFrame-l.startFrame}>
      <Audio src={staticFile(l.file)} volume={0.85}/>
    </Sequence>)}
  </AbsoluteFill>;
};
