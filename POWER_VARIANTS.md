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

# RoosterWorks v0.15.0-dev.1 — PWR stock reactor variants

The user accepted the improved grey finish, then requested that the reactor be selectable on the PWR module with stock-style coloured variant swatches and proportionally reduced storage. This build preserves the accepted dev.2 finish module, both sizes' models and all other parts byte-for-byte.

Place **RW-PWR-250** or **RW-PWR-375**, right-click and use **Variant: Battery only / Integrated nuclear**. The stock editor variant control has coloured swatches. **Exterior finish: White / Grey metal** remains a separate choice, giving four combinations per core. No separate nuclear catalogue entry is needed with Kerbalism Default.

| Core | Battery-only EC | Nuclear EC | Nuclear output |
|---|---:|---:|---:|
| PWR-250 | 3500 | 3060 | 5.5 EC/s |
| PWR-375 | 6750 | 5910 | 6 EC/s |

The reactor and integrated cooling reserve **one of eight modeled battery bays**. That design allocation removes **12.5%** of battery capacity in either size; it is a stated bay allocation, not a physically measured reactor-volume estimate. The familiar exterior and mounting interfaces remain unchanged. Reactor dry mass/cost additions remain 0.0429 t / 11968 (250), 0.0468 t / 13056 (375), applied through the stock variant. The original non-reactor part mass and cost remain the baseline.

Nuclear has 1.65 / 1.8 units of EnrichedUranium, matching depleted-fuel tank capacity. Consumption remains 7.17266e-9 / 7.82472e-9 units per second with 1:1 retained waste; empty fuel or full waste blocks production. It starts off when installed in the editor. External radiators are not required: the existing fixed built-in-cooling abstraction remains. Only excess electricity can be dumped. No crop, life-support, lighting, other battery, geometry, glass, hatch or physics change is made.

## Switching and saved vessels

Hardware configuration is an **editor** operation. Editor switches preserve the EC fill fraction, exchange fuel/waste tanks and leave the reactor off. A passive core has zero process capacity, no fuel tanks and disabled reactor controls. The runtime also removes a passive pseudo-resource if Kerbalism initializes it after our module. Flight loading preserves remaining fuel, waste, absolute charge and saved reactor-running state. Missing flight fuel is empty, never regenerated by loading.

The old `RW_PWR_250_REACTOR` and `RW_PWR_375_REACTOR` definitions are retained and hidden from the Kerbalism Default catalogue so saved vessels still load. Their previous inventory is preserved; newly placed standard PWR parts use the new variant selector and storage tradeoff. No save conversion occurs.

The new stock-variant integration requires **ModuleManager, Kerbalism Default and Community Resource Pack**, which are present in the reference game. It does not require B9PartSwitch or SystemHeat. Without that profile combination, ordinary passive PWR parts remain available and the historical standalone stock-converter reactor editions retain their prior fallback behavior. The accepted grey finish continues independently.

## Source and checks

Inspect this source kit before future changes. `Source/build_power_options.py` emits `Compatibility/PowerVariants.cfg` without altering original part CFGs. `Source/build_options.py` calls it from the canonical and per-asset build wrappers. `Source/build_family375.py` excludes all-size option patches when deriving large-family patches. `Tools/build-power-runtime.ps1` compiles `Source/PowerVariant.cs` against KSP 1.12.5 APIs to a separate `RoosterWorksPowerVariants.dll`; original hatch and accepted finish DLLs remain identical. Reflection invokes Kerbalism's public Configure/SetRunning API while avoiding an assembly dependency for other profiles.

`Tools/validate.py` includes the preserved family suite and `validate_power_variants.py`. The latter validates both swatch configurations, storage ratios, mass/cost additions, guards and legacy definitions, and verifies every prior dev.2 GameData fingerprint apart from version metadata. `Tools/test-power-variants.ps1` executes the actual C# source with state doubles: repeated switches in both sizes, charge fill fractions, passive process shutdown, delayed Kerbalism startup, stopped nuclear startup, preserved running state, no flight refuelling and no repeated editor ship-modification loop. DLL compilation uses installed game assemblies.

## In-game checklist

- Close KSP and replace the RoosterWorks folder with this TEST ZIP, then restart. Existing saves are not modified by the package.
- On newly placed PWR-250/PWR-375, switch both stock Variant choices and both finishes; check symmetry and craft save/reload.
- Confirm exact capacities above, nuclear mass/cost additions, no fuel or active reactor button in Battery only, and finite fuel/empty waste plus start control in Integrated nuclear.
- Start/stop the reactor, test empty fuel/full waste, time warp and background generation. Inspect saved flight resource amounts and reactor-running state after reload.
- Confirm old nuclear craft still load and all accepted finishes, lighting, glass, seals and hatch functions remain intact.

Offline source/config/preservation checks are evidence only; actual KSP stock UI, mass/cost behavior and loaded/background gameplay confirmation remain pending. No installation, save edits, GitHub changes or release was performed.
