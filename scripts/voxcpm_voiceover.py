#!/usr/bin/env python3
"""Optional VoxCPM2 voiceover generator for Remotion/FFmpeg video renders.

The model is downloaded only when this command is invoked. No model weights,
recordings, credentials, or generated media are committed to the repository.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


DEFAULT_MODEL = "openbmb/VoxCPM2"
MAX_TEXT_CHARS = 10_000


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    text = parser.add_mutually_exclusive_group(required=True)
    text.add_argument("--text", help="Narration text, including Tagalog/Taglish")
    text.add_argument("--text-file", type=Path, help="UTF-8 narration text file")
    parser.add_argument("--style", help="Optional natural-language voice/style description")
    parser.add_argument("--reference-audio", type=Path, help="Authorized WAV clip for voice cloning")
    parser.add_argument("--prompt-audio", type=Path, help="WAV clip for continuation cloning")
    parser.add_argument("--prompt-text", help="Exact transcript of --prompt-audio")
    parser.add_argument("--confirm-rights", action="store_true",
                        help="Confirm you own/have explicit permission for reference voice")
    parser.add_argument("--model-id", default=DEFAULT_MODEL)
    parser.add_argument("--device", default="auto", choices=("auto", "cuda", "cpu", "mps"))
    parser.add_argument("--steps", type=int, default=10, help="Diffusion inference steps")
    parser.add_argument("--cfg", type=float, default=2.0, help="Guidance strength")
    parser.add_argument("--seed", type=int, default=42, help="Reproducible generation seed")
    parser.add_argument("--output", type=Path, default=Path("out/voiceover.wav"))
    parser.add_argument("--video", type=Path, help="Optional rendered MP4 to attach narration to")
    parser.add_argument("--video-output", type=Path, help="Default: out/<video-stem>-voiced.mp4")
    parser.add_argument("--original-volume", type=float, default=0.22,
                        help="Level of original video audio when mixing: 0.0 to 1.0")
    parser.add_argument("--overwrite", action="store_true",
                        help="Allow overwriting existing generated output files")
    return parser


def prepare_text(args: argparse.Namespace) -> str:
    narration = args.text if args.text is not None else args.text_file.read_text(encoding="utf-8")
    narration = narration.strip()
    if not narration:
        raise ValueError("Narration text cannot be empty.")
    if len(narration) > MAX_TEXT_CHARS:
        raise ValueError(f"Narration is over {MAX_TEXT_CHARS} characters; split into scenes.")
    if args.style:
        style = args.style.strip()
        if not style or "\n" in style or "(" in style or ")" in style:
            raise ValueError("Style must be a single, nonempty description without parentheses.")
        narration = f"({style}){narration}"
    return narration


def validate_args(args: argparse.Namespace) -> Path | None:
    if args.steps < 1 or args.steps > 100:
        raise ValueError("--steps must be between 1 and 100.")
    if not 0 < args.cfg <= 10:
        raise ValueError("--cfg must be greater than 0 and at most 10.")
    if not 0 <= args.original_volume <= 1:
        raise ValueError("--original-volume must be between 0 and 1.")
    if bool(args.prompt_audio) != bool(args.prompt_text):
        raise ValueError("Use --prompt-audio and --prompt-text together.")
    if (args.reference_audio or args.prompt_audio) and not args.confirm_rights:
        raise ValueError("Voice cloning requires --confirm-rights and consent from the voice owner.")
    for audio in (args.reference_audio, args.prompt_audio):
        if audio is not None and (not audio.is_file() or audio.suffix.lower() != ".wav"):
            raise ValueError(f"Reference audio must be an existing WAV file: {audio}")
    if args.video_output and not args.video:
        raise ValueError("--video-output requires --video.")
    if args.video is not None and not args.video.is_file():
        raise ValueError(f"Video file not found: {args.video}")
    video_output = args.video_output
    if args.video and video_output is None:
        video_output = Path("out") / f"{args.video.stem}-voiced.mp4"
    inputs = [a.resolve() for a in (args.video, args.reference_audio, args.prompt_audio) if a]
    targets = [args.output]
    if video_output:
        targets.append(video_output)
    for target in targets:
        if target.resolve() in inputs:
            raise ValueError(f"Output would overwrite an input: {target}")
        if target.exists() and not args.overwrite:
            raise FileExistsError(f"Output already exists: {target}. Pass --overwrite to replace it.")
    if video_output and video_output.resolve() == args.output.resolve():
        raise ValueError("WAV and MP4 output paths must be different.")
    return video_output


def synthesize(args: argparse.Namespace, narration: str) -> None:
    try:
        import soundfile as sf
        from voxcpm import VoxCPM
    except ImportError as exc:
        raise RuntimeError(
            'Optional VoxCPM2 dependencies missing. Install with: '
            'python -m pip install "voxcpm" "soundfile"'
        ) from exc

    print(f"Loading {args.model_id} on {args.device}; first run downloads model weights.")
    # Disabling torch.compile avoids CUDA Graph / CPU / Codespaces compatibility issues.
    model = VoxCPM.from_pretrained(
        args.model_id, device=args.device, optimize=False, load_denoiser=False
    )
    options = {
        "text": narration,
        "cfg_value": args.cfg,
        "inference_timesteps": args.steps,
        "seed": args.seed,
    }
    if args.reference_audio:
        options["reference_wav_path"] = str(args.reference_audio.resolve())
    if args.prompt_audio:
        options["prompt_wav_path"] = str(args.prompt_audio.resolve())
        options["prompt_text"] = args.prompt_text
    wav = model.generate(**options)
    if len(wav) == 0:
        raise RuntimeError("VoxCPM2 produced no audio.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Atomic write prevents a failed run from leaving a corrupt final WAV.
    with tempfile.NamedTemporaryFile(
        suffix=".wav", prefix=".voxcpm-", dir=args.output.parent, delete=False
    ) as tmp:
        temporary = Path(tmp.name)
    try:
        sf.write(str(temporary), wav, model.tts_model.sample_rate)
        os.replace(temporary, args.output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Saved narration: {args.output}")


def contains_audio(video: Path) -> bool:
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
         "-of", "json", str(video)],
        check=True, capture_output=True, text=True,
    )
    return any(stream.get("codec_type") == "audio"
               for stream in json.loads(probe.stdout).get("streams", []))


def build_mux_command(
    video: Path, wav: Path, output: Path, original_volume: float, has_audio: bool,
) -> list[str]:
    if has_audio and original_volume > 0:
        graph = (
            f"[0:a:0]volume={original_volume}[bed];"
            "[bed][1:a:0]amix=inputs=2:duration=longest:dropout_transition=0,"
            "alimiter=limit=0.95,apad[aout]"
        )
    else:
        graph = "[1:a:0]apad[aout]"
    return [
        "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(video), "-i", str(wav),
        "-filter_complex", graph, "-map", "0:v:0", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-shortest", str(output),
    ]


def mux_video(video: Path, wav: Path, output: Path, original_volume: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    # FFmpeg must finish before replacing the final output; never mutate the source MP4.
    with tempfile.NamedTemporaryFile(
        suffix=".mp4", prefix=".voxcpm-", dir=output.parent, delete=False
    ) as tmp:
        temporary = Path(tmp.name)
    try:
        cmd = build_mux_command(video, wav, temporary, original_volume, contains_audio(video))
        subprocess.run(cmd, check=True)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Saved narrated video: {output}")


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    try:
        narration = prepare_text(args)
        video_output = validate_args(args)
        synthesize(args, narration)
        if args.video and video_output:
            mux_video(args.video, args.output, video_output, args.original_volume)
        return 0
    except (ValueError, FileNotFoundError, FileExistsError, RuntimeError,
            OSError, subprocess.CalledProcessError) as exc:
        print(f"VoxCPM2 voiceover failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
