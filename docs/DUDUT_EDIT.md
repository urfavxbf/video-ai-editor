# Dudut Lang — Premium Emotional Podcast Short

## Timeline and creative direction

Source: user-provided `50812.mp4`, 93.7 seconds, 1920×864 (landscape).
Selected source range: **00:42.000–01:24.000** (42 seconds); transcript timing was checked against the imported original.

- **00:00–00:07.5:** Giant editorial headline *11 YEARS*, restrained animated rule, full-width podcast frame and question.
- **00:07.5–00:17.5:** *RESPETO BA?* editorial transition; subtle scene changes rather than repetitive punch-zooms.
- **00:17.5–00:22:** *HINDI PARA SA KABILA.* Emphasize the contrast while preserving the speaker's context.
- **00:22–00:31.5:** *RESPETO SA SARILI.* Aquamarine liquid-glass-inspired card and restrained impact in the video frame.
- **00:31.5–00:38.5:** *NO SATISFACTION.* Clean split between transcript panel and podcast footage.
- **00:38.5–00:42:** *HINDI MO AKO MAKITANG UMIYAK.* Dramatic editorial finish, no unrelated meme graphics.

Components: `src/podcast/DudutPremium.tsx` uses the repo's `fxSpring`, `popSpring`, and `Sfx` motion/sound primitives. It **does not** attempt segmentation effects requiring macOS Apple Vision. It reuses the original Remotion project setup and bundled typography and cues.

Visual safety: The original frame is shown uncropped in a 990×452 panel so neither podcast participant gets arbitrarily cut off. No artificial video background blur. The final 1080×1920 frame has dynamic typography and deliberate negative space, while the original image retains its honest native sharpness. A 1080p export does not reconstruct detail missing from the original source.

## Rendering

The repository does not commit copyrighted podcast footage or API secrets.

Place footage at `input/50812.mp4` and run from the repository root:

```bash
bash scripts/render-dudut.sh input/50812.mp4
```

Output: `out/dudut-premium-1080x1920.mp4`, H.264 CRF 16, AAC 256k, 1080×1920, 30fps.

Development preview:

```bash
npm run studio
```

Select `DudutPremium` after the source footage is staged at `public/takes/dudut/clip.mp4`.

To inspect a still without private footage, the GitHub Actions CI smoke test uses the synthetic sample media and overrides the source start to 0, producing `out/dudut-premium-smoke.png`.

## Publication note

This edited clip uses third-party podcast material. Review accuracy and secure the necessary rights/permission before uploading. On-screen source attribution is not a replacement for authorization.
