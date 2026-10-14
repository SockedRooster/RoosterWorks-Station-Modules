# Changelog — RoosterWorks Station Modules

## v0.6.0 — Stable release (in-game verified)

- Maintainer confirmed successful in-game testing of the complete v0.6.0 feature set.
- Stable version numbering carries forward the v0.16.0-dev.3 feature baseline: 23 part configurations, appearance and finish variants, power and storage balance, corrected tube models and elbow UVs, and editor organization.
- No gameplay assets were modified as part of the repository's stable-release documentation cleanup.

Earlier entries below are preserved as **historical development notes**. Statements about pending tests or unpublished development packages in those entries do not describe the stable v0.6.0 release.

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

# Change log

# v0.13.0-dev.1 — ElectricCharge balance: reference base + 5%

User requested applying comparable-part battery balance across all parts with
5% above base. This pass changes only initial/max integrated EC storage across
the current 19-part station family. It does not rebalance electrical consumption,
generation, light behavior, greenhouse output, other supplies, crew, dry mass,
price, technology, geometry, attachment or physics. No installed game files edited.

Reference capacities were read from installed, unpatched configs and frozen as
numbers, source IDs and SHA256 in Source/Balancing/electric_charge_policy.json.
No comparator mod is required to build or use these capacities. Rules:
matching stock/SSPXr function and size when available; +5% once on base; no
integrated comparator battery remains zero, rather than creating a battery.
HAB-375 uses the 750 EC six-seat compact SSPXr habitat (-375-3), with HAB-250
using 400 EC SSPXr habitat. CMD uses SSPXr 200/450; CUP stock 200 / SSPXr 500.
LAB stock MPL-LG-2 / SSPXr lab have no top-level battery; their nested EC entries
are consumption, not storage. AIR, cargo LOG and greenhouses also have no
integrated comparator storage. HUB and adapter remain passive with zero EC.
PWR uses installed Near Future Electrical battery-25, 12000 EC, as a dedicated
battery comparator; absent 3.75 counterpart uses 3.375 volume proxy, then +5%.
This avoids comparing a battery core with a crew pod and retains bulk station storage.

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

Adapter EC remains zero. These are base values, BEFORE Kerbalism. Under the
current Default crewed-part x2.8 patch: CMD-250 588; CMD-375 1323; CUP-250 588;
CUP-375 1470; HAB-250 1176; HAB-375 2205. PWR is crewless: 12600 / 42525 EC.
Do not write boosted values into base configs or apply the +5% again in a patch.
LAB/AIR/LOG/GRN now rely on connected vessel batteries/generation. In particular,
greenhouse production needs connected power; manual cosmetic inspection lights
retain their zero added draw. Food/water/gas startup buffers and rates unchanged.

Source/electric_charge_balance.py applies the explicit policy; build_family375.py
overrides its generic resource scaling for EC. Tools/build_ec_balance.py performs
the config-only balance and refreshes metadata/manifest. Canonical family build
and individual builder wrappers apply the policy before manifest output.
No blind cubic scaling for ordinary integrated batteries, no double 5% bonus.

Every pre-balance GameData file hash from v0.12 is recorded. Original own CFGs
are frozen in Source/Balancing/v012-before; check_preserved verifies historical
hashes and reconstructs prior EC values to prove that only those values changed.
All 19 native models, textures, point lights, runtime DLL and compatibility patches
are byte-identical. Existing historical regression checks use this constrained
EC-only exception, not new arbitrary golden hashes. A large config-only rebuild
must reproduce identical balanced CFGs. Offline suite passed.

KSP actual cache and runtime checks remain pending. Verify new parts in VAB after
reloading configs, inspect ModuleManager.ConfigCache, test electrical loads and
supplied greenhouse operation. Existing craft/save snapshots may retain prior
resource capacities: compare newly placed parts before attributing mismatches
to the new configs. No saves were modified. No install, commit, tag or release.

Build: python Tools/build_ec_balance.py. Validate: python Tools/validate.py.
Package: python Tools/package_appearance.py. Models/previews do not need rebuilding
for this balance pass. Previous lighting and large-family checklists still apply,
with their old EC figures superseded by this document.

# v0.12.0-dev.1 — Greenhouse light fix and nine 3.75 m modules

