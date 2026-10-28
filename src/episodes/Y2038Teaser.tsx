import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {PixelGlitchPortrait, type PortraitReactionCue} from '../characters/PixelGlitchPortrait';
import {PORTRAIT_LAYOUT} from '../characters/portraitLayout';
import type {VoiceEvent} from '../characters/CharacterPuppet';

/**
 * New subject / new frame design. The numbers explain a vulnerable signed
 * 32-bit time representation, not that all computers break in 2038.
 * Only the approved enlarged head portrait assets are used.
 */
export type Y2038TeaserProps = {
  assetsReady: boolean;
  voiceEvents?: VoiceEvent[];
  reactions?: PortraitReactionCue[];
  subtitle?: string;
  speaking?: 'pix'|'urfavxbf';
};

const GOLD='#FFDB00', CYAN='#20DFFD';
export const Y2038Teaser: React.FC<Y2038TeaserProps> = ({
  assetsReady, voiceEvents=[], reactions=[],
  subtitle='Some older 32-bit clocks can run out of numbers.',
  speaking='urfavxbf',
}) => {
  const frame=useCurrentFrame();
  const roll=interpolate(frame,[80,142],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const isOverflow=frame>=142;
  const dial=interpolate(frame,[0,80],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const textColor=speaking==='pix'?CYAN:GOLD;
  return (
    <AbsoluteFill style={{
      color:'#F0FAFF',fontFamily:'monospace',overflow:'hidden',
      background:'radial-gradient(ellipse at 50% 44%,#15394b 0%,#081324 52%,#050818 100%)',
    }}>
      <AbsoluteFill style={{
        backgroundImage:'linear-gradient(rgba(9,152,183,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(9,152,183,.09) 1px,transparent 1px)',
        backgroundSize:'40px 40px',
      }}/>
      <div style={{position:'absolute',left:0,top:0,right:0,height:116,
        background:'rgba(4,10,26,.97)',borderBottom:'5px solid #16CFF4',display:'flex',
        alignItems:'center',justifyContent:'space-between',padding:'0 46px'}}>
        <div style={{fontSize:34,fontWeight:900}}>
          <span style={{color:GOLD}}>URFAVXBF</span> + <span style={{color:CYAN}}>PIX</span>
        </div>
        <div style={{fontSize:24,color:'#B4F6FF'}}>THE 2038 PROBLEM // PIXEL-GLITCH</div>
      </div>
      {assetsReady ? <>
        <PixelGlitchPortrait id="urfavxbf" left={PORTRAIT_LAYOUT.left} top={PORTRAIT_LAYOUT.top}
          voiceEvents={voiceEvents} reactions={reactions}/>
        <PixelGlitchPortrait id="pix" right={PORTRAIT_LAYOUT.right} top={PORTRAIT_LAYOUT.top}
          voiceEvents={voiceEvents} reactions={reactions}/>
      </> : <>
        {(['URFAVXBF','PIX'] as const).map((who,i)=>
          <div key={who} style={{position:'absolute',
            top:PORTRAIT_LAYOUT.top,left:i===0?PORTRAIT_LAYOUT.left:undefined,
            right:i===1?PORTRAIT_LAYOUT.right:undefined,
            width:PORTRAIT_LAYOUT.width,height:PORTRAIT_LAYOUT.height,
            borderRadius:24,border:`3px dashed ${i?CYAN:GOLD}`,boxSizing:'border-box',
            display:'flex',alignItems:'center',justifyContent:'center',
            color:i?CYAN:GOLD,fontSize:20,textAlign:'center',padding:40}}>
            STAGE APPROVED {who} HEAD PNGS
          </div>
        )}
      </>}
      <div style={{position:'absolute',left:515,top:192,width:890,height:646,
        padding:'33px 34px',boxSizing:'border-box',border:'3px solid #28DCF7',
        borderRadius:24,background:'rgba(4,15,29,.94)',boxShadow:'0 0 36px rgba(0,199,235,.12)'}}>
        <div style={{fontSize:26,color:CYAN,letterSpacing:2,fontWeight:800}}>THE YEAR 2038 PROBLEM</div>
        <div style={{marginTop:14,fontSize:20,color:'#9DB6C5'}}>SIGNED 32-BIT UNIX TIME // EXPLAINER</div>
        <div style={{marginTop:40,fontSize:95,fontWeight:900,
          letterSpacing:-2,color:isOverflow?'#FF4771':GOLD,
          textShadow:isOverflow?'4px 0 #14DDFF':'0 0 20px rgba(255,210,0,.2)'}}>
          {isOverflow?'1901':'2038'}
        </div>
        <div style={{fontSize:24,color:'#E1F5FF',marginTop:6}}>
          {isOverflow?'13 DEC 1901 // MISREAD DATE':'19 JAN 2038 // 03:14:07 UTC'}
        </div>
        <div style={{marginTop:48,display:'flex',alignItems:'center',height:86,
          border:'2px solid #17B9DC',borderRadius:10,padding:'0 18px',fontSize:34,fontWeight:800}}>
          <span style={{color:isOverflow?'#FF4771':GOLD}}>
            {isOverflow?'−2,147,483,648':'2,147,483,647'}
          </span>
          <span style={{marginLeft:'auto',color:CYAN,fontSize:18}}>32-BIT</span>
        </div>
        <div style={{marginTop:29,fontSize:19,color:'#B2D7E8'}}>
          {isOverflow?'WRAP EXAMPLE ON AFFECTED SYSTEMS':'ONE MORE SECOND CAN EXCEED THE RANGE'}
        </div>
        <div style={{marginTop:22,width:'100%',height:13,background:'#133C4D'}}>
          <div style={{height:'100%',width:`${Math.max(0,100*roll)}%`,
            background:isOverflow?'#FF4771':CYAN}}/>
        </div>
      </div>
      <div style={{position:'absolute',left:515,right:515,bottom:45,minHeight:150,
        padding:'16px 28px',borderRadius:18,boxSizing:'border-box',
        border:`3px solid ${textColor}`,background:'rgba(1,8,23,.96)'}}>
        <div style={{fontSize:22,color:textColor,fontWeight:900,marginBottom:13}}>
          {speaking==='pix'?'PIX':'URFAVXBF'}
        </div>
        <div style={{fontSize:30,lineHeight:1.28,fontWeight:800}}>{subtitle}</div>
      </div>
      <div style={{position:'absolute',bottom:4,right:28,color:'#83A9B7',fontSize:15}}>
        NOT ALL COMPUTERS ARE AFFECTED
      </div>
    </AbsoluteFill>
  );
};
