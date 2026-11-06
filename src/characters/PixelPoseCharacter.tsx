import React from 'react';
import {Img,staticFile,useCurrentFrame} from 'remotion';
import {OwnerSheetHost,type HostPose} from './word-poses/OwnerSheetHost';
import type {CharacterId,BodyGesture,CharacterReaction} from './CharacterPuppet';

/** Current owner host viewports and retained approved PIX images; no old-art fallback. */
export const PIXEL_POSE_PATHS={
  urfavxbf:{
    front:'characters/urfavxbf-8bit/owner-sheet.jpg',
    'three-quarter':'characters/urfavxbf-8bit/owner-sheet.jpg',
    side:'characters/urfavxbf-8bit/owner-sheet.jpg',
    back:'characters/urfavxbf-8bit/owner-sheet.jpg',
    waving:'characters/urfavxbf-8bit/owner-sheet.jpg',
    pointing:'characters/urfavxbf-8bit/owner-sheet.jpg',
    explaining:'characters/urfavxbf-8bit/owner-sheet.jpg',
    'thumbs-up':'characters/urfavxbf-8bit/owner-sheet.jpg',
    surprised:'characters/urfavxbf-8bit/owner-sheet.jpg',
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
  if(reaction==='excited'||gesture==='celebrate')return id==='pix'?'happy':'thumbs-up';
  if(id==='pix'){
    if(reaction==='curious')return 'question';
    if(gesture==='point')return 'point';
    return speaking?'talk':'idle';
  }
  if(gesture==='point')return 'pointing';
  if(gesture==='explain'&&speaking)return 'explaining';
  return speaking?'explaining':'front';
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
/** Host is explicitly white-backed; PIX retains transparent PNGs. */
export const PixelPoseCharacter:React.FC<PixelPoseCharacterProps>=({
 id,speaking,gesture='idle',reaction,poseOverride,width,height,left,right,bottom=0,
})=>{
 const frame=useCurrentFrame();
 const requested=poseOverride??choosePixelPose(id,speaking,gesture,reaction);
 const aliases:Record<string,HostPose>={idle:'front',talk:'explaining',point_camera:'explaining',point_side:'pointing',happy:'thumbs-up'};
 const pose=id==='urfavxbf'?(aliases[requested]??requested):requested;
 const path=(PIXEL_POSE_PATHS[id] as Record<string,string>)[pose];
 if(!path)throw new Error('Unknown pixel pose: '+id+'/'+pose);
 const y=Math.sin(frame/30*(id==='pix'?2.15:1.85)+(id==='pix'?1:0))*2.4;
 return <div data-character={id} data-pose={pose}
  style={{position:'absolute',width,height,left,right,bottom,
    transform:`translateY(${y}px)`,pointerEvents:'none'}}>
  {id==='urfavxbf'?<div style={{position:'absolute',bottom:0,left:'50%',translate:'-50% 0px',background:'#fff',borderRadius:16,padding:8}}><OwnerSheetHost pose={pose as HostPose} height={Math.min(height-16,(width-16)*1.15)}/></div>:<Img src={staticFile(path)} style={{width:'100%',height:'100%',
    objectFit:'contain',imageRendering:'pixelated'}}/>}
 </div>;
};
