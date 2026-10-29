import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import visualAid from '../../productions/youtube-beginner-journey/visual-aid.json';

export const STORYBOARD_SECONDS = visualAid.targetDurationSeconds;
export const STORYBOARD_FRAMES = STORYBOARD_SECONDS * visualAid.format.fps;
export const STORYBOARD_BEATS = visualAid.beats;

const ink = '#060d19';
const card = '#101e32';
const border = '#35485e';
const cyan = '#27e8fd';
const yellow = '#ffda00';
const text = '#f1f6ff';
const muted = '#96a8c3';
const clamp = (x: number) => Math.max(0, Math.min(1, x));
const show = (f: number, delay = 0, duration = 22) =>
  interpolate(f, [delay, delay + duration], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
const drift = (f: number, n: number) => ({
  opacity: show(f, n * 9),
  transform: `translateY(${(1 - show(f, n * 9)) * 28}px)`,
});
const pane: React.CSSProperties = {
  background: card, border: `2px solid ${border}`, borderRadius: 24, padding: 25,
};
const small: React.CSSProperties = {fontSize: 20, letterSpacing: 1.5, color: muted};
const strong: React.CSSProperties = {fontWeight: 900, color: text};

const Pill: React.FC<{children: React.ReactNode; accent?: string}> = ({children,accent=cyan}) =>
  <div style={{border: `1px solid ${accent}88`, background: `${accent}16`, color: accent,
    padding: '10px 18px', fontWeight: 800, fontSize: 23, borderRadius: 14}}>{children}</div>;

const Progress: React.FC<{value: number; color?: string; height?: number}> = ({
  value, color=cyan, height=13,
}) => <div style={{height, background:'#26394e',borderRadius:height/2,overflow:'hidden'}}>
  <div style={{width:`${Math.round(100*clamp(value))}%`, height:'100%',background:color,borderRadius:height/2}}/>
</div>;

const MoneyCounter: React.FC<{f:number}> = ({f}) => {
  const fall = show(f, 62, 28);
  return <div style={{display:'flex',flexDirection:'column',gap:20}}>
    <div style={{...pane,...drift(f,0)}}>
      <div style={{display:'flex',justifyContent:'space-between',...small}}>
        <span>PIX / FIRST VIDEO</span><span style={{color:cyan}}>UPLOAD COMPLETE</span>
      </div>
      <div style={{fontSize:35,fontWeight:900,margin:'24px 0'}}>Why Your Phone Storage Keeps Filling Up</div>
      <Progress value={show(f,5,45)} color={yellow}/>
    </div>
    <div style={{...pane, textAlign:'center', transform:`translateY(${fall*8}px) scale(${1-fall*0.13})`,
      opacity:1-fall, minHeight:124}}>
      <div style={small}>INSTANT MONEY? <span style={{fontSize:15}}>IMAGINARY COUNTER</span></div>
      <div style={{fontSize:65,fontWeight:900,color:yellow}}>$0.00</div>
    </div>
    <div style={{opacity:show(f,74,22),fontSize:34,fontWeight:850,color:yellow,textAlign:'center'}}>
      What actually happens after Upload?
    </div>
  </div>;
};
const AudienceCards: React.FC<{f:number}> = ({f}) => {
  const labels = ['Gaming','Cooking','Space','Phone reviews','Broken printers'];
  return <div style={{display:'flex',flexDirection:'column',gap:24}}>
    <div style={{...small,textAlign:'center'}}>FIVE TOPICS → ONE VIEWER PROMISE</div>
    <div style={{height:165,position:'relative'}}>
      {labels.map((label,i) => {
        const settle=show(f,38+i*9,27);
        const spread=[[-13,-13],[150,65],[345,-5],[480,80],[640,0]][i];
        return <div key={label} style={{
          position:'absolute',left:spread[0]*(1-settle)+i*176*settle,
          top:spread[1]*(1-settle)+35*settle,
          width:170, textAlign:'center', background:card,border:`2px solid ${settle>0.8?cyan:border}`,
          padding:'17px 7px',borderRadius:15,opacity:show(f,i*8),
          transform:`rotate(${(1-settle)*(i%2?-7:8)}deg)`,fontSize:20,fontWeight:750,
        }}>{label}</div>;
      })}
    </div>
    <div style={{...pane,opacity:show(f,90,23),textAlign:'center'}}>
      <div style={{fontSize:19,color:cyan,letterSpacing:2}}>AUDIENCE</div>
      <div style={{fontSize:35,fontWeight:900,margin:'10px 0'}}>People who want tech explained simply</div>
      <div style={{fontSize:24,color:muted}}>One real problem · One clear takeaway</div>
    </div>
  </div>;
};
const Discovery: React.FC<{f:number}> = ({f}) => (
  <div>
    <div style={{...pane,textAlign:'center',fontSize:28,fontWeight:800,marginBottom:32}}>
      <span style={{color:yellow}}>ONE UPLOAD</span> · THREE VIEWING SITUATIONS
    </div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:15}}>
      {[
        {n:'HOME',why:'Viewer interests',hint:'Browsing'},
        {n:'SUGGESTED',why:'What is playing',hint:'Next video'},
        {n:'SEARCH',why:'The viewer’s query',hint:'Looking for help'},
      ].map((x,i)=><div key={x.n} style={{
        ...pane, padding:19,height:277,...drift(f,i+1),
        borderColor:i===2?yellow:cyan,
      }}>
        <div style={{fontSize:18,color:i===2?yellow:cyan,letterSpacing:2,fontWeight:800}}>{x.n}</div>
        <div style={{height:76,margin:'20px 0',borderRadius:10,background:'#1e3852',
          display:'flex',alignItems:'center',justifyContent:'center',fontSize:39,color:text}}>▶</div>
        <div style={{fontSize:23,fontWeight:800}}>{x.why}</div>
        <div style={{fontSize:19,color:muted,marginTop:6}}>{x.hint}</div>
      </div>)}
    </div>
    <div style={{marginTop:26,opacity:show(f,90,25),fontSize:23,color:muted,textAlign:'center'}}>
      Responses and satisfaction matter. There is no universal magic score.
    </div>
  </div>
);
const Packaging: React.FC<{f:number}> = ({f}) => {
  const replace=show(f,48,20);
  return <div style={{display:'flex',flexDirection:'column',gap:20}}>
    <div style={{...small}}>TITLE + THUMBNAIL + OPENING SHOULD MAKE ONE HONEST PROMISE</div>
    <div style={{...pane,minHeight:140}}>
      <div style={{fontSize:17,color:muted,letterSpacing:3}}>VIDEO TITLE</div>
      <div style={{fontSize:34,fontWeight:850,marginTop:20,
        color:replace>0.6?cyan:text}}>
        {replace>0.5?'Why Your Phone Storage Keeps Filling Up':'My Thoughts About Stuff on My Phone'}
      </div>
    </div>
    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:18}}>
      <div style={{...pane,background:'#192943',display:'flex',gap:18,alignItems:'center'}}>
        <div style={{width:75,height:116,borderRadius:12,border:`4px solid ${yellow}`,
          display:'flex',alignItems:'end',padding:9}}>
          <div style={{background:yellow,width:'100%',height:`${22+show(f,40,35)*75}%`}}/>
        </div>
        <div style={{fontSize:26,fontWeight:850}}>STORAGE<br/>FULL</div>
      </div>
      <div style={{...pane,background:'#142f32',display:'flex',flexDirection:'column',justifyContent:'center',
        opacity:show(f,58,20)}}>
        <div style={{fontSize:18,color:cyan,letterSpacing:2}}>OPEN WITH THE PROBLEM</div>
        <div style={{fontSize:26,marginTop:16,fontWeight:750}}>“What is filling up your phone?”</div>
      </div>
    </div>
    <div style={{fontSize:24,color:muted,textAlign:'center',opacity:show(f,84,18)}}>
      Then show the actual storage categories and a useful next step.
    </div>
  </div>;
};
const Gate: React.FC<{kind:'early'|'ads';f:number}> = ({kind,f}) => {
  const early=kind==='early';
  return <div style={{...pane,borderColor:early?cyan:yellow,padding:'17px 23px',
    opacity:show(f,early?4:54,25),height:243}}>
    <div style={{display:'flex',alignItems:'baseline',justifyContent:'space-between'}}>
      <div style={{fontSize:18,color:early?cyan:yellow,fontWeight:850,letterSpacing:1.3}}>
        {early?'EARLY ACCESS · ELIGIBLE COUNTRIES':'AD REVENUE SHARING'}
      </div>
      <span style={{fontSize:32,fontWeight:900,color:early?cyan:yellow}}>
        {early?'500':'1,000'} <span style={{fontSize:15,color:muted}}>subscribers</span>
      </span>
    </div>
    <div style={{fontSize:21,marginTop:13,lineHeight:1.37,fontWeight:650}}>
      {early?<div>3 public uploads / 90 days <span style={{color:muted,fontSize:15}}>AND</span></div>:null}
      <div>{early?'3,000':'4,000'} valid public watch hours / 12 months</div>
      <div style={{color:early?cyan:yellow,fontWeight:900,margin:'1px 0'}}>OR</div>
      <div>{early?'3M':'10M'} valid public Shorts views / 90 days</div>
    </div>
    <div style={{fontSize:17,color:muted,marginTop:10}}>
      {early?'Eligible fan funding / selected Shopping':'Application, approval and feature requirements apply'}
    </div>
  </div>;
};
const Gates:React.FC<{f:number}> = ({f}) => <div style={{display:'flex',flexDirection:'column',gap:14}}>
  <Gate kind="early" f={f}/><Gate kind="ads" f={f}/>
  <div style={{fontSize:17,textAlign:'center',color:muted}}>Eligibility is not automatic approval. Rules and location requirements apply.</div>
