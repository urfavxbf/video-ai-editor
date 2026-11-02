import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import motions from '../../characters/8bit-host-motions.json';
import {PixelPoseCharacter,type HostSpriteAction} from './PixelPoseCharacter';

/**
 * Silent, original 33-motion host explainer/storyboard.
 * The demo motion presets are deliberately separate from the 33 registered source-video FX.
 * The narration displayed on screen is a script; no synthetic WAV or lip-sync is claimed.
 */
export const HOST_MOTION_SCENE_FRAMES=105;
export const HOST_MOTION_DEMO_FRAMES=motions.length*HOST_MOTION_SCENE_FRAMES;
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const interp=(a:number,b:number,t:number)=>a+(b-a)*t;
type Style=React.CSSProperties;
const motionStyle=(name:string,frame:number):Style=>{
 const p=clamp(frame/(HOST_MOTION_SCENE_FRAMES-1)),t=frame,osc=Math.sin;
 const eased=p*p*(3-2*p);
 switch(name){
 case 'fade-in':return {opacity:eased};
 case 'fade-out':return {opacity:1-eased};
 case 'slide-left':return {transform:`translateX(${interp(230,-180,eased)}px)`};
 case 'slide-right':return {transform:`translateX(${interp(-220,190,eased)}px)`};
 case 'slide-up':return {transform:`translateY(${interp(250,-110,eased)}px)`};
 case 'slide-down':return {transform:`translateY(${interp(-200,145,eased)}px)`};
 case 'zoom-in':return {transform:`scale(${interp(.45,1.45,eased)})`};
 case 'zoom-out':return {transform:`scale(${interp(1.45,.45,eased)})`};
 case 'bounce':return {transform:`translateY(${-150*Math.abs(osc(p*Math.PI*3))*(1-p)}px)`};
 case 'rotate':return {transform:`rotate(${eased*90}deg)`};
 case 'spin':return {transform:`rotate(${eased*720}deg)`};
 case 'flip-x':return {transform:`scaleX(${osc(p*Math.PI*2)>0?1:-1})`};
 case 'flip-y':return {transform:`scaleY(${osc(p*Math.PI*2)>0?1:-1})`};
 case 'shake':return {transform:`translateX(${(1-p)*osc(t*2.6)*21}px)`};
 case 'wobble':return {transform:`rotate(${osc(p*11*Math.PI)*(1-p)*20}deg)`};
 case 'pulse':return {transform:`scale(${1+.15*osc(p*Math.PI*8)} )`};
 case 'blink':return {opacity:Math.floor(t/13)%2===0?1:.14};
 case 'pop-up':return {transform:`translateY(${interp(220,0,eased)}px) scale(${interp(.35,1+0.12*osc(p*Math.PI*3)*(1-p),eased)})`,opacity:clamp(p*7)};
 case 'elastic':return {transform:`scaleY(${1+.35*osc(p*Math.PI*6)*(1-p)}) scaleX(${1-.22*osc(p*Math.PI*6)*(1-p)})`};
 case 'glitch':return {transform:`translateX(${Math.floor(t/4)%3===0?9:-7}px)`,filter:'contrast(1.6)'};
 case 'vhs':return {transform:`translateX(${osc(t*1.8)*3}px)`,filter:'contrast(1.22) saturate(.85)'};
 case 'rgb-split':return {filter:'contrast(1.25)'};
 case 'scanlines':return {filter:'contrast(1.3) brightness(.92)'};
 case 'pixelate':return {filter:`blur(${Math.round(2+6*Math.abs(osc(p*Math.PI)))}px)`};
 case 'mosaic':return {filter:`blur(${Math.round(8+10*Math.abs(osc(p*Math.PI)))}px) contrast(1.4)`};
 case 'motion-blur':return {transform:`translateX(${osc(p*7)*110}px)`,filter:`blur(${2+Math.abs(osc(p*7))*9}px)`};
 case 'speed-ramp':{
  const travel=p<.33?p*.3:p<.67?.1+(p-.33)*2.2:.85+(p-.67)*.45;
  return {transform:`translateX(${interp(-200,160,clamp(travel))}px)`};
 }
 case 'parallax':return {transform:`translateX(${osc(p*Math.PI*2)*45}px)`};
 case 'spotlight':return {filter:`brightness(${.42+.9*Math.abs(osc(p*Math.PI))})`};
 case 'sparkle':return {filter:`drop-shadow(0 0 ${6+10*Math.abs(osc(t*.35))}px #ffd44f)`};
 case 'smoke-puff':return {transform:`translateY(${-10*Math.abs(osc(p*3*Math.PI))}px)`};
 case 'fireworks':return {transform:`scale(${1+.06*Math.abs(osc(t*.17))})`};
 default:return {};
 }
};
const chromatic=['glitch','rgb-split'].includes.bind(null);
const Extras:React.FC<{id:string;f:number}> = ({id,f})=>{
 const p=clamp(f/(HOST_MOTION_SCENE_FRAMES-1));
 if(id==='glitch'||id==='rgb-split')return <AbsoluteFill style={{pointerEvents:'none'}}>
   {[-1,1].map((side)=><div key={side} style={{position:'absolute',left:0,top:0,width:'100%',height:'100%',
      transform:`translateX(${side*(8+Math.sin(f*.8)*7)}px)`,
      mixBlendMode:'screen',opacity:.25,filter:side<0?'sepia(1) saturate(9) hue-rotate(296deg)':'sepia(1) saturate(9) hue-rotate(130deg)'}}>
     <PixelPoseCharacter id="urfavxbf" speaking={false} hostAction="surprised" width={430} height={570} left={44} bottom={-14}/>
   </div>)}
 </AbsoluteFill>;
 if(id==='vhs'||id==='scanlines')return <AbsoluteFill style={{pointerEvents:'none',opacity:id==='vhs'?.32:.28,
    background:'repeating-linear-gradient(to bottom,transparent 0 7px,#091323 8px 11px)'}}/>;
 if(id==='sparkle'||id==='fireworks')return <AbsoluteFill style={{pointerEvents:'none'}}>
   {Array.from({length:id==='fireworks'?24:13},(_,i)=>{
     const x=40+(i*107)%440,y=28+(i*69)%480;
     const shine=Math.abs(Math.sin(f*.14+i));
     return <div key={i} style={{position:'absolute',left:x,top:y,width:3+shine*11,height:3+shine*11,
      background:i%3===0?'#ffce42':i%3===1?'#5fd7ff':'#f27ee6',
      transform:`rotate(45deg) translateY(${id==='fireworks'?-(p*80):0}px)`,
      opacity:shine}}/>;
   })}
 </AbsoluteFill>;
 if(id==='smoke-puff')return <AbsoluteFill style={{pointerEvents:'none'}}>
   {Array.from({length:8},(_,i)=><div key={i} style={{position:'absolute',width:40+i*7,height:40+i*7,borderRadius:'50%',
      background:'#c7d3e5aa',left:45+i*48,top:490-(i%2)*25-p*110,opacity:1-p}}/>)}
 </AbsoluteFill>;
 if(id==='spotlight')return <AbsoluteFill style={{pointerEvents:'none',
   background:'radial-gradient(ellipse at 50% 42%,transparent 10%,#040a1acc 73%)'}}/>;
 return null;
};
export const Host33MotionShowcase:React.FC=()=>{
 const frame=useCurrentFrame();
 const index=Math.min(motions.length-1,Math.floor(frame/HOST_MOTION_SCENE_FRAMES));
 const item=motions[index];
 const local=frame-index*HOST_MOTION_SCENE_FRAMES;
 const entrance=clamp(local/9);
 return <AbsoluteFill style={{background:'#071125',fontFamily:'Inter,Arial,sans-serif',color:'#f7f9ff',overflow:'hidden'}}>
  <AbsoluteFill style={{backgroundImage:'radial-gradient(ellipse at 65% 50%,#25467d55,transparent 65%)'}}/>
  <div style={{position:'absolute',left:74,top:54,fontSize:23,letterSpacing:4,fontWeight:700,color:'#91baff'}}>
    URFAVXBF  /  ORIGINAL 8-BIT SPRITE MOTION
  </div>
  <div style={{position:'absolute',left:68,top:136,fontSize:75,fontWeight:900}}>
    {String(index+1).padStart(2,'0')}  {item.title.toUpperCase()}
  </div>
  <div style={{position:'absolute',left:75,top:254,width:670,fontSize:33,lineHeight:1.35,
   opacity:entrance,color:'#e1eafc'}}>{item.id==='typewriter'?item.narration.slice(0,Math.floor(local/3)):item.narration}</div>
  <div style={{position:'absolute',left:105,top:355,width:600,height:610}}>
    <PixelPoseCharacter id="urfavxbf" speaking hostAction="talk" width={500} height={600} left={30} bottom={0} startFrame={index*HOST_MOTION_SCENE_FRAMES}/>
  </div>
  <div style={{position:'absolute',left:1040,top:284,width:550,height:620,
     border:'3px solid #4167a0',background:'#142442b8',overflow:'hidden',borderRadius:20}}>
    {item.id==='parallax'&&<>
      <div style={{position:'absolute',left:-150,top:115,width:700,height:300,
        background:'#3e5a94',clipPath:'polygon(0% 100%,17% 25%,34% 100%,56% 5%,88% 100%)',
        transform:`translateX(${Math.sin(local*.03)*22}px)`}}/>
      <div style={{position:'absolute',left:-150,top:280,width:720,height:200,
        background:'#506db3',clipPath:'polygon(0% 100%,25% 25%,44% 100%,70% 12%,100% 100%)',
        transform:`translateX(${Math.sin(local*.03)*49}px)`}}/>
    </>}
    <div style={{position:'absolute',left:0,bottom:0,width:'100%',height:'100%',
      transformOrigin:'50% 72%',...motionStyle(item.id,local)}}>
      <PixelPoseCharacter id="urfavxbf" speaking={false} hostAction={item.action as HostSpriteAction}
        startFrame={index*HOST_MOTION_SCENE_FRAMES} width={430} height={570} left={58} bottom={7}/>
    </div>
    <Extras id={item.id} f={local}/>
  </div>
  <div style={{position:'absolute',bottom:55,left:75,fontSize:20,letterSpacing:2,color:'#94a8ce'}}>
    ON-SCREEN SCRIPT ONLY  /  NO AUDIO TRACK ATTACHED
  </div>
  <div style={{position:'absolute',bottom:50,right:72,fontSize:25,color:'#aabedb'}}>
    {index+1} / {motions.length}
  </div>
 </AbsoluteFill>;
};
