import React from 'react';
import {AbsoluteFill, Easing, interpolate, Sequence, spring, useCurrentFrame, Img, staticFile, OffthreadVideo} from 'remotion';
import {FX_ALL} from '../fx/index';
import {FxSourceContext, type FxSource, FX_H, FX_W} from '../fx/shared';
import {AfterEffectsLottieProof} from '../after-effects/AfterEffectsLottieProof';
import {DuikBakedCharacterProof} from '../after-effects/DuikBakedCharacterProof';

const FPS = 30;
const INTRO = 57;
const OUTRO = 75;
const LOTTIE = 105;
const DUIK = 105;
const HYPER = 60;
const COLORS = ['#79ffbc','#6eeaff','#f8a476','#b9a4ff','#f5dd82'];
const FACE_SOURCE: FxSource = {
  video:'sample/take.mp4',
  matte:'sample/fg',
  sticker:'sample/sticker',
  frames:300,
  face:{x:540,y:620,mouthY:900},
  continuous:true,
};
const DESCRIPTIONS = [
  '360° layered tool orbit','AI conversation takes over the scene',
  'Break out of the camera frame','Speed-ramped impact punch',
  'Four animated visual callouts','Headline collision and depth',
  'Fly through the portal','Draw an animated curve',
  'B-roll takes over the frame','Real cut-out sticker layering',
  'A kinetic cover reveal','Refractive glass treatment',
  'Fly through a cut point','Chroma studio switch',
  'Break the new frame','Digital crop and scrutiny',
  'Animate a social phone','Every FX counted in motion',
  'Floating data interfaces','Five-stage visual checklist',
  'Split-screen dynamic comparison',
] as const;
const GROUPS = ['CAMERA / DEPTH','AI / INTERFACE','COMPOSITE / FRAMING','CAMERA / IMPACT',
 'MOTION / LISTS','EDITORIAL / IMPACT','CAMERA / PORTAL','DATA / ANIMATION',
 'COMPOSITING / B-ROLL','CUTOUT / STICKERS','EDITORIAL / DESIGN','GLASS / OPTICS',
 'TRANSITION / CAMERA','COMPOSITE / KEYING','TRANSITION / 3D ILLUSION',
 'CAMERA / CROP','UI / SOCIAL','SPEED / TYPOGRAPHY','UI / DATA','MOTION / LISTS','COMPARE / MOTION'];
const schedule = FX_ALL.reduce<Array<{index:number;at:number;entry:(typeof FX_ALL)[number]}>>((acc,entry,index)=>{
  const at = INTRO + (acc.length?acc[acc.length-1].at-INTRO+acc[acc.length-1].entry.duration:0);
  acc.push({index,at,entry});
  return acc;
},[]);
const FX_END = INTRO + FX_ALL.reduce((sum,entry)=>sum+entry.duration,0);
const LOTTIE_START = FX_END;
const DUIK_START = LOTTIE_START + LOTTIE;
const HYPER_START = DUIK_START + DUIK;
const OUTRO_START = HYPER_START + HYPER;
export const SHOWREEL_FRAMES = OUTRO_START + OUTRO;
export const SHOWREEL_EFFECT_IDS = FX_ALL.map(effect=>effect.id);
export const SHOWREEL_EFFECT_STARTS = schedule.map(s=>({id:s.entry.id,at:s.at,duration:s.entry.duration}));

const springIn=(f:number,at=0)=>spring({fps:FPS,frame:f-at,config:{damping:22,stiffness:115,mass:.85}});
const clamp=(v:number)=>Math.min(1,Math.max(0,v));
const easeOut=(x:number)=>1-Math.pow(1-clamp(x),3);
const FONT="'Montserrat','Inter',sans-serif";
const Backdrop=({globalFrame}:{globalFrame:number})=><AbsoluteFill style={{
  background:'radial-gradient(ellipse at 77% 30%,#1b3446 0%,#0c1625 44%,#050a12 100%)',
  overflow:'hidden',
}}>
  <AbsoluteFill style={{opacity:.18,backgroundImage:
    'linear-gradient(#8effce 1px,transparent 1px),linear-gradient(90deg,#8effce 1px,transparent 1px)',
    backgroundSize:'85px 85px',transform:'translateX('+((globalFrame*1.3)%85)+'px)'}}/>
  {Array.from({length:7},(_,i)=><div key={i} style={{position:'absolute',
    left:-350+i*330,top:150+(i%3)*180,width:660,height:4,background:'#5ae7b0',
    opacity:.04+.025*(i%3),transform:'rotate(-28deg) translateX('+((globalFrame*2+i*80)%500)+'px)'}}/>)}
  <div style={{position:'absolute',width:980,height:980,left:760,top:130,borderRadius:490,
    border:'1px solid #4a8a8f44',transform:'rotate('+globalFrame*.16+'deg)'}}/>
