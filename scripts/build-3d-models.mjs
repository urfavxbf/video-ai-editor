// Deterministic original glTF 2.0 character builder. No paid services or packages.
// Run: node scripts/build-3d-models.mjs
import {mkdirSync, writeFileSync} from 'node:fs';

const makeModels = function makeModels() {
  const toHex = (hex) => {
    const n = parseInt(hex.slice(1), 16);
    return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255, 1];
  };
  const b64 = (bytes) => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let s = "";
    for (let i = 0; i < bytes.length; i += 3) {
      const a = bytes[i], b = bytes[i+1], c = bytes[i+2];
      s += chars[a>>2] + chars[((a&3)<<4)|((b??0)>>4)] +
        (i+1<bytes.length ? chars[((b&15)<<2)|((c??0)>>6)] : "=") +
        (i+2<bytes.length ? chars[c&63] : "=");
    }
    return s;
  };
  const geometry = (kind) => {
    let p = [], normal = [], faces = [];
    const v = (x,y,z,nx,ny,nz) => {p.push(x,y,z);normal.push(nx,ny,nz);return p.length/3-1;};
    const tri = (a,b,c) => faces.push(a,b,c);
    if (kind==="sphere") {
      const lat=12, lon=18;
      for(let y=0;y<=lat;y++) {
        const theta=Math.PI*y/lat;
        for(let x=0;x<=lon;x++){
          const phi=2*Math.PI*x/lon;
          const a=Math.sin(theta)*Math.cos(phi), b=Math.cos(theta), c=Math.sin(theta)*Math.sin(phi);
          v(a,b,c,a,b,c);
        }
      }
      for(let y=0;y<lat;y++) for(let x=0;x<lon;x++){let a=y*(lon+1)+x,b=a+lon+1;tri(a,b,a+1);tri(a+1,b,b+1);}
    } else if(kind==="box"){
      const sides=[
        [[0,0,1],[[-.5,-.5,.5],[.5,-.5,.5],[.5,.5,.5],[-.5,.5,.5]]],
        [[0,0,-1],[[.5,-.5,-.5],[-.5,-.5,-.5],[-.5,.5,-.5],[.5,.5,-.5]]],
        [[1,0,0],[[.5,-.5,.5],[.5,-.5,-.5],[.5,.5,-.5],[.5,.5,.5]]],
        [[-1,0,0],[[-.5,-.5,-.5],[-.5,-.5,.5],[-.5,.5,.5],[-.5,.5,-.5]]],
        [[0,1,0],[[-.5,.5,.5],[.5,.5,.5],[.5,.5,-.5],[-.5,.5,-.5]]],
        [[0,-1,0],[[-.5,-.5,-.5],[.5,-.5,-.5],[.5,-.5,.5],[-.5,-.5,.5]]]
      ];
      for(const [n,quad] of sides){const start=p.length/3;for(const q of quad)v(...q,...n);tri(start,start+1,start+2);tri(start,start+2,start+3);}
    } else if(kind==="cone"||kind==="cylinder"){
      const seg=18, r=.5;
      for(let j=0;j<2;j++)for(let i=0;i<=seg;i++){
        const a=i*2*Math.PI/seg, x=Math.cos(a), z=Math.sin(a);
        v(x*(j===1&&kind==="cone"?0:r),j-.5,z*(j===1&&kind==="cone"?0:r),x,0,z);
      }
      for(let i=0;i<seg;i++){let a=i,b=a+seg+1;tri(a,b,a+1);tri(a+1,b,b+1);}
    } else if(kind==="torus"||kind==="arc"){
      const around=kind==="arc"?18:28, tube=8, span=kind==="arc"?Math.PI:2*Math.PI;
      for(let i=0;i<=around;i++) {
        const theta=span*i/around + (kind==="arc"?0:0);
        for(let j=0;j<=tube;j++){
          const phi=2*Math.PI*j/tube, rr=1+0.12*Math.cos(phi);
          v(rr*Math.cos(theta),rr*Math.sin(theta),0.12*Math.sin(phi),
            Math.cos(phi)*Math.cos(theta),Math.cos(phi)*Math.sin(theta),Math.sin(phi));
        }
      }
      for(let i=0;i<around;i++)for(let j=0;j<tube;j++){let a=i*(tube+1)+j,b=a+tube+1;tri(a,a+1,b);tri(a+1,b+1,b);}
    } else throw Error(kind);
    return {p,normal,faces};
  };
  const quat=(x=0,y=0,z=0)=>{
    const a=x/2,b=y/2,c=z/2, c1=Math.cos(a),c2=Math.cos(b),c3=Math.cos(c),s1=Math.sin(a),s2=Math.sin(b),s3=Math.sin(c);
    return [s1*c2*c3+c1*s2*s3,c1*s2*c3-s1*c2*s3,c1*c2*s3+s1*s2*c3,c1*c2*c3-s1*s2*s3];
  };
  function build(id) {
    let buffer=[],bufferViews=[],accessors=[],meshes=[],nodes=[],materials=[],animations=[];
    const geomCache={}, matCache={}, meshCache={},named={};
    const addBytes=(data,target)=>{
      while(buffer.length%4) buffer.push(0);
      const off=buffer.length;
      const bytes=new Uint8Array(data.buffer,data.byteOffset,data.byteLength);
      for(const byte of bytes)buffer.push(byte);
      const view=bufferViews.push({buffer:0,byteOffset:off,byteLength:bytes.length,...(target?{target}:{})})-1;
      return view;
    };
    const accessor=(arr,type,componentType,target,min,max)=>{
      const typed=componentType===5123?new Uint16Array(arr):new Float32Array(arr);
      const bufferView=addBytes(typed,target);
      return accessors.push({bufferView,componentType,count:arr.length/({SCALAR:1,VEC3:3,VEC4:4}[type]),type,...(min?{min}:{}),...(max?{max}:{})})-1;
    };
    const makeGeom=(kind)=>{
      if(geomCache[kind])return geomCache[kind];
      const g=geometry(kind), count=g.p.length/3;
      const bounds=[[0,1,2].map(n=>Math.min(...g.p.filter((_,i)=>i%3===n))),[0,1,2].map(n=>Math.max(...g.p.filter((_,i)=>i%3===n)))];
      const data={POSITION:accessor(g.p,"VEC3",5126,34962,bounds[0],bounds[1]),NORMAL:accessor(g.normal,"VEC3",5126,34962),indices:accessor(g.faces,"SCALAR",5123,34963)};
      geomCache[kind]=data;return data;
    };
    const mat=(hex)=>{
      if(matCache[hex]!==undefined)return matCache[hex];
      const n=materials.push({name:"paint_"+hex.slice(1),doubleSided:true,pbrMetallicRoughness:{baseColorFactor:toHex(hex),metallicFactor:0.07,roughnessFactor:0.73}})-1;
      matCache[hex]=n;return n;
    };
    const getMesh=(kind,color)=>{
      const key=kind+"_"+color;
      if(meshCache[key]!==undefined)return meshCache[key];
      const g=makeGeom(kind);
      const n=meshes.push({name:key,primitives:[{attributes:{POSITION:g.POSITION,NORMAL:g.NORMAL},indices:g.indices,material:mat(color)}]})-1;
      meshCache[key]=n;return n;
    };
    const node=(name,parent,translation=[0,0,0],rotation=[0,0,0],scale=[1,1,1],mesh=null)=>{
      if(named[name]!==undefined)throw Error("duplicate node "+name);
      const n=nodes.push({name,translation,rotation:quat(...rotation),scale,children:[],...(mesh!==null?{mesh}:{})})-1;
      if(parent!==null)nodes[parent].children.push(n);
      named[name]=n; return n;
    };
    const piece=(name,kind,color,parent,xyz,scale,rotation=[0,0,0])=>node(name,parent,xyz,rotation,scale,getMesh(kind,color));
    const C=id==="urfavxbf"?{
      green:"#6ffb8b",hood:"#123f2c",hoodD:"#0b241a",black:"#0a1015",
      skin:"#e8ad81",skinLight:"#f7cba8",hair:"#11191b",shoe:"#1b2e27",
      eye:"#21cf72",white:"#eaf9f5"
    }:{
      cyan:"#70e8ff",ice:"#c3f8ff",white:"#f0ffff",blue:"#14c7f8",
      purple:"#8955ff",pink:"#f588d9",dark:"#23304c",eye:"#6851bf",
      collar:"#20e9e9"
    };
    const root=node("motion_root",null);
    const hip=node("hip",root,[0,0.92,0]);
    if(id==="urfavxbf"){
      const torso=node("torso",hip,[0,0.20,0]);
      piece("hoodie_body","sphere",C.hood,torso,[0,0.12,0],[.52,.69,.34]);
      piece("hoodie_mid_panel","sphere",C.hoodD,torso,[0,.13,.29],[.32,.51,.095]);
      piece("hoodie_pocket","box",C.hoodD,torso,[0,-.20,.347],[.37,.19,.055]);
      piece("hoodie_edge_l","cylinder",C.green,torso,[-.41,.14,.13],[.026,.74,.028],[0,0,-.17]);
      piece("hoodie_edge_r","cylinder",C.green,torso,[.41,.14,.13],[.026,.74,.028],[0,0,.17]);
      piece("hoodie_X_stripe_a","box",C.green,torso,[0,.13,.404],[.36,.065,.026],[0,0,.76]);
      piece("hoodie_X_stripe_b","box",C.green,torso,[0,.13,.405],[.36,.065,.026],[0,0,-.76]);
      piece("hood","sphere",C.hoodD,torso,[0,.57,-.18],[.45,.27,.26]);
      piece("neck","cylinder",C.skin,torso,[0,.75,0],[.17,.24,.16]);
      const head=node("head_joint",torso,[0,.94,0]);
      piece("face","sphere",C.skin,head,[0,.21,.04],[.75,.69,.63]);
      piece("cheek_l","sphere",C.skinLight,head,[-.47,-.10,.46],[.20,.15,.15]);
      piece("cheek_r","sphere",C.skinLight,head,[.47,-.10,.46],[.20,.15,.15]);
      for(const sign of [-1,1]){
        const side=sign<0?"left":"right", x=sign*.34;
        piece(side+"_eyewhite","sphere",C.white,head,[x,.30,.576],[.20,.22,.092]);
        piece(side+"_iris","sphere",C.eye,head,[x,.29,.663],[.113,.145,.044]);
        piece(side+"_pupil","sphere",C.black,head,[x,.29,.704],[.056,.097,.027]);
        piece(side+"_eye_glint","sphere",C.white,head,[x-.033,.354,.731],[.027,.029,.012]);
        piece(side+"_brow","box",C.hair,head,[x,.56,.61],[.28,.049,.057],[0,0,sign*-.10]);
        piece(side+"_headset_cup","sphere",C.hoodD,head,[sign*.77,.32,-.015],[.18,.34,.31]);
        piece(side+"_headset_neon","sphere",C.green,head,[sign*.86,.32,.055],[.07,.22,.22]);
        piece(side+"_headset_X_a","box",C.black,head,[sign*.929,.32,.08],[.016,.25,.042],[.7,0,0]);
        piece(side+"_headset_X_b","box",C.black,head,[sign*.931,.32,.08],[.016,.25,.042],[-.7,0,0]);
      }
      piece("headphones_headband","arc",C.green,head,[0,.26,0],[.90,.86,.90]);
      piece("nose","sphere",C.skinLight,head,[0,.085,.647],[.11,.085,.065]);
      const mouth=node("mouth_joint",head,[0,-.12,.64]);
      piece("mouth_dark","sphere",C.black,mouth,[0,0,.015],[.16,.07,.03]);
      piece("mouth_tongue","sphere","#ed7fa1",mouth,[0,-.025,.039],[.075,.02,.018]);
      piece("hair_mass","sphere",C.hair,head,[0,.80,-.015],[.78,.40,.64]);
      for(let i=0;i<11;i++){
        const a=(i/10)*Math.PI, x=-.71+1.42*i/10, y=.94+(i%3)*.045;
        piece("black_spike_"+i,"cone",C.hair,head,[x,y,.35+Math.sin(a)*.11],[.19,.40+.05*(i%3),.19],[.22,0,-.32+x*.4]);
      }
      for(let i=0;i<4;i++){
        piece("neon_hair_streak_"+i,"cone",C.green,head,[-.40+i*.26,1.04-i*.055,.43],[.052,.35,.062],[.28,0,.27]);
      }
      for(const s of [-1,1]){
        const left=s<0, side=left?"left":"right";
        const arm=node(side+"_arm_joint",torso,[s*.48,.54,0], [0,0,-s*.28]);
        piece(side+"_sleeve","sphere",C.hood,arm,[s*.14,-.32,.02],[.20,.40,.24]);
        piece(side+"_cuff","cylinder",C.green,arm,[s*.26,-.64,.03],[.16,.11,.15],[0,0,s*.1]);
        piece(side+"_palm","sphere",C.skin,arm,[s*.28,-.79,.06],[.16,.21,.09]);
        for(let k=0;k<3;k++)piece(side+"_finger_"+k,"sphere",C.skinLight,arm,[s*(.20+k*.085),-.975,.077],[.037,.105,.039],[0,0,s*.10]);
        const leg=node(side+"_leg_joint",hip,[s*.27,-.28,0]);
        piece(side+"_pants","sphere",C.black,leg,[0,-.28,0],[.27,.48,.29]);
        piece(side+"_cargo_pocket","box",C.hoodD,leg,[s*.21,-.25,.17],[.095,.25,.15]);
        piece(side+"_shoe","box",C.shoe,leg,[0,-.72,.15],[.44,.28,.61]);
        piece(side+"_shoe_cap","box",C.green,leg,[0,-.75,.45],[.43,.12,.13]);
      }
    } else {
      const body=node("torso",hip,[0,-.22,0]);
      piece("fluffy_torso","sphere",C.cyan,body,[0,0,0],[.59,.62,.47]);
      piece("chest","sphere",C.ice,body,[0,-.03,.36],[.37,.47,.17]);
      const head=node("head_joint",body,[0,.72,.05]);
      piece("face","sphere",C.cyan,head,[0,.25,.0],[.75,.66,.62]);
      piece("cheek_fluff_left","sphere",C.ice,head,[-.46,-.06,.41],[.28,.22,.24]);
      piece("cheek_fluff_right","sphere",C.ice,head,[.46,-.06,.41],[.28,.22,.24]);
      for(const s of [-1,1]){
        const side=s<0?"left":"right";
        piece(side+"_ear","cone",C.cyan,head,[s*.47,.90,-.06],[.41,.78,.22],[0,0,s*-.17]);
        piece(side+"_ear_inner","cone",C.pink,head,[s*.47,.89,.14],[.23,.49,.075],[0,0,s*-.17]);
        piece(side+"_eyewhite","sphere",C.white,head,[s*.31,.32,.53],[.235,.29,.105]);
        piece(side+"_iris","sphere",C.purple,head,[s*.31,.31,.632],[.135,.19,.055]);
        piece(side+"_pupil","sphere",C.dark,head,[s*.31,.30,.682],[.075,.125,.027]);
        piece(side+"_glint","sphere",C.white,head,[s*.30-.035,.39,.702],[.04,.05,.018]);
        piece(side+"_headphone","sphere",C.purple,head,[s*.77,.34,-.06],[.17,.32,.30]);
        piece(side+"_headphone_light","torus",C.pink,head,[s*.84,.34,.02],[.27,.27,.27],[0,Math.PI/2,0]);
        for(let i=0;i<3;i++)piece(side+"_whisker_"+i,"cylinder",C.white,head,[s*.58,-.08+(i-1)*.082,.55],[.015,.36,.015],[0,0,-s*1.32+(i-1)*.12]);
      }
      piece("headphone_band","arc",C.purple,head,[0,.32,-.14],[.88,.93,.84]);
      piece("muzzle_l","sphere",C.ice,head,[-.15,-.10,.575],[.22,.15,.12]);
      piece("muzzle_r","sphere",C.ice,head,[.15,-.10,.575],[.22,.15,.12]);
      piece("nose","sphere",C.pink,head,[0,-.08,.701],[.11,.075,.055]);
      const mouth=node("mouth_joint",head,[0,-.24,.64]);
      piece("kitty_mouth","sphere",C.dark,mouth,[0,0,.01],[.13,.06,.03]);
      piece("kitty_tongue","sphere",C.pink,mouth,[0,-.035,.03],[.09,.04,.02]);
      piece("collar","torus",C.purple,body,[0,.45,.04],[.48,.27,.41],[Math.PI/2,0,0]);
      piece("collar_glow","sphere",C.blue,body,[0,.35,.49],[.17,.19,.085]);
      const tail=node("tail_joint",body,[0,-.26,-.43],[.55,0,-.22]);
      piece("tail_base","sphere",C.cyan,tail,[0,.15,-.31],[.19,.20,.43],[-.4,0,0]);
      piece("tail_tip","sphere",C.purple,tail,[0,.44,-.58],[.18,.30,.22]);
      for(const s of [-1,1])for(const front of [true,false]){
        const side=(s<0?"left":"right")+"_"+(front?"front":"back");
        const leg=node(side+"_leg_joint",body,[s*.37,-.32,front?.25:-.27]);
        piece(side+"_paw","sphere",C.cyan,leg,[0,-.35,front?.12:0],[.20,.40,.22]);
        piece(side+"_toe","sphere",C.ice,leg,[0,-.62,.12],[.22,.11,.28]);
      }
    }
    function animation(name,duration,tracks){
      const times=[0,.25,.50,.75,1].map(x=>x*duration);
      const input=accessor(times,"SCALAR",5126,undefined,[0],[duration]);
      const samplers=[],channels=[];
      for(const [target, def] of Object.entries(tracks)){
        if(named[target]===undefined)throw Error(id+": animation missing "+target);
        const path=def.path??"rotation";
        const values=def.values.map(v=>path==="rotation"?quat(...v):v).flat();
        const output=accessor(values,path==="rotation"?"VEC4":"VEC3",5126);
        const sampler=samplers.push({input,output,interpolation:"LINEAR"})-1;
        channels.push({sampler,target:{node:named[target],path}});
      }
      animations.push({name,samplers,channels,extras:{durationSeconds:duration,loop:["idle","walk","run","talk","laugh","tail_wag","curious","explain"].includes(name)}});
    }
    const R=(a)=>a.map(x=>[x,0,0]), Z=(a)=>a.map(x=>[0,0,x]), T=(a)=>a.map(y=>[0,y,0]);
    const idle=[0,-.025,0,.025,0];
    if(id==="urfavxbf"){
      const walk=[-.46,0,.46,0,-.46], inverse=walk.map(v=>-v);
      animation("idle",1.6,{"head_joint":{values:Z(idle)},"torso":{values:R(idle)}});
      animation("walk",1.0,{"left_leg_joint":{values:R(walk)},"right_leg_joint":{values:R(inverse)},"left_arm_joint":{values:R(inverse.map(v=>v*.65))},"right_arm_joint":{values:R(walk.map(v=>v*.65))},"motion_root":{path:"translation",values:T([0,.08,0,.08,0])}});
      animation("run",.7,{"left_leg_joint":{values:R(walk.map(v=>v*1.4))},"right_leg_joint":{values:R(inverse.map(v=>v*1.4))},"left_arm_joint":{values:R(inverse)},"right_arm_joint":{values:R(walk)},"motion_root":{path:"translation",values:T([0,.18,.05,.18,0])}});
      animation("point_camera",1.0,{"right_arm_joint":{values:[[0,0,-.28],[-1.0,0,-.25],[-1.35,0,-.10],[-1.35,0,-.10],[0,0,-.28]]},"head_joint":{values:Z([0,-.07,-.07,-.07,0])}});
      animation("point_object",1.0,{"right_arm_joint":{values:Z([-.28,-.65,-1.22,-1.22,-.28])},"head_joint":{values:Z([0,-.08,-.12,-.12,0])}});
      animation("talk",.9,{"mouth_joint":{path:"scale",values:[[1,1,1],[1,2.0,1],[1,.7,1],[1,1.7,1],[1,1,1]]},"head_joint":{values:R([0,.055,-.03,.06,0])},"right_arm_joint":{values:Z([-.28,-.46,-.20,-.50,-.28])}});
      animation("laugh",1.0,{"mouth_joint":{path:"scale",values:[[1,1.0,1],[1,2.8,1],[1,2,1],[1,2.9,1],[1,1,1]]},"head_joint":{values:R([0,-.14,-.03,-.16,0])},"torso":{values:R([0,-.07,.05,-.1,0])}});
      animation("jump",1.1,{"motion_root":{path:"translation",values:T([0,-.15,.78,.32,0])},"left_arm_joint":{values:Z([0,.5,.8,.5,0])},"right_arm_joint":{values:Z([0,-.5,-.8,-.5,0])},"left_leg_joint":{values:R([0,.1,.35,.2,0])},"right_leg_joint":{values:R([0,-.1,-.35,-.2,0])}});
      animation("explain",1.2,{"left_arm_joint":{values:Z([.28,.55,.22,.55,.28])},"right_arm_joint":{values:Z([-.28,-.54,-.28,-.60,-.28])},"head_joint":{values:Z([0,.05,0,-.04,0])}});
      animation("wave",1.0,{"right_arm_joint":{values:Z([-.28,-2.1,-1.5,-2.1,-.28])}});
    } else {
      const paws=["left_front_leg_joint","right_front_leg_joint","left_back_leg_joint","right_back_leg_joint"];
      animation("idle",1.5,{"head_joint":{values:Z(idle)},"tail_joint":{values:Z([0,.14,0,-.14,0])}});
      animation("walk",.85,{[paws[0]]:{values:R([-.45,0,.45,0,-.45])},[paws[1]]:{values:R([.45,0,-.45,0,.45])},[paws[2]]:{values:R([.45,0,-.45,0,.45])},[paws[3]]:{values:R([-.45,0,.45,0,-.45])},"tail_joint":{values:Z([0,.1,0,-.1,0])}});
      animation("talk",.8,{"mouth_joint":{path:"scale",values:[[1,1,1],[1,2.1,1],[1,.8,1],[1,1.7,1],[1,1,1]]},"head_joint":{values:R([0,.06,-.03,.06,0])}});
      animation("laugh",1.0,{"mouth_joint":{path:"scale",values:[[1,1,1],[1,2.6,1],[1,1.6,1],[1,2.6,1],[1,1,1]]},"head_joint":{values:Z([0,-.10,.08,-.10,0])}});
      animation("jump",1.0,{"motion_root":{path:"translation",values:T([0,.10,.67,.30,0])},"tail_joint":{values:R([0,-.14,-.28,-.16,0])}});
      animation("pounce",.9,{"motion_root":{path:"translation",values:[[0,0,0],[0,.23,.15],[0,.47,.42],[0,.24,.5],[0,0,0]]},"head_joint":{values:R([0,.15,.20,.1,0])}});
      animation("tail_wag",.85,{"tail_joint":{values:Z([0,.5,0,-.5,0])}});
      animation("curious",1.3,{"head_joint":{values:Z([0,-.18,-.27,-.18,0])},"tail_joint":{values:Z([0,.15,0,-.15,0])}});
      animation("assist_point",1.1,{"right_front_leg_joint":{values:R([0,-.55,-1.0,-.55,0])},"head_joint":{values:Z([0,.1,.12,.1,0])}});
      animation("wave",1,{"left_front_leg_joint":{values:R([0,-.55,-.25,-.55,0])}});
    }
    const gltf={asset:{version:"2.0",generator:"UrFavXBF × PIX zero-budget procedural rig generator",copyright:"Original procedural geometry; created for urfavxbf/video-ai-editor"},scene:0,scenes:[{name:id+"_scene",nodes:[root]}],nodes,meshes,materials,buffers:[{byteLength:buffer.length,uri:"data:application/octet-stream;base64,"+b64(buffer)}],bufferViews,accessors,animations,extras:{character:id,visualVersion:"procedural-3d-v1",rigType:"rigid-hierarchical-pivots",productionArtApproved:false,generatedFrom:"official character descriptions dated 2026-10-29",isIdentityMatchedToReference:false,license:"Original project-generated asset"}};
    for(const a of animations){for(const c of a.channels)if(!nodes[c.target.node])throw Error("orphan channel");}
    return {model:gltf,stats:{bytes:buffer.length,nodes:nodes.length,meshes:meshes.length,animations:animations.map(a=>a.name)}};
  }
  return {urfavxbf:build("urfavxbf"),pix:build("pix")};
};
const models = makeModels();
mkdirSync('public/characters/3d', {recursive:true});
for (const id of ['urfavxbf','pix']) {
  writeFileSync('public/characters/3d/'+id+'.gltf', JSON.stringify(models[id].model));
  console.log(id, models[id].stats);
}
