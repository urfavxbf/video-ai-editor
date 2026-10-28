import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import episode from '../../episodes/youtube-automation-en.json';
import type {VoiceEvent} from '../characters/CharacterPuppet';

type Speaker='pix'|'urfavxbf';
type Cue={speaker:Speaker;chapter:string;title:string;stat:string;text:string};
type Timing={startFrame:number;endFrame:number};
type Clip={cueIndex:number;path:string};
export type YoutubeAutomationEnglishProps={
  assetsReady:boolean;
  timedCues?:Timing[];
  voiceClips?:Clip[];
  voiceEvents?:VoiceEvent[];
  totalFrames?:number;
  audioLanguage?:'en';
  audioEngine?:string;
  soundtrack?:string;
  soundtrackVolume?:number;
};
const CUES=episode.cues as Cue[];
const FPS=30;
const DEFAULT_TIMINGS:Timing[]=(()=>{
  let cursor=0;
  return CUES.map(c=>{const begin=cursor;cursor+=Math.max(115,Math.round((c.text.split(/\s+/).length/2.32+0.65)*FPS));
    return {startFrame:begin,endFrame:cursor};});
})();
export const YOUTUBE_AUTOMATION_DEFAULT_FRAMES=DEFAULT_TIMINGS[DEFAULT_TIMINGS.length-1].endFrame+24;
const GOLD='#FFE347', CYAN='#36E7FF', WHITE='#F4FEFF',BG='#040A16';
const lessonColor=(chapter:string)=>chapter==='HOW CREATORS EARN'?'#67FFD0':chapter==='THE REAL RULES'?'#FFDA47':chapter==='WHAT CAN GO WRONG'?'#FF6389':CYAN;
const highlights:Record<string,string[]>={
  'THE PROMISE':['CREATIVE WORK','SYSTEMS','REAL AUDIENCE'],
  'HOW IT WORKS':['RESEARCH','SCRIPT','VOICE','EDIT','ANALYTICS'],
  'HOW CREATORS EARN':['AD REVENUE','AFFILIATES','SPONSORS','PRODUCTS'],
  'THE REAL RULES':['500 SUBSCRIBERS','1,000 SUBSCRIBERS','FEB 2027'],
  'THE EARNINGS MATH':['100,000 / 1,000 = 100','100 × $2 = $200','MINUS COSTS'],
  'WHAT CAN GO WRONG':['REUSED CONTENT','COPYRIGHT','QUALITY'],
  'A NO-BUDGET PLAN':['WEEK ONE','WEEK TWO','WEEKS THREE + FOUR'],
  'FINAL TAKEAWAY':['ORIGINALITY','VALUE','ITERATION'],
};
const chip:React.CSSProperties={background:'rgba(5,19,36,.9)',padding:'12px 15px',borderRadius:10,fontSize:17,
  fontWeight:850,letterSpacing:1,border:'1px solid rgba(51,222,244,.5)'};
const HeadPortrait:React.FC<{id:Speaker;frame:number;voiceEvents:VoiceEvent[]}>=({id,frame,voiceEvents})=>{
  const isPix=id==='pix';
  const active=voiceEvents.find(e=>e.speaker===id&&frame>=e.startFrame&&frame<e.endFrame);
  const energy=active?active.rms[Math.min(active.rms.length-1,Math.max(0,Math.floor((frame-active.startFrame)*active.samplesPerSecond/FPS)))]??0:0;
  const talking=!!active&&energy>0.12&&(frame%7<5);
  const color=isPix?CYAN:GOLD;
  const bob=Math.sin(frame/15+(isPix?1.8:0))*4;
  return <div style={{position:'absolute',top:202,left:isPix?undefined:64,right:isPix?64:undefined,
    width:414,height:468,boxSizing:'border-box',border:'3px solid '+color,borderRadius:24,
    transform:'translateY('+bob+'px)',background:'#061522',overflow:'hidden',
    boxShadow:'0 0 '+(10+energy*27)+'px '+color+'77'}}>
    <div style={{position:'absolute',top:12,left:12,width:384,height:388,
      backgroundImage:'url('+staticFile('episodes/youtube-automation/'+id+'-atlas.png')+')',
      backgroundRepeat:'no-repeat',backgroundPosition:talking?'100% 0%':'0% 0%',
      backgroundSize:'200% 100%',imageRendering:'pixelated'}}/>
    <div style={{position:'absolute',bottom:0,width:'100%',height:61,
      background:'#020B19',color,display:'flex',alignItems:'center',justifyContent:'space-between',
      padding:'0 18px',boxSizing:'border-box',fontSize:24,fontWeight:900,letterSpacing:1}}>
      <span>{isPix?'PIX':'URFAVXBF'}</span>
      <div style={{display:'flex',height:27,alignItems:'flex-end',gap:5}}>
        {[0,1,2,3,4].map(n=><div key={n} style={{width:7,background:color,
          height:6+(active?Math.round(energy*20*Math.abs(Math.sin(frame/4+n))):0)}}/>)}
      </div>
    </div>
  </div>;
};

