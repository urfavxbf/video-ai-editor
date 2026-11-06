import React, {createContext, useContext} from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame} from 'remotion';
import {PixelPoseCharacter} from '../characters/PixelPoseCharacter';
import {performancePose, MATERIAL_EFFECT_IDS, type ShowreelPalette, type ShowreelShot} from './showreelTimeline';

export const PALETTES:Record<ShowreelPalette,{bg:string;fg:string;accent:string;muted:string}>= {
 ink:{bg:'#08090c',fg:'#f4f1e8',accent:'#baff39',muted:'#4d5555'},
 paper:{bg:'#eeeae0',fg:'#15151a',accent:'#5b3df5',muted:'#b6b3a9'},
 acid:{bg:'#baff39',fg:'#102016',accent:'#4d2be9',muted:'#78aa20'},
 violet:{bg:'#39209b',fg:'#f6f0e5',accent:'#aaff35',muted:'#7452c5'},
 cyan:{bg:'#b5e8e7',fg:'#152222',accent:'#5132d9',muted:'#79b9ba'},
};
export const PerformanceContext=createContext<{speaker:'urfavxbf'|'pix'|null;energy:number}>({speaker:null,energy:0});
export const ease=(f:number,at=0)=>spring({frame:Math.max(0,f-at),fps:30,config:{damping:22,stiffness:160,mass:.7}});
export const clamp=(n:number)=>Math.max(0,Math.min(1,n));
export const hash=(n:number)=>{const v=Math.sin(n*127.1+311.7)*43758.5453;return v-Math.floor(v);};
export const DISPLAY="'Montserrat',sans-serif";

export const ShowreelCharacters=({shot,hostOnly=false,pixOnly=false}:{shot:ShowreelShot;hostOnly?:boolean;pixOnly?:boolean})=>{
 const f=useCurrentFrame(), {speaker,energy}=useContext(PerformanceContext);
 const arrival=ease(f);
 return <AbsoluteFill style={{pointerEvents:'none'}}>
  <div style={{position:'absolute',left:930,top:820,width:840,height:80,borderRadius:'50%',background:'#0005',filter:'blur(25px)',transform:`scaleX(${.75+.25*arrival})`}}/>
  {!pixOnly&&<div style={{position:'absolute',inset:0,transform:`translate(${(1-arrival)*95}px,${-Math.sin(f/26)*7-energy*(speaker==='urfavxbf'?6:0)}px)`}}>
   <PixelPoseCharacter id="urfavxbf" speaking={speaker==='urfavxbf'} poseOverride={performancePose('urfavxbf',shot.index,f,speaker==='urfavxbf')} width={740} height={740} left={1000} bottom={94}/>
  </div>}
  {!hostOnly&&<div style={{position:'absolute',inset:0,transform:`translate(${(1-arrival)*180}px,${Math.sin(f/19)*8-energy*(speaker==='pix'?8:0)}px)`}}>
   <PixelPoseCharacter id="pix" speaking={speaker==='pix'} poseOverride={performancePose('pix',shot.index,f,speaker==='pix')} width={440} height={440} left={1430} bottom={72}/>
  </div>}
 </AbsoluteFill>;
};

export const isMaterialShot=(shot:ShowreelShot)=>MATERIAL_EFFECT_IDS.includes(shot.id);
/** A type sculpture is the source object during the abstract motion/light passage. */
export const ShowreelSubject=({shot}:{shot:ShowreelShot})=>{
 const f=useCurrentFrame(),c=PALETTES[shot.palette];
 if(!isMaterialShot(shot))return <ShowreelCharacters shot={shot}/>;
 const chrome=['film-light-leak','glass-shatter','liquid-glass'].includes(shot.id);
 const word=shot.id==='rgb-split'?'TYPE.':shot.id==='audio-reactive-particles'?'FEEL.':'MOVE.';
 return <AbsoluteFill style={{perspective:1400,pointerEvents:'none'}}>
  <div style={{position:'absolute',left:95,right:95,top:300,fontFamily:DISPLAY,fontSize:390,fontWeight:900,lineHeight:1,letterSpacing:-28,textAlign:'center',
   transform:`rotateY(${Math.sin(f/40)*9}deg) rotateX(${chrome?-8:0}deg) translateY(${(1-ease(f))*75}px)`,
   ...(chrome?{color:'transparent',background:'linear-gradient(115deg,#454c50 12%,#f7f1dc 28%,#707a81 38%,#fff 49%,#293238 61%,#d8e8f1 72%,#333 90%)',backgroundClip:'text',WebkitBackgroundClip:'text',filter:'drop-shadow(6px 7px 0 #4a5050) drop-shadow(0 18px 24px #0009)'}:{color:c.fg,textShadow:shot.palette==='ink'?'0 0 35px '+c.accent+'55':undefined})}}>{word}</div>
  {chrome&&<div style={{position:'absolute',left:95,right:95,top:689,fontFamily:DISPLAY,fontSize:390,fontWeight:900,lineHeight:1,letterSpacing:-28,textAlign:'center',color:'#d0d5ce',opacity:.13,transform:'scaleY(-1)',filter:'blur(3px)',maskImage:'linear-gradient(to bottom,transparent 28%,black)'}}>MOVE.</div>}
 </AbsoluteFill>;
};

