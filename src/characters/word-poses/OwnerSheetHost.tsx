import React from 'react';
import {Img, staticFile} from 'remotion';
import art from '../../../characters/urfavxbf-8bit-manifest.json';

export type HostPose = keyof typeof art.poses;

/** The owner JPEG stays intact: these are display viewports, not transparent redraws. */
export const OwnerSheetHost: React.FC<{pose:HostPose; height?:number}> = ({pose,height=660}) => {
  const [x,y,w,h]=art.poses[pose].rect;
  const scale=height/h;
  return <div style={{position:'relative',width:w*scale,height,overflow:'hidden'}}>
    <Img src={staticFile(art.source.replace(/^public\//,''))} style={{position:'absolute',width:1280*scale,height:960*scale,left:-x*scale,top:-y*scale,maxWidth:'none',imageRendering:'pixelated'}}/>
  </div>;
};

/** Seeded character-local slices and square debris; never a full-frame flash. */
export const GlitchHost: React.FC<{pose:HostPose;previous:HostPose;age:number;seed:number}> = ({pose,previous,age,seed}) => {
  const active=age>=0&&age<3;
  return <div style={{position:'relative',width:620,height:700,display:'flex',alignItems:'flex-end',justifyContent:'center'}}>
    <div style={{position:'absolute',bottom:0,translate:active?`${age===1?-7:5}px 0px`:'0px 0px'}}><OwnerSheetHost pose={pose}/></div>
    {active&&[0,1,2,3].map(i=><div key={i} style={{position:'absolute',inset:0,display:'flex',alignItems:'flex-end',justifyContent:'center',clipPath:`inset(${12+i*19}% 0 ${83-i*19}% 0)`,translate:`${(i%2?1:-1)*(22-age*6)}px 0px`}}><OwnerSheetHost pose={previous}/></div>)}
    {active&&Array.from({length:18},(_,i)=>{
      const size=8+((i*7+seed)%4)*7;
      return <div key={i} style={{position:'absolute',width:size,height:size,left:70+((i*97+seed*43)%475),top:70+((i*131+seed*19)%570),background:['#1d2b67','#e43848','#ffc740'][i%3],opacity:(3-age)*.22,translate:`${(i%2?1:-1)*(3-age)*8}px 0px`}}/>;
    })}
  </div>;
};
