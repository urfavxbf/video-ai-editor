import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {PixelGlitchPortrait, type PortraitReactionCue} from '../characters/PixelGlitchPortrait';
import {PORTRAIT_LAYOUT} from '../characters/portraitLayout';
import type {VoiceEvent} from '../characters/CharacterPuppet';
import {Y2038_CHAPTERS, Y2038_CUES, Y2038_TOTAL_FRAMES} from './y2038Dialogues';

const GOLD='#FFDF35', CYAN='#20DFFF', WHITE='#F1FCFF';
const RED='#FF557E';
export type Y2038LongFormProps={
  assetsReady:boolean;
  /** Only pass verified time-aligned WAV envelope events. No synthetic lip sync. */
  voiceEvents?:VoiceEvent[];
  reactions?:PortraitReactionCue[];
  /** Optional rendered WAV/MP3 tracks placed in public/; cueIndex is zero-based. */
  voiceClips?:Array<{cueIndex:number;path:string}>;
  /** Real WAV clip-level boundaries from scripts/y2038_audio_props.py. */
  timedCues?:Array<{startFrame:number;endFrame:number}>;
  totalFrames?:number;
  audioLanguage?:'tl' | 'en';
  /** Original low-volume score placed in public/, optional until mastered. */
  backgroundMusicPath?:string;
  backgroundMusicVolume?:number;
};
export {Y2038_TOTAL_FRAMES};

