import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {type VoiceEvent} from './CharacterPuppet';
import {PixelGlitchPortrait, type PortraitReactionCue} from './PixelGlitchPortrait';

/** 16:9 HUD composition: head portraits flank the data/caption canvas. No body artwork. */
export type PixelPortraitHUDProps = {
  /** Set true only after the real PNG expressions are available in public/characters/pixel-glitch/. */
  assetsReady: boolean;
  voiceEvents?: VoiceEvent[];
  reactions?: PortraitReactionCue[];
  caption?: string;
  captionSpeaker?: 'urfavxbf' | 'pix';
  botTrafficPercent?: number;
};

const YELLOW = '#FFDA00';
const CYAN = '#27E8FD';

export const PixelPortraitHUD: React.FC<PixelPortraitHUDProps> = ({
  assetsReady, voiceEvents = [], reactions = [],
  caption = 'TRAFFIC IS NOT THE SAME AS PEOPLE.',
  captionSpeaker = 'urfavxbf', botTrafficPercent = 53,
}) => {
  const frame = useCurrentFrame();
  const animatedValue = interpolate(frame, [30, 90], [0, botTrafficPercent], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const share = Math.max(0, Math.min(100, animatedValue));
  const highlighted = captionSpeaker === 'pix' ? CYAN : YELLOW;
  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(#060A18, #0D1A2C)', color: '#F1F7FF',
      fontFamily: 'monospace', overflow: 'hidden',
    }}>
      <div style={{position:'absolute', top:0, left:0, right:0, height:112,
        background:'#060C1D', borderBottom:`5px solid ${CYAN}`}}>
        <div style={{position:'absolute', left:46, top:28, fontSize:37, fontWeight:800}}>
          <span style={{color:YELLOW}}>URFAVXBF</span> &nbsp; + &nbsp; <span style={{color:CYAN}}>PIX</span>
        </div>
        <div style={{position:'absolute', right:46, top:33, fontSize:25, color:'#A0D5E4'}}>
          PIXEL/GLITCH // PORTRAITS ONLY
        </div>
      </div>
      {assetsReady ? (
        <>
          <PixelGlitchPortrait id="urfavxbf" left={115} top={226}
            voiceEvents={voiceEvents} reactions={reactions}/>
          <PixelGlitchPortrait id="pix" right={105} top={226}
            voiceEvents={voiceEvents} reactions={reactions}/>
        </>
      ) : (
        <>
          {(['URFAVXBF', 'PIX'] as const).map((name, i) => (
            <div key={name} style={{position:'absolute', top:226, left:i===0?115:undefined,
              right:i===1?105:undefined, width:306, height:346, boxSizing:'border-box',
              border:`3px dashed ${i===0?YELLOW:CYAN}`, borderRadius:20,
              color:i===0?YELLOW:CYAN, fontSize:23, display:'flex', alignItems:'center',
              justifyContent:'center', textAlign:'center', padding:24}}>
              STAGE {name} PORTRAIT PNGS
            </div>
          ))}
        </>
      )}
      <div style={{position:'absolute',left:510,top:200,width:900,height:650,
        boxSizing:'border-box',border:`3px solid ${CYAN}`,borderRadius:24,
        background:'rgba(4,16,32,0.94)',padding:34}}>
        <div style={{color:'#A0D5E4',fontSize:25,letterSpacing:2}}>NETWORK ACTIVITY / 2025</div>
        <div style={{color:'#789BAA',fontSize:22,marginTop:16}}>DATA EXAMPLE — THALES BAD BOT REPORT</div>
        <div style={{fontSize:190,fontWeight:900,letterSpacing:-9,color:YELLOW,marginTop:20}}>
          {animatedValue.toFixed(1)}%
        </div>
        <div style={{fontSize:27,marginTop:-6}}>AUTOMATED WEB REQUESTS</div>
        <div style={{display:'flex',height:53,marginTop:40,
          border:`3px solid ${CYAN}`,padding:5}}>
          <div style={{background:YELLOW,width:`${share}%`}}/>
          <div style={{background:'#16B8D7',flex:1}}/>
        </div>
        <div style={{display:'flex',justifyContent:'space-between',fontSize:22,
          marginTop:16,color:'#9EDBE4'}}><span>BOTS</span><span>HUMANS</span></div>
        <div style={{textAlign:'center',color:YELLOW,fontSize:29,marginTop:30}}>
          TRAFFIC ≠ PEOPLE
        </div>
      </div>
      <div style={{position:'absolute',left:510,right:510,bottom:40,minHeight:140,
        boxSizing:'border-box',border:`3px solid ${highlighted}`,borderRadius:14,
        padding:'17px 24px',background:'#040B19'}}>
        <div style={{color:highlighted,fontSize:21,marginBottom:13,fontWeight:800}}>
          {captionSpeaker === 'pix' ? 'PIX' : 'URFAVXBF'}
        </div>
        <div style={{fontSize:30,fontWeight:700}}>{caption}</div>
      </div>
    </AbsoluteFill>
  );
};
