# Video AI Editor — Showcase

## Original 18-second vertical showreel

The repository now contains `RepoShowcase`, an entirely original 1080×1920 / 30 fps / 18-second **Remotion composition** created with HTML/CSS motion, timed captions, audio-waveform artwork and a podcast-style two-panel illustration. It represents existing product capabilities without redistributing third-party podcast footage or claiming all 21 effects have been rendered.

**The show's six sections:** Intro → 21 FX library → podcast cuts → Tagalog / Taglish captions → Remotion + FFmpeg + Groq STT + VoxCPM2 (testing) → end card.

### Preview it in Remotion Studio

```bash
npm ci
npm run studio
# choose RepoShowcase in Studio
```

### Render full resolution

```bash
npm run render:repo-showcase
```

Output: `out/repo-showcase.mp4` (1080×1920, H.264). This composition is **silent** and requires no source video, paid API, generated voices or model downloads. Pair it with properly licensed music or an original score in postproduction.

### GitHub Actions half-resolution preview

The dedicated `Render Video AI Editor Showcase` workflow validates TypeScript, renders `RepoShowcase` to an MP4 preview at half resolution (540×960), validates output with ffprobe, then uploads the MP4 as a **14-day GitHub Actions artifact**. Running the full-resolution render locally produces the production version. GitHub-hosted runners and Codespaces have compute quotas.

### Distinguish the present and planned features

- Real repository components: 21 library effects in `src/fx/`, Remotion compositing, FFmpeg, podcast templates, Groq transcription tooling.
- VoxCPM2: currently in a **separate draft PR** with tests; actual GPU voice-quality verification is still pending. The showcase labels it *testing*.
- The showreel's cards and fictional camera panels are **illustrations**, not example frames of user-submitted videos or evidence of automated editorial quality.

## Provenance

All graphic elements and typography in the new `RepoShowcase` composition are authored for Video AI Editor. The repository's existing Remotion, imported-effects, and font licenses remain unchanged and continue to apply. See `THIRD_PARTY_NOTICES.md`.
