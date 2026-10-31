// Offline bridge to the same TypeScript manifest validator used by Remotion.
const fs=require('node:fs');const path=require('node:path');const Module=require('node:module');const ts=require('typescript');
try {
 const file=path.resolve(__dirname,'../src/episodes/episodeManifest.ts');
 const m=new Module(file,module);m.filename=file;m.paths=Module._nodeModulePaths(path.dirname(file));
 m._compile(ts.transpileModule(fs.readFileSync(file,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,file);
 const input=process.argv[2];if(fs.statSync(input).size>2*1024*1024)throw new Error('oversized');
 const result=m.exports.compileEpisodeTimeline(JSON.parse(fs.readFileSync(input,'utf8')));
 process.stdout.write(JSON.stringify(result));
} catch { console.error('Episode manifest validation failed');process.exitCode=1; }
