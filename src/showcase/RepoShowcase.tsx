import React from 'react';
import {AbsoluteFill, interpolate, Sequence, spring, useCurrentFrame} from 'remotion';

/**
 * 18-second, footage-free product reel built using real Remotion animation.
 * Scenes intentionally illustrate capabilities; they do not claim to replay all 21 FX.
 */
export const REPO_SHOWCASE_FPS = 30;
export const REPO_SHOWCASE_FRAMES = 18 * REPO_SHOWCASE_FPS;
const INK = '#080e17';
const WHITE = '#f5f3ee';
const CORAL = '#ff8565';
const MINT = '#c8ff91';
const LILAC = '#b5a5ff';
const MUTED = '#a2b0bc';
const FONT = "'Montserrat','Inter',sans-serif";
const ease = (f: number, start = 0) =>
  spring({fps: REPO_SHOWCASE_FPS, frame: Math.max(0, f - start),
    config: {damping: 23, stiffness: 120, mass: 0.72}});
const heading: React.CSSProperties = {
  fontFamily: FONT, fontWeight: 950, letterSpacing: -5, lineHeight: 0.98,
  textShadow: '0 14px 35px rgba(0,0,0,.23)',
};
const Badge = ({children, color = MINT}: {children: React.ReactNode; color?: string}) =>
  <div style={{alignSelf: 'flex-start', display: 'inline-flex', color, background: '#18242b',
    border: '1px solid #35474e', padding: '12px 28px', borderRadius: 40,
    letterSpacing: 4, fontSize: 25, fontWeight: 800}}>{children}</div>;
const Background = () => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 80% 20%, #24213b 0%, #121d2b 34%, #070c15 80%)'}}>
    <AbsoluteFill style={{opacity: .22,
      backgroundImage: 'linear-gradient(#516171 1px, transparent 1px), linear-gradient(90deg, #516171 1px, transparent 1px)',
      backgroundSize: '120px 120px', transform: 'translateX(' + (frame % 120) / 3 + 'px)'}}/>
  </AbsoluteFill>;
};
const Layout = ({children, index}: {children: React.ReactNode; index: string}) =>
  <AbsoluteFill style={{color: WHITE, fontFamily: FONT, padding: '265px 68px 210px'}}>
    {children}
    <div style={{position: 'absolute', top: 64, left: 66, display: 'flex', gap: 25, alignItems: 'center'}}>
      <div style={{width: 68, height: 68, borderRadius: 17, background: CORAL, display: 'flex',
        alignItems: 'center', justifyContent: 'center', color: INK, fontSize: 42, fontWeight: 950}}>V</div>
      <span style={{fontSize: 28, fontWeight: 900, letterSpacing: 3}}>VIDEO / AI / EDITOR</span>
    </div>
    <div style={{position: 'absolute', left: 68, right: 68, bottom: 87, display: 'flex',
      justifyContent: 'space-between', fontSize: 25, color: MUTED, fontWeight: 800}}>
      <span>{index} / CREATIVE SHOWCASE</span><span>2026</span>
    </div>
  </AbsoluteFill>;
