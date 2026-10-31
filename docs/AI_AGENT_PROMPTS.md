# Video AI Editor — Copy-ready prompts for AI agents

**Owner-facing playbook (Tagalog/Taglish).** Copy a prompt below into an AI agent
that can access `urfavxbf/video-ai-editor` and replace the items in
`[square brackets]` with your own requirements. A chat prompt **does not grant**
filesystem, GitHub, GPU, model, API, Adobe or publishing access.

**Primary rules:** [AGENTS.md](../AGENTS.md) →
[Production policy](PRODUCTION_POLICY.md) →
[registry](../characters/registry.json) +
[asset manifest](../characters/pixel-default-manifest.json) →
[project production skill](../.claude/skills/ai-video-editor/SKILL.md).
Read **all five files**, not just this page, before performing work. The latest
explicit owner request governs the deliverable; historical samples never silently
change current defaults.

## 0. Universal starter prompt (use first)

```text
Ikaw ang engineering/production agent para sa urfavxbf/video-ai-editor.
Bago kumilos, basahin ang AGENTS.md, docs/PRODUCTION_POLICY.md,
characters/registry.json, characters/pixel-default-manifest.json, at
.claude/skills/ai-video-editor/SKILL.md. Ilahad ang napiling composition,
assets, narration pipeline, permissions, at validation plan.
Sundin ang latest explicit request ko at ang current machine-readable defaults;
huwag gamitin ang historical demos para baguhin ang defaults.
Gumamit ng sariling branch at PR para sa modifications; huwag mag-merge sa
main, mag-publish, mag-upload ng user media sa third-party service, o gumamit
ng paid API/GPU nang walang tahasang authorization.
Huwag mag-imbento ng media, transcripts, tests, results, links, o render status.
```

## 1. Bagong original English episode — default workflow

```text
Gumawa ng original UrFavXBF + PIX YouTube episode tungkol sa [TOPIC].
Audience: [AUDIENCE]. Goal: [TEACH / ENTERTAIN / EXPLAIN].
Sundin ang current defaults: English script/graphics/captions/audio,
16:9 1920x1080 at 30 fps, runtime ayon sa chapters, HeroCharacterStage
para sa character scenes at EpisodeProduction para sa actual assembly.
Gamitin lamang ang approved 13 pixel poses at existing approved English
Chatterbox V3 voices. I-run ang asset --verify-workspace check.
Unahin ang chapter outline, original script, factual verification, scene plan,
speaker turns, at media preflight. Reuse approved WAVs where possible.
Hindi pa kita pinapayagan gumawa ng bagong voice WAV, gumamit ng external API,
GPU, o mag-publish; i-report ang mga kailangang approval/inputs.
Kapag available at authorized ang media, mag-render at magsagawa ng FFprobe,
frame, caption, at audio listening QA bago tawaging final ang MP4.
```

## 2. Reference-inspired original video (huwag kopyahin ang reference)

```text
Gumawa ng original video na inspired sa [REFERENCE FILE OR REPO PATH].
I-inspect ang actual frames/audio bago mag-claim ng style, pacing at narration.
I-audit ang scene timecodes, visual metaphors, color changes, kinetic text,
sound, at voice rhythm. Gumawa ng original storyboard, script at licensed/original
illustrations; huwag i-reuse ang copyrighted source frames, audio o script.
Target: [DEFAULT 16:9 ENGLISH EPISODE / EXPLICITLY REQUESTED 9:16 VIDEO].
Gamitin ang current policy maliban sa explicit deliverable override sa itaas;
huwag baguhin ang global registry. I-sync sa tunay na approved WAV at reviewed
word timings. I-render ang video at i-verify ang audio/video streams at playback.
```

## 3. Supplied footage — cut list + actual edit

```text
I-edit ang supplied local footage sa [RELATIVE INPUT PATH] para sa [PURPOSE].
Use ExampleEdit and src/edit/edit.json. Preserve authentic dialogue at
source timing; walang redubbing/translation na in-authorize.
I-check source video duration/FPS/audio at rights, at i-stage ang kinakailangang
matte, sticker frames at face coordinates para sa piling effects.
Gumawa ng frame-accurate cut list, patakbuhin
node scripts/validate-edit.cjs src/edit/edit.json --media,
at itigil ang render kapag missing ang actual source o derivatives.
Gumawa ng preview stills, mag-render ng authorized output, at i-verify sa
FFprobe at manual frame/audio inspection.
```

