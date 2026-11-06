import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {interpolatePath} from '@remotion/paths';
import {PALETTES, ShowreelScene, ShowreelSubject, clamp, ease, hash, DISPLAY} from './ShowreelScene';
import {type ShowreelShot, type ShowreelEffectId} from './showreelTimeline';

type Props={shot:ShowreelShot;energy:number};
const Fill=({children,style={}}:{children?:React.ReactNode;style?:React.CSSProperties})=><AbsoluteFill style={{overflow:'hidden',isolation:'isolate',...style}}>{children}</AbsoluteFill>;
const labels=['33 EFFECTS','2 CHARACTERS','13 POSES','2 VOICES'];
const steps=['WRITE THE IDEA','STAGE THE CHARACTERS','ADD THE MOTION','GIVE IT A VOICE','RENDER THE STORY'];

/** Native 1920×1080 variants: same effect IDs/roles, original full-frame character sources.
 * The original portrait implementations and their source contract are untouched.
 * Paths, particles and transforms are deterministic functions of the Remotion frame.
 */
export const ShowreelEffect=({shot,energy}:Props)=>{
 const f=useCurrentFrame(),p=clamp(f/(shot.frames-1)),e=ease(f),c=PALETTES[shot.palette];
 const base=<ShowreelScene shot={shot}/>;
 const characters=<ShowreelSubject shot={shot}/>;
 const titleless=<ShowreelScene shot={shot} hideTitle/>;
 const empty=<ShowreelScene shot={shot} hideCharacters/>;
 const card=(content:React.ReactNode,style:React.CSSProperties={})=><div key={typeof content==='string'?content:undefined} style={{position:'absolute',padding:'26px 34px',fontFamily:DISPLAY,fontWeight:800,color:c.fg,background:shot.palette==='paper'?'#ffffffc9':'#ffffff16',border:'1px solid '+c.fg+'40',backdropFilter:'blur(15px)',borderRadius:24,...style}}>{content}</div>;
 const body=(()=>{switch(shot.id){
  case 'snap-zoom': return <Fill style={{transform:`scale(${1+.2*Math.exp(-f/18)*Math.sin(f/5)})`,transformOrigin:'65% 48%'}}>{base}</Fill>;
  case 'digital-zoom':return <>{empty}<Fill style={{transform:`scale(${1+.5*p*p})`,transformOrigin:'72% 52%'}}>{characters}</Fill></>;
  case 'rgb-split':return <>{base}{[-1,1].map((d,i)=><Fill key={d} style={{opacity:.6*Math.sin(p*Math.PI),mixBlendMode:'screen',filter:`sepia(1) saturate(8) hue-rotate(${i?120:300}deg)`,transform:`translateX(${d*(10+35*Math.sin(f*.6)**2)}px)`}}>{characters}</Fill>)}{Array.from({length:6},(_,i)=><div key={i} style={{position:'absolute',left:0,top:(i*190+f*19)%1080,width:1920,height:3,background:c.accent,opacity:.2}}/>)}</>;
  case 'speed-trails':return <>{empty}{Array.from({length:4},(_,i)=><Fill key={i} style={{opacity:.42-i*.07,transform:`translateX(${-(i+1)*45*e}px)`,filter:'brightness(0) saturate(100%) invert(23%) sepia(100%) saturate(6000%) hue-rotate(240deg)'}}>{characters}</Fill>)}<Fill style={{transform:`translateX(${55*Math.sin(p*Math.PI)}px)`}}>{characters}</Fill></>;
  case 'whip-pan-blur':{
   const t=clamp((f-12)/32),q=t*t*(3-2*t);
   return <><Fill style={{transform:`translateX(${-1920*q}px)`,filter:`blur(${20*Math.sin(q*Math.PI)}px)`}}>{base}</Fill><Fill style={{transform:`translateX(${1920*(1-q)}px)`,filter:`blur(${20*Math.sin(q*Math.PI)}px)`}}><ShowreelScene shot={{...shot,palette:'acid'}}/></Fill></>;
  }
  case 'svg-path-morph':{
   const t=(1-Math.cos(p*Math.PI*2))/2;
   const d=interpolatePath(t,'M 500 130 C 1060 130 1060 950 500 950 C -60 950 -60 130 500 130 Z','M 500 150 C 1030 720 1030 720 500 920 C -30 720 -30 720 500 150 Z');
   return <>{titleless}<svg width="1920" height="1080" style={{position:'absolute',inset:0}}><path d={d} fill={c.accent} stroke={c.fg} strokeWidth={4} transform={`translate(160 0) rotate(${f*.5} 500 540)`}/>{Array.from({length:8},(_,i)=><circle key={i} cx={850+Math.cos(i*Math.PI/4+p*3)*200} cy={540+Math.sin(i*Math.PI/4+p*3)*200} r={12+20*Math.sin(p*Math.PI)} fill={c.bg}/>)}</svg>{characters}</>;
  }
  case 'liquid-displacement':
  case 'shader-portal':{
   const portal=shot.id==='shader-portal',uid='reel-'+shot.id;
   return <><svg width="0" height="0"><defs><filter id={uid} x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency={.006+.003*Math.sin(p*Math.PI)} numOctaves={2} seed={5} result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale={(portal?90:48)*Math.sin(p*Math.PI)} xChannelSelector="R" yChannelSelector="G"/></filter></defs></svg><Fill style={{filter:`url(#${uid})`,transform:'scale(1.035)'}}>{base}</Fill>{portal&&<div style={{position:'absolute',left:730,top:95,width:880,height:880,borderRadius:'50%',border:`${8+20*Math.sin(p*Math.PI)}px solid #baff39`,boxShadow:'0 0 100px #baff3966,inset 0 0 90px #86e8ff66',transform:`rotate(${f*2}deg) scale(${.3+.8*e})`,mixBlendMode:'screen'}}/>}</>;
  }
  case 'liquid-glass':return <>{base}<div style={{position:'absolute',left:700+550*p,top:180,width:520,height:520,borderRadius:'50%',border:'2px solid #fff9',background:'linear-gradient(135deg,#fff5,#fff0 45%,#fff2)',backdropFilter:'blur(4px) contrast(1.4)',boxShadow:'inset 0 0 60px #ffffff44,0 25px 90px #0004',transform:`scale(${.6+.4*e})`}}/></>;
  case 'zoom-portal':return <>{empty}<div style={{position:'absolute',inset:0,clipPath:`circle(${50+1350*e}px at 72% 54%)`,transform:`scale(${1.5-.5*e})`}}>{titleless}</div><div style={{position:'absolute',left:1000,top:230,width:620,height:620,borderRadius:'50%',border:'8px solid '+c.accent,opacity:1-p,transform:`scale(${.4+2.6*p})`}}/>{characters}</>;
  case 'zoom-through-cut':return <><Fill style={{transform:`scale(${1+2*p*p})`,opacity:1-clamp((p-.5)*3)}}>{base}</Fill><Fill style={{opacity:clamp((p-.45)*3),transform:`scale(${1.8-.8*clamp((p-.45)*2)})`}}><ShowreelScene shot={{...shot,palette:'violet'}}/></Fill></>;
  case 'green-screen':return <>{empty}<svg width="1920" height="1080" style={{position:'absolute',inset:0}}>{Array.from({length:7},(_,i)=><path key={i} d={`M -100 ${150+i*150} Q ${500+f*3} ${-100+i*140} 2100 ${200+i*90}`} fill="none" stroke={i%2?'#baff39':'#5132d9'} strokeWidth={70} opacity={.1+i*.05}/>)}</svg>{characters}</>;
  case 'orbit':return <>{base}{[0,1,2,3,4,5,6,7].map((i)=>{
   const a=i*Math.PI/4+f*.035,x=1350+Math.cos(a)*410,y=520+Math.sin(a)*165;
   return <div key={i} style={{position:'absolute',left:x-52,top:y-52,width:104,height:104,borderRadius:26,display:'flex',alignItems:'center',justifyContent:'center',background:i%2?'#baff39':'#eeece4',color:'#121b16',fontFamily:DISPLAY,fontSize:i===4?22:37,fontWeight:900,transform:`scale(${e*(.85+.2*Math.sin(a))}) rotate(${Math.sin(a)*8}deg)`,zIndex:Math.sin(a)>0?5:0,boxShadow:'0 18px 45px #0006'}}>{['✂','Aa','▶','CC','WAV','◇','↗','✦'][i]}</div>;
  })}<Fill style={{zIndex:3}}>{characters}</Fill></>;
  case 'frame-escape':return <>{empty}<div style={{position:'absolute',left:1060,top:220,width:540,height:590,border:'12px solid '+c.accent,transform:`perspective(1200px) rotateY(${-18+15*p}deg)`,borderRadius:20}}/><Fill style={{transform:`translateX(${-130*e}px) scale(${.9+.15*e})`,transformOrigin:'72% 75%'}}>{characters}</Fill></>;
  case 'frame-break':return <>{base}{[0,1,2,3].map(i=><div key={i} style={{position:'absolute',left:i%2?1900:-12,top:i<2?0:1068,width:1920,height:12,background:c.accent,transform:`translate(${(i%2?1:-1)*300*clamp((f-12)/35)}px,${(i<2?-1:1)*300*clamp((f-12)/35)}px) rotate(${(i-1.5)*p*18}deg)`}}/>)}<svg width="1920" height="1080" style={{position:'absolute',inset:0,opacity:1-clamp((f-15)/40)}}><path d="M 1300 490 L 1090 280 980 300 800 80 M 1300 490 L 1570 290 1690 320 1920 100 M 1300 490 L 1530 650 1580 930 1720 1080 M 1300 490 L 1080 720 900 790 760 1080" fill="none" stroke="#fff" strokeWidth={3} strokeDasharray={1800} strokeDashoffset={1800*(1-e)}/></svg></>;
  case 'paper-cutout':return <>{empty}<Fill style={{filter:'drop-shadow(9px 0 0 white) drop-shadow(-9px 0 0 white) drop-shadow(0 9px 0 white) drop-shadow(0 -9px 0 white) drop-shadow(18px 28px 0 #15151a40)',transform:`rotate(${-5+9*e}deg)`,transformOrigin:'72% 70%'}}>{characters}</Fill><div style={{position:'absolute',left:700,top:160,width:150,height:50,background:'#baa97e99',transform:'rotate(-18deg)'}}/></>;
  case 'comic-halftone':return <>{base}<Fill style={{backgroundImage:'radial-gradient(#09061a 2.3px,transparent 2.7px)',backgroundSize:'13px 13px',opacity:.23,mixBlendMode:'multiply'}}/><Fill style={{filter:`contrast(1.35) drop-shadow(15px 12px 0 #0c091c)`,transform:`rotate(${Math.sin(f/13)*2}deg)`}}>{characters}</Fill><div style={{position:'absolute',left:750,top:155,color:'#baff39',fontFamily:DISPLAY,fontWeight:900,fontSize:130,transform:`rotate(-12deg) scale(${e})`,textShadow:'7px 7px 0 #140a32'}}>POW!</div></>;
  case 'magazine-cover':return <>{titleless}<div style={{position:'absolute',left:95,top:100,fontFamily:DISPLAY,fontWeight:900,fontSize:220,letterSpacing:-15,color:c.accent,opacity:e}}>CHARACTER.</div><div style={{position:'absolute',left:120,top:400,fontFamily:DISPLAY,fontWeight:900,fontSize:84,lineHeight:1.05,width:680}}>BIG IDEAS.<br/>TINY PIXELS.<br/>REAL PERSONALITY.</div>{characters}<div style={{position:'absolute',left:125,top:760,fontFamily:DISPLAY,fontSize:25,letterSpacing:6}}>URFAVXBF × PIX / ORIGINAL ART</div></>;
  case 'broll-overlay':return <>{base}<div style={{position:'absolute',left:120,top:600,width:640,height:340,border:'6px solid '+c.accent,overflow:'hidden',transform:`translateY(${(1-e)*180}px) rotate(${-4*e}deg)`,boxShadow:'0 30px 100px #0007'}}><div style={{width:1920,height:1080,transform:'scale(.334)',transformOrigin:'0 0'}}><ShowreelScene shot={{...shot,palette:'paper',title:'ANOTHER PERSPECTIVE.'}}/></div></div></>;
  case 'phone-mockup':return <>{empty}<div style={{position:'absolute',left:1130,top:110,width:405,height:830,border:'15px solid #10171c',borderRadius:66,overflow:'hidden',background:'#39209b',boxShadow:'35px 45px 0 #15222220',transform:`perspective(1500px) rotateY(${-20+15*e}deg) rotate(${8-12*e}deg) translateY(${(1-e)*250}px)`}}><div style={{position:'absolute',left:120,top:12,width:130,height:28,background:'#10171c',borderRadius:20,zIndex:5}}/><div style={{position:'absolute',left:30,right:30,top:90,textAlign:'center',fontFamily:DISPLAY,fontWeight:900,fontSize:56,lineHeight:1,color:'#f5f1e8'}}>YOUR<br/><span style={{color:'#baff39'}}>STORY.</span></div><div style={{position:'absolute',left:-565,top:180,width:1920,height:1080,transform:'scale(.52)',transformOrigin:'0 0'}}>{characters}</div></div></>;
  case 'split':return <>{base}<div style={{position:'absolute',inset:0,clipPath:`polygon(0 0,${45+10*Math.sin(p*Math.PI)}% 0,${58+10*Math.sin(p*Math.PI)}% 100%,0 100%)`}}><ShowreelScene shot={{...shot,palette:'violet'}}/></div><svg width="1920" height="1080" style={{position:'absolute',inset:0}}><path d={`M ${1920*(.45+.1*Math.sin(p*Math.PI))} 0 L ${1920*(.58+.1*Math.sin(p*Math.PI))} 1080`} stroke="#baff39" strokeWidth={4}/></svg></>;
  case 'growth-curve':{
   const reveal=clamp((f-7)/40),counts=[6,7,21,12,33];
   return <>{titleless}<svg width="1920" height="1080" style={{position:'absolute',inset:0}}><path d="M 140 820 C 300 820 360 720 500 690 S 660 640 750 510 900 500 1040 290" fill="none" stroke="#baff39" strokeWidth={9} pathLength={1} strokeDasharray="1" strokeDashoffset={1-reveal}/>{counts.map((n,i)=><g key={i} opacity={clamp((reveal-i*.18)*5)}><circle cx={150+i*200} cy={820-i*i*32} r={9} fill="#baff39"/><text x={150+i*200} y={780-i*i*32} fill="#f4f1e8" fontSize="57" fontFamily={DISPLAY} fontWeight="900">{n}</text></g>)}</svg><div style={{position:'absolute',left:140,top:110,fontFamily:DISPLAY,fontWeight:900,fontSize:95,color:'#f4f1e8'}}>BUILDING BLOCKS.</div><div style={{position:'absolute',left:145,top:900,color:'#baff39',fontFamily:DISPLAY,fontSize:24}}>HOST POSES → PIX POSES → ORIGINAL FX → CINEMATIC FX → TOTAL FX</div>{characters}</>;
  }
  case 'glass-widgets':return <>{base}{labels.slice(0,3).map((label,i)=>card(label,{left:130+i*300,top:700-i*35,fontSize:32,transform:`translateY(${(1-ease(f,i*5))*140}px) rotate(${i*4-4}deg)`,opacity:ease(f,i*5)}))}</>;
  case 'checklist-pop':return <>{titleless}<div style={{position:'absolute',left:115,top:200,width:850}}>{labels.map((label,i)=><div key={label} style={{fontFamily:DISPLAY,fontSize:68,fontWeight:900,color:i%2?c.accent:c.fg,marginBottom:28,opacity:ease(f,i*8),transform:`translateX(${(1-ease(f,i*8))*-100}px)`}}><span style={{display:'inline-block',fontSize:43,verticalAlign:'middle',marginRight:30}}>✦</span>{label}</div>)}</div>{characters}</>;
  case 'checklist':return <>{titleless}<div style={{position:'absolute',left:120,top:175,width:900}}>{steps.map((label,i)=><div key={label} style={{display:'flex',gap:28,alignItems:'center',height:138,borderBottom:'1px solid '+c.fg+'33',fontFamily:DISPLAY,fontSize:40,fontWeight:800,color:c.fg,opacity:ease(f,i*9),transform:`translateY(${(1-ease(f,i*9))*55}px)`}}><span style={{color:c.accent,fontSize:38}}>✓</span>{label}</div>)}</div>{characters}</>;
  case 'checklist-tally':return <>{empty}<div style={{position:'absolute',left:130,top:600,display:'flex',gap:55}}>{[['33','EFFECTS'],['13','POSES'],['2','VOICES']].map(([n,label],i)=><div key={label} style={{fontFamily:DISPLAY,color:c.fg,opacity:ease(f,8+i*8),transform:`translateY(${(1-ease(f,8+i*8))*100}px)`}}><div style={{fontSize:136,fontWeight:900,letterSpacing:-8}}>{Math.round(Number(n)*clamp((f-8-i*8)/25))}</div><div style={{fontSize:21,fontWeight:800,letterSpacing:3}}>{label}</div></div>)}</div>{characters}</>;
  case 'headline-storm':{
   const text=['33 EFFECTS.','URFAVXBF.','PIX.','13 APPROVED POSES.','TWO DISTINCT VOICES.','ORIGINAL MOTION.','ONE CREATIVE REPO.'];
   return <>{titleless}{text.map((label,i)=><div key={label} style={{position:'absolute',left:85+(i%3)*55,top:105+i*115,padding:'15px 35px',background:i%2?c.accent:c.fg,color:i%2?c.bg:'#eeeae0',fontFamily:DISPLAY,fontSize:46,fontWeight:900,letterSpacing:-1,transform:`translateX(${(1-ease(f,i*5))*-1300}px) rotate(${(i%2?1:-1)*(2+i*.5)}deg)`,boxShadow:'0 10px 30px #0002'}}>{label}</div>)}{characters}</>;
  }
  case 'chat-takeover':return <>{titleless}{card(<><div style={{fontSize:23,letterSpacing:4,color:c.accent,marginBottom:30}}>THE IDEA</div><div style={{fontSize:52,lineHeight:1.2}}>“Give every idea<br/>a little character.”</div><div style={{height:2,background:'#fff3',margin:'35px 0'}}/><div style={{fontSize:39,color:c.accent,opacity:ease(f,30)}}>Let's make it move.<span style={{opacity:f%20<10?1:0}}> ▌</span></div></>,{left:115,top:240,width:820,transform:`translateY(${(1-e)*60}px)`,opacity:e})}{characters}</>;
  case 'film-light-leak':return <>{base}<Fill style={{background:'linear-gradient(100deg,transparent 15%,#ffcc4677 40%,#ff5a38aa 48%,#fff9cbaa 52%,transparent 68%)',mixBlendMode:'screen',transform:`translateX(${-1900+3700*p}px)`,filter:'blur(28px)'}}/><Fill style={{background:`radial-gradient(ellipse at ${p*130}% 45%,#ffd684bb,transparent 60%)`,mixBlendMode:'screen',opacity:.65*Math.sin(p*Math.PI)}}/></>;
  case 'glass-shatter':{
   const t=clamp((f-10)/40);
   return <>{empty}{Array.from({length:20},(_,i)=>{
    const x=(i%5)*384,y=Math.floor(i/5)*270,dx=(x-768)*t,dy=(y-400)*t+500*t*t;
    return <Fill key={i} style={{clipPath:`polygon(${x}px ${y}px,${x+384}px ${y}px,${x+384}px ${y+270}px,${x}px ${y+270}px)`,transform:`translate(${dx}px,${dy}px) rotate(${(hash(i)-.5)*55*t}deg)`,opacity:1-t*.9,filter:'drop-shadow(0 0 5px #a9e8ff)'}}>{base}</Fill>;
   })}<div style={{position:'absolute',left:100,top:420,fontFamily:DISPLAY,fontWeight:900,fontSize:180,color:'#baff39',opacity:clamp((t-.3)*3),letterSpacing:-9}}>RE:CREATE.</div></>;
  }
  case 'pixel-dissolve':{
   const t=clamp((f-8)/42);
   return <>{empty}<Fill style={{opacity:1-t,filter:`contrast(${1+t*2})`}}>{characters}</Fill>{Array.from({length:100},(_,i)=>{
    const r=hash(i+10),a=clamp((t-r*.65)*3),x=950+(i%10)*80,y=200+Math.floor(i/10)*70;
    return <div key={i} style={{position:'absolute',left:x+(hash(i+2)-.5)*600*a,top:y+(hash(i+4)-.5)*500*a,width:8+hash(i+8)*36,height:8+hash(i+8)*36,background:i%2?'#baff39':'#a7e9ff',opacity:a*(1-t*.6),transform:`rotate(${i*37+a*80}deg) scale(${1-a*.6})`}}/>;
   })}</>;
  }
  case 'film-burn-reveal':{
   const t=clamp((f-4)/48),x=-600+3200*t;
   return <>{base}<Fill style={{clipPath:`polygon(0 0,${Math.max(0,x)}px 0,${Math.max(0,x-200)}px 1080px,0 1080px)`}}><ShowreelScene shot={{...shot,palette:'paper'}}/></Fill><div style={{position:'absolute',left:x-160,top:-100,width:180,height:1400,background:'linear-gradient(90deg,transparent,#f76a21,#fff4b4,#fff,transparent)',transform:'rotate(11deg)',filter:'blur(18px)',mixBlendMode:'screen',opacity:Math.sin(t*Math.PI)}}/></>;
  }
  case 'audio-reactive-particles':return <>{base}<svg width="1920" height="1080" style={{position:'absolute',inset:0,mixBlendMode:'screen'}}>{Array.from({length:100},(_,i)=>{
   const a=i*Math.PI*2/100+f*.012, radius=240+hash(i)*180+energy*150;
   return <circle key={i} cx={1120+Math.cos(a)*radius*1.7} cy={540+Math.sin(a)*radius*.8} r={2+hash(i+1)*5+energy*5} fill={i%2?'#baff39':'#adf2ff'} opacity={.3+energy*.6}/>;
  })}<circle cx={1120} cy={540} r={230+energy*120} fill="none" stroke="#baff39" strokeWidth={1+energy*4} opacity=".5"/></svg></>;
  default: {const exhaustive:never=shot.id;throw new Error('Unimplemented showreel FX: '+exhaustive);}
 }})();
 return <Fill style={{background:c.bg}}>{body}</Fill>;
};

/** Compile-time exhaustiveness is supplemented by the registry/coverage regression test. */
export const LANDSCAPE_EFFECT_IDS:ShowreelEffectId[]=[
 'orbit','chat-takeover','frame-escape','snap-zoom','checklist-pop','headline-storm','zoom-portal','growth-curve','broll-overlay','paper-cutout','magazine-cover','liquid-glass','zoom-through-cut','green-screen','frame-break','digital-zoom','phone-mockup','checklist-tally','glass-widgets','checklist','split',
 'rgb-split','speed-trails','film-light-leak','glass-shatter','liquid-displacement','pixel-dissolve','whip-pan-blur','svg-path-morph','comic-halftone','shader-portal','film-burn-reveal','audio-reactive-particles',
];
