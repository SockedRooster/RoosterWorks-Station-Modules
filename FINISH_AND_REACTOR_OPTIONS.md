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

# v0.14.0-dev.2 loading/selection fixes

User reported that the finish control appeared but left parts white, and the reactor option was not visible. The installed KSP.log confirms the finish DLL and both nuclear parts loaded. ModuleManager.ConfigCache confirms their fuel/controller configuration and the later experimentalElectrics tier. Missing files or dependency rejection did not cause the observed absence.

Finish now responds directly to both editor field and symmetry callbacks, with Unity Update covering both editor and flight. The old PartModule.OnUpdate-based test did not reproduce the editor lifecycle and failed to catch this bug. The new source test invokes the actual editor callback without OnUpdate and checks a texture-name fallback for renamed materials. Actual KSP compilation passed; this is not a substitute for live visual confirmation.

Nuclear parts now use the same largeElectrics research tier as ordinary PWR cores and are explicitly assigned to VABOrganizer's installed nuclearReactors category. Search **nuclear** or look under **Electrical / Nuclear Reactors**. Choose the separately named **Nuclear Power and Service Core**; the ordinary PWR part still has no reactor. Capacities, output, fuel and cooling behavior are unchanged.

Close KSP before replacing the RoosterWorks folder with this TEST build. Place a part, right-click it and select **Exterior finish: Grey metal**. Switch back to White, test symmetry and reload the craft. Live editor/flight and reactor operation confirmation is still required. No installed files or saves were modified by this fix.

# RoosterWorks v0.14.0-dev.2 — optional grey metal and nuclear cores

All 19 existing parts, including the adapter, offer **Exterior finish: White / Grey metal** in the editor. White is the default. The saved choice is restored in flight and propagates to editor symmetry counterparts. Finish is independent of the HAB Standard / SideHatch selector: both hatch arrangements support both colours. Four shell diffuse textures change; original meshes, collision, glass, readable branding, copper accents and warm-white lighting are preserved. Grey is a metal-coloured finish using the existing shaders.

PWR battery capacities are **3500 EC (250)** and **6750 EC (375)**. These explicit user overrides supersede the previous battery-reference proxy and its +5% rule. Every other part retains v0.13 capacities. Both passive and nuclear editions use the same battery capacities; crewless PWR parts do not receive Kerbalism's crewed-part battery multiplier.

Two optional, separately named editor editions add a reactor to the existing PWR body. Separate IDs keep old passive PWR craft from acquiring a reactor or nuclear fuel. Nuclear editions also offer both finishes. The catalogue contains 19 established parts plus 2 optional nuclear editions, reusing the 19 existing native models.

| Property | Nuclear PWR-250 | Nuclear PWR-375 |
|---|---:|---:|
| Output | 5.5 EC/s | 6 EC/s |
| Battery | 3500 EC | 6750 EC |
| EnrichedUranium capacity / initially full | 1.65 | 1.8 |
| DepletedFuel capacity / initially empty | 1.65 | 1.8 |
| Fuel consumption, units/s | 7.17266e-9 | 7.82472e-9 |
| Added dry reactor/cooling mass | 0.0429 t | 0.0468 t |
| Total core dry mass | 2.5429 t | 8.4843 t |
| Added purchase cost | 11968 | 13056 |

Balance uses the installed Near Future Electrical SNAP-10A (`nfe-reactor-tiny-1`): 5 EC/s, 1.5 fuel / waste units, 6.5206e-9 fuel units/s, 0.014 t bare reactor plus 0.025 t integrated radiator hardware. Output, fuel/waste storage, consumption and added hardware mass/cost receive +10% / +20%. Full-power fuel life is unchanged at about 230040180 seconds (~25 Kerbin years). The screenshot's 5 EC entry was battery storage; its full source independently confirms 5 EC/s generation. The screenshot's displayed loaded mass is not the entire station core mass.

