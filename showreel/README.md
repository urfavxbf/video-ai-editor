# 33-FX showreel (UrFavXBF + PIX)

Branch-only build. `.github/workflows/showreel-33fx.yml`:

1. Verifies the 13 approved pixel poses and builds the character source take + mattes.
2. Synthesizes every line in `showreel/script.json` with **Chatterbox Multilingual V3 on CPU**
   (UrFavXBF = `natural-storyteller-v1`, PIX = `pix-cute-female-emily-v1`).
3. Renders all **33 registered effects** through the real `FxPreview` composition (each clip extended to fit its line).
4. Composes a 1920x1080/30fps reel (`scripts/showreel_compose.py`): effect screen, approved poses, typed cut-list/CLI
   usage, captions, Chatterbox dialogue + each effect's SFX, glitch at every scene boundary.
   Character bounce follows measured voice RMS. **This is not lip-sync.**
5. Commits the MP4, contact sheet and receipts to `showreel/output/` on this branch.

Human listening/visual QA is still required before publishing. Not for merge to main without review.