User reported no greenhouse lighting and requested fixing it, then producing
3.75 versions of the 2.5 station modules. Read source kit and installed stock
KSP light configuration; read prior ModuleManager cache, without editing the
installation. Prior GRN had only emissive geometry, no native Light. Default
removes its cosmetic grow-light toggle, and sets grow emission according to
artificial light demand. A surface glow cannot light real plant meshes.

Add four native warm-white point lights above crop tiers at Y=-0.74,-0.15,0.44,1.03 m, intensity 1.4, range 2.2 m each,
and separate inspection-strip renderer, RW_GreenhouseInspectionLamps. Stock
ModuleLight uses RW_GreenhouseInspectionLight; default on, manual switch in
editor/flight, no animation dependency, no added resource draw. Existing crop
renderer RW_GreenhouseLamps and Default crop support are unchanged. Cosmetic
inspection lighting is independent from growth, and remains available with
Kerbalism; production still requires normal inputs/power/environment. MU Light
record type 23 follows the io_object_mu format documentation. Native parser
extended to read it. No new plugin or modified hatch runtime needed. Small GRN
40764 visual triangles (64 added inspection-strip triangles), previous collision
hull, glazing and 192 plants retained. Actual Unity switch/lighting tests pending.

Added HAB/LAB/CMD/HUB/CUP/LOG/AIR/PWR/GRN-375. Full 1.5 geometry scaling includes
axial length, native colliders, trigger size/position and attach coordinates;
size-3 stack nodes, rescaleFactor=1. Surface 2.25 and volume/dry mass/storage 3.375,
slots double. Crew counts/IVAs retained exactly: HAB4, LAB2, CMD2, HUB0, CUP1,
LOG0, AIR2, PWR0, GRN0. No invented new seats. Command/science behavior retained;
CMD reaction wheel torque/EC scale by 3.375. Original renderer, variant and hatch
trigger names deliberately retained so stock controllers and original runtime
bind correctly. EVA fixed 0.5 m ray-origin offset checked against exported large
HAB and AIR solid hulls, rather than scaling the offset. Hub rounded profile
and all other accepted shapes are proportional; no new boxy hub.

Large labels are new PNGs, original shared cladding/artwork retained. Individual
native MU and scaled editable OBJ/MTL provided; rebuild source uses actual
maintained small exports with strict typed serialization, plus ordered ConfigNode
cloning. Large-specific Kerbalism/VABOrganizer files use new IDs only, inherited
conditions/modules, scaled volume/surface/resources; GRN-375 rates are 1.6875
times installed standard greenhouse. Original adapter already spans these sizes;
no unrequested 5 m adapter. Total 19 parts. All unrelated small GameData hashes
protected by Tools/large_family_baseline.json; original runtime DLL unchanged.

Tools/validate_family375.py checks all nine exports, source-sized triangles/UVs/
normals/materials, colliders, native lights, nodes, IVA/crew roles and ray origins.
Entire historical suite retained; greenhouse validator now requires an actual
Light, stock switch and separate lamp renderer. Canonical build/packaging support
19 parts. Optional Source/Blender/create_family375.py uses --part and --variant;
Blender was not executed. Native CPU overview and dark inspection views include
point-light attenuation as an approximation; no claim of KSP rendering/testing.

First large family is a development candidate. User has not accepted its fit,
appearance, lighting, balance or gameplay yet. No save edits, installation,
GitHub commits, tags or release performed. Earlier source archives preserved.

# v0.11.0-dev.1 — RW-GRN-250 hydroponic greenhouse

User gave positive adapter appearance feedback ("very nice") and requested
the 2.5 greenhouse. Feedback does not establish adapter gameplay/fit checks.
Created separate rw-v0110dev1 from the nine-part v0.10.0-dev.1 kit; prior archives
are intact. New tenth module GRN has 2.5 m interfaces, 3.6 m axial length,
eight actual low-opacity curved glass bays, four tiers of sector-shaped crop
trays, 192 modeled leafy plants, irrigation risers, warm-white grow strips,
continuous frame foundations, central brace and matching sealed endcaps.
Panels, badges and all geometry are originally authored procedural assets.
There is no opaque full barrel behind the glazing or painted crop illustration.

Candidate balance: crewless, 2.75 t dry, 16000 funds, advScienceTech, Utility,
1000 EC. Two size-2 nodes at ±1.8 m. No IVA, EVA, command, docking or generator.
Native MU: 40700 visual triangles and one closed convex 96-triangle hull.
Glazing uses KSP/Alpha/Translucent with RGBA alpha 36/255 and inward/outward
surfaces. Lamps use KSP/Emissive/Diffuse and a warm-white texture; no new plugin.
Static plants are decorative and do not animate with harvest/growth.

