import React from 'react';
import { Audio } from '@remotion/media';
import { AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';

export const MOTION30_FRAMES = 900;
const LIME='#D9FF4B', CREAM='#F7F7ED', MUTE='#A0A6AA', BG='#080B10';
type MotionProps={includeNarration?:boolean;includeMusic?:boolean};
const op=(f:number,start:number)=>interpolate(f,[start,start+13,start+161,start+179],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
const pop=(f:number,start:number)=>spring({fps:30,frame:Math.max(0,f-start),config:{damping:19,stiffness:96}});
const Animated=({children,frame,at=0,style={}}:{children:React.ReactNode;frame:number;at?:number;style?:React.CSSProperties})=>{
 const p=pop(frame,at);
 return <div style={{opacity:p,transform:'translateY('+((1-p)*85)+'px) scale('+(0.94+p*0.06)+')',...style}}>{children}</div>;
};
const Eyebrow=({children}:{children:React.ReactNode})=><div style={{fontFamily:'Inter,sans-serif',fontSize:26,letterSpacing:7,fontWeight:700,color:MUTE,marginBottom:38}}>{children}</div>;
const Heading=({children,size=124,color=CREAM}:{children:React.ReactNode;size?:number;color?:string})=><div style={{fontFamily:'Montserrat,Inter,sans-serif',fontSize:size,fontWeight:900,lineHeight:1.0,letterSpacing:-7,color}}>{children}</div>;
const Frame=({children,frame,start}:{children:React.ReactNode;frame:number;start:number})=><AbsoluteFill style={{opacity:op(frame,start),background:BG,overflow:'hidden',color:CREAM}}>
 <AbsoluteFill style={{background:'radial-gradient(ellipse at 84% 20%, #243622 0%, transparent 50%), radial-gradient(ellipse at 10% 84%,#1C2029 0%,transparent 53%)'}}/>
 <AbsoluteFill style={{opacity:.27,backgroundImage:'linear-gradient(#FFFFFF12 1px, transparent 1px),linear-gradient(90deg,#FFFFFF12 1px,transparent 1px)',backgroundSize:'90px 90px',transform:'translateX('+(-frame%90)+'px)'}}/>
 <div style={{position:'absolute',top:95,left:89,right:89,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
 <span style={{fontFamily:'Inter',fontWeight:900,fontSize:29,letterSpacing:3}}>URFAV<span style={{color:LIME}}>X</span>BF</span>
 <span style={{fontFamily:'Inter',fontSize:22,letterSpacing:4,color:MUTE}}>MOTION / 001</span></div>
 <div style={{position:'absolute',bottom:112,left:90,right:90,height:2,background:'#FFFFFF30'}}/>
 <div style={{position:'absolute',bottom:112,left:90,width:(frame/900*900),height:3,background:LIME}}/>
 <div style={{position:'absolute',bottom:66,left:90,right:90,display:'flex',justifyContent:'space-between',fontFamily:'Inter',fontSize:20,letterSpacing:4,color:MUTE}}>
 <span>MAKE IT HAPPEN</span><span>{String(Math.min(30,Math.floor(frame/30))).padStart(2,'0')} / 30</span></div>
 {children}</AbsoluteFill>;

const SceneOne=({f}:{f:number})=><Frame frame={f} start={0}>
 <div style={{position:'absolute',top:456,left:84,right:60}}>
  <Animated frame={f} at={10}><Eyebrow>01 / A SIMPLE TRUTH</Eyebrow></Animated>
  <Animated frame={f} at={23}><Heading size={124}>PERFECT<br/>IS A<br/><span style={{color:LIME}}>TRAP.</span></Heading></Animated>
  <Animated frame={f} at={52}><div style={{fontFamily:'Inter',fontSize:37,color:MUTE,marginTop:66}}>Your next chapter starts when you move.</div></Animated>
 </div>
 <div style={{position:'absolute',left:615,top:1020,width:690,height:690,border:'5px solid '+LIME,borderRadius:'50%',opacity:.24,transform:'scale('+(0.8+f/900)+')'}}/>
</Frame>;

const SceneTwo=({f}:{f:number})=><Frame frame={f} start={180}>
 <div style={{position:'absolute',left:90,right:80,top:395}}>
  <Animated frame={f} at={193}><Eyebrow>02 / IT ONLY TAKES ONE</Eyebrow></Animated>
  <Animated frame={f} at={208}><Heading color={LIME} size={175}>ONE.</Heading></Animated>
  <Animated frame={f} at={224}><Heading size={102}>IDEA.<br/>DECISION.<br/>ACTION.</Heading></Animated>
  <Animated frame={f} at={249}><div style={{fontFamily:'Inter',fontSize:43,color:MUTE,marginTop:64}}>Small moves change everything.</div></Animated>
 </div>
 {Array.from({length:5},(_,i)=>{const p=pop(f,190+i*17);return <div key={i} style={{position:'absolute',left:95+i*186,top:1390,height:118,width:118,background:i===4?LIME:'#293627',border:'3px solid '+LIME,borderRadius:'50%',transform:'scale('+(0.3+p*.7)+')',opacity:p}}/>;})}
</Frame>;

const SceneThree=({f}:{f:number})=><Frame frame={f} start={360}>
 <div style={{position:'absolute',top:408,left:84,right:64}}>
  <Animated frame={f} at={374}><Eyebrow>03 / BUILD THE ENERGY</Eyebrow></Animated>
  <Animated frame={f} at={390}><Heading size={113}>MOTIVATION<br/><span style={{color:MUTE}}>FADES.</span></Heading></Animated>
  <Animated frame={f} at={422}><Heading size={127} color={LIME}>MOMENTUM<br/>BUILDS.</Heading></Animated>
 </div>
 <div style={{position:'absolute',left:90,right:90,top:1250}}>
 {Array.from({length:6},(_,i)=>{const p=interpolate(f,[389+i*17,478+i*9],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});return <div key={i} style={{height:13,marginBottom:22,background:'#30383A',borderRadius:15}}><div style={{height:'100%',width:(28+i*14)*p+'%',maxWidth:'100%',background:LIME,borderRadius:15}}/></div>;})}
 </div></Frame>;

const SceneFour=({f}:{f:number})=><Frame frame={f} start={540}>
 <div style={{position:'absolute',top:395,left:90,right:64}}>
  <Animated frame={f} at={555}><Eyebrow>04 / TRUST THE PROCESS</Eyebrow></Animated>
  <Animated frame={f} at={575}><Heading size={107}>YOU DON'T<br/>NEED THE<br/><span style={{color:LIME}}>WHOLE</span><br/>PATH.</Heading></Animated>
 </div>
 <svg width={895} height={430} viewBox="0 0 895 430" style={{position:'absolute',left:90,top:1180}}>
 <path d="M 45 354 C 260 354 210 79 430 84 S 635 360 860 42" fill="none" stroke="#FFFFFF55" strokeWidth="5" strokeDasharray="15 16"/>
 <path d="M 45 354 C 260 354 210 79 430 84 S 635 360 860 42" fill="none" stroke={LIME} strokeWidth="9" strokeLinecap="round" pathLength={1} strokeDasharray={(interpolate(f,[558,681],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}))+' 1'}/>
 <circle cx={45} cy={354} r={18} fill={LIME}/><circle cx={860} cy={42} r={19} fill={LIME} opacity={interpolate(f,[680,690],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}/></svg>
 <div style={{position:'absolute',bottom:247,left:90,fontFamily:'Inter',fontSize:37,color:MUTE}}>Take the first step.</div>
</Frame>;

const SceneFive=({f}:{f:number})=><Frame frame={f} start={720}>
 <div style={{position:'absolute',top:530,left:82,right:72}}>
  <Animated frame={f} at={733}><Eyebrow>05 / YOUR MOVE</Eyebrow></Animated>
  <Animated frame={f} at={751}><Heading size={201}>START.</Heading></Animated>
  <Animated frame={f} at={774}><Heading size={264} color={LIME}>NOW.</Heading></Animated>
  <Animated frame={f} at={797}><div style={{fontFamily:'Inter',fontSize:45,letterSpacing:1,marginTop:78}}>YOUR FUTURE IS WATCHING.</div></Animated>
 </div>
 <div style={{position:'absolute',top:1180,left:570,width:810,height:810,border:'4px solid '+LIME,borderRadius:'50%',opacity:.18,transform:'scale('+interpolate(f,[721,890],[.4,1.45],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})+')'}}/>
</Frame>;

export const Motion30=({includeNarration=false,includeMusic=false}:MotionProps)=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:BG}}>
  <SceneOne f={f}/><SceneTwo f={f}/><SceneThree f={f}/><SceneFour f={f}/><SceneFive f={f}/>
  {includeNarration&&<Audio src={staticFile('voiceovers/motion30.wav')} volume={1}/>}
  {includeMusic&&<Audio src={staticFile('voiceovers/motion30-bed.wav')} volume={0.28}/>}
 </AbsoluteFill>;
};
