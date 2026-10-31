import { Composition } from 'remotion'
import {ResourceLibraryProof, RESOURCE_LIBRARY_FRAMES} from './resources/ResourceLibraryProof'
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
import {HeroCharacterStage, HERO_STAGE_DURATION, type HeroStageProps} from './characters/HeroCharacterStage'
import {V4FacialReviewStage, V4_FACIAL_REVIEW_FRAMES, type V4FacialReviewProps} from './characters/V4FacialReviewStage'
import {ChibiV4ReviewStage, CHIBI_V4_REVIEW_DURATION, type ChibiV4ReviewProps} from './characters/ChibiV4ReviewStage'
import {ImportedSpriteAnimation, type ImportedSpriteAnimationProps} from './characters/ImportedSpriteAnimation'
import {CanonicalFullBodyReviewStage, CANONICAL_FULL_BODY_REVIEW_FRAMES, type CanonicalFullBodyReviewProps} from './characters/CanonicalFullBodyReviewStage'
import {TrueFrameReviewStage, type TrueFrameReviewProps} from './characters/TrueFrameReviewStage'
import {PixelProductionProof,PIXEL_PROOF_FRAMES,type PixelProductionProofProps} from './characters/PixelProductionProof'
import episodeFixture from './episodes/episode-proof-v1.json'
import {compileEpisodeTimeline, type EpisodeManifestV1} from './episodes/episodeManifest'
import {EpisodeTimelineProof, calculateEpisodeTimelineMetadata, type EpisodeTimelineProofProps} from './episodes/EpisodeTimelineProof'
import {EpisodeProduction, calculateEpisodeProductionMetadata, type EpisodeProductionProps} from './episodes/EpisodeProduction'
import {AfterEffectsLottieProof, AFTER_EFFECTS_LOTTIE_FRAMES} from './after-effects/AfterEffectsLottieProof'
import {DuikBakedCharacterProof, DUIK_BAKED_PROOF_FRAMES} from './after-effects/DuikBakedCharacterProof'
import './fonts'
import {calculateEditMetadata, calculateHeroMetadata} from './compositionMetadata'

const spec = edit as EditSpec

export const Root = () => <>
  <Composition id="ResourceLibraryProof" component={ResourceLibraryProof}
    width={1920} height={1080} fps={30} durationInFrames={RESOURCE_LIBRARY_FRAMES} />
  <Composition id="DuikBakedCharacterProof" component={DuikBakedCharacterProof}
    width={1920} height={1080} fps={30} durationInFrames={DUIK_BAKED_PROOF_FRAMES} />
  <Composition id="AfterEffectsLottieProof" component={AfterEffectsLottieProof}
    width={1080} height={1920} fps={30} durationInFrames={AFTER_EFFECTS_LOTTIE_FRAMES} />
  <Composition id="EpisodeProduction" component={EpisodeProduction} width={1920} height={1080} fps={30}
    durationInFrames={120} calculateMetadata={calculateEpisodeProductionMetadata}
    defaultProps={{manifest: episodeFixture as EpisodeManifestV1, captions:{}} satisfies EpisodeProductionProps}/>
  <Composition id="PixelProductionProof" component={PixelProductionProof}
    width={1920} height={1080} fps={30} durationInFrames={PIXEL_PROOF_FRAMES}
    defaultProps={{assetsReady:true} satisfies PixelProductionProofProps} />
  <Composition id="TrueFrameReviewStage" component={TrueFrameReviewStage}
    width={1920} height={1080} fps={30} durationInFrames={240}
    defaultProps={{assetsReady:false,artApproved:false,urfavxbfAction:'point_camera',
      pixAction:'assist_point',hostFrames:8,pixFrames:8} satisfies TrueFrameReviewProps} />
  <Composition id="CanonicalFullBodyReviewStage" component={CanonicalFullBodyReviewStage}
    width={1920} height={1080} fps={30} durationInFrames={CANONICAL_FULL_BODY_REVIEW_FRAMES}
    defaultProps={{assetsReady:false,artApproved:false} satisfies CanonicalFullBodyReviewProps} />
  <Composition id="HeroCharacterStage" component={HeroCharacterStage} width={1920} height={1080} fps={30}
    durationInFrames={HERO_STAGE_DURATION}
    calculateMetadata={calculateHeroMetadata}
    defaultProps={{assetsReady:true,artApproved:true,voiceEvents:[],chapter:1} satisfies HeroStageProps} />
  <Composition id="EpisodeTimelineProof" component={EpisodeTimelineProof} width={1920} height={1080} fps={30}
    durationInFrames={compileEpisodeTimeline(episodeFixture).durationFrames}
    calculateMetadata={calculateEpisodeTimelineMetadata}
    defaultProps={{manifest: episodeFixture as EpisodeManifestV1} satisfies EpisodeTimelineProofProps} />
  <Composition id="V4FacialReviewStage" component={V4FacialReviewStage} width={1920} height={1080} fps={30}
    durationInFrames={V4_FACIAL_REVIEW_FRAMES}
    defaultProps={{assetsReady:false,artApproved:false} satisfies V4FacialReviewProps} />
  <Composition id="ChibiV4ReviewStage" component={ChibiV4ReviewStage} width={1920} height={1080} fps={30}
    durationInFrames={CHIBI_V4_REVIEW_DURATION}
    defaultProps={{assetsReady:false} satisfies ChibiV4ReviewProps} />
  <Composition id="ImportedSpriteAnimationReview" component={ImportedSpriteAnimation} width={1920} height={1080} fps={30}
    durationInFrames={240}
    defaultProps={{character:'urfavxbf',action:'idle_normal',durationsMs:[125],loop:true,assetsReady:false} satisfies ImportedSpriteAnimationProps} />
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
	<Composition id="ExampleEdit" component={Edit} width={FX_W} height={FX_H} fps={FX_FPS} durationInFrames={editDuration(spec)} calculateMetadata={calculateEditMetadata} defaultProps={{ spec }} />
</>
