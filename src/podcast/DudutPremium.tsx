import { Video } from '@remotion/media';
import {
  AbsoluteFill,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import { fxSpring, popSpring } from '../fx/shared';
import { Sfx } from '../fx/sfx';

/**
 * Dudut Lang / Galit-Galitan highlight
 * Original uploaded clip: 1920x864 @ 93.7s.
 * Use the verified source range 00:42–01:24 (42s).
 * Preserve the complete wide podcast frame (no aggressive face crop).
 * Source footage belongs in public/takes/dudut/clip.mp4 (gitignored).
 */
export type DudutPremiumProps = {
  videoPath: string;
  sourceStartSeconds: number;
};

export const DUDUT_DURATION = 42 * 30;

const INK = '#090e17';
const IVORY = '#fff9ed';
const MUTED = '#acb6c7';
const AMBER = '#f6c77c';
const AQUA = '#93e7df';

type Caption = { from: number; to: number; text: string; highlight?: boolean };

/** Timestamped against the 93.7-second user-supplied source, shifted by -42 seconds. */
const captions: Caption[] = [
  { from: 0, to: 3.36, text: "Pero ginawa mo ba 'yun? Siyempre, 11 years nga, 'di ba?" },
  { from: 3.60, to: 7.96, text: "Ginawa mo ba siya out of respect sa 11 years na kayo?" },
  { from: 7.96, to: 11.66, text: "Na hindi mo siya sinabi because of respect to that 11 years?" },
  { from: 11.66, to: 16.27, text: "Or hindi mo lang sinabi kasi parang 'yun 'yung tama?" },
  { from: 16.27, to: 17.25, text: 'Parang mali, parang mali.' },
  { from: 17.25, to: 21.78, text: "Hindi siya respect para do'n sa kabila." },
  { from: 22.00, to: 23.48, text: 'RESPETO SA SARILI KO TALAGA.', highlight: true },
  { from: 23.48, to: 26.10, text: 'Respeto sa sarili ko. Ganoon!' },
  { from: 26.55, to: 27.55, text: 'Money!' },
  { from: 28.98, to: 31.96, text: 'Hindi, respeto talaga sa sarili ko.' },
  { from: 31.96, to: 36.20, text: 'Kumbaga, I will not give you the dignity.' },
  { from: 36.20, to: 38.56, text: 'The satisfaction!', highlight: true },
  { from: 38.56, to: 41.64, text: 'Hindi mo ako makitang umiiyak!', highlight: true },
];

const phase = (t: number) => {
  if (t < 7.5) return { kicker: 'ISANG RELASYON', headline: '11 YEARS', sub: 'Bakit piniling manahimik?' };
  if (t < 17.5) return { kicker: 'ANG TANONG', headline: 'RESPETO BA?', sub: 'Sa labing-isang taong pinagsamahan?' };
  if (t < 22) return { kicker: 'ANG TUNAY NA DAHILAN', headline: 'HINDI PARA SA KABILA.', sub: 'Hindi tungkol sa opinyon ng iba.' };
  if (t < 31.5) return { kicker: 'ANG SAGOT NI DUDUT', headline: 'RESPETO SA SARILI.', sub: 'Ito ang pinili niyang panghawakan.' };
  if (t < 38.5) return { kicker: 'ISANG DESISYON', headline: 'NO SATISFACTION.', sub: 'Walang kailangang patunayan.' };
  return { kicker: 'ANG HULING LINYA', headline: 'HINDI MO AKO MAKITANG UMIYAK.', sub: 'Self-respect, not silence.' };
};

const barHeights = [18, 42, 28, 64, 35, 55, 24, 74, 45, 32, 58, 28, 63, 43, 22, 55, 36, 70, 27, 48, 35];

export const DudutPremium = ({
  videoPath,
  sourceStartSeconds,
}: DudutPremiumProps) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const active = captions.find((c) => c.from <= t && t < c.to);
  const current = phase(t);
  const sceneStart = t < 7.5 ? 0 : t < 17.5 ? 7.5 : t < 22 ? 17.5 : t < 31.5 ? 22 : t < 38.5 ? 31.5 : 38.5;
  const localFrames = Math.max(0, f - Math.round(sceneStart * 30));
  const headlineReveal = fxSpring(localFrames, 0, { damping: 24, stiffness: 145, mass: 0.7 });
  const subReveal = fxSpring(localFrames, 7, { damping: 23, stiffness: 112, mass: 0.75 });
  const bigPill = t >= 22 && t < 31.5;
  const dramatic = t >= 38.5;
  const movingFrame = interpolate(t, [0, 12, 21.8, 22.2, 30, 38.5, 42], [1, 1.02, 1.015, 1.055, 1.012, 1.045, 1.02], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const pulse = 0.5 + 0.5 * Math.sin(f / 11);
  const accent = bigPill ? AQUA : AMBER;
  const captionProgress = active ? popSpring(f, Math.round(active.from * 30)) : 0;
  const trimBefore = Math.round(sourceStartSeconds * 30);

  return (
    <AbsoluteFill style={{
      background: INK, color: IVORY, overflow: 'hidden',
      fontFamily: "'Inter', sans-serif",
    }}>
      {/* Graded background with precise lines rather than soft blurry video. */}
      <AbsoluteFill style={{
        background: dramatic
          ? 'radial-gradient(ellipse at 50% 35%, #252b33 0%, #090e17 70%)'
          : 'radial-gradient(ellipse at 58% 29%, #20303d 0%, #101923 50%, #090e17 86%)',
      }} />
      <AbsoluteFill style={{
        opacity: 0.33, backgroundImage: 'linear-gradient(rgba(238,245,253,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(238,245,253,.05) 1px, transparent 1px)',
        backgroundSize: '85px 85px',
      }} />
      <div style={{
        position: 'absolute', top: 89, left: 60, right: 60,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        fontSize: 25, fontWeight: 800, letterSpacing: 5, color: MUTED,
      }}>
        <span>GALIT-GALITAN</span>
        <span style={{ fontWeight: 500, letterSpacing: 3, color: accent }}>DUDUT LANG  /  EP. 09</span>
      </div>
      <div style={{ position: 'absolute', top: 145, left: 58, right: 58, height: 2, background: 'linear-gradient(90deg, #f6c77c, transparent)' }} />

      {/* Editorial headline: changes by dialogue beat, not every word. */}
      <div style={{
        position: 'absolute', top: 207, left: 62, right: 62,
        opacity: headlineReveal, transform: `translateY(${(1 - headlineReveal) * 32}px)`,
      }}>
        <div style={{ color: accent, fontSize: 25, fontWeight: 800, letterSpacing: 5, marginBottom: 23 }}>
          {current.kicker}
        </div>
        <div style={{
          fontFamily: "'Montserrat', sans-serif",
          fontWeight: 900, fontSize: current.headline.length > 24 ? 56 : current.headline.length > 18 ? 65 : current.headline.length > 13 ? 77 : 116,
          letterSpacing: current.headline.length > 18 ? -1 : -4,
          lineHeight: 1.05,
          maxWidth: 950,
          color: bigPill ? AQUA : IVORY,
          textShadow: bigPill ? '0 0 28px rgba(147,231,223,.17)' : 'none',
        }}>
          {current.headline}
        </div>
        <div style={{
          marginTop: 23, color: MUTED, fontSize: 30, fontWeight: 500,
          opacity: subReveal, transform: `translateX(${(1 - subReveal) * -15}px)`,
        }}>
          {current.sub}
        </div>
      </div>

      {/* A no-crop wide podcast frame keeps BOTH hosts legible. */}
      <div style={{
        position: 'absolute', top: 646, left: 45, width: 990, height: 452,
        borderRadius: 27, border: `3px solid ${bigPill ? 'rgba(147,231,223,.9)' : 'rgba(246,199,124,.5)'}`,
        boxShadow: bigPill
          ? '0 12px 70px rgba(67,198,197,.22), 0 30px 90px rgba(0,0,0,.5)'
          : '0 26px 70px rgba(0,0,0,.6)',
        overflow: 'hidden', background: '#050708',
      }}>
        <Video
          src={staticFile(videoPath)}
          trimBefore={trimBefore}
          durationInFrames={DUDUT_DURATION}
          volume={1}
          style={{
            display: 'block', position: 'absolute', width: '100%', height: '100%',
            objectFit: 'contain', transform: `scale(${movingFrame})`,
            transformOrigin: '50% 50%',
          }}
        />
        <div style={{
          position: 'absolute', left: 20, top: 20, padding: '9px 17px',
          background: 'rgba(5,10,17,.8)', color: '#dfe8eb',
          fontSize: 20, letterSpacing: 2, fontWeight: 700, borderRadius: 7,
        }}>
          ORIGINAL PODCAST MOMENT
        </div>
        {bigPill && <div style={{
          position: 'absolute', right: 17, bottom: 17,
          background: 'rgba(7,19,24,.83)', border: '1px solid rgba(147,231,223,.65)',
          padding: '10px 18px', borderRadius: 12, color: AQUA, fontSize: 24, fontWeight: 900,
        }}>SELF-RESPECT</div>}
      </div>

      {/* Deliberate line art and small motion graphics, reusing repo spring language. */}
      <div style={{ position: 'absolute', top: 1165, left: 64, right: 64, display: 'flex', gap: 8, alignItems: 'center', height: 90 }}>
        {barHeights.map((h, i) => <div key={i} style={{
          width: 16, height: h * (0.65 + 0.35 * Math.sin(f / 7 + i * 0.85) ** 2),
          borderRadius: 9, background: i % 5 === 0 ? AQUA : accent,
          opacity: 0.43 + 0.29 * pulse,
        }} />)}
        <div style={{ marginLeft: 'auto', letterSpacing: 4, color: MUTED, fontSize: 23, fontWeight: 700 }}>REAL TALK</div>
      </div>

      <div style={{
        position: 'absolute', top: 1300, left: 60, right: 60,
        minHeight: 295, padding: '38px 45px',
        background: bigPill ? 'rgba(41,85,91,.32)' : 'rgba(236,236,236,.065)',
        border: `2px solid ${bigPill ? 'rgba(147,231,223,.53)' : 'rgba(246,199,124,.22)'}`,
        borderRadius: 26, display: 'flex', alignItems: 'center', justifyContent: 'center',
        boxShadow: '0 20px 70px rgba(0,0,0,.13)',
      }}>
        <div style={{
          textAlign: 'center',
          fontSize: active?.highlight ? 57 : 46,
          fontFamily: "'Montserrat', sans-serif", fontWeight: 850,
          lineHeight: 1.32, letterSpacing: -0.7,
          color: active?.highlight ? accent : IVORY,
          opacity: active ? 1 : 0,
          transform: `translateY(${Math.max(0, (1 - captionProgress) * 26)}px)`,
          textShadow: active?.highlight ? '0 0 24px rgba(246,199,124,.1)' : 'none',
        }}>
          {active?.text ?? ''}
        </div>
      </div>

      <div style={{
        position: 'absolute', left: 65, right: 65, bottom: 165,
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        color: MUTED, fontSize: 24, letterSpacing: 2, fontWeight: 800,
      }}>
        <span>11 YEARS • SELF-RESPECT</span>
        <span>{String(Math.floor(sourceStartSeconds + t) / 60 | 0).padStart(2, '0')}:{String(Math.floor((sourceStartSeconds + t) % 60)).padStart(2, '0')}</span>
      </div>
      <div style={{ position: 'absolute', bottom: 132, left: 65, width: 950, height: 5, borderRadius: 8, background: 'rgba(255,255,255,.1)' }}>
        <div style={{ width: `${t / 42 * 100}%`, height: '100%', background: `linear-gradient(90deg, ${AMBER}, ${AQUA})`, borderRadius: 8 }} />
      </div>

      {/* Subtle earcons from the original repo's Sfx library, not a constant noise bed. */}
      <Sfx cues={[
        { at: 1, sound: 'reveal', volume: 0.11 },
        { at: 660, sound: 'chime', volume: 0.14 },
      ]} />
    </AbsoluteFill>
  );
};
