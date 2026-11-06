import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {ShowreelEffect} from './ShowreelEffects';
import {ShowreelIntro, ShowreelOutro, PerformanceContext, DISPLAY, clamp} from './ShowreelScene';
import {INTRO_FRAMES, OUTRO_FRAMES, SHOWREEL_SHOTS, SHOWREEL_FRAMES} from './showreelTimeline';
import audioManifest from './showreel-audio.json';

type Voice={file:string;character:'urfavxbf'|'pix';at:number;frames:number;text:string;envelope:number[]};
export type ShowreelProps={audioReady:boolean};
const audio=audioManifest as {ready:boolean;score:string;envelope:number[];voices:Voice[]};
const usePerformance=()=>{
 const frame=useCurrentFrame();
 const voice=audio.voices.find(v=>frame>=v.at&&frame<v.at+v.frames);
 return {speaker:voice?.character??null,energy:voice?.envelope[frame-voice.at]??0};
};
const Captions=()=>{
 const frame=useCurrentFrame();
 const voice=audio.voices.find(v=>frame>=v.at&&frame<v.at+v.frames);
 if(!voice)return null;
 return <div style={{position:'absolute',left:160,right:160,bottom:34,display:'flex',justifyContent:'center',zIndex:20}}>
  <div style={{padding:'13px 28px',borderRadius:14,background:'#08090cea',fontFamily:DISPLAY,fontSize:30,fontWeight:600,color:'#f6f2e9',textAlign:'center',maxWidth:1520,lineHeight:1.35,borderLeft:'4px solid '+(voice.character==='pix'?'#a7e9ff':'#baff39')}}>{voice.text}</div>
 </div>;
};
const Shot=({index}:{index:number})=>{
 const shot=SHOWREEL_SHOTS[index],frame=useCurrentFrame()+shot.at;
 return <ShowreelEffect shot={shot} energy={audio.envelope[frame]??0}/>;
};
const ShowreelSound=()=> <>
 <Audio src={staticFile(audio.score)} volume={f=>{
  const speaking=audio.voices.some(v=>f>=v.at-5&&f<v.at+v.frames+8);
  return (speaking?.25:.8)*clamp(f/30)*clamp((SHOWREEL_FRAMES-f)/35);
 }}/>
 {audio.voices.map(v=><Sequence key={v.file} from={v.at} durationInFrames={v.frames} name={v.character+' — '+v.text}>
  <Audio src={staticFile(v.file)} volume={.92}/>
 </Sequence>)}
</>;
/** Delivery mode requires the prepared real WAV manifest; silent preview remains explicit. */
export const CinematicShowreel=({audioReady}:ShowreelProps)=>{
 const performance=usePerformance();
 if(audioReady&&!audio.ready)throw new Error('Showreel narration is not prepared. Run python3 scripts/prepare_showreel.py first.');
 return <AbsoluteFill style={{background:'#08090c',overflow:'hidden'}}>
  <PerformanceContext.Provider value={performance}>
   <Sequence from={0} durationInFrames={INTRO_FRAMES} name="Make it move"><ShowreelIntro/></Sequence>
   {SHOWREEL_SHOTS.map((shot,index)=><Sequence key={shot.id} from={shot.at} durationInFrames={shot.frames} name={shot.id}><Shot index={index}/></Sequence>)}
   <Sequence from={SHOWREEL_FRAMES-OUTRO_FRAMES} durationInFrames={OUTRO_FRAMES} name="Make your next move"><ShowreelOutro/></Sequence>
  </PerformanceContext.Provider>
  {audioReady&&<><ShowreelSound/><Captions/></>}
 </AbsoluteFill>;
};
