# RoosterWorks Station Modules — v0.7.5-dev.4

> **Release status (October 14, 2026):** v0.6.0 is the latest published stable release. **v0.7.5-dev.4 is the upcoming release candidate; the maintainer has completed in-game testing.** No v0.7.5 stable GitHub release has been published yet. Earlier development-stage testing warnings below are historical notes and do not describe the current candidate's testing status.


Command data archives now have five editor choices: 200–1000 MB at 2.5 m, 675–3375 MB at 3.75 m, and 1600–8000 MB at 5 m. Preserves dev3 ring fix, LAB tiers and all prior native models/gameplay. See COMMAND_STORAGE_075.md. Offline checks do not establish in-game acceptance or release status.

## Retained development history

# RoosterWorks Station Modules — v0.7.5-dev.3

Ring selector hotfix: resynchronizes live color selections and reconnects ring materials/meshes after editor/model rebuilds. Models, textures, configs, capacity tiers, reactors and surface options retained from dev2. See RING_MENU_HOTFIX.md. In-game reopen/reselect confirmation pending.

## Retained development history

# RoosterWorks Station Modules — v0.7.5-dev.2

Roadmap 0.7 adds eleven native 5 m station modules and a 3.75-to-5 m adapter. Roadmap 0.75 adds compact two-crew HABs, 4/6/8 m long crew tubes, ten adjustable LAB data/sample tiers and grouped editor appearance swatches. The current catalogue has 41 parts, plus the two hidden historical reactor IDs. White/Grey finish, ring colors, LOG contents, hatch and reactor variants, warm-white lighting and current science limits are retained. Prior part IDs and models remain unchanged.

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

# v0.14.0-dev.1 installation

Copy the TEST ZIP's `GameData/RoosterWorksStationModules` folder into your KSP 1.12.5 `GameData`, replacing the previous RoosterWorks folder. Keep ModuleManager installed. Nuclear editions require Community Resource Pack; with Kerbalism use the Default profile. The package includes the original hatch plugin plus the separate finish plugin. The Developer Source ZIP contains the identical playable GameData plus procedural source and validation tools.

Choose Exterior finish in the editor. Nuclear cores are separately named optional editor entries; reactors start off. Existing passive cores remain passive. Prefer newly placed parts when checking the changed PWR capacities. Check FINISH_AND_REACTOR_OPTIONS.md before reviewing the build in game.

## Historical installation notes

# Install RoosterWorks Station Modules v0.13.0-dev.1 (KSP 1.12.5)

1. Quit KSP and back up existing saves. Keep the prior v0.8.0-dev.1 archive available for rollback.
2. Delete the prior `GameData/RoosterWorksStationModules` folder (do not merge old versions).
3. Extract the **TEST.zip** into the KSP root so `GameData/RoosterWorksStationModules/Parts/RW_LOG_250.cfg` exists. Do not nest additional GameData levels.
4. Remove any obsolete standalone `CMD250_CommNet_Diagnostic_A.cfg` patch if it remains anywhere in GameData.
5. Restart KSP; in the VAB, search for **RW-LOG-250** or **RoosterWorks** under Utility. Attach it by either size-2 end to HAB/CMD/HUB using the original RoosterWorks stack interfaces.
6. Stock KSP has 12 cargo slots and 600 EC; Kerbalism supplies are added ONLY when Kerbalism and the matching Default profile are installed.
7. Use a separate CMD-250 for station control and HAB-250 Side Hatch for EVA. Logistics compartment grilles/doors are visual; they do not open.
8. Follow `APPEARANCE_TEST_CHECKLIST.md` and `TEST_CHECKLIST-v0.7.0.md`. For in-game failures provide KSP.log, ModuleManager.ConfigCache, craft file and screenshots.

Never delete this mod while loading saves containing its modules. New development builds are not guaranteed save-safe.

For the new airlock, search RW-AIR-250 under Utility and follow AIRLOCK_TEST_CHECKLIST.md.
Transfer crew into AIR before testing portrait EVA. Its exit is always present; the
HAB-only variant controller is deliberately not attached to AIR.

For RW-PWR-250, search under Electrical and follow POWER_TEST_CHECKLIST.md.
Use separate generating parts to recharge its battery. Cooling fins are decorative.

Find RW-ADP-250-375 in Structural and follow ADAPTER_TEST_CHECKLIST.md.

Find RW-GRN-250 in Utility. Use the standard Kerbalism Default configuration/
greenhouse part; follow GREENHOUSE_TEST_CHECKLIST.md before relying on production.

This full package contains both 2.5 m and 3.75 m parts. Greenhouse inspection
lighting uses stock Lights On/Off or the Light action group, separate from growth.

EC figures in earlier checklists are superseded by ELECTRIC_CHARGE_BALANCE.md.
Compare newly placed parts after loading the new configs; existing saved resource
capacities may persist. LAB/AIR/LOG/GRN require connected station batteries.