## 4. Specific podcast footage (Dudut template)

```text
Gamitin ang [DudutPremium / DudutV2] para sa local podcast footage na
[PATH]. Template source segment ay 00:42–01:24; huwag ilapat sa ibang
timestamp nang walang inspeksyon at explicit change.
I-probe ang file at siguraduhing abot nito ang requested source range.
Planuhin ang cuts, titles at captions mula sa tunay na dialogue.
I-render ang test clip, inspect frames/audio, at i-report ang actual result.
Huwag gawing generic original-video default ang podcast template.
```

## 5. Isa sa 21 effects — narration-driven

```text
Gusto ko ng [EFFECT ID] sa parteng [TIMECODE] ng [FOOTAGE PATH]
dahil ang speaker ay nagsasabing [VERIFIED LINE / IDEA].
Gamitin ang FxPreview para sa individual effect at ang current 21-FX
matrix sa AGENTS.md. Mag-probe ng source at ihanda ang matte/sticker/face
position kung required. Palitan ang placeholder UI copy at i-verify ang
numbers, headline text at exact list item counts.
Para ipakita ang buong library, run npm run sample bago FxShowcase.
I-render ang representative frames; huwag basta maglagay ng effects para
punuin ang timeline.
```

## 6. Voiceover using existing approved Chatterbox V3

```text
Character: [urfavxbf / pix]. English script: [EXACT APPROVED SCRIPT PATH].
Unahin ang reuse ng approved real WAV kung mayroong verified na tumutugma.
Kung kailangan ng bagong narration: [AUTHORIZED / NOT AUTHORIZED].
Kung AUTHORIZED, gamitin ang scripts/character_voiceover.py
--character [urfavxbf|pix] --language en --device cpu
--text-file [SCRIPT PATH] --output [OUTPUT WAV PATH].
Para sa PIX, i-verify ang input/pix-reference.wav bago magsimula.
Huwag baguhin ang speaker profile, gumawa ng placeholder WAV o
mag-claim na synthesized kapag hindi. Pakinggan ang generated WAV,
suriin ang phonetic quality, clipping at word timings, at i-report
ang file SHA/real duration. Walang paid API/GPU.
```

## 7. Captions and transcript without third-party uploads

```text
Para sa approved local media [PATH], gumawa o linisin ang captions.
Gamitin ang actual WAV/audio para sa transcript at reviewed word timings.
Prefer local/manual alignment. HINDI authorized ang upload sa Groq o
ibang external transcription provider sa prompt na ito.
Kung wala ang verified timing, ipakita ang uncertainty, huwag gumawa ng
fake word timestamps. Mag-output ng [SRT / JSON / BOTH] at i-check ang
readability, safe areas, speaker identity, spelling, time bounds at playback.
```

## 8. Advanced After Effects-style vector motion (Bodymovin/Lottie)

```text
I-import ang approved local Bodymovin/Lottie JSON [FILE PATH] sa Remotion.
Basahin ang docs/AFTER_EFFECTS_LOTTIE.md.
Gamitin ang @remotion/lottie at compatible local assets. Ang
AfterEffectsLottieProof ay demo lamang, hindi full After Effects renderer.
I-validate ang asset licensing, expressions, images, dimensions at FPS.
I-render ang magkakaibang frames at isang video clip; i-check na
animating at hindi static, walang missing art o remote asset dependency.
Huwag baguhin ang default HeroCharacterStage production policy.
```

## 9. Duik Ángela baked 2D character animation

