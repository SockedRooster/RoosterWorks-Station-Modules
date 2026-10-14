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
