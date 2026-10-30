export type MotionVariant = 'fade' | 'slide' | 'scale' | 'bounce' | 'masked-reveal' | 'stagger'
export type MotionEasing = 'linear' | 'ease-out' | 'ease-in-out' | 'overshoot'
export type MotionDirection = 'left' | 'right' | 'up' | 'down'
export type ExitVariant = Exclude<MotionVariant, 'stagger'>

export type MotionPreset = {
	variant: MotionVariant
	staggerVariant: Exclude<MotionVariant, 'stagger'>
	durationInFrames: number
	easing: MotionEasing
	direction: MotionDirection
	distance: number
	fromScale: number
	staggerInFrames: number
	color: string
	accentColor: string
	fontFamily: string
	fontSize: number
	fontWeight: number
	lineHeight: number
	letterSpacing: number
}

export const MOTION_PRESETS = {
	signalFade: {
		variant: 'fade', staggerVariant: 'fade', durationInFrames: 20, easing: 'ease-out', direction: 'up',
		distance: 32, fromScale: 0.92, staggerInFrames: 3, color: '#F3F4EF', accentColor: '#B9F36A',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
	cleanSlide: {
		variant: 'slide', staggerVariant: 'slide', durationInFrames: 24, easing: 'ease-out', direction: 'left',
		distance: 92, fromScale: 0.9, staggerInFrames: 3, color: '#F3F4EF', accentColor: '#73D4D0',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
	softScale: {
		variant: 'scale', staggerVariant: 'scale', durationInFrames: 22, easing: 'ease-out', direction: 'up',
		distance: 36, fromScale: 0.72, staggerInFrames: 3, color: '#F3F4EF', accentColor: '#F2A67A',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
	impactBounce: {
		variant: 'bounce', staggerVariant: 'bounce', durationInFrames: 28, easing: 'overshoot', direction: 'up',
		distance: 24, fromScale: 0.58, staggerInFrames: 3, color: '#F3F4EF', accentColor: '#F1CB67',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
	windowReveal: {
		variant: 'masked-reveal', staggerVariant: 'masked-reveal', durationInFrames: 26, easing: 'ease-in-out', direction: 'left',
		distance: 0, fromScale: 1, staggerInFrames: 3, color: '#F3F4EF', accentColor: '#D995C6',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
	wordCascade: {
		variant: 'stagger', staggerVariant: 'slide', durationInFrames: 20, easing: 'ease-out', direction: 'up',
		distance: 30, fromScale: 0.94, staggerInFrames: 4, color: '#F3F4EF', accentColor: '#82B7ED',
		fontFamily: "'Montserrat', sans-serif", fontSize: 64, fontWeight: 800, lineHeight: 1.1, letterSpacing: 0,
	},
} as const satisfies Record<string, MotionPreset>

export type MotionPresetName = keyof typeof MOTION_PRESETS

export type MotionOptions = Pick<MotionPreset,
	'variant' | 'durationInFrames' | 'easing' | 'direction' | 'distance' | 'fromScale'> & {
	fromFrame?: number
	exitAtFrame?: number
	exitDurationInFrames?: number
	exitVariant?: ExitVariant
	reducedMotion?: boolean
}

export type MotionState = {
	opacity: number
	translateX: number
	translateY: number
	scale: number
	clipInsetRight: number
}

const clamp01 = (value: number) => Math.min(1, Math.max(0, value))

const validateDuration = (value: number, name: string) => {
	if (!Number.isSafeInteger(value) || value < 1) {
		throw new RangeError(`${name} must be a positive safe integer`)
	}
}

const validateFrame = (value: number, name: string) => {
	if (!Number.isSafeInteger(value) || value < 0) {
		throw new RangeError(`${name} must be a non-negative safe integer`)
	}
}

const easedProgress = (progress: number, easing: MotionEasing) => {
	const t = clamp01(progress)
	switch (easing) {
		case 'linear': return t
		case 'ease-out': return 1 - (1 - t) ** 3
		case 'ease-in-out': return t * t * (3 - 2 * t)
		case 'overshoot': return 1 + Math.sin(t * Math.PI) * Math.exp(-5 * t) * (1 - t)
	}
}

const directionOffset = (direction: MotionDirection, distance: number) => ({
	translateX: distance === 0 ? 0 : direction === 'left' ? -distance : direction === 'right' ? distance : 0,
	translateY: distance === 0 ? 0 : direction === 'up' ? -distance : direction === 'down' ? distance : 0,
})

const enterState = (progress: number, options: MotionOptions): MotionState => {
	const eased = easedProgress(progress, options.easing)
	const visibleProgress = clamp01(progress)
	const state: MotionState = { opacity: visibleProgress, translateX: 0, translateY: 0, scale: 1, clipInsetRight: 0 }

	switch (options.variant) {
		case 'fade':
			break
		case 'slide': {
			const offset = directionOffset(options.direction, options.distance * (1 - eased))
			state.translateX = offset.translateX
			state.translateY = offset.translateY
			break
		}
		case 'scale':
			state.scale = options.fromScale + (1 - options.fromScale) * eased
			break
		case 'bounce':
			state.scale = options.fromScale + (1 - options.fromScale) * eased
			break
		case 'masked-reveal':
			state.opacity = 1
			state.clipInsetRight = (1 - eased) * 100
			break
		case 'stagger':
			throw new Error('Use a concrete staggerVariant for individual text units')
	}

	return state
}

export const resolveMotionState = (frame: number, options: MotionOptions): MotionState => {
	validateFrame(frame, 'frame')
	validateFrame(options.fromFrame ?? 0, 'fromFrame')
	validateDuration(options.durationInFrames, 'durationInFrames')
	if (!Number.isFinite(options.distance) || options.distance < 0) {
		throw new RangeError('distance must be a non-negative finite number')
	}
	if (!Number.isFinite(options.fromScale) || options.fromScale < 0) {
		throw new RangeError('fromScale must be a non-negative finite number')
	}
	if (options.exitAtFrame !== undefined) {
		validateFrame(options.exitAtFrame, 'exitAtFrame')
		validateDuration(options.exitDurationInFrames ?? options.durationInFrames, 'exitDurationInFrames')
	}

	const fromFrame = options.fromFrame ?? 0
	const exitDuration = options.exitDurationInFrames ?? options.durationInFrames
	if (options.reducedMotion) {
		const beforeEntrance = frame < fromFrame
		const afterExit = options.exitAtFrame !== undefined && frame >= options.exitAtFrame + exitDuration
		return { opacity: beforeEntrance || afterExit ? 0 : 1, translateX: 0, translateY: 0, scale: 1, clipInsetRight: 0 }
	}

	const progress = clamp01((frame - fromFrame) / options.durationInFrames)
	const state = enterState(progress, options)
	if (options.exitAtFrame === undefined || frame < options.exitAtFrame) return state

	const exitProgress = easedProgress((frame - options.exitAtFrame) / exitDuration, options.easing)
	const exitVariant = options.exitVariant ?? 'fade'
	if (exitVariant === 'fade') state.opacity *= 1 - clamp01(exitProgress)
	if (exitVariant === 'slide') {
		const offset = directionOffset(options.direction, options.distance * exitProgress)
		state.translateX += offset.translateX
		state.translateY += offset.translateY
	}
	if (exitVariant === 'scale' || exitVariant === 'bounce') state.scale *= 1 - 0.8 * clamp01(exitProgress)
	if (exitVariant === 'masked-reveal') state.clipInsetRight = Math.max(state.clipInsetRight, clamp01(exitProgress) * 100)
	return state
}