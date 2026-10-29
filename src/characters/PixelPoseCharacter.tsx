import React from 'react';
import {Img,staticFile,useCurrentFrame} from 'remotion';
import type {CharacterId, BodyGesture, CharacterReaction} from './CharacterPuppet';
export const PIXEL_POSE_PATHS={
 urfavxbf:{idle:'characters/pixel-default/urfavxbf/idle.png',talk:'characters/pixel-default/urfavxbf/talk.png',point_camera:'characters/pixel-default/urfavxbf/point_camera.png',point_side:'characters/pixel-default/urfavxbf/point_side.png',happy:'characters/pixel-default/urfavxbf/happy.png'},
 pix:{idle:'characters/pixel-default/pix/idle.png',curious:'characters/pixel-default/pix/curious.png',talk:'characters/pixel-default/pix/talk.png',point:'characters/pixel-default/pix/point.png',happy:'characters/pixel-default/pix/happy.png'},
} as const;
export const choosePixelPose=(id:CharacterId,speaking:boolean,gesture:BodyGesture='idle',reaction?:CharacterReaction):string=>{
 if(reaction==='excited'||gesture==='celebrate')return 'happy';
 if(id==='pix'){
  if(reaction==='curious'||reaction==='surprised')return 'curious';
  if(gesture==='point')return 'point';
  return speaking?'talk':'idle';
 }
 if(gesture==='point')return 'point_side';
 if(gesture==='explain'&&speaking)return 'point_camera';
 return speaking?'talk':'idle';
};
/** Pose-only system: independent drawings, not a synthetic walk cycle or fake lip-sync. */
export const PixelPoseCharacter:React.FC<{id:CharacterId;speaking:boolean;gesture?:BodyGesture;reaction?:CharacterReaction;width:number;height:number;left?:number;right?:number;bottom?:number;}>=({id,speaking,gesture='idle',reaction,width,height,left,right,bottom=0})=>{
 const frame=useCurrentFrame();
 const pose=choosePixelPose(id,speaking,gesture,reaction);
 const path=(PIXEL_POSE_PATHS[id] as Record<string,string>)[pose];
 if(!path)throw Error('Missing canonical pose for '+id+'/'+pose);
 const y=Math.sin(frame/30*2.0+(id==='pix'?1:0))*2;
 return <div data-character={id} data-pose={pose} style={{position:'absolute',width,height,left,right,bottom,transform:`translateY(${y}px)`,pointerEvents:'none'}}>
  <Img src={staticFile(path)} style={{width:'100%',height:'100%',objectFit:'contain',imageRendering:'pixelated'}} />
 </div>;
};
