import React from 'react';
import {Img,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import type {CharacterId,ReactionCue,VoiceEvent} from './CharacterPuppet';
import {v4FaceAt,type V4ExpressionCue,type V4MouthCue} from './V4FacialController';

/**
 * Dedicated V4 layered face, never using or falling back to the V2 PixelGlitch pack.
 * Artists must supply same-canvas 512x512 RGBA base + eye/brow expression + mouth.
 * The base MUST NOT contain baked-in eyes or mouth.
 */
export type V4FacialPortraitProps={
  id:CharacterId;
  width:number;
  height:number;
  assetsReady:boolean;
  artApproved:boolean;
  voiceEvents?:VoiceEvent[];
  reactionCues?:ReactionCue[];
  expressionCues?:V4ExpressionCue[];
  mouthCues?:V4MouthCue[];
  showDebug?:boolean;
};
const V4_BASE='characters/facial-v4';

export const V4FacialPortrait:React.FC<V4FacialPortraitProps>=({
  id,width,height,assetsReady,artApproved,
  voiceEvents=[],reactionCues=[],expressionCues=[],mouthCues=[],
  showDebug=false,
})=>{
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const state=v4FaceAt({id,frame,fps,voiceEvents,reactionCues,expressionCues,mouthCues});
  const approved=assetsReady&&artApproved;
  const accent=id==='urfavxbf'?'#6ffb8b':'#70e8ff';
  const paths=approved?[
    `${V4_BASE}/${id}/base.png`,
    `${V4_BASE}/${id}/expressions/${state.expression}.png`,
    `${V4_BASE}/${id}/mouth/${state.mouth}.png`,
  ]:[];
  return <div data-character={id} data-v4-expression={state.expression}
    data-v4-mouth={state.mouth} data-mouth-alignment={state.alignment}
    data-asset-gate={approved?'approved-v4-only':'v4-assets-pending'}
    style={{width,height,position:'relative',flexShrink:0,overflow:'hidden',
      background:'#071723',border:'2px solid '+accent,borderRadius:24}}>
    {approved ? paths.map((path,i)=>
      <Img key={path} src={staticFile(path)} style={{
        position:'absolute',inset:0,width:'100%',height:'100%',
        objectFit:'contain',imageRendering:'pixelated',zIndex:i,
      }}/>)
      : <div style={{position:'absolute',inset:14,display:'flex',
          flexDirection:'column',justifyContent:'center',alignItems:'center',
          border:'2px dashed '+accent,color:accent,fontFamily:'monospace',
          padding:24,textAlign:'center',fontSize:24,lineHeight:1.45}}>
          NEW V4 FACIAL ART PENDING
          <span style={{fontSize:17,color:'#b0d0cb',marginTop:14}}>
            {id.toUpperCase()} — never substitute legacy V2 artwork
          </span>
        </div>}
    {showDebug&&<div style={{position:'absolute',bottom:14,left:14,right:14,
      background:'#06101fe8',color:'#e8fff3',fontFamily:'monospace',
      fontSize:16,padding:10,zIndex:4}}>
      {state.expression} · {state.mouth} · {state.alignment}
    </div>}
  </div>;
};
