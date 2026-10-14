# v0.7.0-dev.4 — Family badge and recessed-rim fixes

User supplied two actual KSP screenshots reporting backwards RoosterWorks
badges on every module and a gap between endcaps and rims at every end. Screenshots
are retained in Media/In-game-dev3-LOG-mirrored-badge.png and
Media/In-game-dev3-endcap-rim-gap.png. They show defects in the preceding build;
do not infer complete gameplay or visual acceptance from them.

Revised a separate copy rw-v070dev4, preserving prior source and archives.
Correct source UVs for all nameplate/crest/cladding materials via surface_uv.py;
remove inconsistent HAB/LAB/CMD native-export-only crest flips. Reverse detail
atlas U within each island to preserve intended slot selection. Original PNGs
remain byte-identical. Native UV triangle handedness now matches Unity outward
viewing. The old CPU camera used a right-handed screen basis and concealed
mirrored in-game lettering; corrected it to Unity's camera orientation.

Shared endcap inner cylindrical wall had outward normals, so it disappeared when
seen from within the recessed face. Add correctly wound inward liners and rim
step walls, extend blanket edge under the liner, close outer skirt to top lip,
and fill stepped central-closure edges. All 15 shared interfaces inherit this.
Cupola upper skylight trim also gets an inward liner and overlapping lip; accepted
glass geometry and canopy frame profile are retained. All caps remain within
existing mating planes; no stack node movement or functional door added.

Golden seam_revision_baseline.json was captured from authentic dev.3 BEFORE
rebuilding. All six collider sets, triggers, glass, HAB variants and material
semantics match dev.3 exactly; every non-model/version GameData file, including
all texture PNGs, configs, Kerbalism patches and runtime DLL, is byte-identical.
New validate_surface_fixes.py checks native readable UV determinants and actual
exported liner presence/orientation/overlap on every shared end and CUP crown.
It supplements the complete original suite and preserved native regression.

Build: Tools/build_appearance.py. Latest family/module/detail previews use dev.4
names; close review is Media/RoosterWorks-v0.7.0-dev.4-Surface-Fixes.png generated
by Tools/render_surface_fixes.py. Native MU and OBJ/MTL regenerated; optional
Blender reconstruction was not executed. Source exports retain Unity coordinates.

Offline and fresh-extracted developer-package checks pass. Actual dev.4 KSP
visual and gameplay testing remains pending. No install, save modification,
GitHub commit, tag or release performed. Latest GitHub import remains the
previously verified v0.6.0-dev.1 commit unless separately checked/updated.