**Cooling is built in. External radiators are not required.** This is a fixed-cooling balance abstraction: there is no SystemHeat loop or additional thermal simulation. Uranium converts 1:1 into retained depleted fuel. Empty uranium or full waste storage stops generation. Only excess EC may be dumped; waste is never discarded for unlimited runtime. Reactor starts **off**; use its start/stop control. Reactor editions share the passive cores' largeElectrics tier and are explicitly grouped under VABOrganizer nuclearReactors. Passive cores are grouped under batteries. They remain separate catalogue parts, not a right-click nuclear variant.

## Requirements and behavior

ModuleManager is required for finish and compatibility patches. The included `RoosterWorksFinish.dll` provides only the persistent exterior selector and has been compiled against installed KSP 1.12.5 assemblies. The original hatch DLL remains byte-identical. No NFE, SystemHeat or B9 plugin is required by the nuclear editions.

Nuclear editions require **Community Resource Pack**, already present in the reference game, for EnrichedUranium and DepletedFuel definitions. With Kerbalism Default, a dedicated `ProcessController` and profile process provide loaded/background production and planner rates. Without Kerbalism, mutually exclusive stock `ModuleResourceConverter` nodes provide loaded-vessel generation. Other Kerbalism profiles hide the nuclear editions until a profile integration exists. Passive parts and finishes remain available. No custom refuelling tool is supplied; fuel logistics use the installed game's resource-transfer facilities.

## Build and evidence

Inspect the developer kit before future edits. `Tools/build_appearance.py` remains the canonical native geometry/texture/OBJ build; it applies the frozen EC policy and calls `Source/build_options.py` after building the family. The options generator can regenerate grey textures/reactor editions without rebuilding native models. `Tools/build-finish-runtime.ps1` builds the separate finish DLL using installed KSP managed assemblies and the .NET compiler. `Tools/build_ec_balance.py` refreshes policy/options/version/manifest. All per-asset build wrappers refresh optional content. `Source/Balancing/compact_reactor_reference.json` freezes the exact reference values and config fingerprint.

`Tools/validate.py` runs the preserved model/gameplay suite plus `validate_options.py`. The latter checks all v0.13 GameData fingerprints, permitting only PWR battery changes and version metadata; checks all 19 models' finish coverage and texture alpha; checks exclusive reactor implementations, fuel balance, storage, cooling and rates; verifies deterministic regeneration. `Tools/test-finish.ps1` exercises the actual C# selector source with state doubles. It verifies repeated white/grey changes, overlapping material suffixes, a saved flight choice, symmetry settings and glass/logo/lamp preservation. These checks do not simulate Unity rendering or Kerbalism background execution.

## KSP confirmation checklist

- Use newly placed parts to check capacities. Saved craft/vessels may retain serialized older resource capacities; no save migration is performed.
- On every part and both sizes, switch White -> Grey metal -> White; check symmetry and save/reload a craft with mixed finishes.
- On HAB, exercise Standard and SideHatch with both finishes; check EVA/reboarding and lighting as before.
- Check translucent greenhouse/cupola glass, readable badges and warm-white light controls in VAB and flight.
- Compare passive and nuclear PWR entries. Passive cores must have no uranium, reactor button or generation.
- Nuclear cores: 3500/6750 EC; 1.65/1.8 uranium and empty waste; start off; start generates 5.5/6 EC per second; stop halts fuel use/output. No external radiators fitted.
- With Kerbalism Default, compare planner output, loaded generation and background/time-warp fuel/waste changes. Confirm empty fuel and full waste each stop output, and a full battery cannot discard waste.
- If using the stock fallback, confirm exactly one converter and the same rates while the vessel is loaded.

Offline checks and ZIP integrity are build evidence. Live KSP visual, editor, save/reload, cooling and background gameplay confirmation remain pending. This kit is a development TEST build; no installation, save modification, GitHub commit/publication or release has been performed.
