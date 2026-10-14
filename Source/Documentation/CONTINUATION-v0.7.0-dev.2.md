# v0.7.0-dev.2 — Six-module exterior detail pass

User requested inspection and appearance refinement of every model, seeking a
more advanced detailed family of modules and textures. Built additively from
the supplied v0.7.0-dev.1 source ZIP, SHA256
6c32a40b429d2d0972bd2b847ea3c0fd7f41954866ac52652a1434318178ae74.

All six native models receive original cosmetic details. Shared hull cladding
uses dedicated textures so dense cover/stencil art does not repeat on narrow
window frames. Shared endcaps gain a continuous outer skirt, seam rings,
fasteners and recessed circuit plates. HAB life-support covers, LAB manifold and
cooling fins, CMD avionics, HUB shoulder service looms, CUP optical diagnostics,
and LOG cassette IDs/supply covers remain cosmetic. Fixed LOG shoulder backing
coplanarity and HAB/LAB/CMD nameplate UV mirroring. Original glass geometry,
warm-white emissive PNG, rooster crest, all colliders/triggers, HAB visual
variants, part configurations, Kerbalism patches and runtime binary preserved.

New canonical build: `python Tools/build_appearance.py` (Pillow + NumPy).
Use this entry point; legacy individual main routines regenerate older texture
styles. Current procedural geometry functions and Blender reconstruction scripts
include the detail pass. HUB now has its own optional Blender reconstruction.
Blender scripts were not executed in this environment; editable OBJ/MTL assets
were regenerated alongside all six native .mu models and both HAB variants.

Validation: `python Tools/validate.py`, including native-baseline regression;
render: `python Tools/render_appearance.py`; package:
`python Tools/package_appearance.py`. CPU renders read actual exported MU data
and shipped textures, with supersampling and diffuse studio lighting. They do
not establish KSP runtime appearance. Old Media renders are historical and
retained for provenance/legacy validations; latest previews have dev.2 names.

All checks passed before packaging. Inspect APPEARANCE_TEST_CHECKLIST.md in KSP
before accepting visuals. No installation, GitHub commit, tag or release occurred.
Latest accepted shapes/gameplay baseline remains the prior user-approved work;
the appearance candidate has not yet received user visual acceptance.
