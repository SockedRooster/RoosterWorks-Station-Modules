# RoosterWorks Station Modules

Original code-generated space station modules for Kerbal Space Program 1.12.5, with optional Kerbalism-compatible life-support storage.

## Current prototype: RW-HAB-250 v0.2.2

The **RW-HAB-250**, our first model, is a 2.5 m, four-Kerbal habitat. The latest prototype uses **three square recessed pressure windows per bay**, thick white bevels, smoked gray-green glass, and flush end bulkheads that do not protrude beyond the structural shell.

The v0.2.2 native KSP `.mu`, nine textures, editable OBJ and Blender reconstruction generator are packaged in the source ZIP. **This is a TEST build, not a published stable release**. Existing part ID, crew settings, mass and Kerbalism resource patches are preserved; actual in-game validation is pending.

### Import prepared source to this GitHub repository

1. Download the `RoosterWorks-Station-Modules-v0.2.2-Developer-Source.zip` file supplied in our ChatGPT conversation.
2. In this repository select **Add file → Upload files**, upload **the single ZIP with its exact filename** to `main`, and commit.
3. The [import workflow](.github/workflows/import-prototype.yml) verifies the approved ZIP hash, extracts 28 source/assets/documentation files, runs static tests and commits them to `main`, removing the temporary ZIP.
4. When the import succeeds, the root `README.md` is replaced by detailed installation, Blender rebuild and testing instructions. The separate `RoosterWorks-Station-Modules-v0.2.2-TEST.zip` is for KSP installation, not source import.

**Note:** No gameplay files have been committed until the source ZIP is uploaded and this workflow succeeds.

### Future plans

A cohesive range of 2.5 m, 3.75 m and larger station habitats, labs, command, cupola, docking and logistics parts. Interiors are a later phase. Retain compatibility with RoosterWorks Station Support for larger stations.

MIT — original RoosterWorks models and source; no third-party KSP game assets included.
