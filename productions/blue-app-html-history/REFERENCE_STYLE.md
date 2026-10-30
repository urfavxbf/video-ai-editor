# Faithful high-level visual study of owner-provided reference (not asset copying)

**Owner reference:** `50976.mp4`, 119.85 seconds, 952×472, approximately 29.97 fps, uploaded directly in this conversation. The video is never stored in the repository or included in generated frames.

## What the reference ACTUALLY shows

The source alternates between **cinematic pixel-story scenes** and bold, moving typographic moments:
- Opening outdoors (blue sky, clouds, grass) with a monitor placed naturally in the world
- Saturated red warning cuts with large emphasized words, character acting
- Warm dim study/office scenes: wooden desk, bookcases, practical lamps, screens and atmospheric depth
- Pixel characters walking/presenting/gesturing, not a small brand icon attached to a card
- Scene-specific camera angles (wide, desk overhead, close-up, cutaway), rapid push-ins, motion accents and close-up text
- Occasional almost-black or abstract atmospheric cutaways, highlighted red/white keywords and call-to-action

**The first draft was NOT faithful.** It reused generic OpenMontage Explainer cards. The second draft `BlueAppVisual` also erroneously relied on repetitive blue dashboard windows and a tiny envelope icon. Both were inappropriate responses to the visual reference.

## Revised visual direction (from the reference's high-level grammar, original assets)

The current `BlueAppVisual.tsx` has been fully replaced with staged, story-driven original visuals, not the generic cards:

- Original teal-jacket pixel-guide character with lavender hair and rectangular glasses; separate expressive aqua chat-bubble sidekick. Their designs differ from the reference's characters.
- Outdoor morning scene for the missing-chat hook
- Crimson warning/anti-scam cutaway
- Pixel art shelf/studio environments for archived conversations and Accounts Center navigation
- Warm desk and monitor scenes for export settings
- Grid-lit digital space and floating file symbolism for HTML and ZIP exports
- Midnight/glowing stars scene for encrypted secure storage
- Red warning outro explicitly distinguishing export from deletion recovery
- Big animated two-tone white/accent typography in scene, camera movement, foreground objects and visual depth

Production **content, ownership, title, narration and technical target remain unchanged**. Source isn't copied, traced, embedded, or reproduced. Music/SFX and the final real narration require separate listening QC. Scene-level preview must still be verified for legibility and fidelity by the owner before publishing.

## Technical
- Existing pinned OpenMontage Remotion renderer remains the engine; we stage project-specific composition into the ignored checkout, not replace core editor.
- 16:9 1920×1080 master, 960×540 preview for reliable integer scale.
- Human review required; do not assume staging is faithful just because unit tests pass.
