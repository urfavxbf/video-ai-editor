#!/usr/bin/env python3
"""Generate a Challenger Deep Tagalog documentary Short using shared voice pipeline.

The optional external WAV may come from standalone upstream VoxCPM2 on Colab/GPU.
Default CI voice uses Filipino Edge TTS (or gTTS), NOT VoxCPM2.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent.parent
VOICE=ROOT/'public'/'original'/'challenger'
OUTPUT=ROOT/'out'/'challenger-props.json'
SCRIPT=(
    "Paano kung bumaba ka sa pinakamalalim na bahagi ng karagatan? "
    "Sa unang dalawang daang metro, mabilis na kumukupas ang sikat ng araw. "
    "Paglampas ng isang kilometro, halos wala nang liwanag mula sa araw. "
    "At habang bumababa ka, tumitindi ang pressure. "
    "Bawat sampung metro, nadaragdagan ito ng halos isang atmosphere. "
    "Sa Challenger Deep, umaabot sa sampung libo siyam na raan tatlumpu't limang metro ang lalim. "
    "Higit isang libong beses ang pressure dito kumpara sa ibabaw. "
    "Hindi ito kakayanin ng ordinaryong submarino. "
    "Pero kahit sa matinding dilim at pressure, may mga organismong nabubuhay. "
    "At baka mas marami pang lihim ang karagatan kaysa sa iniisip natin."
)

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--external-wav',type=Path,default=None,
                        help='WAV produced by the independent official VoxCPM2 model')
    options=parser.parse_args()
    spec=importlib.util.spec_from_file_location('shared_speech',ROOT/'scripts'/'make-original-doorway.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Shared original Filipino narration pipeline unavailable')
    engine=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    engine.DIR=VOICE
    engine.DURATION_PATH=OUTPUT
    engine.SCRIPT=SCRIPT
    if options.external_wav is not None:
        wav=options.external_wav
        if not wav.is_file() or wav.suffix.lower()!='.wav':
            raise ValueError('VoxCPM2 import requires existing WAV audio')
        def external_voice() -> bool:
            subprocess.run(['ffmpeg','-nostdin','-y','-loglevel','error',
                            '-i',str(wav),'-c:a','libmp3lame','-q:a','2',
                            str(VOICE/'voiceover.mp3')],check=True,timeout=60)
            (VOICE/'voiceover.srt').unlink(missing_ok=True)
            return False
        engine.generate_voice=external_voice
        source='external-wav'
    else:
        source='filipino-edge-tts-or-gtts'
    engine.main()
    provenance={
        'narrationSource':source,
        'isVoxCPM2Verified':False,
        'note':'Standalone WAV provenance requires external verification; default CI uses Filipino fallback TTS.'
    }
    (ROOT/'out'/'challenger-source.json').write_text(
        json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Narration source:',source)
    print('Finished at:',OUTPUT)

if __name__=='__main__':
    main()
