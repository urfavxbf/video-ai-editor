const assert=require('node:assert/strict');
const fs=require('node:fs');
const {test}=require('node:test');
const perf=JSON.parse(fs.readFileSync('src/characters/word-poses/performance.json'));
const art=JSON.parse(fs.readFileSync('characters/urfavxbf-8bit-manifest.json'));
test('every spoken word triggers a distinct pose and at least one stable rendered frame',()=>{
  assert.equal(perf.words.length,36);
  for(let i=0;i<perf.words.length;i++){
    const word=perf.words[i],at=Math.round(word.startMs*30/1000);
    const next=i+1<perf.words.length?Math.round(perf.words[i+1].startMs*30/1000):perf.durationFrames;
    assert.ok(next-at>=4,`${word.text} must survive its 3-frame glitch`);
    assert.ok(word.endMs>word.startMs);
    assert.ok(word.endMs<=perf.durationFrames/30*1000);
    if(i)assert.notEqual(word.pose,perf.words[i-1].pose);
  }
});
test('all nine owner-selected full-body poses appear, including each turnaround',()=>{
  assert.deepEqual([...new Set(perf.words.map(w=>w.pose))].sort(),Object.keys(art.poses).sort());
  for(const [text,pose] of [['sideways,','side'],['behind','back'],['explain','explaining'],['Wow,','surprised']])assert.equal(perf.words.find(w=>w.text===text).pose,pose);
});
test('every caption belongs to exactly one phrase and has an audio provenance hash',()=>{
  const words=perf.phrases.flatMap(p=>perf.words.slice(p.wordStart,p.wordStart+p.wordCount));
  assert.deepEqual(words,perf.words);
  assert.match(perf.audioSha256,/^[a-f0-9]{64}$/);
  assert.match(perf.alignment,/CTC/);
});
