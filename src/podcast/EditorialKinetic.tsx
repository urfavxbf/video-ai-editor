import {Audio, Video} from '@remotion/media';
import type {CSSProperties} from 'react';
import {AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame} from 'remotion';
import {Sfx} from '../fx/sfx';

/**
 * Editorial / kinetic podcast shorts engine.
 *
 * NOTE: A beat's tokens are timed by a human or forced aligner, in seconds
 * relative to the beat's start. They must be checked against real narration
 * before publishing. This component never presents approximate timing as
 * automated transcription.
 *
 * All graphics are original. Supply only rights-cleared source video/audio.
 */
export type EditorialToken = {
  text: string;
  at: number;
  strong?: boolean;
};
export type EditorialBeat = {
  start: number;
  end: number;
  mode: 'speaker' | 'type';
  tokens: EditorialToken[];
  kicker?: string;
  mark?: 'circle' | 'underline' | 'strike';
};
export type EditorialKineticProps = {
  beats: EditorialBeat[];
  totalSeconds: number;
  videoPath?: string;
  audioPath?: string;
  sourceStartSeconds?: number;
  sourceLabel?: string;
  seriesLabel?: string;
  approximateTiming?: boolean;
};
export const EDITORIAL_FPS = 30;
const PAPER = '#f5f3ee';
const INK = '#11151d';
const RED = '#cf3b44';
const MUTED = '#787d87';
const FONT = "'Montserrat','Inter',sans-serif";
const clamp = (v: number) => Math.max(0, Math.min(1, v));

const Mark = ({kind, opacity}: {kind?: EditorialBeat['mark']; opacity: number}) => {
  if (!kind) return null;
  return <svg aria-hidden="true" viewBox="0 0 550 125" style={{
    position:'absolute',bottom:-56,left:'50%',width:570,height:145,
    transform:'translateX(-50%)',overflow:'visible',opacity,pointerEvents:'none',
  }}>
    {kind === 'circle' && <path d="M57 65 C100 13 426 -2 492 49 S438 116 251 111 S39 97 57 65"
      stroke={RED} strokeWidth={9} fill="none" strokeLinecap="round"/>}
    {kind === 'underline' && <path d="M36 75 Q236 99 512 57 M47 91 Q298 115 497 81"
      stroke={RED} strokeWidth={7} fill="none" strokeLinecap="round"/>}
    {kind === 'strike' && <path d="M28 69 Q240 44 531 73 M99 82 Q250 51 464 62"
      stroke={RED} strokeWidth={7} fill="none" strokeLinecap="round"/>}
  </svg>;
};

const CornerAccents = ({frame}: {frame: number}) => {
  const a = Math.sin(frame / 70) * 4;
  return <>
    <svg aria-hidden="true" viewBox="0 0 340 340" style={{
      position:'absolute',left:-80,top:-80,width:340,height:340,
      transform:'rotate(' + a + 'deg)',pointerEvents:'none',
    }}>
      {Array.from({length:11}, (_,i)=>{
        const theta=i*Math.PI*2/11;
        const x=170+Math.cos(theta)*105;
        const y=170+Math.sin(theta)*105;
        return <path key={i} d={'M170 170 L'+x+' '+y}
          stroke="#11151d" strokeWidth={13} strokeLinecap="round"/>;
      })}
      <circle cx={170} cy={170} r={36} fill={INK}/>
    </svg>
    <svg aria-hidden="true" viewBox="0 0 250 250" style={{
      position:'absolute',right:-55,bottom:180,width:250,height:250,
      transform:'rotate(' + (frame / 20) + 'deg)',pointerEvents:'none',
    }}>
      <path d="M125 0 L151 85 L250 125 L150 150 L125 250 L96 153 L0 125 L95 98 Z" fill={INK}/>
    </svg>
  </>;
};

const WaveMic = ({frame}: {frame: number}) => {
  const bob = Math.sin(frame / 19) * 8;
  return <div aria-hidden="true" style={{position:'absolute',top:245,left:220,width:640,height:820,
    transform:'translateY(' + bob + 'px)',pointerEvents:'none'}}>
    <div style={{position:'absolute',left:90,top:70,width:470,height:470,borderRadius:'50%',
      background:'radial-gradient(circle, #445968 0%, #202f3e 54%, #141e2a 72%)',
      boxShadow:'0 0 0 26px #ffffff10, 0 38px 90px #000a'}}/>
    <div style={{position:'absolute',left:258,top:135,width:135,height:288,
      borderRadius:90,background:'linear-gradient(130deg,#dde1df,#80949b 18%,#223443 56%,#99b3b1)',
      border:'7px solid #e6e8e2'}}/>
    {Array.from({length:8},(_,i)=><div key={i} style={{
      position:'absolute',left:277,top:184+i*27,width:97,height:5,borderRadius:6,
      background:'#101923',opacity:.63,
    }}/>)}
    <div style={{position:'absolute',left:211,top:301,width:226,height:190,border:'11px solid #ece8e0',
      borderTop:'none',borderRadius:'0 0 120px 120px'}}/>
    <div style={{position:'absolute',left:318,top:483,width:13,height:110,background:PAPER}}/>
    <div style={{position:'absolute',left:242,top:592,width:163,height:14,borderRadius:9,background:PAPER}}/>
  </div>;
};

