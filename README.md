# RoosterWorks Station Modules — v0.7.5-dev.4

> **Release status (October 14, 2026):** v0.6.0 is the latest published stable release. **v0.7.5-dev.4 is the upcoming release candidate; the maintainer has completed in-game testing.** No v0.7.5 stable GitHub release has been published yet. Earlier development-stage testing warnings below are historical notes and do not describe the current candidate's testing status.


Command data archives now have five editor choices: 200–1000 MB at 2.5 m, 675–3375 MB at 3.75 m, and 1600–8000 MB at 5 m. Preserves dev3 ring fix, LAB tiers and all prior native models/gameplay. See COMMAND_STORAGE_075.md. Offline checks do not establish in-game acceptance or release status.

## Retained development history

# RoosterWorks Station Modules — v0.7.5-dev.3

Ring selector hotfix: resynchronizes live color selections and reconnects ring materials/meshes after editor/model rebuilds. Models, textures, configs, capacity tiers, reactors and surface options retained from dev2. See RING_MENU_HOTFIX.md. In-game reopen/reselect confirmation pending.

## Retained development history

# RoosterWorks Station Modules — v0.7.5-dev.2

Adds 4/6/8 m long straight crew tubes at 2.5/3.75/5 m diameter, ten adjustable volume-scaled LAB data/sample steps, and grouped editor appearance swatches with optional B9PartSwitch. 41 current parts plus two hidden historical reactor IDs. See EDITOR_AND_STORAGE_075.md for capacities and live acceptance checks. Offline checks do not establish in-game acceptance or release status.

## Retained development history

# RoosterWorks Station Modules — v0.7.5-dev.1

Roadmap 0.7 adds eleven native 5 m station modules and a 3.75-to-5 m adapter. Roadmap 0.75 adds compact two-crew HABs in all three diameters. The current catalogue has 38 parts, plus the two hidden historical reactor IDs. White/Grey finish, ring colors, LOG contents, hatch and reactor variants, warm-white lighting and current science limits are retained. Prior part IDs and models remain unchanged.

See STATION_EXPANSION_070_075.md for specifications and the acceptance checklist. These are local development TEST/source packages; no game installation, save modification or GitHub release is implied. New parts and controls require in-game acceptance.

## Preserved development history

# RoosterWorks Station Modules — roadmap 0.65 / v0.6.5-dev.1

Adds independent ring colors to all current models and editor-selectable contents to both LOG sizes. White/Grey finishes, hatch and reactor variants, native geometry, colliders, lighting, VAB groups and prior gameplay remain preserved. LOG defaults to the exact accepted mixed inventory; dedicated supply tanks start full and waste tanks empty. Flight loading never switches or refills cargo.

See CUSTOMIZATION_065.md for capacities, implementation, source validation and the in-game acceptance checklist. Ring choices are Original, Steel, White, Charcoal, Blue, Green, Red and Gold. LOG choices are Mixed supplies, Food, Water, Oxygen, Nitrogen, Ammonia, Waste and WasteWater, conditional on Kerbalism Default/CRP. This is a local development test build, represented as 0.6.5-dev.1 in version metadata. Unity/VAB and gameplay acceptance remain pending. No installation, save edits or GitHub publication performed.

## Prior development history

# RoosterWorks Station Modules — v0.6.0

The current build is numbered **0.6** (machine-readable **0.6.0**), at the user's request. This numbering reset carries forward the complete v0.16.0-dev.3 development candidate: all 23 current parts, both sizes, appearance fixes, White/Grey finishes, reactor variants, storage balance, elbow UV corrections and VAB organization. It does not revert to the historical v0.6 kit.

Only version metadata and documentation change in this build; every other GameData file is byte-identical to v0.16.0-dev.3. Historical development notes below retain their original version labels. See ROADMAP.md for the new milestone sequence. These are local TEST/source packages; numbering does not establish publication or release status.

## Preserved development history

# RoosterWorks v0.16.0-dev.3 — VAB organization and missing straight tubes

