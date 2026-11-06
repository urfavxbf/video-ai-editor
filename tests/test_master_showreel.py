import importlib.util
from pathlib import Path
import unittest

FILE=Path(__file__).resolve().parents[1]/'scripts/master_showreel.py'
spec=importlib.util.spec_from_file_location('master_showreel',FILE)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class MasteringTests(unittest.TestCase):
    def test_reads_ffmpeg_json_with_trailing_mux_progress(self):
        self.assertTrue(hasattr(m,'read_loudnorm_json'),'missing bounded FFmpeg report parser')
        report='[Parsed_loudnorm_0] \n{\n "input_i":"-22.1",\n "input_tp":"-4.3"\n}\nsize= 58901kB time=00:01:22.00 bitrate=5884.4kbits/s\n'
        self.assertEqual(m.read_loudnorm_json(report),{'input_i':'-22.1','input_tp':'-4.3'})
    def test_missing_report_fails_clearly(self):
        self.assertTrue(hasattr(m,'read_loudnorm_json'),'missing bounded FFmpeg report parser')
        with self.assertRaisesRegex(ValueError,'loudnorm JSON'):
            m.read_loudnorm_json('ffmpeg exited before producing statistics')

if __name__=='__main__':unittest.main()
