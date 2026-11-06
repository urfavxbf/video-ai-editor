# Cinematic showreel

`CinematicShowreel` is an 82-second, native 1920×1080 / 30 fps composition with all 33 FX, approved UrFavXBF/PIX art and all 16 current poses. The owner selected **Jasper for UrFavXBF** (first host audition) and **Kiki for PIX** (second PIX audition) on 2026-11-06. This showreel uses **KittenTTS Mini 0.8 on CPU**, replacing its earlier Chatterbox narration. The same Jasper/Kiki identities and new owner-sheet host are now the global defaults.

`src/showcase/showreel-voices.json` pins the voice mapping, speed, model revision, model/voice files and SDK source hashes. `scripts/kitten_showreel_voice.py` verifies actual model and SDK files before inference. Raw WAV receipts record the engine/model/revision/voice/speed and actual WAV hash. The old Chatterbox identities are never assigned to Kitten recordings.

## Reproduce with delivered audio

Check out the matching source branch first, then extract the delivered production asset ZIP at the repository root. Run `npm ci`, install Python NumPy and FFmpeg/FFprobe, then:

```bash
npm run showreel:check
npm run render:cinematic-showreel -- --browser-executable=/usr/bin/chromium
```

The explicit browser path is optional when Remotion finds a compatible Chrome. The wrapper forwards additional flags to Remotion, then performs two-pass offline mastering with video stream copy, targeting −16 LUFS / −1.5 dBTP. Existing delivered WAVs require no TTS inference or model download.

## Generate the selected voices

The lean setup below was tested with Python 3.12. Use a separate environment; the main editor install does not need TTS packages. The normal upstream install includes KittenTTS 2 dependencies; use the documented ONNX-only installation:

```bash
python3 -m venv .venv-kitten
.venv-kitten/bin/python -m pip install --no-deps 'kittenml @ git+https://github.com/KittenML/KittenTTS.git@b9517e3050adced306219f8bea5f117d87ecfaa7'
.venv-kitten/bin/python -m pip install -r requirements-kitten-onnx.txt
python3 scripts/render_showreel_voices.py --python .venv-kitten/bin/python
npm run showreel:prepare
npm run showreel:check
```

The generator stages only pinned, hash-verified public model files under ignored `input/kitten-tts-mini-0.8/`. It runs ONNX CPUExecutionProvider with two inference threads and produces mono PCM16 WAVs at 24 kHz. No GPU, hosted API, audio upload, voice cloning, or Emily reference is used. Generated raw WAVs stay under `input/showreel-voices-kitten/`; normalized speech and the original score stay under `public/voiceovers/showreel-kitten/`.

Resume requires matching script/speaker/voice/model receipts and unmodified WAVs. It fails on stale data instead of overwriting. For a changed script/voice, generate into a new directory with `--output-dir input/showreel-voices-next`, then run `python3 scripts/prepare_showreel.py --source-dir input/showreel-voices-next`. Keep the selected profile explicit.

Kitten SDK code and Mini model card declare Apache-2.0; retain applicable notices when distributing those dependencies. **KittenTTS 2 is a separate family with separately licensed weights and is not used here.** Sources: [SDK](https://github.com/KittenML/KittenTTS), [Mini model card](https://huggingface.co/KittenML/kitten-tts-mini-0.8).

## Timing and visual behavior

The original typography/character scenes use native landscape variants of all 33 existing effect IDs, not stretched portrait templates. Their legacy implementations remain unchanged. Counts are repository facts, not fabricated performance metrics.

Audio preparation trims only leading/trailing silence, measures actual PCM durations, normalizes levels and rebuilds speaker events/RMS envelopes and whole-utterance caption intervals. Re-render the picture when speech timing changes; merely replacing the AAC track would leave the old burned-in captions and speaking poses.

The score and transition Foley are original deterministic local synthesis. Audio-reactive particles use measured score RMS. Character poses and restrained transforms are 2.5D, not phoneme lip-sync or modeled 3D. The explicitly silent Studio preview defaults to `audioReady:false`; the delivery command requires real verified audio.

## Verification

Run `npm run typecheck`, `node --test tests/*.test.cjs`, `python3 -m unittest discover -s tests`, and approved-art hash verification. Media QA must inspect the actual encoded MP4, dialogue/mix, representative/cut/pose frames and captions. See [delivery verification](CINEMATIC_SHOWREEL_VERIFICATION.md) for actual results and remaining listening review.

Render one job per output directory. Generated videos, recordings, model files and delivery ZIPs are ignored local artifacts.

The shared renderer now uses the exact nine-view navy host from owner sheet 52170.jpg with explicit white backing. Previous delivered MP4s show the art used at their original render; rerender for the new host. Existing pose names are compatibility aliases to current artwork; deleted neon host PNGs are never used.

## Audio delivery: Drive only

The owner selected code/artwork in public Git and audio on Drive. Download the [verified source/audio ZIP](https://drive.google.com/file/d/1dWWqbD8CkfASr-0_Lyqft-oQiBfCtvMe/view), run `python3 scripts/stage_delivery_audio.py /path/to/showreel-assets.zip`, then `npm run showreel:check`. The stager accepts only known WAV paths and SHA-256 values, ignores other ZIP contents and rejects changed existing audio.