Corrects all requested editor groups, with **LOG in Station Utility** as clarified. Both straight tubes are repaired for the installed KSPCF MU loader by removing an unused trailing material entry. Exact tube geometry, UVs, collision, all other models, gameplay and capacities are preserved. Elbow UV corrections remain intact.

See VAB_CATALOGUE.md for the full mapping, diagnosis, source and tests. Selectable logistics contents (Food, Water, Oxygen, Ammonia, Waste, etc.) are added to ROADMAP.md as future work. Close KSP before replacing the TEST folder; actual menu/model-load confirmation remains pending. No installation, save edits, GitHub action or release was performed.

## Prior development record

# v0.16.0-dev.2 — elbow artwork UV fix

User's in-game screenshot showed logos and nameplates repeated six times across the bend. The elbow panel helper subdivided geometry for curvature but restarted texture V=0..1 on every strip. It now maps each strip to its corresponding fraction of the complete panel. Both 250/375 elbows have single continuous nameplates, logos and cladding texture coverage. UVs alone change; exact geometry, normals, indices, materials, textures, colliders, stack nodes, gameplay and the straight tube models are preserved.

New exported-model regression checks sum UV area to require one artwork instance per physical plaque/logo and one texture per cladding tile, and check shared plaque UV edges. The old winding-only test detected mirroring but not repeated artwork; that coverage gap is corrected. The native MU, OBJ/MTL and procedural source agree. Live KSP oblique/close-up visual confirmation remains pending.

Balance and science storage from dev.1 are unchanged. The roadmap includes ground-base modules, adjustable legs and selectable ring colors on each module. Close KSP before replacing the TEST folder. No installation, save edits, GitHub action or release was performed.

## Prior development notes

# RoosterWorks Station Modules — v0.16.0-dev.1

Four new crewless passage models: straight tubes and 90-degree elbows in **2.5 m / 3.75 m**, with pressure/conditional CLS support and accepted White/Grey finishes. HAB batteries cut 30%, PWR Battery only 15%, PWR Nuclear 20%, rounded base EC to tens. CMD/LAB archive limits are **2.5 GB**; LAB sample storage is **100 slots**. Requested **Ground-base modules** and **Adjustable legs** are added to ROADMAP.md.

Latest stats, source, guards and in-game checks: CREW_TUBES_AND_BALANCE.md. The existing 19 native models, glass, lighting, hatch and finish remain preserved. 23 current native/catalogue parts plus hidden legacy reactor IDs. Offline checks are build evidence; new model/gameplay confirmation remains pending. Close KSP before replacing the TEST folder. No installation, save modification, GitHub action or release was performed.

## Previous development history — old capacity figures superseded

# v0.15.0-dev.3 — PWR resource-menu refresh

User confirmed that the reactor is now a stock variant, then reported stale EnrichedUranium/DepletedFuel menu entries after switching to Battery and unchanged displayed EC capacity. The installed dev.2 game log records successful Battery/Nuclear transitions and the rounded 5910 EC target. Prior state-double tests did not model KSP's open resource-widget caching.

The variant controller now fires onPartResourceListChange and calls KSP MonoUtilities.RefreshContextWindows after resource changes, rebuilding open slider ranges and removed fuel rows. It also verifies actual EC capacity when the remembered selection is unchanged, correcting a later editor reset, and removes reintroduced fuel tanks in Battery-only editor mode. Notification is change-triggered, not repeated every idle frame. The source test includes capacity-reset and passive fuel-reintroduction cases, with explicit window-refresh assertions. Actual live menu confirmation remains pending.

Rounded values are **3060 / 5910 EC nuclear**, **3500 / 6750 EC Battery only**, unchanged **5.5 / 6 EC/s** generation. Finish, models, other parts, finite fuel/waste and saved running-state behavior remain unchanged. Close KSP and replace the RoosterWorks folder with the dev.3 TEST build. Test a newly placed PWR core while keeping its right-click menu open: nuclear must show reduced maximum and fuel/waste rows; Battery must restore maximum and remove both fuel rows.

## Previous development notes

# v0.15.0-dev.2 — nuclear EC rounded to nearest 10

