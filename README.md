# RoosterWorks Station Modules

Original Kerbal Space Program 1.12.5 station modules with procedural native assets, optional Kerbalism supplies, and stock cabin lighting.

## Latest development test — v0.4.1

Contains RW-HAB-250, RW-LAB-250 and the compact **RW-CMD-250** station command deck.

**v0.4.1 command-control diagnostic fix**: the RW-CMD-250 previously had only a DIRECT 5 Mm transmitter and allowed hibernation. We've added a separate INTERNAL 500 k telemetry antenna, disabled hibernation and explicitly enabled non-pilot crew authority, while retaining remote telemetry requirements, SAS, reaction wheel and the direct transmitter. **This is a candidate fix, not yet confirmed in-game.** The user previously reported a powered, crewed station with no signal or Kerbin control.

All other existing models, lighting, science and Kerbalism resource configurations are unchanged. RW-LAB-250 retains native Kerbalism science modules and the stock science fallback; HAB window-frame cleanup remains deferred.

### Import the developer source ZIP to GitHub

Download the exact **`RoosterWorks-Station-Modules-v0.4.1-Developer-Source.zip`** from ChatGPT. In this repository choose **Add file → Upload files**, then upload **the single ZIP (do not extract it)** to the `main` branch. The [import workflow](.github/workflows/import-prototype.yml) verifies the archive hash, extracts 66 approved developer/source/GameData files, runs validation and commits the verified files while removing the temporary ZIP.

Use the separate **`RoosterWorks-Station-Modules-v0.4.1-TEST.zip`** to test in KSP. Remove the previous `GameData/RoosterWorksStationModules` folder first; test a **new craft** to avoid persistent old module state. Examine the CommNet icon and Control/Communication sections. If signal still fails, provide the final `ModuleManager.ConfigCache` entry for `RW_CMD_250` and the relevant KSP log messages.

**Development/testing only.** No stable release or KSP runtime validation yet. Original RoosterWorks code/models are MIT-licensed. Custom IVAs are planned later.
