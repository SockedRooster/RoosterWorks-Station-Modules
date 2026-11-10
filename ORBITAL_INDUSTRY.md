# Orbital industrial modules — v0.7.5-dev.11 TEST

Four 2.5 m station parts, each 2.4 m long along the station Y stack axis,
with matching supported industrial equipment on both sides. Uses the station
shell, independent White/Grey finish and ring colors, and role-specific labels.
Two integrated size-2 docking ends have strong acquisition, permanent crossfeed,
manual release and disabled staging. Docking menus show the connected part's
name; naming/force/reference controls are hidden on these four industrial parts.
All appear in **Utility / Station Utility** with VABOrganizer.

| Part | Role | Cargo capacity | Default empty price |
|---|---|---|---:|
| RW-ISRU-250 | Stock Ore refinery: LF+Ox, LF, Oxidizer or Monopropellant | Ore 300; EC 1000 | 14,000 |
| RW-NST-250 | Nuclear materials vault | Uraninite 1000; RW feedstock 500; EnrichedUranium 200; DepletedFuel 200; EC 500 | 24,000 |
| RW-CEN-250 | Fuel centrifuge | RW feedstock 250; EnrichedUranium 40; DepletedFuel 200; EC 1500 | 68,000 |
| RW-NSM-250 | Nuclear smelter | Uraninite 250; RW feedstock 250; EC 1000 | 36,000 |

Cargo starts empty; EC starts full. Configured prices account for KSP's
empty-tank subtraction, so adding cargo increases price normally. Dry masses,
capacities, converter rates and thermal settings match the ground equivalents.
The duplicated exterior equipment is one processor/storage part, not doubled
capacity. Crewless utility modules: no habitat, Shielding resource or reactor.

## Processing

Supply Ore from a miner/cargo vessel to the ISRU. Its four stock converters,
engineer bonuses and core-heat controls are retained. Provide external power,
active radiators and separate destination fuel tanks. The installed generic
Kerbalism/SystemHeat bridge may adapt these stock converters as before.

The nuclear chain shares the ground set's fictional gameplay feedstock:

- NSM: 0.02 Uraninite/s + 60 EC/s → 0.01 RW Nuclear Feedstock/s; 54 kW heat.
- CEN: 0.01 feedstock/s + 120 EC/s → 0.0001 EnrichedUranium/s +
  0.0067 DepletedFuel/s; 108 kW heat.

Nominal rates depend on SystemHeat loop efficiency. Nuclear processors need
active SystemHeat cooling and stop at 850 K or when inputs/output space are
unavailable. Outputs are not dumped. These are abstract game recipes.
EnrichedUranium/DepletedFuel remain local NO_FLOW resources; docking crossfeed
does not refill them automatically. SystemHeat enables manual resource transfer
with a qualified Engineer (default level 3; honor the installed game settings).
The NST and CEN carry the same fuel-container module as the ground versions.

## Installation and compatibility

Close KSP, replace **GameData/RoosterWorksStationModules** from the complete
dev.11 ZIP, then restart. Ground Modules is a separate addon and is not replaced.
Base requirements remain KSP 1.12.5 and ModuleManager. Nuclear parts require
Community Resource Pack and SystemHeat; ISRU uses stock resource modules.

**Ground Modules is optional.** If present, use ground dev.26 or newer so its
identical RW_NuclearFeedstock definition is available. With no Ground Modules,
Station Modules supplies that resource itself. Both addons together use one
definition, allowing feedstock/cargo exchange without duplicate resource IDs.
No Ground Modules DLL/model/texture is referenced by the new orbital parts.
The small included OrbitalIndustry runtime only manages these new docking
menus; existing station plugin binaries are unchanged.

All dev.10 station parts and assets remain unchanged, including the compact
gravity ring and rounded endcap. Ground dev.28 sources/packages are preserved.
New native models and original hardware are included in the editable Blender
project Source/Blender/RW_OrbitalIndustry.blend; Media/OrbitalIndustry contains
renders of the actual models.

## Checks

Native/configuration checks verify geometry, normals, colliders, texture paths,
two clear docking planes, ring maps, positive prices, exact ground recipes and
resource buffers, optional providers, shared feedstock and baseline preservation.
Docking policy compiles against the installed KSP 1.12.5 API. Actual-source tests
cover menus, repeated reopen, crossfeed/staging, attraction scope and all colors.
Both archives undergo CRC, exact-file and manifest checks.

Live KSP acceptance remains pending: spawn the four parts, switch finishes and
ring colors, stack/dock both ends, transfer fuel with an Engineer, run converters
with power/cooling and test the installed background-processing bridge. Test
standalone and combined ground/orbital feedstock transfer in the full mod set.
