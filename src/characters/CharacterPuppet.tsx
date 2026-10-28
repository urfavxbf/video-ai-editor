import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

/**
 * Frame-deterministic 2.5D puppet. Single PNGs move as one piece; independent
 * facial and body actions need real transparent full-canvas rig layers.
 * This is NOT volumetric 3D or phoneme-accurate lip-sync.
 */
export type CharacterId = 'urfavxbf' | 'pix';
export type CharacterReaction = 'curious' | 'excited' | 'surprised' | 'agree';
/** Full-body performance intent. Real per-limb movement requires separate aligned rig PNGs. */
export type BodyGesture = 'idle' | 'explain' | 'point' | 'celebrate' | 'walk';

export type VoiceEvent = {
  speaker: CharacterId;
  startFrame: number;
  endFrame: number; // exclusive
  rms?: number[]; // real WAV RMS envelope, normalized 0..1
  samplesPerSecond?: number; // default 10
};

export type ReactionCue = {
  atFrame: number;
  durationFrames: number;
  kind: CharacterReaction;
};

/** Layer files must have identical original PNG dimensions and transparent backgrounds. */
export type LayeredPuppetRig = {
  /** Torso-only image, NOT a duplicate already containing the articulated limbs. */
  body: string;
  head: string;
  leftArm?: string;
  rightArm?: string;
  leftLeg?: string;
  rightLeg?: string;
  tail?: string;
  leftArmPivotPercent?: [number, number];
  rightArmPivotPercent?: [number, number];
  leftLegPivotPercent?: [number, number];
  rightLegPivotPercent?: [number, number];
  mouthClosed?: string;
  mouthOpen?: string;
  headPivotPercent?: [number, number];
  tailPivotPercent?: [number, number];
};

export type CharacterPuppetProps = {
  id: CharacterId;
  /** staticFile-relative path after staging canonical assets; never a remote image URL. */
  assetPath: string;
  width: number;
  height: number;
  left?: number;
  right?: number;
  bottom?: number;
  voiceEvents?: VoiceEvent[];
  reactions?: ReactionCue[];
  layeredRig?: LayeredPuppetRig;
  bodyGesture?: BodyGesture;
  fadeInFrames?: number;
  /** Set true only for deliberately mirrored screen blocking. */
  mirror?: boolean;
};

const clamp = (value: number, min = 0, max = 1) => Math.min(max, Math.max(min, value));

export const findVoiceEvent = (id: CharacterId, frame: number, events: VoiceEvent[] = []): VoiceEvent | undefined =>
  events.find((event) =>
    event.speaker === id &&
    Number.isFinite(event.startFrame) &&
    Number.isFinite(event.endFrame) &&
    frame >= event.startFrame &&
    frame < event.endFrame
  );

/** No invented spoken energy when WAV samples are unavailable. */
export const voiceEnergyAtFrame = (frame: number, fps: number, event?: VoiceEvent): number => {
  if (!event || !event.rms?.length || fps <= 0) return 0;
  const rate = event.samplesPerSecond ?? 10;
  if (!Number.isFinite(rate) || rate <= 0) return 0;
  const sample = Math.floor(((frame - event.startFrame) * rate) / fps);
  return clamp(event.rms[Math.max(0, Math.min(event.rms.length - 1, sample))] ?? 0);
};

export const reactionAtFrame = (frame: number, cues: ReactionCue[] = []): ReactionCue | undefined =>
  cues.find((cue) => cue.atFrame <= frame && frame < cue.atFrame + cue.durationFrames);

