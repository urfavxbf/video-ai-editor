#!/usr/bin/env python3
"""V4 facial layer QA. Never substitute legacy PixelGlitch sprites for new art.

Without --assets, validate only the facial state contract. With --assets,
validate real V4 512x512 aligned transparent layers, protect against exact
copies of the user's uploaded old-model pack, and emit checksums for review.
A passing QA check is NOT proof of matching artistic identity or owner approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/'characters/facial-v4-rig.json'
BLOCKED_OLD_FINGERPRINTS={
    # SHA256 of user-supplied PixelGlitch V2 pack's old base/expression PNGs.
    'b11936a4ace7c6cba1ee391ff768fce93bee80b2adf81b3a44a89cbaa4cf01b4',
    '6d3bf7838ad81fd67529152d50e1bc6d5a19cd3a580c8afa5d111ea9e7f20aac',
    '66515005594761e7678031b1e4277f5262c76581aef36e1d76c40fb115ca6680',
    '66fd19f82258b8ab1190d59318dec4f181b4a21d3cc4a1a62cd0c929e54d1276',
    '19981da457549ad683efa314316008770d0b007b336c05446249f2412246bb84',
    '446b11af2e39e8a16c47979bb761e30080027c773dfe61c7d66f83909c9f0f4e',
    '547645c63dbea1aa7f5c974ac1ba14f3f27632f203ae26a7434578d37c6ecd53',
    'cc5ecccdbb74b8c90ea3af09a0c75ff2c72db05fcdf0006fdc19255641304c6f',
    '32272566b52f6643feb8c1be6f4df4eb17c5e2c88a331745898f7d6132f49fc7',
    '9032ce26cb8b8ffe9545e9c4eed2903f1da8869148cfc969df16ebfdb0dbf878',
    '0e02e790fc2e5dee39f59c276e224f170036fe4fffe88e7bf12ae30e13a74647',
    '314a849f7b50d2ca080788529c9f1e9cab4ba89efb9cd67c75fe9e0177aa6f51',
    'b72c87cf9672b3128fc01e27f21eade77d66eabd32692cbc382ff1a8a0ab9609',
    '9d18434751b92a0b26c8cd7301c9db90f84272a15aacb22d38d504235721e6e1',
}

def validate_contract(contract:dict)->dict:
    if contract.get('schema')!='video-ai-editor/facial-rig-v4/1':
        raise ValueError('Wrong V4 rig contract version')
    if contract.get('visualVersion')!='chibi-pixel-v4-dark-green':
        raise ValueError('Wrong visual style')
    if set(contract.get('characters',{}))!={'urfavxbf','pix'}:
        raise ValueError('Both V4 protagonists required')
    expressions=contract.get('expressionIds')
    mouths=contract.get('mouthIds')
    if not isinstance(expressions,list) or set(expressions)!={
        'neutral','happy','curious','excited','surprised',
        'thinking','focused','sleepy','glitch','blink'}:
        raise ValueError('Unexpected expression states')
    if not isinstance(mouths,list) or set(mouths)!={
        'rest','small','medium','wide','round','closed','fv'}:
        raise ValueError('Unexpected mouth states')
    canvas=contract['artCanvas']
    if canvas.get('width')!=512 or canvas.get('height')!=512:
        raise ValueError('V4 facial canvas must be 512 x 512')
    for identity in contract['characters'].values():
        legacy=identity.get('legacyReferenceOnly',{})
        if legacy.get('provenance') != 'facial-STATE naming and timings only; no pixel reuse':
            raise ValueError('Legacy data must be semantics-only')
    return {'characters':2,'expressionsPerCharacter':len(expressions),
            'mouthsPerCharacter':len(mouths),'qualityStatus':contract['status']}

def validate_art(contract:dict,assets:Path)->dict:
    validate_contract(contract)
    if not assets.is_dir() or assets.is_symlink():
        raise ValueError('Assets directory missing or symlink')
    approved={}
    used=set()
    for character in ('urfavxbf','pix'):
        root=assets/character
        layers=[root/'base.png']
        layers += [root/'expressions'/f'{n}.png' for n in contract['expressionIds']]
        layers += [root/'mouth'/f'{n}.png' for n in contract['mouthIds']]
        manifest=[]
        for path in layers:
            if not path.is_file() or path.is_symlink():
                raise ValueError(f'Missing/new V4 artwork not ready: {path}')
            raw=path.read_bytes()
            sha=hashlib.sha256(raw).hexdigest()
            if sha in BLOCKED_OLD_FINGERPRINTS:
                raise ValueError(f'LEGACY V2 PNG DETECTED: {path}')
            if sha in used:
                raise ValueError(f'Duplicate layer PNG detected: {path}')
            used.add(sha)
            with Image.open(path) as im:
                if im.format!='PNG' or im.size!=(512,512) or im.mode!='RGBA':
                    raise ValueError(f'Expected 512x512 RGBA PNG: {path}')
                a=im.getchannel('A')
                if a.getextrema() in ((255,255),(0,0)):
                    raise ValueError(f'Opaque or empty layer: {path}')
                if any(a.getpixel(c)>8 for c in ((0,0),(511,0),(0,511),(511,511))):
                    raise ValueError(f'Nontransparent PNG corners: {path}')
                # Prevent one giant old-style full portrait being disguised as a
                # facial feature layer; these must contain only a small overlay.
                if path!=root/'base.png':
                    covered=sum(1 for q in a.getdata() if q>8)
                    if covered > 512*512*.44:
                        raise ValueError(f'Overlay covers too much canvas: {path}')
            manifest.append({'path':str(path.relative_to(assets)),
                             'sha256':sha,'width':512,'height':512})
        approved[character]=manifest
    return {'status':'TECHNICALLY_VALIDATED_AWAITING_OWNER_ART_REVIEW',
            'layerCount':sum(map(len,approved.values())),
            'characters':approved,
            'limits':['Artwork style/identity cannot be proven automatically',
                      'No phoneme timings in an unvoiced asset pack',
                      'Body movements require separate artwork']}

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract',type=Path,default=CONTRACT)
    parser.add_argument('--assets',type=Path,
                        help='Root folder of V4/urfavxbf and V4/pix facial files')
    parser.add_argument('--output',type=Path,help='Write SHA manifest of validated art')
    args=parser.parse_args()
    try:
        contract=json.loads(args.contract.read_text())
        summary=validate_art(contract,args.assets) if args.assets else validate_contract(contract)
        if args.output:args.output.write_text(json.dumps(summary,indent=2)+'\n')
        print(json.dumps(summary,indent=2))
        return 0
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as exc:
        parser.exit(2,f'V4 FACIAL QA BLOCKED: {exc}\n')

if __name__=='__main__':
    raise SystemExit(main())
