/** Render every one of the 33 registered effects through the real FxPreview composition.
 * Bundles once, renders sequentially (CPU only). Each clip is extended to fit its Chatterbox line.
 * usage: node scripts/showreel_render_fx.mjs showreel/script.json out/showreel/voice/voices.json out/showreel/fx
 */
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

const [scriptPath = 'showreel/script.json', voicesPath = 'out/showreel/voice/voices.json', outDir = 'out/showreel/fx'] = process.argv.slice(2);
const LEAD = 8, TAIL = 16, MAX_EXTEND = 75;
const script = JSON.parse(fs.readFileSync(scriptPath, 'utf8'));
const voices = Object.fromEntries(JSON.parse(fs.readFileSync(voicesPath, 'utf8')).lines.map(l => [l.n, l]));
const scale = Number(process.env.SHOWREEL_FX_SCALE || 0.5);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), symlinkPublicDir: true});
const manifest = [];
try {
  for (const s of script.scenes.filter(x => x.kind === 'fx')) {
    const inputProps = {id: s.id, from: 10};
    const comp = await selectComposition({serveUrl, id: 'FxPreview', inputProps});
    const need = Math.ceil((voices[s.n]?.seconds ?? 2) * 30) + LEAD + TAIL;
    const frames = Math.min(Math.max(comp.durationInFrames, need), comp.durationInFrames + MAX_EXTEND, 280);
    const output = path.join(outDir, `${s.id}.mp4`);
    const t0 = Date.now();
    await renderMedia({serveUrl, composition: {...comp, durationInFrames: frames}, inputProps, codec: 'h264',
      outputLocation: output, scale, crf: 18, pixelFormat: 'yuv420p', concurrency: 3, audioCodec: 'aac'});
    if (fs.statSync(output).size < 20000) throw Error('Suspiciously small render: ' + output);
    manifest.push({id: s.id, n: s.n, file: path.basename(output), naturalFrames: comp.durationInFrames, frames});
    console.log(`Rendered ${s.index}/33 ${s.id}: ${frames} frames (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
  }
} finally {
  fs.rmSync(serveUrl, {recursive: true, force: true});
}
if (manifest.length !== 33) throw Error('expected 33 effects, rendered ' + manifest.length);
fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify(manifest, null, 1));
