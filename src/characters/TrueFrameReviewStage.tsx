import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {TrueFrameActionSprite} from './TrueFrameActionSprite';

/** Smoke-only workbench. Preview without sprites shows the pending-art gate. */
export type TrueFrameReviewProps={
  assetsReady:boolean;
  artApproved:boolean;
  urfavxbfAction:'point_camera'|'walk'|'talk';
  pixAction:'assist_point'|'walk'|'talk';
  hostFrames:number;
  pixFrames:number;
};
export const TrueFrameReviewStage:React.FC<TrueFrameReviewProps>=({
  assetsReady,artApproved,urfavxbfAction,pixAction,hostFrames,pixFrames,
})=>{
  const frame=useCurrentFrame();
  return <AbsoluteFill style={{background:'radial-gradient(ellipse at center,#16372e,#060e1c)',
    color:'#ecfff5',fontFamily:'Inter'}}>
    <div style={{position:'absolute',left:80,top:55,fontSize:42,fontWeight:900,letterSpacing:2}}>
      TRUE FRAME-BY-FRAME ANIMATION · SOURCE ART REVIEW
    </div>
    <div style={{position:'absolute',top:184,left:80}}>
      <TrueFrameActionSprite character="urfavxbf" action={urfavxbfAction}
        width={730} height={700} frameCount={hostFrames} fps={12}
        assetsReady={assetsReady} artApproved={artApproved} reviewDraft/>
    </div>
    <div style={{position:'absolute',top:184,right:80}}>
      <TrueFrameActionSprite character="pix" action={pixAction}
        width={730} height={700} frameCount={pixFrames} fps={12}
        assetsReady={assetsReady} artApproved={artApproved} reviewDraft/>
    </div>
    <div style={{position:'absolute',bottom:30,left:80,right:80,textAlign:'center',
      letterSpacing:1,fontSize:18,color:'#a5c9cb'}}>
      ZERO-BUDGET · NO CUTOUT TRANSFORMS · NO AUTOMATIC PAID GENERATION
    </div>
  </AbsoluteFill>;
};
