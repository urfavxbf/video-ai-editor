import React from 'react';
import {useCurrentFrame} from 'remotion';
import {type CharacterId, type VoiceEvent} from './CharacterPuppet';
import {HeroAnimationPlayer,requireRenderableHeroAnimation} from './FullAnimationLibrary';

/**
 * Animation-director cue engine for reusable assets and newly authored frames.
 * Refuses missing body cycles/visemes; does not fake them with joint rotations.
 * Editor supplies approved clip IDs and exact timing on a global 30fps timeline.
 */
export type HeroAnimationCue={
  action:string;
  startFrame:number;
  durationFrames:number;
  /** Number of frames used to fade between already-approved animation frames. */
  blendFrames?:number;
};
export type HeroAnimationTimelineProps={
  id:CharacterId;
  cues:HeroAnimationCue[];
  width:number;
  height:number;
  assetsReady:boolean;
  voiceEvents?:VoiceEvent[];
};
export type ActiveCue={
  current:HeroAnimationCue;
  previous?:HeroAnimationCue;
  opacity:number;
};

export const validateHeroCues=(id:CharacterId,cues:HeroAnimationCue[])=>{
  let previousEnd=0;
  for(const [index,cue] of cues.entries()){
    if(!Number.isInteger(cue.startFrame)||cue.startFrame<0||
       !Number.isInteger(cue.durationFrames)||cue.durationFrames<=0||
       (cue.blendFrames!==undefined &&
         (!Number.isInteger(cue.blendFrames)||cue.blendFrames<0||cue.blendFrames>12))){
      throw new Error(`${id}: invalid animation cue at index ${index}`);
    }
    if(index>0&&cue.startFrame<previousEnd)
      throw new Error(`${id}: animation cues overlap; use transition blending, not overlapping cues`);
    previousEnd=cue.startFrame+cue.durationFrames;
    requireRenderableHeroAnimation(id,cue.action);
  }
};

export const activeHeroCue=(frame:number,cues:HeroAnimationCue[]):ActiveCue|undefined=>{
  const index=cues.findIndex(c=>frame>=c.startFrame&&frame<c.startFrame+c.durationFrames);
  if(index<0)return undefined;
  const current=cues[index];
  const previous=index>0?cues[index-1]:undefined;
  const blend=Math.min(current.blendFrames??5, current.durationFrames);
  const elapsed=frame-current.startFrame;
  const t=blend>0 ? Math.min(1,elapsed/blend) : 1;
  const opacity=t*t*(3-2*t);
  return {current,previous:previous&&previous.startFrame+previous.durationFrames===current.startFrame?
    previous:undefined,opacity};
};

export const HeroAnimationTimeline:React.FC<HeroAnimationTimelineProps>=({
  id,cues,width,height,assetsReady,voiceEvents=[],
})=>{
  const frame=useCurrentFrame();
  validateHeroCues(id,cues);
  const active=activeHeroCue(frame,cues);
  if(!active)return null;
  const {current,previous,opacity}=active;
  return <div data-character={id} data-cue={current.action} style={{
    position:'relative',width,height,pointerEvents:'none',
  }}>
    {previous&&opacity<1&&<div style={{position:'absolute',inset:0,opacity:1-opacity}}>
      <HeroAnimationPlayer id={id} action={previous.action}
        width={width} height={height} voiceEvents={voiceEvents}
        startFrame={previous.startFrame} assetsReady={assetsReady}/>
    </div>}
    <div style={{position:'absolute',inset:0,opacity:previous?opacity:1}}>
      <HeroAnimationPlayer id={id} action={current.action}
        width={width} height={height} voiceEvents={voiceEvents}
        startFrame={current.startFrame} assetsReady={assetsReady}/>
    </div>
  </div>;
};
