# Roadmap 0.75 — editor and storage update (v0.7.5-dev.2)

41 current native models/parts; two hidden reactor IDs retained for old craft.
No installation, save modification, GitHub commit or publication performed.

## Long straight crew tubes

| Diameter | Existing length | New long length | New ID |
|---|---:|---:|---|
| 2.5 m | 2 m | 4 m | RW_TUBL_250 |
| 3.75 m | 3 m | 6 m | RW_TUBL_375 |
| 5 m | 4 m | 8 m | RW_TUBL_500 |

Endcaps, badge proportions, diameter and weathered shell style retained. Twice
the mass, cost, entry cost and interior volume of the corresponding short tube;
surface area recalculated. Crewless, no seats/IVA/EVA/supplies, pressure support
conditional on Kerbalism and passability on Connected Living Space. In VAB
Station Connectors when VABOrganizer is present; Structural fallback.

## Independent LAB data and sample selectors

| Size | Data starting / maximum | Samples starting / maximum |
|---|---|---|
| 2.5 m | 250 MB / 2500 MB (2.5 GB) | 10 / 100 |
| 3.75 m | 843.75 MB / 8437.5 MB (8.4375 GB) | 34 / 338 |
| 5 m | 2000 MB / 20000 MB (20 GB) | 80 / 800 |

Ten steps each; capacities scale by pressure volume (1 / 3.375 / 8). Each sample
step rounds independently to a whole slot, half upward: 3.75 m choices are
34, 68, 101, 135, 169, 203, 236, 270, 304, 338. Data follows decimal MB/GB.
Kerbalism may format display labels differently. Higher capacity retains native
Kerbalism mass/cost modifiers. Only LAB modules change; command archives remain
at their accepted 2.5 GB limits. ScienceTier adapter preserves selected rounded
slot capacities through editor reload. Flight archives/content are never reset
or resized; existing launched vessels retain their saved drive and contents.
An old editor LAB configuration at a non-tier capacity resets to native starting
data/sample choice on load; select the desired capacity and save it again.

## Editor part menu

Appearance groups Surface and Rings near the other visual controls. Optional
B9PartSwitch gives two/eight color swatches matching the supplied SSPX example.
Existing White/Grey and ring selection controllers continue applying materials;
the B9 modules manage no materials, resources, geometry or hardware. Saved color
choices initialize the swatches, not the other way round. With B9 absent, the
original text selectors remain available in the Appearance group. Flight color
restoration continues through the established modules; no cosmetic editor
switches are added in flight. Stock reactor variants retain independent Hardware
controls. Lighting and inventory controls are grouped and collapsed initially.
Science, Habitat, Reliability, Configuration, Processes and resource controls
retain their native functions. Stock resource sliders remain at the bottom.

## Source/rebuild

`Source/build_long_tubes.py` rebuilds the three new native .mu/OBJ/MTL exports.
`Source/build_editor_options.py` generates the cosmetic and science patches.
`Source/EditorMenu.cs` compiles with `Tools/build-editor-runtime.ps1` against KSP's
installed managed assemblies; it has no B9/Kerbalism assembly dependency.
`Tools/build-expansion.py` includes the new builders and refreshes checksums.
Existing original model and gameplay files remain byte-identical except added
ring registrations and version metadata. The late ZZZ science patch overrides
the retained historic fixed-capacity patches without erasing development history.

References: [Kerbalism HardDrive](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Modules/HardDrive.cs),
[B9 switcher controls](https://github.com/blowfishpro/B9PartSwitch/wiki/ModuleB9PartSwitch).

## Live acceptance checklist (pending)

- Find all three long tubes, connect both ends, switch finish/ring colors, inspect
  readable badges, sealed interfaces, symmetry copies and pressure/CLS paths.
- LAB250 begins at 250 MB/10 slots and independently selects through 2500 MB/100.
  LAB375 and LAB500 offer the exact table above; check mass/cost updates.
- Save/reload a LAB375 at 338 slots; check it stays 338. Repeat other tiers.
- Save/reload existing Grey/Green parts; swatches match actual surfaces. Test
  symmetry and copied parts, HAB hatch choices and battery/reactor hardware.
- Appearance, Lighting and Inventory groups display correctly in VAB/SPH;
  test B9 installed and absent. Native resource and experiment controls work.
- Load an existing flight vessel: science archives, stored samples, fuel,
  batteries, supplies, pressure and saved appearance remain intact.
- Ground 0.8/0.9 concept sheets are the accepted direction; they remain plans.