export const ShowreelScene=({shot,hideCharacters=false,hideTitle=false}:{shot:ShowreelShot;hideCharacters?:boolean;hideTitle?:boolean})=>{
 const f=useCurrentFrame(),p=PALETTES[shot.palette],e=ease(f,2);
 const words=shot.title.split(' '), cut=words.length<=3?1:2;
 const lines=[words.slice(0,cut).join(' '),words.slice(cut).join(' ')].filter(Boolean);
 const dark=shot.palette==='ink'||shot.palette==='violet';
 const material=isMaterialShot(shot);
 return <AbsoluteFill style={{background:p.bg,color:p.fg,overflow:'hidden',fontFamily:DISPLAY,isolation:'isolate'}}>
  {dark&&<AbsoluteFill style={{background:`radial-gradient(ellipse at ${73+Math.sin(f/50)*8}% 62%,${shot.palette==='ink'?'#15352b':'#5a36c1'} 0%,transparent 62%)`}}/>}
  <div style={{position:'absolute',right:130,top:70,width:700,height:700,borderRadius:shot.index%3===0?'50%':'28%',border:`2px solid ${p.accent}`,opacity:.2,transform:`rotate(${shot.index*17+f*.35}deg) scale(${.8+.2*e})`}}/>
  <div style={{position:'absolute',width:1500,height:2,left:100,top:900,background:p.fg,opacity:.1}}/>
  <div style={{position:'absolute',right:-300,bottom:-400,width:1200,height:850,borderRadius:'50%',background:p.accent,opacity:dark?.075:.1,filter:'blur(80px)'}}/>
  {!hideTitle&&!material&&<div style={{position:'absolute',left:105,top:220,width:1110,zIndex:2,transform:`translateY(${(1-e)*70}px)`,opacity:e}}>
   {lines.map((line,i)=><div key={i} style={{fontSize:line.length>15?100:line.length>11?115:line.length>8?137:177,lineHeight:.98,fontWeight:900,letterSpacing:-8,marginBottom:15,
    color:i===1?p.accent:p.fg,textShadow:dark&&i===1?'0 0 70px '+p.accent+'22':undefined,transform:`translateX(${(1-ease(f,5+i*3))*-85}px)`}}>{line}</div>)}
   <div style={{width:90+150*clamp((f-8)/26),height:9,marginTop:38,background:p.accent}}/>
  </div>}
  {!hideCharacters&&<ShowreelSubject shot={shot}/>}
 </AbsoluteFill>;
};

export const ShowreelIntro=()=>{
 const f=useCurrentFrame();
 const typed='make it move.'.slice(0,Math.max(0,Math.floor((f-10)/3)));
 const e=ease(f,65);
 return <AbsoluteFill style={{background:'#08090c',color:'#f4f1e8',fontFamily:DISPLAY,overflow:'hidden'}}>
  <div style={{position:'absolute',left:110,top:445,fontSize:50,fontFamily:'monospace',opacity:1-clamp((f-62)/12)}}><span style={{color:'#baff39'}}>&gt; </span>{typed}<span style={{opacity:f%24<12?1:0}}>▌</span></div>
  <div style={{position:'absolute',left:105,top:225,fontSize:185,fontWeight:900,letterSpacing:-10,lineHeight:.95,opacity:e,transform:`translateY(${(1-e)*120}px)`}}>GIVE IDEAS<br/><span style={{color:'#baff39'}}>A PULSE.</span></div>
  <div style={{position:'absolute',right:80,top:340,width:500,height:500,borderRadius:'50%',border:'2px solid #baff39',boxShadow:'0 0 130px #baff3920',transform:`scale(${.1+e*.9})`,opacity:e}}/>
  <div style={{position:'absolute',left:115,bottom:110,fontSize:25,letterSpacing:6,opacity:ease(f,105)}}>URFAVXBF × PIX</div>
  <div style={{position:'absolute',width:1920,height:1080,background:'#baff39',transform:`translateX(${1920*(1-clamp((f-139)/10))}px)`,opacity:f>=139?1:0}}/>
 </AbsoluteFill>;
};

export const ShowreelOutro=()=>{
 const f=useCurrentFrame(),e=ease(f,8);
 const shot:ShowreelShot={id:'orbit',title:'',frames:150,at:0,palette:'ink',index:4};
 return <AbsoluteFill style={{background:'#08090c',color:'#f4f1e8',fontFamily:DISPLAY,overflow:'hidden'}}>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 80% 60%,#16453d55,transparent 60%)'}}/>
  <div style={{position:'absolute',left:110,top:260,fontSize:150,fontWeight:900,lineHeight:1,letterSpacing:-8,opacity:e,transform:`translateY(${(1-e)*75}px)`}}>VIDEO<br/><span style={{color:'#baff39'}}>AI EDITOR.</span></div>
  <div style={{position:'absolute',left:118,top:630,fontSize:31,letterSpacing:3,opacity:ease(f,30)}}>MAKE YOUR NEXT MOVE.</div>
  <ShowreelCharacters shot={shot}/>
  <div style={{position:'absolute',left:118,bottom:105,fontSize:23,color:'#a5a9a6',opacity:ease(f,55)}}>github.com/urfavxbf/video-ai-editor</div>
  <AbsoluteFill style={{background:'#08090c',opacity:clamp((f-135)/14)}}/>
 </AbsoluteFill>;
};