export const getPuppetPose = (
  id: CharacterId,
  frame: number,
  fps: number,
  event?: VoiceEvent,
  reaction?: ReactionCue,
  gesture: BodyGesture = 'idle',
) => {
  const speaking = Boolean(event);
  const energy = voiceEnergyAtFrame(frame, fps, event);
  const t = frame / Math.max(1, fps);
  const cat = id === 'pix';
  // Breathing and slow head-listening rhythm should not resemble constant dancing.
  const breath = Math.sin(t * 2.3 + (cat ? 1.0 : 0.3));
  const y = breath * (cat ? 3.0 : 1.8) + (speaking ? -5 * energy : 0);
  const baseRoll = Math.sin(t * 1.3 + (cat ? 0.6 : 0)) * 0.7;
  const curious = reaction?.kind === 'curious';
  const excited = reaction?.kind === 'excited';
  const surprised = reaction?.kind === 'surprised';
  const agree = reaction?.kind === 'agree';
  const reactionRoll = curious ? (cat ? -5 : 3) : surprised ? (cat ? 5 : -3) : agree ? 3 : 0;
  const reactionBounce = excited ? -9 * Math.abs(Math.sin(t * 13)) : surprised ? -10 : 0;
  const roll = baseRoll + reactionRoll + (speaking ? Math.sin(t * 8) * energy * (cat ? 2.0 : 0.9) : 0);
  const yaw = (cat ? -3 : 3) + Math.sin(t * 0.8) * 2.2 + (speaking ? energy * (cat ? 4 : -3) : 0);
  const headRoll = (speaking ? Math.sin(t * 9) * 3.5 * energy : 0) + (curious ? -6 : 0);
  const tailRoll = Math.sin(t * (speaking ? 6 : 2.7)) * (speaking ? 7 : 4) + (excited ? 11 : 0);
  // Deliberate gesture changes, not a repeating full-body dance while listening.
  const activeVoice = speaking && energy > 0.12;
  const cadence = t * (cat ? 7.8 : 6.3);
  const walking = gesture === 'walk';
  const celebrating = gesture === 'celebrate' || excited;
  const explaining = gesture === 'explain' && activeVoice;
  const pointing = gesture === 'point';
  const stride = walking ? Math.sin(cadence) * 12 : 0;
  const handBeat = activeVoice ? Math.sin(cadence * 1.12) * (4 + 15 * energy) : 0;
  const leftArmRoll = (celebrating ? -36 : pointing ? -8 : explaining ? -16 : -2) - handBeat;
  const rightArmRoll = (celebrating ? 39 : pointing ? 42 : explaining ? 14 : 2) + handBeat * 0.9;
  const leftLegRoll = stride + (celebrating ? Math.sin(cadence)*6 : 0);
  const rightLegRoll = -stride + (celebrating ? Math.sin(cadence+1.5)*6 : 0);
  const stepLift = walking ? Math.abs(Math.sin(cadence)) * 6 : 0;
  const torsoRoll = (walking ? Math.sin(cadence)*1.1 : 0) + (explaining ? handBeat*0.06 : 0);
  // A single full-body image can LEAN or SHIFT as a unit; it cannot actually point an arm.
  // The separate limb layer path below uses the same cue for true joint rotation.
  const x = walking ? Math.sin(cadence)*7
    : pointing ? (cat ? -8 : 8)
    : explaining ? Math.sin(cadence*0.5)*3 : 0;
  const bodyLean = pointing ? (cat ? -4 : 5)
    : explaining ? Math.sin(cadence*0.65)*1.8
    : celebrating ? Math.sin(cadence*0.7)*2.8 : 0;
  const scale = 1 + Math.max(0, breath) * 0.004 + (celebrating ? 0.015 : 0);
  return {speaking, energy, x, y: y + reactionBounce - stepLift,
    roll: roll + torsoRoll + bodyLean, yaw, headRoll: headRoll + (explaining ? handBeat * 0.12 : 0),
    tailRoll, scale, leftArmRoll, rightArmRoll, leftLegRoll, rightLegRoll};
};

const FullCanvasLayer: React.FC<{
  src: string;
  transform?: string;
  origin?: string;
  crisp?: boolean;
}> = ({src, transform, origin, crisp}) => (
  <Img
    src={staticFile(src)}
    style={{
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      objectFit: 'contain',
      transform,
      transformOrigin: origin ?? '50% 50%',
      imageRendering: crisp ? 'pixelated' : 'auto',
    }}
  />
);

