# RoosterWorks Station Modules — continuation checkpoint v0.6.0-dev.1

Prepared October 12, 2026 as a new in-chat developer prototype, **not a GitHub release or commit**.

Baseline is the complete uploaded v0.5.3-rc.1 Developer Source. We explicitly preserved all v0.5.3 native HAB/LAB/CMD/HUB files and working v0.4.6 EVA+control DLL; only changed common VAB Organizer and .version metadata as part of the new v0.6.0-dev.1 dev build.

## New work

RW-CUP-250 terminal observation cupola with one 2.5 m bottom stack node at -0.860, one seat, eight sloped panoramic window panels and top glass viewport, original ivory/bronze/rooster materials, one temporary stock cupolaInternal IVA, 300 EC, warm-white KSP ModuleColorChanger toggle. No integrated EVA hatch, docking port, science experiment or command. Needs an external CMD-250 to control vessel and a HAB Side Hatch for EVA. Conditional Kerbalism Default supplies and FeatureHabitat pressure (volume 6.2 / surface 17). Original generator Source/build_cup250.py, Blender reconstruction Source/Blender/create_cup250.py, OBJ/MTL and .mu assets. Tools/validate_cup250.py tests native geometry, configuration and watertight convex collider. Tools/render_cup250.py produces genuine actual-mesh 3-angle previews with VTK.

## Confirmations

Offline tests: `python Tools/validate.py` PASSED, includes 5 modules and original 0.5.3/0.4.6 regressions. 36 GameData files with SHA256 manifest. All 32 original GameData files remain unchanged except VABOrganizer.cfg and .version; four new GameData files added. Root README/RELEASE_NOTES/INSTALLATION/CHANGELOG and Tools scripts updated to support version.

**No KSP runtime tests were possible here**, especially hub assembly/symmetry, cupola fitting, crew portrait/transfer, render/light action, IVA, pressure, or HAB/CMD/LAB regressions. Use TEST_CHECKLIST-v0.6.0.md. v0.5.3-rc.1 release remains pending user in-game approval and was not published.

## Future guidance

Keep current RWS-style dark tinted glass and ivory/bronze/crest; do not copy SSPXr models. For live KSP bugs request current KSP.log and GameData/ModuleManager.ConfigCache before speculating. Treat old Source/Documentation/CHATGPT_HANDOFF.md as historically accurate for v0.5.3; this file supersedes it for v0.6.0-dev.1 status. Do not publish this developer build as stable without requested approval.
