# RoosterWorks Station Modules

Code-generated, textured KSP 1.12.5 station components, with Kerbalism-aware life-support and science integration.

## v0.3.0 DEVELOPMENT TEST — 2 station parts

- **RW-HAB-250:** 2.5 m, four-Kerbal habitation module. The earlier v0.2.7 exterior, warm-white lights, window and Side Hatch variants are **unchanged**, including the deferred window/hatch frame-fit refinement.
- **RW-LAB-250:** NEW 2.5 m, two-scientist laboratory. Independent original mesh with a smaller three-window observation row, science instrument cassettes, optical scanner, radiators, white thermal panels and RoosterWorks branding. Stock science processing works via standard stock lab modules; a conditional Kerbalism configuration replaces stock research with sample analysis and adds Default-profile supplies.

**No stable release yet.** Native models, config static checks, Blender-editable source, and actual-mesh lab renders are in the developer ZIP. Live VAB / Kerbalism science tests remain outstanding.

### Upload the prepared development source

1. Download the exact `RoosterWorks-Station-Modules-v0.3.0-Developer-Source.zip` from the ChatGPT conversation.
2. On this repository, choose **Add file → Upload files** and commit **the single ZIP as-is** to `main`. Do not extract it.
3. The [import workflow](.github/workflows/import-prototype.yml) validates the ZIP SHA-256 and 51 approved files, then extracts both GameData models, all source and media, runs Python validation, commits the files, and removes the upload ZIP.
4. Use the separate `RoosterWorks-Station-Modules-v0.3.0-TEST.zip` to install **both** parts in KSP; remove old `GameData/RoosterWorksStationModules` first.

The final source `README.md` includes full installation, dependencies, and design limitations. Interiors will be added later.

[Repository](https://github.com/SockedRooster/RoosterWorks-Station-Modules) · MIT licensed original RoosterWorks content.
