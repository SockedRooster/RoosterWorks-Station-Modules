# GRAV-250 corrections — v0.7.5-dev.8 TEST

- Fixed the console FormatException in ModuleRWRingColor.Bind. The generated
  map used 0-255; the established runtime requires start:count, e.g. 0:256.
  All four new map entries now use that grammar. The existing shared color
  plugin remains byte-identical, protecting other station/ground ring controls.
- Gave all eight window banks a dedicated full-white emission mask. The old
  HAB mask depended on HAB UVs and did not match the ring's torus UVs. Added an
  explicit opaque alpha curve to the stock Ring Lights control. Existing
  On/Off and Lights action-group behavior remains; no new lighting plugin.
- Added two opposed enclosed pressure-access tubes from the rotary hub to
  the perimeter, with bands, pivot seals and colliders. They fold with their
  spokes and rotate with the ring. Their stow angles allow clearance around
  a 2.5 m inline module. The assembly still needs a 5 m launch fairing.

Replace only GameData/RoosterWorksStationModules while KSP is closed, then
restart. Test ring color changes/reopening, lights off/on, full folding and
rotation. Existing saved light-off states remain off until switched on.
No installation or saves were modified preparing this build.

The console spam was our map-generation bug. It is distinct from the earlier
native crash stack in Parallax.CollisionManager.RemoveQueuedData. This update
does not change Parallax or include the separate collision diagnostic.

3,690 source-aware color assertions reproduce the old FormatException, then
test the corrected actual maps with all colors/reopens/native resets. 1,788
rotation/folding assertions pass. Native validation checks emission-mask
coverage, light targets/curves, mesh normals/colliders, passage ownership and
fixed-node clearance in addition to five fold poses and preservation hashes.
Full in-game visual/physics confirmation remains pending.

Current source: Source/build_gravity_ring.py, Source/GravityRing.cs and
Source/Blender/RW_GRAV_250.blend. Helpers: Tools/prepare_gravity_fixes.py,
Tools/test-gravity-colors.ps1, Tools/test-gravity-ring.ps1,
Tools/validate_gravity_ring.py. Preview Media/GravityRing/Deployed.png.
The general gravity-ring limitations remain described in GRAVITY_RING.md:
visual rotation only; no physical gravity, rotating IVA or extra habitat bonus.
