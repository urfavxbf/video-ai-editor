# Chatterbox Multilingual V3 voice-over integration

Voice-over generation uses the official [Resemble AI Chatterbox](https://github.com/resemble-ai/chatterbox) project pinned to an immutable GitHub source revision in `requirements-chatterbox.txt`. Its upstream project is MIT-licensed; we install it as an optional dependency rather than copying its source code.

## Supported scope

- Generate one narrated WAV file from a short script (up to 700 characters).
- Optional reference recording for consistent **authorized** speaker voice cloning.
- Choose a supported language and CPU, CUDA, or Apple MPS.
- Overlay that WAV on any Remotion `ExampleEdit` composition and control the source-audio level.
- Supports on-demand local CLI synthesis and a manual GitHub Actions **Generate Chatterbox V3 narration** workflow after it is merged to the default branch. This does not provide a hosted low-latency TTS API or automatically verified natural-sounding audio.

**Tagalog is not officially supported.** The multilingual V3 language list contains Malay (`ms`) and English (`en`), but not Filipino/Tagalog (`tl`). Do not label `ms` as Tagalog support. You can experiment with a Tagalog script tagged as `ms` only with the understanding that accent, transcription, and pronunciation may be incorrect. Manually review every output before publication.

## Important: V3 dependency compatibility

The upstream **PyPI `chatterbox-tts==0.1.7` wheel predates the Multilingual V3 API** and does not support `ChatterboxMultilingualTTS.from_pretrained(..., t3_model="v3")`. Simply installing the PyPI version leads to a runtime error. The optional requirements now pin upstream Git commit `5de7a54aa4e5e2baadb0182dde554908b48b85c2`, which exposes the V3 selector. Upstream's package metadata still says `0.1.7`, so version-number checks alone are insufficient. See the source revision comment in the requirements file. This is verified from *source/API*, **not** by running model inference.

## Install the optional engine

Use a separate environment to keep existing Remotion / Groq dependencies lightweight. A CUDA-capable machine is strongly recommended for practical generation; CPU runs may be slow. Do not install Chatterbox in the default Codespace post-create command or normal GitHub Actions CI.

~~~bash
python3.11 -m venv .venv-chatterbox
.venv-chatterbox/bin/python -m pip install --upgrade pip
.venv-chatterbox/bin/python -m pip install -r requirements-chatterbox.txt
.venv-chatterbox/bin/python scripts/check_chatterbox_v3.py
~~~

The preflight checks the installed V3 loader signature and CUDA availability but does not download weights or generate WAV; a passing preflight is **not** a successful narration test. Run model-free regression tests with `python3 -m unittest discover -s tests -p 'test_chatterbox_preflight.py'`. Python 3.11 is the project-tested environment upstream. The first generation downloads checkpoint files from Hugging Face; this requires disk space, internet access and compute. Standard Codespaces instances generally do not include an NVIDIA GPU. Optional package installation can be resource-intensive.

## Generate narration

English voice-over using the built-in speaker:

~~~bash
.venv-chatterbox/bin/python scripts/chatterbox_voiceover.py \
  --text "What if you could rewind time by just one second?" \
  --language-id en \
  --output public/voiceovers/what-if.wav
~~~

Authorized speaker cloning: provide a clean reference recording **that you have permission to use**.

~~~bash
.venv-chatterbox/bin/python scripts/chatterbox_voiceover.py \
  --text-file input/narration.txt \
  --language-id en \
  --voice-reference input/my-consented-voice.wav \
  --device auto \
  --output public/voiceovers/my-narration.wav
~~~

Output must be a WAV; the CLI refuses to replace an existing file unless `--overwrite` is supplied. For expressive narration, experiment with `--exaggeration 0.65 --cfg-weight 0.3` and review results. Do not store any third-party private voice samples in Git.

### Connect output to Remotion

After generating the WAV, edit the local `src/edit/edit.json` and add these top-level properties:

~~~json
{
  "narration": {"file": "voiceovers/what-if.wav", "volume": 1},
  "sourceVolume": 0
}
~~~

These properties are **additional** to `source`, `segments` and optional `music`; do not replace the entire JSON document. `sourceVolume: 0` mutes the original video audio so narration is not doubled; omission preserves current source-audio behavior. Optional music continues using its existing mixer setting. The voice-over starts at timeline frame 0.

~~~bash
npm run typecheck
npm run render:edit
~~~

Narration is audio-only. Word-by-word captions still require reviewed timestamps from transcription / forced alignment, not guessed timings. The existing `scripts/groq_transcribe.py` can transcribe a generated WAV; inspect the words against the original script for accuracy.

## Long-form narration — one model load, one output WAV

The video editor no longer requires manually synthesizing and stitching individual chapters. Save English narration in a UTF-8 text file, then run:

~~~bash
.venv-chatterbox/bin/python scripts/chatterbox_longform.py \\
  --text-file input/moon-script.txt \\
  --language-id en --device auto --max-chars 320 --pause-ms 280 \\
  --output public/voiceovers/moon-english.wav
~~~

The CLI loads Chatterbox V3 once, chunks on sentences or word boundaries (never splitting words), checks audio samples, joins chunks with a small pause, and writes both `moon-english.wav` and `moon-english.json`. The manifest records *chunk* timings only: it is **not** verified word alignment. The audio retains upstream watermarking. For a different voice, add `--voice-reference input/consented-speaker.wav`; **never commit reference recordings**.

### Android / browser — manual GitHub Actions narration

After this branch is merged into `main`, open the GitHub repository in a browser, navigate to **Actions → Generate Chatterbox V3 narration → Run workflow**. Paste an English script into the narration input and run. The workflow installs the pinned upstream Chatterbox V3, synthesizes with the built-in voice on a CPU runner, and publishes a downloadable artifact named `chatterbox-v3-narration` containing the WAV and timing JSON. GitHub Actions may consume included minutes or billable runner time; CPU model inference can be resource-intensive or time out. If a run fails, inspect its job logs; **never present an ungenerated audio link as though it succeeded**. This workflow does not clone arbitrary speakers or accept remote voice-reference URLs, to avoid handling biometric recordings in Actions logs or public artifacts.

### Real-audio verification gate

`.github/workflows/chatterbox-v3-audio-smoke.yml` provides an English **real model synthesis** smoke test on CPU; unlike the adapter unit tests, this installs the source and downloads model weights. It then checks the resulting WAV and uploads it as `chatterbox-v3-english-voice-sample`. A green build is still insufficient to guarantee narration quality—listen for hallucinations, pronunciation and natural pacing before final video publication.

## Quality, ownership, and operational notes

- Only clone your own voice or one with explicit speaker authorization.
- Chatterbox audio contains upstream Perth watermarking; keep it intact.
- For monetized content, review the upstream MIT license and any voice-recording rights.
- For long scripts, split into scene-sized segments. This CLI exports a single WAV per invocation, with no automatic stitching.
- Generated audio lives under ignored `public/voiceovers/`; do not commit generated files or large model weights.
- GitHub CI uses mocked audio/model tests and **does not** download models or verify audible output. Validate pronunciation, audio duration, and audio/video synchronization with a real synthesis run before releasing videos.
