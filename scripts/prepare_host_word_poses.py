#!/usr/bin/env python3
"""Prepare the owner-sheet performance from measured local word alignment."""
import hashlib,json,math,re,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RATE=24000

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def art_manifest():
    data=json.loads((ROOT/'characters/urfavxbf-8bit-manifest.json').read_text())
    if digest(ROOT/data['source'])!=data['sourceSha256']:raise ValueError('Owner artwork hash mismatch')
    return data

def normalize(text):return re.sub(r"[^a-z']",'',text.lower())

def align_words(row,asr,offset):
    words=row['text'].split();poses=row['poses'];known=art_manifest()['poses']
    if len(words)!=len(asr) or len(words)!=len(poses):raise ValueError('Word/pose/alignment count mismatch')
    previous_end=0;previous_pose=None;result=[]
    for word,pose,item in zip(words,poses,asr):
        start,end=item['start'],item['end']
        if normalize(word)!=normalize(item['text']):raise ValueError('Transcription mismatch: '+word)
        if pose not in known or pose==previous_pose:raise ValueError('Unknown or repeated pose: '+pose)
        if not math.isfinite(start+end) or start<previous_end-.001 or end-start<1/30:raise ValueError('Invalid word bounds: '+word)
        result.append({'text':word,'startMs':round((offset+start)*1000,2),'endMs':round((offset+end)*1000,2),'timestampMs':None,'confidence':item.get('probability'),'pose':pose})
        previous_end=end;previous_pose=pose
    return result

def host_voice_request(profile=None):
    if profile is None:profile=json.loads((ROOT/'src/showcase/showreel-voices.json').read_text())
    if profile['voices']['urfavxbf']!='Jasper':raise ValueError('This owner-requested performance requires Jasper')
    return {key:profile[key] for key in ('engine','model','modelRevision','sdkCommit','speed','sampleRate')}|{'voice':'Jasper'}

def validate_schedule(words,duration_frames,require_all=True):
    known=set(art_manifest()['poses'])
    for i,word in enumerate(words):
        at=math.floor(word['startMs']*30/1000+.5)
        next_at=math.floor(words[i+1]['startMs']*30/1000+.5) if i+1<len(words) else duration_frames
        if next_at-at<4:raise ValueError('Each word requires four frames to survive its glitch')
        if word['pose'] not in known or (i and word['pose']==words[i-1]['pose']):raise ValueError('Unknown or repeated pose')
        if not 0<=word['startMs']<word['endMs']<=duration_frames/30*1000:raise ValueError('Word outside performance')
    if require_all and set(w['pose'] for w in words)!=known:raise ValueError('Not all nine poses are used')

def check_current(data=None):
    if data is None:data=json.loads((ROOT/'src/characters/word-poses/performance.json').read_text())
    if not data.get('ready'):raise ValueError('Missing prepared narration')
    if data.get('scriptSha256')!=digest(ROOT/'src/characters/word-poses/script.json'):raise ValueError('Stale performance: script changed')
    if data.get('generationRequest')!=host_voice_request():raise ValueError('Stale voice request')
    for name,key in [('alignment','alignmentSha256'),('generation','generationSha256')]:
        if data.get(key)!=digest(ROOT/f'input/host-word-poses/{name}.json'):raise ValueError('Stale '+name)
    receipts=json.loads((ROOT/'input/host-word-poses/generation.json').read_text())
    for i,receipt in enumerate(receipts):
        if receipt['sha256']!=digest(ROOT/f'input/host-word-poses/line-{i}.wav'):raise ValueError('Changed raw narration')
    if digest(ROOT/'public'/data['audio'])!=data['audioSha256']:raise ValueError('Changed assembled narration')
    art_manifest();validate_schedule(data['words'],data['durationFrames'])
    print('Host word poses: source art, script, Jasper receipts, WAV and four-frame word holds verified')

def prepare():
    import numpy as np
    rows=json.loads((ROOT/'src/characters/word-poses/script.json').read_text())
    alignment=json.loads((ROOT/'input/host-word-poses/alignment.json').read_text())
    generation=json.loads((ROOT/'input/host-word-poses/generation.json').read_text())
    request=host_voice_request()
    if len(generation)!=len(rows):raise ValueError('Missing generation receipts')
    if len(alignment['lines'])!=len(rows):raise ValueError('Missing aligned phrases')
    samples=[np.zeros(round(.6*RATE),dtype='<i2')];words=[];phrases=[];offset=.6
    for i,(row,line) in enumerate(zip(rows,alignment['lines'])):
        path=ROOT/f'input/host-word-poses/line-{i}.wav'
        if generation[i]!={'text':row['text'],'generationRequest':request,'sha256':digest(path)}:raise ValueError('Stale Jasper generation receipt')
        if line['sha256']!=digest(path):raise ValueError('Alignment belongs to a different WAV')
        with wave.open(str(path)) as source:
            if (source.getnchannels(),source.getsampwidth(),source.getframerate())!=(1,2,RATE):raise ValueError('Expected mono PCM16 24kHz')
            pcm=np.frombuffer(source.readframes(source.getnframes()),dtype='<i2').copy()
        duration=len(pcm)/RATE
        linewords=align_words(row,line['words'],offset)
        if line['words'][-1]['end']>duration:raise ValueError('Word outside real audio')
        if words and words[-1]['pose']==linewords[0]['pose']:raise ValueError('Repeated pose at phrase boundary')
        words.extend(linewords);phrases.append({'text':row['text'],'startMs':linewords[0]['startMs'],'endMs':linewords[-1]['endMs'],'wordStart':len(words)-len(linewords),'wordCount':len(linewords)})
        samples.extend([pcm,np.zeros(round(.26*RATE),dtype='<i2')]);offset+=duration+.26
    samples.append(np.zeros(RATE,dtype='<i2'))
    audio=np.concatenate(samples).astype(np.float64)
    if not np.max(np.abs(audio)):raise ValueError('Silent narration')
    audio=(audio/np.max(np.abs(audio))*.72*32767).astype('<i2')
    output=ROOT/'public/voiceovers/host-word-poses';output.mkdir(parents=True,exist_ok=True)
    path=output/'jasper.wav'
    with wave.open(str(path),'wb') as f:f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(audio.tobytes())
    manifest={'ready':True,'scriptSha256':digest(ROOT/'src/characters/word-poses/script.json'),'generationRequest':request,'alignmentSha256':digest(ROOT/'input/host-word-poses/alignment.json'),'generationSha256':digest(ROOT/'input/host-word-poses/generation.json'),'audio':'voiceovers/host-word-poses/jasper.wav','audioSha256':digest(path),'voice':'Kitten Mini 0.8 Jasper','alignment':alignment['method'],'review':'Local ASR transcript matched; local CTC alignment estimates, no human listening sign-off','fps':30,'durationFrames':math.ceil(len(audio)/RATE*30),'words':words,'phrases':phrases}
    validate_schedule(words,manifest['durationFrames'])
    (ROOT/'src/characters/word-poses/performance.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'words':len(words),'durationSeconds':len(audio)/RATE,'poses':len(set(w['pose'] for w in words))}))

if __name__=='__main__':
    import sys
    check_current() if '--check' in sys.argv else prepare()
