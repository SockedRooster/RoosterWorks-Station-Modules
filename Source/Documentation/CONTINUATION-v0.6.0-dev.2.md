# RoosterWorks Station Modules handoff — v0.6.0-dev.2

This source ZIP contains v0.6.0-dev.1 plus a **cupola-only** exterior mesh refinement.
The VAB user screenshot showed light leaking through joints between the original eight canopy mullions and separately modeled header arcs. v0.6.0-dev.2 fixes this in `Source/build_cup250.py` by replacing the header arcs with 360° conical header rings; eight full-height seam-centred graphite foundations with 0.015 radian overlap to neighboring glazing, steel/bronze/ceramic ribs; and thicker lower retaining belt plus roof fastener details. Interior inset shadow strips run around window borders only and do not block window centres.

Native model `.mu`, source OBJ, three renders and regression validator were regenerated. Glass dimensions, stack node, one seat, stock IVA, textures, optional Kerbalism resources and other four modules are not changed. `RoosterWorksStationModules.version` BUILD=2. Offline tests pass, KSP appearance/lighting/crew and Kerbalism still require user verification.

Full developer source includes `Source/build_cup250.py`, `Tools/render_cup250.py`, `Tools/validate_cup250.py`. Rebuild with `python Source/build_cup250.py`, render with `python Tools/render_cup250.py` (NumPy + VTK), then `python Tools/validate.py` (Pillow). Do not prematurely publish as stable, especially while v0.5.3 hub/endcap flight acceptance remains pending. The repository was imported to GitHub at v0.6.0-dev.1; only push dev.2 after user requests it.
