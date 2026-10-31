import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {FX_ADVANCED} from './AdvancedEffects';
import {useFxSource} from '../shared';

/** Unbranded full-bleed preview of every new cinematic FX over real video/mattes. */
export const advancedShowcaseFrames=()=>FX_ADVANCED.reduce((n,x)=>n+x.duration,0);
export const AdvancedFxShowcase:React.FC=()=>{
 const {frames}=useFxSource();
 let at=0;
 return <AbsoluteFill style={{background:'#000',overflow:'hidden'}}>
 {FX_ADVANCED.map((effect,i)=>{
    const start=at;at+=effect.duration;
    const sourceSpan=Math.max(1,frames-effect.duration-20);
    const from=(i*13)%sourceSpan;
    return <Sequence key={effect.id} from={start} durationInFrames={effect.duration}>
      <effect.Component from={from}/>
    </Sequence>;
 })}
 </AbsoluteFill>;
};
export {FX_ADVANCED} from './AdvancedEffects';
