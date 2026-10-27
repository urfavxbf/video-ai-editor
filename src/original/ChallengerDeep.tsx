import { Audio } from '@remotion/media';
import { AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';

export type ChallengerProps = {
  totalFrames: number;
  captions: {startFrame:number;endFrame:number;text:string}[];
  narrationAvailable: boolean;
};
const CYAN='#66e8fa', LIME='#e5ff89', WHITE='#f6fdff', BG='#020917';
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const parts=[
  {end:.18,head:'PAANO KUNG',sub:'BUMABA KA?',info:'SA PINAKAMALALIM NA KARAGATAN',color:LIME},
  {end:.34,head:'200 METRO',sub:'PAWALA ANG LIWANAG',info:'SUNLIGHT → TWILIGHT ZONE',color:CYAN},
  {end:.49,head:'1,000 METRO',sub:'PURONG DILIM',info:'APHOTIC ZONE',color:CYAN},
  {end:.66,head:'MAS MALALIM',sub:'MAS MATINDING PRESSURE',info:'+1 ATMOSPHERE / ~10 METRO',color:'#ff9b79'},
  {end:.85,head:'10,935 METRO',sub:'CHALLENGER DEEP',info:'HIGIT 1,000× ANG PRESSURE',color:LIME},
  {end:1.01,head:'MAY BUHAY PA',sub:'SA KADILIMAN',info:'MGA LIHIM NG KARAGATAN',color:CYAN},
];
const eased=(t:number)=>t*t*(3-2*t);
const Vessel=({frame,pressure}:{frame:number;pressure:number})=><svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
 <defs>
  <radialGradient id="hull"><stop offset="0" stopColor="#7492a8"/><stop offset=".6" stopColor="#244b60"/><stop offset="1" stopColor="#071825"/></radialGradient>
  <linearGradient id="lamp"><stop offset="0" stopColor="#8df7ff" stopOpacity=".26"/><stop offset="1" stopColor="#8df7ff" stopOpacity="0"/></linearGradient>
 </defs>
 <g transform={`translate(${520+Math.sin(frame*.018)*68} ${1020+Math.sin(frame*.06)*14}) rotate(${Math.sin(frame*.015)*3}) scale(${1-pressure*.09})`}>
  <path d="M120 -14 L660 -250 L660 250 Z" fill="url(#lamp)"/>
  <ellipse cx="0" cy="0" rx="175" ry="94" fill="url(#hull)" stroke="#8ca5b3" strokeWidth="12"/>
  <rect x="-47" y="-132" width="94" height="65" rx="13" fill="#28485a" stroke="#9ec3ce" strokeWidth="9"/>
  <circle cx="45" cy="-5" r="56" fill="#0097b8" stroke="#c5f7fc" strokeWidth="10"/>
  <circle cx="45" cy="-5" r="37" fill="#0a324d" stroke="#42a6c9" strokeWidth="5"/>
  <path d="M-176 -20 l-70 -47 v132 l70 -42" fill="#234655" stroke="#9ccbd4" strokeWidth="6"/>
  <circle cx="147" cy="-10" r="13" fill="#e6ffff"/>
 </g>
</svg>;

export const ChallengerDeep = ({totalFrames,captions,narrationAvailable}:ChallengerProps)=>{
 const frame=useCurrentFrame(), t=clamp(frame/Math.max(totalFrames,1));
 const idx=Math.max(0,parts.findIndex(p=>t<p.end)), phase=parts[idx], start=Math.round((idx?parts[idx-1].end:0)*totalFrames), end=Math.min(totalFrames,Math.round(phase.end*totalFrames));
 const textAlpha=interpolate(frame,[start,start+12,Math.max(start+13,end-12),end],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const up=spring({frame:frame-start,fps:30,config:{damping:20,stiffness:112}});
 const depth=Math.round(10935*eased(clamp((t-.06)/.79))), pressure=depth/10935;
 const caption=captions.find(c=>frame>=c.startFrame&&frame<c.endFrame);
 return <AbsoluteFill style={{background:BG,color:WHITE,fontFamily:"'Montserrat','Inter',sans-serif",overflow:'hidden'}}>
  <AbsoluteFill style={{background:`radial-gradient(ellipse at 52% ${16+(1-t)*12}%,#154b64 0%,#0b263c 30%,#030e1d 75%,#01050a 100%)`}}/>
  <AbsoluteFill style={{background:`linear-gradient(180deg,rgba(68,229,235,${.16*(1-t)}),transparent 58%)`}}/>
  {Array.from({length:65},(_,i)=>{
   const x=((i*7897)%1001+frame*(.11+i%4*.1))%1150-35;
   const y=((i*349)%1913+frame*(.25+i%5*.09))%1960;
   const radius=2+(i%3);
   return <div key={i} style={{position:'absolute',left:x,top:y,width:radius*2,height:radius*2,background:i%9===0?'#baffff':'#9cd3e6',opacity:.16+(i%5)*.10,borderRadius:'50%',boxShadow:i%9===0?'0 0 14px #4bfbff':'none'}}/>;
  })}
  <svg viewBox="0 0 1080 1920" width="1080" height="1920" style={{position:'absolute',inset:0,opacity:.54+.34*pressure}}>
   <defs>
    <linearGradient id="l"><stop stopColor="#020b15"/><stop offset="1" stopColor="#174253"/></linearGradient>
    <linearGradient id="r"><stop stopColor="#184153"/><stop offset="1" stopColor="#020a16"/></linearGradient>
   </defs>
   <path d={`M0 440 L94 500 L30 730 L198 ${850+frame%75} L145 1040 L273 1320 L184 1510 L345 1780 L320 1920 H0 Z`} fill="url(#l)" stroke="#49a1b3" strokeOpacity=".35" strokeWidth="7"/>
   <path d={`M1080 370 L930 580 L1008 670 L844 ${820+frame%65} L937 1100 L787 1250 L869 1490 L686 1690 L753 1920 H1080 Z`} fill="url(#r)" stroke="#49a1b3" strokeOpacity=".35" strokeWidth="7"/>
   <path d="M0 1830 Q200 1800 400 1860 T1080 1820 V1920 H0 Z" fill="#051725"/>
  </svg>
  {idx!==4 && <Vessel frame={frame} pressure={pressure}/>}
  {idx===4 && <div style={{position:'absolute',top:850,left:90,right:90,textAlign:'center',fontSize:165,fontWeight:950,color:LIME,textShadow:'0 0 85px #a8ff7f79'}}>10,935</div>}
  {idx===5 && Array.from({length:5},(_,i)=><div key={i} style={{position:'absolute',left:185+i*170,top:1060+Math.sin(i*2)*135+Math.sin(frame/15+i)*18,width:27,height:27,borderRadius:'50%',background:'#90ffe2',boxShadow:'0 0 55px 25px #64cbd05c',opacity:.7}}/>)}
  <div style={{position:'absolute',left:66,top:78,right:66,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
   <span style={{fontSize:26,fontWeight:900,letterSpacing:4,color:LIME}}>BAKIT NGA BA<span style={{color:WHITE}}>?</span></span>
   <span style={{fontSize:20,fontWeight:800,letterSpacing:3,color:'#b3c4c9'}}>DEEP OCEAN • 001</span>
  </div>
  <div style={{position:'absolute',top:141,left:66,right:66,height:2,background:'linear-gradient(90deg,#8defeb,transparent)'}}/>
  <div style={{position:'absolute',top:170,left:68,right:68,display:'flex',justifyContent:'space-between',fontSize:24,fontWeight:850,letterSpacing:3}}>
   <span style={{color:'#afc9cb'}}>OCEAN DESCENT</span><span style={{color:CYAN}}>{depth.toLocaleString('en-US')} M</span>
  </div>
  <div style={{position:'absolute',top:227,left:68,right:68,height:5,background:'#ffffff22'}}><div style={{height:5,width:`${depth/10935*100}%`,background:LIME}}/></div>
  <div style={{position:'absolute',top:290,left:65,right:65,opacity:textAlpha,transform:`translateY(${(1-up)*-65}px)`,textShadow:'0 6px 28px #000'}}>
   <div style={{fontSize:24,color:phase.color,letterSpacing:5,fontWeight:900,marginBottom:15}}>0{idx+1} / 06 — SCIENCE EXPLAINED</div>
   <div style={{fontSize:idx===4?114:102,letterSpacing:-3,fontWeight:950,lineHeight:1}}>{phase.head}</div>
   <div style={{fontSize:idx===3?58:68,letterSpacing:-1.4,fontWeight:950,lineHeight:1.19,color:phase.color}}>{phase.sub}</div>
   <div style={{display:'inline-block',padding:'12px 19px',fontSize:24,letterSpacing:2,marginTop:23,background:'#06101fdf',borderLeft:`5px solid ${phase.color}`}}>{phase.info}</div>
  </div>
  {idx===3 && <div style={{position:'absolute',top:1280,left:95,right:95,display:'flex',gap:14,alignItems:'end',height:240}}>
   {[1,2,3,4,5,6].map(i=><div key={i} style={{background:'linear-gradient(0deg,#ff9877,#f98d6044)',height:38+i*31,flex:1,boxShadow:'0 0 24px #ff987722'}}/>)}
  </div>}
  <div style={{position:'absolute',bottom:198,left:65,right:65,height:206,display:'flex',justifyContent:'center',alignItems:'center'}}>
   {caption && <div style={{fontSize:48,fontWeight:900,lineHeight:1.24,letterSpacing:-.5,textAlign:'center',padding:'15px 25px',background:'#020b16ef',border:'1px solid #87e6e74b',borderRadius:14,textShadow:'0 4px 10px black',boxShadow:'0 14px 45px #0009'}}>{caption.text}</div>}
  </div>
  <div style={{position:'absolute',left:65,right:65,bottom:126,display:'flex',justifyContent:'space-between',color:'#9bb6bd',fontSize:20,fontWeight:850,letterSpacing:2}}>
   <span>CHALLENGER DEEP / MARIANA TRENCH</span><span>0{idx+1} / 06</span>
  </div>
  <div style={{position:'absolute',left:65,right:65,bottom:97,height:6,background:'#ffffff26'}}><div style={{width:`${t*100}%`,height:6,background:LIME}}/></div>
  {narrationAvailable && <>
    <Audio src={staticFile('original/challenger/voiceover.mp3')} volume={1}/>
    <Audio src={staticFile('original/challenger/score.wav')} volume={.33}/>
  </>}
 </AbsoluteFill>;
};
