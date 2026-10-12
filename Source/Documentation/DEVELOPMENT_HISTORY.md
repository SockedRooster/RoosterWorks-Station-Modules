## v0.5.3 — matching station endcaps

HAB, LAB and CMD now share the hub's layered endcap mesh: recessed bronze insulation, small central pressure closure, narrow structural rings, porthole detail, rails, service lines and rooster branding. Both ends use the same geometry and texture mapping, fitted to the original stack planes. The endcap details are decorative; HAB's working Side Hatch remains its EVA exit.

The shared source is Source/station_endcaps.py. HUB model geometry remains byte-identical to v0.5.2. Attachment nodes, all colliders, runtime plugin, part configs, lights and Kerbalism/science patches are preserved. Existing textures, including the bronze blanket, are preserved. Rebuilds here updated geometry only, not textures. Media/Station-endcaps-v053.png shows the actual meshes.

Install with KSP closed. Check exposed top and bottom faces on all three modules and flush connections to the hub and one another. Confirm HAB Side Hatch EVA/boarding, lights, control/signal and LAB science still behave as before. Static mesh/config checks pass; this revision's in-game appearance remains pending.

## v0.5.2 — layered port faces

Reworked from the user's visual reference: smaller central pressure closures, recessed bronze insulation with shallow modeled folds, thin dark outer rings, fasteners, stand-off rail arcs and routed service lines. Original RoosterWorks materials, branding and independently generated geometry/texture. Branding orientation is corrected on all side ports. All six attachment locations remain unchanged.

The exterior rail, hatch and piping details are decorative: this hub has no EVA exit, functional ladder, or integrated docking port. Use HAB Side Hatch for EVA and fit separate docking ports for docking. The hub still awaits in-game functional and visual confirmation.

## v0.5.1 visual revision

Replaces the wide grey port discs with narrow mating rims, recessed pressure plates, latch details and flat readable branding. Shoulder textures use continuous mapping and smoother normals; the distorted shoulder decals are removed. All six node positions and the existing collision geometry remain unchanged. Pressure-plate details are decorative, not EVA hatches. Hub attachment and flight behavior still require testing.

# Change log

## v0.5.0 — Six-way station hub (TEST)

- Add RW-HUB-250: six 2.5 m stack interfaces, four-way side-node symmetry, pass-through structural role, original matching shell/trim/rooster styling.
- Add native MU, OBJ/MTL source, procedural generator, preview and geometry/config regression checks.
- Add conditional Kerbalism Habitat volume; no dedicated crew seats or exterior EVA exit.
- Preserve all existing HAB/LAB/CMD GameData files byte-for-byte, including the confirmed v0.4.6 hatch runtime. Only shared package version metadata changes.
- Static checks pass; hub flight/attachment/transfer and Kerbalism confirmation remain pending.

# Change log

## v0.4.6 — Side Hatch access and EVA grab rails (TEST)

- User confirmed v0.4.5 EVA, window improvement and radial attachments.
- Add Side Hatch grab rails, curved footholds and an inward-facing native Ladder trigger centered on the working EVA exit.
- Gate the airlock, ladder and portrait EVA by selected exterior variant; Standard Windows no longer supplies an invisible exit.
- Preserve original EVA restrictions when restoring access, and keep editor changes from carrying a temporary EVA lock into flight.
- Validate access transitions using the actual controller method with test doubles; compile the plugin against installed KSP 1.12.5 assemblies. In-game grab/boarding and variant gating await confirmation.
- Preserve working collision hull, airlock position, windows, branding, lights, CMD/LAB, science and Kerbalism integrations.

# Change log

## v0.4.5 — HAB self-obstruction and window seating (TEST)

- User confirmed v0.4.4 control, signal and science working. Preserve those configurations.
- Runtime diagnostics confirm the HAB Airlock is active and registered without fallback, with a crew member eligible for EVA. The failure is now obstruction.
- Replace 12 hollow wall boxes and two end boxes with one closed, convex, 24-sided hull. Reproducing KSP's outward ray against the old boxes hits wall 01 at 0.200 m; the new solid volume contains the ray origin with 0.227 m margin. This addresses self-obstruction while retaining stock checks for external obstacles.
- Cut complete enlarged window-bank footprints from every overlapping hull course. Seat the surrounding frames to the cylinder, reduce window trim to at most 3 mm above the cladding, and tessellate glazing to follow the curvature.
- Correct inward winding on the rectangular foundation/hatch rings and circular hatch glazing.
- Extend diagnostics to identify a remaining exit obstruction. Runtime EVA/boarding and final in-game window appearance remain pending.
- Textures, warm-white lighting, rooster logo, CMD/LAB models, science and Kerbalism patches preserved. Custom IVAs remain deferred.

