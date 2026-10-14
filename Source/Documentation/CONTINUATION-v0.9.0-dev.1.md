# v0.9.0-dev.1 — New RW-PWR-250 power and service core

User reported AIR "worked" and requested next build. After asking for information
on the proposed power/service module, user instructed "code it", authorizing the
described passive crewless battery module, detailed cabinets/conduits/cosmetic
cooling, separate generation/radiators and matching 2.5 m interfaces. The proposed
2.4 m length is retained. Chosen candidate balance: 15000 EC, 2.5 t, 12500 funds,
largeElectrics; these were implementation choices rather than prior requirements.

Created separate rw-v090dev1 from accepted rw-v080dev1. PWR has eight cell cabinets,
protected cables, closed service connectors, small fin hardware and four central
radial mounting areas. Standard stock electric storage supplies the connected
vessel; no new generator, active cooling or electrical controller. No crew, IVA,
EVA, Habitat or gas resources. Kerbalism compatibility uses normal ElectricCharge;
no custom conversion patch needed. No new VABOrganizer patch added; stock
Electrical classification is used. Existing optional patches remain untouched.

All accepted seven-module GameData except package version is byte-identical,
enforced by Tools/power_baseline.json recorded BEFORE building. New PWR CFG, MU,
two PNG textures, OBJ/MTL and Python/optional Blender source. Native 21772 visual
triangles, one watertight convex 96-triangle cylinder collider. Six prior modules'
warm-white lights remain intact; PWR itself has no crew lighting or windows.
Sealed shared caps at ±1.2 m and readable Unity-facing badges preserve accepted
rim/UV fixes. Existing AIR native exit/ladder and runtime are untouched.

Build: Tools/build_power.py (PWR only) or Tools/build_appearance.py (eight parts).
Validate: Tools/validate.py, including validate_pwr250.py and current seam audit
extended to 19 stack interfaces. Render: Tools/render_pwr250.py, actual native MU
preview Media/RW-PWR-250-v0.9.0-dev.1-Review.png. Package: Tools/package_appearance.py.
Blender scripts were not executed; source and editable OBJ/MTL are provided.

Offline and fresh-extracted package checks passed. PWR visual acceptance and
actual charging/discharging, external mounts and Kerbalism electricity behaviour
pending; POWER_TEST_CHECKLIST.md covers runtime tests. User's AIR success is an
overall report, not individual Kerbalism/performance measurements. No install,
save change, GitHub commit/tag/release performed. Previous archives remain intact.