export const YoutubeAutomationEnglish:React.FC<YoutubeAutomationEnglishProps>=({
  assetsReady,voiceEvents=[],voiceClips=[],timedCues,totalFrames,soundtrack,soundtrackVolume=0.16,
})=>{
  const frame=useCurrentFrame();
  const timings=timedCues?.length===CUES.length?timedCues:DEFAULT_TIMINGS;
  let active=0;
  for(let i=0;i<timings.length;i++){if(frame>=timings[i].startFrame)active=i;else break;}
  const cue=CUES[active];
  const range=timings[active];
  const local=Math.max(0,frame-range.startFrame);
  const progress=Math.max(0,Math.min(1,local/Math.max(1,range.endFrame-range.startFrame)));
  const accent=cue.speaker==='pix'?CYAN:GOLD;
  const headingAccent=lessonColor(cue.chapter);
  const stats=highlights[cue.chapter]??[];
  const words=cue.text.split(/\s+/);
  const pages=Math.max(1,Math.ceil(words.length/10));
  const page=Math.min(pages-1,Math.floor(progress*pages));
  const caption=words.slice(page*10,page*10+10).join(' ');
  const panelScale=1+0.01*Math.sin(local/13);
  const total=totalFrames??YOUTUBE_AUTOMATION_DEFAULT_FRAMES;
  const iconPulse=0.5+0.5*Math.sin(local/12);
  const phase=cue.chapter==='THE EARNINGS MATH'?2:cue.chapter==='THE REAL RULES'?1:0;
  return <AbsoluteFill style={{background:'radial-gradient(ellipse at 48% 48%,#122A42,#071327 53%,#040A16 88%)',
    color:WHITE,fontFamily:'Arial, sans-serif',overflow:'hidden'}}>
    <AbsoluteFill style={{backgroundImage:'linear-gradient(rgba(40,213,237,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(40,213,237,.06) 1px,transparent 1px)',
      backgroundSize:'36px 36px',opacity:.8}}/>
    <AbsoluteFill style={{background:'linear-gradient(90deg,#FFDE3710,transparent 28%,transparent 72%,#26DDFF12)'}}/>
    <div style={{position:'absolute',left:0,top:0,width:1920,height:102,
      background:'rgba(2,10,23,.95)',borderBottom:'3px solid #27BFD8',
      display:'flex',justifyContent:'space-between',alignItems:'center',boxSizing:'border-box',padding:'0 56px'}}>
      <div style={{fontSize:34,fontWeight:1000,letterSpacing:1.3}}><span style={{color:GOLD}}>URFAVXBF</span>
        <span style={{padding:'0 19px',color:'#8DAFBF'}}>×</span><span style={{color:CYAN}}>PIX</span></div>
      <div style={{fontSize:23,fontWeight:900,letterSpacing:2}}>YOUTUBE AUTOMATION / EXPLAINED</div>
      <div style={{fontSize:18,color:'#8CCCDD',fontWeight:800}}>ORIGINAL ENGLISH DOCUMENTARY</div>
    </div>
    {assetsReady?<><HeadPortrait id="urfavxbf" frame={frame} voiceEvents={voiceEvents}/>
      <HeadPortrait id="pix" frame={frame} voiceEvents={voiceEvents}/></>:
    (['URFAVXBF','PIX'] as const).map((name,i)=><div key={name}
      style={{position:'absolute',top:202,left:i===0?64:undefined,right:i===1?64:undefined,
        width:414,height:468,borderRadius:25,border:'3px dashed '+(i===0?GOLD:CYAN),
        background:'rgba(2,9,19,.95)',boxSizing:'border-box',display:'flex',justifyContent:'center',
        alignItems:'center',textAlign:'center',padding:30,fontSize:26,fontWeight:900,
        color:i===0?GOLD:CYAN}}>STAGE APPROVED HEAD PORTRAIT<br/> {name}</div>)}
    <div style={{position:'absolute',top:139,left:520,width:880}}>
      <div style={{fontSize:18,letterSpacing:2,color:headingAccent,fontWeight:850}}>{cue.chapter}</div>
      <div style={{fontSize:35,fontWeight:950,marginTop:9,letterSpacing:.4}}>{cue.title}</div>
      <div style={{position:'relative',borderRadius:24,border:'2px solid #236A87',
        marginTop:25,padding:'34px 34px 30px',height:370,boxSizing:'border-box',overflow:'hidden',
        background:'linear-gradient(130deg,rgba(13,42,61,.98),rgba(3,14,31,.98))',
        boxShadow:'0 12px 36px #0008'}}>
        <div style={{fontSize:19,fontWeight:900,letterSpacing:2,color:'#A8DFE9'}}>MAIN IDEA / {String(active+1).padStart(2,'0')} OF {CUES.length}</div>
        <div style={{fontSize:44,fontWeight:1000,marginTop:35,letterSpacing:0.6,
          lineHeight:1.17,color:headingAccent,transform:'scale('+panelScale+')',transformOrigin:'left center',
          textShadow:'0 0 27px '+headingAccent+'33'}}>{cue.stat}</div>
        <div style={{display:'flex',gap:12,flexWrap:'wrap',marginTop:32}}>
          {stats.slice(0,4).map((text,i)=><div key={text}
            style={{...chip,opacity:interpolate(local,[i*8,i*8+10],[.1,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),
              color:i===phase?headingAccent:'#C7E8EF'}}>{text}</div>)}
        </div>
        <div style={{position:'absolute',bottom:27,left:34,right:34,height:9,borderRadius:7,background:'#14384A'}}>
          <div style={{width:(progress*100)+'%',height:'100%',borderRadius:7,
            background:'linear-gradient(90deg,'+GOLD+','+headingAccent+')'}}/>
        </div>
        <div style={{position:'absolute',top:25,right:29,width:13,height:13,borderRadius:12,
          background:headingAccent,opacity:iconPulse,boxShadow:'0 0 26px '+headingAccent}}/>
      </div>
      <div style={{marginTop:18,border:'2px solid '+accent,borderRadius:18,
        background:'rgba(2,12,28,.96)',padding:'15px 23px 20px',height:158,boxSizing:'border-box'}}>
        <div style={{color:accent,fontSize:18,fontWeight:950,letterSpacing:2}}>
          {cue.speaker==='pix'?'PIX / EMILY VOICE':'URFAVXBF / NATURAL STORYTELLER'}
        </div>
        <div style={{fontSize:29,fontWeight:800,lineHeight:1.35,marginTop:15}}>{caption}</div>
      </div>
    </div>
    <div style={{position:'absolute',bottom:44,left:64,fontSize:18,color:'#84C6D7',fontWeight:700}}>
      {cue.chapter.toUpperCase()} · ENGLISH · CHATTERBOX V3
    </div>
    <div style={{position:'absolute',bottom:20,left:64,right:64,height:9,borderRadius:8,background:'#15344A'}}>
      <div style={{width:(Math.min(100,frame/total*100))+'%',height:'100%',borderRadius:8,
        background:'linear-gradient(90deg,'+GOLD+','+CYAN+')'}}/>
    </div>
    {soundtrack?<Audio src={staticFile(soundtrack)} loop volume={soundtrackVolume}/>:null}
    {voiceClips.map(clip=>{
      const t=timings[clip.cueIndex];
      return t?<Sequence key={clip.cueIndex} from={t.startFrame} durationInFrames={t.endFrame-t.startFrame}>
        <Audio src={staticFile(clip.path)}/></Sequence>:null;
    })}
  </AbsoluteFill>;
};
