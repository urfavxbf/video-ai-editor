import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import os
import signal
import time
import test_episode_media

SCRIPTS=Path(__file__).parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('produce_episode',SCRIPTS/'produce-episode.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class EpisodeProductionTests(unittest.TestCase):
 def test_preparation_resume_and_corrupt_wav_recovery(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);media=root/'inputs';media.mkdir()
   manifest,clip=test_episode_media.EpisodeMediaTests().fixture(media)
   mp=root/'manifest.json';cp=root/'clips.json'
   mp.write_text(json.dumps(manifest));cp.write_text(json.dumps({'schemaVersion':1,'clips':[clip]}))
   first=m.produce(mp,cp,media,root/'run',diagnostic=True)
   second=m.produce(mp,cp,media,root/'run',diagnostic=True)
   self.assertTrue(second['manifest']['cached']);self.assertTrue(second['media']['cached'])
   stage=Path(first['media']['directory'])
   wav=next((stage/'public/voiceovers').glob('*.wav'));wav.write_bytes(b'corrupt')
   third=m.produce(mp,cp,media,root/'run',diagnostic=True)
   self.assertFalse(third['media']['cached'])
   self.assertEqual(first['media']['resultHash'],third['media']['resultHash'])
   self.assertGreater(wav.stat().st_size,44)
   self.assertEqual(third['render'],'not-requested')

 def test_cpu_command_deadline_kills_job(self):
  with self.assertRaises(subprocess.TimeoutExpired):
   m.run_cpu([sys.executable,'-c','import time; time.sleep(10)'],timeout=0.1)

 def test_deadline_kills_sigterm_resistant_descendant_after_leader_exits(self):
  with tempfile.TemporaryDirectory() as tmp:
   pidfile=Path(tmp)/'pid'
   child="import os,signal,time;from pathlib import Path;signal.signal(signal.SIGTERM,signal.SIG_IGN);Path("+repr(str(pidfile))+").write_text(str(os.getpid()));time.sleep(30)"
   leader="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(child)+"],start_new_session=True);time.sleep(30)"
   try:
    with self.assertRaises(subprocess.TimeoutExpired):m.run_cpu([sys.executable,'-c',leader],timeout=0.6)
    self.assertTrue(pidfile.exists())
    pid=int(pidfile.read_text())
    for _ in range(20):
     status=Path(f'/proc/{pid}/stat')
     if not status.exists() or status.read_text().split()[2]=='Z':break
     time.sleep(0.01)
    self.assertTrue(not status.exists() or status.read_text().split()[2]=='Z')
   finally:
    if pidfile.exists():
     try:os.kill(int(pidfile.read_text()),signal.SIGKILL)
     except ProcessLookupError:pass

 def test_log_limit_stops_a_running_command(self):
  start=time.monotonic()
  with self.assertRaises(ValueError):
   m.run_cpu([sys.executable,'-c',"import sys,time;sys.stdout.write('x'*3000000);sys.stdout.flush();time.sleep(10)"],timeout=15)
  self.assertLess(time.monotonic()-start,5)

 def test_successful_fast_leader_cannot_orphan_a_detached_child(self):
  with tempfile.TemporaryDirectory() as tmp:
   pidfile=Path(tmp)/'pid'
   child="import os,signal,time;from pathlib import Path;signal.signal(signal.SIGTERM,signal.SIG_IGN);Path("+repr(str(pidfile))+").write_text(str(os.getpid()));time.sleep(30)"
   leader="import subprocess,sys,time;from pathlib import Path;subprocess.Popen([sys.executable,'-c',"+repr(child)+"],start_new_session=True)\nwhile not Path("+repr(str(pidfile))+").exists(): time.sleep(.001)"
   try:
    m.run_cpu([sys.executable,'-c',leader],timeout=3)
    pid=int(pidfile.read_text());status=Path(f'/proc/{pid}/stat')
    self.assertTrue(not status.exists() or status.read_text().split()[2]=='Z')
   finally:
    if pidfile.exists():
     try:os.kill(int(pidfile.read_text()),signal.SIGKILL)
     except ProcessLookupError:pass
