import React from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import motions from '../../characters/8bit-host-motions.json';
import {PixelPoseCharacter} from './PixelPoseCharacter';

/**
 * 33 short, animated TYPOGRAPHY treatments in 39.6 seconds (30 fps).
 * Only the right-hand words receive FX. The 8-bit character is an unaffected presenter.
 * Speech comes from a real approved Chatterbox-generated WAV, when supplied.
 * This is a text-effect showcase, not a replacement for the editor's 33 video FX IDs.
 */
export const HOST_MOTION_SCENE_FRAMES = 36;
export const HOST_MOTION_DEMO_FRAMES = motions.length * HOST_MOTION_SCENE_FRAMES;
export const HOST_MOTION_DURATION_SECONDS = HOST_MOTION_DEMO_FRAMES / 30;
export type Host33MotionShowcaseProps = {voiceoverFile?: string};
type Style = React.CSSProperties;

const clamp = (n:number) => Math.max(0, Math.min(1, n));
const lerp = (a:number,b:number,p:number) => a + (b-a)*p;
const rnd = (n:number) => Math.round(n*100)/100;
const smooth = (n:number) => {const x=clamp(n); return x*x*(3-2*x);};

/** Every style is frame-deterministic for Remotion rendering. */
export const textMotionStyle = (effect:string,frame:number):Style => {
  const p=clamp(frame/(HOST_MOTION_SCENE_FRAMES-1));
  const e=smooth(p), s=Math.sin;
  switch(effect) {
    case 'fade-in': return {opacity:e};
    case 'fade-out': return {opacity:1-e};
    case 'slide-left': return {transform:`translateX(${rnd(lerp(360,0,e))}px)`};
    case 'slide-right': return {transform:`translateX(${rnd(lerp(-360,0,e))}px)`};
    case 'slide-up': return {transform:`translateY(${rnd(lerp(160,0,e))}px)`};
    case 'slide-down': return {transform:`translateY(${rnd(lerp(-160,0,e))}px)`};
    case 'zoom-in': return {transform:`scale(${rnd(lerp(.24,1.10,e))})`};
    case 'zoom-out': return {transform:`scale(${rnd(lerp(1.7,.72,e))})`};
    case 'bounce': return {transform:`translateY(${rnd(-125*Math.abs(s(p*3*Math.PI))*(1-p))}px)`};
    case 'rotate': return {transform:`rotate(${rnd(-30+e*30)}deg)`};
    case 'spin': return {transform:`rotate(${rnd(720*e)}deg)`};
    case 'flip-x': return {transform:`perspective(900px) rotateY(${rnd(180*e)}deg)`};
    case 'flip-y': return {transform:`perspective(900px) rotateX(${rnd(180*e)}deg)`};
    case 'shake': return {transform:`translateX(${rnd(s(frame*3.3)*24*(1-p))}px)`};
    case 'wobble': return {transform:`rotate(${rnd(s(p*9*Math.PI)*19*(1-p))}deg)`};
    case 'pulse': return {transform:`scale(${rnd(1+0.18*s(frame*.7))})`};
    case 'blink': return {opacity:frame%10<5?1:.08};
    case 'typewriter': return {};
    case 'pop-up': return {opacity:clamp(p*7),transform:`translateY(${rnd(lerp(220,0,e))}px) scale(${rnd(lerp(.4,1.04,e))})`};
    case 'elastic': return {transform:`scaleX(${rnd(1+.24*s(p*5*Math.PI)*(1-p))}) scaleY(${rnd(1-.3*s(p*5*Math.PI)*(1-p))})`};
    case 'glitch': return {transform:`translateX(${frame%7<3?12:-9}px)`,filter:'contrast(1.5)'};
    case 'vhs': return {transform:`translateX(${rnd(s(frame*1.9)*3)}px)`,filter:'saturate(.65) contrast(1.3)'};
    case 'rgb-split': return {filter:'contrast(1.2)'};
    case 'scanlines': return {filter:'contrast(1.4)'};
    case 'pixelate': return {filter:`blur(${rnd(lerp(0,3.2,e))}px) contrast(1.5)`};
    case 'mosaic': return {filter:`blur(${rnd(lerp(0,5,e))}px) contrast(1.9)`};
    case 'motion-blur': return {transform:`translateX(${rnd(150*s(p*2*Math.PI))}px)`,filter:`blur(${rnd(1+8*Math.abs(s(p*2*Math.PI)))}px)`};
    case 'speed-ramp': {
      const d=p<.38?p*.12:p<.67?.0456+(p-.38)*2.7:.8286+(p-.67)*.52;
      return {transform:`translateX(${rnd(lerp(-310,260,clamp(d)))}px)`};
    }
    case 'parallax': return {transform:`translateX(${rnd(s(p*2*Math.PI)*65)}px)`,textShadow:'-35px 18px #294882,25px -22px #4777c3'};
    case 'spotlight': return {filter:`brightness(${rnd(.45+.75*Math.abs(s(p*Math.PI)))} )`};
    case 'sparkle': return {filter:`drop-shadow(0 0 ${rnd(10+18*Math.abs(s(frame*.6)))}px #facc5c)`};
    case 'smoke-puff': return {opacity:clamp(p*5),transform:`translateY(${rnd(35*(1-e))}px)`};
    case 'fireworks': return {transform:`scale(${rnd(1+.09*Math.abs(s(frame*.55)))})`,filter:'drop-shadow(0 0 16px #ffd56e)'};
    default: throw new Error('Unknown text effect '+effect);
  }
};

