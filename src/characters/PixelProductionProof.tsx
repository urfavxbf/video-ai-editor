import React from 'react';
import {AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
import {PixelPoseCharacter} from './PixelPoseCharacter';

/** 12-second, 16:9, zero-credits visual smoke test. No fake narration. */
export type PixelProductionProofProps={assetsReady:boolean};
export const PIXEL_PROOF_FRAMES=360;
const SHOTS=[
  {headline:'TWO CHARACTERS.',sub:'ONE STORY.',host:'idle',pix:'idle',accent:'#6ffb8b'},
  {headline:'FOLLOW THE IDEA',sub:'NOT THE TEMPLATE',host:'point_side',pix:'question',accent:'#70e8ff'},
  {headline:'WAIT. WHAT?!',sub:'REACTIONS THAT MATTER',host:'surprised',pix:'surprised',accent:'#f588d9'},
  {headline:'TURN IDEAS',sub:'INTO VIDEOS',host:'talk',pix:'happy',accent:'#6ffb8b'},
] as const;
export const PixelProductionProof:React.FC<PixelProductionProofProps>=({assetsReady})=>{
 const frame=useCurrentFrame();
 if(!assetsReady)throw new Error('13 verified pixel PNG binaries required before PixelProductionProof render (no legacy fallback)');
 const shotIndex=Math.min(SHOTS.length-1,Math.floor(frame/90));
 const shot=SHOTS[shotIndex];
 const beat=frame%90;
 const camera=interpolate(beat,[0,89],[0,1.6]);
 const glitch=beat<7?(7-beat)/7:0;
 const opacity=interpolate(beat,[0,12,78,89],[0,1,1,.95],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const offset=Math.round(glitch*Math.sin(frame*11)*24);
 return <AbsoluteFill style={{
   background:'#060b15',fontFamily:'Arial,sans-serif',color:'#f5f9fc',
   overflow:'hidden',
 }}>
  <AbsoluteFill style={{backgroundImage:
   'radial-gradient(ellipse at 18% 68%,#20472b70,transparent 45%),radial-gradient(ellipse at 83% 30%,#123a5360,transparent 50%),linear-gradient(125deg,#070d16,#0c1522 58%,#080c16)'}}/>
  <div style={{position:'absolute',inset:0,opacity:.36,
    backgroundSize:'90px 90px',
    backgroundImage:'linear-gradient(#69a6aa16 1px,transparent 1px),linear-gradient(90deg,#69a6aa16 1px,transparent 1px)',
    transform:`translateX(${camera*4}px)`}}/>
  <div style={{position:'absolute',right:200,top:125,width:550,height:335,
     background:'linear-gradient(150deg,#122738,#061422)',
     boxShadow:'0 0 100px #2bbdff24,0 22px 60px #0009',
     border:'12px solid #172531',borderRadius:18,transform:`perspective(1000px) rotateY(-10deg) translateX(${-camera*9}px)`}}>
    <div style={{height:5,background:shot.accent,opacity:.8}}/>
    <div style={{margin:28,color:shot.accent,fontSize:28,fontWeight:800,letterSpacing:4}}>PIXEL STUDIO</div>
    <div style={{margin:'0 26px',height:2,background:'#2b5061'}}/>
    {Array.from({length:7},(_,i)=><div key={i} style={{margin:'15px 32px',height:10,
      width:150+(i%4)*70,background:i%3===0?shot.accent:'#1b6273',opacity:.15+i*.075}}/>)}
  </div>
  <div style={{position:'absolute',left:0,right:0,bottom:0,height:175,
    background:'linear-gradient(#152024,#071116)',boxShadow:'0 -18px 90px #0d455228'}}/>
  <div style={{position:'absolute',left:150,top:65,fontSize:20,letterSpacing:8,color:'#8fa9b9'}}>
    URFAVXBF × PIX  /  CHARACTER PROOF
  </div>
  <PixelPoseCharacter id="urfavxbf" speaking={shotIndex===3}
    poseOverride={shot.host} width={680} height={775} left={60} bottom={110}/>
  <PixelPoseCharacter id="pix" speaking={false}
    poseOverride={shot.pix} width={470} height={525} right={46} bottom={105}/>
  <div style={{position:'absolute',left:650,top:570,width:850,opacity,
    transform:`translateX(${offset}px) translateY(${Math.max(0,15-beat)*1.3}px)`}}>
    <div style={{fontSize:92,fontWeight:950,letterSpacing:-3,lineHeight:.98,
      textShadow:glitch?'5px 2px #16d9fa,-6px -2px #e24ef6':'0 12px 35px #000a'}}>
      {shot.headline}
    </div>
    <div style={{marginTop:18,fontSize:43,color:shot.accent,fontWeight:900,letterSpacing:3}}>{shot.sub}</div>
    <div style={{marginTop:22,fontSize:17,letterSpacing:4,color:'#9fb7c5'}}>
      REAL POSES   •   GLITCH TRANSITIONS   •   16:9
    </div>
  </div>
  {glitch>0&&<AbsoluteFill style={{opacity:glitch*.72,pointerEvents:'none'}}>
    {Array.from({length:9},(_,i)=><div key={i} style={{position:'absolute',
      top:(i*139+frame*23)%1080,left:0,width:'100%',height:2+i%4,
      background:i%2?'#23f3e5':'#d43cfa',transform:`translateX(${offset*(i%2?-1:1)}px)`}}/>)}
    <div style={{position:'absolute',top:(frame*59)%1080,width:'100%',height:21,
      background:'#fafcff',opacity:.30}}/>
  </AbsoluteFill>}
 </AbsoluteFill>;
};
