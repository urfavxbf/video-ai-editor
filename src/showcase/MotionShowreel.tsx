import React from 'react';
import {AbsoluteFill, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Lottie} from '@remotion/lottie';
import {FX_ALL} from '../fx/index';
import {FxSourceContext, type FxSource} from '../fx/shared';
import vectorAnimation from '../after-effects/original-growth.json';
import puppetAnimation from '../after-effects/duik-imported.json';

/**
 * EFFECT-FIRST SHOWREEL. No watermark, title card, grid background, fixed HUD,
 * numbers, explanatory sidebar, footer or framing chrome. Full-bleed 9:16
 * matches the 21 portrait-native FX instead of shrinking them into a slide.
 * This is a requested SHOWREEL override, not a change to the 16:9 episode default.
 */
const FPS = 30;
const VECTOR_FRAMES = 90;
const PUPPET_FRAMES = 150;
const HYPER_FRAMES = 60;
const source: FxSource = {
  video: 'sample/take.mp4',
  matte: 'sample/fg',
  sticker: 'sample/sticker',
  frames: 300,
  face: {x: 540, y: 620, mouthY: 900},
  continuous: true,
};

export const SHOWREEL_EFFECT_IDS = FX_ALL.map(effect => effect.id);
export const SHOWREEL_EFFECT_STARTS = FX_ALL.reduce<Array<{
  id:string;at:number;duration:number
}>>((result, effect) => {
  const at = result.length === 0 ? 0 :
    result[result.length - 1].at + result[result.length - 1].duration;
  result.push({id: effect.id, at, duration: effect.duration});
  return result;
}, []);
const FX_END = FX_ALL.reduce((total, effect) => total + effect.duration, 0);
const VECTOR_START = FX_END;
const PUPPET_START = VECTOR_START + VECTOR_FRAMES;
const HYPER_START = PUPPET_START + PUPPET_FRAMES;
export const SHOWREEL_FRAMES = HYPER_START + HYPER_FRAMES;

const FullBleedEffect: React.FC<{
  Component: (typeof FX_ALL)[number]['Component'];
  from: number;
}> = ({Component, from}) => (
  <AbsoluteFill>
    <FxSourceContext.Provider value={source}>
      <Component from={from} />
    </FxSourceContext.Provider>
  </AbsoluteFill>
);

const VectorMoment: React.FC = () => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, VECTOR_FRAMES - 1], [0.86, 1.22]);
  return (
    <AbsoluteFill style={{
      background: 'radial-gradient(ellipse at 47% 45%,#0d665d,#051022 70%)',
      overflow: 'hidden',
    }}>
      <AbsoluteFill style={{transform: `scale(${scale})`}}>
        <Lottie animationData={vectorAnimation} loop={false} style={{
          position: 'absolute', left: 65, top: 400, width: 950, height: 950,
        }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const PuppetMoment: React.FC = () => {
  const frame = useCurrentFrame();
  const amount = Math.sin(frame * 0.045) * 40;
  return (
    <AbsoluteFill style={{
      background: 'radial-gradient(circle at 52% 42%,#264a70,#090d1a 70%)',
      overflow: 'hidden',
    }}>
      <AbsoluteFill style={{transform: `translateY(${amount}px)`}}>
        <Lottie animationData={puppetAnimation} loop={false} style={{
          position: 'absolute', left: 28, top: 360, width: 1024, height: 1024,
        }} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const HyperFramesMoment: React.FC = () => {
  const frame = useCurrentFrame();
  const left = interpolate(frame,[0,HYPER_FRAMES-1],[-150,-750]);
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <OffthreadVideo src={staticFile('hyperframes/kinetic-intro.mp4')} muted
        style={{
          position: 'absolute', top: 0, left,
          width: 3420, height: 1920, objectFit: 'fill',
        }} />
    </AbsoluteFill>
  );
};

export const MotionShowreel: React.FC = () => (
  <AbsoluteFill style={{background: '#050a14', overflow: 'hidden'}}>
    {FX_ALL.map((entry, index) => (
      <Sequence key={entry.id}
        from={SHOWREEL_EFFECT_STARTS[index].at}
        durationInFrames={entry.duration}>
        <FullBleedEffect Component={entry.Component} from={(index * 7) % 90} />
      </Sequence>
    ))}
    <Sequence from={VECTOR_START} durationInFrames={VECTOR_FRAMES}>
      <VectorMoment />
    </Sequence>
    <Sequence from={PUPPET_START} durationInFrames={PUPPET_FRAMES}>
      <PuppetMoment />
    </Sequence>
    <Sequence from={HYPER_START} durationInFrames={HYPER_FRAMES}>
      <HyperFramesMoment />
    </Sequence>
  </AbsoluteFill>
);