</div>;
const Earnings:React.FC<{f:number}> = ({f}) => <div style={{...pane,padding:26}}>
  <div style={{...small,color:cyan}}>HYPOTHETICAL EXAMPLE · NOT AN EARNINGS FORECAST</div>
  <div style={{fontSize:69,fontWeight:900,margin:'12px 0 18px'}}>
    50,000 <span style={{fontSize:24,color:muted}}>views</span>
  </div>
  {[
    {rpm:'$2 RPM',cash:'$100',color:cyan,d:25,w:0.40},
    {rpm:'$5 RPM',cash:'$250',color:yellow,d:55,w:1.0},
  ].map(x=><div key={x.rpm} style={{display:'grid',gridTemplateColumns:'146px 1fr 115px',
    alignItems:'center',gap:18,margin:'23px 0',opacity:show(f,x.d,15)}}>
    <div style={{fontSize:27,fontWeight:800}}>{x.rpm}</div>
    <Progress value={x.w*show(f,x.d,30)} color={x.color} height={23}/>
    <div style={{fontSize:33,fontWeight:900,color:x.color,textAlign:'right'}}>{x.cash}</div>
  </div>)}
  <div style={{height:1,background:border,margin:'15px 0 21px'}}/>
  <div style={{fontSize:25,color:muted}}>Views ÷ 1,000 × RPM = hypothetical revenue</div>
  <div style={{fontSize:17,color:muted,marginTop:12}}>Before creator expenses or taxes · Actual revenue varies</div>
