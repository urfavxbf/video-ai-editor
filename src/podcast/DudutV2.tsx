import { Video } from '@remotion/media';
import type { CSSProperties } from 'react';
import { AbsoluteFill, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Sfx } from '../fx/sfx';
import { fxSpring, popSpring } from '../fx/shared';

/**
 * Dudut Lang — 11 YEARS / Editorial podcast edit V2.
 * Prioritize faces and native footage; no giant quote cards.
 * Source: 50812.mp4, 1920x864, 93.7s. Timeline: source 42–84s.
 * Two synchronized views of the source simulate independently cut cameras.
 * Check left/right speaker mapping against the actual recording before publishing.
 */
export type DudutV2Props = {
  videoPath: string;
  sourceStartSeconds: number;
};

export const DUDUT_V2_DURATION = 42 * 30;
const WHITE = '#f6f3eb';
const GOLD = '#eecb82';
const LIME = '#c1fc74';
const INK = '#080a0b';
const FONT = "'Montserrat', 'Inter', sans-serif";

type Caption = { from: number; to: number; text: string; key?: string };
const captions: Caption[] = [
  { from: 0.00, to: 1.52, text: 'Pero ginawa mo ba yun?' },
  { from: 1.52, to: 3.40, text: 'Siyempre, 11 YEARS nga, di ba?', key: '11 YEARS' },
  { from: 3.40, to: 5.90, text: 'Ginawa mo ba siya' },
  { from: 5.90, to: 7.98, text: 'out of respect?' },
  { from: 7.98, to: 10.60, text: 'Doon sa 11 years?' },
  { from: 10.60, to: 11.70, text: 'Na hindi mo sinabi' },
  { from: 11.70, to: 14.30, text: 'because of respect' },
  { from: 14.30, to: 16.25, text: 'O yun yung tama?' },
  { from: 16.25, to: 17.25, text: 'Parang mali, parang mali.' },
  { from: 17.25, to: 19.85, text: 'Hindi siya respect' },
  { from: 19.85, to: 21.82, text: 'para doon sa kabila.' },
  { from: 22.00, to: 23.48, text: 'RESPETO SA SARILI KO TALAGA.', key: 'RESPETO SA SARILI' },
  { from: 23.48, to: 25.65, text: 'Respeto sa sarili ko.' },
  { from: 25.65, to: 26.18, text: 'Ganun.' },
  { from: 26.56, to: 27.53, text: 'Money!' },
  { from: 28.98, to: 31.95, text: 'Respeto talaga sa sarili ko.' },
  { from: 31.95, to: 35.15, text: 'Kumbaga, I will not give' },
  { from: 35.15, to: 36.18, text: 'you the dignity...' },
  { from: 36.18, to: 38.57, text: 'THE SATISFACTION!', key: 'THE SATISFACTION' },
  { from: 38.57, to: 41.66, text: 'Hindi mo ako makitang umiiyak!', key: 'UMIIYAK' },
];

const phrases = [
  { from: 0.1, to: 3.7, top: '11 YEARS', bottom: 'AT NATAHIMIK?', color: GOLD },
  { from: 5.1, to: 8.4, top: 'OUT OF', bottom: 'RESPECT?', color: WHITE },
  { from: 17.35, to: 21.5, top: 'HINDI PARA', bottom: 'SA KABILA.', color: GOLD },
  { from: 21.9, to: 26.9, top: 'RESPETO SA', bottom: 'SARILI KO.', color: LIME },
  { from: 35.9, to: 38.8, top: 'THE', bottom: 'SATISFACTION.', color: GOLD },
  { from: 38.7, to: 42, top: 'HINDI MO', bottom: 'AKO MAKITANG UMIYAK.', color: WHITE },
];

const clamp = (v: number) => Math.min(1, Math.max(0, v));
const enter = (seconds: number, from: number, len = 0.23) => clamp((seconds - from) / len);
const leave = (seconds: number, to: number, len = 0.2) => clamp((to - seconds) / len);

const VideoLayer = ({
  src, trimBefore, position, muted, style = {},
}: {
  src: string; trimBefore: number; position: string; muted?: boolean; style?: CSSProperties;
}) => (
  <Video
    src={src}
    trimBefore={trimBefore}
    durationInFrames={DUDUT_V2_DURATION}
    muted={muted}
    volume={muted ? 0 : 1}
    style={{
      position: 'absolute', width: '100%', height: '100%', objectFit: 'cover',
      objectPosition: position, ...style,
    }}
  />
);

