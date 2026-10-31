import {Lottie} from '@remotion/lottie';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import originalGrowth from './original-growth.json';

/**
 * Original vector illustration proof that exercises the exact Bodymovin JSON
 * format accepted by @remotion/lottie. Does not depend on After Effects, paid
 * tools, remote assets, provider calls, or third-party artwork at render time.
 */
export const AFTER_EFFECTS_LOTTIE_FRAMES = 150;

export const AfterEffectsLottieProof = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 12, 136, 149], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rise = interpolate(frame, [0, 18], [42, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      background: '#060b18', color: '#f6fcff',
      fontFamily: "'Montserrat', 'Inter', sans-serif",
      overflow: 'hidden',
    }}>
      <AbsoluteFill style={{
        background: 'radial-gradient(circle at 49% 53%, #163d58 0%, #060b18 67%)',
      }} />
      <div style={{
        position: 'absolute', top: 230, left: 72, right: 72,
        fontSize: 35, fontWeight: 700, letterSpacing: 7,
        color: '#7deee2', opacity,
      }}>EVERY NEW CHAPTER STARTS SOMEWHERE</div>
      <div style={{
        position: 'absolute', left: 50, top: 370, width: 980, height: 980,
        opacity,
      }}>
        <Lottie animationData={originalGrowth} loop
          style={{width: '100%', height: '100%'}} />
      </div>
      <div style={{
        position: 'absolute', top: 1295, left: 72, right: 72,
        opacity, transform: `translateY(${rise}px)`,
      }}>
        <div style={{
          fontSize: 116, fontWeight: 950, lineHeight: 0.96,
          letterSpacing: -5,
        }}>GROWTH</div>
        <div style={{
          fontSize: 108, fontWeight: 950, lineHeight: 1.03,
          letterSpacing: -4, color: '#7deee2',
        }}>IS MOTION.</div>
        <div style={{
          marginTop: 35, fontSize: 33, lineHeight: 1.35,
          color: '#ccdae2', letterSpacing: 1,
        }}>An original Lottie animation, rendered frame-by-frame.</div>
      </div>
      <div style={{
        position: 'absolute', bottom: 140, left: 72, right: 72,
        height: 3, background: '#6cf2e5',
      }} />
    </AbsoluteFill>
  );
};