</div>;
const Income:React.FC<{f:number}> = ({f}) => {
  const values=[
    ['Premium viewing','Eligibility applies'],['Memberships','Benefits to deliver'],
    ['Sponsorships','Brand agreement'],['Affiliate offers','Transparent disclosure'],
    ['Own products','A real product to support'],
  ];
  return <div style={{display:'flex',flexDirection:'column',gap:25}}>
    <div style={{...pane,textAlign:'center',fontSize:30,fontWeight:850}}>ADS ARE ONLY ONE PATH</div>
    <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:15}}>
      {values.map(([name,detail],i)=><div key={name} style={{
        ...pane,padding:18,borderColor:i%2?yellow:cyan,opacity:show(f,15+i*14,18),
        transform:`translateX(${(1-show(f,15+i*14,18))*24}px)`,
      }}>
        <div style={{fontSize:23,fontWeight:850}}>{name}</div>
        <div style={{fontSize:17,color:muted,marginTop:9}}>{detail}</div>
      </div>)}
    </div>
    <div style={{fontSize:21,color:muted,textAlign:'center'}}>
      None are automatic rewards for uploading.
    </div>
  </div>;
};
const ActionPlan:React.FC<{f:number;originality:boolean}> = ({f,originality}) => (
  <div style={{display:'flex',flexDirection:'column',gap:20}}>
    {originality?<div style={{...pane}}>
      <div style={{fontSize:20,letterSpacing:2,color:cyan}}>ORIGINAL VALUE</div>
      <div style={{fontSize:34,fontWeight:850,marginTop:20}}>Research → Explain → Illustrate</div>
      <div style={{fontSize:22,color:muted,marginTop:17}}>
        AI can assist. Reused clips, mass-produced filler and copyrighted media are not a shortcut.
      </div>
    </div>:<>
      <div style={{...small}}>THE FIRST-MONTH IMPROVEMENT LOOP</div>
      <div style={{display:'grid',gridTemplateColumns:'repeat(2,1fr)',gap:16}}>
        {[
          ['01','Choose an audience'],['02','Publish useful original videos'],
          ['03','Review real results'],['04','Improve the next upload'],
        ].map(([n,t],i)=><div key={n} style={{
          ...pane, ...drift(f,i+1), display:'flex',alignItems:'center',gap:19,padding:'25px 18px',
        }}><span style={{fontSize:34,color:i%2?yellow:cyan,fontWeight:900}}>{n}</span>
          <span style={{fontSize:23,fontWeight:800}}>{t}</span></div>)}
      </div>
      <div style={{...pane,borderColor:yellow,opacity:show(f,90,20)}}>
        <div style={{fontSize:18,color:yellow,letterSpacing:3}}>PIX'S NEXT VIDEO · NOT A MONEY COUNTER</div>
        <div style={{fontSize:32,fontWeight:900,marginTop:10}}>Why Your Phone Storage Keeps Filling Up</div>
      </div>
    </>}
  </div>
);

