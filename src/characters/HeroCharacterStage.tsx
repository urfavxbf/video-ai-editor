import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {CharacterPuppet, type CharacterId, type LayeredPuppetRig, type VoiceEvent} from './CharacterPuppet';
import {HERO_IDENTITY, heroGestureFor, heroStateAt, listeningReactionCues, smooth01} from './HeroPerformance';
import {CANONICAL_CHARACTER_ASSETS, canonicalArtworkApproved} from './CanonicalCharacterAssets';

/**
 * Reusable 16:9 character-first workbench.
 * No fake narration or substituted characters; real official sprites must be staged.
 */
export type HeroStageAsset = {assetPath: string; layeredRig?: LayeredPuppetRig};
export type HeroStageProps = {
  assetsReady: boolean;
  artApproved?: boolean;
  voiceEvents: VoiceEvent[];
  chapter: number;
  assets?: Record<CharacterId, HeroStageAsset>;
  audio?: {file: string; startFrame: number; endFrame: number}[];
  durationFrames?: number;
};
export const HERO_STAGE_DURATION = 540;

const Wave: React.FC<{energy:number; color:string;frame:number; active:boolean}> = ({
  energy,color,frame,active,
})=><div style={{display:'flex',alignItems:'center',gap:5,height:42}}>
  {Array.from({length:19},(_,i)=>{
    const rate = 0.11 + 0.89 * Math.abs(Math.sin(frame*0.13 + i*0.58));
    const h = 5 + Math.round((active ? energy*30 : 0.12*rate*20)*rate);
    return <div key={i} style={{width:6,height:h,background:color,borderRadius:3,opacity:active?1:0.35}}/>;
  })}
</div>;

const IdentityCard:React.FC<{
  id:CharacterId;energy:number;speaking:boolean;frame:number;
}> = ({id,energy,speaking,frame})=>{
  const p=HERO_IDENTITY[id];
  return <div style={{
    position:'absolute',bottom:69,left:id==='urfavxbf'?82:undefined,
    right:id==='pix'?82:undefined,width:545,height:88,
    background:'rgba(7,16,32,0.89)',borderTop:`3px solid ${p.accent}`,
    borderRadius:12,display:'flex',justifyContent:'space-between',alignItems:'center',
    padding:'11px 23px',boxShadow:`0 15px 30px #0005`,
  }}>
    <div>
      <div style={{fontWeight:900,letterSpacing:2,fontSize:25}}>{p.name.toUpperCase()}</div>
      <div style={{fontSize:16,color:speaking?p.accent:'#96a8c3',marginTop:5,letterSpacing:1}}>
        {speaking?'SPEAKING / VOICE ENERGY':'LISTENING / PERFORMANCE'}
      </div>
    </div>
    <Wave energy={energy} active={speaking} color={p.accent} frame={frame}/>
  </div>;
};

