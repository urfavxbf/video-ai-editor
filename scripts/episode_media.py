"""Import measured local WAVs and supplied reviewed timings; never generate speech/alignment."""
from array import array
import copy
import hashlib
import json
import math
from pathlib import Path
import sys
import time
import wave
from safe_media import local_media_path

PROJECT = Path(__file__).resolve().parents[1]
REGISTRY = PROJECT / 'characters/registry.json'


def digest(path, deadline=None):
    deadline=deadline if deadline is not None else time.monotonic()+30
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            if time.monotonic()>deadline: raise ValueError('media hash deadline exceeded')
            h.update(chunk)
    return h.hexdigest()


def bounded_integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('invalid integer range')
    return value


def wav_measurements(path, deadline=None):
    deadline=min(deadline if deadline is not None else math.inf,time.monotonic()+30)
    with wave.open(str(path), 'rb') as audio:
        if audio.getcomptype() != 'NONE' or audio.getsampwidth() != 2:
            raise ValueError('only uncompressed PCM16 WAV is supported')
        rate, channels, frames = audio.getframerate(), audio.getnchannels(), audio.getnframes()
        if not 8000 <= rate <= 96000 or channels not in (1,2) or not 0 < frames <= rate*3600:
            raise ValueError('unsupported WAV rate, channels or duration')
        square, peak, count = 0, 0, 0
        energies=[];active=[]
        while raw := audio.readframes(max(1,round(rate/10))):
            if time.monotonic()>deadline: raise ValueError('WAV analysis deadline exceeded')
            values = array('h', raw)
            if sys.byteorder != 'little': values.byteswap()
            start=count/(channels*rate)
            count += len(values)
            bucket_square=sum(int(v)*int(v) for v in values)
            square += bucket_square
            energy=math.sqrt(bucket_square/len(values))/32768
            energies.append(energy)
            if energy>0.003:
                end=count/(channels*rate)
                if active and abs(active[-1][1]-start)<0.000001: active[-1][1]=end
                else: active.append([start,end])
            peak = max(peak, max(abs(v) for v in values))
        if time.monotonic()>deadline: raise ValueError('WAV analysis deadline exceeded')
        if count != frames*channels:
            raise ValueError('truncated PCM WAV')
        rms = math.sqrt(square/count)/32768
        if rms < 0.00001:
            raise ValueError('narration WAV is silent')
        percentile=sorted(energies)[int((len(energies)-1)*0.95)]
        normalized=[round(min(1,e/max(percentile,0.0001)),3) for e in energies]
        return {'durationSeconds': frames/rate, 'durationFrames':(frames*30+rate-1)//rate,
                'sampleRate':rate,'channels':channels,
                'rms':rms,'peak':peak/32768,'activeRanges':active,'normalizedRms':normalized}


def reviewed_captions(alignment, sha256, seconds, offset):
    if not isinstance(alignment, dict) or set(alignment) != {'schemaVersion','audioSha256','source','reviewed','words'}:
        raise ValueError('invalid alignment contract')
    if alignment['schemaVersion'] != 1 or alignment['audioSha256'] != sha256 or alignment['reviewed'] is not True:
        raise ValueError('alignment must be reviewed and bound to the exact WAV hash')
    if alignment['source'] not in ('human-reviewed','forced-alignment'):
        raise ValueError('unrecognized alignment source')
    words = alignment['words']
    if not isinstance(words,list) or not 1 <= len(words) <= 3000:
        raise ValueError('alignment requires 1 to 3000 measured words')
    cues, previous = [], 0
    for word in words:
        if not isinstance(word,dict) or set(word) != {'start','end','text'}:
            raise ValueError('invalid word timing')
        start,end,text = word['start'],word['end'],word['text']
        if any(type(v) not in (int,float) or not math.isfinite(v) for v in (start,end)) or not previous <= start < end <= seconds:
            raise ValueError('word timing is outside the WAV or overlaps')
        if not isinstance(text,str) or not text.strip() or len(text)>60 or any(ord(c)<32 for c in text):
            raise ValueError('invalid caption text')
        start_frame,end_frame=offset+math.ceil(start*30-1e-8),offset+math.ceil(end*30-1e-8)
        if end_frame<=start_frame: raise ValueError('word timing is shorter than one display frame')
        cues.append({'startFrame':start_frame,'endFrame':end_frame,'text':text.strip()})
        previous=end
    # Group supplied adjacent words into readable cues; never derive timing from script.
    groups=[]
    for cue in cues:
        if groups and cue['startFrame']-groups[-1]['endFrame']<=15 and cue['endFrame']-groups[-1]['startFrame']<=75 and len(groups[-1]['text'])+len(cue['text'])+1<=60:
            groups[-1]['endFrame']=cue['endFrame'];groups[-1]['text']+=' '+cue['text']
        else: groups.append(dict(cue))
    return groups


