import type {CharacterId, LayeredPuppetRig} from './CharacterPuppet';
import {HERO_IDENTITY} from './HeroPerformance';

/**
 * V2 hand-cut source-art rig paths. Build via:
 * python scripts/rig_official_v2_characters.py --urfavxbf ... --pix ...
 * The image binaries are gitignored and must pass character asset validation.
 * PIX only has two separately visible front paws + tail in the source drawing;
 * do not invent nonexistent hind-leg layers.
 */
const part = (character:CharacterId, name:string) =>
  `characters/pixel-glitch/${character}/rig/${name}.png`;

export const OFFICIAL_V2_RIGS: Record<CharacterId, {assetPath:string;layeredRig:LayeredPuppetRig}> = {
  urfavxbf:{
    assetPath:HERO_IDENTITY.urfavxbf.assetPath,
    layeredRig:{
      underlay:part('urfavxbf','underlay'),
      body:part('urfavxbf','body'),
      head:part('urfavxbf','head'),
      leftArm:part('urfavxbf','leftArm'),
      rightArm:part('urfavxbf','rightArm'),
      leftLeg:part('urfavxbf','leftLeg'),
      rightLeg:part('urfavxbf','rightLeg'),
      headPivotPercent:[54,43],
      leftArmPivotPercent:[37,47],
      rightArmPivotPercent:[72,48],
      leftLegPivotPercent:[41,73],
      rightLegPivotPercent:[63,73],
    },
  },
  pix:{
    assetPath:HERO_IDENTITY.pix.assetPath,
    layeredRig:{
      underlay:part('pix','underlay'),
      body:part('pix','body'),
      head:part('pix','head'),
      leftArm:part('pix','leftArm'),
      rightArm:part('pix','rightArm'),
      tail:part('pix','tail'),
      headPivotPercent:[44,69],
      leftArmPivotPercent:[31,74],
      rightArmPivotPercent:[50,75],
      tailPivotPercent:[66,71],
    },
  },
};