User requested rounding the new storage figures to tens. Nuclear PWR-250 now stores **3060 EC**, nuclear PWR-375 **5910 EC**. Battery-only capacities stay **3500 / 6750 EC**. The one-of-eight-bays calculation is rounded to the nearest ten; generation remains **5.5 / 6 EC/s**. All other stats, variant behavior, grey finish and native assets remain unchanged. Offline checks apply; actual KSP retest remains pending.

## Prior development notes

# RoosterWorks Station Modules — v0.15.0-dev.1

PWR-250/PWR-375 now use the stock **Variant: Battery only / Integrated nuclear** selector with coloured swatches on the same editor part. Accepted **White / Grey metal** finish remains independent. Nuclear uses one of eight battery bays: **3060 / 5910 EC**, versus **3500 / 6750 EC** battery-only. Output stays **5.5 / 6 EC/s**, with finite fuel, retained waste and built-in cooling.

See POWER_VARIANTS.md for controls, requirements, saved-craft handling, source and tests. Old reactor part IDs remain loadable but are hidden from the Kerbalism Default catalogue. Original models, accepted finish DLL, hatch runtime and other parts are preserved. Offline checks are available; live KSP confirmation remains pending. Close KSP before replacing the RoosterWorks folder with the TEST build.

## Historical development notes — older reactor selection instructions superseded

# RoosterWorks v0.14.0-dev.2 — finish and reactor visibility fix

Fixes the reported white-only finish by binding the editor field/symmetry callbacks and using Unity Update in both scenes. Adds texture-name fallback for material renaming. The separate nuclear PWR editions now share the ordinary cores' largeElectrics tier and appear in VABOrganizer's nuclearReactors category. Search nuclear in Electrical; passive cores remain under batteries. Batteries remain 3500/6750 EC, nuclear output 5.5/6 EC/s, with retained fuel/waste and built-in cooling. Original native models and hatch DLL are unchanged.

Installed game log/cache showed both nuclear parts and the finish plugin loaded in dev.1. The prior finish test invoked a callback that did not reproduce editor behavior; updated tests drive actual UI callbacks without PartModule.OnUpdate. DLL compilation uses installed KSP assemblies. Offline validation does not establish live KSP visual/gameplay acceptance. Replace the folder while KSP is closed and retest newly placed parts. Do not claim installation, release, GitHub commit or successful gameplay confirmation.

Inspect this corrected source kit before any future edits. Latest source: rw-v0140dev2. See FINISH_AND_REACTOR_OPTIONS.md for usage, requirements, balance and confirmation checklist.

## Previous development notes

# RoosterWorks Station Modules — v0.14.0-dev.1

Optional grey metal finish on all 19 existing parts, independently selectable from HAB hatch arrangements. Two optional nuclear PWR editions add built-in cooling and uranium-fuelled generation: **5.5 / 6 EC/s**. PWR batteries are now **3500 / 6750 EC** for 250 / 375, including nuclear editions. Other capacities retain v0.13 balance.

Choose **Exterior finish** in the editor. Choose the separately named **Nuclear Power and Service Core** when fitting the reactor; start it with its reactor control. Optional nuclear editions require Community Resource Pack and support Kerbalism Default background generation or the stock loaded-vessel fallback. External radiators are not required. White remains available throughout the family.

See [FINISH_AND_REACTOR_OPTIONS.md](FINISH_AND_REACTOR_OPTIONS.md) for stats, build instructions, dependencies and in-game checks. Original native models, glass, badges, lighting and hatch runtime are preserved. Offline validation and package integrity are checked; live KSP tests remain pending. This is a development candidate, with no installation or publication performed.

## Earlier development history — superseded PWR capacities

# RoosterWorks Station Modules — v0.13.0-dev.1

**19-part ElectricCharge balance update: comparable base + 5%.**

