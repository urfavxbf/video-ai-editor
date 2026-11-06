#!/usr/bin/env node
const fs=require('node:fs');
const path=require('node:path');
const Module=require('node:module');
const ts=require('typescript');
const filename=path.resolve(__dirname,'../src/showcase/showreelTimeline.ts');
const m=new Module(filename,module);m.filename=filename;m.paths=Module._nodeModulePaths(path.dirname(filename));
m._compile(ts.transpileModule(fs.readFileSync(filename,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
const t=m.exports;
const manifest={fps:t.SHOWREEL_FPS,width:1920,height:1080,durationFrames:t.SHOWREEL_FRAMES,
 introFrames:t.INTRO_FRAMES,outroFrames:t.OUTRO_FRAMES,shots:t.SHOWREEL_SHOTS.map(s=>({...s,poses:{urfavxbf:t.shotPose('urfavxbf',s.index),pix:t.shotPose('pix',s.index)}}))};
if(require.main===module)process.stdout.write(JSON.stringify(manifest,null,2)+'\n');
module.exports=manifest;
