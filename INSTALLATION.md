# Install RoosterWorks Station Modules v0.6.0-dev.1

1. Quit KSP 1.12.5, back up saves, and retain the previous **v0.5.3-rc.1** player archive for rollback.
2. Remove the old `GameData/RoosterWorksStationModules` folder entirely. Copy the `GameData` directory from this **player test ZIP** to the game's KSP root. Don't nest an extra GameData folder.
3. Remove obsolete external `CMD250_CommNet_Diagnostic_A.cfg`, if installed; it overrides the tested CMD transmitter setup.
4. Restart KSP and build a *new* test craft. HAB/CMD appear in Pods, LAB under Science, HUB under Structural, and CUP under Utility. Search `RoosterWorks` or `RW-CUP-250`.
5. Attach the new **RW-CUP-250 via its bottom 2.5 m stack node**. The glass crown is a terminal end and has no stack node. Add a separate CMD for command and HAB Side Hatch for exterior EVA access.
6. If Kerbalism + the matching profile/features are installed, the cupola receives conditional supplies and habitat volume. These dependencies are not bundled. Stock installs are supported.

Follow `TEST_CHECKLIST-v0.6.0.md` to test and report the new cupola plus preserved modules. For any loading/config issue supply KSP.log and GameData/ModuleManager.ConfigCache.

**Important:** Test builds are not save-compatible guarantees. Removing this addon while loading vessels that use it can delete those craft from a save. Preserve save backups and the previously working ZIP.
