# RoosterWorks Station Modules v0.6.0-dev.2 — in-game test checklist

**Development build only.** The stable release candidate **v0.5.3-rc.1** remains unchanged and unpublished. This package adds the separate RW-CUP-250 observation cupola.

## Prerequisites

- KSP 1.12.5; optional Kerbalism + ProfileDefault/FeatureHabitat.
- Delete the previous `GameData/RoosterWorksStationModules` folder first and install the supplied `GameData` directory as one replacement.
- Remove any historical `CMD250_CommNet_Diagnostic_A.cfg` patch.
- Build a new test craft; don't use this development build on the only copy of a career save.

## Cupola checks

- [ ] Locate `RW-CUP-250` in Utility/crew-related categorization.
- [ ] Attach its **single 2.5 m bottom node** onto HAB/CMD/LAB or any HUB-250 branch; confirm it sits flush with the mating ring.
- [ ] Inspect all **eight vertical mullion-to-header joints** at the top and bottom in VAB, including tight grazing angles; confirm there are **no open gaps or detached floating trim**.
- [ ] Look at the crown fasteners, thicker lower retaining ring and recessed dark inner frame strips: confirm no z-fighting, excessive visual clutter or transparent holes.
- [ ] Inspect the eight angled tinted windows, top skylight and RoosterWorks crest from multiple VAB viewpoints.
- [ ] Check rotation and node orientation when mounting radially through a separate hub face.
- [ ] Place one crew member in the cupola; confirm the portrait and stock temporary `cupolaInternal` IVA work.
- [ ] Confirm that **no standalone vessel controls, EVA exit or docking port** are advertised for the cupola.
- [ ] Toggle Observation Cabin Lights (editor and flight). This visual toggle does not currently consume EC.
- [ ] In flight test crew transfer to/from an attached HAB via its established Side Hatch. The cupola has no external hatch.
- [ ] If Kerbalism is enabled, verify Habitat 6.2 m3 / surface 17 m2, supplies added only under ProfileDefault, and pressure calculations.

## Regression checks on preserved modules

- [ ] HAB Side Hatch EVA and grab/boarding; Standard Windows intentionally prevents EVA.
- [ ] CMD standalone CommNet signal and SAS on a fresh craft.
- [ ] LAB science panel and Kerbalism experiments/storage.
- [ ] HUB all six nodes, symmetry, resource flow, crew transfers and Kerbalism atmosphere.
- [ ] New endcap appearance and seam matching across HUB/HAB/LAB/CMD/CUP.

If any test fails, provide the symptom, VAB/flight screenshot, `KSP.log` and `GameData/ModuleManager.ConfigCache`. New cupola features have only offline/native checks so far.
