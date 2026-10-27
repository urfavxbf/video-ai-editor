import React from 'react';
import { Audio } from '@remotion/media';
import { AbsoluteFill, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';

export const MOTION30_FRAMES = 900;
type MotionProps = { includeNarration?: boolean; includeMusic?: boolean };
const FPS = 30;
const duration = 180;
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

function fade(frame: number, start: number) {
  return interpolate(frame, [start - 8, start + 8, start + duration - 15, start + duration - 1], [0, 1, 1, 0], clamp);
}
function motion(frame: number, start: number, offset = 0) {
  return spring({ fps: FPS, frame: Math.max(0, frame - start - offset), config: { stiffness: 96, damping: 19, mass: 0.85 } });
}
function Reveal({
  frame, start, delay = 0, children, style,
}: {
  frame: number; start: number; delay?: number; children: React.ReactNode; style?: React.CSSProperties;
}) {
  const p = motion(frame, start, delay);
  return <div style={{ opacity: p, transform: 'translateY(' + Math.round((1 - p) * 105) + 'px)', ...style }}>{children}</div>;
}
const headline = (fontSize: number, color: string): React.CSSProperties => ({
  fontFamily: 'Montserrat, Inter, sans-serif', fontWeight: 900, fontSize, letterSpacing: -7,
  lineHeight: 1.03, color, textTransform: 'uppercase',
});

// Scene 1: editorial paper, a diagonal red strike-through, punchy typographic protest.
// There is deliberately NO shared frame, series title, logo, progress bar or template background.
function BreakPerfection({ frame: f }: { frame: number }) {
  const strike = interpolate(f, [24, 66], [0, 1120], clamp);
  const glitch = interpolate(f, [62, 95], [0, 1], clamp);
  return <AbsoluteFill style={{ opacity: fade(f, 0), background: '#F8F5E9', overflow: 'hidden' }}>
    <AbsoluteFill style={{ background: 'radial-gradient(circle at 85% 17%, #FFE6D2 0%, transparent 42%)' }} />
    <div style={{ position: 'absolute', left: -160, top: 130, width: 490, height: 490, borderRadius: '50%', background: '#E7E5DC' }} />
    <div style={{ position: 'absolute', left: 60, right: 60, top: 340 }}>
      <Reveal frame={f} start={0} delay={9}>
        <div style={headline(169, '#13191F')}>PERFECT</div>
      </Reveal>
      <div style={{ position: 'absolute', left: -24, top: 105, width: strike, maxWidth: '118%', height: 28, transform: 'rotate(-10deg)', transformOrigin: 'left center', background: '#FF423B', borderRadius: 5 }} />
      <Reveal frame={f} start={0} delay={34}>
        <div style={{ ...headline(170, '#13191F'), marginTop: 92 }}>IS A</div>
        <div style={{ ...headline(228, '#FF423B'), letterSpacing: -12, transform: 'rotate(' + (-3 * glitch) + 'deg)', marginTop: 12 }}>TRAP.</div>
      </Reveal>
      <Reveal frame={f} start={0} delay={64}>
        <div style={{ fontFamily: 'Inter, sans-serif', fontSize: 41, fontWeight: 550, lineHeight: 1.42, color: '#3A4147', maxWidth: 780, marginTop: 90 }}>
          Your next chapter starts when you move.
        </div>
      </Reveal>
    </div>
    {Array.from({ length: 8 }, (_, i) => {
      const p = motion(f, 0, 85 + i * 6);
      return <div key={i} style={{ position: 'absolute', width: 65, height: 65, border: '5px solid #FF423B', borderRadius: 999, top: 1460 + (i % 2) * 120, left: 110 + i * 124, transform: 'scale(' + p + ') rotate(' + (f * .5) + 'deg)' }} />;
    })}
  </AbsoluteFill>;
}

// Scene 2: royal blue full-bleed field and a chain reaction of animated geometric tiles.
function SmallAction({ frame: f }: { frame: number }) {
  const s = 180;
  return <AbsoluteFill style={{ opacity: fade(f, s), background: '#1646DE', overflow: 'hidden' }}>
    <div style={{ position: 'absolute', top: -330, left: 430, width: 1040, height: 1040, border: '90px solid #245DF3', borderRadius: '50%', transform: 'rotate(' + (f - s) * .1 + 'deg)' }} />
    <div style={{ position: 'absolute', left: 85, top: 252 }}>
      <Reveal frame={f} start={s} delay={12}>
        <div style={{ ...headline(186, '#FDFFA0'), letterSpacing: -15 }}>ONE.</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={30}>
        <div style={{ ...headline(114, '#FFFFFF') }}>IDEA.</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={53}>
        <div style={{ ...headline(114, '#FFFFFF') }}>DECISION.</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={76}>
        <div style={{ ...headline(114, '#FDFFA0') }}>ACTION.</div>
      </Reveal>
    </div>
    {Array.from({ length: 5 }, (_, i) => {
      const p = motion(f, s, 55 + i * 16);
      const rotate = (1 - p) * -70;
      return <div key={i} style={{ position: 'absolute', left: 94 + i * 191, top: 1245 + (i % 2) * 45, width: 151, height: 258, background: i === 4 ? '#FDFFA0' : '#EDF1FF', borderRadius: 18, transform: 'perspective(500px) rotateZ(' + rotate + 'deg) translateY(' + ((1 - p) * -120) + 'px)', transformOrigin: 'bottom left', boxShadow: '12px 20px 0 #0C31B3' }} />;
    })}
    <Reveal frame={f} start={s} delay={107} style={{ position: 'absolute', left: 90, bottom: 210 }}>
      <div style={{ fontFamily: 'Inter, sans-serif', fontWeight: 600, color: '#EEF0FF', fontSize: 39 }}>Small moves change everything.</div>
    </Reveal>
  </AbsoluteFill>;
}

// Scene 3: animated sound/momentum wave, no reused scene furniture.
function BuildMomentum({ frame: f }: { frame: number }) {
  const s = 360;
  const p = interpolate(f, [s + 15, s + 153], [0, 1], clamp);
  return <AbsoluteFill style={{ opacity: fade(f, s), background: '#141321', overflow: 'hidden' }}>
    <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 62% 85%,#6935A9 0%,transparent 56%)' }} />
    <svg width={1200} height={980} viewBox="0 0 1200 980" style={{ position: 'absolute', top: 730, left: -60 }}>
      {Array.from({ length: 21 }, (_, i) => {
        const y = 130 + i * 31;
        const offset = Math.sin(i * .66 + f * .07) * 62 * p;
        const d = 'M -40 ' + y + ' C 280 ' + (y - 180 - offset) + ' 330 ' + (y + 200 + offset) + ' 610 ' + y +
          ' S 980 ' + (y - 170 - offset) + ' 1240 ' + (y + 35);
        return <path key={i} d={d} fill="none" stroke={i % 4 === 0 ? '#FF9C45' : '#B477FB'} strokeWidth={i % 4 === 0 ? 10 : 4} opacity={.25 + p * .4} />;
      })}
    </svg>
    <div style={{ position: 'absolute', left: 80, top: 284, right: 55 }}>
      <Reveal frame={f} start={s} delay={16}>
        <div style={{ ...headline(111, '#F3F0F6') }}>MOTIVATION</div>
        <div style={{ ...headline(135, '#817E99') }}>FADES.</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={68} style={{ marginTop: 88 }}>
        <div style={{ ...headline(123, '#FFAA60') }}>MOMENTUM</div>
        <div style={{ ...headline(154, '#FFAA60') }}>BUILDS.</div>
      </Reveal>
    </div>
  </AbsoluteFill>;
}

// Scene 4: an actual animated route, shaped around the concept of taking a step.
function FindThePath({ frame: f }: { frame: number }) {
  const s = 540;
  const distance = interpolate(f, [s + 15, s + 158], [0, 1], clamp);
  return <AbsoluteFill style={{ opacity: fade(f, s), background: '#EAE0CE', overflow: 'hidden', color: '#242A2B' }}>
    <div style={{ position: 'absolute', top: -130, left: -150, width: 760, height: 760, background: '#D5D0BF', borderRadius: '50%' }} />
    <div style={{ position: 'absolute', right: -280, bottom: 120, width: 890, height: 890, background: '#F5B875', borderRadius: '50%', opacity: .6 }} />
    <svg width={1080} height={1180} viewBox="0 0 1080 1180" style={{ position: 'absolute', left: 0, top: 620 }}>
      <path d="M 80 900 C 310 1080 500 850 310 690 S 140 330 510 300 S 680 570 960 60" fill="none" stroke="#4C504B" strokeWidth={8} strokeDasharray="16 24" opacity={.4} />
      <path d="M 80 900 C 310 1080 500 850 310 690 S 140 330 510 300 S 680 570 960 60" fill="none" stroke="#F35631" strokeWidth={21} strokeLinecap="round" pathLength={1} strokeDasharray={distance + ' 1'} />
      <circle cx={80} cy={900} r={24} fill="#F35631" />
    </svg>
    <div style={{ position: 'absolute', top: 235, left: 78, right: 65 }}>
      <Reveal frame={f} start={s} delay={13}>
        <div style={{ ...headline(96, '#242A2B') }}>YOU DON'T</div>
        <div style={{ ...headline(96, '#242A2B') }}>NEED THE</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={42}>
        <div style={{ ...headline(158, '#F35631') }}>WHOLE</div>
        <div style={{ ...headline(180, '#242A2B') }}>PATH.</div>
      </Reveal>
    </div>
    <Reveal frame={f} start={s} delay={104} style={{ position: 'absolute', left: 78, bottom: 110 }}>
      <span style={{ fontSize: 43, fontWeight: 700, fontFamily: 'Inter, sans-serif', color: '#363E3E' }}>Just take the first step.</span>
    </Reveal>
  </AbsoluteFill>;
}

// Scene 5: self-contained final punch. Brand is not burned into the video.
function StartNow({ frame: f }: { frame: number }) {
  const s = 720;
  const radial = interpolate(f, [s + 15, s + 135], [.2, 1.8], clamp);
  return <AbsoluteFill style={{ opacity: fade(f, s), overflow: 'hidden', background: '#FA513D', color: '#201819' }}>
    <div style={{ position: 'absolute', left: -310, top: -240, width: 1080, height: 1080, border: '120px solid #FF8A55', borderRadius: '50%', transform: 'scale(' + radial + ')' }} />
    <div style={{ position: 'absolute', left: 80, right: 80, top: 430 }}>
      <Reveal frame={f} start={s} delay={10}>
        <div style={{ ...headline(218, '#22171A'), letterSpacing: -15 }}>START.</div>
      </Reveal>
      <Reveal frame={f} start={s} delay={33}>
        <div style={{ ...headline(270, '#FFFBEA'), letterSpacing: -18 }}>NOW.</div>
      </Reveal>
    </div>
    <Reveal frame={f} start={s} delay={75} style={{ position: 'absolute', left: 86, bottom: 440, right: 70 }}>
      <div style={{ fontSize: 57, color: '#27171B', fontFamily: 'Inter, sans-serif', fontWeight: 900, lineHeight: 1.18 }}>
        YOUR FUTURE<br />IS WATCHING.
      </div>
    </Reveal>
    <div style={{ position: 'absolute', bottom: -320, right: -140, width: 750, height: 750, border: '80px solid #22171A', borderRadius: '50%', opacity: .12, transform: 'scale(' + (1 + radial / 5) + ')' }} />
  </AbsoluteFill>;
}

export const Motion30 = ({ includeNarration = false, includeMusic = false }: MotionProps) => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{ background: '#141321' }}>
    <BreakPerfection frame={frame} />
    <SmallAction frame={frame} />
    <BuildMomentum frame={frame} />
    <FindThePath frame={frame} />
    <StartNow frame={frame} />
    {includeNarration && <Audio src={staticFile('voiceovers/motion30.wav')} volume={1} />}
    {includeMusic && <Audio src={staticFile('voiceovers/motion30-bed.wav')} volume={0.28} />}
  </AbsoluteFill>;
};