const FxAccent:React.FC<{id:string;frame:number;title:string}> = ({id,frame,title}) => {
  const p=clamp(frame/(HOST_MOTION_SCENE_FRAMES-1));
  if(id==='glitch'||id==='rgb-split')return <AbsoluteFill style={{pointerEvents:'none'}}>
    {[-1,1].map((side)=><div key={side} aria-hidden style={{
      position:'absolute',inset:0,display:'flex',alignItems:'center',justifyContent:'center',
      fontFamily:'Inter,Arial,sans-serif',fontSize:117,fontWeight:950,letterSpacing:-3,
      color:side<0?'#ff37a0':'#27f6ff',opacity:.48,mixBlendMode:'screen',
      transform:`translateX(${side*(9+Math.sin(frame*1.2)*6)}px)`,
      clipPath:id==='glitch'?'inset(28% 0 28% 0)':'none',
    }}>{title.toUpperCase()}</div>)}
  </AbsoluteFill>;
  if(id==='scanlines'||id==='vhs')return <AbsoluteFill aria-hidden style={{
    pointerEvents:'none',opacity:.42,
    backgroundImage:'repeating-linear-gradient(to bottom,transparent 0 8px,#091021 9px 12px)',
    transform:id==='vhs'?`translateY(${frame%9}px)`:'none',
  }}/>;
  if(id==='sparkle'||id==='fireworks')return <AbsoluteFill aria-hidden style={{pointerEvents:'none'}}>
    {Array.from({length:id==='fireworks'?22:11},(_,i)=>{
      const glitter=.4+.6*Math.abs(Math.sin(frame*.54+i));
      return <div key={i} style={{
        position:'absolute',left:100+(i*197)%1000,top:40+(i*109)%380,
        width:6+glitter*20,height:6+glitter*20,opacity:glitter,
        background:i%2?'#74eaff':'#ffcf54',
        transform:`rotate(45deg) scale(${rnd(glitter)}) translateY(${id==='fireworks'?-p*65:0}px)`,
      }}/>;
    })}
  </AbsoluteFill>;
  if(id==='smoke-puff')return <AbsoluteFill aria-hidden style={{pointerEvents:'none'}}>
    {Array.from({length:11},(_,i)=><div key={i} style={{
      position:'absolute',left:80+i*105,top:250-(i%3)*28-p*85,
      width:42+i%4*14,height:42+i%4*14,borderRadius:'50%',
      background:'#a7bad8aa',opacity:1-p,filter:'blur(7px)',
    }}/>)}
  </AbsoluteFill>;
  if(id==='spotlight')return <AbsoluteFill aria-hidden style={{
    pointerEvents:'none',background:'radial-gradient(ellipse at 50% 50%,transparent 18%,#061129de 76%)',
  }}/>;
  if(id==='pixelate'||id==='mosaic')return <AbsoluteFill aria-hidden style={{pointerEvents:'none',opacity:p*.25,
    backgroundSize:id==='mosaic'?'32px 32px':'12px 12px',
    backgroundImage:'linear-gradient(90deg,#132f58 1px,transparent 1px),linear-gradient(#132f58 1px,transparent 1px)',
  }}/>;
  return null;
};