Kerbalism Default support copies the installed kerbalism-greenhouse Greenhouse
node after zzzKerbalismDefault, then halves crop_size, EC lamp rate, and each
input/output rate, retaining crop_rate, environmental thresholds and installed
growth behavior. The original greenhouse is untouched. This follows both older
harvest-based versions and newer continuous-production Default balance without
hardcoding a version's chemistry. Override lamps to RW_GreenhouseLamps; blank
shutters/plants animation names; start disabled. Remove the stock cosmetic
ModuleColorChanger only when the copied Greenhouse exists so two controllers
cannot fight over emission. MM node-copy syntax and pass ordering were checked
against the official ModuleManager wiki; actual MM application needs game testing.

Default greenhouse startup buffers: 40 Water, 200 Ammonia, 3000 CarbonDioxide,
2000 Nitrogen; empty output capacity 300 Food / 6000 Oxygen. External station
supplies, generation and replenishment are still needed. Pressure controller
capacity 0.25. Conditional FeatureHabitat provides 12 m³ / 36 m² volume/surface.
Other Kerbalism profiles do not get this Default recipe. Without Default,
manual cosmetic lamp toggle and stock EC storage remain; no food production.
No specific Kerbal feeding count, runtime production, lamp draw or performance
was measured. A standard Kerbalism Default part installation is needed as template.

Prior nine modules' complete GameData except package version is byte-identical,
enforced by Tools/greenhouse_baseline.json. Previous Kerbalism patches, glass,
warm-white lights and runtime DLL are preserved. Native MU, procedural Python,
OBJ/MTL, original leaf/medium/glass/lamp/label PNGs and optional Blender source
included. Blender was not executed. CPU preview reads actual exported geometry
and textures; it now blends actual alpha and shows lamp surfaces on, with studio
lighting and no simulated point-light illumination. Not an in-game screenshot.

Build: python Tools/build_greenhouse.py; full family Tools/build_appearance.py.
Validate: python Tools/validate.py. Preview: python Tools/render_grn250.py.
Package: python Tools/package_appearance.py. GREENHOUSE_TEST_CHECKLIST.md covers
MM cache/recipe, foreground/background operation, light/input/pressure failures,
stock fallback, glass sorting, stack fit and previous modules. In-game checks
remain pending. No installation, save edit, commit, tag or publication performed.

Primary references checked 2026-10-13:
- https://github.com/Kerbalism/Kerbalism/blob/master/GameData/KerbalismConfig/Profiles/Default.cfg
- https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Modules/Greenhouse.cs
- https://github.com/sarbian/ModuleManager/wiki/Module-Manager-Syntax
- https://github.com/sarbian/ModuleManager/wiki/Patch-Ordering

# v0.10.0-dev.1 — RW-ADP-250-375 station adapter

User requested a 2.5 to 3.75 adapter. New ninth part is a crewless structural
transition, 1.8 m long, small size-2 interface at +0.9 m and large size-3
interface at -0.9 m. Candidate balance: 1.1 t, 4200 funds, advMetalworks,
Structural category. These balance/length choices are implementation decisions.
Tapered ivory panels, graphite seams, bronze trim, conformal readable badges,
reinforcing spines, paired service lines and both closed recessed endcaps match
the original family. Large cap is enlarged radially 1.5 times; axial recess
depth is preserved and normals receive inverse-transpose radial scaling.

Native MU contains 16356 visual triangles and three closed convex 96-triangle
colliders following the large collar, taper and small collar. Stack nodes are
attachment nodes, not docking ports. Stock crossfeed and surface attachment
are enabled. No crew, IVA, EVA, resource storage, generator or Habitat module.
No special Kerbalism patch is required for this passive structural part.

All eight prior modules' GameData except package version is byte-identical to
v0.9.0-dev.1, enforced by Tools/adapter_baseline.json. PWR remains a candidate
awaiting in-game feedback. AIR was previously reported working by the user.
Native geometry, procedural Python, OBJ/MTL, new label PNG and optional Blender
reconstruction are included; Blender was not executed. Preview reads actual
exported MU/textures with Unity camera orientation, not an in-game screenshot.