def prepare_episode_media(manifest, clips, public_root, allow_fixtures=False):
    deadline=time.monotonic()+120
    if not isinstance(clips,list) or len(clips)>3000:
        raise ValueError('clips must contain at most 3000 WAVs')
    registry=json.loads(REGISTRY.read_text())
    result=copy.deepcopy(manifest)
    chapters={c['id']:c for c in result['chapters']}
    for chapter in chapters.values():
        if chapter.get('audio') or chapter.get('voiceEvents') or chapter.get('captions'):
            raise ValueError('production inputs need measured clip receipts; remove unverified manifest audio/events/captions')
        chapter['audio']=[];chapter['voiceEvents']=[]
    evidence=[];captions={};files={};measurements={}
    for clip in clips:
        if time.monotonic()>deadline: raise ValueError('episode media preparation deadline exceeded')
        required={'chapterId','speaker','file','startFrame','voiceProfile','sha256','provenance'}
        if not isinstance(clip,dict) or not required <= set(clip) or set(clip)-required-{'alignment'}:
            raise ValueError('invalid clip receipt')
        speaker=clip['speaker']
        if speaker not in registry['characters'] or clip['chapterId'] not in chapters:
            raise ValueError('unknown speaker or chapter')
        if clip['voiceProfile'] != registry['characters'][speaker]['english_voice']['identifier']:
            raise ValueError('voice profile differs from the approved English speaker')
        provenance=clip['provenance']
        if provenance not in ('owner-supplied-chatterbox','fixture-diagnostic') or (provenance=='fixture-diagnostic' and not allow_fixtures):
            raise ValueError('unapproved audio provenance; fixture mode requires explicit opt-in')
        if not isinstance(clip['file'],str) or not clip['file'].lower().endswith('.wav'):
            raise ValueError('episode narration must be a local WAV')
        path=local_media_path(public_root,clip['file'])
        sha=digest(path,deadline)
        if sha != clip['sha256']: raise ValueError('WAV receipt hash mismatch')
        if sha not in measurements: measurements[sha]=wav_measurements(path,deadline)
        measured=copy.deepcopy(measurements[sha])
        chapter=chapters[clip['chapterId']]
        start=bounded_integer(clip['startFrame'],0,chapter['durationFrames']-1)
        event={'speaker':speaker,'startFrame':start,
               'endFrame':start+measured['durationFrames'],
               'rms':measured.pop('normalizedRms'),'samplesPerSecond':10}
        if event['endFrame']>chapter['durationFrames']: raise ValueError('WAV exceeds chapter bounds')
        if any(e['speaker']==speaker and start<e['endFrame'] and e['startFrame']<event['endFrame'] for e in chapter['voiceEvents']):
            raise ValueError('overlapping same-speaker audio')
        target=f'voiceovers/{sha}.wav'
        files[target]=str(path)
        chapter['audio'].append({'file':target,'startFrame':start,'endFrame':event['endFrame']})
        chapter['voiceEvents'].append(event)
        if 'alignment' in clip:
            cues=reviewed_captions(clip['alignment'],sha,measured['durationSeconds'],start)
            captions.setdefault(chapter['id'],[]).extend(cues)
        evidence.append({'chapterId':chapter['id'],'speaker':speaker,'sha256':sha,
          'startFrame':start,
          'voiceProfile':clip['voiceProfile'],'provenance':provenance,
          'voiceIdentity':'diagnostic-nonspeech' if provenance=='fixture-diagnostic' else 'owner-declared-not-acoustically-verified',
          'alignment':'imported-reviewed' if 'alignment' in clip else 'not-provided',**measured})
    for chapter in chapters.values(): chapter['voiceEvents'].sort(key=lambda e:e['startFrame'])
    for cues in captions.values():
        cues.sort(key=lambda c:c['startFrame'])
        if any(a['endFrame']>b['startFrame'] for a,b in zip(cues,cues[1:])):
            raise ValueError('overlapping captions are unreadable')
    if time.monotonic()>deadline: raise ValueError('episode media preparation deadline exceeded')
    return {'manifest':result,'captions':captions,'evidence':evidence,'mediaFiles':files}