const TimedWords = ({beat, elapsed, dark}: {
  beat: EditorialBeat;elapsed: number;dark: boolean;
}) => {
  const active = beat.tokens.reduce((idx,token,i) => elapsed >= token.at ? i : idx, -1);
  const showFrom = active < 0 ? 0 : Math.max(0, active - 4);
  const filtered = beat.tokens.filter((_,i) => i >= showFrom && i <= Math.max(0,active));
  return <div style={{display:'flex',alignItems:'baseline',justifyContent:'center',gap:'13px 17px',
    flexWrap:'wrap',maxWidth:'100%',position:'relative',lineHeight:1.24}}>
    {filtered.map((token,localIndex)=>{
      const index = showFrom + localIndex;
      const emphasis = token.strong || index === active;
      const springIn = spring({fps:EDITORIAL_FPS,
        frame:Math.max(0,Math.round((elapsed-token.at)*EDITORIAL_FPS)),
        config:{damping:20,stiffness:150,mass:.75}});
      const baseColor = dark ? PAPER : INK;
      return <span key={index} style={{
        display:'inline-block',
        fontSize:dark?(emphasis?64:54):(emphasis?80:68),
        fontWeight:emphasis?950:800,
        letterSpacing:emphasis?-2.8:-1.6,
        color:token.strong?RED:(index === active && !dark?RED:baseColor),
        opacity:index===active?1:(dark?.82:.7),
        transform:'translateY(' + ((1-springIn)*34) + 'px) scale(' + (.9+springIn*.1) + ')',
        textShadow:dark?'0 5px 20px #000b':'none',
      }}>{token.text}</span>;
    })}
  </div>;
};

export const EditorialKinetic = ({
  beats,totalSeconds,videoPath,audioPath,sourceStartSeconds=0,
  sourceLabel='PODCAST INTERVIEW',seriesLabel='EDITORIAL / ORIGINAL',
  approximateTiming=true,
}: EditorialKineticProps) => {
  const frame=useCurrentFrame();
  const t=frame/EDITORIAL_FPS;
  const beat=beats.find(b => t>=b.start && t<b.end) ?? beats[beats.length-1];
  const elapsed=clamp(t-beat.start);
  const fade=interpolate(t,[beat.start,beat.start+.2,Math.max(beat.start+.21,beat.end-.2),beat.end],
    [0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const speaker=beat.mode==='speaker';
  const dark=speaker;
  const videoSrc=videoPath?staticFile(videoPath):null;
  const audioSrc=audioPath?staticFile(audioPath):null;
  const rail:CSSProperties={position:'absolute',top:84,left:70,right:70,
    display:'flex',justifyContent:'space-between',fontFamily:FONT,fontSize:19,fontWeight:900,
    letterSpacing:2.7,color:dark?PAPER:INK,zIndex:5};
  const active=beat.tokens.reduce((idx,token,i)=>elapsed>=token.at?i:idx,-1);
  const annotationOpacity=active===beat.tokens.length-1 && t-beat.start>.12 ? fade : 0;
  return <AbsoluteFill style={{background:PAPER,color:INK,fontFamily:FONT,overflow:'hidden'}}>
    <AbsoluteFill style={{background:'radial-gradient(ellipse at center, #fffefa, #e9e8e4 90%)'}}/>
    {!speaker && <CornerAccents frame={frame}/>}
    {speaker && <AbsoluteFill style={{background:'radial-gradient(ellipse at 50% 30%, #314956, #10151f 72%)'}}/>}
    {/* Keep video mounted throughout the timeline to retain source synchronization. */}
    {videoSrc && <Video src={videoSrc} trimBefore={Math.round(sourceStartSeconds*EDITORIAL_FPS)}
      muted style={{position:'absolute',width:'100%',height:'100%',objectFit:'cover',
        opacity:speaker?1:0,transform:'scale(' + (1.03+Math.sin(frame/45)*.018) + ')'}}/>}
    {speaker && !videoSrc && <WaveMic frame={frame}/>}
    {speaker && <AbsoluteFill style={{background:'linear-gradient(180deg,#0008,transparent 24%,transparent 51%,#000c)',
      pointerEvents:'none'}}/>}
    <div style={rail}><span>{seriesLabel}</span><span>{sourceLabel}</span></div>
    {!speaker && <div style={{position:'absolute',top:480,left:64,right:64,
      fontSize:23,fontWeight:900,letterSpacing:4,textAlign:'center',color:MUTED}}>
      {beat.kicker ?? 'THE STORY'}
    </div>}
    <div style={{
      position:'absolute',left:65,right:65,
      top:speaker?1280:830,minHeight:speaker?175:250,
      zIndex:4,textAlign:'center',opacity:fade,
    }}>
      <TimedWords beat={beat} elapsed={elapsed} dark={dark}/>
      {!speaker && <Mark kind={beat.mark} opacity={annotationOpacity}/>}
    </div>
    <div style={{position:'absolute',bottom:140,left:65,right:65,zIndex:4,
      display:'flex',justifyContent:'space-between',fontSize:18,fontWeight:800,
      letterSpacing:1.5,color:dark?'#f5f3eeb2':MUTED}}>
      <span>{approximateTiming?'CAPTION TIMING • DRAFT':'FRAME-ALIGNED CAPTIONS'}</span>
      <span>{Math.floor(t).toString().padStart(2,'0')} / {Math.round(totalSeconds)}</span>
    </div>
    <div style={{position:'absolute',bottom:105,left:65,right:65,height:5,
      background:dark?'#ffffff3f':'#10131a2b',zIndex:4,borderRadius:5}}>
      <div style={{height:'100%',width:(clamp(t/totalSeconds)*100)+'%',background:RED,borderRadius:5}}/>
    </div>
    {audioSrc && <Audio src={audioSrc} volume={1}/>}
    <Sfx cues={beats.slice(1).filter(b=>b.mode==='type').map(b=>({
      at:Math.round(b.start*EDITORIAL_FPS),sound:'whip',volume:.09,
    }))}/>
  </AbsoluteFill>;
};
