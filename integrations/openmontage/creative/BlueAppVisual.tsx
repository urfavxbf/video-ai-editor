import React from "react";
import {
  AbsoluteFill, Audio, Sequence, interpolate, spring, staticFile,
  useCurrentFrame, useVideoConfig,
} from "remotion";

/**
 * Original cinematic pixel-story staging for the owner-approved Blue App
 * tutorial. Inspired by a reference video's general editing grammar, NOT its
 * characters, exact artwork, frames, soundtrack or story.
 *
 * Scenes progress through different illustrated worlds rather than a repeated
 * dashboard template. Built as a project composition in pinned OpenMontage.
 */
type Cut = {id:string; in_seconds:number; out_seconds:number};
type Cue = {word:string; startMs:number; endMs:number; pageBreakAfter?:boolean};
type Props = {cuts:Cut[]; captions?:Cue[]; audio?:{narration?:{src:string;volume?:number}}};
const SKY="#B7F1FF", TEAL="#69F4DB", RED="#FF5369", GOLD="#FFC878", WHITE="#F8FAFF";
const CLAMP={extrapolateLeft:"clamp" as const,extrapolateRight:"clamp" as const};

const BEATS=[
  {world:"sunrise",eyebrow:"BEFORE YOU PANIC",a:"DELETED",b:"MESSAGES?",c:"HERE'S WHAT TO CHECK",device:"CHAT HISTORY",lines:["Your account", "Your own conversations"],color:GOLD},
  {world:"warning",eyebrow:"DO NOT FALL FOR THIS",a:"NO MAGIC",b:"RECOVERY APP",c:"START WITH YOUR OWN ACCOUNT",device:"SAFETY FIRST",lines:["No unknown APKs", "No password sharing"],color:RED},
  {world:"library",eyebrow:"FIRST THING TO CHECK",a:"ARCHIVED",b:"IS NOT DELETED",c:"LOOK IN ARCHIVED CHATS",device:"YOUR CHAT LIST",lines:["Archived → still there","Deleted → may be gone"],color:TEAL},
  {world:"studio",eyebrow:"STEP 01",a:"OPEN",b:"SETTINGS",c:"THEN GO TO ACCOUNTS CENTER",device:"ACCOUNT SETTINGS",lines:["Settings","Accounts Center"],color:SKY},
  {world:"library",eyebrow:"STEP 02",a:"YOUR",b:"INFORMATION",c:"AND PERMISSIONS",device:"YOUR INFORMATION",lines:["Your information","And permissions"],color:TEAL},
  {world:"studio",eyebrow:"STEP 03",a:"CREATE",b:"AN EXPORT",c:"USE YOUR OWN PROFILE",device:"EXPORT YOUR INFO",lines:["Create export","Select your profile"],color:GOLD},
  {world:"digital",eyebrow:"STEP 04",a:"CHOOSE",b:"HTML",c:"MESSAGES · ALL TIME",device:"EXPORT OPTIONS",lines:["Messages","All time · HTML"],color:TEAL},
  {world:"digital",eyebrow:"STEP 05",a:"DOWNLOAD",b:"THE ZIP",c:"EXTRACT · OPEN HTML · SEARCH",device:"EXPORTED FILES",lines:["messages.zip","Open HTML in browser"],color:GOLD},
  {world:"night",eyebrow:"ONE MORE PLACE",a:"ENCRYPTED",b:"CHATS?",c:"CHECK SECURE STORAGE SEPARATELY",device:"SECURE STORAGE",lines:["Encrypted history","Needs a separate check"],color:SKY},
  {world:"warning",eyebrow:"THE IMPORTANT TRUTH",a:"EXPORT IS",b:"NOT UNDELETE",c:"ONLY AVAILABLE DATA CAN APPEAR",device:"REALITY CHECK",lines:["Deleted forever? No guarantee","Only use your own account"],color:GOLD},
] as const;

