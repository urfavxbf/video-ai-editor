# Fresh asset isolation — hard requirements

1. Create all episode-specific material under `openmontage/episodes/youtube-beginners-journey/` or the isolated OpenMontage project workspace. Empty asset directories at initialization are intentional.
2. Forbidden sources: ALL previously approved or rejected UrFavXBF/PIX PNGs or ZIP packs, existing speaker WAVs/Chatterbox embeddings, older episode scripts, legacy voice samples, thumbnails, B-roll, old `public/` video effects media, old compositions and snippets.
3. Preserve old repository files but do not load, import, symlink, copy or render them for this production. If a renderer cannot produce the next scene without a legacy file, fail instead of falling back.
4. Newly created characters, if included, require fresh visual specifications, source-authentic PNG/SVG files, and validation. Character names/roles may be written in the new original script; visual and audio files may not be reused.
5. Music: start with no background track; only add new separately licensed material after provenance checks.
6. Offline/free tooling may consume compute quota (including GitHub Actions). Paid API usage is prohibited; no secrets are forwarded to external OpenMontage checkout.
7. Before any final MP4: verify source hashes/provenance, audio quality, subtitles, timing, 16:9 frames and visual non-reuse.
8. Research and proposal are preproduction artifacts, not edited video. Production must not claim a render exists until its MP4 and ffprobe report are available.
