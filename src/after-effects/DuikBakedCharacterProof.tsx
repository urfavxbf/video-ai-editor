import {Lottie} from '@remotion/lottie';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import importedAnimation from './duik-imported.json';

/**
 * Offline proof of a Duik-style baked 2D character motion import.
 * Bundled animation is original hand-authored Lottie, NOT footage or source
 * copied from Duik. Users replace duik-imported.json with approved exports
 * after running scripts/import_duik_baked_lottie.py.
 */
export const DUIK_BAKED_PROOF_FRAMES = 150;

export const DuikBakedCharacterProof = () => {
  const frame = useCurrentFrame();
  const appear = interpolate(frame, [0, 12, 136, 149], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{background:'#090e20',color:'#f5fbff',
      fontFamily:"'Montserrat','Inter',sans-serif",overflow:'hidden'}}>
      <AbsoluteFill style={{background:
        'radial-gradient(ellipse at 28% 54%, #114e62 0%, #090e20 55%, #030713 100%)'}}/>
      <div style={{position:'absolute',left:75,top:92,right:75,
        fontSize:24,fontWeight:800,letterSpacing:5,color:'#9af6e0'}}>
        2D PUPPET ANIMATION / BAKED KEYFRAME BRIDGE
      </div>
      <div style={{position:'absolute',width:910,height:910,left:110,top:105,opacity:appear}}>
        <Lottie animationData={importedAnimation} loop={false}
          style={{width:'100%',height:'100%'}}/>
      </div>
      <div style={{position:'absolute',left:1050,top:240,right:140,opacity:appear}}>
        <div style={{fontSize:103,fontWeight:950,lineHeight:1.02,letterSpacing:-3}}>
          BUILD<br/>THE RIG.
        </div>
        <div style={{fontSize:100,fontWeight:950,color:'#78f2df',
          marginTop:20,lineHeight:1.02,letterSpacing:-3}}>
          BAKE<br/>THE MOTION.
        </div>
        <div style={{fontSize:35,lineHeight:1.5,marginTop:45,color:'#cbdde4'}}>
          Duik Ángela authoring → After Effects keyframes → Bodymovin JSON → Remotion
        </div>
      </div>
      <div style={{position:'absolute',bottom:70,left:95,right:95,
        display:'flex',justifyContent:'space-between',fontSize:21,
        color:'#8ba5b6',letterSpacing:2,fontWeight:700}}>
        <span>ORIGINAL VECTOR DEMO • NO ADOBE REQUIRED TO RENDER</span>
        <span>FRAME {String(frame + 1).padStart(3,'0')}</span>
      </div>
    </AbsoluteFill>
  );
};