</AbsoluteFill>;
const Track=({globalFrame,chapter}:{globalFrame:number;chapter:string})=><>
  <div style={{position:'absolute',left:90,top:55,right:95,display:'flex',alignItems:'center',gap:22,zIndex:50,color:'#e8fff6',fontSize:20,letterSpacing:5,fontWeight:900}}>
    <span style={{background:'#8cffbd',color:'#04130d',borderRadius:6,padding:'11px 15px'}}>URFAVXBF</span>
    <span>VIDEO AI EDITOR</span><span style={{marginLeft:'auto',color:'#81dccc',fontSize:17}}>{chapter}</span>
  </div>
  <div style={{position:'absolute',left:90,right:90,bottom:56,height:4,background:'#47616b',zIndex:50}}>
    <div style={{height:4,width:(100*globalFrame/SHOWREEL_FRAMES)+'%',background:'#8cffbd',boxShadow:'0 0 20px #77ffd77a'}}/>
  </div>
  <div style={{position:'absolute',bottom:14,left:90,right:90,display:'flex',justifyContent:'space-between',
    zIndex:50,color:'#81949b',letterSpacing:3,fontSize:17,fontWeight:700}}>
    <span>ALL 21 LIVE REMOTION FX + VECTOR / PUPPET / HYPERFRAMES</span>
    <span>{Math.floor(globalFrame/FPS).toString().padStart(2,'0')}s / {Math.ceil(SHOWREEL_FRAMES/FPS)}s</span>
  </div>
