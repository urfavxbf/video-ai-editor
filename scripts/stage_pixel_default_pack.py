"""Verify/stage current owner-sheet host and retained PIX image assets, without redrawing."""
from __future__ import annotations
import hashlib,json,sys,zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
COUNTS={'urfavxbf':9,'pix':7}

def manifest(root=ROOT):
    m=json.loads((Path(root)/'characters/pixel-default-manifest.json').read_text())
    if set(m['characters'])!=set(COUNTS):raise ValueError('Unexpected character identities')
    for who,count in COUNTS.items():
        if len(m['characters'][who]['poses'])!=count:raise ValueError('Incomplete pose manifest for '+who)
    return m

def check(path,raw,item):
    allowed=path=='public/characters/urfavxbf-8bit/owner-sheet.jpg' or path.startswith('public/characters/pixel-default/pix/')
    if path!=item['path'] or not allowed:raise ValueError('Unsafe image path')
    if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:raise ValueError('SHA-256 mismatch for '+path)
    if len(raw)>4_000_000:raise ValueError('Oversized image')
    im=Image.open(BytesIO(raw));im.load()
    if im.size!=(item['width'],item['height']):raise ValueError('Unexpected image dimensions')
    if item.get('kind')=='owner-jpeg-viewport':
        if im.format!='JPEG':raise ValueError('Expected exact owner JPEG')
        x,y,w,h=item['rect']
        if not (0<=x<x+w<=im.width and 0<=y<y+h<=im.height):raise ValueError('Unsafe pose viewport')
    elif im.mode!='RGBA' or im.size!=(1254,1254) or im.getchannel('A').getextrema()!=(0,255) or im.getpixel((0,0))[3]!=0:
        raise ValueError('Expected original transparent PIX PNG')

def verified_archive(zip_path,root=ROOT):
    verified={}
    with zipfile.ZipFile(zip_path) as z:
        for desc in manifest(root)['characters'].values():
            for item in desc['poses'].values():
                path=item['path'];info=z.getinfo(path)
                if info.file_size>4_000_000:raise ValueError('Oversized image '+path)
                raw=z.read(info);check(path,raw,item);verified[path]=raw
    if len(verified)!=8:raise ValueError('Expected 8 current physical image assets')
    return verified

def stage(zip_path,root=ROOT):
    verified=verified_archive(zip_path,root)
    for path in verified:
        if (Path(root)/path).exists():raise FileExistsError(path)
    for path,raw in verified.items():
        p=Path(root)/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    return len(verified)

def verify_workspace(root=ROOT):
    count=0
    for desc in manifest(root)['characters'].values():
        for item in desc['poses'].values():
            path=Path(root)/item['path']
            if not path.is_file():raise FileNotFoundError(item['path'])
            check(item['path'],path.read_bytes(),item);count+=1
    return count

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    print('Verified current poses:',verify_workspace()) if sys.argv[1]=='--verify-workspace' else print('Staged current images:',stage(Path(sys.argv[1])))