export const Host33MotionShowcase:React.FC<Host33MotionShowcaseProps>=({voiceoverFile}) => {
  const frame=useCurrentFrame();
  const index=Math.min(motions.length-1,Math.floor(frame/HOST_MOTION_SCENE_FRAMES));
  const item=motions[index];
  const local=frame-index*HOST_MOTION_SCENE_FRAMES;
  const progress=clamp(local/(HOST_MOTION_SCENE_FRAMES-1));
  const entrance=clamp(local/4), exit=clamp((HOST_MOTION_SCENE_FRAMES-local)/5);
  const title=item.id==='typewriter'?item.title.slice(0,Math.max(0,Math.floor(progress*(item.title.length+1)))):item.title;
  if(voiceoverFile&&!/^narration\/[a-z0-9][a-z0-9-_]*\.wav$/i.test(voiceoverFile))
    throw new Error('Voiceover file must be a local verified narration WAV');
  return <AbsoluteFill style={{
    overflow:'hidden',background:'#081328',fontFamily:'Inter,Arial,sans-serif',color:'#f6f8ff',
  }}>
    <AbsoluteFill style={{backgroundImage:'radial-gradient(ellipse at 80% 51%,#263f7455,transparent 65%)'}}/>
    <div style={{position:'absolute',top:56,left:90,color:'#93bbfd',letterSpacing:4,fontSize:23,fontWeight:800}}>
      URFAVXBF / 8-BIT HOST
    </div>
    <div style={{position:'absolute',top:110,left:88,fontWeight:900,fontSize:58,lineHeight:1.1}}>
      33 TEXT EFFECTS <span style={{color:'#ffd461'}}>IN 40 SECONDS</span>
    </div>
    <div style={{position:'absolute',top:210,left:100,color:'#a5b5d1',fontSize:27,maxWidth:415,lineHeight:1.4}}>
      The words move. The presenter stays put.
    </div>
    <div style={{position:'absolute',left:65,bottom:58,width:545,height:720}}>
      <PixelPoseCharacter id="urfavxbf" speaking hostAction="talk"
        width={525} height={710} left={10} bottom={0} startFrame={index*HOST_MOTION_SCENE_FRAMES}/>
    </div>
    <div style={{position:'absolute',left:605,top:258,width:1200,height:595,
      overflow:'hidden',border:'3px solid #3b5988',borderRadius:24,
      background:'#0f2343cc',boxShadow:'0 26px 72px #03081488'}}>
      <div style={{position:'absolute',left:44,top:26,color:'#91baf8',fontSize:24,letterSpacing:3,fontWeight:800}}>
        {String(index+1).padStart(2,'0')} / 33
      </div>
      <div style={{position:'absolute',top:72,left:12,right:12,bottom:85,
        display:'flex',alignItems:'center',justifyContent:'center',
        opacity:entrance*exit,...textMotionStyle(item.id,local),
        transformOrigin:'50% 50%',willChange:'transform,opacity,filter'}}>
        <span style={{fontSize:item.title.length>13?85:item.title.length>9?100:118,
          fontWeight:950,letterSpacing:-3,lineHeight:1.05,textAlign:'center',
          color:'#f6faff',textShadow:'0 8px 22px #071225cc'}}>
          {title.toUpperCase()}
        </span>
      </div>
      <FxAccent id={item.id} frame={local} title={item.title}/>
      <div style={{position:'absolute',left:46,right:40,bottom:35,textAlign:'center',
        opacity:entrance*exit,color:'#b6c9e9',fontSize:25,fontWeight:600}}>
        {item.narration}
      </div>
    </div>
    <div style={{position:'absolute',left:605,right:116,bottom:92,height:6,
      background:'#253858',borderRadius:4,overflow:'hidden'}}>
      <div style={{height:'100%',width:`${((index+progress)/motions.length)*100}%`,background:'#ffc84a'}}/>
    </div>
    {local<3&&index>0&&<AbsoluteFill style={{pointerEvents:'none',opacity:(3-local)*.1,
      background:'#86b7ff'}}/>}
    {voiceoverFile&&<Audio src={staticFile(voiceoverFile)} volume={.94}/>}
  </AbsoluteFill>;
};
