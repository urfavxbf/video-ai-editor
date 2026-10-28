import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {HeroAnimationPlayer,animationCatalog,lookupAnimation} from './FullAnimationLibrary';

/**
 * Strictly real sprites / actual compositing techniques in the canonical pack.
 * NOT a completed full-body-cycle reel. All unavailable keyframe sequences
 * remain asset gated and cannot quietly fall back to cutout rotations.
 */
export type HeroAnimationReviewReelProps={
  assetsReady:boolean;
};
export const HERO_REEL_FRAMES=720;
const HOST=['idle_normal','idle_talking','surprised','glitch_reaction'];
const PIX=['idle_sitting','meow_talk','happy_excited','float'];

export const HeroAnimationReviewReel:React.FC<HeroAnimationReviewReelProps>=({
  assetsReady,
})=>{
  const frame=useCurrentFrame();
  const index=Math.min(3,Math.floor(frame/180));
  const start=index*180;
  const host=HOST[index];
  const pix=PIX[index];
  const palette={background:'#081124',white:'#f1f5ff',gold:'#ffdc28',cyan:'#28e9fc'};
  const card=(id:'urfavxbf'|'pix',action:string,color:string,left:number)=>
    <div style={{
      position:'absolute',left,top:167,width:790,height:705,borderRadius:26,
      border:`2px solid ${color}55`,background:'linear-gradient(165deg,#101d36,#0b172a)',
      overflow:'hidden',boxShadow:`0 20px 80px #0008`,
    }}>
      <div style={{
        position:'absolute',top:26,left:40,fontWeight:950,fontSize:34,color,
        letterSpacing:2,
      }}>{id==='urfavxbf'?'URFAVXBF':'PIX'}</div>
      <div style={{position:'absolute',left:80,right:80,top:84,height:510,
        display:'flex',alignItems:'center',justifyContent:'center'}}>
        <HeroAnimationPlayer id={id} action={action}
          width={570} height={470} startFrame={start} assetsReady={assetsReady}/>
      </div>
      <div style={{
        position:'absolute',left:40,right:40,bottom:32,
        borderTop:'1px solid #54647a',paddingTop:24,
      }}>
        <div style={{fontSize:23,fontWeight:850,letterSpacing:0.8}}>{lookupAnimation(id,action).label}</div>
        <div style={{fontSize:17,color:'#9bafcb',marginTop:7}}>
          {lookupAnimation(id,action).assetClass==='existing-head-loop'?'REAL 8-FRAME HEAD LOOP':
           lookupAnimation(id,action).assetClass==='existing-expression'?'REAL FACIAL EXPRESSION PORTRAIT':
           'FULL-BODY COMPOSITING VFX — NOT NEW KEYFRAME ART'}
        </div>
      </div>
    </div>;
  return <AbsoluteFill style={{background:palette.background,color:palette.white,fontFamily:'Inter'}}>
    <div style={{position:'absolute',top:47,left:72,fontSize:39,fontWeight:950,letterSpacing:1}}>
      URFAVXBF <span style={{color:palette.cyan}}>×</span> PIX
      <span style={{color:'#8da6c8',fontSize:22,marginLeft:35,fontWeight:500}}>FACIAL SPRITE REVIEW</span>
    </div>
    <div style={{position:'absolute',right:74,top:53,color:'#aabbd3',fontSize:19}}>
      16:9 · 30 FPS · APPROVED ART ONLY
    </div>
    {card('urfavxbf',host,palette.gold,84)}
    {card('pix',pix,palette.cyan,1045)}
    <div style={{position:'absolute',left:89,right:90,bottom:68,display:'flex',gap:10}}>
      {[0,1,2,3].map(i=><div key={i}
        style={{height:7,background:i===index?palette.cyan:'#283a52',flex:1,borderRadius:4}}/>)}
    </div>
    <div style={{position:'absolute',left:90,right:90,bottom:25,textAlign:'center',
      color:'#9bafc6',fontSize:15,letterSpacing:1}}>
      THIS IS AN EXISTING SPRITE REVIEW, NOT COMPLETE WALK/RUN/HAIR/VISEME ANIMATION. NEW DRAWINGS ARE STILL REQUIRED.
    </div>
  </AbsoluteFill>;
};
