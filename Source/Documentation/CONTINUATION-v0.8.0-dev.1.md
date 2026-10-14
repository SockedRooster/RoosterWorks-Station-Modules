# v0.8.0-dev.1 — New RW-AIR-250 dedicated EVA chamber

User accepted dev.4 appearance and asked for the next asset, then selected the
dedicated 2.5 m EVA airlock from the presented role choices. No earlier remaining
parts roadmap was inferred. Checked current source kit, known HAB EVA/ladder
geometry and StationHatch.cs: that controller is explicitly HAB/variant-specific,
so it must not be added to the always-available dedicated airlock.

Created separate rw-v080dev1 from accepted rw-v070dev4. Added original native AIR
model, procedural source, OBJ/MTL and optional Blender reconstruction, label PNG,
part CFG, conditional Habitat patch and separate optional VABOrganizer patch.
No changes to accepted six modules or texture PNGs. airlock_baseline.json records
hashes from authentic dev.4 and enforces all original GameData except package version.

AIR: 2.5 m stack standard, 2.4 m length, top/bottom at ±1.2 m, two crew, 1.85 t,
400 EC, 2 inventory slots / 120 L, 7800 funds. Placeholder mk2CockpitStandardInternals
matches prior two-seat convention. Dedicated side hatch at angle 0/Y=-.15, trigger
centre radial 1.43 m. Always-present tagged Airlock and inward Ladder triggers on
layer21; no variants or new runtime plugin. Closed convex 96-triangle cylinder
contains the stock EVA clearance-ray origin. Boarding rails/rungs and porthole,
suit/pressure service panels, endcap liners and readable branding use current
accepted family geometry/style. Render model has 21,920 triangles.

Kerbalism FeatureHabitat supplies 6 m³ / 20 m². Connect to a supplied station;
no separate provision tanks or custom pressure-cycle/air-recovery system added.
Warm-white porthole light uses stock ModuleColorChanger, no electrical draw yet.
Exterior hatch/pressure apparatus remains non-animated; stock EVA operates via
native trigger. This is a flight-test candidate, not a proven working new exit.

Build AIR only: Tools/build_airlock.py. Full-family rebuild: Tools/build_appearance.py.
Validate: Tools/validate.py; adds validate_air250.py and extends current shared
rim/UV audit to 17 stack interfaces. Render: Tools/render_air250.py. Package:
Tools/package_appearance.py. Actual native MU preview is
Media/RW-AIR-250-v0.8.0-dev.1-Review.png. Blender scripts were not executed.

Offline and fresh-extracted package checks pass. AIR acceptance, IVA, actual
stock EVA/auto-grab/climb/reboarding and Kerbalism pressure/resource behaviour
remain pending; see AIRLOCK_TEST_CHECKLIST.md. All six accepted modules preserved.
No KSP installation, save modification, GitHub commit/tag/release performed.
