# RoosterWorks Station Modules

Custom 2.5 m orbital station modules for KSP 1.12.5 with procedurally generated models, warm-white cabin lighting, optional Kerbalism life support and science features.

## Current developer test: v0.4.2 — HAB-250 Side Hatch EVA

The development package contains three modules:

- **RW-HAB-250:** 4-crew station habitat, two selectable variants: Standard Windows and Exterior Side Hatch.
- **RW-LAB-250:** 2-crew science laboratory with stock/Kerbalism experiments.
- **RW-CMD-250:** Compact 2-crew command pod with SAS, reaction wheels and antennas.

**New in v0.4.2:** The HAB previously had a visual hatch but no functional KSP airlock. The updated native HAB model adds a trigger BoxCollider tagged `Airlock` on KSP physics layer **21**, located outside the side hatch and aligned with the outward normal. The existing stock `ModulePartVariants` turns this trigger off for Standard Windows and on for Exterior Side Hatch. Blender source now displays a guide at the airlock location. No new plugin or additional part ID is required.

This is an **experimental EVA test**, not a confirmed stable fix. We need to confirm KSP recognizes the variant's airlock during part initialization, that a Kerbal aboard the HAB can exit and board again, and that EVA remains unavailable from the window-only variant. If the variant is not discovered correctly at load time, we'll revise the airlock registration mechanism.

The RW-CMD-250 communications investigation continues separately. Previous HAB window-frame fit issues are deferred. LAB/other parts are otherwise unchanged.

### Upload developer sources

Download **`RoosterWorks-Station-Modules-v0.4.2-Developer-Source.zip`** from ChatGPT. On GitHub choose **Add file → Upload files** and commit the **ZIP itself** to `main`, without extracting it. The [GitHub importer](.github/workflows/import-prototype.yml) verifies the exact archive SHA-256, imports the 67 files, validates the model and manifests, then commits the sources and removes the temporary ZIP.

The separate **`RoosterWorks-Station-Modules-v0.4.2-TEST.zip`** is the player test installer. To install, remove the old `GameData/RoosterWorksStationModules` folder and extract the test ZIP into the KSP root. Launch a *new* craft with a crewed HAB in Side Hatch mode and test EVA/boarding from both the ground and orbit. The built-in 2.5m top/bottom endcaps are not separate docking ports.

**Status:** Static model and config checks pass; actual EVA and Kerbalism runtime behavior remain to be confirmed. Custom IVA interiors planned later. Original RoosterWorks work is MIT licensed.
