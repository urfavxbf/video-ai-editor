import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {type VoiceEvent} from '../characters/CharacterPuppet';
import {PixelGlitchPortrait} from '../characters/PixelGlitchPortrait';

const yellow = '#ffda00';
const cyan = '#27e8fd';
const muted = '#96a8c3';
const Panel: React.FC<React.PropsWithChildren<{accent?: string}>> = ({children,accent=cyan}) => <div style={{background:'#101e32',border:`2px solid ${accent}55`,borderRadius:24,padding:30}}>{children}</div>;

/** Original episode layout studies. Static editorial frames, not timed speech. */
export type JourneySceneProps = {sceneOverride?: number; captionOverride?: string; speakerOverride?: string; voiceEvents?: VoiceEvent[]; preview?: boolean; sceneStart?: number};
export const YouTubeJourneyStyleframes: React.FC<JourneySceneProps> = ({sceneOverride,captionOverride,speakerOverride,voiceEvents=[],preview=false,sceneStart=0}) => {
  const frame = useCurrentFrame();
  const scene = sceneOverride ?? Math.min(2,Math.floor(frame/90));
  const reveal = preview ? interpolate(frame-sceneStart,[0,18],[0,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"}) : 1;
  const title = ['YOU HIT UPLOAD. NOW WHAT?','TWO DIFFERENT GATES.','SAME VIEWS. DIFFERENT REVENUE.'][scene];
  const caption = captionOverride ?? ['“Before the money, there’s a person.”','“That’s the first gate. Does it unlock advertising money?”','“So I shouldn’t order a yacht based on somebody else’s screenshot.”'][scene];
  return <AbsoluteFill style={{background:'#060d19',color:'#f1f6ff',fontFamily:'Inter',padding:64}}>
    <div style={{position:'absolute',inset:0,backgroundImage:'radial-gradient(ellipse at 50% 38%, #16324b 0%, transparent 65%)'}} />
    <div style={{position:'absolute',top:49,left:64,right:64,display:'flex',justifyContent:'space-between',fontSize:19,letterSpacing:3,fontWeight:700,color:muted}}><span>URFAVXBF + PIX / CREATOR FIELD GUIDE</span><span>ENGLISH · 16:9</span></div>
    <div style={{position:'absolute',top:108,left:64,right:64,fontSize:52,fontWeight:900,letterSpacing:-1}}>{title}</div>
    <PixelGlitchPortrait id="urfavxbf" left={64} top={240} showGlitch={false} voiceEvents={voiceEvents} reactions={[{speaker:'urfavxbf',startFrame:0,endFrame:999999,reaction:scene===2?'excited':'thinking'}]} />
    <PixelGlitchPortrait id="pix" right={64} top={240} showGlitch={false} voiceEvents={voiceEvents} reactions={[{speaker:'pix',startFrame:0,endFrame:999999,reaction:scene===2?'surprised':'curious'}]} />
    <div style={{position:'absolute',left:515,width:890,top:240,opacity:reveal,transform:`translateY(${(1-reveal)*18}px)`}}>
      <div style={{fontSize:18,fontWeight:800,letterSpacing:3,color:cyan,marginBottom:20}}>0{scene===0?1:scene===1?5:6} / {['THE FIRST UPLOAD','MONETIZATION','THE EARNINGS QUESTION'][scene]}</div>
      {scene===0 ? <>
        <Panel><div style={{display:'flex',justifyContent:'space-between',fontSize:22,color:muted}}><span>PIX’S FIRST VIDEO</span><span style={{color:cyan}}>UPLOAD COMPLETE ✓</span></div><div style={{fontSize:42,fontWeight:800,marginTop:26,lineHeight:1.15}}>Why Your Phone Storage<br/>Keeps Filling Up</div><div style={{marginTop:28,height:12,borderRadius:6,background:'#26394e'}}><div style={{width:'94%',height:12,borderRadius:6,background:yellow}} /></div></Panel>
        <div style={{marginTop:24,display:'flex',alignItems:'center',gap:20}}><div style={{fontSize:61,color:yellow}}>?</div><div style={{fontSize:32,fontWeight:700}}>Who is this for?<div style={{fontSize:22,color:muted,marginTop:8}}>One viewer. One useful promise.</div></div></div>
      </> : scene===1 ? <>
        <Panel accent={cyan}><div style={{color:cyan,fontSize:20,fontWeight:800}}>EARLY ACCESS · ELIGIBLE COUNTRIES</div><div style={{fontSize:37,fontWeight:850,marginTop:12}}>500 subscribers</div><div style={{fontSize:24,lineHeight:1.5,marginTop:10}}>3 public uploads / 90 days<br/><b>3,000</b> qualified hours / 12 months<br/><span style={{color:cyan}}>OR</span> <b>3M</b> qualified Shorts views / 90 days</div></Panel>
        <div style={{marginTop:16}}><Panel accent={yellow}><div style={{color:yellow,fontSize:20,fontWeight:800}}>AD REVENUE ELIGIBILITY</div><div style={{fontSize:37,fontWeight:850,marginTop:12}}>1,000 subscribers</div><div style={{fontSize:24,lineHeight:1.5,marginTop:10}}><b>4,000</b> qualified hours / 12 months<br/><span style={{color:yellow}}>OR</span> <b>10M</b> qualified Shorts views / 90 days</div></Panel></div>
        <div style={{fontSize:19,color:muted,marginTop:16}}>Application, review and feature requirements apply.</div>
      </> : <>
        <Panel><div style={{fontSize:19,letterSpacing:2,color:cyan,fontWeight:800}}>ILLUSTRATIVE MATH · NOT AN EARNINGS FORECAST</div><div style={{fontSize:70,fontWeight:900,marginTop:20}}>50,000 <span style={{fontSize:28,color:muted}}>views</span></div><div style={{height:1,background:'#34455e',margin:'25px 0'}} />{[['$2 RPM','$100'],['$5 RPM','$250']].map(([rpm,result])=><div key={rpm} style={{display:'flex',justifyContent:'space-between',alignItems:'center',margin:'18px 0',fontSize:38}}><span>{rpm}</span><span style={{color:yellow,fontWeight:900}}>{result}</span></div>)}</Panel>
        <div style={{fontSize:26,lineHeight:1.4,color:muted,marginTop:24}}>Views ÷ 1,000 × RPM<br/>Revenue before creator expenses and taxes.</div>
      </>}
    </div>
    <div style={{position:'absolute',left:64,right:64,bottom:preview?65:80,borderTop:'1px solid #35455c',paddingTop:30}}><div style={{fontSize:19,color:scene===0?yellow:cyan,fontWeight:800,letterSpacing:3,marginBottom:14}}>{speakerOverride ?? (scene===0?'URFAVXBF':'PIX')}</div><div style={{fontSize:preview?28:34,fontWeight:600,lineHeight:1.25,maxWidth:1730}}>{caption}</div></div>
    <div style={{position:'absolute',bottom:23,left:64,right:64,display:'flex',justifyContent:'space-between',fontSize:16,color:muted}}><span>{preview?'PRODUCTION PREVIEW / CHAPTER EXCERPTS':'VISUAL DEVELOPMENT / STATIC STYLEFRAME'}</span><span>{scene===1?'Policy checked 28 Oct 2026 · support.google.com/youtube/answer/13429240':scene===2?'Invented RPM values · no income guarantee':'How YouTube Actually Works—and How Creators Make Money'}</span></div>
  </AbsoluteFill>;
};
