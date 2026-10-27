import { Audio, Video } from '@remotion/media';
import type { CSSProperties } from 'react';
import { AbsoluteFill, Sequence, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';

/**
 * An ORIGINAL commentary composition about a verified interview moment.
 * No podcast video/audio, celebrity likenesses, trademarks as artwork, or
 * synthetic celebrity voices are bundled with this repository.
 *
 * Rights-cleared footage can be supplied explicitly with licensedClipPath;
 * it is muted so narration remains the single editorial audio source.
 */
export type TomHollandAccentProps = {
  narrationPath?: string;
  licensedClipPath?: string;
  licensedClipStartSeconds?: number;
};

export const TOM_HOLLAND_ACCENT_FPS = 30;
export const TOM_HOLLAND_ACCENT_DURATION = 43 * TOM_HOLLAND_ACCENT_FPS;
const INK = '#070c17';
const WHITE = '#fff8eb';
const MUTED = '#aeb8c7';
const AMBER = '#ffca75';
const TEAL = '#7ce9da';
const FONT = "'Montserrat','Inter',sans-serif";
const segments = [
  { from: 0, to: 4.5, eyebrow: 'THE IRONIC SPIDER-MAN PROBLEM', first: 'THE ONE', second: 'WORD?', caption: 'Even Spider-Man has an accent problem.', accent: AMBER },
  { from: 4.5, to: 11, eyebrow: 'HOLLYWOOD / BEHIND THE SCENES', first: 'TOM IS', second: 'BRITISH.', caption: 'He switches accents to play an American hero.', accent: TEAL },
  { from: 11, to: 20.5, eyebrow: 'THE FUNNY PART', first: 'SPIDER-', second: 'MAN.', caption: 'The name of his own character trips him up.', accent: AMBER },
  { from: 20.5, to: 28.5, eyebrow: 'GOOD HANG / AMY POEHLER', first: 'IT IS THE', second: 'ACCENT.', caption: 'The American pronunciation is the difficult part.', accent: TEAL },
  { from: 28.5, to: 36, eyebrow: 'AN ACTOR’S CRAFT', first: 'SOUNDS', second: 'EASY?', caption: 'Tiny pronunciation changes can be the hardest.', accent: AMBER },
  { from: 36, to: 43, eyebrow: 'YOUR TURN', first: 'TRY', second: 'SAYING IT.', caption: 'Could you nail the accent?', accent: TEAL },
] as const;

const clamp = (v: number) => Math.max(0, Math.min(1, v));
const enter = (frame: number, start: number) =>
  spring({fps: TOM_HOLLAND_ACCENT_FPS, frame: Math.max(0, frame - Math.round(start * TOM_HOLLAND_ACCENT_FPS)),
    config: {stiffness: 130, damping: 22, mass: 0.75}});

const Microphone = ({frame}: {frame: number}) => {
  const swing = Math.sin(frame / 25) * 7;
  const glow = 0.45 + Math.sin(frame / 13) * 0.12;
  return <div aria-hidden="true" style={{
    position: 'absolute', top: 290, left: 180, width: 720, height: 790,
    transform: 'translateY(' + swing + 'px)', opacity: .93,
  }}>
    <div style={{position:'absolute',left:63,top:0,width:590,height:590,borderRadius:'50%',
      background:'radial-gradient(circle, rgba(124,233,218,.22), rgba(255,202,117,.06) 55%, transparent 72%)',
      transform:'scale(' + (1 + glow * .04) + ')'}}/>
    <div style={{position:'absolute',left:144,top:56,width:420,height:420,borderRadius:'50%',
      border:'3px solid rgba(124,233,218,.26)',boxShadow:'0 0 0 24px rgba(124,233,218,.035)'}}/>
    <div style={{position:'absolute',left:282,top:88,width:145,height:323,
      border:'7px solid #e8edf0',borderRadius:85,
      background:'linear-gradient(140deg,#31475c,#101925 68%)',boxShadow:'0 18px 65px #0009'}}/>
    {Array.from({length:10},(_,i)=><div key={i} style={{
      position:'absolute',top:141+i*22,left:307,width:96,height:5,
      borderRadius:5,background:'#cfdedb',opacity:.55,
    }}/>)}
    <div style={{position:'absolute',left:230,top:263,width:250,height:230,
      border:'15px solid #cbdad9',borderTop:'none',borderRadius:'0 0 125px 125px'}}/>
    <div style={{position:'absolute',left:346,top:485,width:15,height:89,background:'#cbdad9'}}/>
    <div style={{position:'absolute',left:268,top:569,width:173,height:17,borderRadius:10,background:'#cbdad9'}}/>
    {Array.from({length:25},(_,i)=>{
      const height=20+95*Math.abs(Math.sin(i*.75+frame*.09));
      return <div key={i} style={{position:'absolute',left:49+i*26,top:650-height/2,
        height,width:9,borderRadius:7,background:i%3===0?AMBER:TEAL,opacity:.7}}/>;
    })}
  </div>;
};

export const TomHollandAccent = ({
  narrationPath, licensedClipPath, licensedClipStartSeconds = 3756,
}: TomHollandAccentProps) => {
  const frame = useCurrentFrame();
  const time = frame / TOM_HOLLAND_ACCENT_FPS;
  const scene = segments.find((part) => time >= part.from && time < part.to) ?? segments[segments.length-1];
  const reveal = enter(frame, scene.from);
  const exitOpacity = clamp((scene.to - time) / .35);
  const progress = clamp(frame / TOM_HOLLAND_ACCENT_DURATION);
  const pulse = interpolate(Math.sin(frame / 14), [-1, 1], [.96, 1.04]);

  const footer: CSSProperties = {
    position:'absolute',left:65,right:65,bottom:125,
    color:MUTED,fontSize:20,fontWeight:800,letterSpacing:1.5,
  };
  return <AbsoluteFill style={{background:INK,color:WHITE,fontFamily:FONT,overflow:'hidden'}}>
    <AbsoluteFill style={{background:'radial-gradient(ellipse at 48% 35%, #182f39 0%, #111d2c 42%, #070c17 85%)'}}/>
    <AbsoluteFill style={{
      opacity:.14,transform:'translateX(' + ((frame*.25)%120) + 'px)',
      backgroundImage:'linear-gradient(90deg,#92adba 1px,transparent 1px),linear-gradient(#92adba 1px,transparent 1px)',
      backgroundSize:'120px 120px',
    }}/>
    <Microphone frame={frame}/>
    {licensedClipPath && <Sequence from={17*TOM_HOLLAND_ACCENT_FPS} durationInFrames={7*TOM_HOLLAND_ACCENT_FPS}>
      <div style={{position:'absolute',top:220,left:85,right:85,height:1050,
        overflow:'hidden',border:'4px solid rgba(255,255,255,.7)',borderRadius:32,
        boxShadow:'0 40px 110px #000b'}}>
        <Video src={staticFile(licensedClipPath)} muted
          trimBefore={Math.round(licensedClipStartSeconds*TOM_HOLLAND_ACCENT_FPS)}
          style={{width:'100%',height:'100%',objectFit:'cover'}}/>
        <div style={{position:'absolute',top:24,left:24,padding:'12px 20px',background:'#08111adf',
          color:WHITE,fontSize:24,fontWeight:800}}>LICENSED INTERVIEW EXCERPT</div>
      </div>
    </Sequence>}
    <div style={{position:'absolute',top:75,left:65,right:65,display:'flex',justifyContent:'space-between',
      alignItems:'center',fontSize:23,fontWeight:900,letterSpacing:3}}>
      <span>HOLLYWOOD <span style={{color:AMBER}}>/ EXPLAINED</span></span>
      <span style={{color:MUTED}}>01 / 06</span>
    </div>
    <div style={{position:'absolute',top:174,left:65,right:65,height:2,
      background:'linear-gradient(90deg,'+AMBER+',transparent)'}}/>
    <div style={{position:'absolute',top:930,left:60,right:60,textAlign:'center',
      opacity:exitOpacity, transform:'translateY(' + (1-reveal)*95 + 'px) scale(' + (.92+.08*reveal) + ')'}}>
      <div style={{color:scene.accent,fontSize:23,fontWeight:900,letterSpacing:3,marginBottom:30,
        textShadow:'0 4px 15px #000'}}>{scene.eyebrow}</div>
      <div style={{fontSize:102,fontWeight:950,letterSpacing:-5,lineHeight:.98,
        textShadow:'0 9px 30px #000c'}}>{scene.first}</div>
      <div style={{fontSize:112,fontWeight:950,letterSpacing:-5,lineHeight:1.03,color:scene.accent,
        textShadow:'0 9px 30px #000c',transform:'scale(' + pulse + ')'}}>{scene.second}</div>
      <div style={{marginTop:60,marginLeft:'auto',marginRight:'auto',padding:'19px 25px',maxWidth:900,
        background:'rgba(4,10,18,.91)',border:'2px solid #506470',borderRadius:22,
        fontSize:41,fontWeight:800,lineHeight:1.22,textShadow:'0 4px 12px #000'}}>
        {scene.caption}
      </div>
    </div>
    <div style={footer}>Original commentary • Source: Good Hang with Amy Poehler (Jun 2, 2026)</div>
    <div style={{position:'absolute',bottom:93,left:65,right:65,height:5,
      borderRadius:5,background:'#ffffff22'}}>
      <div style={{height:'100%',width:(progress*100)+'%',background:AMBER,borderRadius:5}}/>
    </div>
    {narrationPath && <Audio src={staticFile(narrationPath)} volume={1}/>}
  </AbsoluteFill>;
};
