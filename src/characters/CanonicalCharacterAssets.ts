import type {CharacterId, LayeredPuppetRig} from './CharacterPuppet';

/**
 * Canonical art target paths for new videos as of 2026-10-29.
 * The uploaded reference sheets are NOT transparent cutout sprites.
 * A separately authored, owner-approved production asset must be staged
 * at each path before rendering. No V2 art or rejected V4 draft fallback.
 */
export type CanonicalCharacterAsset = {
  assetPath: string;
  layeredRig?: LayeredPuppetRig;
};

export const CANONICAL_CHARACTER_ASSETS: Record<CharacterId, CanonicalCharacterAsset> = {
  urfavxbf: {assetPath: 'characters/canonical/urfavxbf/full-body.png'},
  pix: {assetPath: 'characters/canonical/pix/full-body.png'},
};

export const CANONICAL_CHARACTER_VERSION = 'urfavxbf-pix-2026-10-29' as const;

/** Guard new episodes until real RGBA art passes review; not source sheets. */
export const canonicalArtworkApproved = (assetsReady: boolean, artApproved: boolean) =>
  assetsReady && artApproved;
