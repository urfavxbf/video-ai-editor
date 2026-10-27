import { Composition } from 'remotion'
import { Edit, type EditSpec, editDuration } from './edit/Edit'
import edit from './edit/edit.json'
import { fxById, FxPreview, type FxPreviewProps } from './fx/index'
import { FxShowcase, showcaseDuration } from './fx/FxShowcase'
import { FX_FPS, FX_H, FX_W } from './fx/shared'
import { DudutPremium, DUDUT_DURATION, type DudutPremiumProps } from './podcast/DudutPremium'
import { DudutV2, DUDUT_V2_DURATION, type DudutV2Props } from './podcast/DudutV2'
import { DoorwayEffect, type DoorwayProps } from './original/DoorwayEffect'
import { OfficialFeaturesDemo, OFFICIAL_FEATURE_DEMO_FRAMES } from './features/OfficialFeaturesDemo'
import { RepoShowcase, REPO_SHOWCASE_FRAMES } from './showcase/RepoShowcase'
import { ChallengerDeep, type ChallengerProps } from './original/ChallengerDeep'
import { Motion30, MOTION30_FRAMES } from './showcase/Motion30'
import './fonts'

const spec = edit as EditSpec

export const Root = () => <>
  <Composition id="Motion30" component={Motion30} width={1080} height={1920} fps={30} durationInFrames={MOTION30_FRAMES} defaultProps={{includeNarration:false,includeMusic:false}} />
  <Composition id="ChallengerDeep" component={ChallengerDeep} width={1080} height={1920} fps={30} durationInFrames={2400}
    defaultProps={{totalFrames:1350,captions:[],narrationAvailable:false} satisfies ChallengerProps} />
  <Composition id="RepoShowcase" component={RepoShowcase} width={1080} height={1920} fps={30} durationInFrames={REPO_SHOWCASE_FRAMES} />
	<Composition id="OfficialFeaturesDemo" component={OfficialFeaturesDemo} width={1080} height={1920} fps={30} durationInFrames={OFFICIAL_FEATURE_DEMO_FRAMES} />
	<Composition id="OriginalDoorway" component={DoorwayEffect} width={1080} height={1920} fps={30} durationInFrames={2400}
    defaultProps={{totalFrames:1230,captions:[],narrationAvailable:false} satisfies DoorwayProps} />
  <Composition id="FxShowcase" component={FxShowcase} width={FX_W} height={FX_H} fps={FX_FPS} durationInFrames={showcaseDuration()} />
	<Composition id="FxPreview" component={FxPreview} width={FX_W} height={FX_H} fps={FX_FPS} durationInFrames={90}
		defaultProps={{ id: 'orbit', from: 0 } satisfies FxPreviewProps}
		calculateMetadata={({ props }) => ({ durationInFrames: fxById(props.id)?.duration ?? 90 })} />
	<Composition id="DudutV2" component={DudutV2} width={1080} height={1920} fps={30} durationInFrames={DUDUT_V2_DURATION} defaultProps={{ videoPath: 'takes/dudut/clip.mp4', sourceStartSeconds: 42 } satisfies DudutV2Props} />
	<Composition id="DudutPremium" component={DudutPremium} width={1080} height={1920} fps={30} durationInFrames={DUDUT_DURATION} defaultProps={{ videoPath: 'takes/dudut/clip.mp4', sourceStartSeconds: 42 } satisfies DudutPremiumProps} />
	<Composition id="ExampleEdit" component={Edit} width={FX_W} height={FX_H} fps={FX_FPS} durationInFrames={editDuration(spec)} defaultProps={{ spec }} />
</>
