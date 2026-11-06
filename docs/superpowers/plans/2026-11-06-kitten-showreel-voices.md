# Kitten showreel voice replacement

Owner selected first host audition Jasper and second PIX audition Kiki on 2026-11-06. Apply to the cinematic showreel; retain the earlier voiced artifact and keep unrelated global character defaults unchanged.

- [x] Pin Mini 0.8 model, SDK source, eight-voice data and selected Jasper/Kiki mapping in showreel configuration.
- [x] Add local ONNX CPU generator with bounded inference threads and model/SDK hash validation. Keep optional dependencies isolated; no hosted TTS or new uploads during synthesis.
- [x] Bind receipts to actual text, character, engine, model revision, SDK, voice, speed and WAV hash. Reject stale or altered WAVs; do not silently relabel Chatterbox recordings.
- [x] Generate seven real WAVs and recompute PCM bounds, normalized speech, RMS and utterance captions. Preserve old audio/output files separately.
- [x] Test selected mapping, invalid model/SDK hashes and existing resume/audio/timeline regressions. Run complete suites and typecheck.
- [x] Re-render actual voiced 82-second composition, master encoded audio, decode/probe and inspect final caption/cut/pose frames.
- [x] Prepare the updated MP4 and matching production assets for the owner's selected Google Drive handoff. No GitHub push/merge is authorized.

Independent review identified stale Chatterbox setup instructions and unverified SDK provenance. The guide/dependency manifest now describe the tested lean Kitten setup; SDK source hashes are verified before inference. The added SDK-integrity regression was observed failing then passing.
