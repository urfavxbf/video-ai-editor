"""Probe the actual silent, two-chapter CI proof; never call this delivery QA."""
import json
import subprocess
import sys


def verify(filename):
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', filename,
    ], check=True, capture_output=True, text=True, timeout=20)
    probe = json.loads(result.stdout)
    assert len(probe['streams']) == 1, 'Silent fixture must have exactly one stream'
    stream = probe['streams'][0]
    for key, expected in dict(codec_name='h264', width=480, height=270,
                              r_frame_rate='30/1', nb_frames='120').items():
        assert stream.get(key) == expected, f'Unexpected {key}'
    assert abs(float(probe['format']['duration']) - 4) < 0.04, 'Expected four seconds'
    # Isolate the static title; breathing animation must not pass this cut check.
    frames = subprocess.run([
        'ffmpeg', '-v', 'error', '-i', filename, '-vf',
        'select=between(n\\,58\\,61),crop=176:58:152:50', '-fps_mode', 'passthrough',
        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-',
    ], check=True, capture_output=True, timeout=30).stdout
    size = 176 * 58 * 3
    assert len(frames) == size * 4, 'Could not decode chapter boundary'
    crops = [frames[i*size:(i+1)*size] for i in range(4)]
    deltas = [sum(abs(x-y) for x, y in zip(a, b)) / size
              for a, b in zip(crops, crops[1:])]
    assert deltas[0] < 2 and deltas[2] < 2, 'Title changes inside chapter'
    assert deltas[1] > 5, 'Missing chapter title cut at frame 60'
    assert all(sum(frame) / size > 5 for frame in crops), 'Black chapter title'
    print('Verified silent H.264 episode proof: 120 frames, 480x270, 30fps; decoded chapter cut')


if __name__ == '__main__':
    verify(sys.argv[1])
