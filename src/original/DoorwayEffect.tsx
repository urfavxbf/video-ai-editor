import { Audio } from '@remotion/media';
import {
  AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame,
} from 'remotion';

export type OriginalCaption = { startFrame: number; endFrame: number; text: string };
export type DoorwayProps = {
  totalFrames: number;
  captions: OriginalCaption[];
  narrationAvailable: boolean;
};

const FPS = 30;
const BG = '#060b11';
const IVORY = '#f8f5ec';
const NEON = '#d5ff58';
const CYAN = '#62e3ed';
const ORANGE = '#ff876d';
const FONT = "'Montserrat','Inter',sans-serif";
const clamp = (n:number) => Math.max(0,Math.min(1,n));

const reveal = (frame:number,at:number) => spring({
  frame:frame-at, fps:FPS, config:{damping:19,stiffness:145,mass:.78},
});
const opacity = (f:number, a:number,b:number) =>
  interpolate(f,[a,a+11,b-11,b],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});

const phases = [
  {start:0,end:.17,tag:'01 / RELATABLE',line1:'BAKIT KA',line2:'NABLANGKO?',sub:'May kukunin ka sana...',accent:NEON},
  {start:.17,end:.32,tag:'02 / THE MOMENT',line1:'BIGLANG',line2:'NAWALA.',sub:'Isang hakbang. Nakalimutan.',accent:ORANGE},
  {start:.32,end:.51,tag:'03 / SCIENCE',line1:'DOORWAY',line2:'EFFECT.',sub:'Kapag nagpapalit ng lugar...',accent:CYAN},
  {start:.51,end:.69,tag:'04 / YOUR BRAIN',line1:'BAGONG',line2:'EKSENA.',sub:'Nagbabago ang konteksto.',accent:NEON},
  {start:.69,end:.83,tag:'05 / IMPORTANT',line1:'HINDI',line2:'PALAGI.',sub:'Iba-iba ang resulta ng pag-aaral.',accent:ORANGE},
  {start:.83,end:1.01,tag:'06 / TRY THIS',line1:'BALIK',line2:'KA MUNA.',sub:'Baka maalala mo ang pakay mo.',accent:CYAN},
];

