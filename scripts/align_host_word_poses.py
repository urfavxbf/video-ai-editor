import json,re,wave,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ['TORCH_HOME']=str(Path('input/host-word-poses/torch-cache').resolve())
import torch,torchaudio
import numpy as np
from scipy.signal import resample_poly
torch.set_num_threads(2)
bundle=torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model=bundle.get_model();model.eval();labels=bundle.get_labels();dictionary={c:i for i,c in enumerate(labels)}
# Independently recognize PCM before forcing the authored transcript.
from faster_whisper import WhisperModel
whisper=WhisperModel(str(next(Path('input/whisper-tiny-en').rglob('model.bin')).parent),device='cpu',compute_type='int8',cpu_threads=2)
result=[]
for i,row in enumerate(json.loads(Path('src/characters/word-poses/script.json').read_text())):
    with wave.open(f'input/host-word-poses/line-{i}.wav') as f:
        pcm=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
    pcm=resample_poly(pcm,2,3)
    segments,_=whisper.transcribe(pcm,language='en',beam_size=5,condition_on_previous_text=False,initial_prompt=row['text'])
    recognized=' '.join(segment.text for segment in segments)
    normalize=lambda text:re.sub("[^a-z']",'',text.lower())
    if normalize(recognized)!=normalize(row['text']):raise ValueError('Local recognition mismatch: '+recognized)
    words=[re.sub("[^A-Z']",'',w.upper()) for w in row['text'].split()]
    text='|'.join(words)
    targets=torch.tensor([[dictionary[c] for c in text]],dtype=torch.int32)
    with torch.inference_mode():emissions,_=model(torch.from_numpy(pcm).unsqueeze(0));emissions=torch.log_softmax(emissions,dim=-1)
    aligned,scores=torchaudio.functional.forced_align(emissions,targets,blank=0)
    spans=torchaudio.functional.merge_tokens(aligned[0],scores[0].exp())
    ratio=len(pcm)/16000/emissions.shape[1]
    chunks=[];chunk=[]
    for span in spans:
        if labels[span.token]=='|':
            chunks.append(chunk);chunk=[]
        else:chunk.append(span)
    chunks.append(chunk)
    assert len(chunks)==len(words),(len(chunks),len(words))
    rowwords=[]
    for word,chunk in zip(row['text'].split(),chunks):
        rowwords.append({'text':word,'start':round(chunk[0].start*ratio,4),'end':round(chunk[-1].end*ratio,4),'probability':round(sum(s.score for s in chunk)/len(chunk),4)})
    result.append(rowwords);print(i,rowwords,flush=True)
import hashlib
receipt={'method':'Local wav2vec2 ASR BASE 960h CTC forced alignment; transcript cross-checked by local Whisper tiny.en','lines':[{'sha256':hashlib.sha256(Path(f"input/host-word-poses/line-{i}.wav").read_bytes()).hexdigest(),'words':words} for i,words in enumerate(result)]}
Path('input/host-word-poses/alignment.json').write_text(json.dumps(receipt,indent=2)+'\n')
