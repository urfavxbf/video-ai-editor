/** Widescreen treatments of the existing FX IDs; original portrait components remain intact. */
export const SHOWREEL_FPS = 30;
export const INTRO_FRAMES = 150;
export const OUTRO_FRAMES = 150;
export const SHOT_DEFINITIONS = [
 ['chat-takeover','MAKE IT MOVE.',90,'ink'],
 ['snap-zoom','MAKE IT MATTER.',60,'acid'],
 ['headline-storm','IDEAS IN MOTION.',90,'paper'],
 ['checklist-pop','CUT. SHAPE. FEEL.',90,'ink'],
 ['digital-zoom','LOOK CLOSER.',60,'paper'],
 ['rgb-split','BREAK THE SIGNAL.',60,'ink'],
 ['speed-trails','KEEP UP.',60,'acid'],
 ['whip-pan-blur','CHANGE DIRECTION.',60,'violet'],
 ['svg-path-morph','NOTHING STAYS STILL.',60,'paper'],
 ['liquid-displacement','LET IT FLOW.',60,'cyan'],
 ['liquid-glass','A DIFFERENT LENS.',60,'ink'],
 ['shader-portal','ANOTHER DIMENSION.',60,'violet'],
 ['zoom-portal','COME THROUGH.',60,'ink'],
 ['zoom-through-cut','NEXT WORLD.',60,'acid'],
 ['green-screen','BUILD YOUR WORLD.',60,'cyan'],
 ['orbit','EVERYTHING CONNECTS.',60,'ink'],
 ['frame-escape','OUTSIDE THE FRAME.',60,'paper'],
 ['frame-break','BREAK THE RULES.',60,'acid'],
 ['paper-cutout','A LITTLE CHARACTER.',60,'paper'],
 ['comic-halftone','A LOT OF ATTITUDE.',60,'violet'],
 ['magazine-cover','YOUR STORY. BIGGER.',60,'paper'],
 ['broll-overlay','MORE THAN ONE VIEW.',60,'ink'],
 ['phone-mockup','MADE TO TRAVEL.',60,'cyan'],
 ['split','TWO WORLDS. ONE CUT.',60,'paper'],
 ['growth-curve','BUILDING BLOCKS.',60,'ink'],
 ['glass-widgets','A COMPLETE PALETTE.',60,'violet'],
 ['checklist','FROM IDEA TO IMPACT.',90,'paper'],
 ['film-light-leak','CHASE THE LIGHT.',60,'ink'],
 ['glass-shatter','LET IT BREAK.',60,'ink'],
 ['pixel-dissolve','BACK TO PIXELS.',60,'violet'],
 ['film-burn-reveal','MAKE SOMETHING NEW.',60,'ink'],
 ['audio-reactive-particles','FEEL EVERY BEAT.',90,'ink'],
 ['checklist-tally','EVERYTHING. TOGETHER.',90,'acid'],
] as const;
export type ShowreelEffectId = typeof SHOT_DEFINITIONS[number][0];
export const MATERIAL_EFFECT_IDS:readonly ShowreelEffectId[]=['rgb-split','speed-trails','whip-pan-blur','svg-path-morph','liquid-displacement','liquid-glass','shader-portal','zoom-portal','zoom-through-cut','film-light-leak','glass-shatter','pixel-dissolve','film-burn-reveal','audio-reactive-particles'];
export type ShowreelPalette = typeof SHOT_DEFINITIONS[number][3];
export type ShowreelShot = {id:ShowreelEffectId; title:string; frames:number; at:number; palette:ShowreelPalette; index:number};
let at = INTRO_FRAMES;
export const SHOWREEL_SHOTS:ShowreelShot[] = SHOT_DEFINITIONS.map(([id,title,frames,palette],index)=>{
 const shot={id,title,frames,palette,index,at};at+=frames;return shot;
});
export const SHOWREEL_FRAMES = at + OUTRO_FRAMES;
export const HOST_POSES=['front','three-quarter','side','back','waving','pointing','explaining','thumbs-up','surprised'] as const;
export const PIX_POSES=['idle','curious','talk','point','happy','question','surprised'] as const;
export const SHOWREEL_FACTS={effects:SHOT_DEFINITIONS.length,characters:2,poses:HOST_POSES.length+PIX_POSES.length,voices:2} as const;
export function shotPose(character:'urfavxbf'|'pix',index:number):string {
 const poses=character==='pix'?PIX_POSES:HOST_POSES;
 return poses[((index%poses.length)+poses.length)%poses.length];
}
export function assertShowreelEffect(id:string):ShowreelEffectId {
 if(!SHOT_DEFINITIONS.some(s=>s[0]===id))throw new Error('Unknown showreel effect: '+id);
 return id as ShowreelEffectId;
}

/** Hold the director's selected expression for 1.2 seconds, including over speech. */
export function performancePose(character:'urfavxbf'|'pix',index:number,localFrame:number,speaking:boolean):string {
 return speaking&&localFrame>=36?(character==='pix'?'talk':'explaining'):shotPose(character,index);
}
