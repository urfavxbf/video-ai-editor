import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {ChibiV4Sprite,V4_PALETTE,type V4Character,getV4FrameCount} from './ChibiV4Sprite';

/** New V4 dark-green/cyan chibi artwork review, separate from old V2 episodes. */
export type ChibiV4ReviewProps = {assetsReady:boolean};
export const CHIBI_V4_REVIEW_DURATION=540;
const HOST_ACTIONS=['idle_normal','idle_talking','walk','run','jump','surprised'];
const PIX_ACTIONS=['idle_sitting','meow_talk','walk','run_trot','jump_pounce','happy_excited'];

const Card:React.FC<{
  id:V4Character;
  action:string;
  assetsReady:boolean;
  startFrame:number;
}> = ({id,action,assetsReady,startFrame})=>{
  const hue=V4_PALETTE[id];
  const name=id==='urfavxbf'?'URFAVXBF':'PIX';
  const numFrames=getV4FrameCount(id,action);
  return <div style={{
    width:810,height:745,border:'2px solid '+hue,
    borderRadius:24,background:id==='urfavxbf'?'#0c241e':'#101e33',
    boxShadow:'0 22px 44px #0007',padding:35,
    position:'relative',overflow:'hidden',
  }}>
    <div style={{color:hue,fontWeight:900,fontSize:35,letterSpacing:3}}>{name}</div>
    <div style={{
      position:'absolute',inset:'110px 150px 152px',
      display:'flex',alignItems:'center',justifyContent:'center',
    }}>
      <ChibiV4Sprite id={id} action={action} width={450} height={520}
        startFrame={startFrame} assetsReady={assetsReady}/>
    </div>
    <div style={{
      position:'absolute',bottom:34,left:36,right:36,
      fontSize:20,background:'#09151a',padding:18,borderRadius:9,
    }}>
      {action.replace(/_/g,' ').toUpperCase()}
      <div style={{marginTop:7,color:'#98b8ba',fontSize:17}}>
        {numFrames} newly drawn source poses · concept draft
      </div>
    </div>
  </div>;
};

export const ChibiV4ReviewStage:React.FC<ChibiV4ReviewProps>=({assetsReady})=>{
  const frame=useCurrentFrame();
  const index=Math.min(HOST_ACTIONS.length-1,Math.floor(frame/90));
  const first=index*90;
  return <AbsoluteFill style={{
    background:'radial-gradient(ellipse at center,#102e2b,#060f17)',
    color:'#f2fff7',fontFamily:'Inter',
  }}>
    <div style={{position:'absolute',top:35,left:78,letterSpacing:3,fontWeight:900,fontSize:40}}>
      NEW CHIBI V4
      <span style={{color:'#66fa9e',marginLeft:30,fontSize:26}}>
        URFAVXBF + PIX
      </span>
    </div>
    <div style={{position:'absolute',top:49,right:81,fontSize:18,color:'#9bbaa9'}}>
      16:9 / 30 FPS / ORIGINAL V4 CONCEPT FRAME REFERENCES
    </div>
    <div style={{position:'absolute',top:155,left:68,right:68,
      display:'flex',gap:55,justifyContent:'space-between'}}>
      <Card id="urfavxbf" action={HOST_ACTIONS[index]}
        assetsReady={assetsReady} startFrame={first}/>
      <Card id="pix" action={PIX_ACTIONS[index]}
        assetsReady={assetsReady} startFrame={first}/>
    </div>
    <div style={{position:'absolute',bottom:45,left:0,right:0,
      textAlign:'center',fontSize:18,color:'#b1cebe',letterSpacing:1}}>
      DRAFT ART · no 8-frame claim when only 3–5 drawings exist · no phoneme lip-sync or completed character hair rig
    </div>
  </AbsoluteFill>;
};
