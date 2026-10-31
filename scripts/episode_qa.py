"""Machine checks of actual encoded delivery; semantic/listening review remains human."""
import json
import math
from pathlib import Path
import re
import subprocess
from types import SimpleNamespace
from production_process import run_bounded


def command(args, timeout=120):
    try:
        return SimpleNamespace(**run_bounded(args,timeout=timeout))
    except subprocess.SubprocessError:
        raise ValueError('bounded media verification command failed') from None


def verify_delivery(filename, frames, width=1920, height=1080, require_audio=True, audio_ranges=None):
    filename=Path(filename).resolve(strict=True)
    if not filename.is_file() or filename.is_symlink(): raise ValueError('invalid delivery artifact')
    probe=json.loads(command(['ffprobe','-v','error','-protocol_whitelist','file',
       '-format_whitelist','mov,mp4,m4a,3gp,3g2,mj2','-show_entries',
       'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,duration,start_time',
       '-of','json',str(filename)],20).stdout)
    video=[s for s in probe['streams'] if s['codec_type']=='video']
    audio=[s for s in probe['streams'] if s['codec_type']=='audio']
    if len(video)!=1: raise ValueError('delivery requires one video stream')
    expected={'codec_name':'h264','width':width,'height':height,'r_frame_rate':'30/1','nb_frames':str(frames)}
    if any(video[0].get(k)!=v for k,v in expected.items()): raise ValueError('video stream violates delivery contract')
    if abs(float(probe['format']['duration'])-frames/30)>0.1: raise ValueError('delivery duration mismatch')
    if len(audio)>1 or (require_audio and not audio) or (audio and audio[0]['codec_name']!='aac'):
        raise ValueError('delivery audio stream missing or unsupported')
    if require_audio:
        try:
            audio_start=float(audio[0].get('start_time',0))
            audio_end=audio_start+float(audio[0]['duration'])
            required=audio_ranges or [(0,frames/30)]
            if not math.isfinite(audio_end) or any(a<audio_start-0.05 or b>audio_end+0.05 for a,b in required):
                raise ValueError('audio stream ends before expected narration')
        except (KeyError,TypeError):
            raise ValueError('unverifiable delivery audio duration') from None
    args=['ffmpeg','-hide_banner','-nostdin','-threads','2','-protocol_whitelist','file',
       '-i',str(filename),'-vf','blackdetect=d=0.15:pix_th=0.10:pic_th=0.98']
    if audio: args+=['-af','silencedetect=noise=-50dB:d=0.3,ebur128=peak=true,volumedetect']
    args+=['-f','null','-']
    log=command(args,300).stderr
    black=[float(s) for s in re.findall(r'black_duration:([0-9.]+)',log)]
    if any(d>=0.15 for d in black): raise ValueError('unreviewed black frames detected')
    levels={}
    if audio:
        for field,label in [('meanDb','mean_volume'),('maxDb','max_volume')]:
            match=re.search(label+r':\s*(-?[0-9.]+|-inf) dB',log)
            if not match: raise ValueError('audio level measurement missing')
            levels[field]=float(match.group(1))
        if require_audio and (not math.isfinite(levels['meanDb']) or levels['meanDb'] < -60 or levels['maxDb'] > -0.1):
            raise ValueError('audio is silent, too quiet or clipping')
        # ebur128 provides the integrated ITU-R BS.1770 loudness and the
        # oversampled true peak. Parse its final summary, not per-frame logs.
        summary = log.rsplit('Summary:', 1)[-1] if 'Summary:' in log else ''
        integrated = re.search(r'Integrated loudness:\\s*I:\\s*(-inf|-?[0-9]+(?:\\.[0-9]+)?)\\s+LUFS', summary)
        true_peak = re.search(r'True peak:\\s*Peak:\\s*(-inf|-?[0-9]+(?:\\.[0-9]+)?)\\s+dBFS', summary)
        if not integrated or not true_peak:
            raise ValueError('EBU R128 loudness or true-peak measurement missing')
        measured_lufs = float(integrated.group(1))
        measured_peak = float(true_peak.group(1))
        if require_audio and (not math.isfinite(measured_lufs) or
                              not math.isfinite(measured_peak)):
            raise ValueError('unmeasurable narration loudness')
        if require_audio and measured_peak > 0:
            raise ValueError('true peak exceeds digital full-scale')
        # None for silence keeps JSON QA records standards-compliant
        # (never persist Infinity/-Infinity as a JSON number).
        levels['integratedLufs'] = measured_lufs if math.isfinite(measured_lufs) else None
        levels['truePeakDbfs'] = measured_peak if math.isfinite(measured_peak) else None
        starts=[float(s) for s in re.findall(r'silence_start: ([0-9.]+)',log)]
        ends=[float(s) for s in re.findall(r'silence_end: ([0-9.]+)',log)]
        if len(ends)<len(starts): ends.append(frames/30)
        for start,end in zip(starts,ends):
            for a,b in audio_ranges or []:
                if min(end,b)-max(start,a)>0.35:
                    raise ValueError('unexpected silence inside a narration interval')
    return {'machineChecks':'passed','video':video[0],'audio':levels,
            'durationSeconds':float(probe['format']['duration']),
            'blackIntervals':len(black),'manualReviewRequired':True,
            'limitations':['Integrated LUFS and true-peak dBFS are measured, not normalized or mastered.',
                          'Semantic captions, speaker identity and audiovisual quality require manual review.']}
