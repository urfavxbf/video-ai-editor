const assert=require('node:assert/strict');
const fs=require('node:fs'); const path=require('node:path'); const Module=require('node:module');
const {test}=require('node:test'); const ts=require('typescript');
const file=path.resolve(__dirname,'../src/episodes/productionCaptions.ts');
const m=new Module(file,module);m.filename=file;m.paths=Module._nodeModulePaths(path.dirname(file));
m._compile(ts.transpileModule(fs.readFileSync(file,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,file);
const {validateProductionCaptions}=m.exports;
const chapters=[{id:'intro',durationFrames:60}];
test('accepts supplied bounded captions and rejects untrusted ranges/text/chapters',()=>{
 const okay={intro:[{startFrame:3,endFrame:18,text:'Measured words'}]};
 assert.deepEqual(validateProductionCaptions(okay,chapters),okay);
 for(const value of [{intro:[{startFrame:0,endFrame:61,text:'overrun'}]}, {intro:[{startFrame:0,endFrame:5,text:'x'.repeat(61)}]},
 {unknown:[]},{intro:[{startFrame:0,endFrame:10,text:'one'},{startFrame:9,endFrame:12,text:'two'}]},
 {intro:[{startFrame:NaN,endFrame:10,text:'bad'}]}]) assert.throws(()=>validateProductionCaptions(value,chapters));
});