export type JourneyVisualsProps = {
  beat: number;
  chapter?: number;
  localFrame: number;
};

export const JourneyVisualAid:React.FC<JourneyVisualsProps> = ({beat,localFrame,chapter}) => {
  const f=Math.max(0,localFrame);
  switch(beat) {
    case 1: return <MoneyCounter f={f}/>;
    case 2: return <AudienceCards f={f}/>;
    case 3: return <Discovery f={f}/>;
    case 4: return <Packaging f={f}/>;
    case 5: return <Gates f={f}/>;
    case 6: return <Earnings f={f}/>;
    case 7: return <Income f={f}/>;
    case 8: return <ActionPlan f={f} originality={chapter===8}/>;
    default: return null;
  }
};

/** Asset-free visual-development composition: eight original graphical treatments. */
export const YouTubeJourneyVisualBoard:React.FC = () => {
  const frame=useCurrentFrame();
  const seconds=frame/visualAid.format.fps;
  const current=STORYBOARD_BEATS.find(b=>seconds>=b.startSeconds&&seconds<b.endSeconds)
    ?? STORYBOARD_BEATS[STORYBOARD_BEATS.length-1];
  return <AbsoluteFill style={{background:ink,color:text,fontFamily:'Inter'}}>
    <div style={{position:'absolute',inset:0,
      backgroundImage:'radial-gradient(ellipse at 50% 40%, #12324b 0%, transparent 68%)'}}/>
    <div style={{position:'absolute',left:64,top:48,right:64,display:'flex',
      justifyContent:'space-between',fontSize:18,color:muted,letterSpacing:2}}>
      <span>URFAVXBF × PIX / YOUTUBE BEGINNER JOURNEY</span>
      <span>ORIGINAL VISUAL DEVELOPMENT · 16:9</span>
    </div>
    <div style={{position:'absolute',left:64,top:114,right:64,
      fontSize:55,fontWeight:900}}>{current.label}</div>
    <div style={{position:'absolute',left:515,top:241,width:890}}>
      <JourneyVisualAid beat={current.index} localFrame={frame-current.startSeconds*30}
        chapter={current.index}/>
    </div>
    <div style={{position:'absolute',left:64,top:355,width:414,
      fontSize:22,color:yellow,textAlign:'center'}}>URFAVXBF<br/><span style={{fontSize:15,color:muted}}>Approved portrait asset required</span></div>
    <div style={{position:'absolute',right:64,top:355,width:414,
      fontSize:22,color:cyan,textAlign:'center'}}>PIX<br/><span style={{fontSize:15,color:muted}}>Approved portrait asset required</span></div>
    <div style={{position:'absolute',bottom:120,left:64,right:64,display:'flex',
      justifyContent:'space-between',fontSize:26,color:muted}}>
      <span>{current.story}</span>
    </div>
    <div style={{position:'absolute',bottom:43,left:64,right:64,display:'flex',
      justifyContent:'space-between',fontSize:17,letterSpacing:1.2,color:muted}}>
      <span>STORYBOARD TIMING IS EDITORIAL · NO NARRATION</span>
      <span>BEAT {String(current.index).padStart(2,'0')} / 08</span>
    </div>
  </AbsoluteFill>;
};
