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

# v0.9.0-dev.1 — New RW-PWR-250 power and service core

The eighth module is a crewless 15000 EC battery bank, 2.5 m interface standard
and 2.4 m long. Eight layered cabinet banks, detailed original cell labels,
protected service trunks, connectors, small cosmetic fins and central mounting
areas match accepted ivory/bronze/graphite styling and sealed endcaps.
Candidate balance: 2.5 t, 12500 funds, largeElectrics technology, Electrical category.

Normal stock resource flow shares ElectricCharge with the attached vessel.
Use separate solar panels or generators to recharge, and separate radiators for
functional cooling. The part has no generator, active radiator, crew, IVA, EVA,
Habitat or invented air supplies. Kerbalism uses its normal electrical system;
this passive stock battery requires no custom Kerbalism conversion patch.

Original seven-module GameData is byte-identical to accepted v0.8.0-dev.1 except
package version. Warm-white lights on prior crew modules, AIR exit/ladder,
rounded HUB, readable badges and closed rims are retained. AIR was reported
working by the user; no separate checklist measurements were supplied.

New PWR model: 21772 visual triangles and one closed convex 96-triangle solid
collider. Native MU, editable OBJ/MTL, procedural source, two new PNGs and optional
Blender reconstruction included. Blender was not executed. Offline and package
checks passed; PWR visual and electrical runtime testing remains pending.

No KSP installation, save modification, GitHub commit, tag or release performed.
Previous history follows.

# v0.8.0-dev.1 — New dedicated EVA airlock

The seventh module, RW-AIR-250, is a two-crew EVA staging chamber with 2.5 m
interfaces and 2.4 m axial length. Original modeled side hatch, porthole, boarding
rails/rungs, suit-service panels and pressure IDs match the accepted station family.
It includes 400 EC, two inventory slots / 120 L and a stock two-seat placeholder IVA.
Balance candidate: 1.85 t, 7800 funds, specializedConstruction.

Native stock Airlock/Ladder triggers are always present on layer 21. No variants
or HAB-only controller are applied. A single solid convex hull protects the EVA
clearance-ray origin from self-obstruction. This is a configured stock EVA exit,
not a claim of runtime confirmation: stock discovery, portrait EVA, auto-grab,
climbing, boarding and flight loading require actual KSP tests.

Kerbalism FeatureHabitat adds volume 6 m³ / surface 20 m². Normal Kerbalism rules
remain active; there is no bespoke pressure cycling, pumping or gas recovery.
Attach to a provisioned station. Pressure equipment and end closures are cosmetic.
Warm-white porthole lights use the established stock toggle without power draw.

All accepted v0.7.0-dev.4 GameData files are byte-identical apart from package
version. The new module has 21,920 visual triangles, one 96-triangle solid collider
and two native triggers. Native MU, OBJ/MTL, procedural Python and optional Blender
reconstruction are included. Blender was not executed. Offline and fresh-package
checks pass; model acceptance and gameplay testing pending.

No KSP installation, save change, GitHub commit, tag or release was performed.
Earlier development history follows.

# v0.7.0-dev.4 — Badge and endcap seam correction

User's dev.3 KSP screenshots show mirrored LOG nameplate text and background
visible between the recessed endcap and rim. Correct the label mappings across
all six modules and reverse the shared atlas within its existing islands.
The original crest and all texture PNGs are preserved.

The shared rim's recessed cylinder previously faced outward; KSP culled it from
the cavity side. Replace it with inward-facing geometry, overlap the blanket
perimeter, connect the rim steps and close the outer skirt to the lip. Seal the
small central pressure-plate steps too. This applies to 15 shared end faces;
the CUP upper viewport trim also gains a continuous liner and overlapping lip.
Glass, colliders, stack positions and all gameplay/light systems remain unchanged.

Source UVs, native MU and OBJ/MTL now agree. The CPU renderer's camera right-axis
is corrected to match Unity, so review images can reveal reversed lettering.
The previous studio previews masked the actual in-game UV problem.

Full offline and fresh-package validation passed. Dev.4 KSP visual/gameplay
confirmation remains pending. No installation, GitHub commit, tag or release
performed. Earlier build history follows.

# v0.7.0-dev.3 — Rounded HUB development candidate

The HUB's square centre is replaced by a spherical pressure body with smoothly
blended circular necks. Existing 2.5 m interfaces, six nodes at ±2 m, endcap
detail and service fittings are retained. All part configurations, Kerbalism
patches, textures, warm-white lighting and the other five native models are
byte-identical to dev.2.

HUB physics deliberately changes: the central box becomes a 224-triangle convex
spherical mesh, and neck/collar colliders are rebuilt to fit the rounded shape.
There are still 13 solid convex colliders. Exported data is checked for winding,
watertightness, convexity, cooking limits and containment within the visible body.
Actual radial attachment and joint stability need KSP testing.
The HUB now has 78,588 render triangles versus 49,404 in dev.2 (about 59%
more), including its detailed endcaps. The largest material mesh has 46,272
vertices, below the 16-bit limit. Station performance requires in-game review.

Preview: Media/RW-HUB-250-v0.7.0-dev.3-Rounded-Review.png reads the exported .mu
and shipped textures. It includes three angles and a comparison to dev.2;
it is a software studio render, not an in-game screenshot.

Offline validation and ZIP checks pass. User visual acceptance and KSP gameplay
confirmation are pending. No installation, GitHub commit, tag or release was
performed.

## Prior family appearance pass

# v0.7.0-dev.2 — Six-module exterior detail pass

Development candidate built from the supplied v0.7.0-dev.1 source kit.

- Detailed cladding textures with chamfered cover borders, fasteners, witness
  marks, MMOD stencils and restrained grain. Separate hull materials prevent
  panel artwork repeating on thin glass frames or rails.
- Refined graphite, bronze and metal diffuse finishes; stitched insulation,
  revised grilles, an economical shared service atlas and crisp original labels.
- HAB life-support hardware; LAB manifold and thermal fins; CMD avionics;
  HUB shoulder looms/collar IDs; CUP optical diagnostics; LOG cassette IDs and
  supply-bank covers. All new equipment is cosmetic.
- Common endcaps gain continuous outer metal skirts, recessed circuit plates,
  seam rings and fastening detail while retaining original mating planes.
- Correct HAB/LAB/CMD nameplate UV mirroring and recessed LOG backing to stop
  coplanar white/graphite overlap at its shoulder collars.
- Exported all six native .mu models, updated OBJ/MTL assets, and both HAB
  variants. Added HUB Blender reconstruction, family build/render/package tools
  and independent native baseline fingerprints.

Physics colliders, triggers, glass geometry, HAB variants, warm-white emissive
mask, original rooster, gameplay CFGs, Kerbalism patches, runtime binary and
stock shader definitions are preserved. Render triangle counts increase by
roughly 6–36%; three shared cosmetic material slots are added. No normal-map or
new shader dependency is introduced. Offline success does not establish KSP
performance, visual quality or gameplay; review APPEARANCE_TEST_CHECKLIST.md.

No KSP install, GitHub commit, tag or release was performed.
