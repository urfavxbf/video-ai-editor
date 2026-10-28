import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import catalog from '../../characters/full-animation-set.json';
import {type CharacterId, type VoiceEvent, findVoiceEvent, voiceEnergyAtFrame} from './CharacterPuppet';

/**
 * Real-sprite animation library. All supported assets are actual approved PNGs.
 * Head sprites are a self-contained close-up, NEVER an overlay on a full-body
 * sprite (that causes double hair/ear outlines). No fabricated A/E/I/O/U shapes.
 */
export type HeroAnimationEntry = (typeof catalog.characters.urfavxbf)[number];
export type HeroAnimationStatus =
  | 'available-closeup' | 'available-composite' | 'needs-new-animation-art';
export type HeroAnimationPresentation = 'closeup' | 'composite';

type ClipSource =
  | {kind:'loop';mode:'idle'|'talk'|'react';frames:number;rate:number}
  | {kind:'portrait';expression:string}
  | {kind:'fullbody';effect:'glitch'|'float'|'appear'|'disappear'};

export const animationCatalog = catalog;
export const animationIds = (id:CharacterId):string[] => catalog.characters[id].map(a=>a.id);
export const lookupAnimation = (id:CharacterId, actionId:string):HeroAnimationEntry => {
  const a = catalog.characters[id].find(entry=>entry.id===actionId);
  if (!a) throw new Error(`Unknown ${id} animation: ${actionId}`);
  return a;
};

const sourceFor = (id:CharacterId, action:string):ClipSource => {
  if (action==='idle_normal'||action==='idle_sitting')return {kind:'loop',mode:'idle',frames:8,rate:5};
  if (action==='idle_talking'||action==='meow_talk')return {kind:'loop',mode:'talk',frames:8,rate:8};
  if (action==='surprised')return {kind:'portrait',expression:'surprised'};
  if (action==='laugh')return {kind:'portrait',expression:'excited'};
  if (action==='serious_focused')return {kind:'portrait',expression:'thinking'};
  if (action==='happy_excited')return {kind:'portrait',expression:'happy'};
  if (action==='curious'||action==='head_tilt')return {kind:'portrait',expression:'curious'};
  if (action==='glitch_idle'||action==='glitch_reaction'||action==='hair_glitch')return {kind:'fullbody',effect:'glitch'};
  if (action==='float')return {kind:'fullbody',effect:'float'};
  if (action==='appear_glitch')return {kind:'fullbody',effect:'appear'};
  if (action==='disappear_glitch')return {kind:'fullbody',effect:'disappear'};
  throw new Error(`${id}/${action} needs new actual animation drawings; no stock sprites or joint-cutout substitute allowed`);
};

export const requireRenderableHeroAnimation = (id:CharacterId, action:string):ClipSource => {
  const entry=lookupAnimation(id,action);
  if(entry.status==='needs-new-animation-art') {
    throw new Error(`${id}/${action}: original hand-authored animation frames missing; see full-animation-set.json`);
  }
  return sourceFor(id,action);
};

export type HeroAnimationPlayerProps = {
  id:CharacterId;
  action:string;
  width:number;
  height:number;
  voiceEvents?:VoiceEvent[];
  startFrame?:number;
  /** Must be true only when the canonical, checksum-verified asset pack is staged. */
  assetsReady:boolean;
};

export const HeroAnimationPlayer:React.FC<HeroAnimationPlayerProps>=({
  id,action,width,height,voiceEvents=[],startFrame=0,assetsReady,
})=>{
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  // Validate even when assets are absent: a requested missing animation fails
  // closed instead of rendering the wrong motion or pretending it is supported.
  const source=requireRenderableHeroAnimation(id,action);
  const event=findVoiceEvent(id,frame,voiceEvents);
  const energy=voiceEnergyAtFrame(frame,fps,event);
  const relative=Math.max(0,frame-startFrame);
  const base=`characters/pixel-glitch/${id}`;
  const head=source.kind!=='fullbody';
  const spritePath=source.kind==='loop'?
    `${base}/loops/${source.mode}/${String(Math.floor(relative*source.rate/fps)%source.frames).padStart(2,'0')}.png`
    :source.kind==='portrait'?`${base}/${source.expression}.png`:`${base}/base.png`;
  const glitch=source.kind==='fullbody' && source.effect==='glitch';
  const fx=source.kind==='fullbody'?source.effect:null;
  const t=relative/fps;
  const bob=(fx==='float'?Math.sin(t*3.2)*11:head?Math.sin(t*2.3)*2.4:0)
    -(event?energy*2.5:0);
  const duration=14;
  const reveal=Math.max(0,Math.min(1,relative/duration));
  const op=fx==='appear'?reveal:fx==='disappear'?1-reveal:1;
  const step=glitch && relative%29<3;
  return <div data-character={id} data-action={action} data-visual-kind={head?'head-only':'full-body-composite'}
    data-render-status={assetsReady?'assets-staged':'not-staged'}
    style={{
      position:'relative',width,height,overflow:'visible',pointerEvents:'none',
      opacity:op,transform:`translateY(${bob.toFixed(2)}px)`,
      filter:step?'drop-shadow(5px 0 #f535ff) drop-shadow(-5px 0 #00edff)':
        id==='pix'?'drop-shadow(0 0 7px rgba(34,231,255,0.20))':'drop-shadow(0 0 7px rgba(255,202,3,0.17))',
    }}>
    {assetsReady?<Img src={staticFile(spritePath)} style={{
      width:'100%',height:'100%',objectFit:'contain',imageRendering:'pixelated',
    }}/>:<div style={{
      width:'100%',height:'100%',display:'flex',alignItems:'center',justifyContent:'center',
      background:'#131c31',border:'1px dashed #58677b',fontFamily:'monospace',
      textAlign:'center',color:'#adbed4',fontSize:16,padding:30,
    }}>STAGE VERIFIED ARTWORK<br/>TO REVIEW {id.toUpperCase()} / {action}</div>}
  </div>;
};
