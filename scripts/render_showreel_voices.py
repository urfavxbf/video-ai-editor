#!/usr/bin/env python3
"""Generate selected Jasper/Kiki Kitten Mini lines locally on CPU; verify resume receipts."""
import argparse,json,subprocess,sys
from pathlib import Path
from prepare_showreel import ROOT,voice_request,validate_receipt,digest,load_voice

def same_python_environment(selected:str,active:str)->bool:
    # Venv executables can be symlinks to the same base binary: do not resolve them.
    return Path(selected).absolute()==Path(active).absolute()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python',default=sys.executable)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'input/showreel-voices-kitten')
    parser.add_argument('--model-dir',type=Path,default=ROOT/'input/kitten-tts-mini-0.8')
    args=parser.parse_args()
    if not same_python_environment(args.python,sys.executable):
        return subprocess.call([args.python,__file__,'--model-dir',str(args.model_dir),'--output-dir',str(args.output_dir)],cwd=ROOT)
    from kitten_showreel_voice import stage_model,load_model,generate
    stage_model(args.model_dir)
    script=json.loads((ROOT/'src/showcase/showreel-script.json').read_text())
    destination=args.output_dir;destination.mkdir(parents=True,exist_ok=True)
    model=None
    for line in script:
        path=destination/(line['name']+'.wav')
        if path.exists():
            validate_receipt(path,line);load_voice(path,line['maxFrames'])
            print('Reusing verified Kitten WAV:',path.name,flush=True);continue
        if model is None:model=load_model(args.model_dir)
        generate(model,line['text'],line['character'],path)
        load_voice(path,line['maxFrames'])
        path.with_suffix('.voice.json').write_text(json.dumps({'request':voice_request(line),'sha256':digest(path)},indent=2)+'\n')
        print('Generated',line['character'],voice_request(line)['voice'],path.name,flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
