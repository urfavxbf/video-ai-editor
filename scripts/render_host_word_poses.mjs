import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import crypto from 'node:crypto';
const run=(cmd,args)=>{const result=spawnSync(cmd,args,{stdio:'inherit'});if(result.status!==0)process.exit(result.status??1)};
run('python3',['scripts/prepare_host_word_poses.py','--check']);
const data=JSON.parse(fs.readFileSync('src/characters/word-poses/performance.json'));
const art=JSON.parse(fs.readFileSync('characters/urfavxbf-8bit-manifest.json'));
const hash=path=>crypto.createHash('sha256').update(fs.readFileSync(path)).digest('hex');
if(!data.ready||hash('public/'+data.audio)!==data.audioSha256||hash(art.source)!==art.sourceSha256)throw new Error('Missing or changed narration/art: prepare and verify assets first');
fs.mkdirSync('out/host-poses',{recursive:true});
run('npx',['remotion','render','WordPoseHostDemo','out/host-poses/unmastered.mp4','--props={"audioReady":true}','--codec=h264','--audio-codec=aac','--audio-bitrate=320k','--pixel-format=yuv420p','--crf=18','--concurrency=2','--gl=angle','--browser-executable=/usr/bin/chromium']);
run('python3',['scripts/master_showreel.py','--source','out/host-poses/unmastered.mp4','--output','out/host-poses/mastered.mp4']);

// Bound the AAC tail to the authored picture duration; retain the rendered picture.
run('ffmpeg',['-v','error','-y','-i','out/host-poses/mastered.mp4','-t',String(data.durationFrames/30),'-c','copy','-movflags','+faststart','out/host-poses/urfavxbf-word-poses.mp4']);
