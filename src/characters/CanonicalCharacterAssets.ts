import type {CharacterId, LayeredPuppetRig} from './CharacterPuppet';
export type CanonicalCharacterAsset={assetPath:string; layeredRig?:LayeredPuppetRig};
/** Active 8-bit host; original PNG host art retained for archival verification. */
export const CANONICAL_CHARACTER_ASSETS:Record<CharacterId,CanonicalCharacterAsset>={
  urfavxbf:{assetPath:'characters/8bit-host/urfavxbf/idle/frame-00.svg'},
  pix:{assetPath:'characters/pixel-default/pix/idle.png'},
};
export const CANONICAL_CHARACTER_VERSION='original-8bit-svg-action-frames-2026-11-02' as const;
export const canonicalArtworkApproved=(assetsReady:boolean,artApproved:boolean)=>assetsReady&&artApproved;