export const CharacterPuppet: React.FC<CharacterPuppetProps> = ({
  id,
  assetPath,
  width,
  height,
  left,
  right,
  bottom = 0,
  voiceEvents = [],
  reactions = [],
  layeredRig,
  bodyGesture = 'idle',
  fadeInFrames = 10,
  mirror = false,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const event = findVoiceEvent(id, frame, voiceEvents);
  const reaction = reactionAtFrame(frame, reactions);
  const pose = getPuppetPose(id, frame, fps, event, reaction, bodyGesture);
  const activeCue = reaction && reaction.durationFrames > 0
    ? Math.min(1, (frame - reaction.atFrame) / Math.max(1, Math.min(8, reaction.durationFrames)))
    : 1;
  const pop = 0.92 + 0.08 * clamp(frame / Math.max(1, fadeInFrames));
  const fade = clamp(frame / Math.max(1, fadeInFrames));
  const outer = [
    `translate3d(${pose.x.toFixed(2)}px, ${pose.y.toFixed(2)}px, 0)`,
    `rotateY(${pose.yaw.toFixed(2)}deg)`,
    `rotateZ(${(pose.roll * activeCue).toFixed(2)}deg)`,
    `scale(${(pose.scale * pop).toFixed(4)})`,
    mirror ? 'scaleX(-1)' : '',
  ].filter(Boolean).join(' ');

  const crisp = id === 'urfavxbf';
  const headPivot = layeredRig?.headPivotPercent ?? (id === 'pix' ? [51, 48] : [51, 22]);
  const tailPivot = layeredRig?.tailPivotPercent ?? [39, 77];
  const armPivots = {
    left: layeredRig?.leftArmPivotPercent ?? [33, 38],
    right: layeredRig?.rightArmPivotPercent ?? [68, 38],
  };
  const legPivots = {
    left: layeredRig?.leftLegPivotPercent ?? [43, 69],
    right: layeredRig?.rightLegPivotPercent ?? [57, 69],
  };
  // Energy can ONLY switch an open/closed mouth with actual provided mouth layer assets.
  // This is approximate mouth flapping, not phoneme-to-viseme alignment.
  const hasMouthLayers = Boolean(layeredRig?.mouthClosed && layeredRig?.mouthOpen);
  const mouthIsOpen = hasMouthLayers && Boolean(event?.rms?.length) && pose.energy >= 0.22;

  return (
    <div
      data-character={id}
      data-speaker-active={pose.speaking ? 'true' : 'false'}
      data-layout="full-body"
      data-rig-mode={layeredRig ? 'articulated-layers' : 'single-sprite'}
      data-body-gesture={bodyGesture}
      style={{
        position: 'absolute', left, right, bottom, width, height,
        transformStyle: 'preserve-3d', perspective: 1200, pointerEvents: 'none', opacity: fade,
      }}
    >
      <div style={{
        position: 'absolute', left: '14%', bottom: 0, width: '72%', height: 25,
        background: id === 'pix' ? 'rgba(0,207,250,0.21)' : 'rgba(255,192,0,0.18)',
        borderRadius: '50%', filter: 'blur(14px)',
        transform: `scale(${Math.max(0.7, 1 - Math.abs(pose.y) / 120)})`,
      }}/>
      <div style={{
        position: 'absolute', inset: 0, transform: outer,
        transformStyle: 'preserve-3d', transformOrigin: '50% 85%',
        filter: id === 'pix' ? 'drop-shadow(0 0 13px rgba(0,210,235,0.16))' : 'drop-shadow(0 0 12px rgba(255,190,0,0.10))',
      }}>
        {!layeredRig ? (
          <FullCanvasLayer src={assetPath} crisp={crisp}/>
        ) : (
          <>
            {layeredRig.tail && (
              <FullCanvasLayer
                src={layeredRig.tail}
                crisp={crisp}
                origin={`${tailPivot[0]}% ${tailPivot[1]}%`}
                transform={`rotate(${pose.tailRoll.toFixed(2)}deg)`}
              />
            )}
            {layeredRig.leftLeg && (
              <FullCanvasLayer src={layeredRig.leftLeg} crisp={crisp}
                origin={`${legPivots.left[0]}% ${legPivots.left[1]}%`}
                transform={`rotate(${pose.leftLegRoll.toFixed(2)}deg)`}/>
            )}
            {layeredRig.rightLeg && (
              <FullCanvasLayer src={layeredRig.rightLeg} crisp={crisp}
                origin={`${legPivots.right[0]}% ${legPivots.right[1]}%`}
                transform={`rotate(${pose.rightLegRoll.toFixed(2)}deg)`}/>
            )}
            <FullCanvasLayer src={layeredRig.body} crisp={crisp}/>
            {layeredRig.leftArm && (
              <FullCanvasLayer src={layeredRig.leftArm} crisp={crisp}
                origin={`${armPivots.left[0]}% ${armPivots.left[1]}%`}
                transform={`rotate(${pose.leftArmRoll.toFixed(2)}deg)`}/>
            )}
            {layeredRig.rightArm && (
              <FullCanvasLayer src={layeredRig.rightArm} crisp={crisp}
                origin={`${armPivots.right[0]}% ${armPivots.right[1]}%`}
                transform={`rotate(${pose.rightArmRoll.toFixed(2)}deg)`}/>
            )}
            <FullCanvasLayer
              src={layeredRig.head}
              crisp={crisp}
              origin={`${headPivot[0]}% ${headPivot[1]}%`}
              transform={`rotate(${pose.headRoll.toFixed(2)}deg)`}
            />
            {hasMouthLayers && (
              <FullCanvasLayer src={mouthIsOpen ? layeredRig.mouthOpen! : layeredRig.mouthClosed!} crisp={crisp}/>
            )}
          </>
        )}
      </div>
    </div>
  );
};
