# UrFavXBF owner-sheet word performance

The owner supplied `52170.jpg` on 2026-11-06 and requested this new navy-hoodie Filipino host, all poses/views, a semantically appropriate swap at each spoken word, and fast pixels/glitch on every swap. `WordPoseHostDemo` is the new example composition. The current default host and shared character runtime now use this same artwork; six superseded old host PNGs were removed.

The exact source JPEG is committed at `public/characters/urfavxbf-8bit/owner-sheet.jpg`, SHA-256 recorded in `characters/urfavxbf-8bit-manifest.json`. `OwnerSheetHost` shows it in bounded CSS viewports. These preserve the supplied art, including small expression marks, without regenerating it; they are **white-backed viewports, not transparent sprite PNGs**. Use a white stage. This is pose-swapped art, not frame animation, phoneme lip-sync or true 3D.

Nine poses: front, three-quarter, side, back, waving, pointing, explaining, thumbs-up, surprised. Script and explicit word-to-pose mapping live in `src/characters/word-poses/script.json`. Each consecutive spoken word has a different pose. Word starts trigger a three-frame (100 ms) character-local slice/pixel glitch; at least one stable frame must remain before the next word. No full-frame flashing.

Narration is the previously owner-selected **Kitten Mini 0.8 Jasper**, locally generated on CPU through the pinned/hashed showreel adapter. A changed host voice is rejected, rather than silently inheriting another showreel choice. PIX does not speak in this host-only example. Current English defaults are Jasper/Kiki throughout the registry and production CLI. Older pose names resolve through explicit aliases to the new art.

## Render included audio

Word timing and receipts are committed. The owner selected **Drive-only audio**, so WAVs are excluded from public Git. Download the [host source/audio ZIP](https://drive.google.com/file/d/1dWWqbD8CkfASr-0_Lyqft-oQiBfCtvMe/view), then stage its verified audio locally. No speech generation is needed:

```bash
python3 scripts/stage_delivery_audio.py /path/to/Video-AI-Editor-Current-Approved-Audio.zip
python3 scripts/prepare_host_word_poses.py --check
npm run render:host-word-poses
```

## Regenerate narration

Use the Kitten ONNX environment documented in `CINEMATIC_SHOWREEL.md`. Alignment additionally uses local CPU torch/torchaudio 2.6.0, scipy and faster-whisper, and an already staged local Whisper tiny.en model under `input/whisper-tiny-en`. The alignment script downloads Torchaudio's wav2vec2 BASE 960h model into ignored `input/host-word-poses/torch-cache` if missing; no speech is uploaded. No model weights are redistributed in the delivery archive.

```bash
/tmp/kitten-onnx/bin/python scripts/generate_host_word_poses.py
/tmp/showreel-tts/bin/python scripts/align_host_word_poses.py
python3 scripts/prepare_host_word_poses.py
python3 scripts/prepare_host_word_poses.py --check
npm run render:host-word-poses
```

The `/tmp` environment paths are this session's interpreter locations, not installed cross-machine requirements. Set up equivalent environments before reproducing elsewhere. New generation can change PCM: always align again. Generation receipts bind actual WAV hashes, text and pinned voice request. Preparation rejects omitted/mismatched words, unknown/repeated poses, stale receipts, changed WAVs and too-short quantized holds. Delivery additionally rejects a changed script, alignment, raw generation inputs, art or assembled narration.

`performance.json` contains standard Caption fields plus pose IDs. Its word estimates come from CTC forced alignment of the actual PCM, after local Whisper independently matches the authored transcript. They are **machine alignment estimates, not human listening approval**. Text and timings are bound to actual WAV hashes. Speech identity follows the verified generator request; local ASR is not a voice-identification test.

The renderer exports native 1920×1080 H.264/AAC at 30 fps, then applies the shared two-pass loudness master. Final QA uses `scripts/episode_qa.py`, full FFmpeg decode, actual MP4 pose and glitch contact frames and local transcription of the encoded mix. See the included `verification.json` for measured values and remaining manual review.
