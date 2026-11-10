# GRAV-250 compact stow — v0.7.5-dev.9 TEST

The folded silhouette now has eight fuller pressure packs in two alternating
rows around the hub. Spokes telescope from 2.75 m deployed reach to 0.95 m
when stowed; their diameter is retained. Packs retain 50% radial thickness,
85% axial height and 70% tangential width, replacing the tiny 18% scale from
dev.8. The complete stowed model fits within the hub's 3.7 m axial span.
Keep the recommended 5 m fairing; this is a shorter package, not a narrower one.

Sliding root mounts move the folded packs out just enough to clear the hub.
Hinge pins keep their proportions. Pressure passages telescope with their
arms and their seals follow the pivots. The entire original deployed geometry
is unchanged, with only new small root guides added. Hub attachment points,
mass, crew capacity, resources, rotation/power behavior and crew interlocks
are retained. The user-confirmed lighting fix, mask and stock light controls
remain byte-identical, as do the corrected color maps and shared plugins.

Close KSP, replace only GameData/RoosterWorksStationModules, then restart.
Preview Stowed/Unfolding/Deployed under Media/GravityRing. Test deploy/fold
and rotation on an uncrewed test part before using it on a working station.
No game installation, existing build or save was modified preparing this kit.

2,652 actual controller-source assertions pass. Native checks evaluate five
folding positions, pressure-pack clearance from the hub, shorter axial bounds,
unchanged full-deployment vertices for every old mesh, accepted lighting/mask
and map bytes, collider/material validity and preserved prior files. In-game
visual/physics acceptance is pending. Existing 3,690 color regressions remain
valid because their runtime, map entries and targeted meshes are unchanged.

Current builder Source/build_gravity_ring.py, runtime Source/GravityRing.cs,
packed editable source Source/Blender/RW_GRAV_250.blend. See GRAVITY_RING.md
for the retained limitations: visual rotation only; no physical gravity,
rotating IVA or automatically granted ring habitation/comfort bonus.
