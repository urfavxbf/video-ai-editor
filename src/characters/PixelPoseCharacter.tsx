import React from 'react';
import {Img,staticFile,useCurrentFrame} from 'remotion';
import type {CharacterId,BodyGesture,CharacterReaction} from './CharacterPuppet';

/** Exact approved pose filenames; no legacy model fallback or crop-from-sheet. */
export const PIXEL_POSE_PATHS={
  urfavxbf:{
    idle:'characters/pixel-default/urfavxbf/idle.png',
    talk:'characters/pixel-default/urfavxbf/talk.png',
    point_camera:'characters/pixel-default/urfavxbf/point_camera.png',
    point_side:'characters/pixel-default/urfavxbf/point_side.png',
    happy:'characters/pixel-default/urfavxbf/happy.png',
    surprised:'characters/pixel-default/urfavxbf/surprised.png',
  },
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
export type PixelPoseId = keyof typeof PIXEL_POSE_PATHS.urfavxbf | keyof typeof PIXEL_POSE_PATHS.pix;

/** Pure deterministic pose selection. Speech is a pose swap, NOT phoneme lip-sync. */
export const choosePixelPose=(id:CharacterId,speaking:boolean,gesture:BodyGesture='idle',reaction?:CharacterReaction):string=>{
  if(reaction==='surprised')return 'surprised';
  if(reaction==='excited'||gesture==='celebrate')return 'happy';
  if(id==='pix'){
    if(reaction==='curious')return 'question';
    if(gesture==='point')return 'point';
    return speaking?'talk':'idle';
  }
  if(gesture==='point')return 'point_side';
  if(gesture==='explain'&&speaking)return 'point_camera';
  return speaking?'talk':'idle';
};
export type PixelPoseCharacterProps={
  id:CharacterId;
  speaking:boolean;
  gesture?:BodyGesture;
  reaction?:CharacterReaction;
  /** For storyboards / explicitly timed scenes. Enforced against character's pose registry. */
  poseOverride?:string;
  width:number;height:number;left?:number;right?:number;bottom?:number;
};
/** Independent high-resolution transparent PNGs, crisp pixel edges on enlargement. */
export const PixelPoseCharacter:React.FC<PixelPoseCharacterProps>=({
 id,speaking,gesture='idle',reaction,poseOverride,width,height,left,right,bottom=0,
})=>{
 const frame=useCurrentFrame();
 const pose=poseOverride??choosePixelPose(id,speaking,gesture,reaction);
 const path=(PIXEL_POSE_PATHS[id] as Record<string,string>)[pose];
 if(!path)throw new Error('Unknown pixel pose: '+id+'/'+pose);
 const y=Math.sin(frame/30*(id==='pix'?2.15:1.85)+(id==='pix'?1:0))*2.4;
 return <div data-character={id} data-pose={pose}
  style={{position:'absolute',width,height,left,right,bottom,
    transform:`translateY(${y}px)`,pointerEvents:'none'}}>
  <Img src={staticFile(path)} style={{width:'100%',height:'100%',
    objectFit:'contain',imageRendering:'pixelated'}}/>
 </div>;
};
