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
import {CharacterAnimationLab, type CharacterAnimationLabProps} from './characters/CharacterAnimationLab'
import {PixelPortraitHUD, type PixelPortraitHUDProps} from './characters/PixelPortraitHUD'
import {Y2038Teaser, type Y2038TeaserProps} from './episodes/Y2038Teaser'
import './fonts'
import {YouTubeJourneyStyleframes} from './episodes/YouTubeJourneyStyleframes'
import {YouTubeJourneyPreview, type YouTubeJourneyPreviewProps} from './episodes/YouTubeJourneyPreview'

const spec = edit as EditSpec

export const Root = () => <>
  <Composition id="YouTubeJourneyPreview" component={YouTubeJourneyPreview} width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{lines:[],voiceEvents:[],totalFrames:30,chapterBreakStart:0,chapterBreakEnd:0} satisfies YouTubeJourneyPreviewProps} calculateMetadata={({props})=>({durationInFrames:props.totalFrames})}/>
  <Composition id="YouTubeJourneyStyleframes" component={YouTubeJourneyStyleframes} width={1920} height={1080} fps={30} durationInFrames={270} />
  <Composition id="Y2038Teaser" component={Y2038Teaser} width={1920} height={1080} fps={30} durationInFrames={720}
    defaultProps={{assetsReady: false} satisfies Y2038TeaserProps} />
  <Composition id="PixelPortraitHUD" component={PixelPortraitHUD}
    width={1920} height={1080} fps={30} durationInFrames={240}
    defaultProps={{assetsReady: false} satisfies PixelPortraitHUDProps} />
  <Composition id="CharacterAnimationLab" component={CharacterAnimationLab}
    width={1920} height={1080} fps={30} durationInFrames={240}
    defaultProps={{assetsReady: false} satisfies CharacterAnimationLabProps} />
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
