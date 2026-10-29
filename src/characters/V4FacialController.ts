import type {CharacterId, ReactionCue, VoiceEvent} from './CharacterPuppet';

/**
 * V4-only facial controller. Old V2 PixelGlitch sprites are NEVER loaded.
 * A voice RMS envelope controls generic mouth OPENNESS, not phoneme identity.
 * Real phoneme accuracy is only possible when explicit timed mouth cues exist.
 */
export type V4Expression =
  'neutral'|'happy'|'curious'|'excited'|'surprised'|'thinking'|
  'focused'|'sleepy'|'glitch'|'blink';
export type V4Mouth =
  'rest'|'small'|'medium'|'wide'|'round'|'closed'|'fv';

export type V4ExpressionCue={
  atFrame:number;
  durationFrames:number;
  expression:V4Expression;
};
export type V4MouthCue={
  atFrame:number;
  durationFrames:number;
  shape:V4Mouth;
  provenance:'authored-phoneme-alignment'|'manual';
};
export type V4FacialState={
  expression:V4Expression;
  mouth:V4Mouth;
  speaking:boolean;
  voiceEnergy:number;
  alignment:'explicit-mouth-cue'|'audio-energy-proxy'|'no-lipsync';
  blink:boolean;
};
const within=(frame:number,start:number,end:number)=>
  Number.isFinite(start)&&Number.isFinite(end)&&frame>=start&&frame<end;
const bound=(x:number)=>Math.min(1,Math.max(0,Number.isFinite(x)?x:0));

export const activeV4Voice=(id:CharacterId,frame:number,events:VoiceEvent[]=[]) =>
  events.find((e)=>e.speaker===id&&within(frame,e.startFrame,e.endFrame));

/** Sample only a real, supplied RMS envelope. Missing data is silence/unknown. */
export const v4VoiceEnergy=(frame:number,fps:number,event?:VoiceEvent):number=>{
  if(!event||!event.rms?.length||!Number.isFinite(fps)||fps<=0)return 0;
  const rate=event.samplesPerSecond??10;
  if(!Number.isFinite(rate)||rate<=0)return 0;
  const position=Math.max(0,(frame-event.startFrame)*rate/fps);
  const i=Math.min(event.rms.length-1,Math.floor(position));
  const fraction=Math.max(0,Math.min(1,position-i));
  return bound((event.rms[i]??0)*(1-fraction)+(event.rms[Math.min(i+1,event.rms.length-1)]??0)*fraction);
};

const genericMouth=(energy:number):V4Mouth=>
  energy>=.75?'wide':energy>=.46?'medium':energy>=.18?'small':'rest';

/** Short controlled blink, offset per character; no random/flickering pixels. */
export const v4BlinkAt=(id:CharacterId,frame:number):boolean=>{
  const period=id==='pix'?139:167;
  const offset=id==='pix'?48:83;
  const phase=((Math.floor(frame)-offset)%period+period)%period;
  return frame>=offset&&phase<3;
};

export const v4FaceAt=({
  id,frame,fps,voiceEvents=[],reactionCues=[],expressionCues=[],mouthCues=[],
}:{
  id:CharacterId;
  frame:number;
  fps:number;
  voiceEvents?:VoiceEvent[];
  reactionCues?:ReactionCue[];
  expressionCues?:V4ExpressionCue[];
  mouthCues?:V4MouthCue[];
}):V4FacialState=>{
  const voice=activeV4Voice(id,frame,voiceEvents);
  const speaking=Boolean(voice);
  const energy=v4VoiceEnergy(frame,fps,voice);
  const expressionCue=expressionCues.find((c)=>within(frame,c.atFrame,c.atFrame+c.durationFrames));
  const reaction=reactionCues.find((c)=>within(frame,c.atFrame,c.atFrame+c.durationFrames));
  const expressionFromReaction:Record<ReactionCue['kind'],V4Expression>={
    curious:'curious',excited:'excited',surprised:'surprised',agree:'happy',
  };
  let expression:V4Expression=expressionCue?.expression??
    (reaction?expressionFromReaction[reaction.kind]:speaking?'focused':'neutral');
  const blink=expression==='neutral'&&v4BlinkAt(id,frame);
  if(blink)expression='blink';
  // Mouth cue is used ONLY during this character's own voice event.
  const cue=speaking?mouthCues.find((c)=>within(frame,c.atFrame,c.atFrame+c.durationFrames)):undefined;
  const hasEnvelope=speaking&&Boolean(voice?.rms?.length)&&Number.isFinite(voice?.samplesPerSecond??10);
  const mouth=cue?.shape??(hasEnvelope?genericMouth(energy):'rest');
  return {expression,mouth,speaking,voiceEnergy:energy,
    alignment:cue?'explicit-mouth-cue':hasEnvelope?'audio-energy-proxy':'no-lipsync',blink};
};