const Title = () => {
  const f = useCurrentFrame();
  const e = ease(f);
  return <Layout index="INTRO">
    <Badge color={CORAL}>THE NEXT CUT</Badge>
    <div style={{...heading, fontSize: 242, marginTop: 115,
      transform: 'translateX(' + (1-e)*-230 + 'px)'}}>
      <div>EDIT</div><div>LIKE</div><div style={{color: CORAL}}>YOU</div><div style={{fontSize: 146}}>MEAN IT.</div>
    </div>
    <div style={{fontSize: 43, color: MUTED, marginTop: 80}}>Motion. Storytelling. Precision.</div>
    <div style={{fontSize: 29, fontWeight: 800, letterSpacing: 3, color: MINT, marginTop: 22}}>ONE CREATIVE WORKSPACE</div>
  </Layout>;
};
const Motion = () => {
  const f = useCurrentFrame();
  const effects = [
    {n: 'SNAP ZOOM', sub: 'FAST / KINETIC', color: CORAL, icon: '◎'},
    {n: 'LIQUID GLASS', sub: 'DEPTH / REFINEMENT', color: LILAC, icon: '◉'},
    {n: 'FRAME ESCAPE', sub: 'LAYERS / IMMERSION', color: MINT, icon: '↗'},
  ];
  return <Layout index="MOTION">
    <Badge>01 / MOTION SYSTEM</Badge>
    <div style={{...heading, marginTop: 75, fontSize: 140}}>21 MOTION<br/><span style={{color: MINT}}>EFFECTS.</span></div>
    <div style={{fontSize: 36, color: MUTED, marginTop: 41, marginBottom: 98}}>Building blocks from the FX library.</div>
    {effects.map((it, i) => <div key={it.n} style={{height: 188, marginBottom: 27, padding: 25,
      borderRadius: 29, border: '2px solid #3e4d59', background: '#172531',
      display: 'flex', alignItems: 'center', gap: 38,
      opacity: ease(f, 7+i*7), transform: 'translateX(' + (1-ease(f, 7+i*7))*160 + 'px)'}}>
      <div style={{width: 129, height: 129, background: it.color, borderRadius: 22,
        color: INK, fontSize: 91, textAlign: 'center', lineHeight: '129px'}}>{it.icon}</div>
      <div><div style={{fontSize: 54, fontWeight: 900}}>{it.n}</div>
      <div style={{fontSize: 29, marginTop: 10, letterSpacing: 2, color: MUTED}}>{it.sub}</div></div>
    </div>)}
  </Layout>;
};
const Podcast = () => {
  const f = useCurrentFrame();
  const bars = Array.from({length: 37}, (_, i) => {
    const h = 17 + 90*Math.abs(Math.sin((i*19+f*3)*.12));
    return <div key={i} style={{width: 10, height: h, borderRadius: 5, background: CORAL}}/>;
  });
  return <Layout index="PODCAST">
    <Badge color={CORAL}>02 / PODCAST EDITING</Badge>
    <div style={{...heading, fontSize: 139, marginTop: 74}}>PODCAST<br/><span style={{color: CORAL}}>TO VIRAL.</span></div>
    <div style={{fontSize: 39, color: MUTED, marginTop: 41}}>Multi-camera rhythm. Impact typography.</div>
    <div style={{display: 'flex', gap: 18, marginTop: 105}}>
      {['CAM A','CAM B'].map((label, i) => <div key={label} style={{width: '50%', height: 395,
        position: 'relative', borderRadius: 30, background: i===0?'#294755':'#453856',
        overflow: 'hidden', border: '3px solid #6c7080'}}>
        <div style={{position: 'absolute', top: 35, left: 30, fontWeight: 900, fontSize: 29}}>{label}</div>
        <div style={{position: 'absolute', top: 110, left: 88, width: 140, height: 140,
          background: i===0?'#5a9fa9':'#a58db8', borderRadius: '50%',
          transform: 'translateY(' + Math.sin(f/8+i)*9 + 'px)'}}/>
        <div style={{position: 'absolute', left: 45, bottom: -38, width: 230, height: 200,
          background: i===0?'#4f8393':'#786291', borderRadius: 95}}/>
      </div>)}
    </div>
    <div style={{marginTop: 24, background: '#0a131f', padding: '25px 25px', borderRadius: 20,
      textAlign: 'center', fontSize: 59, fontWeight: 900, color: MINT}}>
      {['ANG TOTOONG', 'KWENTO AY', 'NASA EDIT.'][Math.min(2,Math.floor(f/30))]}
    </div>
    <div style={{display: 'flex', height: 180, gap: 7, alignItems: 'center', marginTop: 50,
      justifyContent: 'space-between'}}>{bars}</div>
  </Layout>;
};
const Captions = () => {
  const f = useCurrentFrame();
  const word = Math.min(2, Math.floor(f/30));
  return <Layout index="CAPTIONS">
    <Badge color={LILAC}>03 / DYNAMIC CAPTIONS</Badge>
    <div style={{...heading, fontSize: 153, marginTop: 85}}>SAY IT.<br/><span style={{color: LILAC}}>MAKE IT</span><br/>VISIBLE.</div>
    <div style={{fontSize: 36, color: MUTED, marginTop: 58}}>Tagalog / Taglish caption design.</div>
    <div style={{display: 'flex', gap: 16, marginTop: 105}}>
      {['BAKIT','NGA','BA?'].map((w,i)=><div key={w} style={{padding: '45px 20px',
        width: '33.33%', textAlign: 'center', fontWeight: 950, fontSize: 62, borderRadius: 26,
        color: i===word?INK:WHITE, background: i===word?LILAC:'#182631',
        border: '2px solid #707386',
        transform: 'scale(' + (i===word?1.04:1) + ')'}}>{w}</div>)}
    </div>
    <div style={{marginTop: 51, background: '#122330', borderRadius: 20, padding: 32,
      fontSize: 33, letterSpacing: 2, fontWeight: 800}}>WORD-TIMED • HIGH CONTRAST</div>
    <div style={{display: 'flex', gap: 6, alignItems: 'center', height: 200, marginTop: 40}}>
      {Array.from({length: 46},(_,i)=><div key={i} style={{width: 11, borderRadius: 5,
        height: 15+110*Math.abs(Math.sin(i*.76+f*.16)),
        background: i%7===0?CORAL:LILAC}}/>)}
    </div>
  </Layout>;
};
const Stack = () => {
  const f = useCurrentFrame();
  const entries = [
    ['REMOTION','Motion graphics & compositions'],
    ['FFMPEG','Video processing and mixdown'],
    ['GROQ STT','Speech-to-text captions'],
    ['VOXCPM2','Optional voice engine · testing'],
  ];
  return <Layout index="STACK">
    <Badge>04 / THE TOOLCHAIN</Badge>
    <div style={{...heading, fontSize: 147, marginTop: 85}}>POWERED<br/><span style={{color: MINT}}>BY CODE.</span></div>
    <div style={{fontSize: 39, color: MUTED, marginTop: 40}}>A modular creative production stack.</div>
    <div style={{marginTop: 110}}>
      {entries.map(([name, sub], i) => <div key={name} style={{marginBottom: 25, padding: '32px 35px',
        background: '#192a35', border: '2px solid #43535b', borderRadius: 22,
        opacity: ease(f,i*7), transform: 'translateX(' + (1-ease(f,i*7))*130 + 'px)'}}>
        <div style={{fontWeight: 950, fontSize: 54}}><span style={{color: MINT, marginRight: 28,
          fontSize: 36}}>{String(i+1).padStart(2,'0')}</span>{name}</div>
        <div style={{marginLeft: 90, fontSize: 29, color: MUTED, marginTop: 10}}>{sub}</div>
      </div>)}
    </div>
  </Layout>;
};
const Outro = () => {
  const f = useCurrentFrame();
  const e = ease(f);
  return <Layout index="OUTRO">
    <div style={{height: 980, background: '#172b32', border: '3px solid #5f7578', borderRadius: 45,
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      opacity: e, transform: 'scale(' + (.85+.15*e) + ')'}}>
      <div style={{fontSize: 180, width: 260, height: 230, borderRadius: 48,
        background: CORAL, color: INK, textAlign: 'center', fontWeight: 950}}>V</div>
      <div style={{...heading, textAlign: 'center', fontSize: 133, marginTop: 70}}>VIDEO AI<br/><span style={{color: CORAL}}>EDITOR.</span></div>
      <div style={{fontSize: 40, color: MINT, fontWeight: 900, marginTop: 50}}>CRAFT THE NEXT CUT.</div>
      <div style={{fontSize: 26, color: MUTED, marginTop: 80}}>github.com/urfavxbf/video-ai-editor</div>
    </div>
  </Layout>;
};
export const RepoShowcase = () => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{overflow: 'hidden'}}>
    <Background/>
    <Sequence from={0} durationInFrames={90}><Title/></Sequence>
    <Sequence from={90} durationInFrames={90}><Motion/></Sequence>
    <Sequence from={180} durationInFrames={90}><Podcast/></Sequence>
    <Sequence from={270} durationInFrames={90}><Captions/></Sequence>
    <Sequence from={360} durationInFrames={90}><Stack/></Sequence>
    <Sequence from={450} durationInFrames={90}><Outro/></Sequence>
    <div style={{position: 'absolute', left: 65, right: 65, bottom: 58, height: 7,
      borderRadius: 10, background: '#43535f'}}>
      <div style={{width: (100*frame/REPO_SHOWCASE_FRAMES)+'%',
        background: CORAL, height: '100%', borderRadius: 10}}/>
    </div>
  </AbsoluteFill>;
};
