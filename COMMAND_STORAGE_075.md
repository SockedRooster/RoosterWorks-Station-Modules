# Command archives — v0.7.5-dev.4

RW-CMD station command cores use independent Kerbalism editor data capacity
choices, starting at 200 MB and reaching 1 GB at 2.5 m. Larger cores scale by
volume, matching the science-module scaling rule (×3.375 and ×8).

| Diameter | Starting data | Maximum data | Selectable MB steps |
|---|---:|---:|---|
| 2.5 m | 200 MB | 1000 MB / 1 GB | 200, 400, 600, 800, 1000 |
| 3.75 m | 675 MB | 3375 MB / 3.375 GB | 675, 1350, 2025, 2700, 3375 |
| 5 m | 1600 MB | 8000 MB / 8 GB | 1600, 3200, 4800, 6400, 8000 |

Decimal MB/GB. Kerbalism may round display labels; internal capacities are exact.
The native HardDrive selector is used, retaining its mass/cost modifiers and
save behaviour. Sample storage is unchanged. Only RW_CMD_250/375/500 are targeted;
crewless rounded RW_HUB junctions are not command/science cores.

The late ZZZCommandStorage075.cfg FINAL patch overrides historic fixed command
limits after StorageBalance.cfg and Family500.cfg. LAB tiers and the dev3 ring
hotfix remain intact. Original models, textures, plugins and configs remain
byte-identical; one patch and version metadata change. Source builder:
Source/build_command_storage.py; included in Tools/build-expansion.py.

Existing launched flight archives retain their saved capacity and stored data;
no migration/reset/deletion is performed. An old editor craft's non-tier
capacity is reset to the native starting tier on editor load. Choose its desired
capacity and save again. New command parts start at the minimum tier.

## Live acceptance checklist

- CMD250 offers 200/400/600/800/1000 MB independently selectable data capacity.
- CMD375 and CMD500 offer the exact scaled choices in the table.
- Editor save/reload and symmetry preserve selected tiers; mass/cost update.
- LAB data/sample tiers, rings, White/Grey surface, reactors, lighting and all
  existing functions remain available.
- Existing flight vessel archives/contents remain intact.

Offline validation and archive checks passed when packaged; these VAB/SPH and
flight checks remain pending. No game install/save edits or GitHub publication.
