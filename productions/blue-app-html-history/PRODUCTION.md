# Pilot production — Blue App message history export

**Approved title:** DELETED MESSAGES ON THE BLUE APP? 👀 HERE'S WHAT TO CHECK!

**Owner-selected premise:** Tutorial on exporting available Facebook/Messenger message history as an HTML archive, not a promise to recover permanently deleted chat text.

**Platform:** TikTok / vertical 9:16 / final intended 1080×1920, 30 fps, approximately 60–70 seconds.

**Voice:** Existing English Natural Storyteller, `natural-storyteller-v1`, Chatterbox Multilingual V3. No generic replacement TTS. Speech is generated only in the narrated render job. Silence is for technical preview only, clearly named as such.

**Visual strategy:** Original animated diagrams and title cards using the **existing pinned OpenMontage Remotion Explainer**. Visuals are schematic instructions, not actual or simulated screenshots from a user's private account. No external stock media is required for this pilot. Primary title is unchanged; shorter legible on-screen hook is deliberate.

**Narration (approved theme, technical draft for QC):**
Deleted messages on the blue app? Before using a recovery app, check what your account still has. First, search for the conversation in Messenger. Then check Archived Chats. Archived means hidden, not deleted. Next, open the blue app's Settings, then Accounts Center. Choose Your Information and Permissions, then Export Your Information. Create an export, select your profile and Messages, choose All Time and HTML, then start. When the ZIP is ready, download it, extract it, and open the HTML files. Search for the conversation. For recent end-to-end encrypted chats, secure storage may need to be checked separately. Remember, this export only shows data still available. It cannot guarantee recovery of permanently deleted messages. Only check your own account.

**Scenes:** hook → recovery-app caution → archive vs deletion → settings → Accounts Center information permissions → export → HTML / all time → ZIP and browser → encrypted secure storage → explicit no-undelete disclaimer.

**Accuracy:** Menu labels vary by account, country, rollout and app version. Export your information and encrypted Message storage are two different paths. A downloadable HTML archive is an export of available data, **not** restoration of permanently deleted messages. Do not ask for passwords, downloads of somebody else's chats, or install unauthorized recovery apps.

**Sources reviewed 2026-10-30:**
- Meta's encrypted storage explanation: https://about.fb.com/news/2024/03/end-to-end-encryption-on-messenger-explained/
- Meta data export availability: https://www.meta.com/safety/communities/law/guidelines/
- Updated explanation of Accounts Center, HTML/ZIP data export and limitations: https://www.itechguides.com/how-to-recover-permanently-deleted-facebook-messages/
- Guide distinguishing Accounts Center HTML exports from encrypted-chat secure storage: https://textexporter.com/export/facebook-messenger/

**Tool selection:** OpenMontage's upstream curated `Explainer` Remotion composition; no replacement pipeline. Original visual props kept in this repository. Full output will be checked using `ffprobe` for vertical H.264 video and AAC audio, and audio timing manifest. Word highlight timings generated from TTS chunk boundaries are **estimates**, not confirmed forced alignment; review before publishing. Render stays private to GitHub artifact viewers subject to repository visibility and Actions permissions; not uploaded to TikTok.

**Approval boundary:** This production brief is the owner's approved tutorial topic and title. A final publish approval is still required; do not publish autonomously.

**Upstream pinned OpenMontage:** `195eab24478dc9363326aec437aefc3701635ddf`, installed by `integrations/openmontage/scripts/setup.sh`.
