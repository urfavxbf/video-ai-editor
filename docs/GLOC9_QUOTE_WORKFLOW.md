# Quote-first podcast clips — Gloc-9 / Kara David example

Our target is a **memorable idea in the guest's real words**, not a narrated recap or a 35-second block of unbroken scrolling subtitles. The guest's exact delivery and pauses determine the edit. Edit only source media the production is authorized to use; do not assume that a publicly accessible upload is licensed for reposting.

## Source moment

- Source: *i-Listen with Kara David* (GMA Public Affairs), featuring Gloc-9, August 5, 2026.
- Original episode: https://www.youtube.com/watch?v=nVTYAJyW-ls
- The public transcript places the lesson at approximately **29:35–29:55** of the episode (verify manually against the provided source before publication).
- Central message: People may forget a song, but not how you treated them. Emphasize the contrast rather than sensationalizing the guest.

## Recommended production recipe

1. Leave **handles** on both ends of the selection; trim to conversational boundaries on actual source audio, without changing the meaning.
2. Reframe the landscape interview to **1080×1920 / 30fps**, centering Gloc-9 and switching the reframe when Kara is speaking.
3. Keep **the real interview voice** throughout. Use moderate speech compression, high-pass below ~85Hz and a -16 LUFS output target; music may be added very quietly using properly cleared material or original synthesis.
4. Make 2–3 minimalist **off-white editorial typography** cards. Use a bold black sans serif, restrained hand-drawn red annotation, short lines, animated word entrance and clean corner accents. Keep the quote legible.
5. Verify captions by listening to the exact file; don't present stylized paraphrases as verbatim quotes. Preserve the question and next sentence when they materially affect meaning.
6. QA at 1x with the sound on: make sure no text overlaps, faces remain inside the crop, scene changes match speech, the release tail isn't cut, audio doesn't double, and credits remain accurate.

### Output created from the user-supplied extract

A 35.5-second portrait edit, retaining the original interview sound and using original animated typography for the central lesson. The user-provided source MP4 is **not stored in GitHub**. In the chat, the edited file is provided separately as an artifact.

## Tooling

For local use with your own caption file:

```sh
SOURCE_START=13.5 DURATION=35.5 CROP_X=820 \
  bash scripts/render-quote-short.sh input.mp4 editorial.ass out/gloc9-quote.mp4
```

This generic helper assumes a 3200×1440 source (the uploaded source in this edit). For other sources, adjust the crop dimensions in the script to the actual frame aspect and speaker position, or use the main Remotion EditorialKinetic composition from the separate in-progress PR.


## Revised motion standard (Gloc-9 V6)

The first output was rejected because it overused static editorial paraphrases, displayed words at the wrong time, and allowed some 9:16 crops to show empty studio shelves. Use the new word-reveal renderer instead:

- **No invented lower thirds or fake quotations**: text must be sourced from the audible interview, with a reviewed transcript. If a line is uncertain, do not show it as a quote.
- **Per-word keyframes**: each word has an independent entry time, short upward slide, 190 ms elastic scale and ~95 ms fade. Reveal in rolling groups of at most four words; avoid long quote cards.
- **Alternating visual modes**: clean full-screen speaker shots and a warm off-white frame with small centered words, spare black corner graphics and one restrained red underline. The supplied reference informs principles, not copied assets or branding.
- **Source audio uninterrupted**, with subtle dialogue compression and ~-16 LUFS target. Don't fabricate or clone speaker voices.
- **Camera QA**: where the 3200×1440 source switches from Gloc-9 to Kara David or archival footage, change the crop to show the actual face rather than the trophy shelf or the empty edge.
- **Review at 1x** with the source audio to validate every caption. The supplied source and publicly available transcript alone cannot establish millisecond-accurate word timing; the rough work-in-progress timing must be aligned and manually checked before claiming a publish-ready subtitle track.

### Word-by-word generator

\`scripts/generate-podcast-word-pop.py\` composes an ASS overlay from a reviewed JSON alignment manifest. It deliberately does not guess speech text or word onsets. Example manifest excerpt:

\`\`\`json
{
  "scenes": [
    {
      "start": 0.0,
      "end": 2.5,
      "mode": "speaker",
      "words": [
        {"start": 0.18, "text": "A"},
        {"start": 0.52, "text": "verified"},
        {"start": 1.14, "text": "phrase", "emphasis": true}
      ]
    }
  ]
}
\`\`\`

Then:

\`\`\`sh
python3 scripts/generate-podcast-word-pop.py reviewed-alignment.json aligned.ass
bash scripts/render-quote-short.sh authorized-source.mp4 aligned.ass out/podcast-quote.mp4
\`\`\`

These example words are placeholders, not a Gloc-9 quote. Audio-to-text transcription or human transcription and word-level time alignment remain required upstream; do not fabricate accuracy.

## Rights and publishing

Creating an edit from an uploaded clip does not necessarily grant reupload/monetization rights to the original GMA footage. Confirm permission or obtain appropriate rights guidance before public distribution. Credit is useful but is not a substitute for a license.
