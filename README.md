# RoosterWorks Station Modules

Original station modules for **Kerbal Space Program 1.12.5**, with optional Kerbalism integration.

## Latest development build: v0.6.0-dev.1

The latest developer kit contains **five** 2.5 m station modules: **RW-HAB-250**, **RW-LAB-250**, **RW-CMD-250**, **RW-HUB-250**, and the newly added **RW-CUP-250 panoramic observation cupola**.

The HAB/CMD/LAB/HUB models and runtime hatch plug-in were preserved from the v0.5.3-rc.1 development candidate. The new cupola has eight sloped windows, an overhead viewport, one crew seat, a 2.5 m bottom attachment, optional Kerbalism habitat resources and stock-compatible lighting. The cupola and the newer HUB/endcap work still need in-game validation; this is **not a stable published release**.

### Import the complete source tree to this repository

This repository uses a single-ZIP import because the source package contains large native KSP **.mu models**, textures, DLL, editable OBJ geometry, Blender reconstruction scripts, and model preview renders.

1. Download [`RoosterWorks-Station-Modules-v0.6.0-dev.1-Developer-Source.zip`](https://chatgpt.com/) from the current ChatGPT conversation (the ZIP is attached there).
2. In GitHub open this repository's **main** branch and select **Add file → Upload files**.
3. Upload **the single developer-source ZIP without extracting it**, and commit the upload to `main`.
4. The [import workflow](.github/workflows/import-prototype.yml) verifies the exact SHA-256 and 113 approved source paths, extracts and statically validates the five-module source, commits the actual assets, and removes the temporary ZIP.

**Exact ZIP SHA-256:** `2ecaa133ee427115838563abadb1502c25e6d3b53ef46b98e27c9186ceb306fe`

Do **not** upload the KSP install/test ZIP; it is not the developer source.

After the import, `GameData/`, `Source/`, `Tools/`, `Media/` and their binary assets will appear directly in this repository. This does not create a GitHub release or tag.

For in-game tests, install the separate `RoosterWorks-Station-Modules-v0.6.0-dev.1-TEST.zip`, keeping your existing tested saves backed up.

Licensed MIT. All RoosterWorks art and code are original; additional dependencies remain governed by their own licenses.