const capsule=(accent:string):React.CSSProperties=>({
  border:`2px solid ${accent}`,borderRadius:12,padding:'10px 18px',background:'rgba(4,13,29,.91)',
  boxShadow:`0 0 30px ${accent}20`,
});
const chapterFacts:Record<number,{heading:string;eyebrow:string;stats:string[]}> = {
  1:{heading:'2038 / 1901',eyebrow:'TIMESTAMP ROLLOVER DEMO',stats:['2038-01-19','03:14:08 UTC','NOT ALL DEVICES']},
  2:{heading:'1970 → 2038',eyebrow:'UNIX EPOCH TIMELINE',stats:['START: 1970-01-01','+1 / SECOND','SECONDS SINCE EPOCH']},
  3:{heading:'2,147,483,647',eyebrow:'MAXIMUM SIGNED 32-BIT VALUE',stats:['2³¹ − 1','NEXT VALUE OVER LIMIT','WRAP IS ONE POSSIBLE OUTCOME']},
  4:{heading:'ERROR ≠ APOCALYPSE',eyebrow:'SYSTEM-SPECIFIC CONSEQUENCES',stats:['ERROR / REJECT','WRAP / MISREAD','UNDEFINED BEHAVIOR']},
  5:{heading:'TIME64',eyebrow:'MODERN REPRESENTATIONS',stats:['64-BIT RANGE','MIGRATED SYSTEMS','AUDIT ALL DEPENDENCIES']},
  6:{heading:'2040 EXPIRY',eyebrow:'THE BUG CAN START EARLY',stats:['DATE ARITHMETIC','LONG-LIVED DEVICES','FUTURE TIMESTAMPS']},
  7:{heading:'TEST → FIX → VERIFY',eyebrow:'ENGINEERING CHECKLIST',stats:['BOUNDARY TESTS','MIGRATE SAFELY','CHECK API + STORAGE']},
  8:{heading:'KNOW THE LIMITS',eyebrow:'THE REAL LESSON',stats:['UNDERSTAND','TEST','DON’T PANIC']},
};
const showPanel = (chapter:number, frame:number, start:number, speaker:string, accent:string) => {
  const fact=chapterFacts[chapter];
  const local=frame-start;
  const scale=1+0.006*Math.sin(local/16);
  return (
    <div style={{marginTop:22,borderRadius:24,border:'2px solid #1D9BB6',position:'relative',
      background:'linear-gradient(150deg,rgba(12,42,66,.94),rgba(4,11,26,.95))',
      padding:'30px 34px 24px',minHeight:340,overflow:'hidden'}}>
      <div style={{fontSize:20,color:CYAN,letterSpacing:2,fontWeight:900}}>{fact.eyebrow}</div>
      <div style={{marginTop:28,fontSize:chapter===3?69:72,fontWeight:1000,lineHeight:1.15,
        transform:`scale(${scale})`,transformOrigin:'left center',
        color:chapter===4?RED:accent,textShadow:`0 0 22px ${accent}55`}}>{fact.heading}</div>
      <div style={{display:'flex',gap:12,marginTop:30,flexWrap:'wrap'}}>
        {fact.stats.map((s,i)=><div key={s} style={{...capsule(i===0?accent:CYAN),fontSize:18,
          opacity:interpolate(local,[i*8,i*8+9],[.35,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{s}</div>)}
      </div>
      {chapter===3||chapter===1?<div style={{marginTop:27,height:10,background:'#12334B',borderRadius:12,overflow:'hidden'}}>
        <div style={{width:`${Math.min(100,Math.max(0,(local%180)/180*100))}%`,height:'100%',
          background:chapter===3?RED:GOLD}}/></div>:null}
      {chapter===2?<div style={{position:'absolute',bottom:20,left:34,right:34,display:'flex',justifyContent:'space-between',
        borderTop:'3px solid #25D8ED',paddingTop:8,color:'#ACECF6',fontSize:20}}>
        <span>1970</span><span>2026</span><span>2038</span></div>:null}
      <div style={{position:'absolute',right:19,top:16,color:'#3A7A95',fontSize:15}}>CH.{chapter.toString().padStart(2,'0')}</div>
    </div>
  );
};

export const Y2038LongForm:React.FC<Y2038LongFormProps>=({
  assetsReady,voiceEvents=[],reactions=[],voiceClips=[],timedCues,
  totalFrames, audioLanguage='tl',
  backgroundMusicPath,backgroundMusicVolume=0.25,
})=>{
  const frame=useCurrentFrame();
  const cues=timedCues?.length===Y2038_CUES.length
    ?Y2038_CUES.map((cue,i)=>({...cue,startFrame:timedCues[i].startFrame,endFrame:timedCues[i].endFrame}))
    :Y2038_CUES;
  let cueIndex = 0;
  for (let i = 0; i < cues.length; i++) {
    if (frame >= cues[i].startFrame) cueIndex = i;
    else break;
  }
  const cue=cues[cueIndex]??cues[cues.length-1];
  const accent=cue.speaker==='pix'?CYAN:GOLD;
  const words=cue.text.split(/\s+/u);
  // Cue-level paging is provisional; word alignment needs a dedicated pass.
  const pages=Math.ceil(words.length/11);
  const wordPage=Math.min(pages-1,Math.max(0,Math.floor((frame-cue.startFrame)/Math.max(1,cue.endFrame-cue.startFrame)*pages)));
  const subtitle=words.slice(wordPage*11,wordPage*11+11).join(' ');
  const lower=subtitle.toLocaleLowerCase('en');
  const triggers=['2038','1901','64-bit','32-bit','2,147,483,647','1970','2040'];
  const featured=triggers.find(t=>lower.includes(t.toLowerCase()));
  return <AbsoluteFill style={{color:WHITE,fontFamily:'Arial, sans-serif',overflow:'hidden',
    background:'radial-gradient(ellipse at center, #12334b 0%, #08172a 53%, #030813 100%)'}}>
    <AbsoluteFill style={{backgroundImage:'linear-gradient(rgba(13,190,219,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(13,190,219,.055) 1px,transparent 1px)',
      backgroundSize:'38px 38px',opacity:.82}}/>
    <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(255,223,53,.07),transparent 30%,transparent 70%,rgba(32,223,255,.08))'}}/>
    <div style={{position:'absolute',left:0,top:0,width:'100%',height:112,boxSizing:'border-box',
      display:'flex',alignItems:'center',justifyContent:'space-between',padding:'0 55px',
      borderBottom:'3px solid #1DBCD2',background:'rgba(2,10,21,.93)'}}>
      <div style={{fontSize:32,fontWeight:900,letterSpacing:1}}><span style={{color:GOLD}}>URFAVXBF</span>
      <span style={{color:'#D4ECF1',padding:'0 14px'}}>×</span><span style={{color:CYAN}}>PIX</span></div>
      <div style={{fontSize:23,fontWeight:800,color:'#B0E6F1'}}>THE 2038 PROBLEM</div>
    </div>
    {assetsReady?<><PixelGlitchPortrait id="urfavxbf" left={PORTRAIT_LAYOUT.left} top={PORTRAIT_LAYOUT.top} voiceEvents={voiceEvents} reactions={reactions}/>
      <PixelGlitchPortrait id="pix" right={PORTRAIT_LAYOUT.right} top={PORTRAIT_LAYOUT.top} voiceEvents={voiceEvents} reactions={reactions}/></>
      :(['URFAVXBF','PIX'] as const).map((label,i)=><div key={label} style={{position:'absolute',
          top:PORTRAIT_LAYOUT.top,left:i===0?64:undefined,right:i===1?64:undefined,
          width:414,height:468,borderRadius:24,boxSizing:'border-box',
          background:'rgba(7,19,34,.9)',border:`3px dashed ${i?CYAN:GOLD}`,
          display:'grid',placeItems:'center',textAlign:'center',color:i?CYAN:GOLD,fontWeight:800,fontSize:22,padding:22}}>
          STAGE APPROVED {label} PORTRAIT ASSETS
        </div>)}
    <div style={{position:'absolute',left:515,top:156,width:890}}>
      <div style={{fontSize:19,color:'#93DCE8',letterSpacing:2}}>CHAPTER {cue.chapter.toString().padStart(2,'0')} / 08</div>
      <div style={{fontSize:30,fontWeight:900,marginTop:6}}>{Y2038_CHAPTERS[cue.chapter-1]}</div>
      {showPanel(cue.chapter,frame,cue.startFrame,cue.speaker,accent)}
      <div style={{borderTop:`3px solid ${accent}`,marginTop:20,padding:'19px 25px 24px',
        minHeight:158,boxSizing:'border-box',borderRadius:16,
        background:'rgba(2,11,26,.94)',position:'relative',boxShadow:`0 0 24px ${accent}22`}}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
          <span style={{fontSize:20,color:accent,fontWeight:900,letterSpacing:1}}>
            {cue.speaker==='pix'?'PIX':'URFAVXBF'} // {audioLanguage==='tl'?'TAGALOG':'ENGLISH'}
          </span>
          {featured?<span style={{fontSize:20,color:accent,fontWeight:900}}>{featured.toUpperCase()}</span>:null}
        </div>
        <div style={{fontSize:32,lineHeight:1.35,fontWeight:750,marginTop:16}}>{subtitle}</div>
      </div>
    </div>
    <div style={{position:'absolute',bottom:26,left:64,right:64,height:8,
      background:'rgba(8,56,77,.88)',borderRadius:8}}>
      <div style={{height:'100%',width:`${Math.round(frame/(totalFrames??Y2038_TOTAL_FRAMES)*10000)/100}%`,
        background:'linear-gradient(90deg,#FFDF35,#20DFFF)',borderRadius:8}}/>
    </div>
    <div style={{position:'absolute',bottom:40,left:64,fontSize:17,color:'#83C6D5'}}>
      SIGNED 32-BIT TIME • SYSTEMS VARY • UTC
    </div>
    {backgroundMusicPath?<Audio src={staticFile(backgroundMusicPath)} loop volume={backgroundMusicVolume}/>:null}
    {voiceClips.map(clip=>{
      const c=cues[clip.cueIndex];
      return c?<Sequence key={clip.cueIndex} from={c.startFrame} durationInFrames={c.endFrame-c.startFrame}>
        <Audio src={staticFile(clip.path)}/></Sequence>:null;
    })}
  </AbsoluteFill>;
};