function PolyStar({x,y,size,color="#FFFFFF"}:{x:number;y:number;size:number;color?:string}){
 return <div style={{position:"absolute",left:x,top:y,width:size,height:size,
   background:color,clipPath:"polygon(50% 0%,60% 40%,100% 50%,60% 60%,50% 100%,40% 60%,0% 50%,40% 40%)",
   filter:"drop-shadow(0 0 9px "+color+")"}}/>;
}
function PixelGuide({scale=1,walk=0}:{scale?:number;walk?:number}){
 // New original character: lavender bob haircut, rectangular glasses and
 // turquoise puffer jacket. Does not reproduce reference character's costume.
 const pixels=[
 "000000666666000000",
 "000066666666660000",
 "000666666666666000",
 "006666677776666600",
 "006666777777766600",
 "006667777777776600",
 "006667011110776600",
 "006667033330776600",
 "006667333333776600",
 "000677333333776000",
 "000077333333770000",
 "000008888888000000",
 "000888888888880000",
 "008888888888888000",
 "088888888888888800",
 "088888888888888800",
 "033888888888883300",
 "033888888888883300",
 "000888888888880000",
 "000088888888800000",
 "000099990099990000",
 "000099990099990000",
 "000099990099990000",
 "000044440044440000",
 "000044440044440000",
 ];
 const colors:Record<string,string>={
 "0":"transparent","6":"#9B83E5","7":"#29243B","1":"#F8E09B",
 "3":"#F9BA89","8":"#4FCEBB","9":"#2D3950","4":"#20212E"
 };
 const square=10;
 return <svg width={180*scale} height={250*scale} viewBox="0 0 180 250"
  style={{imageRendering:"pixelated",filter:"drop-shadow(5px 11px 2px rgba(0,0,0,.35))",
    transform:"translateY("+walk+"px)"}}>
  {pixels.flatMap((row,y)=>row.split("").map((p,x)=>p==="0"?null:
    <rect key={x+"-"+y} x={x*square} y={y*square} width={square} height={square}
       fill={colors[p]}/>))}
  <rect x={71} y={80} width={17} height={8} fill="#1B2741"/>
  <rect x={100} y={80} width={17} height={8} fill="#1B2741"/>
  <rect x={82} y={144} width={18} height={7} fill="#E9FFE8"/>
 </svg>;
}
function PixelChat({size=160,bob=0}:{size?:number;bob?:number}){
 return <svg width={size} height={size} viewBox="0 0 160 160"
  style={{imageRendering:"pixelated",transform:"translateY("+bob+"px)",
   filter:"drop-shadow(0px 8px 12px rgba(0,0,0,.4))"}}>
  <rect x={16} y={22} width={122} height={94} rx={4} fill="#08465A"/>
  <rect x={24} y={16} width={114} height={93} rx={4} fill="#60E5DF"/>
  <rect x={34} y={30} width={95} height={68} fill="#0A5673"/>
  <rect x={38} y={45} width={18} height={20} fill={WHITE}/>
  <rect x={106} y={45} width={18} height={20} fill={WHITE}/>
  <rect x={46} y={49} width={9} height={15} fill="#172641"/>
  <rect x={112} y={49} width={9} height={15} fill="#172641"/>
  <rect x={68} y={75} width={29} height={6} fill={GOLD}/>
  <rect x={27} y={107} width={23} height={20} fill="#60E5DF"/>
  <rect x={33} y={124} width={11} height={12} fill="#60E5DF"/>
 </svg>;
}
function Studio({frame,world}:{frame:number;world:string}){
 const pan=Math.sin(frame/23)*11;
 const warm=world==="studio"||world==="library";
 const sky=world==="sunrise";
 const night=world==="night";
 const red=world==="warning";
 const digital=world==="digital";
 const bg=sky
  ?"linear-gradient(180deg,#8BCDFE 0%,#E5F6FF 55%,#B9DDB2 56%,#438B6B 100%)"
  :red
  ?"radial-gradient(circle at 63% 40%,#8C2032 0%,#3B0F21 49%,#0B0612 95%)"
  :night
  ?"radial-gradient(circle at 50% 30%,#244F71 0%,#08162C 48%,#030711 100%)"
  :digital
  ?"radial-gradient(ellipse at 60% 50%,#1C5A57 0%,#081F2E 54%,#030910 100%)"
  :"linear-gradient(100deg,#201721 0%,#43272F 48%,#171725 100%)";
 return <AbsoluteFill style={{background:bg,overflow:"hidden"}}>
  {sky&&<>
    <div style={{position:"absolute",left:0,top:480,width:"130%",height:390,
      background:"#73A883",borderRadius:"50% 50% 0 0",transform:"rotate(-5deg)"}}/>
    <div style={{position:"absolute",left:0,top:640,width:"130%",height:440,
      background:"linear-gradient(180deg,#4A9463,#1B5446)",borderRadius:"40% 40% 0 0"}}/>
    {[170,490,1200,1560].map((x,i)=><div key={x} style={{position:"absolute",
      left:x+pan*(i%2?1:-1),top:96+(i%2)*80,width:245,height:92,
      background:"#FFFFFFBB",filter:"blur(7px)",borderRadius:"70% 65% 45% 40%"}}/>)}
    {Array.from({length:28},(_,i)=><div key={i} style={{position:"absolute",
      left:(i*211)%1920,top:820+(i%3)*25,width:7,height:20,
      transform:"rotate("+(i*31)+"deg)",background:i%3?"#D1EAC4":"#FFD480"}}/>)}
  </>}
  {warm&&<>
    <div style={{position:"absolute",top:0,left:0,right:0,height:690,
      background:"repeating-linear-gradient(90deg,#4C2E34 0px,#4C2E34 54px,#40252E 56px,#40252E 65px)"}}/>
    <div style={{position:"absolute",left:0,top:680,right:0,height:410,
      background:"linear-gradient(180deg,#361822,#160D18)"}}/>
    <div style={{position:"absolute",left:1020,top:40,width:700,height:410,
      background:"#1D1826",border:"24px solid #5B3640",
      boxShadow:"0 0 90px #F5B36E1C"}}/>
    {[0,1,2].map(j=><React.Fragment key={j}>
      <div style={{position:"absolute",left:1060,top:118+j*113,width:635,height:14,
        background:"#8A5548"}}/>
      {Array.from({length:13},(_,i)=><div key={i} style={{position:"absolute",
        left:1081+i*43,top:58+j*112,width:21+i%3*4,height:61,
        background:["#6D7990","#C27B5A","#BAAA67","#5B877C"][i%4],
        opacity:.72}}/>)}
    </React.Fragment>)}
    <div style={{position:"absolute",left:0,top:685,height:17,width:"100%",
      background:"#C27D5D"}}/>
    <div style={{position:"absolute",left:0,top:720,height:70,width:"100%",
      background:"linear-gradient(180deg,#77424B,#301924)",boxShadow:"0 30px 65px #0008"}}/>
    <div style={{position:"absolute",left:145,top:140,width:200,height:170,
      borderRadius:"50%",background:"#FFCF924A",filter:"blur(62px)"}}/>
    <div style={{position:"absolute",right:140,top:80,width:150,height:130,
      borderRadius:"50%",background:"#FFA97144",filter:"blur(60px)"}}/>
  </>}
  {red&&Array.from({length:9},(_,i)=><div key={i} style={{position:"absolute",
    left:100+i*224,top:-100,width:5,height:1320,
    background:i%2?"#FA5B5730":"#DE506520",
    transform:"rotate(17deg)"}}/>)}
  {night&&Array.from({length:28},(_,i)=>
    <PolyStar key={i} x={(i*317)%1920} y={(i*113)%820} size={i%4+5}
      color={i%3===0?TEAL:WHITE}/>)}
  {digital&&<>
    <div style={{position:"absolute",left:0,right:0,bottom:0,height:410,
      background:"repeating-linear-gradient(0deg,transparent 0px,transparent 46px,#37EAC91A 48px),repeating-linear-gradient(90deg,transparent 0px,transparent 75px,#37EAC91A 78px)",
      transform:"perspective(560px) rotateX(50deg) scale(1.5)",
      transformOrigin:"bottom"}}/>
    {Array.from({length:18},(_,i)=><div key={i} style={{position:"absolute",
      left:(i*163)%1920,top:(i*97)%680,width:20+(i%4)*10,height:20+(i%4)*10,
      border:"3px solid #4AEAB24D",transform:"rotate(25deg)"}}/>)}
  </>}
  <AbsoluteFill style={{background:"radial-gradient(ellipse at 50% 55%,transparent 30%,rgba(0,0,0,.55) 100%)"}}/>
 </AbsoluteFill>;
}
function Computer({frame,beat}:{frame:number;beat:typeof BEATS[number]}){
 const bob=Math.sin(frame/18)*8;
 const isFile=beat.device.includes("ZIP")||beat.device==="EXPORTED FILES";
 const tilt=interpolate(frame,[0,18],[-8,0],CLAMP);
 return <div style={{position:"absolute",right:145,top:242,width:700,height:505,
   transform:"perspective(1100px) rotateY("+tilt+"deg) translateY("+bob+"px)",
   filter:"drop-shadow(16px 31px 22px #0009)"}}>
  <div style={{background:"#121C2A",height:427,border:"21px solid #303542",
    borderRadius:15,boxShadow:"inset 0 0 70px #0CC9A512,0 0 60px #E6AB5A13",
    position:"relative",overflow:"hidden"}}>
   <div style={{position:"absolute",top:0,left:0,right:0,height:47,
      background:"#222B38",display:"flex",alignItems:"center",paddingLeft:22,
      gap:12,color:"#BFD4E5",fontWeight:800,fontSize:18}}>
      <span style={{color:RED}}>●</span><span style={{color:GOLD}}>●</span>
      <span style={{color:TEAL}}>●</span>
      <span style={{marginLeft:"auto",marginRight:24,letterSpacing:2}}>TUTORIAL VIEW</span>
   </div>
   <div style={{padding:"78px 47px 30px"}}>
    <div style={{color:beat.color,fontSize:22,fontWeight:800,
      letterSpacing:4,marginBottom:21}}>YOUR OWN ACCOUNT</div>
    <div style={{fontSize:37,fontWeight:900,color:WHITE,marginBottom:28}}>
      {beat.device}</div>
    {beat.lines.map((l,i)=><div key={i} style={{height:64,display:"flex",
      alignItems:"center",gap:24,borderBottom:"2px solid #3E5563",
      color:WHITE,fontSize:29,fontWeight:700}}>
      <span style={{width:26,height:26,border:"3px solid "+beat.color,
        background:i===0?beat.color:"transparent",borderRadius:5}}/>
      {l}
    </div>)}
   </div>
   <div style={{position:"absolute",left:30,right:30,bottom:15,height:2,
      background:"linear-gradient(90deg,transparent,"+beat.color+",transparent)"}}/>
  </div>
  <div style={{position:"absolute",left:281,top:426,width:125,height:71,
    background:"linear-gradient(90deg,#282D3B,#6C7682,#242B39)"}}/>
  <div style={{position:"absolute",left:208,top:491,width:272,height:15,
    background:"#3F434F",borderRadius:7}}/>
  {isFile&&<div style={{position:"absolute",left:475,top:-45,width:115,height:140,
    background:GOLD,clipPath:"polygon(0 0,65% 0,100% 27%,100% 100%,0 100%)",
    border:"4px solid #381F1B",transform:"rotate(11deg)",boxShadow:"10px 13px 0px #0004"}}>
    <div style={{position:"absolute",top:69,left:22,width:71,height:6,background:"#8D4A44"}}/>
    <div style={{position:"absolute",top:91,left:22,width:71,height:6,background:"#8D4A44"}}/>
  </div>}
 </div>;
}
function BigType({beat,frame}:{beat:typeof BEATS[number];frame:number}){
 const enter=spring({frame,fps:30,config:{damping:18,stiffness:120}});
 const shift=(1-enter)*110;
 const emph=beat.b.length>15?73:beat.b.length>11?91:114;
 return <div style={{position:"absolute",left:122,top:125,width:1040,
   transform:"translateX("+-shift+"px)",opacity:enter,
   textShadow:"0px 7px 22px #0008",zIndex:8}}>
    <div style={{fontSize:25,letterSpacing:6,fontWeight:900,color:beat.color,
       marginBottom:34}}>{beat.eyebrow}</div>
    <div style={{fontSize:95,lineHeight:1.08,letterSpacing:-3.3,
      fontWeight:950,color:WHITE}}>{beat.a}</div>
    <div style={{fontSize:emph,lineHeight:1.08,letterSpacing:-3,
      fontWeight:950,color:beat.color,maxWidth:1000}}>{beat.b}</div>
    <div style={{fontSize:32,letterSpacing:2.5,fontWeight:750,
      marginTop:35,maxWidth:860,color:WHITE}}>{beat.c}</div>
 </div>;
}
function Scene({index}:{index:number}){
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const beat=BEATS[index]??BEATS[0];
 const shift=Math.sin(frame/33)*14;
 const isWarn=beat.world==="warning";
 const cameraZoom=1+frame/(fps*210);
 const entrance=interpolate(frame,[0,15],[0,1],CLAMP);
 return <AbsoluteFill style={{overflow:"hidden",fontFamily:"Inter,Arial,sans-serif"}}>
   <AbsoluteFill style={{transform:"scale("+cameraZoom+") translateX("+shift+"px)"}}>
    <Studio frame={frame} world={beat.world}/>
   </AbsoluteFill>
   {(beat.world==="studio"||beat.world==="library"||beat.world==="sunrise")&&
    <div style={{position:"absolute",bottom:125,left:-10,width:"110%",
      height:60,background:"linear-gradient(180deg,#925C4C,#301D27)",
      boxShadow:"0 33px 72px #0009",zIndex:4}}/>}
   {isWarn&&<div style={{position:"absolute",right:210,top:130,
     border:"25px solid #FF879421",width:660,height:660,borderRadius:"50%",
     transform:"scale("+(0.96+Math.sin(frame/11)*0.06)+")"}}/>}
   <Computer frame={frame} beat={beat}/>
   <BigType beat={beat} frame={frame}/>
   <div style={{position:"absolute",bottom:82,left:140,zIndex:10,
      transform:"translateX("+((1-entrance)*-100)+"px)"}}>
      <PixelGuide scale={1.48} walk={Math.sin(frame/13)*5}/>
   </div>
   <div style={{position:"absolute",bottom:115,left:460,zIndex:11,
      transform:"rotate("+(-7+Math.sin(frame/13)*4)+"deg)"}}>
      <PixelChat size={153} bob={Math.sin(frame/13)*6}/>
   </div>
   <div style={{position:"absolute",bottom:58,right:138,color:"#C2C8C9",
      fontSize:20,fontWeight:800,letterSpacing:3,
      textShadow:"0 3px 10px #000D"}}>ILLUSTRATION · CHECK YOUR OWN ACCOUNT</div>
   <div style={{position:"absolute",top:42,right:115,color:beat.color,
      fontSize:26,fontWeight:800,letterSpacing:4}}>0{index+1} / 10</div>
   <div style={{position:"absolute",bottom:50,left:120,width:800,height:8,
      background:"#1F2531"}}>
      <div style={{height:"100%",width:((index+1)*10)+"%",background:beat.color}}/>
   </div>
   {frame<5&&<AbsoluteFill style={{background:beat.color,opacity:(1-frame/5)*0.18,
      pointerEvents:"none"}}/>}
 </AbsoluteFill>;
}
function Captions({cues}:{cues:Cue[]}){
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const ms=frame/fps*1000;
 let current=cues.findIndex(c=>ms>=c.startMs&&ms<c.endMs);
 if(current<0)return null;
 const start=Math.max(0,current-2),page=cues.slice(start,current+3);
 return <div style={{position:"absolute",bottom:16,left:485,right:485,zIndex:20,
    display:"flex",justifyContent:"center"}}>
   <div style={{display:"flex",gap:13,flexWrap:"wrap",
     justifyContent:"center",background:"rgba(2,7,13,.92)",
     padding:"12px 25px",borderRadius:10,border:"1px solid #77919C44"}}>
    {page.map((c,i)=><span key={i} style={{fontSize:37,fontWeight:900,
      color:(start+i)===current?GOLD:WHITE}}>{c.word}</span>)}
   </div>
 </div>;
}
export const BlueAppVisual:React.FC<Props>=({cuts,captions=[],audio={}})=>{
 const {fps}=useVideoConfig();
 return <AbsoluteFill style={{background:"#02050D"}}>
   {cuts.map((cut,i)=><Sequence key={cut.id} from={Math.round(cut.in_seconds*fps)}
      durationInFrames={Math.max(1,Math.round((cut.out_seconds-cut.in_seconds)*fps))}>
     <Scene index={i}/>
   </Sequence>)}
   {audio.narration?.src&&<Audio src={staticFile(audio.narration.src)}
     volume={audio.narration.volume??1}/>}
   {captions.length>0&&<Captions cues={captions}/>}
 </AbsoluteFill>;
};
