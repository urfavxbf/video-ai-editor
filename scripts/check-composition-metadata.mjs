// Exercise actual registrations through Remotion, without rendering or external media.
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition} from '@remotion/renderer';

const temp = await mkdtemp(path.join(tmpdir(), 'composition-metadata-'));
const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE;
const edit = JSON.parse(await readFile('src/edit/edit.json', 'utf8'));
const shortEdit = {...edit, segments: [{kind: 'aroll', at: 0, frames: 10}]};
const episode = JSON.parse(await readFile('src/episodes/episode-proof-v1.json', 'utf8'));
const shortEpisode = structuredClone(episode);
shortEpisode.chapters = [{...shortEpisode.chapters[0], durationFrames: 17}];
let browser;
try {
  const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), outDir: path.join(temp, 'bundle')});
  browser = await openBrowser('chrome', {browserExecutable});
  const select = (id, inputProps) => selectComposition({
    serveUrl, id, inputProps, browserExecutable, puppeteerInstance: browser,
  });
  const cases = [
    ['HeroCharacterStage', {}, 540],
    ['HeroCharacterStage', {durationFrames: 900}, 900],
    ['ExampleEdit', {}, 299],
    ['ExampleEdit', {spec: shortEdit}, 10],
    ['EpisodeTimelineProof', {}, 120],
    ['EpisodeTimelineProof', {manifest: shortEpisode}, 17],
    ['EpisodeProduction', {}, 120],
    ['EpisodeProduction', {manifest: shortEpisode, captions:{}}, 17],
  ];
  const invalidEpisode = structuredClone(episode);
  invalidEpisode.chapters[1].startFrame = 59;
  await assert.rejects(select('EpisodeTimelineProof', {manifest: invalidEpisode}), /contiguous timeline offset/);
  const actual = [];
  for (const [id, inputProps, expected] of cases) {
    const composition = await select(id, inputProps);
    console.log(JSON.stringify({id, expected, actual: composition.durationInFrames}));
    actual.push(composition.durationInFrames);
  }
  assert.deepEqual(actual, cases.map(([, , expected]) => expected));
  console.log('Verified actual metadata registrations, defaults and overrides');
} finally {
  if (browser) await browser.close({silent: true});
  await rm(temp, {recursive: true, force: true});
}
