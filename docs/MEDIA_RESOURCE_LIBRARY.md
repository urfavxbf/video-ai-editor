# Media Resource Library — stock video, photos, fonts, music and SFX

## What exists right now

**Resource library is a real local workflow**, not a claim that third-party stock
assets are already downloaded and licensed. The repo currently contains:

- **Three OFL-licensed fonts**: Inter, Montserrat, Caveat in `public/fonts/`.
  They are already loaded by `src/fonts.ts`.
- **Thirteen legacy sound effects** in `public/sfx/`. Their imported provenance
  is documented in `THIRD_PARTY_NOTICES.md`, but separate publication and
  commercial usage rights have **not yet been independently verified**. The
  library shows **review-before-publication**; do not confuse “present in repo”
  with “approved for every new commercial video.”
- **Two original, committed abstract SVG backgrounds** under
  `public/resources/original/`. These are original project artwork.
- **Original silent B-roll composition**, `ResourceLibraryProof`, that uses the
  local illustrations and exports 1920×1080 at 30fps, 4 seconds.
- **Original ambient audio bed generator**, a simple synthesized 8-second
  stereo PCM16 WAV. This is a modest starter cue, **not** a library of
  professionally recorded songs.

The **13 approved UrFavXBF/PIX PNG poses** remain managed separately by
`characters/pixel-default-manifest.json`; we do **not** duplicate them in
the generic resource registry.

## How to run

Requires a checked-out repo, Python 3.11+, Pillow (`requirements.txt`),
Node 22+, pinned Remotion and FFmpeg/FFprobe.

```bash
npm ci
python3 -m pip install -r requirements.txt
python3 scripts/resource_library.py audit
python3 scripts/resource_library.py list

# Generate new original, local-only starter assets
npm run resources:render-broll
npm run resources:ambient
```

The two generated files default to:
`out/resources/original-broll.mp4` and
`out/resources/original-ambient-bed.wav`. **Neither is an approved Chatterbox
narration file.** Generated media is ignored rather than tracked as a fake
large stock pack.

To stage an original B-roll file for Remotion:

```bash
python3 scripts/resource_library.py intake out/resources/original-broll.mp4 \
  --kind video --slug abstract-new-horizons \
  --license owner-original --creator "Video AI Editor" --rights-confirmed

python3 scripts/resource_library.py intake out/resources/original-ambient-bed.wav \
  --kind music --slug quiet-ambient-bed \
  --license owner-original --creator "Video AI Editor" --rights-confirmed

python3 scripts/resource_library.py audit
```

The local copy is in `public/library/video/` or `public/library/music/`;
metadata goes to `resources/local-catalog.json` (ignored, to avoid committing
unreviewed source paths, raw stock assets or private rights documentation).
For a verified `video` file, a Remotion component can play it with
`<OffthreadVideo src={staticFile('library/video/abstract-new-horizons.mp4')}/>`.
For a still image use `<Img src={staticFile('library/image/your-image.png')}/>`.
For a music bed use the existing Remotion audio components with
`staticFile('library/music/quiet-ambient-bed.wav')` and **explicit approved**
volume/cue timing. These asset paths do not cause automatic insertion into an
episode; authors must choose narrative-appropriate resources per script.

## Adding a manually reviewed third-party resource

1. Pick a **specific asset** from a listed provider below, review its **item
   license and intended commercial distribution**, and consider identifiable
   people, property, trademarks, AI-usage limits, attribution, channel and
   redistribution restrictions. A catalogued source isn't blanket clearance.
2. Save the licensed media **manually** in your private workspace. No bulk
   downloading, hidden scraping, remote API calls, cloud generation or payments
   are part of the standard library tool.
3. Supply real author, **asset-level** source URL, exact license URL and any
   required attribution. If unsure, **do not intake or publish**.
