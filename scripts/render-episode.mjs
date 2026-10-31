// CPU-only rendering bridge. Python owns deadlines, immutable inputs and stage state.
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderMedia} from '@remotion/renderer';
import {mkdtemp,readFile,rm,stat} from 'node:fs/promises';
import path from 'node:path';
import {tmpdir} from 'node:os';
const [propsFile, publicDir, outputLocation, scaleString='1'] = process.argv.slice(2);
const scale=Number(scaleString);
if(![1,0.25].includes(scale)) throw new Error('Only production or diagnostic quarter scale allowed');
if((await stat(propsFile)).size>4*1024*1024) throw new Error('Oversized episode props');
const inputProps=JSON.parse(await readFile(propsFile,'utf8'));
const temp=await mkdtemp(path.join(tmpdir(),'episode-render-'));
const browserExecutable=process.env.REMOTION_BROWSER_EXECUTABLE;
const chromiumOptions={gl:'swangle'};
let browser;
try {
 const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),publicDir:path.resolve(publicDir),outDir:path.join(temp,'bundle')});
 browser=await openBrowser('chrome',{browserExecutable,chromiumOptions});
 const composition=await selectComposition({serveUrl,id:'EpisodeProduction',inputProps,browserExecutable,chromiumOptions,puppeteerInstance:browser});
 await renderMedia({serveUrl,composition,inputProps,outputLocation,codec:'h264',audioCodec:'aac',
  pixelFormat:'yuv420p',concurrency:2,scale,browserExecutable,puppeteerInstance:browser,
  chromiumOptions,hardwareAcceleration:'disable',timeoutInMilliseconds:30000,overwrite:false,logLevel:'error'});
 console.log('Rendered local episode artifact');
} finally {
 if(browser) await browser.close({silent:true});
 await rm(temp,{recursive:true,force:true});
}
