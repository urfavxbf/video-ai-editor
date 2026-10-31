import { AbsoluteFill } from 'remotion'
import { brollOverlayFx } from './BrollOverlay'
import { chatTakeoverFx } from './ChatTakeover'
import { checklistFx } from './Checklist'
import { checklistPopFx } from './ChecklistPop'
import { checklistTallyFx } from './ChecklistTally'
import { digitalZoomFx } from './DigitalZoom'
import { frameBreakFx } from './FrameBreak'
import { frameEscapeFx } from './FrameEscape'
import { glassWidgetsFx } from './GlassWidgets'
import { greenScreenFx } from './GreenScreen'
import { growthCurveFx } from './GrowthCurve'
import { headlineStormFx } from './HeadlineStorm'
import { liquidGlassFx } from './LiquidGlass'
import { magazineCoverFx } from './MagazineCover'
import { orbitFx } from './Orbit'
import { paperCutoutFx } from './PaperCutout'
import { phoneMockupFx } from './PhoneMockup'
import { Sfx } from './sfx'
import { type FxEntry, type FxSource, FxSourceContext, useFxSource } from './shared'
import { snapZoomFx } from './SnapZoom'
import { splitFx } from './Split'
import { zoomPortalFx } from './ZoomPortal'
import { zoomThroughCutFx } from './ZoomThroughCut'
import { EDIT_EFFECT_IDS } from '../compositionMetadata'

export const FX_ALL: FxEntry[] = [
	orbitFx, chatTakeoverFx, frameEscapeFx, snapZoomFx, checklistPopFx, headlineStormFx, zoomPortalFx, growthCurveFx, brollOverlayFx,
	paperCutoutFx, magazineCoverFx, liquidGlassFx, zoomThroughCutFx, greenScreenFx, frameBreakFx, digitalZoomFx, phoneMockupFx, checklistTallyFx,
	glassWidgetsFx, checklistFx, splitFx,
]
export const fxById = (id: string) => FX_ALL.find(e => e.id === id)
if (FX_ALL.length !== EDIT_EFFECT_IDS.length || new Set(FX_ALL.map(e => e.id)).size !== FX_ALL.length ||
  EDIT_EFFECT_IDS.some(id => !fxById(id))) throw new Error('Edit contract and FX registry disagree')

export type FxPreviewProps = { id: string; from: number; source?: FxSource }

/** One effect on its own, with its sound cues. */
export const FxPreview = ({ id, from, source }: FxPreviewProps) => {
	const entry = fxById(id)
	const fallback = useFxSource()
	if (!entry) return <AbsoluteFill style={{ background: '#111' }} />
	return <FxSourceContext.Provider value={source ?? fallback}>
		<AbsoluteFill style={{ background: '#000' }}><entry.Component from={from} /><Sfx cues={entry.sfx ?? []} /></AbsoluteFill>
	</FxSourceContext.Provider>
}
