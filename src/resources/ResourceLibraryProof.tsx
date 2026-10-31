import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';

/** Original silent B-roll using only repo-owned SVG resources.
 * This is a starter asset, not licensed documentary stock footage.
 */
export const RESOURCE_LIBRARY_FRAMES = 120;

export const ResourceLibraryProof: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 119], [-48, 60]);
  const scale = interpolate(frame, [0, 119], [1.04, 1.18]);
  const lift = interpolate(frame, [0, 30], [110, 0], {extrapolateRight:'clamp'});
  const fade = interpolate(frame,[0,12,96,119],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const orbit = frame >= 56;
  return <AbsoluteFill style={{background:'#070c1a',overflow:'hidden',color:'#f2fff7',fontFamily:'Inter,Montserrat,sans-serif'}}>
    <AbsoluteFill style={{transform:'translateX('+drift+'px) scale('+scale+')'}}>
      <Img src={staticFile(orbit?'resources/original/orbit-lines.svg':'resources/original/neon-grid.svg')}
        style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    </AbsoluteFill>
    <AbsoluteFill style={{background:'linear-gradient(90deg,#070c1acc,#070c1a44 63%,#070c1a1a)'}}/>
    <div style={{position:'absolute',left:145,top:235,letterSpacing:9,fontSize:31,
      fontWeight:800,color:'#78f5bf',opacity:fade}}>ORIGINAL VISUAL RESOURCES / 01</div>
    <div style={{position:'absolute',left:130,top:338,transform:'translateY('+lift+'px)',
      fontWeight:900,letterSpacing:-7,fontSize:132,lineHeight:1.02,opacity:fade}}>
      EVERY FRAME<br/><span style={{color:'#86efd4'}}>HAS A STORY.</span>
    </div>
    <div style={{position:'absolute',left:145,bottom:190,letterSpacing:3,fontSize:32,
      color:'#c9e4db',opacity:fade}}>LOCAL ARTWORK · FRAME-ACCURATE · NO EXTERNAL ASSETS</div>
    <div style={{position:'absolute',left:145,right:145,bottom:137,height:3,background:'#66f2b9',opacity:fade}}/>
  </AbsoluteFill>;
};
