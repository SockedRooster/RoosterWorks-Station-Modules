# Install RoosterWorks Station Modules v0.7.5

**Stable player release:** [v0.7.5 for Kerbal Space Program 1.12.5](https://github.com/SockedRooster/RoosterWorks-Station-Modules/releases/tag/v0.7.5)

1. Exit KSP and back up saves and craft files.
2. Remove the previous `GameData/RoosterWorksStationModules` directory rather than merging old files.
3. Extract `RoosterWorks-Station-Modules-v0.7.5.zip` into the KSP installation directory.
4. Verify `GameData/RoosterWorksStationModules/` contains `Parts/`, `Models/`, `Compatibility/` and `Plugins/`.
5. Restart KSP and verify existing craft and resource settings before using an upgraded save.

**Integrations:** Kerbalism Default compatibility is conditional on an installed compatible Kerbalism setup. VAB Organizer and B9PartSwitch editor integrations are optional where supported. ModuleManager is needed to apply ModuleManager patches. Resource features that use Community Resource Pack resources also require compatible CRP data. Third-party dependencies are not included in the player archive.

**Existing saves:** All legacy part identifiers needed for saved craft are retained, including historical reactor parts hidden in the editor. Never delete them as apparent clutter. Existing vessels can retain serialized capacities or variants after updates; compare against a newly placed part if necessary.

The [release notes](RELEASE_NOTES.md) describe the shipped features. Instructions for older testing candidates are archived under [Docs/History](Docs/History/).
