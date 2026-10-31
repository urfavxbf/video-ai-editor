#!/usr/bin/env node
/** Stage pinned local GSAP into this standalone HyperFrames project.
 * Never download an external browser script or vendor a stale binary in Git.
 */
import {copyFileSync, existsSync, mkdirSync} from 'node:fs';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const source=join(root,'node_modules/gsap/dist/gsap.min.js');
const target=join(root,'hyperframes/projects/kinetic-intro/assets/gsap.min.js');
if(!existsSync(source)) throw Error('Pinned GSAP missing; run npm ci');
mkdirSync(dirname(target),{recursive:true});
copyFileSync(source,target);
console.log('Staged local GSAP for offline HyperFrames render');
