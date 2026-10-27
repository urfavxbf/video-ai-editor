# Moon documentary — 2026 visual re-edit, v2

**Current delivery:** local visual review cut, 4:03.125 (16:9, 1280×720, H.264/AAC), with 32 editorial image-based shots and original atmospheric underscore. It is *not* YouTube upload-ready, because there is no real voice-over track yet.

## Direction based on submitted reference video
The reference was reviewed for visual semantics rather than overlaid text. The following principles now govern the Moon edit:
- The narrated concept determines what is shown. Motion graphics are a visual explanation, not decorative animated subtitles.
- Cinematic establishing visuals introduce atmosphere; relevant annotations and callouts appear only to clarify a mechanism.
- Earth/Moon/sea scenes need animated camera travel, cuts at the narrative beat, and clear contrast before/after disappearance.
- Distinguish real scientific data, schematic explanations, and AI-generated illustrative footage. No numerical claims inferred from AI imagery.
- Natural, intelligible voice, paced and aligned to scene changes. Never silently substitute robotic placeholder speech.

## 8-chapter / 32-shot edit
1. Night the Moon vanished: Earth, disappearance, skyline, altered nighttime skyline
2. Without moonlight: city, moonless night, terrestrial night cues
3. Oceans respond: stormy shore, tidal redistribution, local geography
4. Sun still pulls: Sun's residual tidal influence, not instant ocean freeze
5. Nature loses its clock: corals, turtles, altered environmental cues
6. Planet's balance: current 23.5° tilt, long-timescale axial stability
7. Eclipses and rotation: eclipses stop; daytime and Earth's rotation continue
8. Quiet partner: close with oceans/wildlife/climate and audience question

## Remotion skills crosswalk
Project's 12 pinned official Remotion skills are documented at `docs/REMOTION_SKILLS.md`. Relevant to production: `remotion-best-practices` (render-safe animation), `remotion-create` (composition design), `remotion-markup` (visual layers), `remotion-captions` (narration timing), `remotion-multimedia` (audio+visual assets), `remotion-render` (export) and `remotion-studio` (preview). Interactivity is relevant when making the edit user-configurable; maps, SaaS, docs-navigation and upgrade are not visual effects and should only be applied where appropriate. **Having those skills in the repository does not mean they were executed for this revision.** 

The current standalone visual review render was produced with Pillow and FFmpeg because the Remotion npm runtime is not available in the active rendering container. Retain the repo's Remotion architecture for subsequent integrated renders.

## Voice-over blocker
The committed Chatterbox adapter remains the designated final English narration engine. The GPU checkpoint/runtime is not available in the active environment. A fallback vidIQ voice attempt was rejected due to insufficient credits (0 credits spent). Another fallback required a paid plan. Therefore **v2 deliberately contains no robotic replacement narration.** Natural VO, sentence-aligned captions, final 1080p master, visual consistency and listening review are remaining release gates.

## Assets and QA
The local download pack includes render scripts, a manifest with all 32 shot decisions, generated illustrative scene plates, and moon-removal processing. The 4:03 visual review cut was probed: H.264 video 1280×720 and AAC ambient-only audio. Review frames across the timeline were inspected. The assets are not uploaded to the GitHub repository via this docs-only PR. 

References: [NASA Tides](https://science.nasa.gov/moon/tides/) • [NOAA Tides](https://www.noaa.gov/education/resource-collections/ocean-coasts/tides) • [NASA Moon Facts](https://science.nasa.gov/moon/facts/)
