import React from 'react';
import {Img,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';

/** Only independently authored whole-character PNG frames are allowed. */
export type TrueActionCharacter = 'urfavxbf'|'pix';
export const TRUE_ACTIONS = [
  'idle','talk','point_camera','point_object','assist_point','explain','walk','run','jump',
  'laugh','think','curious','surprised','confused','wave','celebrate','listen','happy_bounce','sleepy',
] as const;
export type TrueActionName = typeof TRUE_ACTIONS[number];
export type TrueFrameSpriteProps = {
  character:TrueActionCharacter;
  action:TrueActionName;
  frameCount:number;
  fps:number;
  width:number;
  height:number;
  /** Real sprites passed alpha/art QA, not merely their reference sheet. */
  assetsReady:boolean;
  /** Human confirms all full-body frames preserve character consistency and motion. */
  artApproved:boolean;
  /** Draft review composition only; renders an explicit NOT APPROVED mark. */
  reviewDraft?:boolean;
  startFrame?:number;
};

export const TrueFrameActionSprite:React.FC<TrueFrameSpriteProps>=({
  character,action,frameCount,fps,width,height,assetsReady,artApproved,reviewDraft=false,startFrame=0,
})=>{
  const frame=useCurrentFrame();
  const {fps:videoFps}=useVideoConfig();
  if(!TRUE_ACTIONS.includes(action))throw new Error('Unknown true sprite action');
  if(!Number.isInteger(frameCount)||frameCount<1||frameCount>120)
    throw new Error('Invalid drawn-frame count');
  if(!Number.isFinite(fps)||fps<=0||fps>30)throw new Error('Invalid drawn-frame fps');
  const index=Math.floor(Math.max(0,frame-startFrame)*fps/videoFps)%frameCount;
  const source=`characters/true-action/${character}/${action}/${String(index).padStart(3,'0')}.png`;
  const show=assetsReady&&(artApproved||reviewDraft);
  return <div data-character={character} data-action={action}
    data-animation-technique="independent-full-body-drawn-frames"
    data-art-approval={artApproved?'approved':'unapproved'}
    style={{position:'relative',width,height,flexShrink:0,overflow:'hidden'}}>
      {show?<Img src={staticFile(source)} style={{width:'100%',height:'100%',objectFit:'contain'}}/>:
        <div style={{width:'100%',height:'100%',display:'flex',alignItems:'center',
          justifyContent:'center',flexDirection:'column',color:'#bcd8d5',
          border:'2px dashed #4a6d70',borderRadius:16,background:'#0b1a25',
          fontSize:22,fontFamily:'monospace',textAlign:'center'}}>
          REAL WHOLE-BODY SPRITE FRAMES PENDING
          <span style={{fontSize:15,marginTop:13}}>{character} / {action}</span>
        </div>}
      {show&&!artApproved?<div style={{position:'absolute',bottom:0,left:0,right:0,
        background:'#121b26e0',color:'#ffd386',padding:10,fontSize:16,
        textAlign:'center',fontFamily:'monospace'}}>
        UNAPPROVED · INDEPENDENT FRAMES NEED MOTION REVIEW
      </div>:null}
    </div>;
};