4. Verify through the offline CLI, which refuses unknown/noncommercial
   licenses, symlink sources, invalid/huge media, duplicate slugs, malformed
   files, missing attribution and missing rights confirmation. It verifies
   physical media via Pillow/FFprobe, records a SHA-256 receipt, and refuses
   modified files during later audits.

Example (replace with real reviewed fields):

```bash
python3 scripts/resource_library.py intake input/my-approved-stock-clip.mp4 \
  --kind video --slug city-evening-001 \
  --license "Pexels License" \
  --creator "ACTUAL CREATOR CREDIT" \
  --source-url "https://www.pexels.com/video/EXACT-ITEM/" \
  --license-url "https://www.pexels.com/legal-pages/license/" \
  --rights-confirmed \
  --review-note "Reviewed for this episode, commercial YouTube context"
```

The tool records the **owner's attestation**, not a legal opinion or an
independent proof that a model release exists. Stock sites restrict standalone
redistribution and other uses: **never commit or publish a raw downloadable
stock pack** in this repository just because it says “free to use.”
A future shared/team library needs approved private media storage and
asset-level distribution rights, not blind `git add` of stock binaries.

## Curated sources (not pre-installed assets)

See [`resources/sources.json`](../resources/sources.json) for links and
restrictions. Research/review each intended asset:

| Media | Source | License caveat |
| --- | --- | --- |
| Videos & photos | [Pexels](https://www.pexels.com/) | License permits many edits/commercial uses, not standalone resale or general bulk scraping; model/brand/property rights may remain |
| Images, video & audio | [Pixabay](https://pixabay.com/) | Asset license, standalone-use restrictions and third-party rights apply |
| Photos | [Unsplash](https://unsplash.com/) | No competing stock-library compilation; commercial context/model/property rights |
| Video, music & SFX | [Mixkit](https://mixkit.co/) | **Item-specific Free/Restricted licenses**; music has narrower permitted uses than SFX |
| Fonts | [Google Fonts](https://fonts.google.com/) | Preserve each family's exact OFL/other license notice; approved existing fonts already ship |
| Sound recordings | [Freesound](https://freesound.org/) | Per-sound CC0/CC BY/CC BY-NC; exclude **CC BY-NC** from commercial production |
| Music & effects for YouTube | [YouTube Audio Library](https://www.youtube.com/audiolibrary) | Some tracks need description attribution; YouTube-specific guidance is not a grant for every off-platform use |

Reference licenses:
[Pexels](https://www.pexels.com/legal-pages/license/),
[Pixabay](https://pixabay.com/service/license-summary/),
[Unsplash](https://unsplash.com/license),
[Mixkit](https://mixkit.co/license/),
[Freesound](https://freesound.org/help/faq/),
[Google Fonts](https://github.com/google/fonts/blob/main/README.md),
[YouTube Audio Library](https://support.google.com/youtube/answer/3376882).

## Quality and production policy

- For each use, document the exact asset ID, source, rights receipt, in/out
  frames and actual output path. Check context, visuals, captions and audio.
- Assets in `out/`, `public/library/` and `resources/local-catalog.json`
  are **local/ignored**. CI does not magically have owner-provided stock
  footage or a connected private storage service.
- Image imports: local PNG/JPEG/WebP. Font imports: TTF/OTF with independently
  reviewed license. Video/audio: local, media-probed supported formats.
  The original repo-made SVGs are **tracked built-ins**, not untrusted SVG
  uploads (SVG can include executable or remote content).
- Existing approved characters/Chatterbox voices remain unchanged. Never
  substitute stock art for the approved UrFavXBF/PIX identities, or stock music
  for the approved voices.
- Inspect actual footage and listen to final audio. Stock clips, original
  B-roll proof, catalog metadata and successful CI are not a finished episode.

For production rules and copy-ready owner requests, see
[`AGENTS.md`](../AGENTS.md),
[`docs/PRODUCTION_POLICY.md`](PRODUCTION_POLICY.md) and
[`docs/AI_AGENT_PROMPTS.md`](AI_AGENT_PROMPTS.md).
