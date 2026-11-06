import type {CharacterId, LayeredPuppetRig} from './CharacterPuppet';
/** The selected 2026-11-06 pixel pose defaults. Never fall back to rejected art. */
export type CanonicalCharacterAsset={assetPath:string; layeredRig?:LayeredPuppetRig};
export const CANONICAL_CHARACTER_ASSETS:Record<CharacterId,CanonicalCharacterAsset>={
  urfavxbf:{assetPath:'characters/urfavxbf-8bit/owner-sheet.jpg'},
  pix:{assetPath:'characters/pixel-default/pix/idle.png'},
};
export const CANONICAL_CHARACTER_VERSION='pixel-pose-default-2026-11-06' as const;
export const canonicalArtworkApproved=(assetsReady:boolean,artApproved:boolean)=>assetsReady&&artApproved;
