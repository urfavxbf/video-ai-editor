import React from 'react';
import {AbsoluteFill,Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import performance from './performance.json';
import {GlitchHost,type HostPose} from './OwnerSheetHost';

export const WORD_POSE_FRAMES=performance.durationFrames;

const ActingStage:React.FC=()=>{
  const frame=useCurrentFrame();
  const index=performance.words.reduce((last,w,i)=>Math.round(w.startMs*30/1000)<=frame?i:last,-1);
  const word=performance.words[Math.max(0,index)];
  const previous=performance.words[Math.max(0,index-1)];
  const at=Math.round(word.startMs*30/1000);
  const phrase=performance.phrases.find(p=>frame>=Math.round(p.startMs*30/1000)&&frame<Math.round(p.endMs*30/1000)+10);
  const age=index<0?100:frame-at;
  const accent=word.pose==='surprised'?'#e43848':'#263d8d';
  return <AbsoluteFill style={{background:'#fff',color:'#171833',fontFamily:'Montserrat',overflow:'hidden'}}>
    <div style={{position:'absolute',left:110,top:155,fontSize:26,fontWeight:700,letterSpacing:6,color:accent}}>{index<6?'URFAVXBF':'A LITTLE CHARACTER.'}</div>
    <div style={{position:'absolute',left:100,top:290,width:820,fontSize:word.text.length>9?91:126,lineHeight:1.02,fontWeight:900,letterSpacing:-5,color:accent,translate:`0px ${age<5?(5-age)*2:0}px`}}>{index<0?'Hey!':word.text}</div>
    <div style={{position:'absolute',left:110,top:phrase&&phrase.wordCount>10?515:535,width:770,fontSize:43,lineHeight:1.45,fontWeight:600,letterSpacing:-1}}>
      {phrase?performance.words.slice(phrase.wordStart,phrase.wordStart+phrase.wordCount).map((w,i)=><React.Fragment key={i}><span style={{color:phrase.wordStart+i===index?accent:'#52566a',background:phrase.wordStart+i===index?'#ffdb62':'transparent',padding:'2px 2px'}}>{w.text}</span>{' '}</React.Fragment>):null}
    </div>
    <div style={{position:'absolute',left:114,top:855,width:105,height:10,background:'#e43848'}}/>
    <div style={{position:'absolute',left:234,top:855,width:55,height:10,background:'#263d8d'}}/>
    <div style={{position:'absolute',left:1080,bottom:180,width:620,height:700}}>
      <div style={{position:'absolute',left:90,right:90,bottom:-7,height:13,borderRadius:'50%',background:'#ededf4'}}/>
      <GlitchHost pose={word.pose as HostPose} previous={previous.pose as HostPose} age={age} seed={index+1}/>
    </div>
  </AbsoluteFill>;
};

export const WordPoseHostDemo:React.FC<{audioReady:boolean}>=({audioReady})=>{
  if(audioReady&&!performance.ready)throw new Error('Prepare real Jasper audio before delivery');
  return <><ActingStage/>{audioReady&&<Sequence name="Jasper · word-aligned performance"><Audio src={staticFile(performance.audio)}/></Sequence>}</>;
};