Both sizes use explicit role-based capacities, not generic volume scaling for
crew modules. Under your current Kerbalism Default setup, CMD-375 is expected
to show **1323 EC**, CUP-375 **1470 EC**. PWR-250/PWR-375 store **12600/42525 EC**.
LAB, AIR, LOG and GRN match counterparts with no integrated battery and now need
connected station power. HAB/CMD/CUP retain role-appropriate backup batteries.
Hub and adapter remain batteryless. No consumption or generation rates changed.

| Role | 2.5 m base EC | 3.75 m base EC | Reference |
|---|---:|---:|---|
| HAB | 420 | 787.5 | sspx-habitation-25-1 / sspx-habitation-375-3 |
| LAB | 0 | 0 | Large_Crewed_Lab / sspx-lab-375-1 |
| CMD | 210 | 472.5 | sspx-core-25-1 / sspx-core-375-1 |
| HUB | 0 | 0 | passive structural junction/adapter / passive structural junction/adapter |
| CUP | 210 | 525 | cupola / sspx-cupola-375-1 |
| LOG | 0 | 0 | sspx-cargo-25-1 / sspx-cargo-25-1 |
| AIR | 0 | 0 | sspx-airlock-25-1 / sspx-airlock-25-1 |
| PWR | 12600 | 42525 | battery-25 / battery-25 |
| GRN | 0 | 0 | sspx-greenhouse-25-1 / sspx-greenhouse-375-1 |

These are BEFORE Kerbalism's x2.8 crewed-part multiplier. Full reference IDs,
policy, expected game values and testing instructions: ELECTRIC_CHARGE_BALANCE.md.
All meshes, textures, the four-point greenhouse lighting fix, larger variants,
other resources, crew, mass/cost and gameplay modules are preserved. Source
and a config-only rebuild regression prevent capacities reverting in future builds.

Offline validation passed. KSP config-cache/new-part and electrical gameplay
confirmation remain pending. No installation, save edits or publication performed.

## Previous development documentation (historical EC figures are superseded)

# RoosterWorks Station Modules — v0.12.0-dev.1

Greenhouse lighting repair and the complete first 3.75 m family. **19 parts**:
the original nine 2.5 m station modules, the existing 2.5→3.75 adapter, plus
RW-HAB-375, RW-LAB-375, RW-CMD-375, RW-HUB-375, RW-CUP-375, RW-LOG-375,
RW-AIR-375, RW-PWR-375 and RW-GRN-375.

The greenhouse now has four native warm-white point lights that illuminate crop
meshes, separate inspection-light strips and a stock Lights On/Off control in
editor/flight. The inspection light starts enabled on new parts and remains
available with Kerbalism, regardless of crop activity or natural solar flux.
Use the greenhouse part's Lights On/Off control or the normal Light action group.
Inspection lighting is cosmetic and has no added EC drain, consistent with the
family's cabin glow. Actual crop lamps/EC and greenhouse operation remain under
Kerbalism's control; the two controllers target separate renderers.

Large geometry, collision shapes and attachment positions scale by 1.5 in all
dimensions, so axial lengths also increase. New native MU files use real metres,
rescaleFactor=1 and size-3 stack nodes. Existing rounded HUB, sealed endcaps,
correct UV orientation, HAB variants and EVA/ladder features are retained.
Dry mass and storage/habitat volume scale 3.375; surface/joint strength 2.25;
inventory slots double. Current crew counts and stock IVAs remain unchanged to
avoid assigning occupants to absent seats. Roles, scientific processing, command
authority, communications and most equipment settings remain unchanged; CMD
wheel torque and draw increase with its size. These are development balance choices.

Each large module has a readable 375 nameplate. Original shared textures/branding
are retained. Large Kerbalism patches target only new part IDs. GRN-375 inherits
the installed Default greenhouse at 1.6875 times its rates (3.375 times GRN-250),
with appropriately scaled startup/output storage, Habitat and pressure controller.
Crewless modules remain crewless; terminal CUP keeps one bottom port. Adapter is
unchanged and connects the two sizes. Nine non-greenhouse small parts, their
patches, textures and runtime DLL remain byte-identical. Small GRN alone receives
the authorized lighting repair; its crop-support patch and gameplay balance stay.

