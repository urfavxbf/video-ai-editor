"""Read-only signed-media URL audit. Output paths/counts only, never URL values."""
import json
import re
import subprocess

SIGNED = re.compile(rb'https?://[^\s"<>]+[?&](?:token|sig|signature|x-amz-signature|x-goog-signature|expires|se)=[^\s"<>]+', re.I)


def git(*args):
    return subprocess.check_output(['git', *args])


def audit():
    tracked = []
    for raw in git('ls-files', '-z').split(b'\0'):
        if not raw:
            continue
        name = raw.decode('utf8')
        try:
            with open(name, 'rb') as f:
                count = len(SIGNED.findall(f.read()))
        except OSError:
            continue
        if count:
            tracked.append({'path': name, 'occurrences': count})
    # Unique blob versions across all reachable refs; inspect content only in memory.
    objects = {}
    for line in git('rev-list', '--objects', '--all').splitlines():
        sha, _, name = line.partition(b' ')
        objects[sha.decode()] = name.decode('utf8', errors='replace')
    historical = []
    for sha, name in objects.items():
        if git('cat-file', '-t', sha).strip() != b'blob':
            continue
        if int(git('cat-file', '-s', sha)) > 4 * 1024 * 1024:
            continue  # Media/binary blobs excluded; report scope explicitly.
        count = len(SIGNED.findall(git('cat-file', 'blob', sha)))
        if count:
            historical.append({'path': name, 'blob': sha, 'occurrences': count})
    return {'tracked': tracked, 'reachable_blob_versions': historical,
            'scope': 'all fetched refs; blobs <=4MiB; heuristic signed-URL scan; deployments and token validity unverified'}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2))