# Change log

## v0.4.4 â€” Station classification and late hatch registration (TEST)

- Runtime/save evidence establishes that RW-only vessels launch as Debris. KSP 1.12.5 CommNetVessel.OnStart destroys the connection component for Debris, SpaceObject and Unknown. Explicitly classify HAB/LAB/CMD as Station.
- Add a small HAB-only runtime module: if Part.airlock is null after startup, bind the existing active, enabled, named Airlock trigger on layer 21. Log whether binding was needed and the EVA eligibility state. This is a targeted fallback, not a runtime-confirmed EVA root-cause fix.
- No model, texture, light, lab science, crew-capacity or Kerbalism patch changes.
- Existing saved Debris vessels require reclassification or fresh craft; no save rewriting or automatic vessel reclassification.

# Change log

## v0.4.3 â€” EVA registration + station CommNet control point (test)

- Keep RW-HAB-250 Airlock-tagged trigger continuously active on its native model; remove cosmetic variant toggle for that transform so KSP can cache it in Part.Awake.
- Add stock `ModuleProbeControlPoint` to RW-CMD-250, requiring one crew member for crewed control-point functionality; preserve its separate direct/internal transmitters.
- No changes to existing meshes, textures, supplies, lights or lab science.
- This is not a verified CommNet/EVA runtime fix; test both and report result.

# RoosterWorks Station Modules â€” Changelog

## v0.4.2 (TEST) â€” Side Hatch EVA trigger

- Added a proper native KSP `Airlock` BoxCollider *trigger* on physics layer 21 at the HAB-250 side hatch's outward-facing spawn location.
- Connected it to the two stock visual variants: Standard Windows disables the EVA trigger; Exterior Side Hatch enables it.
- Kept the existing modeled hatch, HAB/CMD/LAB configurations and textures unchanged.
- No compiled plugin; first functional-EVA candidate requires in-game EVA/boarding and variant switching tests.

---

## v0.4.1 (TEST) â€” Station command control/telemetry correction

- Reworked **RW-CMD-250 command configuration** after an in-game report of no signal and no Kerbin remote control.
- Added a separate **INTERNAL short-range 500 k antenna** to complement the existing **DIRECT 5 Mm transmitter**; no extra mesh/antenna part required.
- Removed command hibernation and explicitly configured `requiresPilot = false` (crew of any profession), `remoteControl = true` and `requiresTelemetry = true` (uncrewed control still requires a valid signal).
- Preserved both crew seats, existing SAS, reaction wheel, direct antenna, science, visuals, supplies, lights, part ID and model geometry.
- Updated the static validator to assert presence of both transmitter modules and the new command-state settings.
- **This is a targeted configuration test, not a verified fix yet**: command authority/CommNet/Kerbalism radio behavior must be checked in KSP.

---

## v0.4.0 (WIP) â€” Laboratory science and compact command station

- Added **RW-CMD-250**: compact 2.5 m Ã— 1.72 m two-seat command module, five recessed windows, original procedural `.mu` model/textures, flush endcaps, avionics exterior, rooster emblem and warm-white cabin lighting.
- Added autonomous-capable ModuleCommand, SAS, moderate reaction-wheel torque, direct antenna, 2,400 ElectricCharge and optional Kerbalism-Default life support storage/habitat configuration.
- Finalized **RW-LAB-250** science capabilities: six stock experiments (temperature, pressure, gravity, atmosphere, materials and Goo) with ModuleScienceExperiment IDs; Kerbalism FeatureScience-native replacements plus conditional `geigerCounter`, HardDrive and sample-analysis lab.
- Stock/Kerbalism science modes are mutually exclusive via ModuleManager. Geiger is Kerbalism-only; stock KSP has no built-in Geiger experiment.
- Lab v0.3.0 exterior geometry and HAB v0.2.7 geometry remain visually unchanged pending previous VAB-feedback decisions.
- Added command Blender reconstruction script, OBJ/MTL, KSP model, review render and three-part static validation.
- **Test build, not stable release; in-game science/command/IVA compatibility not yet established.**

## v0.3.0 (WIP) â€” RW-LAB-250 initial model

- New science laboratory procedural mesh with three independent viewports, equipment panels, passive radiators and optical sensor.
- Stock Mobile Processing Lab / conditional Kerbalism sample-analysis processing.

## v0.2.7 (WIP) â€” RW-HAB-250 preserved

- Latest HAB geometry revision: curved window/hatch mounting; both exterior variants and warm-white illumination.
- Residual curved-hull frame fit issue acknowledged and deferred.
