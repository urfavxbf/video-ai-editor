import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {CanonicalActionSprite,CANONICAL_ACTIONS} from './CanonicalActionSprite';

export type CanonicalFullBodyReviewProps={assetsReady:boolean;artApproved:boolean};
export const CANONICAL_FULL_BODY_REVIEW_FRAMES=840;

/** The seven full-body actions play sequentially for both canonical models. */
export const CanonicalFullBodyReviewStage:React.FC<CanonicalFullBodyReviewProps>=({
  assetsReady,artApproved
})=>{
  const frame=useCurrentFrame();
  const idx=Math.min(CANONICAL_ACTIONS.length-1,Math.floor(frame/120));
  const action=CANONICAL_ACTIONS[idx];
  return <AbsoluteFill style={{
    overflow:'hidden',fontFamily:'Inter',color:'#f5faf9',
    background:'radial-gradient(ellipse at center,#173e36,#08131f 78%)'
  }}>
    <div style={{position:'absolute',left:64,top:38,fontSize:36,fontWeight:900,letterSpacing:3}}>
      UrFavXBF <span style={{color:'#70e8ff'}}>× PIX</span>
    </div>
    <div style={{position:'absolute',right:64,top:50,fontSize:18,letterSpacing:2}}>
      CANONICAL FULL-BODY MOTION REVIEW · 1920×1080
    </div>
    <div style={{position:'absolute',left:700,top:158,right:700,textAlign:'center',
      color:'#a0f9b1',fontSize:38,fontWeight:900}}>{action.toUpperCase()}</div>
    <div style={{position:'absolute',left:95,top:190}}>
      <CanonicalActionSprite character="urfavxbf" action={action} width={720} height={690}
        assetsReady={assetsReady} artApproved={artApproved} reviewDraft/>
    </div>
    <div style={{position:'absolute',right:95,top:190}}>
      <CanonicalActionSprite character="pix" action={action} width={720} height={690}
        assetsReady={assetsReady} artApproved={artApproved} reviewDraft/>
    </div>
    <div style={{position:'absolute',bottom:40,width:'100%',textAlign:'center',
      fontSize:18,letterSpacing:1,color:'#a0b8c5'}}>
      2.5D CUTOUT TRANSFORMS · NOT NEW DRAWN POSES · NO PHONEME-ACCURATE LIP-SYNC
    </div>
  </AbsoluteFill>;
};
