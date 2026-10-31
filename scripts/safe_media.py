"""Bounded, offline media probes. The allowlist is public/ production media only."""
import json
import math
from pathlib import Path
import re
import subprocess

MEDIA_DIRS = {'sample', 'takes', 'voiceovers', 'audio', 'music'}
MEDIA_EXTENSIONS = {'.wav', '.mp3', '.m4a', '.aac', '.ogg', '.mp4', '.mov', '.webm'}


def stream_duration(probe, kind):
    """Never infer video/audio length from a longer sibling stream."""
    stream = next((s for s in probe['streams'] if s.get('codec_type') == kind), None)
    if stream is None:
        raise ValueError(f'missing {kind} stream')
    try:
        seconds = float(stream['duration'])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f'unverifiable {kind} stream duration') from None
    if not math.isfinite(seconds) or not 0 < seconds <= 3600:
        raise ValueError(f'invalid {kind} stream duration')
    return seconds


def local_media_path(root, relative):
    if not isinstance(relative, str) or len(relative) > 240 or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_./-]*', relative):
        raise ValueError('invalid local media path')
    parts = relative.split('/')
    if parts[0] not in MEDIA_DIRS or any(not p or p.startswith('.') for p in parts):
        raise ValueError('media path is outside the allowlist')
    base = Path(root).resolve(strict=True)
    candidate = base
    for part in parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError('symlink media paths are not allowed')
    try:
        resolved = candidate.resolve(strict=True)
    except OSError:
        raise ValueError('local media is missing') from None
    if not resolved.is_relative_to(base) or not resolved.is_file() or resolved.suffix.lower() not in MEDIA_EXTENSIONS:
        raise ValueError('unsupported local media file')
    if not 0 < resolved.stat().st_size <= 2 * 1024**3:
        raise ValueError('media size must be between 1 byte and 2 GiB')
    return resolved


def probe_local_media(root, relative):
    filename = local_media_path(root, relative)
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-protocol_whitelist', 'file',
            '-format_whitelist', 'mov,mp4,m4a,3gp,3g2,mj2,matroska,webm,wav,mp3,aac,ogg',
            '-probesize', '5000000', '-analyzeduration', '5000000',
            '-show_entries', 'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,duration,sample_rate,channels',
            '-of', 'json', str(filename),
        ], capture_output=True, text=True, check=True, timeout=15)
        if len(result.stdout) > 1024 * 1024:
            raise ValueError('oversized probe response')
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        if not 0 < duration <= 3600:
            raise ValueError('duration must be positive and at most one hour')
        return {'duration': duration, 'streams': data['streams']}
    except (subprocess.SubprocessError, KeyError, TypeError, json.JSONDecodeError):
        # Never echo stderr: malicious container metadata can include secrets/URLs.
        raise ValueError('local media probe failed') from None