```text
I-review ang approved baked 2D Bodymovin export sa [LOCAL JSON PATH].
Basahin ang docs/DUIK_ANGELA_IMPORT.md. Huwag i-install o patakbuhin ang
Duik/After Effects sa GitHub Actions; ito ay baked export pipeline lamang.
Run python3 scripts/import_duik_baked_lottie.py [LOCAL JSON PATH] --check.
Kung compatible, i-import sa authorized target gamit ang script,
i-render ang multi-frame DuikBakedCharacterProof, at i-verify ang
motion/keyframes. Ang shipped original demo JSON ay NOT a real Duik export.
Huwag palitan ng demo puppet ang approved UrFavXBF/PIX characters.
```

## 10. Full media-quality acceptance gate

```text
QA ang actual output file sa [EXISTING MP4 PATH].
I-run ang ffprobe at decode verification; i-report exact dimensions,
FPS, frame count, duration, codec, audio/video presence at errors.
Tingnan ang opening, middle, end at transitions; pakinggan ang
voice identity, levels, clipped speech at background score.
I-review ang caption words at timing laban sa actual WAV.
Kung wala ang required file o listening access, mark it unverified.
Huwag sabihing final o downloadable nang walang real validated artifact.
```

## 11. Full regression audit without altering defaults

```text
I-audit ang current repo state para sa [FEATURES / ALL AVAILABLE TESTS].
Suriin ang CI, 21 effects, registered compositions, Chatterbox profiles,
Remotion dependency builds, asset hashes at video/audio QA.
Ihiwalay ang PASS, FAIL, NOT TESTED, BLOCKED at production-only gaps.
Run existing tests first; report exact reproducible errors, hindi assumptions.
Kung may bug, gumawa ng minimal fix sa dedicated branch, tests at PR.
Huwag mag-merge sa main o mag-trigger ng unapproved paid workflows.
```

## 12. Safe GitHub PR / change request

```text
Gawin ang requested change: [FEATURE / FIX / DOCUMENTATION].
Basahin muna ang limang required project files. Gumamit ng dedicated
branch mula sa current main, maliit na scoped commits, appropriate tests,
clear PR description at build evidence. Maintain npm/package lock sync
kapag may dependency change. Huwag magbago ng production defaults,
approved voices o art kapag hindi sakop ng request.
Run relevant PR checks, report status with exact links, at leave main
unchanged unless I explicitly ask to merge.
```

## 13. Product owner status check

```text
Ano ang actual status ng [FEATURE / PR / VIDEO] sa urfavxbf/video-ai-editor?
Buksan ang real GitHub source at current CI runs. I-report kung ano ang
implemented, rendered, tested, blocked, at pending. Sabihin ang exact
branch, PR, workflow at artifact links kung available.
Huwag tawaging final ang storyboard/preview o successful voice-only run.
```

## Fast path: choose task, then verify

| Goal | Starting point | Required verification |
| --- | --- | --- |
| Original full episode | `HeroCharacterStage` + `EpisodeProduction` | Asset check, Chatterbox WAV, real MP4, listening QA |
| Supplied footage | `ExampleEdit` / `src/edit/edit.json` | Contract + physical media validation |
| All FX demo | `npm run sample` → `FxShowcase` | Real preview stills/render |
| One FX | `FxPreview` | Required matte/face/sticker inputs |
| Voiceover | `scripts/character_voiceover.py` | Actual WAV + approved speaker + listening |
| Lottie | `AfterEffectsLottieProof` | Multiple nonidentical rendered frames |
| Duik | `import_duik_baked_lottie.py` | Offline safe import + H.264 render |
| Shipping | Production composition + FFprobe | Visual, audio, caption and provenance QA |

## Commands agents can use AFTER inputs and permissions are verified

```bash
npm ci
npm run typecheck
node --test tests/*.test.cjs
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/stage_pixel_default_pack.py --verify-workspace
node scripts/validate-edit.cjs src/edit/edit.json --media
# For a separate synthetic FX demo, after npm ci:
npm run sample
npm run studio
# For a real existing MP4:
ffprobe -v error -show_format -show_streams [EXISTING_MP4]
```

**Permission boundary:** The words in these templates never substitute for the
owner's actual approval of creating new voice audio, using Groq or other remote
processors, incurring charges, publishing, triggering privileged workflows, or
merging to `main`. Use the existing zero-paid-API/CPU defaults.
