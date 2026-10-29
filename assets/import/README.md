# One-file activation of the selected character PNGs

The 13 standalone transparent PNGs are currently delivered in the user's verified `UrFavXBF_PIX_13_Pose_Production_Pack.zip` (11.5 MB).

**To finish the GitHub binary installation, upload exactly this ZIP into this folder on branch** `feat/official-pixel-pose-default-20261029`, using GitHub's `Add file → Upload files` UI (the folder exists because this README is tracked):

`assets/import/UrFavXBF_PIX_13_Pose_Production_Pack.zip`

A no-cost GitHub Actions workflow, `.github/workflows/install-pixel-pose-pack.yml`, will:
1. Validate all 13 exact original 1254×1254 RGBA PNGs by SHA-256.
2. Stage them at `public/characters/pixel-default/{character}/{pose}.png`.
3. Typecheck and render the actual `PixelProductionProof` Remotion composition.
4. Mark the registry as `runtime_assets_ready=true` **only after** the smoke still succeeds.
5. Commit all verified PNG binaries to this branch and remove the import ZIP to avoid committing duplicate binaries.

If any check fails, the action stops before declaring the characters ready.

No new random character artwork, no crop from the owner's reference sheet, no paid APIs/GPU, no auto-publish or merge. The active defaults remain the selected independent pixel-art poses.

**Current state:** Before the ZIP lands on GitHub, image binaries remain absent from the branch. Green code CI does not mean production assets are installed. A local MP4 validation sample can be produced with the exact files separately; it is not the same as the Remotion GitHub render.
