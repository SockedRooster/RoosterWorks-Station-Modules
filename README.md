# RoosterWorks Station Modules

**Latest stable release: v0.7.5** | **KSP 1.12.5** | **MIT** | **SockedRooster**

Modular orbital-station parts in 2.5 m, 3.75 m, and 5 m families: habitats, command modules, science labs, greenhouses, airlocks, logistics, power, hubs, cupolas, adapters and crew tubes.

[Download v0.7.5](https://github.com/SockedRooster/RoosterWorks-Station-Modules/releases/tag/v0.7.5) · [Installation](INSTALLATION.md) · [Release notes](RELEASE_NOTES.md) · [Roadmap](ROADMAP.md)

## What's included in v0.7.5

- Expanded 5 m family and a 3.75 m-to-5 m adapter.
- Compact habitats and 4 m, 6 m and 8 m long crew tubes.
- White/Grey exterior finishes and independent ring-color selections.
- Logistics resource loadouts, laboratory science-storage tiers and five command data archive sizes.
- Improved ring synchronization, editor controls, and resource/electrical balancing.
- Existing part identifiers retained, including hidden reactor entries used by older saved craft.

**Release status:** v0.7.5 was published on October 14, 2026, and the maintainer reported in-game testing before release. The source version file uses internal build number 4, inherited from the final v0.7.5 development candidate.

## Install

Back up saves, close KSP, remove the old `GameData/RoosterWorksStationModules` folder, and install the v0.7.5 player ZIP into your KSP directory. See [INSTALLATION.md](INSTALLATION.md) for compatibility notes and optional integrations.

## Repository layout

- `GameData/` — shipped parts, models, textures, compatibility patches and runtime plugins; **do not delete hidden legacy parts or required DLLs**.
- `Source/` — editable procedural scripts, OBJ/MTL files, baseline data and development history.
- `Tools/` — build, packaging, renderer and regression-validator utilities.
- `Media/` — visual previews, screenshots and future concept art (not playable parts).
- `Docs/History/` — historical test checklists and milestone documents, plus the original pre-cleanup root documentation.
- `CHECKSUMS-SHA256.txt` — checksum manifest used by the GameData validation suite.

## Developer notes

Run `python Tools/validate.py` to check the mod with the necessary Python dependencies installed. Validation does not replace testing in KSP.

The source tree deliberately retains similarly named older models, configurations and baselines to support regression tests. Do not remove these merely because they resemble current game files.

`Tools/package_appearance.py` is the retained v0.7.5-dev.4 development packaging tool, not an automatic GitHub publisher. The tested stable player ZIP is available under [Releases](https://github.com/SockedRooster/RoosterWorks-Station-Modules/releases).

[License](LICENSE) · [Issue tracker](https://github.com/SockedRooster/RoosterWorks-Station-Modules/issues)
