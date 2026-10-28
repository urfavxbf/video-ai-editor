# How YouTube Automation Works & How to Earn From It

**Production:** English long-form explainer with UrFavXBF + PIX. 34 dialogue turns, 991 words. 1920×1080, 30fps. Approved super-pixelated glitch head-only portraits.

**Voices are non-negotiable:** UrFavXBF **Natural Storyteller** (Chatterbox Multilingual V3 built-in English voice, exaggeration 0.5, cfg_weight 0.5); PIX **Emily** (Chatterbox Multilingual V3 plus hash-verified reference, exaggeration 0.65, cfg_weight 0.35). No espeak, no substituted provider, no paid GPU, no Tagalog model. The English voice profiles remain the production defaults in `characters/registry.json`.

## Episode chapters
1. The promise: what automation really is
2. How it works: niche, research, scripting, voice, visuals, editing, thumbnails, and analytics
3. How creators earn: ads, affiliates, sponsorships, products, and fan support
4. Monetization rules and announced February 2027 entry change
5. Worked $200 hypothetical RPM calculation, costs and uncertainty
6. Risks: reused, repetitive, low-value content; copyright; unverified AI output
7. A no-budget first-month action plan
8. Final takeaway: original value before automation volume

Script: `episodes/youtube-automation-en.json` (English).
Remotion: `YoutubeAutomationEnglish`.
Generator: `scripts/generate_automation_english.py`.
Verified WAV packaging: `scripts/package_automation_english.py`.
Approved character atlas preparation: `scripts/stage_automation_atlases.py`.
GitHub workflow: `.github/workflows/youtube-automation-english.yml` (standard hosted CPU only).

## Local build commands
```bash
python3 scripts/generate_automation_english.py --validate-only
python3 scripts/stage_automation_atlases.py
python3 -m unittest discover -s scripts -p 'test_automation_english.py' -v

# Separate Python 3.11 environment with pinned *CPU* torch and Chatterbox V3:
python3 -m pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 torchaudio==2.6.0
python3 -m pip install -r requirements-chatterbox.txt
python3 scripts/check_chatterbox_v3.py
python3 scripts/generate_automation_english.py --device cpu

python3 scripts/package_automation_english.py
python3 scripts/stage_automation_atlases.py --props out/youtube-automation/voice-props.json

npm ci
npm run typecheck
npx remotion render YoutubeAutomationEnglish out/youtube-automation-english-chatterbox.mp4 --props=out/youtube-automation/voice-props.json --codec=h264 --crf=22 --pixel-format=yuv420p --audio-codec=aac
```

The voice generator reuses one actual V3 checkpoint for all cues, instead of loading it 34 times. It fails if the exact English identities are changed and only writes PCM16 WAVs from successful inference. All 34 WAVs must exist before the timeline/MP4 is packaged. The timeline is derived from measured WAV durations and RMS envelopes; captions currently have **cue-level** approximate paging, not real word alignment. All output must pass audio listening and full playback QA before publication.

**No automatic upload to YouTube.** Do not label a preview as a completed voice-verified MP4 unless CI produced the artifact and the H.264/AAC check passed. GitHub-hosted CPU minutes may be subject to the repository's Actions quota; no paid GPU runner is configured.

## Official policy references (checked October 28, 2026)
- YPP thresholds and qualified watch time: https://support.google.com/youtube/answer/72851
- Fan funding and ad revenue: https://support.google.com/youtube/answer/94522
- Announced February 1, 2027 updated new-entrant thresholds: https://support.google.com/youtube/answer/12843009
- Inauthentic and reused content policy: https://support.google.com/youtube/answer/1311392

## YouTube upload draft — English, do not upload automatically

**Title:** How YouTube Automation REALLY Works (And How Creators Make Money)

**Description:** Is YouTube automation truly passive income? UrFavXBF and PIX break down the real channel workflow—from finding an audience and researching topics to writing scripts, producing voiceovers, editing original visuals, and reading analytics. Learn how creators earn from advertising, affiliate links, sponsorships, products and viewer support. We also work through a hypothetical RPM calculation, explain key YouTube monetization milestones and the announced 2027 rule change, and show why copyright, originality and genuine viewer value matter.

**Thumbnail concept:** oversized yellow UrFavXBF head + cyan PIX head, central video-production flow leading to a small dollar symbol, bold text: **AUTOMATION = MONEY?**. No exaggerated guaranteed earning claims.

**Music:** Original or properly licensed ambient track mixed quietly under dialogue; do not use unlicensed songs or AI-generated imitations of protected music.
