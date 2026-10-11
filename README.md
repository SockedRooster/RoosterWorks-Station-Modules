# RoosterWorks Station Modules — development

Custom KSP 1.12.5 space station habitats and service modules, featuring original models, procedurally generated textures and optional Kerbalism life-support integration.

## Current design-review model — RW-HAB-250 v0.2.0

We're **developing one part first**: the 2.5 m, four-crew **RW-HAB-250** orbital habitat, with realistic ceramic hull paneling, dark graphite frames, bronze trim, recessed windows, service-bay details, handrails and RoosterWorks branding.

**Important exterior change:** the top and bottom endcaps are **flush integrated bulkheads** rather than axially projecting collars. The attachment planes match the physical ends at `Y = ±1.98 m`. These are *not* built-in docking ports.

**Prototype status:** Static source checks pass. Actual Blender/KSP runtime tests and final visual approval are still pending. Custom IVA interiors are later work. Kerbalism storage is conditional on the Default profile and must be validated in-game.

### One-ZIP GitHub source import

1. Download the exact **`RoosterWorks-Station-Modules-v0.2.0-Developer-Source.zip`** package from ChatGPT.
2. Upload the single ZIP (do **not** extract) through **Add file → Upload files** in the repository and commit to `main`.
3. GitHub Actions automatically verifies its fixed SHA-256, imports the 28 source/render/asset files, runs static validation, and deletes the temporary ZIP from `main`.

The separate **`RoosterWorks-Station-Modules-v0.2.0-TEST.zip`** is the player installer for VAB testing, not the developer source import.

Once imported, see the comprehensive root README and `Media/RW-HAB-250-v0.2.0-Review-Render.png` for further instructions.

### Future catalog

Only after approving RW-HAB-250: 2.5 m lab, cupola, logistics, junction and Frontier modules (3.75 m, 5 m, 7.5 m). Add custom interiors later.

MIT licensed for original RoosterWorks files. No third-party KSP game assets or Kerbalism binaries are included.