export const HeroCharacterStage:React.FC<HeroStageProps> = ({
  assetsReady,artApproved=false, voiceEvents,chapter,assets,audio=[],
})=>{
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const host=heroStateAt('urfavxbf',chapter,frame,fps,voiceEvents);
  const pix=heroStateAt('pix',chapter,frame,fps,voiceEvents);
  const fade=smooth01(frame/23);
  const hostAsset=assets?.urfavxbf??CANONICAL_CHARACTER_ASSETS.urfavxbf;
  const pixAsset=assets?.pix??CANONICAL_CHARACTER_ASSETS.pix;
  const ready=canonicalArtworkApproved(assetsReady,artApproved);
  if (audio.length && !ready) {
    throw new Error('Stage and approve both official 2026-10-29 canonical character assets before voiced hero rendering');
  }
  return <AbsoluteFill style={{
    background:'#060d19',color:'#f1f6ff',fontFamily:'Inter',overflow:'hidden',
  }}>
    <AbsoluteFill style={{backgroundImage:'radial-gradient(ellipse at 20% 54%, #2f2d19aa 0%, transparent 47%),radial-gradient(ellipse at 80% 54%, #123b4e66 0%, transparent 45%)'}}/>
    <div style={{
      position:'absolute',left:0,right:0,top:0,bottom:0,
      opacity:0.28,backgroundSize:'54px 54px',
      backgroundImage:'linear-gradient(to right, #4c658024 1px,transparent 1px),linear-gradient(to bottom, #4c658024 1px,transparent 1px)',
    }}/>
    <div style={{position:'absolute',left:0,right:0,bottom:62,height:2,background:'linear-gradient(90deg,transparent,#f1f6ff60,transparent)'}}/>
    <div style={{position:'absolute',left:60,top:43,letterSpacing:5,fontSize:20,color:'#96a8c3'}}>
      URFAVXBF × PIX // HERO CHARACTER SYSTEM
    </div>
    <div style={{position:'absolute',right:60,top:43,letterSpacing:2,fontSize:17,color:'#96a8c3'}}>
      1920×1080 · 30 FPS · CANONICAL CHIBI
    </div>
    <div style={{position:'absolute',top:145,left:625,width:670,textAlign:'center',opacity:fade}}>
      <div style={{letterSpacing:7,fontSize:18,color:'#70e8ff',fontWeight:750}}>
        CHARACTER PERFORMANCE STUDY
      </div>
      <div style={{fontSize:76,fontWeight:950,letterSpacing:-2,lineHeight:1.05,marginTop:20}}>
        THE HOST<br/><span style={{color:'#6ffb8b'}}>+</span> THE AI PET
      </div>
      <div style={{height:2,background:'linear-gradient(90deg,transparent,#40617a,transparent)',margin:'29px 34px 24px'}}/>
      <div style={{fontSize:23,lineHeight:1.6,color:'#a8bcd2'}}>
        Expressive body language.<br/>Thoughtful listening.<br/>Real voice-driven energy.
      </div>
      <div style={{display:'flex',justifyContent:'center',gap:15,marginTop:42}}>
        {['IDLE','SPEAK','REACT','CELEBRATE'].map((x,i)=>
          <div key={x} style={{border:'1px solid #46546c',borderRadius:10,
            padding:'10px 15px',fontSize:15,letterSpacing:1,
            color:i===Math.floor(frame/105)%4?'#27e8fd':'#839ab4',
            background:i===Math.floor(frame/105)%4?'#17334f':'#0e1b2b'}}>
            {x}
          </div>)}
      </div>
    </div>
    {ready ? <>
      <CharacterPuppet id="urfavxbf"
        assetPath={hostAsset.assetPath} layeredRig={hostAsset.layeredRig}
        left={35} width={585} height={810} bottom={165}
        voiceEvents={voiceEvents}
        reactions={listeningReactionCues('urfavxbf',voiceEvents,chapter)}
        bodyGesture={heroGestureFor('urfavxbf',chapter,host.isSpeaking?'urfavxbf':undefined,frame,voiceEvents)}
        fadeInFrames={20}/>
      <CharacterPuppet id="pix"
        assetPath={pixAsset.assetPath} layeredRig={pixAsset.layeredRig}
        right={35} width={585} height={810} bottom={165}
        voiceEvents={voiceEvents}
        reactions={listeningReactionCues('pix',voiceEvents,chapter)}
        bodyGesture={heroGestureFor('pix',chapter,pix.isSpeaking?'pix':undefined,frame,voiceEvents)}
        fadeInFrames={24}/>
    </>:<div style={{position:'absolute',bottom:210,left:80,right:80,
      padding:20,textAlign:'center',border:'1px dashed #60728e',borderRadius:12,
      background:'#0d1a2b',fontSize:21}}>
      NEW CANONICAL ART PENDING — original references approved; production PNGs must be separately rigged and verified.
    </div>}
    <IdentityCard id="urfavxbf" energy={host.speakingEnergy}
      speaking={host.isSpeaking} frame={frame}/>
    <IdentityCard id="pix" energy={pix.speakingEnergy}
      speaking={pix.isSpeaking} frame={frame}/>
    <div style={{position:'absolute',left:60,right:60,bottom:23,
      display:'flex',justifyContent:'space-between',fontSize:14,letterSpacing:1.5,color:'#8aa3be'}}>
      <span>2026-10-29 CANONICAL VISUALS · NO LEGACY FALLBACK</span>
      <span>2.5D MOTION STUDY · NOT INDEPENDENT LIMB RIGGING</span>
    </div>
    {audio.map((a,i)=><Sequence key={i} from={a.startFrame}
      durationInFrames={a.endFrame-a.startFrame}>
      <Audio src={staticFile(a.file)} volume={0.88}/>
    </Sequence>)}
  </AbsoluteFill>;
};
