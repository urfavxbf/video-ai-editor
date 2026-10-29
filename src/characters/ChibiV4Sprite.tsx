import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

/**
 * New dark-green/cyan chibi V4 sprites from a SEPARATE generated concept
 * sheet, not old V2 cutouts. Current assets are DRAFT source keyposes.
 * The labels "8F" on the source sheet do not mean eight extracted frames.
 *
 * Binary PNGs live in the private render workspace and are deliberately
 * excluded from the public repository. Never silently fall back to V2.
 */
export const V4_FRAMES = {
  urfavxbf: {
    idle_normal:4, idle_talking:4, walk:5, run:4, jump:3, fall_landing:1,
    crouch_sit:4, sit:3, turn_left:4, turn_right:4, surprised:4, laugh:4,
    serious_focused:3, alert:3, glitch_reaction:5, point_forward:4,
    point_side:4, wave:3, cross_arms:3, hand_on_hip:2,
    thinking_pose:4, talking_gestures:5, glitch_idle:5,
  },
  pix: {
    idle_sitting:3, idle_standing:3, walk:4, run_trot:4, jump_pounce:4,
    sit_to_stand:4, turn_left:3, turn_right:3, head_tilt:3,
    paw_raise_point:3, tail_wag:3, lick_paw:1, stretch:2,
    meow_talk:5, glitch_idle:6, happy_excited:4, curious:3,
    annoyed:3, surprised:3, sleepy:2, glitch_reaction:5,
    appear_glitch:5, disappear_glitch:5, float:5,
  },
} as const;

export type V4Character = keyof typeof V4_FRAMES;
export type V4Action = keyof typeof V4_FRAMES.urfavxbf | keyof typeof V4_FRAMES.pix;
export const V4_PALETTE = {
  urfavxbf:'#6ffb8b',
  pix:'#70e8ff',
} as const;

export const getV4FrameCount = (id:V4Character,action:string):number => {
  const frames = V4_FRAMES[id] as Record<string,number>;
  const found=frames[action];
  if(!Number.isInteger(found) || found<1){
    throw new Error(`New V4 character ${id}/${action}: drawing not in the source sprite pack`);
  }
  return found;
};

export type ChibiV4SpriteProps = {
  id:V4Character;
  action:string;
  width:number;
  height:number;
  startFrame?:number;
  playbackFps?:number;
  /** True ONLY after the new V4 assets have been staged and SHA validated. */
  assetsReady:boolean;
  /** Use source-preserving 128x128 normalized QA poses, staged separately. */
  normalizedReview?:boolean;
};

export const ChibiV4Sprite:React.FC<ChibiV4SpriteProps> = ({
  id,action,width,height,startFrame=0,playbackFps=8,assetsReady,normalizedReview=false,
})=>{
  const currentFrame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const count=getV4FrameCount(id,action);
  const elapsed=Math.max(0,currentFrame-startFrame);
  const frameIndex=Math.floor(elapsed*Math.max(1,playbackFps)/fps);
  // One-shots must stop on their last real drawing; no fake jumps repeating.
  const loop=/^(idle_|walk$|run$|run_trot$|meow_talk$|tail_wag$|glitch_idle$|float$)/.test(action);
  const frame=loop ? frameIndex%count : Math.min(count-1,frameIndex);
  const prefix=normalizedReview?'characters/animation-v4-normalized':'characters/animation-v4';
  const path=`${prefix}/${id}/${action}/${String(frame).padStart(3,'0')}.png`;
  return <div data-character={id} data-v4-action={action}
    data-review-state="source-extracted-draft"
    data-real-drawn-frames={count}
    data-source-variant={normalizedReview?'normalized-qa':'original-draft'}
    style={{width,height,position:'relative',pointerEvents:'none'}}>
    {assetsReady ? <Img src={staticFile(path)} style={{
      width:'100%',height:'100%',objectFit:'contain',
      imageRendering:'pixelated',
    }}/> : <div style={{
      background:'#112a30',border:'2px dashed #528a80',borderRadius:14,
      color:'#c6e9dc',fontFamily:'monospace',textAlign:'center',
      display:'flex',alignItems:'center',justifyContent:'center',
      width:'100%',height:'100%',fontSize:16,padding:18,
    }}>V4 CHIBI ASSETS NOT STAGED
      <div style={{position:'absolute',bottom:20}}>
        {id} / {action} / {count} source poses
      </div>
    </div>}
  </div>;
};
