#!/usr/bin/env python3
"""Render actual Chatterbox V3 WAV per speaker turn for ghost-town episode."""
import argparse
import json
from pathlib import Path
import sys
import torch
import torchaudio

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX
from check_chatterbox_v3 import require_v3_loader

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--speaker",required=True,choices=["urfavxbf","pix"])
    ap.add_argument("--script",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    data=json.loads(a.script.read_text(encoding="utf-8"))
    turns=[t for t in data["turns"] if t["speaker"]==a.speaker]
    if not turns: raise ValueError("No turns for speaker")
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    require_v3_loader(ChatterboxMultilingualTTS.from_pretrained)
    torch.set_num_threads(min(4,torch.get_num_threads()))
    model=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3")
    profile=DEFAULT_PIX if a.speaker=="pix" else DEFAULT_NARRATOR
    kw={"language_id":"en","exaggeration":profile.exaggeration,"cfg_weight":profile.cfg_weight}
    if a.speaker=="pix":
        from prepare_pix_reference import prepare
        reference=prepare(Path("input/pix-reference.wav"))
        kw["audio_prompt_path"]=str(reference)
    out=a.out/a.speaker
    out.mkdir(parents=True,exist_ok=True)
    manifest={"engine":"Chatterbox Multilingual V3","speaker":a.speaker,"profile":profile.identifier,"files":[]}
    for t in turns:
        text=t["text"].strip()
        if len(text)>700 or not text: raise ValueError("Turn invalid")
        print(f"RENDER {t['id']} {len(text)} chars",flush=True)
        audio=model.generate(text,**kw).detach().cpu()
        if audio.ndim==1: audio=audio.unsqueeze(0)
        if audio.ndim!=2 or audio.shape[1] < model.sr//3: raise RuntimeError("Bad waveform")
        path=out/(t["id"]+".wav")
        torchaudio.save(str(path),audio,model.sr,encoding="PCM_S",bits_per_sample=16)
        manifest["files"].append({"id":t["id"],"file":path.name,"duration":round(audio.shape[1]/model.sr,3),"text":text})
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"COMPLETE {len(turns)} turns",flush=True)
if __name__=="__main__":
    main()
