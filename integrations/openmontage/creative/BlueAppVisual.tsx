import React from "react";
import {
  AbsoluteFill, Audio, Sequence, interpolate, spring,
  staticFile, useCurrentFrame, useVideoConfig,
} from "remotion";

/**
 * Original widescreen storytelling treatment of the approved Blue App tutorial.
 * Uses the EXISTING pinned OpenMontage Remotion runtime — no third-party media.
 * The pixel envelope is newly authored geometry, not an imitation of a
 * reference video's character, logo, mascot, or background art.
 */
type Cut = {
  id: string; type?: string; text?: string; title?: string; subtitle?: string;
  leftLabel?: string; rightLabel?: string; leftValue?: string; rightValue?: string;
  in_seconds: number; out_seconds: number;
};
type Cue = {word:string;startMs:number;endMs:number;pageBreakAfter?:boolean};
type Props = {
  cuts:Cut[]; captions?:Cue[];
  audio?:{narration?:{src:string;volume?:number}};
};
const DARK="#071322";
const INK="#E9F5FF";
const TEAL="#63F6D4";
const AMBER="#FFC768";
const BLUE="#51ADFF";
const panels:Record<string,{category:string;header:string;rows:string[];accent:string}>={
  "01-hook":{category:"THE PROBLEM",header:"MISSING CHAT?",rows:["Check what still exists","Avoid fake recovery tricks"],accent:AMBER},
  "02-stop":{category:"SECURITY CHECK",header:"BE CAREFUL",rows:["Skip unknown recovery apps","Never share your password"],accent:AMBER},
  "03-archive":{category:"CHECK FIRST",header:"YOUR INBOX",rows:["Archived = still available","Deleted = not guaranteed"],accent:TEAL},
  "04-settings":{category:"STEP 01",header:"SETTINGS",rows:["Open your own account","Go to Accounts Center"],accent:BLUE},
  "05-information":{category:"STEP 02",header:"INFORMATION",rows:["Your information","And permissions"],accent:TEAL},
  "06-export":{category:"STEP 03",header:"EXPORT",rows:["Export your information","Create export"],accent:BLUE},
  "07-html":{category:"STEP 04",header:"FORMAT",rows:["Select Messages","All time · HTML"],accent:TEAL},
  "08-zip":{category:"STEP 05",header:"YOUR ZIP FILE",rows:["Download and extract","Open the HTML file"],accent:AMBER},
  "09-secure":{category:"EXTRA CHECK",header:"SECURE STORAGE",rows:["Encrypted chat history","Separate restoration path"],accent:BLUE},
  "10-reality":{category:"IMPORTANT",header:"THE LIMIT",rows:["Only available account data","No guaranteed undelete"],accent:AMBER},
};
const clamp={extrapolateLeft:"clamp" as const,extrapolateRight:"clamp" as const};
const pixelGlyph=[
  "0000000000000000",
  "0011111111111100",
  "0112222222222210",
  "0122222222222210",
  "0122211111122210",
  "0122122222212210",
  "0121222222221210",
  "0121222222221210",
  "0122122222212210",
  "0122211111122210",
  "0122222222222210",
  "0112222222222210",
  "0011111111111100",
  "0000110000110000",
  "0000100000010000",
  "0000000000000000",
];
function PixelEnvelope({accent}:{accent:string}){
  const frame=useCurrentFrame();
  const bob=Math.sin(frame/12)*7;
  return <div style={{
    width:186,height:186,position:"relative",flexShrink:0,
    filter:`drop-shadow(0 12px 35px ${accent}38)`,
    transform:`translateY(${bob}px)`
  }}>
    <svg viewBox="0 0 160 160" width="186" height="186" aria-hidden="true">
      {pixelGlyph.flatMap((line,y)=>line.split("").map((c,x)=>{
        if(c==="0")return null;
        const fill=c==="1"?"#122238":c==="2"?(y>=13?"#F6BC67":accent):INK;
        return <rect key={`${x}-${y}`} x={x*10} y={y*10}
          width={10.2} height={10.2} fill={fill}/>;
      }))}
    </svg>
    <div style={{position:"absolute",right:0,top:14,borderRadius:40,
      background:"#10293B",border:`2px solid ${accent}`,padding:"7px 15px",
      color:INK,fontWeight:900,fontSize:20}}>?</div>
  </div>;
}
function BottomCaptions({words}:{words:Cue[]}){
  const frame=useCurrentFrame();const {fps}=useVideoConfig();
  const ms=frame/fps*1000;
  let active=words.findIndex(w=>ms>=w.startMs&&ms<w.endMs);
  if(active<0)active=words.findIndex(w=>w.startMs>ms)-1;
  if(active<0||!words.length)return null;
  let pageStart=active;
  for(let i=active;i>Math.max(-1,active-6);i--)if(words[i-1]?.pageBreakAfter){pageStart=i;break;}
  pageStart=Math.max(pageStart,active-4);
  const page=words.slice(pageStart,Math.min(words.length,pageStart+5));
  return <div style={{position:"absolute",bottom:54,left:170,right:170,
      textAlign:"center",pointerEvents:"none"}}>
    <div style={{display:"inline-flex",justifyContent:"center",flexWrap:"wrap",gap:13,
      maxWidth:"100%",background:"rgba(2,8,16,0.87)",padding:"16px 31px",
      borderRadius:16,border:"1px solid #325669"}}>
      {page.map((w,i)=><span key={i} style={{fontWeight:900,fontSize:42,
        color:ms>=w.startMs&&ms<w.endMs?TEAL:INK,letterSpacing:-0.4}}>
        {w.word}</span>)}
    </div>
  </div>;
}
function Stage({cut,index,total}:{cut:Cut;index:number;total:number}){
  const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();
  const info=panels[cut.id]??panels["01-hook"];
  const fade=interpolate(frame,[0,11],[0,1],clamp);
  const shift=interpolate(frame,[0,18],[100,0],clamp);
  const bounce=spring({frame,fps,config:{damping:22,stiffness:110}});
  const beams=Array.from({length:9},(_,i)=>i);
  const isFirst=index===0;
  const raw=cut.type==="comparison"
      ?["CHECK THE CHAT", "ARCHIVED ≠ DELETED"]
      :((cut.text??cut.title??"").split("\n").filter(Boolean));
  const headlines=raw.length?raw:[info.header];
  const sceneLabel=`${String(index+1).padStart(2,"0")} / ${String(total).padStart(2,"0")}`;
  return <AbsoluteFill style={{overflow:"hidden",background:DARK,color:INK,
    fontFamily:"Inter, Arial, sans-serif"}}>
    <AbsoluteFill style={{background:`radial-gradient(ellipse at 75% 40%,${info.accent}20,transparent 43%),linear-gradient(140deg,#071322 0%,#0A172A 53%,#08242C 100%)`}}/>
    {beams.map(i=><div key={i} style={{position:"absolute",width:3,height:height*1.5,
      top:-height*.25,left:115+i*219,transform:"rotate(12deg)",
      background:"rgba(118,223,232,0.045)"}}/>)}
    <div style={{position:"absolute",top:55,left:116,display:"flex",gap:22,
      alignItems:"center",fontSize:22,fontWeight:800,letterSpacing:3,
      color:"#A6BAC9"}}>
      <span style={{width:11,height:11,background:info.accent,boxShadow:`0 0 15px ${info.accent}`}}/>
      THE BLUE APP / MESSAGE HISTORY
    </div>
    <div style={{position:"absolute",top:54,right:110,fontSize:24,fontWeight:800,
      letterSpacing:3,color:info.accent}}>CHAPTER {sceneLabel}</div>
    <div style={{position:"absolute",left:110,top:185,width:940,
      opacity:fade,transform:`translateX(${-shift}px)`}}>
      <div style={{fontSize:25,fontWeight:900,letterSpacing:6,color:info.accent,marginBottom:32}}>
        {info.category}
      </div>
      {headlines.map((line,i)=>{
        const long=line.length>24;
        const size=long?59:line.length>18?69:85;
        return <div key={i} style={{
          maxWidth:895,fontWeight:950,fontSize:size,lineHeight:1.12,
          letterSpacing:-2.5,marginBottom:17,overflowWrap:"anywhere",
          color:i===0?INK:info.accent,
          textShadow:i>0?`0 0 28px ${info.accent}33`:undefined,
          transform:`translateY(${(1-bounce)*(i+1)*34}px)`
        }}>{line.toUpperCase()}</div>;
      })}
      {cut.title&&cut.type!=="comparison"&&<div style={{fontSize:34,fontWeight:700,
        marginTop:24,color:"#B2CBD9"}}>{cut.title}</div>}
      {cut.subtitle&&<div style={{fontSize:31,marginTop:25,color:"#C0D2DC"}}>
        {cut.subtitle}</div>}
      {cut.type==="comparison"&&<div style={{marginTop:35,
        display:"flex",gap:14,flexWrap:"wrap"}}>
          <span style={{padding:"17px 24px",borderRadius:12,
            background:"#143549",fontSize:27,fontWeight:900}}>
            ARCHIVED: STILL THERE</span>
          <span style={{padding:"17px 24px",borderRadius:12,
            background:"#493128",fontSize:27,fontWeight:900}}>
            DELETED: MAY BE GONE</span>
        </div>}
    </div>
    <div style={{position:"absolute",top:170,right:104,width:615,height:668,
      transform:`translateX(${shift}px) perspective(1300px) rotateY(${(1-fade)*-8}deg)`,
      opacity:fade}}>
      <div style={{position:"absolute",inset:0,borderRadius:24,
        border:"1px solid #44728C",background:"#0E2031",
        boxShadow:"0 55px 115px #0008, 0 0 90px #4FBFDB12",overflow:"hidden"}}>
        <div style={{height:80,background:"#162E42",borderBottom:"1px solid #2A5062",
          display:"flex",alignItems:"center",gap:14,padding:"0 30px"}}>
          {["#FF725A",AMBER,TEAL].map((c,i)=>
            <div key={i} style={{height:14,width:14,borderRadius:"50%",background:c}}/>)}
          <span style={{marginLeft:"auto",fontWeight:900,fontSize:19,
            letterSpacing:2,color:"#92C9DB"}}>ACCOUNT VIEW</span>
        </div>
        <div style={{padding:"39px 37px"}}>
          <div style={{color:info.accent,fontSize:23,fontWeight:900,letterSpacing:4}}>
            {info.category}</div>
          <div style={{fontSize:49,fontWeight:950,marginTop:17,marginBottom:30,
            lineHeight:1.12,maxWidth:540,overflowWrap:"anywhere"}}>
            {info.header}</div>
          <div style={{background:"#142F42",borderRadius:18,padding:"26px 25px",
            border:"1px solid #2F576D"}}>
          {info.rows.map((label,i)=><div key={i} style={{display:"flex",
            alignItems:"center",gap:19,minHeight:70,
            borderBottom:i===info.rows.length-1?"none":"1px solid #2F4B60"}}>
            <span style={{display:"inline-flex",alignItems:"center",justifyContent:"center",
              width:33,height:33,border:`2px solid ${info.accent}`,
              borderRadius:8,color:info.accent,fontSize:20,fontWeight:900}}>✓</span>
            <span style={{fontSize:28,fontWeight:750,color:INK,
              overflowWrap:"anywhere"}}>{label}</span>
          </div>)}
          </div>
          <div style={{color:"#89AFC2",fontWeight:700,fontSize:21,marginTop:26,
            letterSpacing:1}}>ILLUSTRATION · NOT A LIVE ACCOUNT</div>
        </div>
      </div>
      <div style={{position:"absolute",right:-43,bottom:-45,
        transform:`scale(${0.9+0.1*bounce})`}}>
        <PixelEnvelope accent={info.accent}/>
      </div>
    </div>
    <div style={{position:"absolute",bottom:37,left:110,display:"flex",gap:12}}>
      {panels&&Array.from({length:total},(_,i)=><div key={i} style={{
        width:i===index?70:25,height:6,borderRadius:7,
        background:i<=index?info.accent:"#365165"}}/>)}
    </div>
    <div style={{position:"absolute",bottom:32,right:114,
      fontSize:18,letterSpacing:2,color:"#779BAD"}}>CHECK YOUR OWN ACCOUNT ONLY</div>
    {isFirst&&<div style={{position:"absolute",width:560,height:7,
      background:info.accent,left:0,top:150,transform:`translateX(${-540+550*fade}px)`}}/>}
  </AbsoluteFill>;
}
export const BlueAppVisual:React.FC<Props>=({cuts,captions=[],audio={}})=>{
  const {fps}=useVideoConfig();
  return <AbsoluteFill style={{background:DARK}}>
    {cuts.map((cut,i)=><Sequence key={cut.id}
      from={Math.round(cut.in_seconds*fps)}
      durationInFrames={Math.max(1,Math.round((cut.out_seconds-cut.in_seconds)*fps))}>
        <Stage cut={cut} index={i} total={cuts.length}/>
      </Sequence>)}
    {audio?.narration?.src&&<Audio src={staticFile(audio.narration.src)}
      volume={audio.narration.volume??1}/>}
    {captions.length>0&&<BottomCaptions words={captions}/>}
  </AbsoluteFill>;
};