</>;
const EnterWipe=({frame,color}:{frame:number;color:string})=>{
  const amount=easeOut(frame/10);
  if(amount>=1)return null;
  return <AbsoluteFill style={{background:color,clipPath:'polygon(0 0,'+(100-amount*100)+'% 0,'+(110-amount*110)+'% 100%,0 100%)',zIndex:32,opacity:.87}}/>;
};
const PortraitScreen=({children,frame}:{children:React.ReactNode;frame:number})=>{
  const reveal=springIn(frame);
  const punch=1+.025*Math.exp(-Math.max(0,frame)/11);
  return <div style={{position:'absolute',left:1135,top:50,width:540,height:960,
    borderRadius:28,overflow:'hidden',border:'3px solid #74f9c789',
    boxShadow:'0 0 0 15px #152c328c,0 30px 150px #53ffc52b',
    transform:'translateX('+((1-reveal)*190)+'px) scale('+punch+')',
    transformOrigin:'center',background:'#10191f',zIndex:5}}>
    <div style={{width:FX_W,height:FX_H,transform:'scale(.5)',transformOrigin:'top left'}}>{children}</div>
    <div style={{position:'absolute',left:20,top:19,padding:'7px 14px',borderRadius:6,
      background:'#030b1099',color:'#85f6c1',fontSize:18,fontWeight:800,letterSpacing:3}}>LIVE FX / SOURCE</div>
  </div>;
};
const EffectsSequence=({index,entry,globalFrame}:{index:number;entry:(typeof FX_ALL)[number];globalFrame:number})=>{
  const frame=useCurrentFrame();
  const active=easeOut(frame/18);
  const appear=interpolate(frame,[0,12,entry.duration-11,entry.duration-1],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const color=COLORS[index%COLORS.length];
  const from=(index*7)%90;
  return <AbsoluteFill style={{fontFamily:FONT,color:'#f5fff9'}}>
    <Backdrop globalFrame={globalFrame}/>
    <PortraitScreen frame={frame}>
      <FxSourceContext.Provider value={FACE_SOURCE}>
        <entry.Component from={from}/>
      </FxSourceContext.Provider>
    </PortraitScreen>
    <div style={{position:'absolute',left:92,top:180,width:1010,zIndex:10}}>
      <div style={{display:'flex',alignItems:'center',gap:14,transform:'translateY('+((1-active)*35)+'px)',opacity:active}}>
        <div style={{width:55,height:4,background:color}}/>
        <div style={{fontSize:25,color,letterSpacing:4,fontWeight:900}}>{GROUPS[index]}</div>
      </div>
      <div style={{fontSize:68,fontWeight:1000,letterSpacing:-3.4,marginTop:76,
        lineHeight:1.04,transform:'translateX('+((1-active)*-90)+'px)',opacity:active,
        maxWidth:990,textTransform:'uppercase'}}>{entry.name}</div>
      <div style={{marginTop:30,maxWidth:820,fontSize:34,color:'#b4ced3',fontWeight:500,
        lineHeight:1.35,opacity:appear}}>{DESCRIPTIONS[index]}</div>
      <div style={{display:'flex',alignItems:'baseline',gap:26,marginTop:93,color:color,opacity:appear}}>
        <span style={{fontSize:145,fontWeight:950,lineHeight:1,letterSpacing:-9}}>{String(index+1).padStart(2,'0')}</span>
        <span style={{fontSize:31,fontWeight:700,color:'#f0fff9'}}>/ 21 EFFECTS</span>
      </div>
      <div style={{height:5,width:380,marginTop:50,background:'#34515a'}}>
        <div style={{height:'100%',width:(100*clamp(frame/entry.duration))+'%',background:color}}/>
      </div>
      <div style={{fontSize:18,color:'#749eae',marginTop:25,fontWeight:700,letterSpacing:2}}>
        REAL REGISTERED EFFECT COMPONENT / ORIGINAL ANIMATED SOURCE
      </div>
    </div>
    <div style={{position:'absolute',left:88,top:125,width:30,height:30,borderTop:'2px solid '+color,
      borderLeft:'2px solid '+color,opacity:.7}}/>
    <EnterWipe frame={frame} color={color}/>
  </AbsoluteFill>;
};
const Intro=()=>{const f=useCurrentFrame();const p=springIn(f);return <AbsoluteFill style={{fontFamily:FONT,color:'white'}}>
  <Backdrop globalFrame={f}/>
  <div style={{position:'absolute',left:98,top:214,fontSize:32,letterSpacing:8,color:'#98dccc',fontWeight:800,opacity:p}}>A REAL-TIME CREATIVE SYSTEM</div>
  <div style={{position:'absolute',left:85,top:305,display:'flex',alignItems:'baseline',gap:40}}>
    <span style={{fontSize:325,fontWeight:950,letterSpacing:-28,color:'#8effbb',
      transform:'scale('+(.65+.35*p)+')',opacity:p}}>21</span>
    <span style={{fontSize:143,lineHeight:1,fontWeight:950,letterSpacing:-9,
      transform:'translateY('+((1-p)*100)+'px)',opacity:p}}>EFFECTS.<br/><span style={{color:'#81d8ff'}}>IN MOTION.</span></span>
  </div>
  <div style={{position:'absolute',left:95,top:772,fontSize:39,color:'#b1cacb',
    letterSpacing:2,opacity:interpolate(f,[15,33],[0,1],{extrapolateRight:'clamp'})}}>
    NO SLIDES. ACTUAL EFFECTS. LIVE COMPOSITING.
  </div>
  <div style={{position:'absolute',right:170,top:136,width:270,height:270,borderRadius:135,
    border:'4px solid #8effbb',transform:'scale('+(.8+.2*p)+') rotate('+(f*3)+'deg)',
    boxShadow:'0 0 90px #6fffbc35'}}/>
</AbsoluteFill>};
const Bridge=({title,tag,description,children,color}:{title:string;tag:string;description:string;children:React.ReactNode;color:string})=>{
 const f=useCurrentFrame();const p=springIn(f);
 return <AbsoluteFill style={{fontFamily:FONT,color:'#f2fff8'}}>
  <Backdrop globalFrame={FX_END+f}/>
  <div style={{position:'absolute',top:230,left:90,width:750,zIndex:5}}>
    <div style={{fontSize:28,letterSpacing:5,fontWeight:800,color}}>{tag}</div>
    <div style={{fontSize:83,fontWeight:950,lineHeight:1.1,letterSpacing:-4,marginTop:70,opacity:p,
      transform:'translateX('+((1-p)*-90)+'px)'}}>{title}</div>
    <div style={{fontSize:34,color:'#adccd1',lineHeight:1.4,marginTop:46}}>{description}</div>
    <div style={{marginTop:90,width:360,height:6,background:color}}/>
    <div style={{fontSize:18,color:'#86aeb5',marginTop:24,letterSpacing:3}}>OFFLINE BRIDGE / ACTUAL RENDERED FRAMES</div>
  </div>
  <div style={{position:'absolute',top:98,left:1030,width:720,height:810,zIndex:6,overflow:'hidden',
   border:'3px solid '+color,borderRadius:26,boxShadow:'0 20px 120px #57f5b42a',
   transform:'translateX('+((1-p)*135)+'px)'}}>
   {children}
  </div>
 </AbsoluteFill>
};
const Outro=()=>{const f=useCurrentFrame();const p=springIn(f);return <AbsoluteFill style={{fontFamily:FONT,color:'white'}}>
 <Backdrop globalFrame={OUTRO_START+f}/>
 <div style={{position:'absolute',left:120,top:262,fontSize:46,color:'#8cfabd',letterSpacing:7,fontWeight:850}}>21 EFFECTS. THREE BRIDGES.</div>
 <div style={{position:'absolute',left:110,top:365,fontSize:140,fontWeight:950,lineHeight:1,letterSpacing:-6,
    opacity:p,transform:'translateY('+((1-p)*110)+'px)'}}>
   BUILD <span style={{color:'#8cfabd'}}>MOTION.</span><br/>NOT SLIDES.
 </div>
 <div style={{position:'absolute',left:120,top:747,color:'#b6d4d1',fontSize:32}}>
   ORIGINAL ARTWORK + ACTUAL REMOTION EFFECTS + LOCAL MOTION ENGINES
 </div>
 </AbsoluteFill>};
export const MotionShowreel = ()=>{
  const frame=useCurrentFrame();
  return <AbsoluteFill style={{background:'#040a12',overflow:'hidden'}}>
    <Sequence from={0} durationInFrames={INTRO}><Intro/></Sequence>
    {schedule.map(({entry,index,at})=><Sequence key={entry.id} from={at} durationInFrames={entry.duration}>
      <EffectsSequence entry={entry} index={index} globalFrame={frame}/>
    </Sequence>)}
    <Sequence from={LOTTIE_START} durationInFrames={LOTTIE}>
      <Bridge title={'AFTER EFFECTS\n→ LOTTIE'} tag="22 / VECTOR ANIMATION" color="#a3e6ff"
        description="Genuine keyframed vector playback. No static images.">
        <div style={{width:1080,height:1920,transform:'translate(-90px,-125px) scale(.45)',transformOrigin:'top left'}}>
          <AfterEffectsLottieProof/>
        </div>
      </Bridge>
    </Sequence>
    <Sequence from={DUIK_START} durationInFrames={DUIK}>
      <Bridge title="PUPPET MOTION" tag="23 / BAKED 2D RIG BRIDGE" color="#baa5ff"
        description="Articulated keyframes, exported to Remotion. Demo rig, not a native Duik project.">
        <div style={{width:1920,height:1080,transform:'translate(-360px,130px) scale(.75)',transformOrigin:'top left'}}>
          <DuikBakedCharacterProof/>
        </div>
      </Bridge>
    </Sequence>
    <Sequence from={HYPER_START} durationInFrames={HYPER}>
      <Bridge title="HYPERFRAMES" tag="24 / HTML + GSAP ENGINE" color="#87ffc7"
        description="Locally rendered timeline animation, composited into the final video.">
        <OffthreadVideo src={staticFile('hyperframes/kinetic-intro.mp4')} muted
          style={{width:'100%',height:'100%',objectFit:'cover'}}/>
      </Bridge>
    </Sequence>
    <Sequence from={OUTRO_START} durationInFrames={OUTRO}><Outro/></Sequence>
    <Track globalFrame={frame} chapter={frame<INTRO?'OPENING':frame<FX_END?'21 LIVE EFFECTS':frame<OUTRO_START?'MOTION ENGINES':'WRAP'}/>
  </AbsoluteFill>;
};
