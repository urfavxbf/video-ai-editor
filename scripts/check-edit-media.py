"""Physical preflight invoked by `node scripts/validate-edit.cjs spec.json --media`."""
import json
from pathlib import Path
import sys
from safe_media import probe_local_media, stream_duration


def verify(spec, root):
    source = spec['source']
    probe = probe_local_media(root, source['video'])
    if source['frames'] > stream_duration(probe, 'video') * 30 + 0.01:
        raise ValueError('declared source exceeds measured duration')
    # Verify every referenced derivative frame. These are files, never URLs.
    for segment in spec['segments']:
        if segment['kind'] != 'fx':
            continue
        matte_effects = {'orbit','frame-escape','headline-storm','growth-curve','paper-cutout',
                         'magazine-cover','green-screen','frame-break','glass-widgets'}
        directories = ['matte'] if segment['id'] in matte_effects else []
        if segment['id'] == 'paper-cutout':
            directories.append('sticker')
        for directory in directories:
            for frame in range(segment['at'], segment['at'] + segment['frames']):
                relative = f"{source[directory]}/{frame:04d}.webp"
                # The same syntax/realpath boundary, with WebP allowed only here.
                candidate = Path(root) / relative
                if any(p.startswith('.') or not p for p in relative.split('/')) or candidate.is_symlink():
                    raise ValueError('invalid derivative path')
                resolved = candidate.resolve(strict=True)
                if not resolved.is_relative_to(Path(root).resolve()) or not resolved.is_file():
                    raise ValueError('missing local derivative frame')
    total = sum(s['frames'] for s in spec['segments'])
    for kind in ('music','narration'):
        if kind not in spec:
            continue
        audio = spec[kind]
        p = probe_local_media(root, audio['file'])
        if (audio.get('trimBefore', 0) + total) / 30 > stream_duration(p, 'audio') + 0.001:
            raise ValueError('audio trim/timeline exceeds measured duration')


if __name__ == '__main__':
    try:
        verify(json.loads(Path(sys.argv[1]).read_text()), Path(__file__).resolve().parents[1] / 'public')
        print('Verified whitelisted local edit media and measured bounds')
    except (ValueError, OSError, KeyError):
        sys.exit('Local media verification failed; no remote inputs were followed')
