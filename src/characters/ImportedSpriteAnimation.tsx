import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';

/** Review external sprites without regeneration, watermark removal or fake poses. */
export type ImportedSpriteAnimationProps={
  character:'urfavxbf'|'pix';
  action:string;
  durationsMs:number[];
  loop:boolean;
  assetsReady:boolean;
  startFrame?:number;
};

export const importedFrameAtTime=(elapsedMs:number,durationsMs:number[],loop:boolean):number=>{
  const durations=durationsMs.map((n)=>Math.max(20,Math.floor(n)));
  if(durations.length===0||durations.length>600||durations.some((n)=>!Number.isFinite(n))){
    throw new Error('Expect 1–600 source frames with valid durations');
  }
  const total=durations.reduce((a,b)=>a+b,0);
  const t=loop?Math.max(0,elapsedMs)%total:Math.min(Math.max(0,elapsedMs),total-1);
  let cursor=0;
  for(let i=0;i<durations.length;i++){
    cursor+=durations[i];
    if(t<cursor)return i;
  }
  return durations.length-1;
};

export const ImportedSpriteAnimation:React.FC<ImportedSpriteAnimationProps>=({
  character,action,durationsMs,loop,assetsReady,startFrame=0,
})=>{
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  if(!/^[a-z][a-z0-9_-]{0,48}$/.test(action))throw new Error('Invalid action');
  const index=importedFrameAtTime(Math.max(0,frame-startFrame)*1000/fps,durationsMs,loop);
  const path=`characters/imported/${character}/${action}/${String(index).padStart(3,'0')}.png`;
  return <AbsoluteFill style={{
    background:'radial-gradient(ellipse at center,#13362b,#071118)',
    display:'flex',alignItems:'center',justifyContent:'center',
    fontFamily:'system-ui',color:'#c2ffdc',
  }}>
    {assetsReady
      ? <Img src={staticFile(path)} style={{
          width:750,height:900,objectFit:'contain',imageRendering:'pixelated',
        }}/>
      : <div style={{padding:40,border:'2px dashed #69a58b',borderRadius:12,
          textAlign:'center',fontSize:34}}>
          ASSETS NOT STAGED — {character} / {action}
          <div style={{fontSize:23}}>{durationsMs.length} real source frames awaiting review</div>
        </div>}
    <div style={{position:'absolute',bottom:38,fontSize:22,opacity:.75}}>
      Imported asset review only · no new poses · no watermark removal
    </div>
  </AbsoluteFill>;
};
