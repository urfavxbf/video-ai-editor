import type { CSSProperties, ElementType, FC } from 'react'
import { useCurrentFrame } from 'remotion'
import {
	MOTION_PRESETS,
	resolveMotionState,
	type ExitVariant,
	type MotionEasing,
	type MotionPreset,
	type MotionPresetName,
	type MotionVariant,
} from './motionMath'

export type MotionTextProps = {
	text: string
	preset?: MotionPresetName | MotionPreset
	fromFrame?: number
	durationInFrames?: number
	easing?: MotionEasing
	color?: string
	accentColor?: string
	fontFamily?: string
	fontSize?: number
	fontWeight?: number
	lineHeight?: number
	letterSpacing?: number
	direction?: MotionPreset['direction']
	distance?: number
	fromScale?: number
	staggerInFrames?: number
	exitAtFrame?: number
	exitDurationInFrames?: number
	exitVariant?: ExitVariant
	reducedMotion?: boolean
	as?: 'span' | 'div'
	className?: string
	style?: CSSProperties
}

const motionStyle = (
	frame: number,
	variant: MotionVariant,
	staggerVariant: Exclude<MotionVariant, 'stagger'>,
	staggerInFrames: number,
	index: number,
	fromFrame: number,
	options: Omit<Parameters<typeof resolveMotionState>[1], 'variant' | 'fromFrame'>,
): CSSProperties => {
	const concreteVariant = variant === 'stagger' ? staggerVariant : variant
	const state = resolveMotionState(frame, {
		...options,
		variant: concreteVariant,
		fromFrame: fromFrame + (variant === 'stagger' ? index * staggerInFrames : 0),
	})
	return {
		display: 'inline-block',
		opacity: state.opacity,
		translate: `${state.translateX}px ${state.translateY}px`,
		scale: state.scale,
		clipPath: concreteVariant === 'masked-reveal' ? `inset(0 ${state.clipInsetRight}% 0 0)` : undefined,
		whiteSpace: 'pre-wrap',
	}
}

export const MotionText: FC<MotionTextProps> = ({
	text,
	preset = 'signalFade',
	fromFrame = 0,
	durationInFrames,
	easing,
	color,
	accentColor,
	fontFamily,
	fontSize,
	fontWeight,
	lineHeight,
	letterSpacing,
	direction,
	distance,
	fromScale,
	staggerInFrames,
	exitAtFrame,
	exitDurationInFrames,
	exitVariant,
	reducedMotion = false,
	as = 'span',
	className,
	style,
}) => {
	const frame = useCurrentFrame()
	const selected = typeof preset === 'string' ? MOTION_PRESETS[preset] : preset
	const variant = selected.variant
	const staggerVariant = selected.staggerVariant
	const unitStyle = (index: number) => motionStyle(frame, variant, staggerVariant, staggerInFrames ?? selected.staggerInFrames, index, fromFrame, {
		durationInFrames: durationInFrames ?? selected.durationInFrames,
		easing: easing ?? selected.easing,
		direction: direction ?? selected.direction,
		distance: distance ?? selected.distance,
		fromScale: fromScale ?? selected.fromScale,
		exitAtFrame,
		exitDurationInFrames,
		exitVariant,
		reducedMotion,
	})
	const Tag: ElementType = as
	const typography: CSSProperties = {
		fontFamily: fontFamily ?? selected.fontFamily,
		fontSize: fontSize ?? selected.fontSize,
		fontWeight: fontWeight ?? selected.fontWeight,
		lineHeight: lineHeight ?? selected.lineHeight,
		letterSpacing: letterSpacing ?? selected.letterSpacing,
		color: color ?? selected.color,
		'--motion-accent-color': accentColor ?? selected.accentColor,
		...style,
	} as CSSProperties

	return <Tag aria-label={text} className={className} style={{ display: 'inline-block', ...typography }}>
		{variant === 'stagger'
			? Array.from(text).map((character, index) => <span key={index} aria-hidden="true" style={unitStyle(index)}>
				{character === ' ' ? '\u00a0' : character}
			</span>)
			: <span style={unitStyle(0)}>{text}</span>}
	</Tag>
}