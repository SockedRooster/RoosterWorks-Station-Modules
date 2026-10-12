# RoosterWorks Station Modules

Original KSP 1.12.5 station habitats, science laboratories and compact command modules with optional Kerbalism life-support and science integration.

## Current testing candidate: v0.4.3

Three parts: **RW-HAB-250**, **RW-LAB-250**, and **RW-CMD-250**.

### v0.4.3 development notes

- **EVA hatch registration:** The game scans active Airlock-tagged colliders during Part.Awake. The native HAB model already contains the airlock trigger, but the Standard Windows variant disabled it. This version leaves the physical collider active across visual variants to permit KSP initialization. **Temporary limitation:** EVA may be possible from the cosmetic Standard Windows variant at an invisible hatch position.
- **CMD signal diagnostic:** Adds a stock `ModuleProbeControlPoint` requiring one crew member, following station control-module conventions. The separate direct/internal transmitters, SAS and existing command functions remain in place. **Signal restoration is not yet confirmed.**
- The HAB's remaining curved window-frame visual refinement remains deferred. LAB science, warm-white lights, part sizes, Kerbalism supplies and graphics are otherwise unchanged.

### Upload the tested developer source

Download **`RoosterWorks-Station-Modules-v0.4.3-Developer-Source.zip`** from ChatGPT and upload this **single ZIP without extracting it** to the `main` branch using **Add file → Upload files**. The GitHub import workflow verifies the file's known checksum and 67-entry contents, runs static tests and commits the extracted source and GameData files, deleting the temporary ZIP afterward.

The separate **`RoosterWorks-Station-Modules-v0.4.3-TEST.zip`** is for testing inside KSP, not for GitHub source import.

### Test procedure

1. Remove the previously installed `GameData/RoosterWorksStationModules` folder **and any separately installed `CMD250_CommNet_Diagnostic_A.cfg`** from the earlier isolation test.
2. Install the v0.4.3 TEST ZIP, restart KSP, and use a fresh craft.
3. Test EVA **from a Kerbal seated in RW-HAB-250**, with Exterior Side Hatch selected and a clear exit.
4. Test a fresh RW-CMD-250 near KSC with a crew member, **without another probe core**. Check stock CommNet signal and Kerbalism signal. Repeat uncrewed.
5. If either issue persists, supply the full `ModuleManager.ConfigCache` entry for the part and relevant `KSP.log` entries. This prevents further speculative changes.

This is a development test and not a stable published release. The original RoosterWorks assets and code are MIT licensed. Custom IVA interiors are deferred.
