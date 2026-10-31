#!/usr/bin/env node
/** Deterministic, local-only HyperFrames render to a staged Remotion media asset.
 * Never uses HeyGen cloud, provider media APIs, GPU flags, credentials or publishing.
 */
import {spawnSync} from 'node:child_process';
import {existsSync, mkdirSync, copyFileSync, statSync} from 'node:fs';
import {resolve, join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const project = join(root,'hyperframes/projects/kinetic-intro');
const output = join(root,'out/hyperframes/kinetic-intro.mp4');
const staged = join(root,'public/hyperframes/kinetic-intro.mp4');
const bin = join(root,'node_modules/.bin/hyperframes');
const scrub = {...process.env,
  HYPERFRAMES_NO_TELEMETRY:'1', DO_NOT_TRACK:'1', CI:'true',
  HEYGEN_API_KEY:'', HYPERFRAMES_API_KEY:'', HEYGEN_ACCESS_TOKEN:'',
  ELEVENLABS_API_KEY:'', OPENROUTER_API_KEY:'', GEMINI_API_KEY:'',
};
for(const k of Object.keys(scrub)) {
  if (k.startsWith('HEYGEN_') || k.startsWith('HYPERFRAMES_API_')) {
    if (k !== 'HYPERFRAMES_NO_TELEMETRY') scrub[k]='';
  }
}
function run(program,args,{cwd=project,capture=false}={}) {
  const r=spawnSync(program,args,{cwd,env:scrub,encoding:'utf8',
    stdio:capture?['ignore','pipe','pipe']:'inherit',timeout:1200000});
  if(r.error || r.status!==0) {
    if (capture) console.error(r.stderr);
    throw new Error('Local HyperFrames operation failed: '+args[0]);
  }
  return capture ? r.stdout : '';
}
if (!existsSync(bin)) throw new Error('HyperFrames CLI not installed: run npm ci');
run(process.execPath,[join(root,'scripts/prepare-hyperframes.mjs')],{cwd:root});
if (!existsSync(join(project,'index.html'))) throw new Error('Missing original HyperFrames composition');
run(bin,['lint']);
mkdirSync(dirname(output),{recursive:true});
run(bin,['render','--output',output]);
const probe=JSON.parse(run('ffprobe',['-v','error','-show_entries',
  'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration',
  '-of','json',output],{cwd:root,capture:true}));
const v=probe.streams?.filter(s=>s.codec_type==='video')??[];
if(v.length!==1 || v[0].codec_name!=='h264' ||
   v[0].width!==1920 || v[0].height!==1080 ||
   v[0].r_frame_rate!=='30/1' || v[0].nb_frames!=='60' ||
   Math.abs(Number(probe.format.duration)-2)>0.12 ||
   statSync(output).size<12000) throw new Error('HyperFrames render media contract failed');
run('ffmpeg',['-v','error','-xerror','-i',output,'-f','null','-'],{cwd:root});
mkdirSync(dirname(staged),{recursive:true});
copyFileSync(output,staged);
console.log('Verified original local HyperFrames animation and staged:',staged);
