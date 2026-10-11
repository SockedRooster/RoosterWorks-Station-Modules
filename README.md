# RoosterWorks Station Modules

Code-generated KSP 1.12.5 station habitats, with original textured meshes, optional Kerbalism life-support storage, and Blender-editable source.

## Current prototype: RW-HAB-250 v0.2.5 (not a stable release)

Our first part is a 2.5 m, four-crew habitat with **50%-larger square windows**, **flush slim end rings**, an original RoosterWorks rooster emblem, and two VAB variants (**Standard Windows** / **Exterior Side Hatch**).

**New in v0.2.5:** A stock **Toggle Cabin Lights** control (VAB and flight, default Lights action group) switches the window material between dark glass and a soft **warm-white glow**. Extra curved fairings improve the top/bottom mounting of the hatch and window frames.

**Important limitations:** This version does **not** yet consume ElectricCharge for lighting or shut off at low power. The side hatch is cosmetic, not a verified EVA airlock. Custom IVA interiors come later. In-game light state, thermal overlays, and variant switching still need testing.

### Upload the approved source archive to GitHub

1. Download the exact `RoosterWorks-Station-Modules-v0.2.5-Developer-Source.zip` from ChatGPT.
2. Use **Add file → Upload files** to upload that single ZIP, without extracting it, and commit it to this repository's `main` branch.
3. The [source import workflow](.github/workflows/import-prototype.yml) checks the approved ZIP SHA-256, extracts the 34 developer assets, validates the model and its manifest, then commits them to `main` and removes the temporary ZIP.

The separate `RoosterWorks-Station-Modules-v0.2.5-TEST.zip` is the KSP test installer, **not** the GitHub source upload.

### Long-term roadmap

2.5 m labs, cupolas, logistics and station junctions; 3.75 m Frontier series and larger 5 m / 7.5 m integration. Custom interiors later.

All original RoosterWorks material is MIT-licensed. No third-party game assets are distributed.
