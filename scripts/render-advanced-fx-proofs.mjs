/** Verify 2 distinct rendered frames for every one of the 12 original advanced effects.
 * Bundles once; runs sequentially for bounded CPU/memory and zero paid services.
 */
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const ids=[
  'rgb-split','speed-trails','film-light-leak','glass-shatter',
  'liquid-displacement','pixel-dissolve','whip-pan-blur','svg-path-morph',
  'comic-halftone','shader-portal','film-burn-reveal','audio-reactive-particles',
];
const out=path.resolve(process.argv[2]||'out/cinematic-fx/stills');
fs.mkdirSync(out,{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),symlinkPublicDir:true});
try{
  for(const id of ids){
    const props={id,from:12};
    const composition=await selectComposition({serveUrl,id:'FxPreview',inputProps:props});
    const frames=[15,Math.min(48,composition.durationInFrames-2)];
    for(const frame of frames){
      const output=path.join(out,`${id}-f${frame}.png`);
      await renderStill({serveUrl,composition,inputProps:props,frame,
        scale:.25,output,imageFormat:'png'});
      if(fs.statSync(output).size<1000) throw Error('Invalid still: '+output);
      console.log('Rendered actual effect',id,'frame',frame);
    }
    const first=fs.readFileSync(path.join(out,`${id}-f${frames[0]}.png`));
    const second=fs.readFileSync(path.join(out,`${id}-f${frames[1]}.png`));
    if(first.equals(second))throw Error(id+' produced two identical frames');
  }
}finally{fs.rmSync(serveUrl,{recursive:true,force:true});}
