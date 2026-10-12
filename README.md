# RoosterWorks Station Modules

Original 2.5 m KSP 1.12.5 station habitat prototypes with procedural native `.mu` assets, optional Kerbalism storage, and Blender-editable geometry.

## Current test build — RW-HAB-250 v0.2.7

**Geometry root-cause fix:** v0.2.6 used a wide eight-corner window foundation. Its triangular faces cut straight across the curved hull, resulting in flying white side wings and incomplete top/bottom frame contact in the VAB. v0.2.7 rebuilds the mounting foundation from finely segmented **cylindrical contours** and removes stacked cosmetic filler trim and exposed stand-offs.

The **50% enlarged square windows, both Standard Windows and Side Hatch variants, working warm-white light toggle, rooster emblem, slim end rings, 4-crew capacity and Kerbalism patches** are preserved.

The Side Hatch remains **visual-only**, without a confirmed EVA airlock; cabin lights currently have no EC drain/automatic cutoff. The new model passed static tests and angled offscreen render review but **still requires a VAB test**.

### Developer source import

Download the exact `RoosterWorks-Station-Modules-v0.2.7-Developer-Source.zip` from our ChatGPT conversation and upload **the single ZIP without extraction** to the GitHub repo `main` branch using Add file → Upload files. GitHub Actions verifies the known SHA-256, unpacks all 35 source/render/GameData files, checks the native model and manifests, commits the extracted files and deletes the ZIP from the branch.

The `RoosterWorks-Station-Modules-v0.2.7-TEST.zip` is for actual KSP installation, not the GitHub source import. Always remove the prior `GameData/RoosterWorksStationModules` folder before installing a test ZIP.

MIT licensed, original RoosterWorks assets. Future Station Modules: 2.5m labs, cupolas, hubs, logistics, and larger Frontier habitats. Custom IVA interiors later.
