#!/usr/bin/env python3
"""Route UrFavXBF/PIX dialogue to owner-selected English Kitten by default or optional Tagalog VoxCPM2.

Default voice identities are stored in characters/registry.json. Importing this
module does not download model weights; Tagalog is never routed as Malay.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from chatterbox_voice_profile import DEFAULT_NARRATOR
from pix_voice_profile import DEFAULT_PIX

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "characters" / "registry.json"


def default_language() -> str:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["production_language"]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Synthesize UrFavXBF or PIX dialogue (English by default, Tagalog optional).")
    p.add_argument("--character", required=True, choices=("urfavxbf", "pix"))
    p.add_argument("--language", choices=("tl", "en"), default=default_language(),
                   help="Tagalog/Taglish (tl, optional) or English (en, default).")
    t = p.add_mutually_exclusive_group(required=True)
    t.add_argument("--text")
    t.add_argument("--text-file", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", choices=("auto", "cpu", "cuda", "mps"), default="auto")
    p.add_argument("--engine", choices=("kitten", "chatterbox"), default="kitten", help="Current Kitten voices, or explicitly requested legacy Chatterbox.")
    p.add_argument("--model-dir", type=Path, default=ROOT/"input/kitten-tts-mini-0.8")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="Print the selected voice plan without inference or downloads.")
    return p


def synth_args(args: argparse.Namespace, pix_reference: Path | None = None) -> list[str]:
    """Legacy English Chatterbox arguments; never use for Tagalog."""
    if args.language != "en":
        raise ValueError("Chatterbox V3 is not approved for Tagalog; use VoxCPM2")
    profile = DEFAULT_PIX if args.character == "pix" else DEFAULT_NARRATOR
    options = ["--output", str(args.output), "--device", args.device,
               "--language-id", profile.language,
               "--exaggeration", str(profile.exaggeration),
               "--cfg-weight", str(profile.cfg_weight)]
    if args.text_file is not None:
        options.extend(["--text-file", str(args.text_file)])
    else:
        options.extend(["--text", args.text])
    if args.character == "pix":
        if pix_reference is None:
            raise ValueError("PIX requires a verified English speaker reference.")
        options.extend(["--voice-reference", str(pix_reference)])
    if args.overwrite:
        options.append("--overwrite")
    return options


def kitten_request(args: argparse.Namespace) -> dict:
    profile=json.loads((ROOT/'src/showcase/showreel-voices.json').read_text())
    voice=profile['voices'][args.character]
    registered=json.loads(REGISTRY.read_text())['characters'][args.character]['english_voice']
    if registered.get('voice')!=voice or registered.get('modelRevision')!=profile['modelRevision']:
        raise ValueError('Kitten config differs from the approved character registry')
    return {key:profile[key] for key in ('engine','model','modelRevision','sdkCommit','speed','sampleRate')}|{'voice':voice}

def kitten_main(args: argparse.Namespace) -> int:
    try:
        request=kitten_request(args)
        if args.device not in ('auto','cpu'):raise ValueError('Current Kitten adapter supports CPU only')
        if args.dry_run:
            print(json.dumps(request));return 0
        if args.output.suffix.lower()!='.wav':raise ValueError('Output must have a .wav extension')
        if args.output.exists() and not args.overwrite:raise ValueError('Output exists; choose a new path or explicitly use --overwrite')
        text=args.text_file.read_text(encoding='utf-8') if args.text_file is not None else args.text
        if not text.strip():raise ValueError('Narration text is empty')
        from kitten_showreel_voice import stage_model,load_model,generate
        stage_model(args.model_dir);model=load_model(args.model_dir)
        generate(model,text,args.character,args.output)
        import hashlib
        receipt={'request':request,'character':args.character,'text':text,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}
        args.output.with_suffix('.voice.json').write_text(json.dumps(receipt,indent=2)+'\n')
        return 0
    except (ImportError,OSError,ValueError) as exc:
        print('Kitten voice error:',exc);return 2

def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.language == "tl":
        from voxcpm_voiceover import main as voxcpm_main
        options = ["--character", args.character, "--device", args.device,
                   "--output", str(args.output)]
        if args.text_file is not None:
            options.extend(["--text-file", str(args.text_file)])
        else:
            options.extend(["--text", args.text])
        if args.overwrite:
            options.append("--overwrite")
        if args.dry_run:
            options.append("--dry-run")
        return voxcpm_main(options)

    if args.engine == "kitten":
        return kitten_main(args)
    if args.dry_run:
        print("English Chatterbox dry-run is unavailable; use --language tl for a design preview.")
        return 2
    reference = None
    if args.character == "pix":
        from prepare_pix_reference import prepare
        reference = prepare(Path("input/pix-reference.wav"))
    from chatterbox_voiceover import main as chatterbox_main
    return chatterbox_main(synth_args(args, reference))


if __name__ == "__main__":
    raise SystemExit(main())
