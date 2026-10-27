# Third-party notices and licensing

This project uses [Remotion](https://github.com/remotion-dev/remotion) and includes code and assets from other sources. There is **no repository-wide MIT license** in this project, and the old root `LICENSE` should not be taken as a license for all code in `urfavxbf/video-ai-editor`.

## Imported motion-effects code

The initial motion-effects foundation was imported from:
- [JesseEisenbart/video-effects-skill](https://github.com/JesseEisenbart/video-effects-skill), via [urfavxbf/video-effects-mobile](https://github.com/urfavxbf/video-effects-mobile).
- This includes components in `src/fx/` and associated imported scripts, tools, configurations, and editing helpers.

The source repository published that code under the MIT License. The full copyright and license notice for those imported portions is preserved at [licenses/video-effects-skill-MIT.txt](licenses/video-effects-skill-MIT.txt), as required by its license. This notice applies to the applicable imported code and modifications of it; it does **not** assign ownership of later independent additions or declare the entire repository MIT-licensed.

**Provenance clarification:** Building effects with Remotion or importing Remotion packages does not establish that these effects were copied from the Remotion monorepo. This project makes no claim that the third-party author created the underlying Remotion framework.

## Official Remotion Agent Skills

The repository also vendors 12 official skills and their reference materials from [remotion-dev/skills](https://github.com/remotion-dev/skills). The exact pinned source commit is recorded in [docs/REMOTION_SKILLS_SOURCE_COMMIT.txt](docs/REMOTION_SKILLS_SOURCE_COMMIT.txt). These materials are upstream Remotion content, not original code authored by this repository, and are not represented as MIT-licensed. Follow the publisher's applicable terms.

## Remotion framework

The `remotion` and `@remotion/*` dependencies come from [remotion-dev/remotion](https://github.com/remotion-dev/remotion), which publishes its **own license** at [LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md). Remotion is not generally MIT-licensed. Review its eligibility and commercial usage rules separately.

We consume Remotion as npm dependencies; we do not relicense it by including this project in a repository.

## Optional VoxCPM2 speech model

The integration script `scripts/voxcpm_voiceover.py` calls the [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) Python package and the `openbmb/VoxCPM2` model. No VoxCPM2 weights or upstream sources are bundled here. OpenBMB publishes its model and code under the **Apache-2.0** license, which applies to those external components; comply with its upstream notice and permitted-use requirements. This does not license the rest of Video AI Editor under Apache-2.0.

## Bundled fonts

Inter, Montserrat and Caveat in `public/fonts/` retain their separate [SIL Open Font License notice](public/fonts/OFL.txt).

## Sound effects and other assets

The sound effects under `public/sfx/` came with the imported effects project. Its archived README describes their production and use; see [docs/UPSTREAM_README.md](docs/UPSTREAM_README.md). That description alone is not a substitute for evaluating any distribution and commercial-use rights that apply to generated audio assets.

## Original work added here

The independent additions, including the Dudut editing compositions, original Doorway Effect composition, automation workflows, and editorial scripts, are not licensed solely by the imported MIT notice. No new project-wide open-source grant is made by this notices file.

The historic Git commit record preserves prior files and their notices, including the formerly present top-level `LICENSE`.
