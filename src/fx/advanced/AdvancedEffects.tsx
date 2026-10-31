import React from 'react';
import {AbsoluteFill, Audio, Easing, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {interpolatePath, evolvePath} from '@remotion/paths';
import {ARoll, Cutout, FX_H, FX_W, type FxEntry, type FxProps, clamp01} from '../shared';
import envelope from './reactive-envelope.json';

/** Local 30fps, 9:16 frame-driven cinematic effects; no hard-coded branding or HUDs. */
const lerp=(f:number,start:number,end:number)=>clamp01((f-start)/Math.max(1,end-start));
const ease=(n:number)=>Easing.inOut(Easing.cubic)(clamp01(n));
const noise=(n:number)=>{const x=Math.sin(n*127.1+18.27)*43758.5453;return x-Math.floor(x);};
const layer:React.CSSProperties={position:'absolute',inset:0,overflow:'hidden'};
const FullVideo=({from,style}:{from:number;style?:React.CSSProperties})=>
  <AbsoluteFill style={{...style,overflow:'hidden'}}><ARoll from={from}/></AbsoluteFill>;
const sprite=(from:number,style?:React.CSSProperties)=> <Cutout from={from} style={style}/>;
const shimmer=(progress:number,angle=30)=>({
  background:\`linear-gradient(\${angle}deg,transparent 15%,rgba(255,209,142,.0) 29%,rgba(255,144,56,.84) 51%,rgba(248,87,65,.38) 66%,transparent 80%)\`,
  transform:\`translateX(\${-1450+progress*2750}px)\`,mixBlendMode:'screen' as const,
});
export const RgbSplit:React.FC<FxProps>=({from})=>{
  const frame=useCurrentFrame();
  const burst=Math.sin(Math.PI*lerp(frame,5,42))**2;
  const offset=Math.round(37*burst*(.4+.6*Math.abs(Math.sin(frame*.65))));
  return <AbsoluteFill style={{background:'#03070b',overflow:'hidden'}}>
    <FullVideo from={from} style={{filter:\`contrast(\${1+burst*.28})\`}}/>
    {offset>0&&<>
      <AbsoluteFill style={{transform:\`translateX(\${-offset}px)\`,mixBlendMode:'screen',opacity:burst*.6,filter:'brightness(1.5) sepia(1) saturate(12) hue-rotate(305deg)'}}>{sprite(from)}</AbsoluteFill>
      <AbsoluteFill style={{transform:\`translateX(\${offset}px)\`,mixBlendMode:'screen',opacity:burst*.6,filter:'brightness(1.5) sepia(1) saturate(12) hue-rotate(135deg)'}}>{sprite(from)}</AbsoluteFill>
      {Array.from({length:7},(_,i)=><div key={i} style={{position:'absolute',left:0,top:(i*273+frame*23)%FX_H,width:FX_W,height:2+noise(i)*10,
       background:'rgba(152,255,229,.30)',opacity:burst}}/>)}
    </>}
  </AbsoluteFill>;
};
export const SpeedTrails:React.FC<FxProps>=({from})=>{
  const f=useCurrentFrame(),p=ease(lerp(f,4,35)),decay=1-ease(lerp(f,38,70));
  return <AbsoluteFill style={{overflow:'hidden'}}>
    <FullVideo from={from} style={{transform:\`scale(\${1+.09*p})\`}}/>
    {Array.from({length:8},(_,i)=><AbsoluteFill key={i} style={{opacity:(.34-i*.031)*p*decay,
      transform:\`translateX(\${-(i+1)*29*p}px) scale(\${1+i*.004})\`,
      filter:\`blur(\${i*1.1}px) brightness(1.6)\`,mixBlendMode:'screen'}}>
      {sprite(from)}
    </AbsoluteFill>)}
    {sprite(from,{transform:\`translateX(\${26*p*decay}px)\`})}
  </AbsoluteFill>;
};
export const FilmLightLeak:React.FC<FxProps>=({from})=>{
  const f=useCurrentFrame(),p=ease(lerp(f,0,62));
  return <AbsoluteFill style={{overflow:'hidden'}}>
    <ARoll from={from}/>
    <AbsoluteFill style={{...shimmer(p),opacity:.92}}/>
    <AbsoluteFill style={{background:\`radial-gradient(ellipse at \${p*118}% 35%,rgba(255,227,140,.68),transparent 52%)\`,
      mixBlendMode:'screen',opacity:.67}}/>
    <AbsoluteFill style={{background:'rgba(252,186,95,.18)',mixBlendMode:'screen',
      opacity:Math.sin(p*Math.PI)}}/>
  </AbsoluteFill>;
};
// Each shard retains the real tracked source image and moves with its own physically
// plausible displacement. This is original CSS compositing, not Remotion's newer WebGL shatter().
export const GlassShatter:React.FC<FxProps>=({from})=>{
  const f=useCurrentFrame(),t=ease(lerp(f,10,70));
  return <AbsoluteFill style={{overflow:'hidden',background:'#060e18'}}>
    <FullVideo from={from} style={{filter:'brightness(.35)'}}/>
    {Array.from({length:24},(_,i)=>{
      const col=i%4,row=Math.floor(i/4),x=col*270,y=row*320;
      const a=noise(i+9)*Math.PI*2,force=80+noise(i+28)*560;
      return <AbsoluteFill key={i} style={{
        clipPath:\`polygon(\${x}px \${y}px,\${x+270}px \${y}px,\${x+270}px \${y+320}px,\${x}px \${y+320}px)\`,
        transform:\`translate(\${Math.cos(a)*force*t}px,\${Math.sin(a)*force*t+480*t*t}px) rotate(\${(noise(i+44)-.5)*52*t}deg) scale(\${1-.31*t})\`,
        opacity:1-ease(lerp(f,49,76)),filter:\`drop-shadow(0 0 \${4+12*t}px #fff9)\`,
      }}>{sprite(from)}</AbsoluteFill>;
    })}
    <AbsoluteFill style={{background:'radial-gradient(circle at 50% 46%,#efffff 0%,transparent 38%)',
      opacity:Math.max(0,1-Math.abs(f-12)/7)*.75,mixBlendMode:'screen'}}/>
  </AbsoluteFill>;
};
export const LiquidDisplacement:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,3,68));
 const amount=(.015+.085*Math.sin(Math.PI*t)**2).toFixed(3);
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <svg width="0" height="0" style={{position:'absolute'}}>
    <defs><filter id="advanced-liquid" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency={amount} numOctaves={2} seed={4} result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale={90*Math.sin(Math.PI*t)**2}
        xChannelSelector="R" yChannelSelector="G"/>
    </filter></defs>
  </svg>
  <AbsoluteFill style={{filter:'url(#advanced-liquid)',transform:\`scale(\${1+.12*t})\`}}><ARoll from={from}/></AbsoluteFill>
  <AbsoluteFill style={{background:'linear-gradient(50deg,transparent 34%,#5cebc122 55%,transparent 71%)',mixBlendMode:'screen'}}/>
 </AbsoluteFill>;
};
export const PixelDissolve:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,8,65));
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <ARoll from={from}/>
  <AbsoluteFill style={{background:'#081224',opacity:t*.78}}/>
  {Array.from({length:192},(_,i)=>{
    const x=(i%12)*90,y=Math.floor(i/12)*120,r=noise(i+29);
    const active=clamp01((t-r)*5);
    return <div key={i} style={{position:'absolute',left:x+(noise(i+2)-.5)*130*active,
      top:y+(noise(i+4)-.5)*160*active,width:86,height:116,opacity:active*(1-t*.76),
      background:i%3===0?'#74f2c9':i%3===1?'#3d8cf8':'#c6b8ff',
      transform:\`rotate(\${noise(i+8)*72*active}deg) scale(\${1-.5*active})\`,
      mixBlendMode:'screen'}}/>
  })}
  <AbsoluteFill style={{opacity:1-t,filter:\`contrast(\${1+4*t})\`}}>{sprite(from)}</AbsoluteFill>
 </AbsoluteFill>;
};
export const WhipPanBlur:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),p=ease(lerp(f,15,55));
 const kick=Math.sin(Math.PI*p);
 return <AbsoluteFill style={{overflow:'hidden',background:'#030608'}}>
  <FullVideo from={from} style={{
    transform:\`translateX(\${-FX_W*p}px) scale(1.14)\`,
    filter:\`blur(\${kick*32}px)\`,
  }}/>
  <FullVideo from={from+24} style={{
    transform:\`translateX(\${FX_W*(1-p)}px) scale(1.14)\`,
    filter:\`blur(\${kick*32}px)\`,
  }}/>
  {Array.from({length:4},(_,i)=><div key={i} style={{position:'absolute',
    left:(i*315+p*1900)%1750-400,top:150+i*315,width:300,height:5,
    background:'#dbffff',opacity:kick*.42,filter:'blur(8px)'}}/>)}
 </AbsoluteFill>;
};
const MORPH_A='M 150 540 C 280 250 800 250 930 540 C 800 830 280 830 150 540 Z';
const MORPH_B='M 540 110 C 830 420 830 1150 540 1630 C 240 1150 240 420 540 110 Z';
export const SvgPathMorph:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,8,64));
 const d=interpolatePath(t,MORPH_A,MORPH_B);
 const draw=evolvePath(clamp01(f/35),d);
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <ARoll from={from}/>
  <AbsoluteFill style={{background:'#07112288'}}/>
  <svg width={FX_W} height={FX_H} viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
    <defs><linearGradient id="morph-gradient" x1="0" y1="0" x2="1" y2="1">
     <stop stopColor="#50ffe4" stopOpacity=".85"/><stop offset="1" stopColor="#8294ff" stopOpacity=".54"/>
    </linearGradient></defs>
    <path d={d} fill="url(#morph-gradient)" fillOpacity=".32" stroke="#e6fff8" strokeWidth={9}
      strokeDasharray={draw.strokeDasharray} strokeDashoffset={draw.strokeDashoffset}/>
  </svg>
  {sprite(from,{opacity:.9,filter:'drop-shadow(0 8px 30px #020b14)'})}
 </AbsoluteFill>;
};
export const ComicHalftone:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,7,30));
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <FullVideo from={from} style={{filter:\`grayscale(\${t*.25}) contrast(\${1+1.15*t}) saturate(1.5)\`}}/>
  <AbsoluteFill style={{opacity:t*.53,backgroundImage:'radial-gradient(circle,#091426 2px,transparent 2.5px)',
    backgroundSize:'13px 13px',mixBlendMode:'multiply',transform:\`scale(\${1+.02*t})\`}}/>
  <AbsoluteFill style={{opacity:t*.18,background:'#ffff66',mixBlendMode:'color-burn'}}/>
  {sprite(from,{filter:\`contrast(\${1+t*.45}) drop-shadow(\${Math.round(t*13)}px 9px 0 #090d1f)\`})}
 </AbsoluteFill>;
};
// SVG displacement map is an offline procedural shader-like transition. It does NOT
// bundle or claim a specific licensed third-party GL-Transitions GLSL shader.
export const ShaderPortal:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,8,65)),radius=25+t*1420;
 const warp=78*(1-t);
 return <AbsoluteFill style={{overflow:'hidden',background:'#050b17'}}>
  <svg width="0" height="0" style={{position:'absolute'}}>
   <defs><filter id="advanced-portal" x="-30%" y="-30%" width="160%" height="160%">
    <feTurbulence type="turbulence" baseFrequency="0.015" seed={18} numOctaves={2} result="warp"/>
    <feDisplacementMap in="SourceGraphic" in2="warp" scale={warp} xChannelSelector="R" yChannelSelector="B"/>
   </filter></defs>
  </svg>
  <FullVideo from={from} style={{filter:'brightness(.45)'}}/>
  <AbsoluteFill style={{clipPath:\`circle(\${radius}px at 52% 45%)\`,
    transform:\`scale(\${1.35-.35*t}) rotate(\${12*(1-t)}deg)\`,
    filter:'url(#advanced-portal)'}}>
     <ARoll from={from+14}/>
  </AbsoluteFill>
  <div style={{position:'absolute',left:'52%',top:'45%',height:radius*2,width:radius*2,
    transform:'translate(-50%,-50%)',borderRadius:'50%',
    boxShadow:\`0 0 \${120*(1-t)}px \${22*(1-t)}px #5ae9fff0, inset 0 0 50px #7bf7ffd4\`,
    border:\`\${Math.max(0,14*(1-t))}px solid #a2ffff\`,opacity:1-t}}/>
 </AbsoluteFill>;
};
export const FilmBurnReveal:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),t=ease(lerp(f,7,66));
 const inner=10+t*153;
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <FullVideo from={from} style={{filter:'sepia(.35) contrast(1.14) brightness(.8)'}}/>
  <AbsoluteFill style={{clipPath:\`circle(\${inner}% at 48% 50%)\`}}>
    <ARoll from={from+17}/>
  </AbsoluteFill>
  <AbsoluteFill style={{opacity:.64*(1-t),pointerEvents:'none',background:
   \`radial-gradient(circle at 48% 50%,transparent \${Math.max(0,inner-11)}%,rgba(255,245,161,.84) \${Math.max(0,inner-8)}%,rgba(245,90,23,.94) \${Math.max(0,inner-3)}%,transparent \${inner+3}%)\`,
   mixBlendMode:'screen'}}/>
  <AbsoluteFill style={{opacity:.19*(1-t),background:'linear-gradient(160deg,#eb4c20,transparent 55%)',mixBlendMode:'screen'}}/>
 </AbsoluteFill>;
};
export const AudioReactiveParticles:React.FC<FxProps>=({from})=>{
 const f=useCurrentFrame(),index=Math.min(f,envelope.length-1);
 const level=envelope[Math.max(0,index)]??0;
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <ARoll from={from}/>
  <AbsoluteFill style={{background:'#00121d',opacity:.30}}/>
  {Array.from({length:90},(_,i)=>{
    const a=noise(i+1)*Math.PI*2,r=110+noise(i+20)*420+(level*410);
    const x=FX_W/2+Math.cos(a+f*.013)*r;
    const y=FX_H*.50+Math.sin(a+f*.013)*r*1.4;
    const size=5+noise(i+70)*13+level*18;
    return <div key={i} style={{position:'absolute',left:x,top:y,width:size,height:size,borderRadius:'50%',
      opacity:Math.min(.9,.23+level*1.8),background:i%3===0?'#65fff1':i%3===1?'#60a5ff':'#e6a4ff',
      boxShadow:\`0 0 \${9+level*45}px \${2+level*12}px #60f3ff88\`,
    }}/>;
  })}
  {sprite(from,{filter:\`drop-shadow(0 0 \${10+level*70}px #8bfff2)\`})}
  <Audio src={staticFile('sample/advanced-reactive.wav')}/>
 </AbsoluteFill>;
};
export const FX_ADVANCED:FxEntry[]=[
 {id:'rgb-split',name:'RGB Split',duration:72,Component:RgbSplit},
 {id:'speed-trails',name:'Speed Trails',duration:75,Component:SpeedTrails},
 {id:'film-light-leak',name:'Film Light Leak',duration:72,Component:FilmLightLeak},
 {id:'glass-shatter',name:'Glass Shatter',duration:80,Component:GlassShatter},
 {id:'liquid-displacement',name:'Liquid Displacement',duration:75,Component:LiquidDisplacement},
 {id:'pixel-dissolve',name:'Pixel Dissolve',duration:75,Component:PixelDissolve},
 {id:'whip-pan-blur',name:'Whip Pan Blur',duration:70,Component:WhipPanBlur},
 {id:'svg-path-morph',name:'SVG Path Morph',duration:75,Component:SvgPathMorph},
 {id:'comic-halftone',name:'Comic Halftone',duration:72,Component:ComicHalftone},
 {id:'shader-portal',name:'Shader Portal',duration:75,Component:ShaderPortal},
 {id:'film-burn-reveal',name:'Film Burn Reveal',duration:75,Component:FilmBurnReveal},
 {id:'audio-reactive-particles',name:'Audio Reactive Particles',duration:120,Component:AudioReactiveParticles},
];
if(new Set(FX_ADVANCED.map(e=>e.id)).size!==12)throw new Error('Advanced effect catalog is not unique');
