# VoxCPM2 optional AI voiceover

This repository provides an **optional integration**, not a bundled model. The adapter lives in `scripts/voxcpm_voiceover.py`. It produces standalone WAV narration and can also attach narration to an already rendered MP4 without re-encoding the video stream.

**Upstream:** https://github.com/OpenBMB/VoxCPM · https://huggingface.co/openbmb/VoxCPM2

## What it supports

- Tagalog, Taglish, English, and other languages covered by VoxCPM2 (officially 30; real-world Tagalog accent/word accuracy needs listening tests).
- Text-to-speech, voice descriptions, consent-based reference-voice cloning, and continuation cloning with exact transcript.
- 48 kHz WAV output, with optional FFmpeg audio mixdown for Remotion outputs.
- No Groq or ElevenLabs key is needed to synthesize locally. Model inference is still a compute expense.

## System requirements

- Python 3.10–3.12; PyTorch 2.5+; install a compatible PyTorch wheel for your environment.
- An NVIDIA GPU is strongly recommended. VoxCPM2 typically needs about **8 GB VRAM** for inference; CUDA 12+ for CUDA runtime. CPU inference is possible but can be very slow.
- FFmpeg and FFprobe only for the optional MP4 attachment.
- A standard GitHub Codespace does **not** come with a GPU. Use a GPU-equipped machine, a cloud GPU, or Google Colab with a GPU runtime. Generate the WAV there and import it into the editor if necessary.
- Model weights download on first use and can occupy several GB. Do not install or download them into the repository or Git history.

## Install only when needed

From a Python 3.10–3.12 virtual environment with an appropriate PyTorch build:

```bash
python -m pip install voxcpm soundfile
```

Do **not** add VoxCPM2 to the Codespaces bootstrap: it would force large PyTorch dependencies and model downloads on normal editors.

## Generate a Tagalog voiceover

```bash
python3 scripts/voxcpm_voiceover.py \
  --text "Bakit nga ba tayo kinikilabutan kapag nakikinig ng musika?" \
  --style "Warm, expressive Filipino male narrator, clear conversational Tagalog" \
  --device auto \
  --output out/goosebumps-vo.wav
```

For longer content, put UTF-8 narration in `input/voiceover.txt` (untracked):

```bash
python3 scripts/voxcpm_voiceover.py \
  --text-file input/voiceover.txt --output out/narration.wav
```

`--style` is optional; expressive control can vary. Use short, reviewed scene-level scripts for more reliable delivery. The CLI limits narration to 10,000 characters; split longer scripts into scenes. `--seed` defaults to 42 for repeatability.

## Add narration to a rendered Remotion video

```bash
npm run render:edit
python3 scripts/voxcpm_voiceover.py \
  --text-file input/voiceover.txt \
  --output out/narration.wav \
  --video out/edit.mp4 \
  --video-output out/edit-voiced.mp4 \
  --original-volume 0.22
```

The original MP4 is preserved. Its audio is mixed under the synthetic narration at 22% gain by default; set `--original-volume 0` to replace audio. If the input video has no audio, narration is added by itself. The synthesized narration begins at 0 seconds; edit your script or timeline for precise scene sync. Generated narration longer than the rendered video is truncated by the final video's duration. **This is not automatic word-level lip-sync**.

For captions, review the narration and then use the existing transcription/caption pipeline (`scripts/groq_transcribe.py`) where needed.

## Clone a voice you have permission to use

```bash
python3 scripts/voxcpm_voiceover.py \
  --text "Magandang araw! Narito ang bagong kuwento." \
  --reference-audio input/my-authorized-voice.wav \
  --confirm-rights \
  --output out/my-voice.wav
```

For continuation-style cloning, provide `--prompt-audio input/voice.wav --prompt-text "exact words spoken in the clip" --confirm-rights`; optionally add `--reference-audio`.

Only use reference voices with the speaker's permission or your own voice. Do not use for impersonation, fraud, or misleading speech; disclose synthetic voice use where appropriate.

## Real Tagalog audio verification on Google Colab GPU

Open the [VoxCPM2 Tagalog GPU QA notebook](../notebooks/VoxCPM2_Tagalog_GPU_QA.ipynb) in [Google Colab](https://colab.research.google.com/github/urfavxbf/video-ai-editor/blob/feat/voxcpm2-voiceover/notebooks/VoxCPM2_Tagalog_GPU_QA.ipynb) and choose a GPU runtime. The notebook synthesizes **one** Tagalog WAV from the actual 2B model, plays it in the browser and attaches that same WAV to a locally generated test MP4 (no additional model run). GPU quota/costs may apply, and this process has **not** been executed by GitHub Actions. Do not claim pronunciation or voice quality has passed until someone has listened to the produced audio.

## Verification and failure handling

```bash
python3 -m unittest discover -s tests -p 'test_voxcpm_voiceover.py' -v
python3 scripts/voxcpm_voiceover.py --help
```

These tests require no model, no GPU, and no network. Generation is only proven once you run synthesis and listen to the WAV on a suitable GPU runtime. A CPU-only Codespace cannot serve as a meaningful VoxCPM2 quality benchmark. Overwriting existing files requires the explicit `--overwrite` flag.

## Licensing

VoxCPM2 is an upstream dependency and is **not copied** into this repository. Its upstream source and model weights are licensed under Apache-2.0; comply with their license, attribution, and acceptable-use requirements. The independent Remotion licensing terms still apply. See `THIRD_PARTY_NOTICES.md`.
