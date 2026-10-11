# RoosterWorks Station Modules

Procedurally modeled and textured space station modules for KSP 1.12.5 with optional Kerbalism life-support storage.

## Current development build — RW-HAB-250 v0.2.3

**First habitat only:** a 2.5 m, four-crew orbital module with larger square pressure windows (50% wider and taller than v0.2.2), **slimmer flush connection rims**, and two stock KSP part variants: **Standard Windows** or **Exterior Side Hatch**. The side hatch replaces a single lower window bank; no second part ID is created.

The **Side Hatch** is a cosmetic prototype, **not yet a tested functional EVA airlock**. Full custom interiors are also a later phase. The conditional Kerbalism resource patches are unchanged.

### Import the complete model/source package

The repository import workflow is configured for the exact `RoosterWorks-Station-Modules-v0.2.3-Developer-Source.zip` asset supplied in ChatGPT. To populate the repository:

1. Download the developer ZIP **without renaming it**.
2. Open this repository on GitHub and use **Add file → Upload files** to commit the **single ZIP** on `main`; do not extract it first.
3. GitHub Actions will check the fixed SHA-256, unpack the 31 approved source/asset files, run the geometry and checksum tests, commit the files to the repository, and remove the temporary ZIP.
4. The imported README then includes KSP installation and Blender instructions. The separately supplied `RoosterWorks-Station-Modules-v0.2.3-TEST.zip` is the KSP installer, **not** the GitHub upload.

**Current status:** models and configs are packaged, but the gameplay model is not yet present on GitHub until the developer ZIP is uploaded and the import Action succeeds.

### Long-term lineup

2.5 m habitation, lab, logistics, cupola and junction modules; 3.75 m Frontier series; larger 5 m and 7.5 m integration. Custom IVAs later.

MIT-licensed original RoosterWorks materials. No third-party Kerbalism binaries or textures.
