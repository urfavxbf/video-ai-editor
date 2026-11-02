import React from 'react';
import {Img,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import spriteManifest from '../../characters/8bit-host-sprite-manifest.json';
import type {CharacterId,BodyGesture,CharacterReaction} from './CharacterPuppet';

const HOST_ACTIONS=spriteManifest.characters.urfavxbf.actions;
export type HostSpriteAction=keyof typeof HOST_ACTIONS;
export const HOST_SPRITE_FPS=spriteManifest.frameRate;
export const HOST_SPRITE_PATH='characters/8bit-host/urfavxbf';
const HOST_ALIASES:Record<string,HostSpriteAction>={
  happy:'celebrate',point_side:'point_object',point:'point_object',
  idle:'idle',talk:'talk',point_camera:'point_camera',surprised:'surprised',
};
export const hostFramePath=(action:HostSpriteAction,index:number):string=>{
  const count=HOST_ACTIONS[action].frames;
  if(!Number.isSafeInteger(index)||index<0||index>=count)throw new Error('Invalid host sprite frame');
  return `${HOST_SPRITE_PATH}/${action}/frame-${String(index).padStart(2,'0')}.svg`;
};
export const hostSpriteFrame=(action:HostSpriteAction,frame:number,videoFps:number):number=>{
  if(!Number.isFinite(frame)||!Number.isFinite(videoFps)||videoFps<=0)throw new Error('Invalid host animation time');
  const {frames,loop}=HOST_ACTIONS[action];
  const raw=Math.max(0,Math.floor(frame*HOST_SPRITE_FPS/videoFps));
  return loop?raw%frames:Math.min(raw,frames-1);
};
export const hostActionFor=(speaking:boolean,gesture:BodyGesture='idle',reaction?:CharacterReaction):HostSpriteAction=>{
  if(reaction==='surprised')return 'surprised';
  if(reaction==='curious')return 'think';
  if(reaction==='excited'||gesture==='celebrate')return 'celebrate';
  if(gesture==='walk')return 'walk';
  if(gesture==='point')return 'point_object';
  if(gesture==='explain')return 'explain';
  return speaking?'talk':'idle';
};

/** PIX retains the original approved 7 transparent PNG poses. */
export const PIXEL_POSE_PATHS={
  pix:{
    idle:'characters/pixel-default/pix/idle.png',
    curious:'characters/pixel-default/pix/curious.png',
    talk:'characters/pixel-default/pix/talk.png',
    point:'characters/pixel-default/pix/point.png',
    happy:'characters/pixel-default/pix/happy.png',
    question:'characters/pixel-default/pix/question.png',
    surprised:'characters/pixel-default/pix/surprised.png',
  }
} as const;
export type PixelPoseId = HostSpriteAction | keyof typeof PIXEL_POSE_PATHS.pix;
export const choosePixelPose=(id:CharacterId,speaking:boolean,gesture:BodyGesture='idle',reaction?:CharacterReaction):string=>{
  if(id==='urfavxbf')return hostActionFor(speaking,gesture,reaction);
  if(reaction==='surprised')return 'surprised';
  if(reaction==='excited'||gesture==='celebrate')return 'happy';
  if(reaction==='curious')return 'question';
  if(gesture==='point')return 'point';
  return speaking?'talk':'idle';
};
export type PixelPoseCharacterProps={
  id:CharacterId; speaking:boolean; gesture?:BodyGesture; reaction?:CharacterReaction;
  poseOverride?:string;
  hostAction?:HostSpriteAction;
  startFrame?:number;
  width:number;height:number;left?:number;right?:number;bottom?:number;
};
export const PixelPoseCharacter:React.FC<PixelPoseCharacterProps>=({
 id,speaking,gesture='idle',reaction,poseOverride,hostAction,startFrame=0,width,height,left,right,bottom=0,
})=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig();
 let pose:string,source:string,animation:'svg-frames'|'png-pose'='png-pose';
 if(id==='urfavxbf'){
   if(poseOverride&&!HOST_ALIASES[poseOverride]&&!(poseOverride in HOST_ACTIONS))
     throw new Error('Unknown 8-bit host pose: '+poseOverride);
   const action:HostSpriteAction=hostAction??(poseOverride
      ?(HOST_ALIASES[poseOverride]??poseOverride) as HostSpriteAction
      :hostActionFor(speaking,gesture,reaction));
   pose=action;
   source=hostFramePath(action,hostSpriteFrame(action,Math.max(0,frame-startFrame),fps));
   animation='svg-frames';
 }else{
   pose=poseOverride??choosePixelPose(id,speaking,gesture,reaction);
   const path=(PIXEL_POSE_PATHS.pix as Record<string,string>)[pose];
   if(!path)throw new Error('Unknown PIX pose: '+pose);
   source=path;
 }
 const y=Math.sin(frame/30*(id==='pix'?2.15:1.85)+(id==='pix'?1:0))*2.4;
 return <div data-character={id} data-pose={pose} data-animation={animation}
  style={{position:'absolute',width,height,left,right,bottom,transform:`translateY(${y}px)`,pointerEvents:'none'}}>
  <Img src={staticFile(source)} style={{width:'100%',height:'100%',
    objectFit:'contain',imageRendering:'pixelated'}}/>
 </div>;
};
