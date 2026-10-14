# v0.10.0-dev.1 — RW-ADP-250-375 station adapter

User requested a 2.5 to 3.75 adapter. New ninth part is a crewless structural
transition, 1.8 m long, small size-2 interface at +0.9 m and large size-3
interface at -0.9 m. Candidate balance: 1.1 t, 4200 funds, advMetalworks,
Structural category. These balance/length choices are implementation decisions.
Tapered ivory panels, graphite seams, bronze trim, conformal readable badges,
reinforcing spines, paired service lines and both closed recessed endcaps match
the original family. Large cap is enlarged radially 1.5 times; axial recess
depth is preserved and normals receive inverse-transpose radial scaling.

Native MU contains 16356 visual triangles and three closed convex 96-triangle
colliders following the large collar, taper and small collar. Stack nodes are
attachment nodes, not docking ports. Stock crossfeed and surface attachment
are enabled. No crew, IVA, EVA, resource storage, generator or Habitat module.
No special Kerbalism patch is required for this passive structural part.

All eight prior modules' GameData except package version is byte-identical to
v0.9.0-dev.1, enforced by Tools/adapter_baseline.json. PWR remains a candidate
awaiting in-game feedback. AIR was previously reported working by the user.
Native geometry, procedural Python, OBJ/MTL, new label PNG and optional Blender
reconstruction are included; Blender was not executed. Preview reads actual
exported MU/textures with Unity camera orientation, not an in-game screenshot.

Build adapter: python Tools/build_adapter.py. Rebuild family:
python Tools/build_appearance.py. Validate: python Tools/validate.py.
Preview: python Tools/render_adapter.py. Package: python Tools/package_appearance.py.
Offline and package checks must pass before delivery. In-game stack fit,
appearance, radial attachments and save/load testing remain pending; see
ADAPTER_TEST_CHECKLIST.md. No installation, GitHub commit, tag or release.
