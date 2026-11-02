// Deterministic original 8-bit sprite generator. Run: node scripts/generate_8bit_host_sprites.mjs
import {mkdirSync,writeFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
const ROOT=resolve(process.env.SPRITE_OUTPUT_ROOT??resolve(import.meta.dirname,'..'));

const counts={"idle":6,"talk":8,"point_camera":8,"point_object":8,"explain":8,"walk":12,"run":10,"jump":8,"laugh":8,"think":6,"surprised":6,"confused":6,"wave":8,"celebrate":8,"listen":6};
const rect=(x,y,w,h,fill)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}"/>`;
const path=(d,fill)=>`<path d="${d}" fill="${fill}"/>`;
const round=n=>Math.round(n*10)/10;
function limb(x,y,ex,ey,thick,inside){
const coord=`M${round(x)} ${round(y)}L${round(ex)} ${round(ey)}`;
return `<path d="${coord}" fill="none" stroke="#10172e" stroke-width="${thick}" stroke-linecap="square"/><path d="${coord}" fill="none" stroke="${inside}" stroke-width="${thick-4}" stroke-linecap="square"/>`;
}
function spriteSvg(action,index,count){
const tau=Math.PI*2, phase=tau*index/count, sine=Math.sin(phase), wave=Math.sin(phase*2);
const moving=action==="walk"||action==="run";
const offset=moving?round(sine*(action==="run"?5:3)):0;
const jumping=action==="jump"||action==="celebrate";
const lift=jumping?round(-6*Math.max(0,Math.sin(Math.PI*index/Math.max(1,count-1)))):0;
const bob=moving?Math.round(Math.abs(sine)*1.5):action==="idle"||action==="listen"?Math.round(Math.sin(phase)*0.8):0;
let left=0.15,right=0.15,expression="smile",talking=false;
if(action==="talk"){left=0.40+0.16*sine;right=0.65+0.18*wave;talking=index%3!==0;}
if(action==="point_camera"){right=1.15+0.12*sine;left=0.12;talking=true;}
if(action==="point_object"){right=1.52;left=0.08;talking=true;}
if(action==="explain"){left=0.7+0.15*sine;right=0.85+0.12*wave;talking=index%2===0;}
if(action==="walk"){left=0.3+0.35*sine;right=0.3-0.28*sine;}
if(action==="run"){left=0.45+0.5*sine;right=0.6-0.48*sine;talking=false;}
if(action==="jump"){left=1.1;right=1.12;expression="happy";}
if(action==="laugh"){left=0.8+0.1*sine;right=0.9+0.2*wave;expression="happy";}
if(action==="think"){right=1.92;left=0.14;expression="think";}
if(action==="surprised"){left=1.0;right=1.0;expression="surprised";}
if(action==="confused"){left=1.15+0.1*sine;right=1.15-0.1*sine;expression="confused";}
if(action==="wave"){right=2.38+0.23*sine;left=0.12;expression="happy";}
if(action==="celebrate"){left=2.55+0.14*sine;right=2.55-0.14*sine;expression="happy";}
if(action==="listen"){left=0.18;right=0.18;expression="smile";}
const y=bob+lift;
const breathingOffsets=[[0,0],[1,0],[1,1],[0,2],[-1,1],[-1,0],[0,-1],[1,-1]];
const staticBreathing=["idle","listen","point_object","think","surprised"].includes(action);
const [offsetX,offsetY]=staticBreathing?breathingOffsets[index]:[0,0];
const endpoint=(x,a,side)=>[x+side*17*Math.sin(a),39+17*Math.cos(a)];
const [lx,ly]=endpoint(23,left,-1),[rx,ry]=endpoint(49,right,1);
const stride=moving?offset:jumping?Math.round(2*sine):0;
const legY=action==="run"?-Math.abs(offset)*0.6:0;
const lFootX=29-stride,rFootX=43+stride;
let s=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 72 82" width="288" height="328" shape-rendering="crispEdges" role="img" aria-label="8-bit UrFavXBF ${action} frame ${index+1}">`;
s+=`<g transform="translate(${offsetX} ${y+offsetY})">`;
s+=limb(29,53,lFootX,69+legY,12,"#303247")+limb(43,53,rFootX,69+legY,12,"#303247");
s+=rect(round(lFootX-8),round(69+legY),17,7,"#11162d")+rect(round(lFootX-7),round(70+legY),15,4,"#f5f5ff")+rect(round(rFootX-8),round(69+legY),17,7,"#11162d")+rect(round(rFootX-7),round(70+legY),15,4,"#f5f5ff");
s+=limb(23,39,lx,ly,11,"#203968")+limb(49,39,rx,ry,11,"#203968");
s+=rect(round(lx-3),round(ly-3),7,6,"#10172e")+rect(round(lx-2),round(ly-2),5,4,"#e2a074");
s+=rect(round(rx-3),round(ry-3),7,6,"#10172e")+rect(round(rx-2),round(ry-2),5,4,"#e2a074");
s+=path("M23 32h26v24H23z","#10172e")+rect(25,34,22,19,"#20396a")+rect(27,35,18,4,"#a1a9c1")+rect(32,38,8,15,"#f1f3f9")+rect(35,38,2,15,"#c1c8d9");
s+=rect(24,37,4,16,"#344e83")+rect(44,37,4,16,"#344e83");
s+=rect(42,39,5,5,"#10172e")+rect(43,40,3,1,"#f8f8ff")+rect(43,41,3,1,"#2853af")+rect(43,42,3,1,"#d52b3b")+rect(43,40,1,1,"#fee379");
s+=rect(32,29,8,7,"#10172e")+rect(33,30,6,5,"#d38b5e");
s+=rect(22,13,28,20,"#10172e")+rect(24,15,24,16,"#e5a06e")+rect(24,25,2,4,"#c77d51")+rect(46,25,2,4,"#c77d51");
s+=rect(21,23,4,6,"#10172e")+rect(22,24,3,4,"#e5a06e")+rect(47,23,4,6,"#10172e")+rect(47,24,3,4,"#e5a06e");
s+=path("M20 18h3V10h4V7h7V5h12v2h4v4h2v11h-4v-5h-6v-3h-8v4h-5v-2h-6v6h-3z","#1a1b30");
s+=rect(26,9,6,2,"#3e405d")+rect(37,7,8,3,"#3e405d")+rect(45,12,3,2,"#4d4d69");
s+=rect(28,20,6,2,"#1d1b31")+rect(39,20,6,2,"#1d1b31");
if(expression==="happy"){s+=rect(30,23,2,2,"#171a31")+rect(41,23,2,2,"#171a31");}
else if(expression==="surprised"){s+=rect(29,23,4,5,"#111729")+rect(40,23,4,5,"#111729");}
else {s+=rect(30,23,3,4,"#121830")+rect(41,23,3,4,"#121830")+rect(31,23,1,1,"#fff")+rect(42,23,1,1,"#fff");}
if(expression==="surprised"){s+=rect(35,28,4,4,"#7e3542")+rect(36,29,2,2,"#10172e");}
else if(expression==="think"){s+=rect(35,29,5,2,"#8d4c42");}
else if(expression==="confused"){s+=rect(35,28,4,1,"#8d4c42");s+=rect(41,19,5,1,"#10172e");}
else if(talking||expression==="happy"){s+=rect(33,28,8,4,"#10172e")+rect(34,28,6,1,"#fff")+rect(35,31,4,1,"#da6971");}
else{s+=rect(34,28,6,2,"#8c4742")+rect(35,29,5,1,"#fff");}
s+=`</g></svg>`;
return s;
}
for(const [action,count] of Object.entries(counts)){
 for(let i=0;i<count;i++){
  const destination=resolve(ROOT,'public/characters/8bit-host/urfavxbf',action,'frame-'+String(i).padStart(2,'0')+'.svg');
  mkdirSync(dirname(destination),{recursive:true});
  writeFileSync(destination,spriteSvg(action,i,count)+'\n');
 }
}
