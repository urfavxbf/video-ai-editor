# Pixel Glitch V2 — portraits-only layout (owner-approved)

## Latest layout requirement — 28 October 2026

The user identified the small **animated face portraits** on the previous 23.5s sample and explicitly requested: **remove both full-body avatars and keep only the two animated portraits**.

This overrides the older layout suggestions in any earlier production docs. It does NOT remove or delete the archived full-body PNGs from the asset pack; it changes what is composited onto NEW video frames.

### Standard 16:9 composition

- **UrFavXBF:** upper left, expressive pixel-art head portrait, yellow bordered panel, yellow reacting audio bars, correct male Chatterbox V3 Natural Storyteller profile.
- **PIX:** upper right, expressive cat head portrait, cyan bordered panel, cyan reacting audio bars, correct female Emily-based Chatterbox V3 profile.
- **Center:** unobstructed infographic/motion-graphics field. During explanatory scenes, animated data and words highlighted in captions should share the speaker's actual timing and semantic topic.
- **Bottom center:** readable, speaker-tagged captions. Do not recreate the two large body cutouts or the old lower-left/lower-right character nameplates.
- Keep the subtle CRT/glitch treatments and vocal reactions on the **small portraits only**; frame and labels are part of the portrait panel.

### Re-rendered, verified example

`UrFavXBF_PIX_PixelGlitch_PortraitsOnly_Sample.mp4` was generated in the ChatGPT workspace from the old sample's **same two real Chatterbox dialogues**, graphics and ambient audio, with the full-body image composites removed.

Technical file QA: **23.5s / 1920 × 1080 / 30fps / H.264 video + AAC audio**. The clip still shows character expressions, talking vs. listening state, glitch pulses, caption emphasis and center data graphics. Character lip states are amplitude-driven proxies, **not phoneme-aligned**.

The output and its preview still are saved in the owner's ChatGPT Library at `/UrFavXBF Video Characters/Pixel Glitch V2/`.

### Reusable engine components

- `src/characters/PixelGlitchPortrait.tsx` — ONLY portrait PNGs from `public/characters/pixel-glitch/<character>/<expression>.png`; no whole-body image access. Accepts actual voice events, RMS envelopes, and optional reaction cues.
- `src/characters/PixelPortraitHUD.tsx` — 1920 × 1080 horizontal layout: two portraits plus centered data/HUD and caption field. Registered as Remotion composition **PixelPortraitHUD** in `src/Root.tsx`.
- `characters/registry.json` — default setting `default_video.character_layout = "animated-head-portraits-only"`; archive images preserved but not rendered by this default.

### Media staging

The source PNGs are stored as the previously delivered `UrFavXBF_PIX_PixelGlitch_Complete_Pack.zip` in the owner's Library, not in GitHub. Extract/copy the **`urfavxbf/` and `pix/` expression PNGs** from that pack to `public/characters/pixel-glitch/` before setting `assetsReady=true`.

```bash
npm ci
npm run typecheck
# Assets must be staged before enabling avatars.
npx remotion studio
# Find the PixelPortraitHUD composition.
```

Do not claim the repository render includes the official assets until those binary files exist in the workspace.

### Acceptance checks for future edits

1. No full-body characters visible in any frame; only head portraits and labels attached to portrait panels.
2. Speaker portraits change correctly with their **own** actual Chatterbox WAV; listener reacts without falsely mouthing the other character's speech.
3. Data and caption animations remain unobstructed and readable.
4. Confirm actual export has H.264 video, AAC audio, 16:9 1920 × 1080 at 30fps and correct total duration.
5. Never auto-upload to YouTube without permission.
