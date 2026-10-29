# Rigged 3D replacement — 2026-10-29

The previous UrFavXBF and PIX PNG character models were **not committed** to GitHub: the old paths were placeholders pointing at unavailable render-workspace files. Their active paths were removed from `characters/registry.json` and replaced with the **two actual original glTF 2.0 models** below. Historical 2D review tools remain in the repo solely to avoid destroying old test/render work; they are not an authorized model source for new productions.

## New 3D files
- `public/characters/3d/urfavxbf.gltf` — genuine 3D chibi man: black/green spiked hair, green eyes, neon X headphones, dark-green cyber hoodie, dark cargo pants, green trainers; moving head, mouth, arms and legs.
- `public/characters/3d/pix.gltf` — genuine 3D cat: ice-cyan fur, pink inner ears, purple eyes, cyber headphones, glowing collar, muzzle, paws and tail; moving head, mouth, legs and tail.
- `scripts/build-3d-models.mjs` — zero-dependency deterministic generator. Run `node scripts/build-3d-models.mjs` to rebuild both models.

These are **first-pass low-poly geometric models**, deliberately not illustrations pasted on flat planes. They have *independently articulated rigid-transform node hierarchies*, not deformable skinned mesh weights, and embedded named glTF animation clips (walking, talking, pointing, running, jumping, laughing, etc.). Timing is illustrative; **precise audio lip-sync is not implemented**. The models are editable and importable in Blender and glTF viewers; Remotion direct 3D playback still needs a glTF/R3F scene integration. Never describe the models as final, source-image-identical or video-render-verified without actual inspection.

## Voice and budget
English Chatterbox defaults are unchanged; Tagalog GPU generation remains disabled. No paid API, GPU subscription, external asset credits or copied IP are required.

## Validation
Run `node scripts/build-3d-models.mjs` and `python -m unittest tests/test_3d_models.py -v`; the test checks nodes, unique character identity, real geometry, embedded animation tracks, valid glTF buffer offsets and the active model selection. 3D visual review and production composition are separate acceptance gates.