Native MU, OBJ/MTL and procedural source for all parts are included. Optional
Blender reconstruction was not executed. CPU previews read actual exported meshes,
textures and light positions/ranges; their illumination is an approximation and
does not establish Unity/KSP visual behavior. In-game lighting, large-part fit,
EVA, gameplay and performance confirmation are pending. No install or publication.

Build: `python Tools/build_greenhouse.py`, then `python Tools/build_large_family.py`;
or rebuild everything with `python Tools/build_appearance.py`. Validate:
`python Tools/validate.py`. Preview: `python Tools/render_family375.py`.
Package: `python Tools/package_appearance.py`. Python/Pillow/NumPy required.
Read LARGE_FAMILY_TEST_CHECKLIST.md, GREENHOUSE_TEST_CHECKLIST.md and INSTALLATION.md.

## Previous development history

# RoosterWorks Station Modules — v0.11.0-dev.1

New tenth part **RW-GRN-250** is a detailed 2.5 m hydroponic greenhouse with
eight genuinely transparent bays, four growing tiers and modeled crops,
irrigation hardware, warm-white grow strips and matching closed endcaps.
3.6 m long, 2.75 t dry, 16000 funds, advScienceTech, Utility. Crewless equipment
chamber; no IVA or EVA. 1000 EC storage; external station supplies are required.

With Kerbalism Default, production and inputs are half the installed standard
greenhouse's rates. Its installed harvest/continuous-production behavior and
environmental requirements are inherited, rather than replaced with a fixed
version's recipe. Standard kerbalism-greenhouse part is required as template.
Startup water, nutrients, carbon and nitrogen are supplied; output tanks start
empty. Normal Kerbalism pressure control/conditional Habitat integration.
Other profiles get no Default food-production patch. Without Default, glass,
crops, battery and cosmetic manual lamps work, but no food is produced.
Plants are static model detail. In Default, greenhouse activity/lighting controls
emission and actual lamp EC use; stock cosmetic toggle is removed in that branch.

All nine prior parts and their gameplay are byte-identical except package version.
Adapter appearance feedback was positive; in-game adapter fit was not confirmed.
Native MU, Python, OBJ/MTL, source textures and optional Blender reconstruction
included. Blender was not executed. Preview uses actual exports, alpha glazing
and lamp-on surfaces in studio lighting. In-game geometry/greenhouse/MM tests pending.

Build: `python Tools/build_greenhouse.py`; family: `python Tools/build_appearance.py`.
Validate: `python Tools/validate.py`; render: `python Tools/render_grn250.py`;
package: `python Tools/package_appearance.py`. Python, Pillow and NumPy required.
Read GREENHOUSE_TEST_CHECKLIST.md and INSTALLATION.md before testing.
Current continuation: Source/Documentation/CONTINUATION-v0.11.0-dev.1.md.

## Prior development documentation

# RoosterWorks Station Modules — v0.10.0-dev.1

New ninth module **RW-ADP-250-375** joins 2.5 m and 3.75 m stacks with a detailed
1.8 m tapered body. Crewless, 1.1 t, 4200 funds, advMetalworks, Structural category.
Small end is +Y (size 2), large end is -Y (size 3); nodes are at ±0.9 m.
Matching ivory/bronze/graphite panels, service lines, readable RoosterWorks
badges and closed recessed endcaps. Three convex solids follow the tapered body.
Stock crossfeed and surface attachment; no docking, crew or built-in resources.

All eight existing modules and their gameplay, textures and Kerbalism support
remain byte-identical to v0.9.0-dev.1 except package version. KSP 1.12.5 test
candidate; adapter in-game appearance and attachment confirmation pending.
PWR still awaits feedback; AIR was previously reported working.

Native MU, procedural Python, editable OBJ/MTL, optional Blender reconstruction
and actual exported-model preview included. Blender was not executed.
Read ADAPTER_TEST_CHECKLIST.md and INSTALLATION.md. Build/validation commands
and development history: Source/Documentation/CONTINUATION-v0.10.0-dev.1.md.

## Previous development documentation

