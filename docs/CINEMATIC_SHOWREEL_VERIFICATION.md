# Current cinematic showreel verification

The current export uses the owner-selected navy-hoodie host (9 exact JPEG views), retained PIX (7 PNG poses), Jasper/Kiki narration and all 33 landscape effects. The six old host PNGs and their installer have been removed. Default voice routing now uses Kitten Mini throughout the registry/CLI.

[Updated MP4](https://drive.google.com/file/d/1TK4S5Tt46HdVtvkCpVqbTBzWuQii-600/view) · [Approved audio pack](https://drive.google.com/file/d/1dWWqbD8CkfASr-0_Lyqft-oQiBfCtvMe/view) · [Word-acting example](https://drive.google.com/file/d/1Xz_LYJSSvzi3kD3acJHYiGhqNQGMkNu7/view)

- H.264/AAC, native 1920×1080, 30 fps, 2460 picture frames; container duration 82.1 seconds.
- Integrated loudness -16.1 LUFS, true peak -1.4 dBFS; max volume -1.5 dB.
- Full FFmpeg `-xerror` decode passed. Script/voice/profile/WAV receipts verified before export. All 33 effects and all 16 scheduled poses pass automated coverage checks.
- Shared QA flags the intentional dark typewriter intro (0–2.2s); independent analysis found no unexpected black gap in the body. This is a recorded design exception, not an unconditional shared-QA pass.
- Local ASR checks the seven actual encoded dialogue regions. Proper-name transcription of UrFavXBF remains ambiguous. Human listening and full-speed aesthetic approval are not claimed.
- New owner art is white-backed JPEG viewport rendering, not transparent sprites, true 3D or phoneme lip-sync. The 22-second example specifically demonstrates per-word pose cues and 100ms local glitches.

Audio is **not published to public GitHub**. The owner selected Drive-only WAV/score delivery. Stage the approved ZIP with `scripts/stage_delivery_audio.py`; it verifies recorded hashes and ignores non-audio archive entries. Model caches and rendered MP4s also remain outside Git.

The Drive file is updated in place for final copy corrections; its link stays stable. Exact size and SHA-256 are recorded in the local `out/showreel/verification.json` after each actual export rather than copied into this source document.