const Doorway = ({f,frameStart,accent,scale=1}:{f:number;frameStart:number;accent:string;scale?:number}) => {
  const local = Math.max(0,f-frameStart);
  const turn = interpolate(local,[0,24,78,110],[-11,-8,-61,-70],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const glow = .55+.25*Math.sin(f/13);
  return <div style={{position:'absolute',left:105,top:445,width:860,height:895,perspective:1300,transform:'scale('+scale+')'}}>
    <div style={{position:'absolute',left:90,top:50,width:670,height:800,
      background:'radial-gradient(ellipse,#e8f1fd 0%,#7aeee9 17%,#0b3c50 58%,#0b1724 100%)',
      filter:'drop-shadow(0 0 70px '+accent+')',opacity:glow,
      border:'15px solid rgba(212,248,234,.72)',boxShadow:'0 0 100px rgba(104,229,216,.28) inset',
    }}/>
    <div style={{position:'absolute',left:92,top:45,width:662,height:810,
      transformOrigin:'left center',
      transform:'rotateY('+turn+'deg)',
      background:'linear-gradient(115deg,#34404b 0%,#101720 18%,#25343b 47%,#0b1118 100%)',
      border:'22px solid #65747a',boxShadow:'20px 32px 65px rgba(0,0,0,.92)',
    }}>
      <div style={{position:'absolute',inset:38,border:'7px solid #52636c',boxShadow:'0 0 25px rgba(0,0,0,.9) inset'}}/>
      <div style={{position:'absolute',top:300,right:45,width:30,height:30,borderRadius:'50%',background:accent,boxShadow:'0 0 35px '+accent}}/>
    </div>
    {Array.from({length:19},(_,i)=>{
      const x=(i*71+f*1.3)%840;
      const y=(i*93+f*.65)%800;
      return <div key={i} style={{position:'absolute',left:x,top:y,width:4+(i%3)*2,height:4+(i%3)*2,borderRadius:15,background:accent,opacity:.30+(i%4)*.12,filter:'blur(1px)'}}/>;
    })}
  </div>;
};

const BrainCircuit = ({f,accent}:{f:number,accent:string}) => (
 <div style={{position:'absolute',left:95,top:490,width:900,height:800}}>
  <svg width="900" height="800" viewBox="0 0 900 800">
    <defs>
      <radialGradient id="brainCore"><stop offset="0%" stopColor="#dffeff"/><stop offset="45%" stopColor="#48c4cd"/><stop offset="100%" stopColor="#102b40"/></radialGradient>
      <filter id="glow"><feGaussianBlur stdDeviation="13"/></filter>
    </defs>
    <circle cx="455" cy="390" r={230+Math.sin(f/13)*11} fill="#30cfd3" opacity=".14" filter="url(#glow)"/>
    <circle cx="455" cy="390" r="225" fill="url(#brainCore)" opacity=".28" stroke={accent} strokeWidth="5"/>
    {Array.from({length:9},(_,i)=>{
      const a=(i*40+f*.65)*Math.PI/180;
      const b=(i*40+f*.65+100)*Math.PI/180;
      const x=455+225*Math.cos(a),y=390+220*Math.sin(a);
      const x2=455+178*Math.cos(b),y2=390+175*Math.sin(b);
      return <g key={i}>
       <line x1={x} y1={y} x2={x2} y2={y2} stroke={i%2?accent:CYAN} strokeWidth="3" opacity=".72"/>
       <circle cx={x} cy={y} r={i%3===0?20:12} fill={accent} opacity=".85"/>
      </g>;
    })}
    <path d="M360 345 Q330 250 430 235 Q515 205 553 280 Q660 267 643 380 Q690 470 555 516 Q490 590 427 520 Q312 552 308 437 Q257 370 360 345" fill="none" stroke={IVORY} strokeWidth="8" opacity=".83"/>
    <path d="M450 234 Q420 320 475 372 Q410 416 435 515 M340 347 Q410 348 440 400 M556 282 Q502 335 536 409 Q575 450 552 515" fill="none" stroke={accent} strokeWidth="7" opacity=".84"/>
    <text x="455" y="720" fill={IVORY} fontSize="33" textAnchor="middle" letterSpacing="9" fontWeight="800">EVENT BOUNDARIES</text>
  </svg>
 </div>
);

const Fragment = ({f,accent}:{f:number;accent:string}) => (
  <div style={{position:'absolute',left:42,top:490,width:995,height:820,overflow:'hidden'}}>
    {Array.from({length:16},(_,i)=>{
      const x=50+(i%4)*238;
      const y=70+Math.floor(i/4)*167;
      const drift= Math.sin(f/17+i*1.7)*32;
      const rot = (i%2?1:-1)*(12+(f%95)*.14);
      return <div key={i} style={{
        position:'absolute',left:x+drift,top:y+(f%90)*.20,width:160,height:114,
        border:'2px solid '+(i%3===0?accent:'rgba(250,250,250,.24)'),
        background:i%4===0?'rgba(255,135,109,.15)':'rgba(109,180,193,.1)',
        transform:'rotate('+rot+'deg)',borderRadius:14,
        boxShadow:'0 12px 35px rgba(0,0,0,.5)'
      }}>
        <div style={{position:'absolute',top:25,left:20,right:20,height:9,background:accent,opacity:.35}}/>
        <div style={{position:'absolute',top:53,left:20,width:62,height:9,background:IVORY,opacity:.28}}/>
      </div>;
    })}
    <div style={{position:'absolute',top:280,left:80,right:80,textAlign:'center',fontSize:142,
      fontWeight:900,letterSpacing:1,color:accent,textShadow:'0 0 65px rgba(0,0,0,.98)',
      transform:'scale('+(1+.05*Math.sin(f/9))+')'}}>???</div>
  </div>
);

export const DoorwayEffect = ({totalFrames,captions,narrationAvailable}:DoorwayProps) => {
  const frame=useCurrentFrame();
  const total=Math.max(1,totalFrames);
  const pct=frame/total;
  const idx=phases.findIndex(p=>pct>=p.start && pct<p.end);
  const pi=Math.max(0,idx);
  const phase=phases[pi];
  const start=Math.round(phase.start*total);
  const end=Math.min(total,Math.round(phase.end*total));
  const anim=reveal(frame,start);
  const sceneAlpha=opacity(frame,start,end);
  const caption=captions.find(c=>frame>=c.startFrame && frame<c.endFrame);
  const captionStart=caption?.startFrame??frame;
  const emphatic = /DOORWAY|BAKIT|NAKALIMUTAN|BALIK|UTAK/i.test(caption?.text??'');
  const barOffset=(frame%90)/90;

  return <AbsoluteFill style={{background:BG,color:IVORY,fontFamily:FONT,overflow:'hidden'}}>
    <AbsoluteFill style={{
       background:'radial-gradient(ellipse at '+(35+Math.sin(frame/45)*12)+'% 40%, #23393b 0%, #0b1720 45%, #04090f 92%)'
    }}/>
    <AbsoluteFill style={{opacity:.22,
      backgroundImage:'linear-gradient(rgba(235,255,240,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(235,255,240,.09) 1px,transparent 1px)',
      backgroundSize:'92px 92px',
      transform:'translate('+(frame*.27%92)+'px,'+(frame*.2%92)+'px)',
    }}/>
    <div style={{position:'absolute',top:78,left:62,right:62,display:'flex',alignItems:'center',
      justifyContent:'space-between',fontSize:24,fontWeight:900,letterSpacing:4}}>
      <span style={{color:NEON}}>BAKIT NGA BA<span style={{color:IVORY}}>?</span></span>
      <span style={{color:'#9bafb3',fontWeight:650,letterSpacing:3,fontSize:20}}>ORIGINAL • 001</span>
    </div>
    <div style={{position:'absolute',top:142,left:62,right:62,height:2,background:'linear-gradient(90deg,'+NEON+',transparent)'}}/>
    {pi===0 && <Doorway f={frame} frameStart={start} accent={phase.accent}/>}
    {pi===1 && <Fragment f={frame} accent={phase.accent}/>}
    {pi===2 && <Doorway f={frame} frameStart={start} accent={CYAN} scale={.97}/>}
    {pi===3 && <BrainCircuit f={frame} accent={NEON}/>}
    {pi===4 && <div style={{position:'absolute',top:550,left:45,right:45,height:600,
      border:'13px solid '+ORANGE,borderRadius:280,transform:'rotate('+(frame*.12)+'deg)',
      boxShadow:'0 0 120px rgba(255,135,109,.2),0 0 60px rgba(255,135,109,.25) inset'}}>
      <div style={{textAlign:'center',position:'absolute',left:0,right:0,top:110,fontSize:280,fontWeight:900,color:ORANGE,transform:'rotate(-'+(frame*.12)+'deg)'}}>!</div>
    </div>}
    {pi===5 && <div style={{position:'absolute',top:480,left:60,right:60,height:770}}>
      {[0,1,2,3].map(i=><div key={i} style={{position:'absolute',left:115+i*16,top:70+i*108,
        fontSize:145,color:i%2===0?CYAN:NEON,fontWeight:900,
        textShadow:'0 0 55px rgba(98,227,237,.5)',
        opacity:1-i*.18,
        transform:'translateX('+Math.sin(frame/8+i)*20+'px)'}}>↶</div>)}
      <div style={{position:'absolute',right:44,top:240,background:'rgba(0,0,0,.55)',
        border:'3px solid '+CYAN,padding:28,borderRadius:20,fontSize:38,fontWeight:850}}>OLD CONTEXT ✓</div>
    </div>}
    {/* Editorial type is foreground, while the animated diagram remains full-screen. */}
    <div style={{
      position:'absolute',left:64,right:64,
      top:pi===3?300:pi===4?302:pi===5?283:254,
      opacity:sceneAlpha,
      transform:'translateY('+((1-anim)*-68)+'px)',
      textShadow:'0 10px 28px rgba(0,0,0,.95)',
    }}>
      <div style={{fontSize:24,color:phase.accent,fontWeight:900,letterSpacing:5,marginBottom:16}}>{phase.tag}</div>
      <div style={{fontSize:pi===5?106:119,lineHeight:.95,fontWeight:900,letterSpacing:-5}}>{phase.line1}</div>
      <div style={{fontSize:pi===5?101:122,lineHeight:1.1,fontWeight:900,color:phase.accent,letterSpacing:-5}}>{phase.line2}</div>
      <div style={{display:'inline-block',marginTop:18,fontSize:27,fontWeight:680,
        padding:'11px 16px',background:'rgba(4,12,15,.72)',borderLeft:'5px solid '+phase.accent,
        letterSpacing:.7}}>{phase.sub}</div>
    </div>
    {/* Keep captions in a consistent Shorts-safe zone; source captions come from TTS timings. */}
    <div style={{position:'absolute',bottom:195,left:46,right:46,height:210,display:'flex',
      justifyContent:'center',alignItems:'center'}}>
      {caption && <div style={{
        textAlign:'center',fontSize:emphatic?60:52,fontWeight:900,
        lineHeight:1.2,letterSpacing:-1.4,
        color:emphatic?phase.accent:IVORY,
        padding:'14px 25px',borderRadius:16,
        background:'rgba(5,9,13,.76)',
        border:'1px solid rgba(255,255,255,.16)',
        boxShadow:'0 15px 35px rgba(0,0,0,.45)',
        textShadow:'0 3px 10px #000',
        transform:'scale('+(.96+.04*reveal(frame,captionStart))+')',
      }}>{caption.text}</div>}
    </div>
    <div style={{position:'absolute',left:60,right:60,bottom:128,display:'flex',alignItems:'center',justifyContent:'space-between',
      color:'#91a1a7',fontSize:21,fontWeight:800,letterSpacing:2}}>
      <span>ONE QUESTION • ONE FACT</span>
      <span>0{pi+1} / 06</span>
    </div>
    <div style={{position:'absolute',left:60,right:60,bottom:102,height:7,background:'rgba(255,255,255,.15)',borderRadius:99}}>
      <div style={{width:(100*clamp(pct))+'%',height:'100%',background:'linear-gradient(90deg,'+NEON+','+CYAN+')',borderRadius:99}}/>
      <div style={{position:'absolute',left:(100*barOffset)+'%',top:-2,width:12,height:11,background:IVORY,borderRadius:30,opacity:.2}}/>
    </div>
    {narrationAvailable && <>
      <Audio src={staticFile('original/doorway/voiceover.mp3')} volume={1}/>
      <Audio src={staticFile('original/doorway/score.wav')} volume={.28}/>
    </>}
    {frame>=0 && frame<7 && <AbsoluteFill style={{background:IVORY,opacity:clamp((7-frame)/45),pointerEvents:'none'}}/>}
  </AbsoluteFill>;
};