# RoosterWorks Station Modules — v0.9.0-dev.1

**KSP 1.12.5 · eight-module development candidate with Kerbalism compatibility.**

New **RW-PWR-250** power and service core: crewless, 15000 EC, 2.5 t, 2.5 m stack
interfaces and 2.4 m axial length. Eight modeled cell cabinets with new detailed
textures, protected electrical trunks, service connectors, cosmetic cooling fins
and clear central mounting areas for separate solar panels/radiators. Matching
endcaps and original readable RoosterWorks labels.

It stores electricity and shares it through normal vessel resource flow.
Generation and functional cooling come from attached parts. No crew, IVA,
EVA, Habitat or custom power-system controller. Stock-KSP fallback needs no
Kerbalism; with Kerbalism it participates through normal ElectricCharge storage.

All seven accepted modules — HAB, LAB, CMD, HUB, CUP, LOG and AIR — remain
byte-identical to v0.8.0-dev.1, including their textures, configs, Kerbalism
patches and runtime DLL. Only package metadata and new PWR files change GameData.
User reported AIR working; preserve its native exit/ladder and previous features.

Build PWR only: `python Tools/build_power.py`. Full-family rebuild:
`python Tools/build_appearance.py`. Requires Python, Pillow and NumPy.
Validate: `python Tools/validate.py` includes new geometry/battery checks and
recorded authentic seven-module hashes. Render: `python Tools/render_pwr250.py`.
Package: `python Tools/package_appearance.py`.

Current preview: Media/RW-PWR-250-v0.9.0-dev.1-Review.png reads actual exported
MU/PNG data with Unity camera orientation; it is not an in-game screenshot.
Native MU and OBJ/MTL regenerated; optional Blender reconstruction not executed.
Offline and package checks passed; PWR visual/electrical confirmation pending.
Read POWER_TEST_CHECKLIST.md and INSTALLATION.md before testing. No installation
or publication performed. Latest history: Source/Documentation/CONTINUATION-v0.9.0-dev.1.md.

## Earlier seven-module documentation (historical)

# RoosterWorks Station Modules — v0.8.0-dev.1

**KSP 1.12.5 · seven-module development candidate with Kerbalism support.**

New **RW-AIR-250** dedicated EVA staging chamber: 2.5 m interfaces, 2.4 m long,
two seats, side hatch, native exit/boarding ladder, two inventory slots / 120 L,
400 EC and warm-white porthole glow. Matching sealed endcaps, readable badges,
graphite service panels and original ivory/bronze styling. Candidate mass 1.85 t.

Kerbalism adds a 6 m³ / 20 m² Habitat when FeatureHabitat is installed. Connect
to a supplied station; no special air-recovery cycle or animated pressure door.
Uses a temporary stock two-seat IVA and normal stock/Kerbalism EVA restrictions.
The dedicated airlock is always present, with no cosmetic variant gating.

The accepted HAB, LAB, CMD, rounded HUB, CUP and LOG models, texture PNGs,
configurations, Kerbalism patches and runtime DLL are byte-identical to dev.4.
Package version and new AIR files are the only GameData differences.

**Build:** `python Tools/build_airlock.py` adds/rebuilds AIR without touching the
accepted six-module assets; `python Tools/build_appearance.py` rebuilds the full
family. Use Python with Pillow/NumPy. `python Tools/validate.py` runs the complete
suite including new native AIR checks and authenticated dev.4 file hashes.
`python Tools/render_air250.py` generates the new model review; earlier dev.4
family previews remain applicable to the six unchanged modules.
`python Tools/package_appearance.py` creates TEST and Developer-Source archives.

Latest AIR preview: Media/RW-AIR-250-v0.8.0-dev.1-Review.png (actual exported native
MU and PNGs, Unity camera orientation, software studio lighting). Native MU and
OBJ/MTL are regenerated; optional Blender reconstruction was not executed.

Full offline and fresh-package checks pass. AIR visual acceptance, stock EVA,
boarding, IVA and Kerbalism pressure need in-game confirmation. Read INSTALLATION.md
and AIRLOCK_TEST_CHECKLIST.md. No installation or GitHub publication is implied.
Latest continuation: Source/Documentation/CONTINUATION-v0.8.0-dev.1.md.