Build adapter: python Tools/build_adapter.py. Rebuild family:
python Tools/build_appearance.py. Validate: python Tools/validate.py.
Preview: python Tools/render_adapter.py. Package: python Tools/package_appearance.py.
Offline and package checks must pass before delivery. In-game stack fit,
appearance, radial attachments and save/load testing remain pending; see
ADAPTER_TEST_CHECKLIST.md. No installation, GitHub commit, tag or release.

## v0.9.0-dev.1 — RW-PWR-250 battery and service core

Add crewless 2.5 m-interface, 2.4 m-long passive battery module with 15000 EC,
eight chamfered cell cabinets, original cabinet texture, protected cable trunks,
connectors, cosmetic fins and four central mounting areas for separate parts.
2.5 t, 12500 funds, largeElectrics, Electrical category. Matching sealed endcaps
and correctly oriented original branding. No generation, active cooling, crew,
EVA, IVA or Habitat. Accepted seven-module GameData byte-identical except version.
Native MU, procedural Python, OBJ/MTL, optional Blender source and native review
included. Offline validation passed; appearance/electrical flight testing pending.

## v0.8.0-dev.1 — Dedicated RW-AIR-250 EVA chamber

Add a two-crew 2.5 m-interface, 2.4 m-long EVA chamber with dedicated side hatch,
boarding rails/rungs, suit-service panels, sealed shared endcaps, readable original
branding and warm-white hatch porthole glow. Native always-present Airlock and
Ladder triggers use KSP's stock access path; no HAB variant controller is added.
One closed convex 96-triangle hull contains the stock clearance-ray origin.
Two stock inventory slots / 120 L, 400 EC, 1.85 t; temporary stock two-seat IVA.
Conditional Kerbalism Habitat: 6 m³ / 20 m². No custom pressure-cycle, air recovery
or animated door. Accepted v0.7.0-dev.4 GameData stays byte-identical except package
version; new model, configs and label added. Offline checks pass; flight tests pending.

## v0.7.0-dev.4 — Readable badges and sealed endcap rims

Correct family label/crest UV orientation in source geometry and remove inconsistent
export-only crest flips. Reverse atlas U within each island and orient cladding
stencils for Unity's outward view, without changing PNG artwork. Correct the CPU
preview camera handedness that previously masked in-game mirroring. Add inward
recess liners, overlapping blanket edges and continuous rim/pressure-plate step
walls at all 15 shared interfaces. Seal the CUP upper viewport trim too, preserving
its accepted glass geometry. All physics, triggers, node positions, configurations,
Kerbalism, textures and runtime remain unchanged from dev.3. Native regression,
UV handedness and liner checks pass; KSP confirmation pending.

## v0.7.0-dev.3 — Rounded HUB pressure junction

Replace the box-shaped HUB centre and straight shoulders with six joined
spherical shell patches and smooth curved necks. Preserve all six node positions,
the 4 m axial envelope, port diameter, matching endcaps, materials, service looms
and gameplay settings. Rebuild the HUB's 13 solid convex colliders to follow the
new shell. The other five native models and all textures are byte-identical to
dev.2. Add actual native-model before/after and multi-angle previews, spherical
seam/tangent checks, and exported collider containment checks. Offline checks
passed; visual acceptance and KSP radial-fit/gameplay confirmation pending.

## v0.7.0-dev.2 — Family exterior-detail pass

Refine all six native models and diffuse textures with original service hardware, dedicated detailed cladding, stitched insulation, common endcap detail and readable labels. Fix LOG shoulder coplanarity. Preserve all native physics/glass/variants, branding/light masks, gameplay configs, Kerbalism and runtime. Add current native-model previews and baseline regression audit. Offline checks passed; KSP review pending.

## v0.7.0-dev.1 — New RW-LOG-250 station logistics vault

- Implement native original **2.5 m × 3.0 m logistics module** using the shared ivory/bronze/graphite RoosterWorks materials and common two-ended pressure bulkheads. Includes eight paired cargo-service cassettes, instrument grille textures, latch hinges, structural railings, a central strengthening collar and branded labels.
- Add 12-slot **stock ModuleInventoryPart** with 1400 L packed volume, 600 EC, and fully compatible stock-KSP fallback (no Kerbalism resources required to load).
- Add optional **Kerbalism ProfileDefault** consumables: Food 120, Water 60, Oxygen 20,000, Nitrogen 8,500; empty Waste 120 and WasteWater 75. Add optional FeatureHabitat volume and surface figures, without fictitious generation or crew capacity.
- Add native `.mu`, OBJ/MTL, procedural Python generator, optional Blender reconstruction script, two original texture PNGs and 3-angle actual geometry-based review renders.
- Add new offline geometry/module/collider validator; retain previous five validators and shared live-runtime models unchanged.
- Packaging/metadata updated to dev.1; **not** yet in-game confirmed, not released to GitHub. Accepted v0.6.0-dev.2 cupola geometry is preserved.


