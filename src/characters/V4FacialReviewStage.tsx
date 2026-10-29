import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {V4FacialPortrait} from './V4FacialPortrait';
import type {CharacterId,VoiceEvent} from './CharacterPuppet';
import type {V4Expression,V4ExpressionCue,V4MouthCue} from './V4FacialController';

export const V4_FACIAL_REVIEW_FRAMES=540;
const HOST:V4Expression[]=['neutral','happy','thinking','surprised','focused','curious'];
const PIX:V4Expression[]=['neutral','happy','curious','surprised','excited','sleepy'];

/**
 * Assetless preview shows only state labels, NOT finished art.
 * With real art, render ONLY when V4 PNGs pass alignment QA and owner approval.
 */
export type V4FacialReviewProps={
  assetsReady:boolean;
  artApproved:boolean;
  voiceEvents?:VoiceEvent[];
  mouthCues?:Partial<Record<CharacterId,V4MouthCue[]>>;
};
const Card:React.FC<{
  id:CharacterId;state:V4Expression;frame:number;
  ready:boolean;approved:boolean;
  voiceEvents:VoiceEvent[];mouthCues:V4MouthCue[];
}> = ({id,state,frame,ready,approved,voiceEvents,mouthCues})=>{
  const accent=id==='urfavxbf'?'#6ffb8b':'#70e8ff';
  const expressionCues:V4ExpressionCue[]=[{
    atFrame:Math.floor(frame/90)*90,durationFrames:90,expression:state,
  }];
  return <div style={{width:770,display:'flex',flexDirection:'column',gap:20,alignItems:'center'}}>
    <div style={{fontSize:28,fontWeight:900,color:accent,letterSpacing:3}}>
      {id==='urfavxbf'?'URFAVXBF · DARK GREEN':'PIX · CYAN / PURPLE'}
    </div>
    <V4FacialPortrait id={id} width={660} height={660}
      assetsReady={ready} artApproved={approved}
      voiceEvents={voiceEvents} expressionCues={expressionCues}
      mouthCues={mouthCues} showDebug/>
    <div style={{fontSize:22,color:'#c5dfe0'}}>Expression requested: {state}</div>
  </div>;
};
export const V4FacialReviewStage:React.FC<V4FacialReviewProps>=({
  assetsReady,artApproved,voiceEvents=[],mouthCues={},
})=>{
  const frame=useCurrentFrame();
  const index=Math.min(5,Math.floor(frame/90));
  return <AbsoluteFill style={{
    fontFamily:'system-ui',color:'#edfff7',overflow:'hidden',
    background:'radial-gradient(circle at 50% 45%,#163d35,#060d19 78%)',
  }}>
    <div style={{padding:'35px 75px',fontSize:38,fontWeight:900,letterSpacing:3}}>
      V4 · FACIAL EXPRESSION SYSTEM
    </div>
    <div style={{display:'flex',justifyContent:'space-around',
      alignItems:'center',marginTop:30}}>
      <Card id="urfavxbf" state={HOST[index]} frame={frame}
        ready={assetsReady} approved={artApproved} voiceEvents={voiceEvents}
        mouthCues={mouthCues.urfavxbf??[]}/>
      <Card id="pix" state={PIX[index]} frame={frame}
        ready={assetsReady} approved={artApproved} voiceEvents={voiceEvents}
        mouthCues={mouthCues.pix??[]}/>
    </div>
    <div style={{position:'absolute',bottom:29,textAlign:'center',width:'100%',
      fontSize:19,color:'#a6bfc2',letterSpacing:1}}>
      DESIGN STATES ONLY · NEW 512² FACE ART REQUIRED · NO V2 PIXELS · NO PHONEME CLAIMS
    </div>
  </AbsoluteFill>;
};
