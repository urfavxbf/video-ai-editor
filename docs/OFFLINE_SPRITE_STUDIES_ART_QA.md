# Offline full-body frame study generator (NOT approved character art)

`scripts/generate_zero_budget_sprite_studies.py` draws **230 complete whole-character raster images** from individual changing pose geometries, across 15 action names for each of UrFavXBF and PIX. Unlike the discarded 2.5D cutout demos, each PNG is constructed directly onto a new transparent frame; the approved character image is never cut into moving pieces.

**Artwork quality limitation:** this is a deliberately simplified *original vector study*, **not** the detailed approved October 29 anime design. The user-approved faces, hoodie textures, and PIX details are not perfectly replicated. No art or motion approval is implied, and no source image is upscaled. It would be deceptive to ship these as the final canonical characters.

**Budget:** $0 external generation, no Spritesheets.ai or OpenArt credits, no GPU runners, no subscription changes. Python/Pillow CPU drawing only.

To regenerate and review the technical proof:

```sh
python -m pip install Pillow==11.3.0
ZERO_BUDGET_OUT=out/offline-sprite-study python scripts/generate_zero_budget_sprite_studies.py
```

GitHub Action `offline-sprite-studies.yml` publishes a 230-PNG ZIP and Remotion review MP4 as a workflow artifact when this script is changed on main or a PR is opened. This is bounded CPU validation and does not call any generative external service. The generated manifest explicitly says `productionApproved=false`.

## Next art milestones before production
- Render **independently drawn, reference-faithful** sequential sprites, with clean hand/leg/face details, for both characters at native high resolution.
- Resolve PIX matching full-body artwork against the official face reference.
- Validate motion continuity for walking, running, jumping, pointing and speaking, without pose drift or hidden source crops.
- Produce high-quality aligned viseme drawings and phoneme timings for the English Chatterbox voices.
- Obtain explicit owner art approval; only then stage new frames as production assets and flip production art gates.

The 8-pose high-detail UrFavXBF sprite study and its rough pointing-camera animatic are separately saved in the owner's persistent ChatGPT Library, under `/UrFavXBF Video Characters/True Frame Studies/`. They cannot substitute for all 30 motion cycles either.