## v0.6.0-dev.2 — Cupola glazing-frame joint cleanup

- Replace eight disconnected lower and upper window header arcs with **continuous full-circumference conical rings**. The original gaps existed where mullion lines met each segmented header.
- Build eight opaque graphite mullion foundations centred exactly on glass-sector boundaries. The foundations overlap both adjacent panes by 0.015 radian per side and extend under the upper and lower header rings. Strengthen mullions with ceramic structural spines, steel bevel edges and bronze detail.
- Enlarge the lower canopy retaining belt and add continuous graphite/ceramic/steel/bronze header lips, eliminating butt-joint seams at grazing angles.
- Add dark inner gasket/reveal backing *only at each glass perimeter*: keeps the centre of every window unobstructed and preserves the existing eight sloped pane sizes and canopy profile.
- Add subtle engineering details to the top cap: reinforced crown collar, sixteen inset graphite plates and small steel retaining studs. Original round overhead skylight dimension is unchanged.
- Regenerate **native RW_CUP_250.mu**, procedural OBJ/MTL source and three real mesh-based review renders. Extend cupola regression checks to enforce overlap margins and continuous header ranges.
- All other four native models, part configurations and runtime hatch DLL remain **byte-for-byte identical to v0.6.0-dev.1**. Cupola part CFG and Kerbalism supplies are unchanged. Version BUILD increments to 2.
- Offline validation passed; **VAB/flight window seams, canopy lights and Kerbalism still require in-game confirmation.** No GitHub commit/release is implied by this package.


## v0.6.0-dev.1 — New RW-CUP-250 observation cupola

- Add new original 2.5 m terminal, one-crew observation cupola with eight sloped canopy windows and overhead skylight, compact RoosterWorks service collar and bronze rings.
- Include native `.mu`, OBJ/MTL and procedural Python/Blender editable source, original label texture and actual mesh-based three-angle review renders.
- Provide a single size-2 lower stack node and an independent, closed 96-triangle convex collider. No EVA, docking ports, command or science experiments advertised.
- Stock temporary `cupolaInternal` IVA, warm-white exterior window illumination toggle and 300 ElectricCharge.
- Add conditional Kerbalism Default life-support quantities and optional Habitat (volume 6.2 m³, surface 17 m²).
- Include new cupola regression validator in the full static suite, installation notes and comprehensive in-game checklist.
- Preserve previous 0.5.3-rc.1 native HAB/LAB/CMD/HUB models, configs, textures and runtime DLL unchanged. Bump version metadata and append optional VAB Organizer category.
- **Development build only:** cupola and previously unconfirmed hub/endcaps require in-game validation. No publishing action performed.

# Change log

## v0.5.3-rc.1 — release preparation

- Package the v0.5.3 GameData payload without changing installed models, configuration, textures or runtime.
- Consolidate README, installation guidance and release notes; preserve development history and ChatGPT handoff.
- Prepare checksum-pinned source importer and prerelease checklist. No tag or release is published by packaging.

## v0.5.3

- Share the hub's layered endcap geometry across both ends of HAB, LAB and CMD while preserving attachment planes, colliders, glazing and runtime systems.

## v0.5.2

- Redesign hub interfaces with bronze insulation, small pressure closures, layered rims, piping and decorative rails using the user's visual reference.

## v0.5.1

- Refine hub rims, texture mapping, shoulder shading and branding.

## v0.5.0

- Add six-way HUB-250, native model/OBJ source, 13 solid colliders, six 2.5 m nodes and conditional Kerbalism Habitat.

## v0.4.6 — user-confirmed functional baseline

- Make HAB EVA/boarding access depend on selected exterior variant; add a functional Side Hatch ladder/grab point.

## v0.4.5

- Fix HAB self-obstruction with a solid convex hull and improve curved window seating, cutouts and winding.

## v0.4.4

- Classify all modules as Station to restore standalone CMD CommNet; add targeted late hatch registration and diagnostics.

Earlier editable sources/history are preserved under Source/Documentation/DEVELOPMENT_HISTORY.md.