export const DudutV2 = ({ videoPath, sourceStartSeconds }: DudutV2Props) => {
  const f = useCurrentFrame();
  const t = f / 30;
  const src = staticFile(videoPath);
  const trimBefore = Math.round(sourceStartSeconds * 30);
  const caption = captions.find((c) => c.from <= t && t < c.to);
  const phrase = phrases.find((p) => p.from <= t && t < p.to);
  const phaseStart = t < 3.7 ? 0.1 : t < 8.4 ? 5.1 : t < 21.5 ? 17.35 : t < 26.9 ? 21.9 : t < 38.8 ? 35.9 : 38.7;
  const anim = fxSpring(f, Math.round(phaseStart * 30), { stiffness: 170, damping: 24, mass: 0.72 });
  const fadePhrase = phrase ? enter(t, phrase.from) * leave(t, phrase.to) : 0;
  const showDuo = t < 17.25 || (t >= 31.9 && t < 38.7);
  const portraitRight = t >= 17.25 && t < 31.9;
  const focusPosition = portraitRight ? '78% center' : (t >= 38.7 ? '78% center' : '25% center');
  const zoom = interpolate(t, [0, 4, 10, 17.2, 22, 27, 32, 38.7, 42], [1, 1.06, 1.02, 1.03, 1.095, 1.02, 1.06, 1.095, 1.06], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp'
  });
  const firstHalf = t < 17.25;
  const dynamicColor = t >= 21.9 && t < 31.9 ? LIME : GOLD;
  const sceneFlash = Math.max(
    1 - Math.abs(t - 17.25) / 0.14,
    1 - Math.abs(t - 21.95) / 0.14,
    1 - Math.abs(t - 38.65) / 0.14,
  );
  const isEmphatic = Boolean(caption?.key);
  const capPop = caption ? popSpring(f, Math.round(caption.from * 30)) : 1;
  const progress = t / 42;

  return (
    <AbsoluteFill style={{ background: INK, color: WHITE, fontFamily: FONT, overflow: 'hidden' }}>
      {/* Real video is the hero: 75% of the frame, not a tiny horizontal picture-in-picture. */}
      <div style={{
        position:'absolute', inset:0, background:'linear-gradient(155deg,#141a19,#050809 70%)'
      }} />
      <div style={{
        position:'absolute', top:130, left:0, right:0, height:1500, overflow:'hidden',
        borderTop:'2px solid rgba(255,255,255,.25)',
        borderBottom:'2px solid rgba(255,255,255,.25)',
      }}>
        <VideoLayer src={src} trimBefore={trimBefore} position={focusPosition} style={{
          transform:'scale(' + zoom + ')',
          filter:'contrast(1.07) saturate(.94) brightness(.88)',
          transformOrigin:focusPosition,
        }} />
        {/* A second synchronized camera angle is only visible during conversational exchanges. */}
        {showDuo && (
          <>
            <div style={{
              position:'absolute', top:firstHalf?0:110, left:18, right:18, height:593,
              overflow:'hidden', borderRadius:19, border:'2px solid rgba(255,255,255,.72)',
              boxShadow:'0 30px 60px rgba(0,0,0,.5)',
            }}>
              <VideoLayer src={src} trimBefore={trimBefore} muted position='22% center'
                style={{filter:'contrast(1.08) saturate(.98)',transform:'scale(1.35)',transformOrigin:'25% center'}} />
              <div style={{
                position:'absolute', left:0, top:0, bottom:0, width:7, background:GOLD,
              }}/>
            </div>
            <div style={{
              position:'absolute', bottom:firstHalf?0:110, left:18, right:18, height:593,
              overflow:'hidden', borderRadius:19, border:'2px solid rgba(255,255,255,.72)',
              boxShadow:'0 30px 60px rgba(0,0,0,.5)',
            }}>
              <VideoLayer src={src} trimBefore={trimBefore} muted position='78% center'
                style={{filter:'contrast(1.08) saturate(.98)',transform:'scale(1.35)',transformOrigin:'75% center'}} />
              <div style={{
                position:'absolute', right:0, top:0, bottom:0, width:7, background:LIME,
              }}/>
            </div>
          </>
        )}
        {/* Frame edges are deliberate, but there is no fake heavy blur on the faces. */}
        <div style={{
          position:'absolute', inset:0, pointerEvents:'none',
          background:'linear-gradient(180deg,rgba(2,6,7,.20) 0%,transparent 19%,transparent 65%,rgba(2,6,7,.82) 100%)'
        }}/>
        {portraitRight && (
          <div style={{
            position:'absolute', right:30, top:32, padding:'9px 16px',
            border:'1px solid rgba(193,252,116,.85)', borderRadius:5,
            color:LIME, background:'rgba(3,9,5,.78)', fontSize:22, fontWeight:900,
            letterSpacing:2
          }}>REAL TALK • DUDUT</div>
        )}
      </div>

      {/* Refined top rail with episode metadata, not a permanent massive title panel. */}
      <div style={{
        position:'absolute', left:45, right:45, top:48, height:40, display:'flex',
        justifyContent:'space-between', alignItems:'center', fontSize:20, fontWeight:800,
        letterSpacing:3
      }}>
        <span style={{color:WHITE}}>GALIT-GALITAN <span style={{color:GOLD}}> /  DUDUT LANG</span></span>
        <span style={{color:'#abb6b5', fontSize:17}}>PODCAST CUT 02</span>
      </div>

      {/* Big editorial impact type appears briefly and varies with the actual sentence. */}
      {phrase && (
        <div style={{
          position:'absolute', top: t >= 21.9 && t < 32 ? 880 : t>=38.7?1060:790,
          left:45, right:45, zIndex:3,
          opacity:fadePhrase,
          transform:'translate3d(' + ((1-anim)*-120) + 'px,' + ((1-anim)*22) + 'px,0) rotate(' + ((1-anim)*-2.5) + 'deg)',
          filter:'drop-shadow(0 12px 15px rgba(0,0,0,.8))',
        }}>
          <div style={{
            display:'inline-block', background:INK, borderLeft:'10px solid ' + phrase.color,
            padding:'9px 22px 8px', color:WHITE, fontSize:phrase.top.length>15?48:67,
            fontWeight:900, letterSpacing:-1.6, lineHeight:1.06
          }}>{phrase.top}</div>
          <div style={{height:9}}/>
          <div style={{
            display:'inline-block', background:phrase.color, color:INK,
            padding:'8px 22px', maxWidth:990,
            fontSize:phrase.bottom.length>18?50:phrase.bottom.length>14?60:78,
            fontWeight:900, lineHeight:1.09, letterSpacing:-2.1,
            boxShadow:'12px 13px 0 rgba(0,0,0,.7)'
          }}>{phrase.bottom}</div>
        </div>
      )}

      {/* Motion-design accents animate near the pivotal 11-year and respect lines. */}
      {t>=0.3 && t<4.5 && (
        <div style={{
          position:'absolute', top:240, right:53, width:160, height:160,
          border:'4px solid ' + GOLD, borderRadius:160, display:'flex',
          justifyContent:'center', alignItems:'center',
          transform:'rotate(' + (t*10) + 'deg) scale(' + (0.88 + 0.08*Math.sin(f/13)) + ')',
          boxShadow:'0 0 0 11px rgba(0,0,0,.20)',
        }}>
          <span style={{fontSize:52, fontWeight:900}}>11</span>
        </div>
      )}
      {t>=21.95 && t<31.9 && (
        <div style={{
          position:'absolute', right:55, top:330, width:100, height:100,
          border:'3px solid ' + LIME, transform:'rotate(' + (t*20) + 'deg)',
          opacity:.8
        }}>
          <div style={{position:'absolute',left:36,top:0,bottom:0,width:4,background:LIME}}/>
          <div style={{position:'absolute',top:35,left:0,right:0,height:4,background:LIME}}/>
        </div>
      )}

      {/* Clean subtitles track the recorded words. The background is a local translucent strip,
          not an always-on quote card spanning a third of the screen. */}
      <div style={{
        position:'absolute', left:38, right:38, bottom:164, height:235,
        display:'flex', justifyContent:'center', alignItems:'center',
        zIndex:6
      }}>
        {caption && (
          <div style={{
            padding:'14px 24px', maxWidth:'100%',
            fontFamily:"'Montserrat','Inter',sans-serif",
            fontSize:isEmphatic?62:51, fontWeight:900,
            lineHeight:1.15, textAlign:'center', letterSpacing:-1.4,
            color:isEmphatic?dynamicColor:WHITE,
            textShadow:'0px 4px 8px rgba(0,0,0,.95), 0 0 25px rgba(0,0,0,.7)',
            background:'rgba(0,0,0,.27)', borderRadius:13,
            opacity:clamp((t-caption.from)*12)*clamp((caption.to-t)*11),
            transform:'translateY(' + ((1-capPop)*32) + 'px) scale(' + (.96+.04*capPop) + ')',
          }}>{caption.text}</div>
        )}
      </div>

      {/* Editorial footer and progress bar. */}
      <div style={{
        position:'absolute', bottom:90, left:49, right:49, height:2,
        background:'rgba(255,255,255,.2)',
      }}>
        <div style={{width:(progress*100)+'%',height:5,background:dynamicColor,marginTop:-2}} />
      </div>
      <div style={{
        position:'absolute', bottom:35, left:50, right:50, display:'flex',
        justifyContent:'space-between', alignItems:'center', color:'#a4a9a6',
        fontSize:19, fontWeight:800, letterSpacing:2
      }}>
        <span>11 YEARS / SELF-RESPECT</span>
        <span>{String(Math.floor(t)).padStart(2,'0')} / 42</span>
      </div>

      {/* 3–4-frame cut flashes support the story without hiding the face. */}
      <AbsoluteFill style={{background:WHITE, opacity:clamp(sceneFlash)*.16, pointerEvents:'none'}}/>
      <Sfx cues={[
        {at:45,sound:'hit',volume:.14},
        {at:524,sound:'whip',volume:.12},
        {at:660,sound:'reveal',volume:.12},
        {at:1100,sound:'hit',volume:.11},
      ]}/>
    </AbsoluteFill>
  );
};
