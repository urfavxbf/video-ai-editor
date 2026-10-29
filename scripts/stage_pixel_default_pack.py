"""Stage independently generated approved UrFavXBF/PIX PNGs without cropping or blurring.
Usage: python scripts/stage_pixel_default_pack.py /path/to/UrFavXBF_PIX_Official_10_Poses.zip
Requires Pillow. Refuses existing assets; verifies every SHA-256 and RGBA canvas first.
"""
import hashlib,json,sys,zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def validate(zip_path,root=ROOT):
    d=json.loads((Path(root)/'characters/pixel-default-manifest.json').read_text())
    staged={}
    with zipfile.ZipFile(zip_path) as z:
        for id,info in d['characters'].items():
            for pose,item in info['poses'].items():
                path=item['path']
                if path!=f'public/characters/pixel-default/{id}/{pose}.png':raise ValueError('unsafe path')
                if z.getinfo(path).file_size>4_000_000:raise ValueError('image too large')
                raw=z.read(path)
                if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:raise ValueError('SHA mismatch '+path)
                im=Image.open(BytesIO(raw));im.load()
                if im.mode!='RGBA' or im.size!=(1254,1254):raise ValueError('invalid RGBA PNG '+path)
                if im.getchannel('A').getextrema()!=(0,255) or im.getpixel((0,0))[3]!=0:raise ValueError('not transparent '+path)
                staged[path]=raw
    if len(staged)!=10:raise ValueError('expected exactly ten images')
    return staged

def stage(zip_path,root=ROOT):
    output=validate(zip_path,root)
    for path in output:
        if (Path(root)/path).exists():raise FileExistsError(path)
    for path,raw in output.items():
        target=Path(root)/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    return len(output)

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    print('Staged poses:',stage(sys.argv[1]))
