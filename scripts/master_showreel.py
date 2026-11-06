#!/usr/bin/env python3
"""Two-pass offline loudness mastering; stream-copy the native rendered picture."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def read_loudnorm_json(stderr:str)->dict:
    start=stderr.rfind('{')
    if start<0:
        raise ValueError('FFmpeg did not produce loudnorm JSON')
    # FFmpeg can write mux progress after the filter's JSON report.
    return json.JSONDecoder().raw_decode(stderr[start:])[0]


def master(source:Path,output:Path)->dict:
    if not source.is_file():
        raise ValueError('Missing rendered showreel: '+str(source))
    if source.resolve()==output.resolve():
        raise ValueError('Mastering source and destination must differ')
    first=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-threads','2','-i',str(source),
        '-vn','-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'],
        text=True,capture_output=True,check=True,timeout=300)
    stats=read_loudnorm_json(first.stderr)
    effect=('loudnorm=I=-16:TP=-1.5:LRA=11:measured_I='+stats['input_i']+
            ':measured_TP='+stats['input_tp']+':measured_LRA='+stats['input_lra']+
            ':measured_thresh='+stats['input_thresh']+':offset='+stats['target_offset']+
            ':linear=true:print_format=json')
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=output.with_name('.'+output.stem+'-mastering.mp4')
    try:
        result=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-y','-threads','2','-i',str(source),
            '-map','0:v:0','-map','0:a:0','-c:v','copy','-af',effect,'-c:a','aac','-b:a','320k',
            '-ar','48000','-movflags','+faststart',str(temporary)],
            text=True,capture_output=True,check=True,timeout=300)
        measured=read_loudnorm_json(result.stderr)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    output.with_suffix('.mastering.json').write_text(json.dumps({'source':source.name,
        'targetLufs':-16,'targetTruePeakDbfs':-1.5,'analysis':stats,'master':measured},indent=2)+'\n')
    return measured

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'out/showreel/cinematic-showreel-unmastered.mp4')
    p.add_argument('--output',type=Path,default=ROOT/'out/showreel/cinematic-showreel.mp4')
    args=p.parse_args()
    try:
        result=master(args.source,args.output)
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print('Showreel mastering failed:',exc);return 2
    print('Audio mastered; picture stream copied unchanged:',json.dumps(result))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
