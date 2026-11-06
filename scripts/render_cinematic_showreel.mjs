#!/usr/bin/env node
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root=fileURLToPath(new URL('../',import.meta.url));
function run(command,args){
 const result=spawnSync(command,args,{cwd:root,stdio:'inherit'});
 if(result.error)throw result.error;
 if(result.status!==0)process.exit(result.status??1);
}
run('python3',['scripts/prepare_showreel.py','--check']);
run(process.execPath,[path.join(root,'node_modules/@remotion/cli/remotion-cli.js'),
 'render','CinematicShowreel','out/showreel/cinematic-showreel-unmastered.mp4',
 '--props',JSON.stringify({audioReady:true}),'--codec=h264','--audio-codec=aac',
 '--audio-bitrate=320k','--pixel-format=yuv420p','--crf=18','--concurrency=2','--gl=angle',
 ...process.argv.slice(2)]);
run('python3',['scripts/master_showreel.py']);
