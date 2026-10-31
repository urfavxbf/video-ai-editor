// Reuse the actual pure TypeScript contract, with the installed compiler.
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const ts = require('typescript');
const {spawnSync} = require('node:child_process');
const filename = path.resolve(__dirname, '../src/compositionMetadata.ts');
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = Module._nodeModulePaths(path.dirname(filename));
loaded._compile(ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022},
}).outputText, filename);
try {
  const input = process.argv[2] ?? 'src/edit/edit.json';
  if (fs.statSync(input).size > 2 * 1024 * 1024) throw new Error('edit JSON exceeds 2 MiB');
  const spec = JSON.parse(fs.readFileSync(input, 'utf8'));
  const frames = loaded.exports.editDuration(spec);
  if (process.argv.includes('--media')) {
    const result = spawnSync('python3', [path.join(__dirname, 'check-edit-media.py'), input], {stdio:'inherit',timeout:120000});
    if (result.error || result.status !== 0) throw new Error('local media preflight failed');
  }
  console.log(`Valid edit contract: ${frames} frames`);
} catch (error) {
  // Syntax errors may include input excerpts. Only contract errors are safe to print.
  console.error(error.message.startsWith('ExampleEdit') ? error.message : 'Edit validation failed; check local JSON/media');
  process.exitCode = 1;
}
