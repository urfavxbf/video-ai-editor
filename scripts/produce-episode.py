#!/usr/bin/env python3
"""Explicit, local-only episode production; imports approved inputs, never calls providers."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import sys
import time
from episode_pipeline import StageRunner, StageError, read_json, file_sha256, canonical_hash
from episode_media import prepare_episode_media, digest
from episode_qa import verify_delivery
from production_process import run_bounded
from safe_media import local_media_path

ROOT=Path(__file__).resolve().parents[1]


def run_cpu(args, timeout=60):
    return run_bounded(args,timeout=timeout,cwd=ROOT)['stdout']


def write_json(path, value):
    Path(path).write_text(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n')


def source_hashes():
    paths=[*ROOT.glob('src/**/*.ts'),*ROOT.glob('src/**/*.tsx'),*ROOT.glob('src/**/*.json'),
        ROOT/'package-lock.json',*ROOT.glob('scripts/episode_*.py'),ROOT/'scripts/produce-episode.py',
        ROOT/'scripts/compile-episode.cjs',ROOT/'scripts/render-episode.mjs',ROOT/'scripts/extract_voice_envelope.py',
        ROOT/'scripts/safe_media.py',ROOT/'scripts/production_process.py',ROOT/'characters/registry.json',ROOT/'characters/pixel-default-manifest.json']
    return {str(p.relative_to(ROOT)):file_sha256(p) for p in sorted(paths)}


def approved_assets():
    manifest=read_json(ROOT/'characters/pixel-default-manifest.json')
    assets={}
    for character in manifest['characters'].values():
        for pose in character['poses'].values():
            path=ROOT/pose['path']
            if file_sha256(path)!=pose['sha256']: raise ValueError('approved artwork hash mismatch')
            assets[str(path.relative_to(ROOT/'public'))]=file_sha256(path)
    for path in (ROOT/'public/fonts').glob('*'):
        if path.is_file(): assets[str(path.relative_to(ROOT/'public'))]=file_sha256(path)
    return assets


def produce(manifest_path, clips_path, media_root, work_dir, *, render=False, diagnostic=False):
    runner=StageRunner(work_dir)
    manifest=read_json(manifest_path,max_bytes=2*1024*1024)
    job=read_json(clips_path)
    if not isinstance(job,dict) or set(job)!={'schemaVersion','clips'} or job['schemaVersion']!=1:
        raise ValueError('invalid local production job')
    clips=job['clips']
    if not isinstance(clips,list) or len(clips)>3000: raise ValueError('invalid clip list')
    sources=source_hashes(); assets=approved_assets()
    media_hashes={};media_bytes=0;hash_deadline=time.monotonic()+120
    for clip in clips:
        if not isinstance(clip,dict) or 'file' not in clip: raise ValueError('invalid clip')
        if clip['file'] in media_hashes: continue
        path=local_media_path(media_root,clip['file'])
        media_bytes+=path.stat().st_size
        if media_bytes>2*1024**3: raise ValueError('episode WAV inputs exceed 2 GiB')
        media_hashes[clip['file']]=digest(path,hash_deadline)
    def compile_action(temp):
        write_json(temp/'manifest.json',manifest)
        compiled=json.loads(run_cpu(['node','scripts/compile-episode.cjs',str(temp/'manifest.json')]))
        write_json(temp/'compiled.json',compiled)
        write_json(temp/'provenance.json',{'schemaVersion':1,'sourceHashes':sources,
            'manifestHash':canonical_hash(manifest)})
        return {'durationFrames':compiled['durationFrames']}
    compiled=runner.run('manifest','1',{'manifest':manifest,'code':sources},compile_action)
    valid=read_json(Path(compiled['directory'])/'compiled.json')['manifest']
    def prepare_action(temp):
        result=prepare_episode_media(valid,clips,media_root,allow_fixtures=diagnostic)
        for relative,source in result.pop('mediaFiles').items():
            target=temp/'public'/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
            if file_sha256(target)!=Path(relative).stem: raise ValueError('media changed during preparation')
        for relative,sha in assets.items():
            target=temp/'public'/relative;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/'public'/relative,target)
            if file_sha256(target)!=sha: raise ValueError('artwork changed during preparation')
        props={'manifest':result['manifest'],'captions':result['captions']}
        write_json(temp/'props.json',props);write_json(temp/'evidence.json',result['evidence'])
        write_json(temp/'provenance.json',{'schemaVersion':1,'assetHashes':assets,
            'mediaHashes':media_hashes,'clipReceiptsHash':canonical_hash(clips),
            'manifestStage':compiled['resultHash']})
        # Revalidate the compiled media event ranges via the same TS contract.
        write_json(temp/'manifest.json',props['manifest'])
        run_cpu(['node','scripts/compile-episode.cjs',str(temp/'manifest.json')])
        return {'clips':len(clips),'voiceGeneration':'not-run','alignmentGeneration':'not-run',
                'manualReviewRequired':True,'diagnostic':diagnostic}
    prepared=runner.run('media','1',{'compiled':compiled['resultHash'],'clips':clips,
        'media':media_hashes,'assets':assets,'code':sources,'diagnostic':diagnostic},prepare_action)
    summary={'manifest':compiled,'media':prepared,'render':'not-requested'}
    if not render: return summary
    # 600 seconds is a hard CPU wall-clock limit; long episodes require explicit future scheduling.
    scale=0.25 if diagnostic else 1
    def render_action(temp):
        run_cpu(['node','scripts/render-episode.mjs',str(Path(prepared['directory'])/'props.json'),
            str(Path(prepared['directory'])/'public'),str(temp/'episode.mp4'),str(scale)],600)
        write_json(temp/'provenance.json',{'schemaVersion':1,'toolchain':toolchain,
            'mediaStage':prepared['resultHash'],'sourceHashes':sources})
        return {'scale':scale,'width':int(1920*scale),'height':int(1080*scale),'fps':30,
                'diagnostic':diagnostic,'published':False}
    browser=os.environ.get('REMOTION_BROWSER_EXECUTABLE')
    browser_version=run_cpu([browser,'--version']).strip() if browser else 'managed-chrome-pinned-by-remotion-lock'
    toolchain={'node':run_cpu(['node','--version']).strip(),
        'ffmpeg':run_cpu(['ffmpeg','-version']).splitlines()[0],
        'browser':browser or 'managed-chrome','browserVersion':browser_version}
    rendered=runner.run('render','1',{'prepared':prepared['resultHash'],'code':sources,
        'toolchain':toolchain,'scale':scale},render_action)
    props=read_json(Path(prepared['directory'])/'props.json')
    evidence=read_json(Path(prepared['directory'])/'evidence.json')
    chapters={c['id']:c for c in props['manifest']['chapters']}
    ranges=[((chapters[e['chapterId']]['startFrame']+e['startFrame'])/30+a,
             (chapters[e['chapterId']]['startFrame']+e['startFrame'])/30+b)
            for e in evidence for a,b in e['activeRanges']]
    def qa_action(temp):
        report=verify_delivery(Path(rendered['directory'])/'episode.mp4',compiled['payload']['durationFrames'],
            int(1920*scale),int(1080*scale),bool(clips),ranges)
        report['diagnostic']=diagnostic
        report['audioIdentity']='diagnostic-nonspeech' if diagnostic else 'owner-declaration-requires-listening-review'
        report['captions']='imported-reviewed-timings' if props['captions'] else 'not-provided'
        write_json(temp/'qa.json',report)
        return {'machineChecks':'passed','manualReviewRequired':True,'diagnostic':diagnostic}
    qa=runner.run('qa','1',{'render':rendered['resultHash'],'media':prepared['resultHash'],'code':sources},qa_action)
    return {**summary,'render':rendered,'qa':qa}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,required=True);p.add_argument('--clips',type=Path,required=True)
    p.add_argument('--media-root',type=Path,default=ROOT/'public');p.add_argument('--work-dir',type=Path,required=True)
    p.add_argument('--render',action='store_true');p.add_argument('--diagnostic',action='store_true',
        help='Explicit nonspeech fixtures; quarter-scale output, never production delivery')
    args=p.parse_args()
    try:
        result=produce(args.manifest,args.clips,args.media_root,args.work_dir,render=args.render,diagnostic=args.diagnostic)
        print(json.dumps({name:({'cached':s['cached'],'directory':s['directory'],'resultHash':s['resultHash']}
            if isinstance(s,dict) else s) for name,s in result.items()},indent=2))
    except KeyboardInterrupt:
        return 130
    except StageError as exc:
        print(json.dumps(exc.error),file=sys.stderr);return 1
    except (ValueError,OSError,KeyError,TypeError):
        print('Production input/preflight failed; no providers called',file=sys.stderr);return 1
    return 0

if __name__=='__main__': raise SystemExit(main())