## Accepted six-module appearance baseline (historical dev.4 documentation)

# RoosterWorks Station Modules — v0.7.0-dev.4

**KSP 1.12.5 · six-module badge and endcap-seam development candidate.**

Fix reversed RoosterWorks nameplates throughout the family. UV orientation is
now consistent with Unity's outward camera view in source geometry, native MU
and editable exports. Original PNG artwork remains unchanged. Shared service
atlas islands and small hull-panel stencils also read outward correctly.

Close the recessed endcap-to-rim seams at all 15 shared stack interfaces:
inward-facing cavity liners, overlapping bronze blanket perimeter, rim step
walls, an outer skirt reaching the lip, and closed central pressure-plate steps.
The cupola's upper viewport also gains a continuous recessed liner and overlapping
retaining lip, with its accepted glass aperture and canopy geometry preserved.

| Module | Role | Crew | Interfaces |
|---|---|---:|---|
| RW-HAB-250 | Habitat / functional Side Hatch | 4 | Two size-2 stack ends |
| RW-LAB-250 | Stock / Kerbalism laboratory | 2 | Two size-2 stack ends |
| RW-CMD-250 | Station command / SAS / CommNet | 2 | Two size-2 stack ends |
| RW-HUB-250 | Rounded six-way pressure junction | 0 | Six size-2 faces |
| RW-CUP-250 | Terminal observation cupola | 1 | One size-2 lower stack end |
| RW-LOG-250 | Passive logistics storage | 0 | Two size-2 stack ends |

The dev.2 exterior hardware/textures and dev.3 rounded HUB are retained. Node
positions, physics colliders/triggers, all glazing, HAB variants, part/compatibility
CFGs, Kerbalism balance, runtime DLL, textures and warm-white lighting are unchanged
from dev.3. Cosmetic MU models and package version are deliberately updated.
Original material/shader definitions remain protected by native regression checks.

LOG remains 2.5 m × 3.0 m, 3.25 t, 600 EC, 12 slots / 1400 L. Kerbalism Default
storage remains Food 120, Water 60, Oxygen 20000, Nitrogen 8500, empty Waste capacity
120 and WasteWater 75; FeatureHabitat 12.5 m³ / 34 m². Endcap closures and exterior
equipment remain cosmetic; they add no docking ports, EVA exits or animations.

**Validation:** complete offline suite, native label handedness, all recessed
liners, authentic dev.3 physics/glass/variant/material comparisons, unchanged
GameData texture/config/runtime hashes and archive integrity checks pass.
KSP visual and gameplay confirmation of this candidate is pending. Supplied
in-game screenshots document the dev.3 defects, not confirmation of dev.4.

## Build and review

Use Python with Pillow and NumPy:

```
python Tools/build_appearance.py
python Tools/validate.py
python Tools/render_appearance.py
python Tools/render_surface_fixes.py
python Tools/package_appearance.py
```

Use the family builder; older individual main routines retain legacy texture
generation. Native MU and OBJ/MTL are regenerated. Optional Blender reconstruction
scripts read the corrected source geometry; Blender was not executed.

Latest previews: Media/RoosterWorks-v0.7.0-dev.4-Surface-Fixes.png,
Media/RoosterWorks-v0.7.0-dev.4-Family.png and six dev.4 review sheets.
CPU previews use actual exported native models and PNGs, with corrected Unity
camera handedness. Previous CPU previews used a right-handed camera that masked
the in-game label reversal; retain them only as historical references.
These renders are not in-game screenshots.

Read INSTALLATION.md, APPEARANCE_TEST_CHECKLIST.md and TEST_CHECKLIST-v0.7.0.md.
Full history is retained in Source/Documentation/; the latest record is
CONTINUATION-v0.7.0-dev.4.md. Earlier source directories and archives remain intact.
No installation, GitHub commit, tag or release was performed. Original RoosterWorks
assets, MIT licensed.
