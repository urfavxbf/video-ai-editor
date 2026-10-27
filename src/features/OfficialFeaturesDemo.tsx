import type {Caption} from '@remotion/captions';
import {createTikTokStyleCaptions} from '@remotion/captions';
import {Circle} from '@remotion/shapes';
import {linearTiming, TransitionSeries} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

export const OFFICIAL_FEATURE_DEMO_FRAMES = 180;

const FPS = 30;
const WHITE = '#f8f7f4';
const INK = '#070e1b';
const NEON = '#c8fc53';
const BLUE = '#8deafa';

const words: Caption[] = [
  {text: 'OFFICIAL', startMs: 0, endMs: 490, timestampMs: 245, confidence: 1},
  {text: ' REMOTION', startMs: 490, endMs: 1030, timestampMs: 750, confidence: 1},
  {text: ' FEATURES', startMs: 1030, endMs: 1780, timestampMs: 1400, confidence: 1},
  {text: ' CAPTIONS', startMs: 1780, endMs: 2440, timestampMs: 2120, confidence: 1},
  {text: ' TRANSITIONS', startMs: 2440, endMs: 3500, timestampMs: 2850, confidence: 1},
  {text: ' SHAPES', startMs: 3500, endMs: 4260, timestampMs: 3910, confidence: 1},
  {text: ' AND', startMs: 4260, endMs: 4700, timestampMs: 4470, confidence: 1},
  {text: ' EFFECTS', startMs: 4700, endMs: 5750, timestampMs: 5230, confidence: 1},
];
const {pages} = createTikTokStyleCaptions({
  captions: words,
  combineTokensWithinMilliseconds: 1050,
});

const Scene = ({
  title, subtitle, kicker, accent, shape,
}: {
  title: string;
  subtitle: string;
  kicker: string;
  accent: string;
  shape: 'circle' | 'ring' | 'orbit';
}) => {
  const frame = useCurrentFrame();
  const intro = interpolate(frame, [0, 17], [0, 1], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  const spin = frame * 1.6;
  return <AbsoluteFill style={{
    background: 'radial-gradient(ellipse at 45% 41%, #1a3445 0%, #0a1928 48%, #06101c 84%)',
    color: WHITE, fontFamily: "'Montserrat','Inter',sans-serif",
    overflow: 'hidden',
  }}>
    <AbsoluteFill style={{opacity: 0.19,
      backgroundImage: 'linear-gradient(rgba(235,251,255,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(235,251,255,.13) 1px,transparent 1px)',
      backgroundSize: '100px 100px',
    }}/>
    <div style={{position: 'absolute', left: 62, top: 110, letterSpacing: 6,
      fontWeight: 800, fontSize: 27, color: accent}}>{kicker}</div>
    <div style={{position: 'absolute', left: 60, top: 205, right: 60,
      fontWeight: 900, fontSize: title.length > 11 ? 92 : 118, lineHeight: 1.1,
      letterSpacing: -4, opacity: intro,
      transform: `translateY(${(1-intro)*40}px)`,
    }}>{title}</div>
    <div style={{position: 'absolute', left: 60, top: 460, right: 60,
      color: '#b8d0dc', fontSize: 36, fontWeight: 600}}>{subtitle}</div>
    <div style={{position: 'absolute', top: 650, left: 80, right: 80, height: 710,
      display: 'flex', justifyContent: 'center', alignItems: 'center',
      transform: `rotate(${spin}deg)`}}>
      <Circle radius={shape === 'circle' ? 240 : 285}
        fill={shape === 'circle' ? accent : 'transparent'}
        stroke={shape === 'circle' ? WHITE : accent} strokeWidth={shape === 'circle' ? 3 : 18}
        style={{opacity: .92, filter: 'drop-shadow(0 0 64px rgba(141,234,250,.19))'}}/>
      {shape !== 'circle' && <div style={{
        position: 'absolute', width: 460, height: 460, borderRadius: '50%',
        border: `5px dashed ${WHITE}`, opacity: 0.55,
        transform: 'rotate(-35deg)',
      }}/>}
      {shape === 'orbit' && <div style={{
        position: 'absolute', width: 140, height: 140, borderRadius: '50%',
        background: WHITE, boxShadow: `0 0 90px ${accent}`,
      }}/>}
    </div>
  </AbsoluteFill>;
};

export const OfficialFeaturesDemo = () => {
  const frame = useCurrentFrame();
  const nowMs = frame / FPS * 1000;
  const page = pages.find(p => nowMs >= p.startMs && nowMs < p.startMs + p.durationMs);
  return <AbsoluteFill style={{background: INK}}>
    <TransitionSeries>
      <TransitionSeries.Sequence durationInFrames={70}>
        <Scene kicker="01 / WORD-TIMED" title="CAPTIONS"
          subtitle="Accurate grouping and word highlights" accent={NEON} shape="circle"/>
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={slide()}
        timing={linearTiming({durationInFrames: 15})}/>
      <TransitionSeries.Sequence durationInFrames={70}>
        <Scene kicker="02 / SCENE EDITS" title="TRANSITIONS"
          subtitle="Built-in professional scene blending" accent={BLUE} shape="ring"/>
      </TransitionSeries.Sequence>
      <TransitionSeries.Transition presentation={fade()}
        timing={linearTiming({durationInFrames: 15})}/>
      <TransitionSeries.Sequence durationInFrames={70}>
        <Scene kicker="03 / SVG DESIGN" title="SHAPES"
          subtitle="Original scalable vector graphics" accent={NEON} shape="orbit"/>
      </TransitionSeries.Sequence>
    </TransitionSeries>
    <div style={{position: 'absolute', bottom: 235, left: 55, right: 55,
      padding: 29, textAlign: 'center', background: 'rgba(6,10,16,.82)',
      border: '1px solid rgba(255,255,255,.25)', borderRadius: 22,
      fontFamily: "'Montserrat','Inter',sans-serif", lineHeight: 1.14,
      fontSize: 50, fontWeight: 900, color: WHITE,
    }}>
      {page?.tokens.map((token, i) => <span key={i} style={{
        color: nowMs >= token.fromMs && nowMs < token.toMs ? NEON : WHITE,
        whiteSpace: 'pre-wrap',
      }}>{token.text}</span>)}
    </div>
    <div style={{position: 'absolute', top: 56, right: 53,
      fontFamily: "'Inter',sans-serif", fontSize: 20, fontWeight: 800,
      letterSpacing: 3, color: NEON}}>VIDEO AI EDITOR / OFFICIAL FEATURES</div>
    <div style={{position: 'absolute', bottom: 115, left: 55, right: 55,
      background: 'rgba(255,255,255,.22)', height: 5}}>
      <div style={{width: `${Math.min(100, 100*frame/OFFICIAL_FEATURE_DEMO_FRAMES)}%`,
        background: NEON, height: '100%'}}/>
    </div>
  </AbsoluteFill>;
};
