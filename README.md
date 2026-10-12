# RoosterWorks Station Modules — v0.6.0-dev.1

**KSP 1.12.5 | DEVELOPMENT TEST, not a published release.**

Original modular station family with RoosterWorks ivory thermal cladding, dark tinted glass, bronze insulation, original rooster crest and optional Kerbalism compatibility.

| Part | Purpose | Crew | Stack nodes |
|---|---|---:|---|
| RW-HAB-250 | Habitat with selectable functional exterior Side Hatch | 4 | two 2.5 m ends |
| RW-LAB-250 | Laboratory with stock / Kerbalism science | 2 | two 2.5 m ends |
| RW-CMD-250 | Compact station command, SAS and CommNet | 2 | two 2.5 m ends |
| RW-HUB-250 | Six-way structural pressurized junction | 0 | six 2.5 m sides |
| **RW-CUP-250** | **NEW: terminal observation cupola, eight sloped viewports and skylight** | **1** | **one 2.5 m bottom** |

v0.6.0-dev.1 includes a native `.mu` and editable `.obj` for the new 1.5m-class cupola, Blender reconstruction script, matching label texture, cabin-light shader action, one-seat temporary stock IVA, conditional Kerbalism supplies and volume, original convex collision mesh, review renders and regression validators.

**Cupola limitations:** no integrated EVA hatch, docking port, command avionics or research experiments. Use RW-CMD-250 for control and RW-HAB-250 Side Hatch for EVA. Window glazing uses the existing tinted-glass material; custom interior viewing is not yet provided. Its cabin light action is visual and does not consume electricity. Cupola has not been tested in KSP.

**Source preservation:** all non-versioned v0.5.3-rc.1 HAB/LAB/CMD/HUB native models, physics colliders, part configurations, original textures and hatch runtime DLL are retained byte-for-byte. The shared VAB Organizer optional patch receives a new cupola entry; root `.version` metadata is bumped for this dev build.

Run `python Tools/validate.py` after installing Pillow. Developer ZIP contains all original sources, new `Source/build_cup250.py`, Blender source reconstruction, `.mu`, verification scripts and KSP GameData. `Tools/render_cup250.py` requires NumPy and VTK only for previews. No KSP/Unity assemblies are redistributed.

Read `INSTALLATION.md` and `TEST_CHECKLIST-v0.6.0.md` before flight testing. No GitHub tag/release or source commit is implied by packaging. MIT licensed, original RoosterWorks assets.
