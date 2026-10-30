import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion'
import { MotionText } from './MotionText'
import { MOTION_PRESETS, type MotionPresetName } from './motionMath'

export const MOTION_TOOLKIT_DEMO_FRAMES = 240

const examples: { name: string; preset: MotionPresetName; text: string; note: string }[] = [
	{ name: '01 / FADE', preset: 'signalFade', text: 'Fade into focus', note: 'Soft entrance, quiet confidence' },
	{ name: '02 / SLIDE', preset: 'cleanSlide', text: 'Slide with intent', note: 'Directional movement, clean stop' },
	{ name: '03 / SCALE', preset: 'softScale', text: 'Scale to emphasize', note: 'A measured rise in presence' },
	{ name: '04 / BOUNCE', preset: 'impactBounce', text: 'Bounce with control', note: 'One spring, no endless wobble' },
	{ name: '05 / MASK', preset: 'windowReveal', text: 'Reveal the headline', note: 'A clipped, left-to-right reveal' },
	{ name: '06 / STAGGER', preset: 'wordCascade', text: 'Build word by word', note: 'Characters arrive in a measured cascade' },
]

const MotionSample = ({ name, preset, text, note, index }: typeof examples[number] & { index: number }) => {
	const accent = MOTION_PRESETS[preset].accentColor
	const column = index % 3
	const row = Math.floor(index / 3)
	const left = 112 + column * 568
	const top = 306 + row * 286
	return <>
		<div style={{ position: 'absolute', left, top, width: 536, height: 254, padding: '25px 28px', boxSizing: 'border-box', border: '1px solid #394649', borderRadius: 6, background: '#182124' }}>
			<div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: accent, fontFamily: "'Montserrat', sans-serif", fontSize: 15, fontWeight: 800, letterSpacing: 1 }}>
				<span>{name}</span><span style={{ width: 9, height: 9, borderRadius: 9, background: accent }} />
			</div>
			<div style={{ position: 'absolute', left: 28, top: 91, width: 480 }}>
				<MotionText text={text} preset={preset} fromFrame={24} exitAtFrame={202} exitDurationInFrames={20} exitVariant="fade" fontSize={38} lineHeight={1.16} />
			</div>
			<div style={{ position: 'absolute', left: 28, right: 24, bottom: 23, color: '#AAB7B6', fontFamily: "'Montserrat', sans-serif", fontSize: 16, fontWeight: 500 }}>{note}</div>
		</div>
	</>
}

export const MotionToolkitDemo = () => {
	const frame = useCurrentFrame()
	const progress = interpolate(frame, [0, MOTION_TOOLKIT_DEMO_FRAMES - 1], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
	return <AbsoluteFill style={{ overflow: 'hidden', background: '#101719', color: '#F3F4EF', fontFamily: "'Montserrat', sans-serif" }}>
		<AbsoluteFill style={{ opacity: 0.18, backgroundImage: 'linear-gradient(#415052 1px, transparent 1px), linear-gradient(90deg, #415052 1px, transparent 1px)', backgroundSize: '56px 56px' }} />
		<div style={{ position: 'absolute', left: 112, top: 61, color: '#B9F36A', fontSize: 16, fontWeight: 800, letterSpacing: 1 }}>VIDEO AI EDITOR / ORIGINAL MOTION SYSTEM</div>
		<div style={{ position: 'absolute', left: 110, top: 105, fontSize: 62, fontWeight: 800, lineHeight: 1.05 }}>Move a message.</div>
		<div style={{ position: 'absolute', right: 114, top: 132, color: '#AAB7B6', fontSize: 18, fontWeight: 600 }}>FRAME-DRIVEN / REUSABLE / EDITABLE</div>
		{examples.map((example, index) => <MotionSample key={example.name} {...example} index={index} />)}
		<div style={{ position: 'absolute', left: 112, right: 112, bottom: 47, color: '#AAB7B6', fontSize: 15, fontWeight: 700, display: 'flex', justifyContent: 'space-between' }}>
			<span>30 FPS <span style={{ color: '#647274' }}>/</span> 8 SECONDS <span style={{ color: '#647274' }}>/</span> 16:9</span>
			<span>Six original presets <span style={{ color: '#647274' }}>/</span> custom timing and typography</span>
		</div>
		<div style={{ position: 'absolute', left: 112, right: 112, bottom: 28, height: 3, background: '#344143' }}>
			<div style={{ width: `${progress}%`, height: '100%', background: '#B9F36A' }} />
		</div>
	</AbsoluteFill>
}